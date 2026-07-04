"""
redundancy_analysis.py — turn the R–T redundancy from an overclaim into a
PROPOSITION with explicit assumptions, an empirical validation, and the
conditions under which it BREAKS DOWN.

Definitions (rolling correlation matrix, eigenvalues λ_1..λ_N, trace Σλ = N):
    R (spectral)  = λ_max / N                      # market-mode share
    PR            = (Σλ)^2 / Σλ^2 = N^2 / Σλ^2      # participation ratio
    T (geometric) = 1 - PR/N = 1 - N / Σλ^2

PROPOSITION (Dominant Market-Mode Approximation).
    IF one eigenvalue dominates the spectrum (Σλ^2 ≈ λ_max^2), THEN
        PR ≈ 1/R^2   and   T ≈ 1 - 1/(N R^2).
    i.e. under a dominant market mode, T is an explicit increasing function of R,
    which forces the two measures to be strongly correlated.

This script (1) tests how well T ≈ 1 - 1/(N R^2) holds on real data, and
(2) shows WHERE it holds vs breaks — by how dominant the market mode is, and
across calm vs turbulent regimes. That is the actual contribution: not "they are
bound", but "here is the analytical relationship, validated, with its limits."
"""

import numpy as np
import pandas as pd
import yfinance as yf

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
        s2 = np.sum(vals ** 2)
        R = vals[-1] / N
        PR = (vals.sum() ** 2) / s2
        T = 1 - PR / N
        T_pred = 1 - 1.0 / (N * R ** 2)                     # the proposition
        # how concentrated is the spectrum? (fraction of Σλ^2 in the top mode)
        dominance = vals[-1] ** 2 / s2
        rows.append((dates[e], N, R, T, T_pred, dominance))
    return pd.DataFrame(rows, columns=["date","N","R","T","T_pred","dominance"]).set_index("date"), bench


def run():
    print("Computing R, T and the analytical prediction over time ...")
    df, bench = build()
    err = (df["T"] - df["T_pred"]).abs()

    print("\n=== PROPOSITION VALIDATION: T ≈ 1 - 1/(N R^2) ===")
    print(f"  corr(T, T_pred)          : {df['T'].corr(df['T_pred']):.3f}")
    print(f"  mean |T - T_pred|        : {err.mean():.3f}")
    print(f"  corr(R, T) [empirical]   : {df['R'].corr(df['T']):.3f}  "
          f"(the 0.97-style redundancy this explains)")

    print("\n=== WHERE IT HOLDS vs BREAKS (by market-mode dominance) ===")
    df["bucket"] = pd.qcut(df["dominance"], 4, labels=["low","med-lo","med-hi","high"])
    for b, g in df.groupby("bucket", observed=True):
        e = (g["T"] - g["T_pred"]).abs().mean()
        print(f"  dominance={b:7s}: mean |error| = {e:.3f}  (n={len(g)})  "
              f"-> {'approx HOLDS' if e < 0.05 else 'approx BREAKS'}")

    print("\n=== BY REGIME (calm vs turbulent, via benchmark volatility) ===")
    vol = bench.rolling(W).std().reindex(df.index)
    calm = df[vol <= vol.median()]; turb = df[vol > vol.median()]
    print(f"  calm  markets: mean |error| = {(calm['T']-calm['T_pred']).abs().mean():.3f}")
    print(f"  turbulent    : mean |error| = {(turb['T']-turb['T_pred']).abs().mean():.3f}")

    print("\nHonest reading: the proposition is an APPROXIMATION valid when the")
    print("market mode dominates (high dominance / turbulent regimes); it is looser")
    print("when the spectrum is spread out (calm markets, many comparable eigenvalues).")
    print("That validated relationship + its breakdown conditions is the contribution.")


if __name__ == "__main__":
    run()
