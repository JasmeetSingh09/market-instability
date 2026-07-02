"""
multimarket.py — Does the framework GENERALISE beyond Indian equities?

Runs two of the three lenses across THREE markets (India equities, US equities,
crypto) to separate what is UNIVERSAL from what is market-specific — directly
answering the ISEF reviewer question "does it generalise?".

Metrics (both comparable across markets, with dispersion across assets):
  * TEMPORAL (Hawkes): branching ratio n of extreme-move events — how strongly
    do big moves trigger more big moves? (self-excitation)
  * SPECTRAL (RMT): does Ledoit-Wolf covariance cleaning cut out-of-sample GMV
    volatility vs the raw sample covariance? (is cleaning universally needed?)
"""

import os
import sys
import numpy as np
import yfinance as yf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "1_spectral_rmt"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "3_temporal_hawkes"))
from rmt import cov_sample, cov_ledoit, gmv_weights          # noqa: E402
from hawkes import fit_hawkes                                  # noqa: E402

MARKETS = {
    "India equities": ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
                       "ITC.NS","SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS"],
    "US equities":    ["AAPL","MSFT","GOOGL","AMZN","META","JPM","XOM","JNJ","PG","WMT"],
    "Crypto":         ["BTC-USD","ETH-USD","BNB-USD","XRP-USD","ADA-USD","SOL-USD",
                       "DOGE-USD","LTC-USD"],
}


def branching_ratios(tickers, period="8y"):
    """Fit a Hawkes process to each asset's extreme-move (top-5%) event times."""
    out = []
    for t in tickers:
        try:
            px = yf.download(t, period=period, auto_adjust=True,
                             progress=False)["Close"].squeeze().dropna()
            if len(px) < 250:
                continue
            r = np.log(px / px.shift(1)).dropna()
            thr = r.abs().quantile(0.95)
            days = np.arange(len(r)).astype(float)
            ev = days[r.abs().values > thr]
            f = fit_hawkes(ev, float(len(r)))
            if f and np.isfinite(f[3]):
                out.append(min(f[3], 0.999))
        except Exception:
            continue
    return np.array(out)


def cleaning_benefit(tickers, period="8y", t_est=120):
    """Realised out-of-sample GMV vol: raw sample covariance vs Ledoit-Wolf."""
    px = yf.download(tickers, period=period, auto_adjust=True, progress=False)["Close"]
    good = [t for t in tickers if px[t].notna().mean() > 0.9]
    px = px[good].dropna()
    R = px.pct_change().dropna().values
    s, l = [], []
    t = t_est
    while t < len(R) - 1:
        win = R[t - t_est:t]; nxt = R[t:t + 21]
        if len(nxt) == 0:
            break
        try:
            s.extend((nxt @ gmv_weights(cov_sample(win))).tolist())
            l.extend((nxt @ gmv_weights(cov_ledoit(win))).tolist())
        except Exception:
            pass
        t += 21
    v = lambda a: float(np.std(a) * np.sqrt(252)) if a else np.nan
    return v(s), v(l)


def run():
    print("Multi-market generalisation study (India / US / Crypto)\n")
    print(f"{'Market':>16} | {'Hawkes n (mean [range])':>28} | "
          f"{'GMV vol: sample -> Ledoit':>26}")
    print("-" * 78)
    for name, tickers in MARKETS.items():
        ns = branching_ratios(tickers)
        vs, vl = cleaning_benefit(tickers)
        if len(ns):
            lo, hi = np.percentile(ns, [10, 90])
            nstr = f"{ns.mean():.2f} [{lo:.2f},{hi:.2f}]"
        else:
            nstr = "n/a"
        print(f"{name:>16} | {nstr:>28} | {vs*100:>10.1f}% -> {vl*100:.1f}%")

    print("\nWhat to look for:")
    print("  * UNIVERSAL if it holds in all three: e.g. Ledoit-Wolf cleaning cuts vol")
    print("    everywhere (cleaning is needed in every market).")
    print("  * MARKET-SPECIFIC if it differs: e.g. crypto self-excites far more than")
    print("    equities (higher branching ratio) — a real cross-market finding.")


if __name__ == "__main__":
    run()
