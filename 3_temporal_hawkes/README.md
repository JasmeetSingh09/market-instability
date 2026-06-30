# Hawkes Processes for Pump-and-Dump Detection

**ISEF category:** Mathematics → *Probability & Statistics* (applied stochastic processes)
**Purpose:** protect retail investors — detect coordinated manipulation that volume-based surveillance misses.
**Result:** ✅ strong, with honest caveats.

---

## The idea
A pump-and-dump is a burst of **coordinated, self-exciting** trading: one buy
triggers the next. Volume-based detection is *blind* to a "stealth pump" that has
the **same volume** as normal trading but is **clustered in time**. We model trade
events as a **Hawkes process** (self-exciting point process — originally for
earthquake aftershocks) and use its self-excitation to expose manipulation.

## The math
Univariate Hawkes process, exponential kernel, conditional intensity:
```
        λ(t) = μ + Σ_{tᵢ < t} α · exp(−β (t − tᵢ))
```
- `μ` background rate, `α` excitation jump, `β` decay.
- **Branching ratio** `n = α/β ∈ [0,1)` = expected events triggered by each event.
  `n → 0` is Poisson (no manipulation); `n → 1` is critical/explosive (a pump).

We implement the **exact log-likelihood** (O(N) recursion), fit by maximum
likelihood, and simulate via **Ogata thinning** — all from scratch (`hawkes.py`).

## Results

### Part A — real markets genuinely self-excite
Fitting Hawkes to the extreme-move times of **BTC-USD** (5-min bars, 60 days):
> **Branching ratio n = 0.77** — strongly self-exciting. Each extreme move
> triggers ~0.77 further moves on average. Real markets are *not* Poisson.

### Part B — Hawkes catches what volume cannot (the key experiment)
We generated **volume-matched** episodes: "normal" (Poisson) vs "pump" (Hawkes),
designed to have the **same expected number of events** — the only difference is
the pump is *clustered*. A volume detector therefore *cannot* tell them apart by
design; the question is whether self-excitation can.

| Detector | AUC (pump vs normal) |
|---|---|
| Volume (event count) | **0.39** — blind (≈ chance, by construction) |
| **Hawkes branching ratio** | **1.00** — perfect separation |

Fitted branching ratio: **0.04** on normal episodes vs **0.65** on pumps. The
Hawkes self-excitation parameter cleanly exposes the manipulation that volume
completely misses.

## Conclusion
**Self-excitation (the Hawkes branching ratio) is a manipulation signal that
volume-based surveillance is structurally blind to.** Real crypto markets exhibit
strong measurable self-excitation (n ≈ 0.77), and on controlled volume-matched
simulations the branching ratio detects stealth pumps that volume cannot.

**Honest caveats (important):**
- The AUC = 1.00 is on **clean simulations** with a clear separation (n = 0.7 vs
  Poisson). On noisy real data with ambiguous events it will be **lower** — this
  experiment proves the *mechanism*, not a deployed accuracy.
- Real-world validation needs a **labelled dataset** of actual pump-and-dump
  events (the hard part — and the next step with the professor).
- A real surveillance system would use a **multivariate** Hawkes process (cross-
  asset / order-book contagion), not the univariate model here.

## Files
- `hawkes.py` — Hawkes log-likelihood, MLE fit, simulation (from scratch)
- `detect.py` — real-crypto validation + the detection experiment

## Open directions (for the full paper)
- Acquire labelled pump events (Telegram pump-group archives, regulator filings).
- Multivariate / order-book Hawkes; time-varying baseline μ(t).
- Rolling real-time branching-ratio monitor with alerting.

## Reference
Hawkes (1971), *Spectra of some self-exciting and mutually exciting point
processes*; Bacry, Mastromatteo & Muzy (2015), *Hawkes processes in finance*.
