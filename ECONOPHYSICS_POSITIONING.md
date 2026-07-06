# Econophysics Positioning — framing only, defensible claims only

*This is a writing/positioning note, not new analysis. It sets the correct
expectation for readers and judges (this is a complex-systems / statistical-physics
characterization, not a price-prediction bot) and justifies why these three lenses.
It is deliberately conservative: use physics language only where the project already
does the physics. Metaphors you cannot derive at a whiteboard are listed as things to
AVOID.*

---

## Why the project is econophysics (this is accurate, not decoration)

Econophysics applies the tools of statistical physics and random-matrix theory to
markets treated as many-body complex systems. This project already lives there:

- **Spectral lens = Random Matrix Theory.** RMT originates in physics (Wigner, nuclear
  energy levels) and entered finance through Bouchaud, Laloux, Potters. Using the
  Marchenko–Pastur law to separate correlation "noise" from genuine collective
  structure is a core econophysics method — which is literally what our spectral lens
  does.
- **Temporal lens = self-organized criticality.** Hawkes processes were built to model
  earthquake aftershocks; the branching ratio is a criticality parameter (cascade size
  1/(1−n) diverges at n → 1). Testing whether markets approach that critical point is a
  standard econophysics question — and we *test it directly* in `branching_criticality.py`.
- **Integration = a phase / state space.** Representing each market state as a point
  F(t) = (R, T, H) and studying how it moves between ordered and disordered regions is
  exactly how physicists study complex systems (phase space, state clustering).

So framing the project as econophysics is *description*, not costume. It also does two
useful things for a defense:
1. **Corrects expectations.** Physics measures the *stability of a complex system*; it
   does not day-trade. This is why our honest result — "characterize fragility, do not
   reliably predict crashes" — is a feature, not a failure.
2. **Justifies the three lenses.** They are three physically motivated coordinates of
   one phenomenon (loss of statistical independence / onset of synchronization), not
   three unrelated scripts.

## The strongest econophysics statement we can actually make

Not a borrowed metaphor — a tested result:

> *We tested whether market crashes behave as self-organized-criticality phase
> transitions — whether the self-excitation branching ratio approaches its critical
> value n → 1 with the classical critical-slowing-down signatures — and found that,
> on daily data and after controlling for volatility, they do not (mean n ≈ 0.13).*

That is real statistical-physics reasoning with an honest null. It is worth more than
any amount of physics vocabulary.

## Claims to use (earned — you can defend these)

- Spectral: Marchenko–Pastur noise/signal separation (Wigner-origin RMT).
- Temporal: Hawkes branching ratio as a criticality index; n → 1 is a genuine
  phase transition (derived in `BRANCHING_CRITICALITY.md`); we *tested* critical
  slowing down and report the null.
- Integration: F(t) = (R, T, H) as a phase/state space; cluster it to see regimes.
- Overall stance: a **non-equilibrium complex-systems characterization** of fragility.

## Claims to AVOID (metaphor, not result — a physics judge will probe these)

- ❌ Do not claim literal **Bose–Einstein condensation** or **Ising / spin-glass
  magnetization** unless you can write down the mapping and Hamiltonian and defend it.
  Loose "like ice freezing" intuition is fine in one sentence; a *claim* is not.
- ❌ Do not say the project **"rejects equilibrium economics."** It measures correlation
  structure; it does not overturn a field.
- ❌ Do not call it a **"contribution to mathematical physics."** It is an *applied*
  characterization that *uses* physics tools — say exactly that.
- ❌ Do not treat "thermal noise," "gas vs solid phase," etc. as literal physical
  claims; they are at most one-line intuitions, clearly flagged as analogy.
- ❌ Do not let the physics vocabulary imply new prediction power we do not have.

## The governing rule

**Use physics language only as far as you can derive the physics.** Framing is armor
only when it is true; the moment it outruns what Jasmeet can defend at a whiteboard, it
becomes the easiest thing for a judge to attack. Keep it honest and it strengthens the
project; inflate it and it sinks it.
