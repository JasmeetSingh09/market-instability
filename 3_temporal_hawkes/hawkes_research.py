"""
hawkes_research.py — RIGOROUS study (research-grade, not a prototype).

RESEARCH QUESTION
-----------------
How strong must a pump-and-dump's self-excitation be before the Hawkes branching
ratio can reliably detect it — and does a volume detector ever catch up?

WHY THIS IS RESEARCH, NOT A DEMO
--------------------------------
The prototype reported a single AUC = 1.0 on one clean simulation, which is not
credible on its own. Here we instead SWEEP the pump's branching ratio n and run
many Monte-Carlo trials at each level, reporting detection AUC with a 95%
confidence interval — for BOTH the Hawkes branching ratio and a volume baseline.
Crucially, every pump is VOLUME-MATCHED to normal trading, so volume *should*
stay at chance (AUC ~ 0.5) by construction; the question is how well self-
excitation separates them, and at what intensity it starts to work.
"""

import numpy as np
from hawkes import simulate_hawkes, simulate_poisson, fit_hawkes

rng = np.random.default_rng(0)

N_TRIALS = 15          # Monte-Carlo repetitions per intensity level -> CIs
M_EPISODES = 8         # normal + pump episodes per trial
T_EP = 150.0
BASE_RATE = 0.6        # normal Poisson intensity


def _auc(score, label):
    score, label = np.asarray(score, float), np.asarray(label, int)
    m = np.isfinite(score)
    score, label = score[m], label[m]
    pos, neg = score[label == 1], score[label == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    return (ranks[label == 1].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def one_trial(n_pump):
    beta, alpha = 1.0, n_pump          # branching ratio n = alpha/beta
    mu_pump = BASE_RATE * (1 - n_pump)  # volume-matched background
    br, vol, lab = [], [], []
    for _ in range(M_EPISODES):
        ev = simulate_poisson(BASE_RATE, T_EP)          # normal
        f = fit_hawkes(ev, T_EP)
        if f: br.append(f[3]); vol.append(len(ev)); lab.append(0)
        ev = simulate_hawkes(mu_pump, alpha, beta, T_EP)  # pump
        f = fit_hawkes(ev, T_EP)
        if f: br.append(f[3]); vol.append(len(ev)); lab.append(1)
    return _auc(br, lab), _auc(vol, lab)


def run():
    print("Monte-Carlo sweep of pump intensity (detection AUC with 95% CIs)\n")
    print(f"{'branching n':>12} {'Hawkes AUC (95% CI)':>26} {'Volume AUC (95% CI)':>26}")
    for n_pump in [0.3, 0.5, 0.7, 0.9]:
        haw, vol = [], []
        for _ in range(N_TRIALS):
            a_h, a_v = one_trial(n_pump)
            if np.isfinite(a_h): haw.append(a_h)
            if np.isfinite(a_v): vol.append(a_v)
        h_lo, h_hi = np.percentile(haw, [2.5, 97.5])
        v_lo, v_hi = np.percentile(vol, [2.5, 97.5])
        print(f"{n_pump:>12.1f}   {np.mean(haw):>6.3f} [{h_lo:.3f},{h_hi:.3f}]"
              f"     {np.mean(vol):>6.3f} [{v_lo:.3f},{v_hi:.3f}]")

    print("\nInterpretation: Hawkes AUC should climb toward 1.0 as pump self-excitation")
    print("rises, while the volume baseline stays ~0.5 (blind, by construction). The")
    print("branching ratio n at which Hawkes AUC clears ~0.7 is the detection threshold.")


if __name__ == "__main__":
    run()
