"""
Topological Early-Warning Signals for Stock-Market Crashes (Indian Market)
==========================================================================

Research question
-----------------
Do TOPOLOGICAL features of the Indian equity market change *before* a crash,
giving an early-warning signal that ordinary volatility does not?

Method (after Gidea & Katz, 2018 — applied here to Indian markets)
------------------------------------------------------------------
1. Take 4 large, liquid NSE stocks spanning sectors.
2. Each trading day is a point  (r1, r2, r3, r4)  = that day's log-returns,
   so a sliding window of w days is a *point cloud* of w points in R^4.
3. Compute the window's persistence diagram (H1 — loops) via Vietoris-Rips.
4. Summarise each diagram by the L1 and L2 norms of its loop "lifespans".
   When the market becomes unstable, these topological norms RISE.
5. Test whether that rise *precedes* large drawdowns in the Nifty 50,
   and compare its early-warning power against plain rolling volatility.

This is a MATHEMATICS project (Geometry & Topology): the object of study is
the persistent homology of a financial point cloud. The market data is just
the experimental vehicle.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from ripser import ripser

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
TICKERS   = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
             "ITC.NS", "SBIN.NS", "LT.NS", "HINDUNILVR.NS", "BHARTIARTL.NS"]  # 10 stocks, R^10
BENCHMARK = "^NSEI"            # Nifty 50 — used only to *label* crashes
START     = "2005-01-01"
END       = "2024-12-31"
WINDOW    = 50                 # sliding window length (trading days)
CRASH_DROP = -0.10            # a "crash" = 20-day forward Nifty return below -10%
HORIZON    = 20                # forward window (days) over which we measure a crash


# ----------------------------------------------------------------------------
# 1. Data
# ----------------------------------------------------------------------------
def load_returns():
    """Download adjusted closes and return aligned daily log-returns."""
    px = yf.download(TICKERS + [BENCHMARK], start=START, end=END,
                     auto_adjust=True, progress=False)["Close"]
    px = px.dropna()
    logret = np.log(px / px.shift(1)).dropna()
    stock_ret = logret[TICKERS]            # the point-cloud coordinates
    bench_ret = logret[BENCHMARK]          # for crash labelling
    return stock_ret, bench_ret, px[BENCHMARK]


# ----------------------------------------------------------------------------
# 2. Topological signal
# ----------------------------------------------------------------------------
def topological_norms(stock_ret, window=WINDOW, standardize=False):
    """
    Slide a window over the 4-D return series; for each window compute the
    H1 persistence diagram and summarise it by L1 / L2 lifespan norms.

    standardize=False -> raw returns (norm partly reflects volatility scale).
    standardize=True  -> z-score each stock WITHIN the window, isolating the
                         *geometric/correlation structure* from the magnitude.
                         This is the "pure topology" signal, independent of vol.

    Returns a DataFrame indexed by the window's END date.
    """
    X = stock_ret.values
    dates = stock_ret.index
    rows = []
    for end in range(window, len(X)):
        cloud = X[end - window:end]                 # w points in R^4
        if standardize:
            mu = cloud.mean(axis=0)
            sd = cloud.std(axis=0)
            sd[sd == 0] = 1.0
            cloud = (cloud - mu) / sd               # shape only, scale removed
        dgm = ripser(cloud, maxdim=1)["dgms"][1]    # H1 (loops)
        if len(dgm) == 0:
            l1 = l2 = 0.0
        else:
            life = dgm[:, 1] - dgm[:, 0]            # persistence (death - birth)
            life = life[np.isfinite(life)]
            l1 = float(np.sum(life))               # L1 norm
            l2 = float(np.sqrt(np.sum(life ** 2)))  # L2 norm
        rows.append((dates[end], l1, l2))
    out = pd.DataFrame(rows, columns=["date", "tda_L1", "tda_L2"]).set_index("date")
    return out


# ----------------------------------------------------------------------------
# 3. Crash labels + baseline
# ----------------------------------------------------------------------------
def label_crashes(bench_ret):
    """A day is 'pre-crash' if the Nifty falls more than CRASH_DROP over the
    next HORIZON days (i.e. the topological signal *should* fire here)."""
    fwd = bench_ret.shift(-1).rolling(HORIZON).sum().shift(-(HORIZON - 1))
    return (fwd < CRASH_DROP).astype(int)          # 1 = a crash follows


def rolling_volatility(bench_ret, window=WINDOW):
    return bench_ret.rolling(window).std()


# ----------------------------------------------------------------------------
# 4. Evaluation — does the signal warn EARLY?
# ----------------------------------------------------------------------------
def auc(signal, label):
    """Area under ROC for using `signal` to predict an upcoming crash.
    No sklearn dependency — rank-based (Mann-Whitney) computation."""
    s = signal.values
    y = label.reindex(signal.index).values
    m = np.isfinite(s) & np.isfinite(y)
    s, y = s[m], y[m]
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    order = np.argsort(s)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(s) + 1)
    rank_pos = ranks[y == 1].sum()
    return (rank_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def run():
    print("Downloading data ...")
    stock_ret, bench_ret, nifty_px = load_returns()
    print(f"  {len(stock_ret)} trading days, {START}..{END}")

    print("Computing persistent homology over sliding windows (raw) ...")
    tda = topological_norms(stock_ret, standardize=False)
    print("Computing persistent homology (standardized = pure structure) ...")
    tda_s = topological_norms(stock_ret, standardize=True)

    label = label_crashes(bench_ret)
    vol = rolling_volatility(bench_ret).reindex(tda.index)

    # align everything
    df = tda.copy()
    df["tda_struct"] = tda_s["tda_L2"]            # scale-free topological signal
    df["volatility"] = vol
    df["crash_ahead"] = label.reindex(df.index)
    df = df.dropna()

    print("\n=== EARLY-WARNING POWER (AUC: predicting a crash within "
          f"{HORIZON} days) ===")
    auc_tda1 = auc(df["tda_L1"], df["crash_ahead"])
    auc_tda2 = auc(df["tda_L2"], df["crash_ahead"])
    auc_vol = auc(df["volatility"], df["crash_ahead"])
    print(f"  TDA  L1 norm : AUC = {auc_tda1:.3f}")
    print(f"  TDA  L2 norm : AUC = {auc_tda2:.3f}")
    print(f"  Volatility   : AUC = {auc_vol:.3f}   (baseline)")
    best = max(auc_tda1, auc_tda2)
    verdict = "BEATS" if best > auc_vol else "trails"
    print(f"\n  -> TDA alone {verdict} volatility ({best:.3f} vs {auc_vol:.3f}).")

    # --- The pure structural (scale-free) topological signal ---
    # A crash is preceded by rising correlations: the point cloud collapses
    # toward a line, H1 loops vanish, so the structural norm FALLS. We therefore
    # use the *negated* structural norm ("topological collapse") as the warning.
    df["tda_collapse"] = -df["tda_struct"]
    auc_struct = auc(df["tda_collapse"], df["crash_ahead"])
    corr_raw = df["tda_L2"].corr(df["volatility"])
    corr_struct = df["tda_collapse"].corr(df["volatility"])
    print("\n=== ISOLATING PURE TOPOLOGY (scale-free 'topological collapse') ===")
    print(f"  Topological collapse : AUC = {auc_struct:.3f}")
    print(f"  Raw TDA   vs volatility correlation : {corr_raw:.2f} (overlapping)")
    print(f"  Collapse  vs volatility correlation : {corr_struct:.2f} "
          f"({'INDEPENDENT signal' if abs(corr_struct) < 0.4 else 'still overlapping'})")

    # --- Is topology COMPLEMENTARY to volatility? (the real question) ---
    def z(s):
        return (s - s.mean()) / s.std()
    combined = z(df["tda_collapse"]) + z(df["volatility"])
    auc_combined = auc(combined, df["crash_ahead"])
    print("\n=== COMPLEMENTARITY: does (topological collapse + volatility) beat vol? ===")
    print(f"  Volatility only          : AUC = {auc_vol:.3f}")
    print(f"  Collapse + Volatility    : AUC = {auc_combined:.3f}")
    lift = auc_combined - auc_vol
    print(f"  -> Adding pure topology {'IMPROVES' if lift > 0 else 'does not improve'} "
          f"detection by {lift:+.3f} AUC.")

    # --- Does topology warn EARLIER? lead time before each crash ---
    print("\n=== LEAD TIME: how many days BEFORE a crash does each signal fire? ===")
    crash_starts = df.index[(df["crash_ahead"].diff() == 1)]
    tda_thr = df["tda_L2"].quantile(0.80)
    vol_thr = df["volatility"].quantile(0.80)
    tda_leads, vol_leads = [], []
    idx = df.index
    for cs in crash_starts:
        pos = idx.get_loc(cs)
        lookback = df.iloc[max(0, pos - 40):pos]      # 40 trading days before
        t_fire = lookback.index[lookback["tda_L2"] > tda_thr]
        v_fire = lookback.index[lookback["volatility"] > vol_thr]
        if len(t_fire):
            tda_leads.append(pos - idx.get_loc(t_fire[0]))   # TRADING days, not calendar
        if len(v_fire):
            vol_leads.append(pos - idx.get_loc(v_fire[0]))
    if tda_leads and vol_leads:
        print(f"  TDA fired early on {len(tda_leads)}/{len(crash_starts)} crashes, "
              f"avg {np.mean(tda_leads):.0f} trading days ahead")
        print(f"  Vol fired early on {len(vol_leads)}/{len(crash_starts)} crashes, "
              f"avg {np.mean(vol_leads):.0f} trading days ahead")

    df["combined_z"] = combined
    df.to_csv("tda_results.csv")
    print("\nSaved per-day signals to tda_results.csv")
    make_plot(df, nifty_px)
    return df, nifty_px


def make_plot(df, nifty_px):
    """Nifty 50 (log) with crash periods shaded, plus the two warning signals."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def z(s):
        return (s - s.mean()) / s.std()

    px = nifty_px.reindex(df.index)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.semilogy(px.index, px.values, color="black", lw=1)
    ax1.set_ylabel("Nifty 50 (log scale)")
    ax1.set_title("Topological Early-Warning vs. Nifty 50 Crashes (2005–2024)")
    # shade crash periods
    crash = df["crash_ahead"] == 1
    ax1.fill_between(df.index, px.min(), px.max(), where=crash,
                     color="red", alpha=0.15, label="crash within 20d")
    ax1.legend(loc="upper left")

    ax2.plot(df.index, z(df["volatility"]), color="steelblue", lw=0.8,
             label="Volatility (z)")
    ax2.plot(df.index, z(df["tda_collapse"]), color="darkorange", lw=0.8,
             label="Topological collapse (z)")
    ax2.fill_between(df.index, -3, 3, where=crash, color="red", alpha=0.15)
    ax2.set_ylabel("z-score")
    ax2.legend(loc="upper left")
    ax2.set_ylim(-3, 4)
    plt.tight_layout()
    plt.savefig("tda_figure.png", dpi=130)
    print("Saved figure to tda_figure.png")


if __name__ == "__main__":
    run()
