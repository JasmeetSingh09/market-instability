"""
From detection to ACTION: does the topological signal actually protect a
portfolio — net of transaction costs — and is its edge statistically real?

This is the contribution that the (descriptive) prior TDA-finance literature
on Indian markets does not provide:
  1. A strictly out-of-sample de-risking strategy (no look-ahead).
  2. Transaction-cost-aware evaluation vs. buy-and-hold AND vs. a volatility-only
     rule -> isolating the *incremental* value of topology.
  3. A bootstrap significance test of the AUC lift.

Run `python tda_crash.py` first to generate tda_results.csv.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from tda_crash import auc, BENCHMARK, START, END

COST = 0.0010          # 10 bps per position switch (round-trip ~ realistic retail)
WARMUP = 250           # 1y before the strategy may trade (sets initial threshold)
QUANTILE = 0.80        # "warning" fires when signal is in its top 20% (so far)


def load_signals_and_returns():
    df = pd.read_csv("tda_results.csv", parse_dates=["date"]).set_index("date")
    nifty = yf.download(BENCHMARK, start=START, end=END,
                        auto_adjust=True, progress=False)["Close"].squeeze()
    ret = np.log(nifty / nifty.shift(1))
    df["nifty_ret"] = ret          # pandas aligns by DATE INDEX (safe, not positional)
    return df.dropna(subset=["nifty_ret"])


def metrics(daily_ret):
    daily_ret = np.asarray(daily_ret)
    equity = np.cumprod(1 + daily_ret)
    years = len(daily_ret) / 252
    cagr = equity[-1] ** (1 / years) - 1
    sharpe = (daily_ret.mean() / (daily_ret.std() + 1e-12)) * np.sqrt(252)
    peak = np.maximum.accumulate(equity)
    maxdd = ((equity - peak) / peak).min()
    return dict(CAGR=cagr, Sharpe=sharpe, MaxDD=maxdd, final=equity[-1])


def derisk_strategy(df, signal_col):
    """
    Out-of-sample de-risking rule with NO look-ahead:
    decide tomorrow's position from a signal threshold built ONLY from the past
    (expanding quantile). In cash when the warning fires, else fully invested.
    Charges COST whenever the position changes.
    """
    s = df[signal_col]
    thr = s.expanding(min_periods=WARMUP).quantile(QUANTILE)
    warn = (s > thr)                       # warning today...
    position = (~warn).astype(float).shift(1).fillna(1.0)  # ...sets tomorrow's position
    switches = position.diff().abs().fillna(0.0)
    strat_ret = position * df["nifty_ret"] - switches * COST
    return strat_ret, position


def run():
    df = load_signals_and_returns()
    simple = np.expm1(df["nifty_ret"])      # arithmetic returns for compounding

    print(f"Backtest 2006-2024 | cost {COST*1e4:.0f} bps/switch | "
          f"warning = top {int((1-QUANTILE)*100)}% of signal (expanding, no look-ahead)\n")

    # buy & hold
    bh = metrics(simple)

    # volatility-only de-risking
    vr, _ = derisk_strategy(df, "volatility")
    vrm = metrics(np.expm1(vr))

    # topology + volatility de-risking
    cr, pos = derisk_strategy(df, "combined_z")
    crm = metrics(np.expm1(cr))

    rows = [("Buy & hold Nifty", bh),
            ("De-risk on volatility only", vrm),
            ("De-risk on TOPOLOGY + volatility", crm)]
    print(f"{'Strategy':35s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'x money':>8s}")
    for name, m in rows:
        print(f"{name:35s} {m['CAGR']*100:6.1f}% {m['Sharpe']:7.2f} "
              f"{m['MaxDD']*100:7.1f}% {m['final']:7.2f}x")

    print("\nReading: a good crash filter should cut MaxDD and lift Sharpe vs "
          "buy-and-hold; topology EARNS ITS PLACE only if it beats the "
          "volatility-only rule.")

    # --- statistical significance of the AUC lift (paired bootstrap) ---
    print("\n=== Is the detection lift (vol -> vol+topology) statistically real? ===")
    y = df["crash_ahead"].to_numpy()
    sv = df["volatility"].to_numpy()
    sc = df["combined_z"].to_numpy()
    rng = np.random.default_rng(0)
    diffs = []
    n = len(df)
    idx_all = np.arange(n)
    base_v = auc(df["volatility"], df["crash_ahead"])
    base_c = auc(df["combined_z"], df["crash_ahead"])
    for _ in range(1000):
        bi = rng.choice(idx_all, n, replace=True)
        a_v = _auc_np(sv[bi], y[bi])
        a_c = _auc_np(sc[bi], y[bi])
        diffs.append(a_c - a_v)
    diffs = np.array(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    print(f"  Volatility AUC          : {base_v:.3f}")
    print(f"  Topology+volatility AUC : {base_c:.3f}")
    print(f"  Lift                    : {base_c-base_v:+.3f}  "
          f"(95% bootstrap CI [{lo:+.3f}, {hi:+.3f}])")
    sig = lo > 0
    print(f"  -> The lift is {'STATISTICALLY SIGNIFICANT' if sig else 'NOT significant'} "
          f"(CI {'excludes' if sig else 'includes'} 0).")

    _plot(df, simple, vr, cr)


def _auc_np(s, y):
    m = np.isfinite(s) & np.isfinite(y)
    s, y = s[m], y[m]
    pos, neg = (y == 1), (y == 0)
    if pos.sum() == 0 or neg.sum() == 0:
        return np.nan
    order = np.argsort(s)
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum())


def _plot(df, bh, vr, cr):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    eq = lambda r: np.cumprod(1 + np.expm1(np.asarray(r)))
    plt.figure(figsize=(12, 6))
    plt.semilogy(df.index, eq(df["nifty_ret"]), label="Buy & hold", color="black", lw=1)
    plt.semilogy(df.index, eq(vr), label="De-risk on volatility", color="steelblue", lw=1)
    plt.semilogy(df.index, eq(cr), label="De-risk on topology+vol", color="darkorange", lw=1.3)
    plt.title("Crash-protection strategy — growth of ₹1 (net of costs, log scale)")
    plt.legend(); plt.tight_layout()
    plt.savefig("strategy_figure.png", dpi=130)
    print("\nSaved strategy_figure.png")


if __name__ == "__main__":
    run()
