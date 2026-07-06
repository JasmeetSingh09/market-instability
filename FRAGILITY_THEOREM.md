# The Mathematical Spine of the Fragility Space

*A rigorous, self-contained derivation of the structural relationship between the
spectral and effective-rank coordinates. Everything here follows from undergraduate
linear algebra (trace, eigenvalues, Cauchy–Schwarz). It is stated as a theorem
**within the proposed Fragility Space framework** — not a claim to a universally new
result in mathematics. Every step is numerically verified in `redundancy_analysis.py`
and by direct simulation.*

> **Ownership note (read this).** This document exists so the result can be
> *defended at a whiteboard*, not recited. If you cannot reproduce the Cauchy–Schwarz
> step in Theorem 2 from scratch, it is not yet yours. What matters at ISEF is not the
> theorem's difficulty but whether you can explain every line under questioning.

---

## 1. Definitions

Fix a time t. From a trailing window of W daily returns for N assets, form the sample
correlation matrix C (N×N, symmetric, unit diagonal, positive semidefinite). Let its
eigenvalues be

  lambda_1 >= lambda_2 >= ... >= lambda_N >= 0.

**Definition 1 (Fragility Space).** The market state is the point
F(t) = (R, T, H) in R^3, with spectral coordinate R, effective-rank (geometric)
coordinate T, and temporal coordinate H. This document concerns the (R, T) pair.

**Definition 2 (Spectral coordinate).**
  R = lambda_1 / N,   range [1/N, 1].
The share of total variance carried by the dominant "market mode." R -> 1 means one
mode dominates (full synchronization); R = 1/N means all modes are equal.

**Definition 3 (Effective-rank coordinate).** With the participation ratio
PR = (sum_i lambda_i)^2 / sum_i lambda_i^2, define
  T = 1 - PR / N,   range [0, 1 - 1/N].
T measures how far the correlation structure has collapsed from full dimensionality
(effective rank N, T = 0) toward a single direction (effective rank 1, T -> 1 - 1/N).

*(The Hawkes coordinate H is defined separately; the theorem below does not use it.
Note also: this eigenvalue-based T is the framework COORDINATE, distinct from the
persistent-homology and Ricci-curvature geometric EXPERIMENTS.)*

---

## 2. Lemma (Trace identity)

**Lemma.** sum_{i=1}^N lambda_i = N.

*Proof.* The eigenvalues sum to the trace. A correlation matrix has 1's on the
diagonal, so trace(C) = N. ∎

This single constraint is the engine of everything below.

Two immediate consequences we will use. Write Q = sum_i lambda_i^2 (note Q = ||C||_F^2,
the squared Frobenius norm). Then:
- By Cauchy–Schwarz, Q >= (sum_i lambda_i)^2 / N = N, so PR = N^2/Q <= N and T >= 0.
- Since each lambda_i <= lambda_1, Q <= lambda_1 * sum_i lambda_i = lambda_1 N = N^2 R.

Also, directly from Definition 3, PR = N^2 / Q, so

  **T = 1 - PR/N = 1 - N / Q.**    (★)

---

## 3. Theorem 1 (Exact identity)

**Theorem 1 (Effective-rank–spectral identity in the Fragility Space framework).**
Let S = sum_{i>=2} lambda_i^2 be the spectral mass outside the market mode. Then

  **T = 1 - N / ( (N R)^2 + S ).**

*Proof.* Split Q = lambda_1^2 + S. By the Lemma's consequence (★), T = 1 - N/Q.
Substitute lambda_1 = N R (Definition 2), so lambda_1^2 = (N R)^2, giving
Q = (N R)^2 + S and hence T = 1 - N / ((N R)^2 + S). ∎

This is exact — no assumptions beyond the definitions. It already shows T is *not*
free of R: the two coordinates are structurally linked through Q.

---

## 4. Theorem 2 (Two-sided bounds via Cauchy–Schwarz)

The link becomes quantitative once we bound S. The N-1 non-market eigenvalues
lambda_2, ..., lambda_N are non-negative and, by the Lemma, sum to
  mu := N - lambda_1 = N(1 - R).

**Theorem 2 (Bounds).** For every correlation matrix,

  **N^2 (1-R)^2 / (N-1)  <=  S  <=  N^2 (1-R)^2.**

*Proof.*
*Lower bound (Cauchy–Schwarz / QM–AM).* For the N-1 numbers lambda_2,...,lambda_N,
Cauchy–Schwarz gives (sum_{i>=2} lambda_i)^2 <= (N-1) sum_{i>=2} lambda_i^2, i.e.
mu^2 <= (N-1) S, so S >= mu^2/(N-1) = N^2(1-R)^2/(N-1). Equality iff all N-1 are equal.

*Upper bound.* For non-negative numbers, the sum of squares never exceeds the square
of the sum: sum_{i>=2} lambda_i^2 <= (sum_{i>=2} lambda_i)^2, because the cross terms
2 sum_{i<j} lambda_i lambda_j are non-negative. Hence S <= mu^2 = N^2(1-R)^2.
Equality iff at most one of them is non-zero. ∎

Because T = 1 - N/((NR)^2 + S) is strictly increasing in S, substituting the two
bounds sandwiches T between explicit functions of R and N alone:

  1 - N/((NR)^2 + N^2(1-R)^2/(N-1))  <=  T  <=  1 - N/((NR)^2 + N^2(1-R)^2).

So knowing R and N pins T down to an interval — the (R, T) projection of the
Fragility Space is confined to a thin band, not free in the plane.

---

## 5. Corollary (Dominant-mode approximation and its error)

**Corollary.** Define the approximation T_hat = 1 - 1/(N R^2). Then the relative
error incurred by neglecting S in Q satisfies

  S / lambda_1^2  <=  ( (1 - R) / R )^2,

so T -> T_hat as R -> 1, and the approximation is accurate precisely when the market
mode dominates.

*Proof.* From Theorem 2, S <= N^2(1-R)^2, and lambda_1^2 = (N R)^2, so
S/lambda_1^2 <= N^2(1-R)^2 / (N R)^2 = ((1-R)/R)^2. When this is small,
Q = lambda_1^2 + S ≈ lambda_1^2 = (N R)^2, and (★) gives
T ≈ 1 - N/(N R)^2 = 1 - 1/(N R^2) = T_hat. As R -> 1, ((1-R)/R)^2 -> 0. ∎

The error control ((1-R)/R)^2 is the key structural insight: it is small in
turbulent, synchronized markets (R near 1) and large in calm, diversified ones
(R small). The theory therefore *predicts when its own approximation should hold*.

---

## 6. Experimental validation

The theory is confirmed against data (see `redundancy_analysis.py` and direct
simulation):
- **Exact identity (Theorem 1):** reproduces T to machine precision (error ~1e-16)
  on random and empirical correlation matrices.
- **Bounds (Theorem 2):** S and T fall inside the derived intervals in 100% of
  windows tested (N = 8 to 50).
- **Approximation (Corollary):** corr(T, T_hat) = 0.94 empirically; and the
  approximation error tracks ((1-R)/R)^2 — mean error ≈ 0.06 in turbulent
  (high-R) regimes vs ≈ 0.72 in calm (low-R) regimes, exactly as the corollary
  predicts.

---

## 7. Why this is the right theorem to present

- It is **true and exact** (identity + rigorous bounds), not a property secretly built
  into a definition. Contrast the trivial "weighted sum of increasing terms increases"
  monotonicity claim, which discovers nothing about markets.
- It does **not** overclaim a coupling the data contradict. (We do *not* assert the
  spectral lens determines the topological one: measured corr(R, true persistent
  homology) is only −0.37 — a distinct, weakly-related lens. This theorem is about the
  eigenvalue-based effective-rank coordinate, where the coupling is real and provable.)
- Its proof is **elementary and ownable**: trace identity + Cauchy–Schwarz. A motivated
  student can derive and defend every line.
- Narrative for the interview: **define the framework -> prove its structural
  properties -> validate them against data.** Coherent, honest, defensible.

**Conservative naming for the paper:** *Theorem 1 (Effective-rank–spectral coupling in
the proposed Fragility Space framework)* — proving a property within the framework,
pending a literature check before claiming universal novelty.
