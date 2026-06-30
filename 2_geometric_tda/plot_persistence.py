"""
HERO VISUAL #2 — TDA persistence diagrams: the market's topological "shape".

We build the correlation-distance point cloud of NSE stocks in two regimes and
compute their persistence diagrams (H0 = clusters, H1 = loops). In a CALM market
the structure is rich (loops with long lifespans, far from the diagonal). Near a
CRASH, correlations spike, the cloud collapses, and the loops vanish (points
hug the diagonal). The diagram literally shows the topology dying.
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ripser import ripser

TICKERS = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
    "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
    "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS","MARUTI.NS","CIPLA.NS",
]
WINDOW = 60


def dgms_ending(ret, end_date):
    sub = ret.loc[:end_date].tail(WINDOW)
    C = np.clip(np.corrcoef(sub.values.T), -1, 1)
    D = np.sqrt(2 * (1 - C)); np.fill_diagonal(D, 0.0)
    return ripser(D, distance_matrix=True, maxdim=1)["dgms"]


def panel(ax, dgms, title):
    lim = 1.6
    ax.plot([0, lim], [0, lim], "k--", lw=1, alpha=0.6)
    for d, c, lab in [(dgms[0], "steelblue", "H0 (clusters)"),
                      (dgms[1], "crimson", "H1 (loops)")]:
        d = d[np.isfinite(d).all(1)]
        if len(d):
            ax.scatter(d[:, 0], d[:, 1], s=40, c=c, alpha=0.75,
                       edgecolors="k", linewidths=0.4, label=lab)
    nloops = int(np.isfinite(dgms[1]).all(1).sum())
    ax.set_title(f"{title}\n({nloops} topological loops)")
    ax.set_xlabel("birth"); ax.set_ylabel("death")
    ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.legend(loc="lower right", fontsize=8)


def main():
    px = yf.download(TICKERS, start="2015-01-01", end="2021-01-01",
                     auto_adjust=True, progress=False)["Close"].dropna()
    ret = np.log(px / px.shift(1)).dropna()
    calm = dgms_ending(ret, "2017-09-30")        # quiet bull market
    crash = dgms_ending(ret, "2020-03-20")       # COVID crash

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6))
    panel(axes[0], calm, "CALM market (Sep 2017)")
    panel(axes[1], crash, "CRASH (Mar 2020, COVID)")
    fig.suptitle("Persistence diagrams: market topology collapses under stress\n"
                 "(points far above the diagonal = long-lived structure; "
                 "near the diagonal = noise)", y=1.02)
    plt.tight_layout()
    plt.savefig("tda_persistence_diagram.png", dpi=140, bbox_inches="tight")
    print(f"calm loops: {len(calm[1])}, crash loops: {len(crash[1])}")
    print("Saved tda_persistence_diagram.png")


if __name__ == "__main__":
    main()
