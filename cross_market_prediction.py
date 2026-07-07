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

MARKETS = {
    "India equities": ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
                       "ITC.NS","SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS"],
    "US equities":    ["AAPL","MSFT","GOOGL","AMZN","META","JPM","XOM","JNJ","PG","WMT"],
    "Japan (Nikkei)": ["7203.T","6758.T","6861.T","9984.T","8306.T","6098.T","7974.T",
                       "4063.T","9433.T","8035.T"],
    "UK (FTSE)":      ["AZN.L","SHEL.L","HSBA.L","ULVR.L","BP.L","GSK.L","RIO.L","DGE.L",
                       "BATS.L","LLOY.L"],
    "HK (Hang Seng)": ["0700.HK","9988.HK","0939.HK","1299.HK","0005.HK","3690.HK",
                       "0941.HK","1810.HK","2318.HK","0388.HK"],
    "Crypto":         ["BTC-USD","ETH-USD","BNB-USD","XRP-USD","ADA-USD","SOL-USD",
                       "DOGE-USD","LTC-USD"],
}


def auc(score, label):
    s = np.asarray(score, float); y = np.asarray(label, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    if y.sum() == 0 or y.sum() == len(y): return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    pos = (y == 1)
    a = (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (len(y) - pos.sum()))
    return max(a, 1 - a)


def analyse(tickers, start="2012-01-01"):
    px = yf.download(tickers, start=start, end="2024-12-31", auto_adjust=True,
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
    df["crash"] = (fwd < -0.10).astype(float)
    df = df.dropna()
    y = df["crash"].values
    z = lambda s: (s - s.mean()) / (s.std() + 1e-9)
    frag = z(df["R"]) + z(df["T"]) + z(df["H"])
    return {
        "windows": len(df), "crashes": int(y.sum()),
        "Fragility": auc(frag, y), "volatility": auc(df["vol"], y),
        "avg_corr": auc(df["avgcorr"], y), "spectral_R": auc(df["R"], y),
    }


def run():
    print("Cross-market crash-warning: Fragility Index vs baselines (higher AUC = better)\n")
    print(f"{'Market':>16} | {'win':>5} {'crash':>5} | {'Fragility':>9} {'volatility':>10} "
          f"{'avg_corr':>9} {'spectral_R':>10} | beats baselines?")
    print("-" * 92)
    results = {}
    for name, tickers in MARKETS.items():
        try:
            r = analyse(tickers)
        except Exception as e:
            print(f"{name:>16} | error: {e}"); continue
        if r is None:
            print(f"{name:>16} | insufficient data"); continue
        results[name] = r
        base = max(r["volatility"], r["avg_corr"], r["spectral_R"])
        verdict = "YES" if r["Fragility"] > base + 0.02 else "no (~= baselines)"
        print(f"{name:>16} | {r['windows']:>5} {r['crashes']:>5} | {r['Fragility']:>9.3f} "
              f"{r['volatility']:>10.3f} {r['avg_corr']:>9.3f} {r['spectral_R']:>10.3f} | {verdict}")

    if results:
        import numpy as _np
        wins = sum(1 for r in results.values()
                   if r["Fragility"] > max(r["volatility"], r["avg_corr"], r["spectral_R"]) + 0.02)
        print(f"\nGeneralisation: Fragility Index beats all baselines in {wins}/{len(results)} markets.")
        print("Honest reading: if it does NOT consistently beat a trivial avg-correlation or")
        print("volatility baseline, the honest conclusion is that it CHARACTERISES fragility")
        print("but does not reliably out-PREDICT simple measures -- reported across markets,")
        print("which is itself the cross-market result (#2) with proper baselines (#4).")


if __name__ == "__main__":
    run()
