"""
HERO VISUAL #1 — the iconic Random Matrix Theory plot.

Shows the empirical eigenvalue spectrum of the market correlation matrix against
the Marchenko-Pastur "pure noise" prediction. Eigenvalues inside the MP band are
statistically indistinguishable from noise; only the few beyond the upper edge
(plus the giant market mode) carry real structure. This single figure visually
justifies the entire RMT-cleaning approach.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rmt import load, T_EST


def mp_density(lam, q, sigma2):
    """Marchenko-Pastur density on its support [lam_-, lam_+]."""
    lp = sigma2 * (1 + np.sqrt(q)) ** 2
    lm = sigma2 * (1 - np.sqrt(q)) ** 2
    d = np.zeros_like(lam)
    m = (lam > lm) & (lam < lp)
    d[m] = np.sqrt((lp - lam[m]) * (lam[m] - lm)) / (2 * np.pi * sigma2 * q * lam[m])
    return d, lp, lm


def main():
    print("Loading data ...")
    ret = load()
    R = ret.values
    N = R.shape[1]
    T = T_EST
    q = N / T

    # pool eigenvalues over rolling windows for a smooth empirical density
    eigs, top = [], []
    for t in range(T, len(R), 20):
        C = np.corrcoef(R[t - T:t].T)
        ev = np.linalg.eigvalsh(C)
        eigs.extend(ev)
        top.append(ev[-1])
    eigs = np.array(eigs)
    market_mode = np.mean(top)
    # variance left for the "noise" part after removing the market mode
    sigma2 = 1.0 - market_mode / N

    x = np.linspace(0.01, 3.0, 500)
    dens, lp, lm = mp_density(x, q, sigma2)
    n_signal = int(np.mean([(np.linalg.eigvalsh(np.corrcoef(R[t - T:t].T)) > lp).sum()
                            for t in range(T, len(R), 20)]))

    plt.figure(figsize=(10, 6))
    plt.hist(eigs[eigs < 3.0], bins=90, density=True, alpha=0.55,
             color="steelblue", label="empirical eigenvalues (real market)")
    plt.plot(x, dens, "r-", lw=2.5, label="Marchenko-Pastur (pure noise)")
    plt.axvline(lp, color="k", ls="--", lw=1.5,
                label=f"noise edge $\\lambda_+$ = {lp:.2f}")
    plt.title(f"Random Matrix Theory: most market eigenvalues are NOISE\n"
              f"N={N} stocks, T={T} days, q=N/T={q:.2f}  "
              f"(only ~{n_signal} eigenvalues are real signal; "
              f"the market mode $\\approx${market_mode:.0f} sits far to the right)")
    plt.xlabel("eigenvalue $\\lambda$")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("rmt_eigenvalue_spectrum.png", dpi=140)
    print(f"  market mode ~ {market_mode:.1f}, noise edge lp = {lp:.2f}, "
          f"~{n_signal} signal eigenvalues per window")
    print("Saved rmt_eigenvalue_spectrum.png")


if __name__ == "__main__":
    main()
