"""
crisis_trajectories.py — the second-discovery experiment (see DISCOVERY_AND_PLAN.md).

Question (the reviewer's strongest remaining opportunity):
    "Does every crash follow the same path through Fragility Space?"

For five historical U.S.-equity crises we trace the fragility coordinates
F = (R, T, H) through the run-up to each onset, aligned by event time and z-scored on
each crisis's own pre-window so the shapes are comparable. Then we ask:
  (1) Do the trajectories look alike (a common path) or differ (classes of crises)?
  (2) Which lens moves FIRST — spectral, structural, or temporal?

We commit to reporting whichever answer the data gives.

Coordinates (cheap, fast):
  R = lambda_max/N (spectral)   T = 1 - PR/N (effective-rank)   H = lag-1 autocorr of
  squared equal-weight returns (temporal self-excitation proxy).
"""

import numpy as np
import pandas as pd
import yfinance as yf

W = 60
# large caps with history back to the late 1990s
TICKERS = ["AAPL","MSFT","JNJ","PG","JPM","XOM","WMT","KO","IBM","GE",
           "INTC","CSCO","MRK","PFE","HD"]
CRISES = {                       # onset dates (approx.)
    "Dot-com 2000":  "2000-09-01",
    "GFC 2008":      "2008-09-15",
    "Euro/2011":     "2011-08-01",
    "COVID 2020":    "2020-02-20",
    "2022 selloff":  "2022-01-04",
}
PRE, POST = 70, 15               # trading days around onset


def coords(win, mkt_win):
    C = np.clip(np.corrcoef(win.T), -1, 1)
    vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
    R = vals[-1] / N
    T = 1 - (N * N / np.sum(vals ** 2)) / N
    sq = mkt_win ** 2
    H = np.corrcoef(sq[:-1], sq[1:])[0, 1] if len(sq) > 2 else 0.0
    return R, T, H


def trajectory(px, onset):
    """Return a DataFrame indexed by days-relative-to-onset with (R,T,H)."""
    rets = px.pct_change().dropna()
    mkt = rets.mean(axis=1).values
    Rv = rets.values
    dates = rets.index
    o = dates.searchsorted(pd.Timestamp(onset))
    rows = []
    for e in range(o - PRE, o + POST):
        if e - W < 0 or e >= len(Rv):
            continue
        R, T, H = coords(Rv[e - W:e], mkt[e - W:e])
        rows.append((e - o, R, T, H))
    df = pd.DataFrame(rows, columns=["rel","R","T","H"]).set_index("rel")
    # z-score each coordinate on this crisis's own pre-onset window (rel < 0)
    pre = df[df.index < 0]
    for c in ["R","T","H"]:
        mu, sd = pre[c].mean(), pre[c].std() + 1e-9
        df[c] = (df[c] - mu) / sd
    return df


def first_crossing(series, thr=1.0):
    """rel-day at which a z-scored coordinate first exceeds thr before onset."""
    pre = series[series.index <= 0]
    hit = pre[pre > thr]
    return int(hit.index[0]) if len(hit) else None


def run():
    print("Downloading long-history large caps (this pulls ~25 years)...")
    px = yf.download(TICKERS, start="1998-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    px = px.dropna(how="all")
    trajs = {}
    print("\n=== Which lens moves first? (rel-day it first exceeds +1 sigma before onset) ===")
    print(f"{'Crisis':>14} | {'R (spectral)':>12} {'T (structural)':>14} {'H (temporal)':>12} | first mover")
    for name, onset in CRISES.items():
        cols = [t for t in TICKERS if t in px and px[t].loc[:onset].notna().mean() > 0.8]
        sub = px[cols].loc[:pd.Timestamp(onset) + pd.Timedelta(days=40)].dropna()
        if len(sub) < W + PRE:
            print(f"{name:>14} | insufficient history"); continue
        df = trajectory(sub, onset)
        trajs[name] = df
        fr = {c: first_crossing(df[c]) for c in ["R","T","H"]}
        order = sorted([c for c in fr if fr[c] is not None], key=lambda c: fr[c])
        first = {"R":"spectral","T":"structural","H":"temporal"}.get(order[0], "—") if order else "none"
        fmt = lambda v: f"{v:>+4}d" if v is not None else "  — "
        print(f"{name:>14} | {fmt(fr['R']):>12} {fmt(fr['T']):>14} {fmt(fr['H']):>12} | {first}")

    # (1) common path? correlate the (R,T,H) trajectories pairwise across crises
    print("\n=== Do crises follow a COMMON path? (avg pairwise trajectory correlation) ===")
    names = list(trajs)
    for c in ["R","T","H"]:
        mat = pd.DataFrame({n: trajs[n][c] for n in names}).dropna()
        if mat.shape[1] < 2:
            continue
        corr = mat.corr().values
        avg = (corr.sum() - len(names)) / (len(names) * (len(names) - 1))
        tag = "similar across crises" if avg > 0.4 else "heterogeneous (classes of crises?)"
        print(f"  {c}: avg pairwise trajectory corr = {avg:+.2f}   [{tag}]")

    print("\nReading: if one lens consistently crosses +1 sigma FIRST, that is a staged")
    print("signature (a discovery about HOW fragility builds). If trajectory correlations")
    print("are high, crises share a common path; if low, there are distinct classes of")
    print("crises — either is a genuine, reportable finding.")


if __name__ == "__main__":
    run()
