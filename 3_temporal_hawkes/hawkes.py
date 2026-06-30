"""
Hawkes Processes for Pump-and-Dump Detection
============================================

Purpose
-------
Market manipulation ("pump-and-dump") is a burst of *coordinated, self-exciting*
trading — one buy triggers the next. Standard tools that look at *volume* miss
it, because a stealth pump can have the SAME volume as normal trading, just
*clustered in time*. This project models trade-event arrivals as a **Hawkes
process** (self-exciting point process, originally for earthquake aftershocks)
and shows its self-excitation parameter detects manipulation that volume cannot.

Math (Probability & Statistics — applied stochastic processes)
--------------------------------------------------------------
A univariate Hawkes process with an exponential kernel has conditional intensity
        lambda(t) = mu + sum_{t_i < t} alpha * exp(-beta (t - t_i))
- mu    : background rate (independent arrivals)
- alpha : jump in intensity caused by each event (self-excitation)
- beta  : decay rate of that excitation
- BRANCHING RATIO  n = alpha / beta  in [0,1): the expected number of "child"
  events triggered by each event. n -> 0 is Poisson (no manipulation); n -> 1 is
  critical/explosive (a pump). n is our manipulation signal.

We implement the exact log-likelihood (O(N) recursion), fit by MLE, validate on
real crypto data, and run a controlled detection experiment.
"""

import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(0)


# ---------------------------------------------------------------------------
# Hawkes log-likelihood (exponential kernel), O(N) recursion
# ---------------------------------------------------------------------------
def neg_loglik(params, events, T):
    mu, alpha, beta = params
    if mu <= 0 or alpha < 0 or beta <= 0:
        return 1e12
    # recursive sum A_i = sum_{j<i} exp(-beta (t_i - t_j))
    A = 0.0
    ll = 0.0
    prev = None
    for t in events:
        if prev is not None:
            A = np.exp(-beta * (t - prev)) * (1.0 + A)
        ll += np.log(mu + alpha * A)
        prev = t
    # compensator (integral of intensity)
    comp = mu * T + (alpha / beta) * np.sum(1.0 - np.exp(-beta * (T - events)))
    return -(ll - comp)


def fit_hawkes(events, T):
    """MLE fit; returns (mu, alpha, beta, branching_ratio)."""
    events = np.sort(np.asarray(events, dtype=float))
    if len(events) < 5:
        return None
    rate0 = len(events) / T
    best = None
    for a0, b0 in [(rate0, 2 * rate0 + 1e-3), (0.5 * rate0, 1.0), (rate0, 5.0)]:
        try:
            r = minimize(neg_loglik, [rate0, a0, b0], args=(events, T),
                         method="L-BFGS-B",
                         bounds=[(1e-6, None), (0, None), (1e-3, None)])
            if best is None or r.fun < best.fun:
                best = r
        except Exception:
            continue
    if best is None:
        return None
    mu, alpha, beta = best.x
    return mu, alpha, beta, alpha / beta


# ---------------------------------------------------------------------------
# Hawkes simulation (Ogata thinning)
# ---------------------------------------------------------------------------
def simulate_hawkes(mu, alpha, beta, T):
    events = []
    t = 0.0
    while t < T:
        lam_bar = mu + alpha * np.sum(np.exp(-beta * (t - np.array(events)))) if events else mu
        t += rng.exponential(1.0 / lam_bar)
        if t >= T:
            break
        lam = mu + alpha * np.sum(np.exp(-beta * (t - np.array(events)))) if events else mu
        if rng.uniform() <= lam / lam_bar:
            events.append(t)
    return np.array(events)


def simulate_poisson(rate, T):
    n = rng.poisson(rate * T)
    return np.sort(rng.uniform(0, T, n))
