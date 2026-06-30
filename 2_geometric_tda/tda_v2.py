"""
TDA v2 — the PRINCIPLED construction (giving topology its strongest shot).

Instead of a thin point cloud of a few stocks, we study the topology of the
market's *correlation structure*:

  * ~40 NSE stocks, rolling window.
  * Build the correlation matrix -> convert to a distance  d_ij = sqrt(2(1-rho_ij)).
  * Persistent homology of that distance matrix (H0 + H1).
  * Summaries that prior crude version lacked:
       - L2 lifespan norm        (size of topological features)
       - persistent entropy      (how evenly spread the features are)
       - WASSERSTEIN change-rate (how much the topology *reorganized* vs yesterday)

The Wasserstein change-rate is the key addition: crashes are preceded by a rapid
*reorganization* of correlation structure, which a static norm misses.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser
from persim import wasserstein
from tda_crash import auc, label_crashes, rolling_volatility, BENCHMARK, START, END

WINDOW = 60
# Long-history set: all trading by early 2005, so 2008 IS included (fair to vol)
TICKERS = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
    "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
    "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS","MARUTI.NS","CIPLA.NS",
    "DRREDDY.NS","GRASIM.NS","HINDALCO.NS","BPCL.NS","HEROMOTOCO.NS","TITAN.NS",
]


def load():
    px = yf.download(TICKERS + [BENCHMARK], start=START, end=END,
                     auto_adjust=True, progress=False)["Close"]
    # keep stocks with near-full history
    good = [t for t in TICKERS if px[t].notna().mean() > 0.80]
    px = px[good + [BENCHMARK]].dropna()
    logret = np.log(px / px.shift(1)).dropna()
    print(f"  using {len(good)} stocks, {len(logret)} days")
    return logret[good], np.log(px[BENCHMARK] / px[BENCHMARK].shift(1)).dropna()


def topology_signals(stock_ret, window=WINDOW):
    R = stock_ret.values
    dates = stock_ret.index
    prev_dgm = None
    rows = []
    for end in range(window, len(R)):
        win = R[end - window:end]
        C = np.corrcoef(win.T)                       # correlation structure
        C = np.clip(C, -1, 1)
        D = np.sqrt(2 * (1 - C))                      # correlation -> distance
        np.fill_diagonal(D, 0.0)
        dgm = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
        life = (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.array([])
        life = life[np.isfinite(life)]
        l2 = float(np.sqrt(np.sum(life ** 2))) if len(life) else 0.0
        # persistent entropy
        if len(life) and life.sum() > 0:
            p = life / life.sum()
            ent = float(-np.sum(p * np.log(p + 1e-12)))
        else:
            ent = 0.0
        # wasserstein change-rate vs previous window (handle empty diagrams
        # explicitly: an empty->nonempty transition IS a real topological change)
        if prev_dgm is not None:
            a = dgm if len(dgm) else np.zeros((0, 2))
            b = prev_dgm if len(prev_dgm) else np.zeros((0, 2))
            try:
                wd = 0.0 if (len(a) == 0 and len(b) == 0) else float(wasserstein(b, a))
            except Exception:
                wd = np.nan
        else:
            wd = np.nan
        prev_dgm = dgm
        rows.append((dates[end], l2, ent, wd))
    return pd.DataFrame(rows, columns=["date","tda_L2","tda_entropy",
                                       "tda_wasserstein"]).set_index("date")


def run():
    print("Downloading ...")
    stock_ret, bench_ret = load()
    print("Computing correlation-structure persistence (this takes a minute) ...")
    tda = topology_signals(stock_ret)

    df = tda.copy()
    df["volatility"] = rolling_volatility(bench_ret).reindex(df.index)
    df["crash_ahead"] = label_crashes(bench_ret).reindex(df.index)
    df = df.dropna()

    print("\n=== AUC: predicting a crash within 20 days ===")
    signals = ["volatility","tda_L2","tda_entropy","tda_wasserstein"]
    aucs = {}
    for s in signals:
        # orient each signal so higher = more crash-like
        a = auc(df[s], df["crash_ahead"])
        if a < 0.5:
            a = auc(-df[s], df["crash_ahead"]); df[s] = -df[s]
        aucs[s] = a
        tag = "  (baseline)" if s == "volatility" else ""
        print(f"  {s:18s}: AUC = {a:.3f}{tag}")

    # best topological signal + volatility
    def z(x): return (x - x.mean()) / x.std()
    best_tda = max([s for s in signals if s != "volatility"], key=lambda s: aucs[s])
    combined = z(df["volatility"]) + z(df[best_tda])
    a_comb = auc(combined, df["crash_ahead"])
    corr = df[best_tda].corr(df["volatility"])
    print(f"\n  Best topology = {best_tda} (AUC {aucs[best_tda]:.3f}, "
          f"corr w/ vol {corr:.2f})")
    print(f"  Volatility alone          : AUC {aucs['volatility']:.3f}")
    print(f"  Volatility + best topology: AUC {a_comb:.3f}  "
          f"(lift {a_comb-aucs['volatility']:+.3f})")

    # significance of the lift
    y = df["crash_ahead"].to_numpy(); sv = df["volatility"].to_numpy()
    sc = combined.to_numpy(); rng = np.random.default_rng(0)
    n = len(df); diffs = []
    for _ in range(1000):
        bi = rng.choice(np.arange(n), n, replace=True)
        diffs.append(_a(sc[bi], y[bi]) - _a(sv[bi], y[bi]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    print(f"  95% bootstrap CI of lift  : [{lo:+.3f}, {hi:+.3f}]  "
          f"-> {'SIGNIFICANT' if lo > 0 else 'not significant'}")
    df.to_csv("tda_v2_results.csv")
    print("\nSaved tda_v2_results.csv")


def _a(s, y):
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    pos, neg = (y == 1), (y == 0)
    if pos.sum() == 0 or neg.sum() == 0: return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s)+1)
    return (r[pos].sum() - pos.sum()*(pos.sum()+1)/2) / (pos.sum()*neg.sum())


if __name__ == "__main__":
    run()
