"""
geometric_independence.py (Improvement #3) — a GENUINELY distinct geometric lens.

The redundancy corr(R, T) = 0.97 arose because the geometric coordinate T was
defined from the participation ratio PR = N^2 / sum(lambda^2) — a *function of the
eigenvalues*, so really a second SPECTRAL measure. We replace it with a coordinate
that is NOT eigenvalue-based: the persistent-homology (H1) signal of the
correlation-distance point cloud (topology / connectivity, not variance).

Two tests:
  (A) CORRELATION with the spectral coordinate R (is it still redundant?).
  (B) ABLATION — does adding the true topological feature give crash-warning
      information the spectral lens alone does not? (Correlation alone is weak
      evidence; unique predictive contribution is stronger.)

NOTE ON LANGUAGE: a correlation near -0.37 is NOT statistical independence. We say
"weakly-to-moderately correlated / complementary / captures distinct information."
"""

import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser
from itertools import combinations

W, BENCH = 60, "^NSEI"
TICKERS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
           "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
           "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS"]


def auc(score, label):
    s = np.asarray(score, float); y = np.asarray(label, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    pos, neg = (y == 1), (y == 0)
    if pos.sum() == 0 or neg.sum() == 0: return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    a = (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum())
    return max(a, 1 - a)


def build():
    px = yf.download(TICKERS + [BENCH], start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.9]
    px = px[good + [BENCH]].dropna()
    R_ = px[good].pct_change().dropna().values
    bench = px[BENCH].pct_change().dropna()
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R_)):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
        R = vals[-1] / N
        PR = (vals.sum() ** 2) / np.sum(vals ** 2)
        T_pr = 1 - PR / N
        D = np.sqrt(2 * (1 - C)); np.fill_diagonal(D, 0.0)
        dgm = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
        life = (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.array([])
        life = life[np.isfinite(life)]
        T_tda = float(np.sqrt(np.sum(life ** 2))) if len(life) else 0.0
        idx = win.mean(axis=1); sq = idx ** 2
        H = np.corrcoef(sq[:-1], sq[1:])[0, 1] if len(sq) > 2 else 0.0
        rows.append((dates[e], R, T_pr, T_tda, H))
    df = pd.DataFrame(rows, columns=["date","R","T_pr","T_tda","H"]).set_index("date").fillna(0)
    return df, bench


def run():
    print("Computing spectral R, participation-ratio proxy, true H1 topology, temporal H ...")
    df, bench = build()

    print("\n=== (A) Correlation with the spectral coordinate R ===")
    for col, label in [("T_pr", "participation-ratio proxy (eigenvalue-based)"),
                       ("T_tda", "persistent homology H1 (true topology)")]:
        c = df["R"].corr(df[col])
        tag = ("REDUNDANT (near-perfect)" if abs(c) > 0.6
               else "weak-to-moderate; complementary")
        print(f"  corr(R, {label:44s}) = {c:+.2f}   [{tag}]")
    print("  (Note: -0.37 is NOT statistical independence — it means the topological")
    print("   summary is only weakly-to-moderately correlated with the spectrum, i.e.")
    print("   it carries information that is not merely a restatement of the eigenvalues.)")

    # ablation
    fwd = bench.shift(-1).rolling(20).sum().shift(-19)
    df["crash"] = (fwd < -0.10).astype(int).reindex(df.index)
    df = df.dropna(); y = df["crash"].values
    z = lambda s: (s - s.mean()) / s.std()
    print("\n=== (B) ABLATION: does the TRUE topological lens add unique crash-warning info? ===")
    print("    (geometric coordinate = persistent homology, not the proxy)")
    for k in range(1, 4):
        for combo in combinations([("R","spectral"),("T_tda","geometric"),("H","temporal")], k):
            score = sum(z(df[c]) for c, _ in combo)
            names = "+".join(n for _, n in combo)
            print(f"    {names:26s}: AUC {auc(score, y):.3f}")
    a_r = auc(df["R"], y)
    a_rt = auc(z(df["R"]) + z(df["T_tda"]), y)
    print(f"\n  spectral alone = {a_r:.3f};  spectral + true-topology = {a_rt:.3f}  "
          f"({'topology adds unique info' if a_rt > a_r + 0.005 else 'little unique lift here'})")
    print("\nHonest wording for the paper: the three coordinates are 'weakly-to-moderately")
    print("correlated and complementary', each capturing distinct information — NOT")
    print("'statistically independent' (which -0.37 does not establish).")


if __name__ == "__main__":
    run()
