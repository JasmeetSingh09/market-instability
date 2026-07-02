"""
tda_research.py — RIGOROUS study (research-grade): is the TDA null robust?

RESEARCH QUESTION
-----------------
Does topological structure add statistically significant crash-warning power
over plain volatility on Indian markets — and is that answer ROBUST to how we
define a "crash"?

WHY THIS IS RESEARCH, NOT A DEMO
--------------------------------
The prototype found the TDA lift over volatility was not significant for one
crash definition. A skeptic could object: "you just picked a definition that
kills it." So here we compute the correlation-structure topology ONCE, then
sweep the crash definition (drawdown threshold x horizon) and, for each, report
the AUC lift of (TDA + volatility) over volatility alone with a paired
block-bootstrap 95% CI. If the null holds across definitions, it is robust.
"""

import numpy as np
import pandas as pd
from tda_v2 import load, topology_signals
from tda_crash import rolling_volatility, auc, BENCHMARK

rng = np.random.default_rng(0)


def label_crashes(bench_ret, drop, horizon):
    fwd = bench_ret.shift(-1).rolling(horizon).sum().shift(-(horizon - 1))
    return (fwd < drop).astype(int)


def boot_auc_lift(combined, vol, label, n_boot=800, block=21):
    """Paired block-bootstrap 95% CI for AUC(combined) - AUC(vol)."""
    df = pd.DataFrame({"c": combined, "v": vol, "y": label}).dropna()
    c, v, y = df["c"].values, df["v"].values, df["y"].values
    n = len(y); nb = int(np.ceil(n / block)); diffs = []
    def _a(s, yy):
        pos, neg = (yy == 1), (yy == 0)
        if pos.sum() == 0 or neg.sum() == 0: return np.nan
        o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
        return (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum())
    base = _a(c, y) - _a(v, y)
    for _ in range(n_boot):
        starts = rng.integers(0, max(1, n - block), nb)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        diffs.append(_a(c[idx], y[idx]) - _a(v[idx], y[idx]))
    lo, hi = np.nanpercentile(diffs, [2.5, 97.5])
    return base, lo, hi


def run():
    print("Computing correlation-structure topology once (this takes a minute) ...")
    stock_ret, bench_ret = load()
    tda = topology_signals(stock_ret)
    vol = rolling_volatility(bench_ret).reindex(tda.index)

    def z(x): return (x - x.mean()) / x.std()
    # best topological summary, oriented so higher = more crash-like
    print("\n=== Robustness of the TDA-vs-volatility null across crash definitions ===")
    print(f"{'crash def':>18} {'vol AUC':>8} {'+TDA AUC':>9} {'lift':>7} {'95% CI':>18} {'verdict':>14}")
    for drop in [-0.08, -0.10, -0.12]:
        for horizon in [15, 20, 30]:
            lab = label_crashes(bench_ret, drop, horizon).reindex(tda.index)
            df = pd.DataFrame({"tda": tda["tda_L2"], "ent": tda["tda_entropy"],
                               "vol": vol, "y": lab}).dropna()
            if df["y"].sum() < 10:
                continue
            # pick best topo signal by |AUC-0.5|, orient it
            best, bestcol = 0.5, None
            for col in ["tda", "ent"]:
                a = auc(df[col], df["y"])
                a = a if a >= 0.5 else 1 - a
                if a > best: best, bestcol = a, col
            sig = df[bestcol] if auc(df[bestcol], df["y"]) >= 0.5 else -df[bestcol]
            combined = z(df["vol"]) + z(sig)
            av = auc(df["vol"], df["y"])
            ac = auc(combined, df["y"])
            base, lo, hi = boot_auc_lift(combined.values, df["vol"].values, df["y"].values)
            verdict = "significant" if lo > 0 else "NOT sig"
            print(f"{str(drop)+'/'+str(horizon)+'d':>18} {av:>8.3f} {ac:>9.3f} "
                  f"{base:>+7.3f} [{lo:>+.3f},{hi:>+.3f}] {verdict:>14}")

    print("\nInterpretation: if the lift's CI includes 0 across (nearly) all crash")
    print("definitions, the 'TDA adds no significant edge over volatility' result is")
    print("ROBUST — not an artifact of one arbitrary crash definition.")


if __name__ == "__main__":
    run()
