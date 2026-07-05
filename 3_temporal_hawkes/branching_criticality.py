"""
branching_criticality.py — do crises show signatures consistent with a self-exciting
process approaching branching-process criticality (n -> 1)?

Theory in ../BRANCHING_CRITICALITY.md: the Hawkes branching ratio n = alpha/beta is
the mean-offspring (criticality) parameter of an equivalent Galton-Watson process;
expected cascade size 1/(1-n) diverges as n -> 1. Critical slowing down predicts
that AR(1) and variance also rise toward criticality before a transition.

We TEST this hypothesis (not assert it), with the reviewer's six guardrails:
  1. branching ratio n through time (does it move toward 1 before crashes?)
  2. lag-1 autocorrelation before crashes
  3. variance before crashes
  4. bootstrap confidence intervals on the pre-crash vs baseline gap
  5. CONTROL FOR VOLATILITY (residualize signals on volatility) — the key test
  6. false-positive rate (how often the signal fires without a crash)
"""

import numpy as np
import yfinance as yf
from hawkes import fit_hawkes

W, BENCH = 60, "^NSEI"
rng = np.random.default_rng(0)


def resid(y, x):
    """residual of y after regressing on x (+ intercept) — removes volatility part."""
    X = np.c_[np.ones_like(x), x]
    return y - X @ np.linalg.lstsq(X, y, rcond=None)[0]


def build():
    px = yf.download(BENCH, start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"].squeeze().dropna()
    r = px.pct_change().dropna()
    rv = r.values
    thr = np.quantile(np.abs(rv), 0.90)          # extreme-move threshold (full sample)
    n_, ar1_, var_, vol_, dates = [], [], [], [], []
    for e in range(W, len(rv)):
        seg = rv[e - W:e]
        ev = np.where(np.abs(seg) > thr)[0].astype(float)
        f = fit_hawkes(ev, float(W))
        n = min(f[3], 1.5) if (f and np.isfinite(f[3])) else np.nan
        ar1 = np.corrcoef(seg[:-1], seg[1:])[0, 1]
        n_.append(n); ar1_.append(ar1); var_.append(seg.var())
        vol_.append(seg.std() * np.sqrt(252)); dates.append(r.index[e])
    import pandas as pd
    df = pd.DataFrame({"n": n_, "ar1": ar1_, "var": var_, "vol": vol_}, index=dates)
    fwd = px.pct_change().shift(-1).rolling(20).sum().shift(-19)
    df["crash"] = (fwd.reindex(df.index) < -0.10).astype(float)
    return df.dropna()


def gap_ci(sig, crash, B=2000):
    """pre-crash minus baseline mean, with bootstrap 95% CI."""
    pre, base = sig[crash == 1], sig[crash == 0]
    obs = pre.mean() - base.mean()
    boot = [rng.choice(pre, len(pre)).mean() - rng.choice(base, len(base)).mean()
            for _ in range(B)]
    return obs, np.percentile(boot, 2.5), np.percentile(boot, 97.5)


def fpr(sig, crash, q=80):
    """false-positive rate: fraction of NON-crash windows where signal exceeds its qth pct."""
    thr = np.percentile(sig, q)
    non = sig[crash == 0]
    return np.mean(non > thr)


def run():
    print("Fitting rolling Hawkes n, AR(1), variance on NSE; testing branching criticality\n")
    df = build()
    y = df["crash"].values
    print(f"windows: {len(df)}   pre-crash windows: {int(y.sum())}   "
          f"mean n = {df['n'].mean():.2f}\n")

    print("=== Experiments 1-3: are signals elevated before crashes? (raw) ===")
    for s, name in [("n","branching ratio n"), ("ar1","lag-1 autocorr"), ("var","variance")]:
        o, lo, hi = gap_ci(df[s].values, y)
        sig = "SIGNIFICANT" if (lo > 0 or hi < 0) else "not significant"
        print(f"  {name:18s}: pre-crash − baseline = {o:+.4f}  95% CI [{lo:+.4f},{hi:+.4f}]  [{sig}]")

    print("\n=== Experiment 5 (THE KEY TEST): does it survive controlling for volatility? ===")
    print("    (residualize each signal on volatility, then re-test the pre-crash gap)")
    for s, name in [("n","branching ratio n"), ("ar1","lag-1 autocorr"), ("var","variance")]:
        rsig = resid(df[s].values, df["vol"].values)
        o, lo, hi = gap_ci(rsig, y)
        sig = "SURVIVES" if (lo > 0 or hi < 0) else "vanishes (was mostly volatility)"
        print(f"  {name:18s}: vol-controlled gap = {o:+.4f}  95% CI [{lo:+.4f},{hi:+.4f}]  [{sig}]")

    print("\n=== Experiment 6: false-positive rate (signal > 80th pct on NON-crash windows) ===")
    for s, name in [("n","branching ratio n"), ("ar1","lag-1 autocorr"), ("var","variance")]:
        print(f"  {name:18s}: FPR = {fpr(df[s].values, y):.3f}")

    print("\nRead honestly: a signal only counts if its pre-crash elevation SURVIVES the")
    print("volatility control AND has a low false-positive rate. If variance's gap vanishes")
    print("once volatility is removed, that is the expected null — report it plainly. If n or")
    print("AR(1) survive, that is genuine evidence consistent with branching criticality.")


if __name__ == "__main__":
    run()
