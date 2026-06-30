"""
Random Matrix Theory for Portfolio Construction (Indian Market)
===============================================================

Research question
-----------------
A covariance matrix of N stocks estimated from T days is mostly NOISE when N is
not << T. Random Matrix Theory (Marchenko-Pastur) tells us exactly which
eigenvalues are noise. Does *cleaning* that noise build portfolios with lower
realised risk and higher Sharpe than the raw sample covariance — out-of-sample,
net of transaction costs — on NSE stocks?

Math (Algebra / Probability & Statistics)
-----------------------------------------
For a purely random N x T correlation matrix with q = N/T, the eigenvalues fall
inside the Marchenko-Pastur band [lambda_-, lambda_+] with
        lambda_+- = sigma^2 (1 +- sqrt(q))^2 .
Any eigenvalue below lambda_+ is statistically indistinguishable from noise.
We keep the eigenvectors above lambda_+ (genuine market/sector structure) and
replace the sub-band eigenvalues with their average (preserving the trace).

We then build Global Minimum Variance portfolios from (a) the raw sample
covariance, (b) the RMT-cleaned covariance, (c) Ledoit-Wolf shrinkage, and an
equal-weight benchmark, and compare them strictly out-of-sample.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.covariance import LedoitWolf

START, END = "2010-01-01", "2024-12-31"
T_EST   = 120          # estimation window (days) -> q = N/T is meaningfully large
REBAL   = 21           # rebalance monthly
COST    = 0.0010       # 10 bps per unit turnover

TICKERS = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
    "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","KOTAKBANK.NS",
    "MARUTI.NS","HCLTECH.NS","SUNPHARMA.NS","WIPRO.NS","ONGC.NS","NTPC.NS",
    "TITAN.NS","ULTRACEMCO.NS","TATASTEEL.NS","TATAMOTORS.NS","JSWSTEEL.NS",
    "GRASIM.NS","HINDALCO.NS","CIPLA.NS","DRREDDY.NS","BPCL.NS","HEROMOTOCO.NS",
    "BAJAJ-AUTO.NS","COALINDIA.NS","ASIANPAINT.NS","NESTLEIND.NS","POWERGRID.NS",
    "ADANIPORTS.NS","TECHM.NS","DIVISLAB.NS","BRITANNIA.NS","EICHERMOT.NS","SBILIFE.NS",
]


def load():
    px = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.95]
    px = px[good].dropna()
    ret = px.pct_change().dropna()
    print(f"  {len(good)} stocks, {len(ret)} days, q = N/T = {len(good)/T_EST:.2f}")
    return ret


# ---------------------------------------------------------------------------
# Covariance estimators
# ---------------------------------------------------------------------------
def cov_sample(R):
    return np.cov(R.T)


def cov_rmt(R):
    """Marchenko-Pastur eigenvalue cleaning of the correlation matrix."""
    T, N = R.shape
    stds = R.std(0, ddof=1)
    C = np.corrcoef(R.T)
    vals, vecs = np.linalg.eigh(C)
    q = N / T
    lam_max = vals[-1]
    # variance carried by the noise band (exclude the market mode)
    sigma2 = max(1.0 - lam_max / N, 1e-6)
    lam_plus = sigma2 * (1 + np.sqrt(q)) ** 2
    vals_clean = vals.copy()
    noise = vals < lam_plus
    if noise.any():
        vals_clean[noise] = vals[noise].mean()          # preserve trace
    C_clean = (vecs * vals_clean) @ vecs.T
    d = np.sqrt(np.clip(np.diag(C_clean), 1e-12, None))
    C_clean = C_clean / np.outer(d, d)                   # restore unit diagonal
    return C_clean * np.outer(stds, stds)                # back to covariance


def cov_ledoit(R):
    return LedoitWolf().fit(R).covariance_


# ---------------------------------------------------------------------------
# Global minimum-variance portfolio
# ---------------------------------------------------------------------------
def gmv_weights(cov):
    N = cov.shape[0]
    inv = np.linalg.pinv(cov)
    w = inv @ np.ones(N)
    return w / w.sum()


# ---------------------------------------------------------------------------
# Walk-forward backtest
# ---------------------------------------------------------------------------
def backtest(ret, t_est=T_EST):
    R = ret.values
    dates = ret.index
    T_EST_LOCAL = t_est
    estimators = {
        "Equal weight":   None,
        "Sample cov":     cov_sample,
        "Ledoit-Wolf":    cov_ledoit,
        "RMT-cleaned":    cov_rmt,
    }
    results = {k: {"ret": [], "w_prev": None, "pred_vol": []} for k in estimators}

    t = T_EST_LOCAL
    while t < len(R) - 1:
        window = R[t - T_EST_LOCAL:t]
        nxt = R[t:t + REBAL]                     # out-of-sample holding period
        if len(nxt) == 0:
            break
        for name, fn in estimators.items():
            if fn is None:
                w = np.ones(R.shape[1]) / R.shape[1]
                cov = cov_sample(window)
            else:
                cov = fn(window)
                w = gmv_weights(cov)
            # predicted annualised vol of this portfolio
            results[name]["pred_vol"].append(np.sqrt(w @ cov @ w * 252))
            # realised daily returns, charge cost on turnover at rebalance
            wp = results[name]["w_prev"]
            turn = np.abs(w - wp).sum() if wp is not None else 0.0
            daily = nxt @ w
            daily[0] -= turn * COST
            results[name]["ret"].extend(daily.tolist())
            results[name]["w_prev"] = w
        t += REBAL
    return results


def metrics(daily):
    d = np.asarray(daily)
    eq = np.cumprod(1 + d)
    yrs = len(d) / 252
    cagr = eq[-1] ** (1 / yrs) - 1
    vol = d.std() * np.sqrt(252)
    sharpe = (d.mean() / (d.std() + 1e-12)) * np.sqrt(252)
    peak = np.maximum.accumulate(eq)
    maxdd = ((eq - peak) / peak).min()
    return cagr, vol, sharpe, maxdd


def run():
    print("Downloading ...")
    ret = load()
    print("Walk-forward backtest (monthly rebalance, 10bps cost) ...")
    res = backtest(ret)

    print(f"\n{'Estimator':16s} {'CAGR':>7s} {'Vol':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
          f"{'PredVol':>8s}")
    rows = {}
    for name, r in res.items():
        cagr, vol, sharpe, maxdd = metrics(r["ret"])
        pv = np.mean(r["pred_vol"])
        rows[name] = (cagr, vol, sharpe, maxdd, pv)
        print(f"{name:16s} {cagr*100:6.1f}% {vol*100:6.1f}% {sharpe:7.2f} "
              f"{maxdd*100:7.1f}% {pv*100:7.1f}%")

    # the headline comparison
    s_raw = rows["Sample cov"]; s_rmt = rows["RMT-cleaned"]
    print("\n=== DID RMT CLEANING HELP? (vs raw sample covariance) ===")
    print(f"  Realised vol : {s_raw[1]*100:.1f}% -> {s_rmt[1]*100:.1f}%  "
          f"({'LOWER (better)' if s_rmt[1] < s_raw[1] else 'higher'})")
    print(f"  Sharpe       : {s_raw[2]:.2f} -> {s_rmt[2]:.2f}  "
          f"({'HIGHER (better)' if s_rmt[2] > s_raw[2] else 'lower'})")
    print(f"  Max drawdown : {s_raw[3]*100:.1f}% -> {s_rmt[3]*100:.1f}%")
    # RMT's classic point: raw cov UNDER-predicts realised risk
    print(f"\n  Risk honesty: raw cov predicted {s_raw[4]*100:.1f}% vol but realised "
          f"{s_raw[1]*100:.1f}%; RMT predicted {s_rmt[4]*100:.1f}% vs realised "
          f"{s_rmt[1]*100:.1f}% (closer = more honest risk estimate).")


def sweep(ret):
    """RMT's benefit should GROW as q = N/T grows (shorter, noisier windows)."""
    N = ret.shape[1]
    print("\n=== THEORY CHECK: does RMT help MORE as the matrix gets noisier? ===")
    print(f"{'Window T':>9s} {'q=N/T':>7s} {'Raw Sharpe':>11s} {'RMT Sharpe':>11s} "
          f"{'RMT edge':>9s} {'Raw vol':>8s} {'RMT vol':>8s}")
    for t_est in [40, 60, 90, 120, 200]:
        res = backtest(ret, t_est=t_est)
        _, vraw, sraw, _ = metrics(res["Sample cov"]["ret"])
        _, vrmt, srmt, _ = metrics(res["RMT-cleaned"]["ret"])
        print(f"{t_est:9d} {N/t_est:7.2f} {sraw:11.2f} {srmt:11.2f} "
              f"{srmt-sraw:+9.2f} {vraw*100:7.1f}% {vrmt*100:7.1f}%")
    print("  -> if 'RMT edge' is larger at small T (large q), the theory holds.")


if __name__ == "__main__":
    print("Downloading ...")
    _ret = load()
    print("Walk-forward backtest (monthly rebalance, 10bps cost) ...")
    _res = backtest(_ret)
    print(f"\n{'Estimator':16s} {'CAGR':>7s} {'Vol':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'PredVol':>8s}")
    _rows = {}
    for _name, _r in _res.items():
        _c, _v, _s, _dd = metrics(_r["ret"])
        _pv = np.mean(_r["pred_vol"]); _rows[_name] = (_c, _v, _s, _dd, _pv)
        print(f"{_name:16s} {_c*100:6.1f}% {_v*100:6.1f}% {_s:7.2f} {_dd*100:7.1f}% {_pv*100:7.1f}%")
    _sr, _sm = _rows["Sample cov"], _rows["RMT-cleaned"]
    print("\n=== DID RMT CLEANING HELP? (vs raw sample covariance) ===")
    print(f"  Realised vol : {_sr[1]*100:.1f}% -> {_sm[1]*100:.1f}%  "
          f"({'LOWER (better)' if _sm[1] < _sr[1] else 'higher'})")
    print(f"  Sharpe       : {_sr[2]:.2f} -> {_sm[2]:.2f}  "
          f"({'HIGHER (better)' if _sm[2] > _sr[2] else 'lower'})")
    print(f"  Risk honesty : raw predicted {_sr[4]*100:.1f}% vs realised {_sr[1]*100:.1f}%; "
          f"RMT predicted {_sm[4]*100:.1f}% vs realised {_sm[1]*100:.1f}%")
    sweep(_ret)
