"""
rq_a_regime_divergence.py — pre-registered RQ-A (see DISCOVERY_AND_PLAN.md).

Question: do the spectral coordinate R and the TRUE persistent-homology topological
coordinate diverge in calm markets and converge in crises?

Hypothesis: in calm regimes spectral (correlation-dominated) and topological (local
structure) measures track different things (low agreement); as stress rises and the
market synchronizes, both saturate and agree more.

We commit to reporting WHICHEVER outcome occurs, including the null. Regimes are split
by realized-volatility terciles so the split is not chosen to flatter the result.
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
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]
        R = vals[-1] / len(vals)
        D = np.sqrt(2 * (1 - C)); np.fill_diagonal(D, 0.0)
        dgm = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
        life = (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.array([])
        life = life[np.isfinite(life)]
        T = float(np.sqrt(np.sum(life ** 2))) if len(life) else 0.0
        vol = win.mean(axis=1).std() * np.sqrt(252)   # realized vol of the index proxy
        rows.append((dates[e], R, T, vol))
    return pd.DataFrame(rows, columns=["date","R","T","vol"]).set_index("date")


def run():
    print("Computing R and true persistent-homology T over rolling windows ...")
    df = build()
    # regime split by realized-vol terciles (data-driven, not hand-picked)
    q1, q2 = df["vol"].quantile([1/3, 2/3])
    df["regime"] = np.where(df["vol"] <= q1, "calm",
                    np.where(df["vol"] <= q2, "stressed", "crisis"))

    print(f"\nwindows: {len(df)}  (vol terciles at {q1:.2%}, {q2:.2%})\n")
    print("=== corr(R, true-topology T) within each regime ===")
    overall = df["R"].corr(df["T"])
    print(f"  overall                : {overall:+.2f}")
    for reg in ["calm", "stressed", "crisis"]:
        g = df[df["regime"] == reg]
        c = g["R"].corr(g["T"])
        print(f"  {reg:8s} (n={len(g):4d}) : corr = {c:+.2f}   mean R={g['R'].mean():.3f}  mean T={g['T'].mean():.2f}")

    calm_c   = df[df.regime=="calm"]["R"].corr(df[df.regime=="calm"]["T"])
    crisis_c = df[df.regime=="crisis"]["R"].corr(df[df.regime=="crisis"]["T"])
    print("\n=== Pre-registered outcome read (report whichever) ===")
    if abs(crisis_c) > abs(calm_c) + 0.1:
        print("  -> They agree MORE in crises than calm (converge under stress) — supports the hypothesis.")
    elif abs(calm_c) > abs(crisis_c) + 0.1:
        print("  -> They agree MORE in calm than crisis — OPPOSITE of the hypothesis (report honestly).")
    else:
        print("  -> No clear regime dependence in their agreement — NULL result (report honestly).")
    print("\n  (This directly tests the discovery: if spectral & topology only align under")
    print("   stress, the 'redundancy' is a crisis phenomenon, and topology carries distinct")
    print("   information in calm markets — a precise, testable refinement.)")


if __name__ == "__main__":
    run()
