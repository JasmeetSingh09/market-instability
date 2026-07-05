# Theoretical Interpretation through Branching Criticality

*A theoretical section for the temporal (Hawkes) lens. We do NOT claim to have
discovered phase transitions in markets. We show that the Hawkes branching ratio
admits a natural, rigorous interpretation as a **criticality parameter** of a
branching process, and we test — honestly, controlling for volatility — whether
financial crises show signatures **consistent with** approaching that critical
regime.*

---

## 1. The theoretical chain

```
Hawkes self-exciting process
      ↓  (cluster representation)
Galton–Watson branching process
      ↓
critical parameter  n = branching ratio
      ↓
critical regime  n → 1
      ↓
diverging cascades  ↔  financial crashes
```

This is not a metaphor. The link at each arrow is a theorem.

## 2. Hawkes ↔ branching process (why n is THE criticality parameter)

A Hawkes process has intensity
    λ(t) = μ + Σ_{t_i < t} φ(t − t_i),   with kernel φ(u) = α e^(−β u).

**Cluster (Hawkes–Oakes) representation.** Every Hawkes process is equivalent to a
branching process: "immigrant" events arrive at rate μ (Poisson), and each event
independently produces "offspring" via the kernel φ. The **mean number of direct
offspring per event** is the integral of the kernel:

    n = ∫_0^∞ φ(u) du = ∫_0^∞ α e^(−β u) du = α / β.

So the Hawkes **branching ratio n = α/β is exactly the mean offspring number of a
Galton–Watson branching process.** That identification is the whole bridge.

## 3. The phase transition (derive this — it is the defensible core)

In a Galton–Watson process where each individual has on average n offspring, start
from one "shock." It produces on average n events; each of those produces n more;
and so on. The expected total cascade size (the original event plus all descendants)
is the geometric series

    E[cascade size] = 1 + n + n² + n³ + ...

**Case n < 1 (subcritical):** the series converges,

    E[cascade size] = 1 / (1 − n)   <  ∞.

Shocks die out. The market absorbs disturbances. Stable.

**Case n = 1 (critical):** the series is 1 + 1 + 1 + ... The sum **diverges**:

    E[cascade size] = 1 / (1 − n) → ∞   as n → 1⁻.

This divergence **is** the phase transition. It is the exact point separating a
stable (subcritical) regime from an explosive (supercritical) one — the same
critical point (mean offspring = 1) that governs epidemics (R₀ = 1) and nuclear
chain reactions.

**Case n > 1 (supercritical):** cascades grow without bound with positive
probability — an explosive, self-sustaining regime.

**Stationarity condition.** A Hawkes process is stationary (well-defined long-run
behaviour) **iff n < 1**. The boundary n = 1 is therefore the stability boundary of
the model itself — not an imposed interpretation.

## 4. Why "approaching n = 1" is critical SLOWING DOWN

Statistical physics: near a critical transition a system recovers from perturbations
ever more slowly ("critical slowing down"). Same statement, two languages:

- **Cascade language:** as n → 1, expected cascade size 1/(1−n) → ∞ — one shock
  echoes through ever-longer chains before dying out.
- **Time-series language:** model the observable as AR(1), x_{t+1} = a·x_t + noise.
  Its recovery rate after a shock is −ln(a); as the stability parameter a → 1 the
  recovery rate → 0 (infinitely slow recovery), and the lag-1 autocorrelation → 1
  and the variance → ∞.

So the classical early-warning signals — **rising lag-1 autocorrelation** and
**rising variance** — are the time-domain fingerprints of the *same* criticality
that n → 1 expresses in the cascade domain. That is why we test all three together.

## 5. The research question (hypothesis, not assertion)

> **Do financial crises exhibit statistical signatures consistent with a
> self-exciting process approaching branching-process criticality (n → 1),
> as reflected jointly in the branching ratio, lag-1 autocorrelation, and
> variance — after controlling for volatility?**

We *test* this. We do not assume it.

## 6. What would count as evidence — and the traps

**Positive evidence** would be: n, AR(1), and variance all rise toward their
critical values in the run-up to crashes, and the rise **survives controlling for
volatility** and has a **low false-positive rate**.

**Three traps that would invalidate a naïve "yes":**
1. **Variance ≈ volatility.** Rising variance is almost tautologically "volatility
   went up." Unless the signal survives residualizing against volatility, it says
   nothing new. (This is the same confound that sank our TDA lens — we do not repeat
   the mistake.)
2. **False positives.** Critical-slowing-down indicators rise before many non-events.
   We must report the false-positive rate, not just pre-crash averages.
3. **Estimator instability near n = 1.** The Hawkes MLE is noisy when n is close to
   1 and events are few; every estimate carries a bootstrap confidence interval.

## 7. Honest claim boundaries

- ✅ Defensible: *"The Hawkes branching ratio is the criticality parameter of an
  equivalent branching process; we test whether crises approach n = 1."*
- ✅ Defensible (if data supports): *"Financial crashes exhibit signatures
  consistent with approaching a critical branching regime."*
- ✅ Defensible (if data does not): *"After controlling for volatility, evidence
  for critical slowing down is weak"* — a real, publishable negative.
- ❌ NOT defensible: *"This project proves markets undergo phase transitions."*

The value of this section is that it adds **theory and interpretation**, upgrading
the project's structure from *methods → experiments → results* to
*theory → methods → experiments → interpretation* — without inventing a new
algorithm or overclaiming.

---

## 8. Empirical result (`3_temporal_hawkes/branching_criticality.py`)

Rolling W = 60-day windows on the Nifty (2010–2024); 1961 windows, 31 pre-crash.
Branching ratio n fit by Hawkes MLE on extreme-move times; AR(1) and variance
computed per window; crash = forward-20-day return < −10%.

| Signal | Pre-crash − baseline (raw), 95% CI | After controlling for volatility |
|---|---|---|
| Branching ratio n | −0.078 [−0.139, +0.032] — n.s. | −0.071 [−0.131, +0.031] — vanishes |
| Lag-1 autocorrelation | +0.013 [−0.009, +0.036] — n.s. | +0.004 [−0.019, +0.028] — vanishes |
| Variance | ≈0 (CI excludes 0 but effect ~0) | ≈0 — vanishes |

False-positive rates ≈ 0.19–0.20 for all three — i.e. no better than the base rate
(no discrimination).

**Honest conclusion (a real, publishable negative).** On daily Indian-equity data,
**financial crashes do NOT show clean signatures of branching-process criticality
once volatility is controlled for.** Specifically:
- The branching ratio does **not** rise toward the critical value n = 1 before
  crashes — if anything it is slightly *lower*, and the difference is not
  significant.
- Mean n ≈ 0.13 — the daily-extreme-event process is **strongly subcritical**,
  nowhere near the n = 1 transition.
- Every apparent pre-crash elevation **disappears after controlling for
  volatility**, and false-positive rates match the base rate.

**Interpretation, with the honest caveats from §6.**
1. This is the *expected* result if crashes are largely volatility-driven rather
   than genuine critical transitions — consistent with this project's spine finding
   (fragility is characterizable, crashes are not reliably predictable).
2. **Estimator/data caveat (trap #3 + the daily-data caveat).** n ≈ 0.13 here is far
   below the ~0.6 seen on richer cross-sectional/crypto data, because it is fit on a
   single index's few extreme days per 60-day window — a noisy, low-event regime.
   Genuine branching criticality, if it exists, would most plausibly appear in
   **intraday / order-book data**, where self-excitation is a microstructural
   reality, not on daily bars. So this is a null *on daily data*, not a refutation
   of criticality in general.

**Defensible sentence for the paper:** *"After controlling for volatility, we find
weak evidence for critical-slowing-down signatures on daily data; the Hawkes
branching ratio remains strongly subcritical (n ≈ 0.13) and does not approach the
critical value before crashes, consistent with a volatility-driven rather than a
critical-transition account at the daily scale."*
