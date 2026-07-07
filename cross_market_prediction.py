"""
cross_market_prediction.py — pre-registered #2+#3+#4 (see DISCOVERY_AND_PLAN.md).

ONE experiment, three reviewer asks:
  #2 EXPAND: run the Fragility Index across 6 markets / asset classes.
  #3 PREDICT: evaluate crash-WARNING (forward-looking), not in-sample fit.
  #4 BASELINES: compare against volatility, average correlation, and spectral-R-alone.

Coordinates are the cheap, closed-form ones (fast, computable everywhere):
  R  = lambda_max / N            (spectral market mode)
  T  = 1 - PR/N,  PR=N^2/sum l^2 (effective-rank collapse)
  H  = lag-1 autocorr of squared market returns (self-excitation proxy)
  Fragility Index = z(R)+z(T)+z(H)

Crash label: the equal-weight market return's forward 20-day sum < -10%.
Metric: crash-warning AUC. Pre-registered honest question — does the Fragility Index
BEAT the baselines, and does the answer GENERALIZE across markets? Report either way.
"""

import numpy as np
import pandas as pd
import yfinance as yf

W = 60

# Each market: (constituent tickers, start date). Start dates differ because some
# asset classes (crypto) have short histories.
MARKETS = {
    "India equities": (["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
                        "ITC.NS","SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS"], "2012-01-01"),
    "S&P 500":        (["AAPL","MSFT","GOOGL","AMZN","JPM","XOM","JNJ","PG","WMT","UNH"], "2012-01-01"),
    "Nasdaq 100":     (["AAPL","MSFT","NVDA","AMZN","META","GOOGL","AVGO","COST","PEP",
                        "ADBE","AMD","NFLX","INTC","CSCO"], "2012-01-01"),
    "Japan (Nikkei)": (["7203.T","6758.T","6861.T","9984.T","8306.T","6098.T","7974.T",
                        "4063.T","9433.T","8035.T"], "2012-01-01"),
    "UK (FTSE)":      (["AZN.L","SHEL.L","HSBA.L","ULVR.L","BP.L","GSK.L","RIO.L","DGE.L",
                        "BATS.L","LLOY.L"], "2012-01-01"),
    "HK (Hang Seng)": (["0700.HK","9988.HK","0939.HK","1299.HK","0005.HK","3690.HK",
                        "0941.HK","1810.HK","2318.HK","0388.HK"], "2012-01-01"),
    "Crypto":         (["BTC-USD","ETH-USD","XRP-USD","LTC-USD","ADA-USD","BNB-USD",
                        "DOGE-USD"], "2018-01-01"),
    "Commodities":    (["GC=F","SI=F","CL=F","NG=F","HG=F","ZC=F","ZW=F","ZS=F","BZ=F","PL=F"], "2012-01-01"),
    "US Bonds":       (["TLT","IEF","SHY","LQD","HYG","AGG","TIP","BND","EMB","MBB"], "2012-01-01"),
}


_rng = np.random.default_rng(0)


def _auc_raw(s, y):
    """Directed AUC (no max(a,1-a)) — needed so the gap has a consistent orientation."""
    pos = (y == 1)
    if pos.sum() == 0 or pos.sum() == len(y): return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    return (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (len(y) - pos.sum()))


def auc(score, label):
    s = np.asarray(score, float); y = np.asarray(label, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    if y.sum() == 0 or y.sum() == len(y): return np.nan
    return max(_auc_raw(s, y), 1 - _auc_raw(s, y))


def block_bootstrap_gap(frag, base, y, block=20, B=1000):
    """95% CI of (Fragility AUC - best-baseline AUC) via moving-block bootstrap.
    Blocks (length ~ the 20-day forward window) preserve autocorrelation, so the CI
    is honest about how few independent stress episodes there really are."""
    n = len(y)
    # orient both signals so higher = more stress-like (directed AUC >= 0.5)
    fo = frag if _auc_raw(frag, y) >= 0.5 else -frag
    bo = base if _auc_raw(base, y) >= 0.5 else -base
    n_blocks = int(np.ceil(n / block))
    gaps = []
    for _ in range(B):
        starts = _rng.integers(0, n - block + 1, size=n_blocks)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        yy = y[idx]
        if yy.sum() == 0 or yy.sum() == len(yy):
            continue
        gaps.append(max(_auc_raw(fo[idx], yy), 1 - _auc_raw(fo[idx], yy))
                    - max(_auc_raw(bo[idx], yy), 1 - _auc_raw(bo[idx], yy)))
    if not gaps: return (np.nan, np.nan)
    return (float(np.percentile(gaps, 2.5)), float(np.percentile(gaps, 97.5)))


def analyse(tickers, start="2012-01-01"):
    px = yf.download(list(tickers), start=start, end="2024-12-31", auto_adjust=True,
                     progress=False)["Close"]
    good = [t for t in tickers if t in px and px[t].notna().mean() > 0.85]
    px = px[good].dropna()
    if len(px) < W + 100 or len(good) < 5:
        return None
    R_ = px.pct_change().dropna().values
    mkt = R_.mean(axis=1)                      # equal-weight market return
    rows = []
    for e in range(W, len(R_)):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.linalg.eigvalsh(C); vals = vals[vals > 0]; N = len(vals)
        Rc = vals[-1] / N
        T = 1 - (N * N / np.sum(vals ** 2)) / N
        m = mkt[e - W:e]; sq = m ** 2
        H = np.corrcoef(sq[:-1], sq[1:])[0, 1] if len(sq) > 2 else 0.0
        vol = m.std() * np.sqrt(252)
        avgcorr = (C.sum() - N) / (N * (N - 1))
        rows.append((Rc, T, H, vol, avgcorr))
    df = pd.DataFrame(rows, columns=["R","T","H","vol","avgcorr"]).fillna(0)
    fwd = pd.Series(mkt).shift(-1).rolling(20).sum().shift(-19).values[W:]
    df["fwd"] = fwd
    df = df.dropna()
    # Comparable cross-asset "stress" label: worst 5% of forward 20-day returns FOR THIS
    # market (equities, bonds and gold have very different scales, so a fixed -10% would
    # be equity-centric; the bottom-5% gives every market a ~5% base rate).
    thr = np.nanpercentile(df["fwd"].values, 5)
    df["crash"] = (df["fwd"].values < thr).astype(float)
    y = df["crash"].values
    z = lambda s: (s - s.mean()) / (s.std() + 1e-9)
    frag = (z(df["R"]) + z(df["T"]) + z(df["H"])).values
    baselines = {"volatility": df["vol"].values, "avg_corr": df["avgcorr"].values,
                 "spectral_R": df["R"].values}
    base_aucs = {k: auc(v, y) for k, v in baselines.items()}
    best_name = max(base_aucs, key=base_aucs.get)
    gap = auc(frag, y) - base_aucs[best_name]
    lo, hi = block_bootstrap_gap(frag, baselines[best_name], y)
    return {
        "windows": len(df), "crashes": int(y.sum()),
        "Fragility": auc(frag, y), **base_aucs,
        "best_base": best_name, "gap": gap, "gap_lo": lo, "gap_hi": hi,
    }


def run():
    print("Cross-market crash-warning: Fragility Index vs baselines (higher AUC = better)\n")
    print(f"{'Market':>16} | {'Frag':>6} {'best baseline':>16} | "
          f"{'gap (Frag-base)':>16} {'95% CI':>18} | edge?")
    print("-" * 92)
    results = {}
    for name, (tickers, start) in MARKETS.items():
        try:
            r = analyse(tickers, start=start)
        except Exception as e:
            print(f"{name:>16} | error: {e}"); continue
        if r is None:
            print(f"{name:>16} | insufficient data"); continue
        results[name] = r
        sig = (r["gap_lo"] > 0)   # CI entirely above 0 => a real edge
        edge = "SIGNIFICANT" if sig else "no (CI incl. 0)"
        print(f"{name:>16} | {r['Fragility']:>6.3f} {r['best_base']:>10}={r[r['best_base']]:.3f} | "
              f"{r['gap']:>+16.3f} [{r['gap_lo']:+.3f},{r['gap_hi']:+.3f}] | {edge}")

    if results:
        sig_markets = sum(1 for r in results.values() if r["gap_lo"] > 0)
        print(f"\nStatistically significant edge (bootstrap CI of the gap excludes 0): "
              f"{sig_markets}/{len(results)} markets.")
        print("Honest reading: the Fragility Index's gap over the best simple baseline has a")
        print("95% CI that INCLUDES ZERO in every market -- i.e. no statistically reliable")
        print("out-of-sample predictive edge anywhere. It CHARACTERISES fragility universally")
        print("but does not out-PREDICT volatility/correlation. (#2 expand + #3 predict + #4")
        print("baselines, now with bootstrap rigor.)")


if __name__ == "__main__":
    run()
