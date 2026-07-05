"""
geometric_role.py — what DOES the topological lens contribute, if not crash lift?

The ablation showed the true persistent-homology coordinate adds little UNIQUE
crash-PREDICTION value over the spectral lens. Fair reviewer point: then give it a
scientific ROLE beyond prediction. We test one concrete, falsifiable claim:

  "Conditional on the SAME spectral signature R, does topology T_tda separate
   market states that go on to behave differently?"

If two windows look identical to the spectral lens (same R bin) but differ in
topology, and their FORWARD behaviour differs, then topology carries regime
information the spectrum does not — a purpose beyond crash timing.

Tests:
  (1) Matched-spectral separation: within R quintiles, split by median T_tda and
      compare forward 20-day realized vol and forward max drawdown.
  (2) Partial correlation: corr(T_tda, forward outcome) after removing R.
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
    bench = px[BENCH].pct_change().dropna()
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R_)):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
        R = vals[-1] / N
        D = np.sqrt(2 * (1 - C)); np.fill_diagonal(D, 0.0)
        dgm = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
        life = (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.array([])
        life = life[np.isfinite(life)]
        T_tda = float(np.sqrt(np.sum(life ** 2))) if len(life) else 0.0
        rows.append((dates[e], R, T_tda))
    df = pd.DataFrame(rows, columns=["date","R","T_tda"]).set_index("date")
    # forward outcomes (character of what comes next)
    fvol = bench.rolling(20).std().shift(-20) * np.sqrt(252)
    fdd = bench.shift(-1).rolling(20).apply(
        lambda x: (np.cumprod(1+x) / np.maximum.accumulate(np.cumprod(1+x)) - 1).min(), raw=True)
    df["fwd_vol"] = fvol.reindex(df.index)
    df["fwd_dd"] = fdd.reindex(df.index)
    return df.dropna()


def partial_corr(x, y, z):
    # corr(x, y) controlling for z
    def resid(a, b):
        b1 = np.c_[np.ones_like(b), b]
        return a - b1 @ np.linalg.lstsq(b1, a, rcond=None)[0]
    rx, ry = resid(x, z), resid(y, z)
    return np.corrcoef(rx, ry)[0, 1]


def run():
    print("Computing spectral R, true topology T_tda, and forward behaviour ...")
    df = build()
    R, T = df["R"].values, df["T_tda"].values

    print("\n=== (1) Matched-spectral separation (same R quintile, split by topology) ===")
    print("    Within each spectral quintile, do high- vs low-topology states differ")
    print("    in what comes NEXT? (forward 20d vol, forward drawdown)\n")
    df["Rq"] = pd.qcut(df["R"], 5, labels=False)
    print(f"    {'R quintile':>11} {'fwd vol: loT':>13} {'fwd vol: hiT':>13} "
          f"{'fwd dd: loT':>12} {'fwd dd: hiT':>12}")
    for q in range(5):
        g = df[df["Rq"] == q]
        med = g["T_tda"].median()
        lo, hi = g[g["T_tda"] <= med], g[g["T_tda"] > med]
        print(f"    {q+1:>11} {lo['fwd_vol'].mean():>13.3f} {hi['fwd_vol'].mean():>13.3f} "
              f"{lo['fwd_dd'].mean():>12.3f} {hi['fwd_dd'].mean():>12.3f}")

    print("\n=== (2) Partial correlation: topology vs forward outcome, controlling for R ===")
    pv = partial_corr(T, df["fwd_vol"].values, R)
    pd_ = partial_corr(T, df["fwd_dd"].values, R)
    print(f"    corr(T_tda, forward vol | R)      = {pv:+.2f}")
    print(f"    corr(T_tda, forward drawdown | R) = {pd_:+.2f}")
    print("\n  Interpretation: a non-trivial partial correlation means topology carries")
    print("  information about the CHARACTER of the coming regime (how volatile / how")
    print("  deep a drawdown) that is NOT already in the spectral coordinate — a role")
    print("  beyond crash timing. A near-zero value would mean topology adds little even")
    print("  here, and we should say so plainly.")


if __name__ == "__main__":
    run()
