"""
fragility_space.py — ablation + fragility-space geometry + benchmark battery.

Implements the stronger framing: treat the three lenses as ORTHOGONAL DIMENSIONS
of fragility, F = (R, T, H), rather than a hand-weighted score. We then:

  1. ABLATION: every subset of {spectral R, geometric T, temporal H} -> crash-
     warning AUC with bootstrap 95% CI. Quantifies what each lens adds.
  2. FRAGILITY-SPACE model: a logistic classifier on all 3 dimensions, evaluated
     with time-series cross-validation (does the *geometry* separate crashes?).
  3. BENCHMARK battery: volatility, rolling average correlation, trailing
     drawdown — the standard risk measures the SFI must beat to matter.

Honest framing: the goal is to CHARACTERISE fragility, not to claim crash
prediction. Verdicts are reported with CIs, no cherry-picking.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from itertools import combinations
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(0)
W, BENCH = 60, "^NSEI"
TICKERS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
           "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
           "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS"]


def auc(s, y):
    s = np.asarray(s, float); y = np.asarray(y, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    pos, neg = (y == 1), (y == 0)
    if pos.sum() == 0 or neg.sum() == 0: return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    a = (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum())
    return max(a, 1 - a)   # orient so higher-is-crash


def boot_auc(s, y, n_boot=600, block=21):
    s = np.asarray(s, float); y = np.asarray(y, int)
    n = len(y); nb = int(np.ceil(n / block)); out = []
    for _ in range(n_boot):
        st = rng.integers(0, max(1, n - block), nb)
        idx = np.concatenate([np.arange(k, k + block) for k in st])[:n]
        out.append(auc(s[idx], y[idx]))
    return np.nanpercentile(out, [2.5, 97.5])


def build():
    px = yf.download(TICKERS + [BENCH], start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.9]
    px = px[good + [BENCH]].dropna()
    R = px[good].pct_change().dropna().values
    bench = px[BENCH].pct_change().dropna()
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R)):
        win = R[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
        spectral = vals[-1] / N
        pr = (vals.sum() ** 2) / np.sum(vals ** 2)
        geometric = 1 - pr / N
        idx = win.mean(axis=1); sq = idx ** 2
        temporal = np.corrcoef(sq[:-1], sq[1:])[0, 1] if len(sq) > 2 else 0.0
        avg_corr = (C.sum() - N) / (N * (N - 1))
        rows.append((dates[e], spectral, geometric, temporal, avg_corr))
    df = pd.DataFrame(rows, columns=["date","R","T","H","avg_corr"]).set_index("date").fillna(0)
    df["vol"] = bench.rolling(W).std().reindex(df.index)
    cum = (1 + bench).cumprod()
    df["drawdown"] = (cum / cum.cummax() - 1).reindex(df.index)
    fwd = bench.shift(-1).rolling(20).sum().shift(-19)
    df["crash"] = (fwd < -0.10).astype(int).reindex(df.index)
    return df.dropna()


def z(s): return (s - s.mean()) / s.std()


def run():
    print("Building fragility space (fast — eigenvalues only, no persistence) ...")
    df = build()
    y = df["crash"].values
    names = {"R": "spectral", "T": "geometric", "H": "temporal"}

    print("\n=== ABLATION: crash-warning AUC by lens combination (with 95% CI) ===")
    for k in range(1, 4):
        for combo in combinations(["R","T","H"], k):
            score = sum(z(df[c]) for c in combo)
            a = auc(score, y); lo, hi = boot_auc(score, y)
            print(f"  {'+'.join(combo):8s} : AUC {a:.3f}  [{lo:.3f},{hi:.3f}]")

    print("\n=== FRAGILITY-SPACE model (logistic on R,T,H, time-series CV) ===")
    X = df[["R","T","H"]].values
    aucs = []
    for tr, te in TimeSeriesSplit(n_splits=5).split(X):
        if y[tr].sum() == 0 or y[te].sum() == 0: continue
        clf = LogisticRegression(max_iter=1000).fit(X[tr], y[tr])
        aucs.append(roc_auc_score(y[te], clf.predict_proba(X[te])[:, 1]))
    print(f"  cross-validated AUC = {np.mean(aucs):.3f} (std {np.std(aucs):.3f})")

    print("\n=== BENCHMARK battery (standard risk measures) ===")
    for b in ["vol","avg_corr","drawdown"]:
        a = auc(df[b], y); lo, hi = boot_auc(df[b], y)
        print(f"  {b:9s}: AUC {a:.3f}  [{lo:.3f},{hi:.3f}]")

    print("\nHonest read: compare the 'R+T+H' ablation and the CV model against the")
    print("benchmark battery. Overlapping CIs = no significant edge. NOTE: 2010-2024")
    print("excludes 2008, so the volatility benchmark is weaker here than on a fair,")
    print("2008-inclusive sample — interpret cross-market, not just this window.")


if __name__ == "__main__":
    run()
