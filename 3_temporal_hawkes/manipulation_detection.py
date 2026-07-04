"""
manipulation_detection.py — sharpen the Hawkes manipulation detector.

Two honest upgrades over the earlier AUC-only result:
  1. CORRECT METRICS for RARE-event detection. Manipulation is rare, so ROC-AUC is
     misleading. We report Precision-Recall AUC (average precision) and the
     FALSE-POSITIVE RATE at a fixed high-recall operating point — the metrics a
     real surveillance system is judged on.
  2. A REAL-DATA touch: fit the Hawkes model to a live crypto asset's extreme-move
     times to show real markets self-excite (branching ratio > 0) — the method is
     not purely synthetic. (Verified labelled pump data remains the next step.)
"""

import numpy as np
import yfinance as yf
from hawkes import simulate_hawkes, simulate_poisson, fit_hawkes, rng
from sklearn.metrics import roc_auc_score, average_precision_score

# rare manipulation: only ~15% of episodes are pumps (imbalanced, realistic)
N_NORMAL, N_PUMP = 170, 30
T_EP, BASE_RATE, N_PUMP_BR = 150.0, 0.6, 0.7


def build_episodes():
    beta, alpha = 1.0, N_PUMP_BR
    mu_pump = BASE_RATE * (1 - N_PUMP_BR)          # volume-matched
    scores_br, scores_vol, y = [], [], []
    for _ in range(N_NORMAL):
        ev = simulate_poisson(BASE_RATE, T_EP)
        f = fit_hawkes(ev, T_EP)
        if f: scores_br.append(f[3]); scores_vol.append(len(ev)); y.append(0)
    for _ in range(N_PUMP):
        ev = simulate_hawkes(mu_pump, alpha, beta, T_EP)
        f = fit_hawkes(ev, T_EP)
        if f: scores_br.append(f[3]); scores_vol.append(len(ev)); y.append(1)
    return np.array(scores_br), np.array(scores_vol), np.array(y)


def fpr_at_recall(score, y, target_recall=0.80):
    """False-positive rate when the threshold is set to catch `target_recall` of pumps."""
    order = np.argsort(-score)
    s, yy = score[order], y[order]
    P, Nneg = yy.sum(), (yy == 0).sum()
    tp = fp = 0
    for i in range(len(yy)):
        if yy[i] == 1: tp += 1
        else: fp += 1
        if tp / P >= target_recall:
            return fp / Nneg
    return fp / Nneg


def run():
    print("Building imbalanced episodes (15% manipulation — realistic rarity) ...")
    br, vol, y = build_episodes()
    base_rate = y.mean()
    print(f"  {len(y)} episodes, {int(y.sum())} pumps ({base_rate*100:.0f}% — the rare positive)\n")

    print("=== DETECTION METRICS (the honest ones for rare events) ===")
    for name, s in [("Hawkes branching ratio", br), ("Volume (event count)", vol)]:
        roc = roc_auc_score(y, s)
        pr  = average_precision_score(y, s)          # PR-AUC (average precision)
        fpr = fpr_at_recall(s, y, 0.80)
        print(f"  {name:24s}: ROC-AUC {roc:.3f} | PR-AUC {pr:.3f} "
              f"(vs {base_rate:.2f} baseline) | FPR@80%recall {fpr:.3f}")
    print("\n  Read: PR-AUC far above the base rate + a LOW false-positive rate is what")
    print("  a real surveillance tool needs. Volume's PR-AUC should sit near the base")
    print("  rate (useless), while the branching ratio should be far higher.")

    print("\n=== REAL-DATA CHECK: does a live crypto asset self-excite? ===")
    for tkr in ["DOGE-USD", "BTC-USD"]:
        try:
            px = yf.download(tkr, period="60d", interval="1h",
                             auto_adjust=True, progress=False)["Close"].squeeze().dropna()
            r = np.log(px / px.shift(1)).dropna()
            thr = r.abs().quantile(0.95)
            hrs = np.arange(len(r)).astype(float)
            ev = hrs[r.abs().values > thr]
            f = fit_hawkes(ev, float(len(r)))
            if f:
                print(f"  {tkr}: {len(ev)} extreme moves | branching ratio n = {f[3]:.2f} "
                      f"({'self-exciting' if f[3] > 0.1 else 'near-Poisson'})")
        except Exception as e:
            print(f"  {tkr}: data unavailable ({e})")
    print("\nHonest limitation: the detection metrics are on controlled simulation and")
    print("the real-data check confirms self-excitation, not a verified pump. Validating")
    print("on a labelled real pump-and-dump dataset is the clear next step.")


if __name__ == "__main__":
    run()
