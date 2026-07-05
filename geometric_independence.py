"""
geometric_independence.py (Improvement #3) — is there a GENUINELY independent
geometric lens?

The redundancy corr(R, T) = 0.97 arose because the geometric coordinate T was
defined from the participation ratio PR = N^2 / sum(lambda^2) — i.e. it is a
*function of the eigenvalues*, so it is really a second SPECTRAL measure, not a
topological one. Naturally it tracks R.

Here we test a coordinate that is NOT a function of the eigenvalue spectrum: the
persistent-homology (H1) signal from the correlation-distance point cloud. Loops
in that space encode connectivity, not variance concentration. If this genuinely
topological measure is markedly LESS correlated with R than the participation-
ratio proxy, then the geometric lens can be made genuinely independent.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser

W, BENCH = 60, "^NSEI"
TICKERS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
           "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
           "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS"]


def build():
    px = yf.download(TICKERS + [BENCH], start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.9]
    px = px[good + [BENCH]].dropna()
    R_ = px[good].pct_change().dropna().values
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R_)):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
        # SPECTRAL R and the (eigenvalue-based) participation-ratio proxy T_pr
        R = vals[-1] / N
        PR = (vals.sum() ** 2) / np.sum(vals ** 2)
        T_pr = 1 - PR / N
        # GENUINELY GEOMETRIC: persistent homology (H1) of the correlation distance
        D = np.sqrt(2 * (1 - C)); np.fill_diagonal(D, 0.0)
        dgm = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
        life = (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.array([])
        life = life[np.isfinite(life)]
        T_tda = float(np.sqrt(np.sum(life ** 2))) if len(life) else 0.0     # H1 L2 norm
        # persistent entropy (another topological summary)
        if len(life) and life.sum() > 0:
            p = life / life.sum(); ent = float(-np.sum(p * np.log(p + 1e-12)))
        else:
            ent = 0.0
        rows.append((dates[e], R, T_pr, T_tda, ent))
    return pd.DataFrame(rows, columns=["date","R","T_pr","T_tda","T_entropy"]).set_index("date")


def run():
    print("Computing spectral R, the participation-ratio proxy, and true H1 topology ...")
    df = build()
    print("\n=== Correlation with the spectral coordinate R ===")
    for col, label in [("T_pr", "participation-ratio proxy (eigenvalue-based)"),
                       ("T_tda", "persistent homology H1 norm (true topology)"),
                       ("T_entropy", "persistent entropy (true topology)")]:
        c = df["R"].corr(df[col])
        tag = "REDUNDANT" if abs(c) > 0.6 else "≈ INDEPENDENT" if abs(c) < 0.4 else "partial"
        print(f"  corr(R, {label:44s}) = {c:+.2f}   [{tag}]")

    print("\nVerdict:")
    c_pr, c_tda = abs(df['R'].corr(df['T_pr'])), abs(df['R'].corr(df['T_tda']))
    if c_tda < c_pr - 0.2:
        print("  The TRUE topological coordinate is markedly less correlated with R than")
        print("  the participation-ratio proxy -> a genuinely INDEPENDENT geometric lens")
        print("  exists. Recommendation: use persistent homology (not the PR proxy) as the")
        print("  geometric coordinate; the three lenses then measure three distinct things.")
    else:
        print("  Even the true topological coordinate tracks R substantially -> on daily")
        print("  correlation structure, geometric collapse and market-mode dominance are")
        print("  hard to separate. That itself is an honest, reportable finding.")


if __name__ == "__main__":
    run()
