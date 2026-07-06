# Whiteboard Defense Sheet — Fragility Theorem

*One page. Drill it until you can reproduce every line from memory — not verbatim,
but because you understand it. Judges ask at a whiteboard, not on paper.*

---

## The 30-second pitch (say this first)
"Within the Fragility Space framework I define two eigenvalue-based coordinates of a
market correlation matrix — spectral R and effective-rank T. I prove they are not
independent: an exact identity plus closed-form bounds, from R and N alone, trap T in
a band. The band is tight in synchronized (crisis) markets and wide in calm ones —
which my data confirm. It's an applied-linear-algebra result *within the framework*,
and I do NOT claim it covers my topological or temporal lenses."

## Setup (write on the board)
- C = N×N correlation matrix, eigenvalues λ₁ ≥ … ≥ λ_N ≥ 0.
- R = λ₁/N.   Q = Σλᵢ².   T = 1 − N/Q.   S = Σ_{i≥2} λᵢ².

## Proof skeleton (4 moves — memorize the ORDER)
1. **Lemma (trace):** diagonal of C is all 1's ⇒ trace = N; trace = Σλᵢ ⇒ **Σλᵢ = N.**
   (Why trace = Σλᵢ? C = QΛQᵀ, trace(QΛQᵀ)=trace(Λ) via trace(AB)=trace(BA).)
2. **Theorem 1 (identity):** Q = λ₁² + S = (NR)² + S ⇒ **T = 1 − N/((NR)² + S).**
3. **Theorem 2 (bounds):** the N−1 tail eigenvalues are ≥ 0, sum to μ = N(1−R).
   - Lower (Cauchy–Schwarz, aᵢ=λᵢ, bᵢ=1):  μ² ≤ (N−1)·S ⇒ **S ≥ N²(1−R)²/(N−1).**
   - Upper (non-negativity):  (Σλᵢ)² = Σλᵢ² + 2·(≥0 cross terms) ⇒ **S ≤ N²(1−R)².**
4. **Substitute:** T increases in S ⇒ plug S-min for T's floor, S-max for its ceiling.
   T is trapped in a band determined by R and N.

## Corollary (say it)
Relative error of dropping S:  S/λ₁² ≤ ((1−R)/R)²  ⇒  T ≈ 1 − 1/(NR²), exact as R→1.

## Equality conditions (they WILL ask)
- Lower bound tight ⇔ all tail eigenvalues **equal** (residual structure perfectly even).
- Upper bound tight ⇔ only **one** tail eigenvalue non-zero (fully concentrated).

## Rapid-fire answers (one line each)
- **Trace = N?** unit diagonal.
- **Why bᵢ=1?** turns "known sum μ" into a statement about "sum of squares S."
- **Need Cauchy–Schwarz for upper bound?** No — just non-negative cross terms.
- **Negative eigenvalue?** breaks the **upper** bound only (lower needs no sign).
- **Correlation not covariance?** unit diagonal ⇒ trace = N; covariance = scale-dependent.
- **Why bounds not exact S?** (R,N) fix only the *sum* μ, not the full spectrum.
- **Cauchy–Schwarz vs Jensen/Hölder?** identical here (Jensen on x², Hölder p=q=2).
- **Does it prove topology?** No — eigenvalue coordinate only; corr(R, PH) ≈ −0.37.
- **Tighter possible?** Yes — fixing λ₂ narrows the band; I use R,N for a clean form.
- **Someone proves tighter later?** Refines, doesn't invalidate — mine stays true.

## Novelty statement (memorize — this answers "what's new?")
"We derive, within the proposed Fragility Space framework, an exact identity and
closed-form two-sided bounds relating the effective-rank coordinate to the dominant
eigenvalue, with an error term that characterizes when the dominant-mode approximation
holds — and validate it across markets."
*(Individual tools — RMT, TDA, Hawkes, Ricci — are NOT the novelty; the integration +
this structural result + the honest evaluation are. Pending final literature check.)*

## Limitations (state them BEFORE they're asked)
- Theorem is about the eigenvalue-based coordinate only (not PH / Hawkes).
- Bounds use only R and N (looser in calm, low-R markets — widest band there).
- Characterizes fragility; does NOT reliably predict crashes out-of-sample.
- "Within the framework" — not claiming a universal new theorem pending lit review.

## Validation one-liners
- Identity: reproduces T to ~1e-16.  Bounds: hold for all tested N = 8…50.
- corr(T, 1−1/(NR²)) = 0.94; error 0.06 turbulent vs 0.72 calm — matches ((1−R)/R)².

---
**Self-test before the interview:** blank page, reprove Step 3 lower bound
(N−1 non-negative numbers summing to μ ⇒ S ≥ μ²/(N−1)) and state equality. If you can,
you own it.
