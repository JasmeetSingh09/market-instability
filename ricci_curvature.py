"""
ricci_curvature.py — discrete Ollivier-Ricci curvature as an alternative geometric
lens (theory in RICCI_CURVATURE.md). We compute average network curvature per window
and ask three honest questions:

  (A) corr with the spectral coordinate R (is curvature just the market mode again?)
  (B) does average curvature RISE before crashes? (Sandhu et al.'s hypothesis)
  (C) ABLATION: does curvature add crash-warning AUC over spectral alone —
      i.e. does it succeed where the persistent-homology geometric lens (AUC ~0.53,
      no lift) failed?

Ollivier-Ricci: kappa(x,y) = 1 - W1(m_x, m_y)/d(x,y), with m_x a lazy random walk
on correlation-weighted neighbours and W1 the earth-mover distance (solved exactly
as a transportation LP via scipy.optimize.linprog). Weekly step (5 trading days)
keeps the LP count tractable.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import linprog

W, BENCH, STEP, ALPHA = 60, "^NSEI", 5, 0.5
TICKERS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
           "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
           "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS"]
rng = np.random.default_rng(0)


def auc(score, label):
    s = np.asarray(score, float); y = np.asarray(label, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    if y.sum() == 0 or y.sum() == len(y): return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    pos = (y == 1)
    a = (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (len(y) - pos.sum()))
    return max(a, 1 - a)


def _make_eq(n):
    """marginal-constraint matrix for an n->n transport LP (built once)."""
    A = np.zeros((2 * n, n * n))
    for i in range(n):
        A[i, i * n:(i + 1) * n] = 1          # row (source) marginals
        A[n + i, i::n] = 1                    # col (target) marginals
    return A


def w1(a, b, C, A_eq):
    res = linprog(C.ravel(), A_eq=A_eq, b_eq=np.concatenate([a, b]),
                  bounds=(0, None), method="highs")
    return res.fun if res.success else np.nan


def curvature(Cmat):
    """average Ollivier-Ricci curvature of the correlation network."""
    n = Cmat.shape[0]
    d = np.sqrt(np.clip(2 * (1 - Cmat), 0, None)); np.fill_diagonal(d, 0.0)
    s = np.clip(Cmat, 0, None); np.fill_diagonal(s, 0.0)     # positive-corr weights
    # lazy-random-walk distributions m_x (one per node)
    M = np.zeros((n, n))
    for x in range(n):
        tot = s[x].sum()
        M[x] = (1 - ALPHA) * s[x] / tot if tot > 0 else 0.0
        M[x, x] += ALPHA
    A_eq = _make_eq(n)
    ks, ws = [], []
    for x in range(n):
        for y in range(x + 1, n):
            if d[x, y] <= 0:
                continue
            wd = w1(M[x], M[y], d, A_eq)
            if np.isfinite(wd):
                ks.append(1 - wd / d[x, y]); ws.append(s[x, y])
    ks, ws = np.array(ks), np.array(ws)
    return float(np.average(ks, weights=ws)) if len(ks) and ws.sum() > 0 else np.nan


def build():
    px = yf.download(TICKERS + [BENCH], start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.9]
    px = px[good + [BENCH]].dropna()
    R_ = px[good].pct_change().dropna().values
    bench = px[BENCH].pct_change().dropna()
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R_), STEP):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]
        R = vals[-1] / len(vals)
        kap = curvature(C)
        rows.append((dates[e], R, kap))
    df = pd.DataFrame(rows, columns=["date","R","ricci"]).set_index("date").dropna()
    fwd = bench.shift(-1).rolling(20).sum().shift(-19)
    df["crash"] = (fwd.reindex(df.index) < -0.10).astype(float)
    return df.dropna()


def gap_ci(sig, crash, B=2000):
    pre, base = sig[crash == 1], sig[crash == 0]
    if len(pre) == 0: return np.nan, np.nan, np.nan
    obs = pre.mean() - base.mean()
    boot = [rng.choice(pre, len(pre)).mean() - rng.choice(base, len(base)).mean() for _ in range(B)]
    return obs, np.percentile(boot, 2.5), np.percentile(boot, 97.5)


def run():
    print("Computing Ollivier-Ricci curvature per window (this takes a few minutes)...")
    df = build()
    y = df["crash"].values
    print(f"windows: {len(df)}  pre-crash: {int(y.sum())}  "
          f"mean curvature: {df['ricci'].mean():+.3f}\n")

    print("=== (A) Is curvature just the spectral market mode again? ===")
    print(f"  corr(Ricci curvature, R) = {df['ricci'].corr(df['R']):+.2f}")

    print("\n=== (B) Does curvature RISE before crashes? (Sandhu et al. hypothesis) ===")
    o, lo, hi = gap_ci(df["ricci"].values, y)
    sig = "SIGNIFICANT" if (lo > 0 or hi < 0) else "not significant"
    print(f"  pre-crash − baseline curvature = {o:+.4f}  95% CI [{lo:+.4f},{hi:+.4f}]  [{sig}]")

    print("\n=== (C) Ablation: does curvature add crash-warning info over spectral? ===")
    z = lambda s: (s - s.mean()) / s.std()
    a_r = auc(df["R"], y)
    a_k = auc(df["ricci"], y)
    a_rk = auc(z(df["R"]) + np.sign(df['ricci'].corr(df['R'])) * -z(df["ricci"]), y)
    print(f"  spectral R only            : AUC {a_r:.3f}")
    print(f"  Ricci curvature only       : AUC {a_k:.3f}")
    print(f"  spectral + curvature       : AUC {a_rk:.3f}")
    print(f"\n  (compare: persistent-homology geometric lens gave AUC ~0.53 and NO lift)")
    print(f"  curvature { 'ADDS' if a_rk > a_r + 0.01 else 'does NOT add' } "
          f"unique crash-warning value over spectral alone.")


if __name__ == "__main__":
    run()
