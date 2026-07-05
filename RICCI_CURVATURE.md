# Network Geometry: Discrete Ricci Curvature as a Fragility Lens

*Assimilating "network geometry" (idea 4) into the geometric lens — carefully. The
persistent-homology geometric coordinate is a genuinely distinct measurement but
has no predictive value on our data. Discrete Ricci curvature is a DIFFERENT
geometric object with documented fragility signal (Sandhu, Georgiou & Tannenbaum,
Science Advances 2016). We test whether it succeeds where persistent homology
failed — and report honestly either way.*

---

## 1. The idea in one line

Model the market as a weighted network (assets = nodes, correlations = edges) and
measure the **curvature** of that network. Positive curvature = robust, redundant,
well-connected (sphere-like); negative curvature = fragile, tree-like, bottlenecked
(saddle-like). The hypothesis (Sandhu et al.): as a market becomes fragile it
**synchronizes and contracts**, and its average curvature **rises**.

## 2. Ollivier–Ricci curvature (the defensible math)

Classical Ricci curvature (from differential geometry) measures whether nearby
geodesics converge (positive) or diverge (negative). Ollivier gave a discrete
version using optimal transport that works on any metric space, including graphs.

**Construction.**
- Graph metric: from correlation ρ_ij define distance d_ij = √(2(1 − ρ_ij))
  (the standard correlation distance; ρ = 1 → d = 0, ρ = 0 → d = √2).
- At each node x, a probability measure m_x on its neighbours (a **lazy random
  walk**): mass α stays at x, mass (1 − α) spreads to neighbours in proportion to
  edge strength s_xy = max(ρ_xy, 0). Here α = 1/2.
- For an edge (x, y), compute the **Wasserstein-1 (earth-mover) distance**
  W₁(m_x, m_y): the minimum total "mass × distance" to morph the distribution
  m_x into m_y, using d as the ground cost. This is a linear program (a
  transportation problem) — we solve it exactly with `scipy.optimize.linprog`.
- The **Ollivier–Ricci curvature** of the edge is

    **κ(x, y) = 1 − W₁(m_x, m_y) / d(x, y).**

**Reading κ.** If the two neighbourhoods overlap heavily, little mass must travel,
W₁ is small, κ > 0 (robust). If they are far apart / bottlenecked, W₁ ≈ d, κ ≈ 0
or negative (fragile). This is a genuine optimal-transport quantity — the kind of
mathematics valued in both pure math and quant finance.

## 3. Why this is a *different* object from persistent homology

- Persistent homology (our current geometric coordinate) counts topological
  **loops** (H1) — global connectivity holes. It found no predictive signal.
- Ricci curvature is a **local geometric** quantity (edge-by-edge), aggregated to a
  network average. Different mathematics, different information.
- So this is not "another TDA statistic"; it is a distinct geometric lens with its
  own theorem-backed interpretation (Ricci flow contracts positively-curved spaces).

## 4. The research question (hypothesis, not assertion)

> **Does average Ollivier–Ricci curvature of the market network rise before crashes,
> and does it add crash-warning information beyond the spectral lens — succeeding
> where the persistent-homology geometric coordinate failed?**

## 5. What would count as evidence — and the guardrails

- **Direction:** curvature should *rise* into crises (Sandhu's claim). We test the
  pre-crash vs baseline gap with bootstrap CIs.
- **Unique value:** curvature must improve crash-warning AUC *over the spectral lens
  alone* — the same ablation bar persistent homology failed.
- **Honesty:** if curvature is just another restatement of the market mode (high
  |corr| with R), or adds no AUC lift, we say so. It must earn its place.

## 6. Honest claim boundaries

- ✅ *"Discrete Ollivier–Ricci curvature is a well-defined optimal-transport measure
  of network fragility; we test it as an alternative geometric coordinate."*
- ✅ (if supported) *"Curvature rises before crashes and adds crash-warning
  information beyond the spectral lens."*
- ✅ (if not) *"On daily Indian-equity data, curvature is largely a restatement of
  the spectral market mode and adds little unique predictive value"* — an honest
  null that still resolves which geometric object is worth keeping.
- ❌ Not claiming we invented curvature-based fragility detection (Sandhu 2016 did);
  our contribution is integrating it into the fragility space and testing it head-to-
  head against persistent homology.

---

## 7. Empirical result (`ricci_curvature.py`)

Weekly-step W = 60-day windows, 16 NSE stocks, 724 windows (13 pre-crash). Average
Ollivier–Ricci curvature computed exactly (W₁ transport LP per edge).

| Question | Result |
|---|---|
| (A) corr(curvature, spectral R) | **+0.91** — largely redundant with the market mode |
| (B) Does curvature rise before crashes? | **+0.017, 95% CI [+0.003, +0.032] — YES, significant** |
| (C) Curvature-only crash-warning AUC | **0.670** (vs spectral 0.667) |
| (C) Spectral + curvature AUC | 0.602 — **no unique lift** (they are redundant) |

**Honest conclusion — a genuinely informative outcome (and a nice structural
insight):**

1. **Curvature confirms the theory's direction.** Average Ollivier–Ricci curvature
   **rises significantly before crashes**, exactly as Sandhu et al. predict — the
   network contracts and becomes more positively curved as it synchronizes. This is
   a *positive* result, unlike the persistent-homology lens.
2. **As a standalone fragility signal it works** — curvature-only AUC 0.670 slightly
   *beats* the spectral lens (0.667) and massively beats persistent homology (~0.53).
3. **But it is not an independent new dimension.** corr(curvature, R) = +0.91:
   curvature is largely a *restatement of the market mode*, so it adds no unique
   crash-warning value on top of spectral (combined AUC does not improve).

**The real insight — a trade-off between the two geometric candidates:**

| Geometric coordinate | Independence from spectral | Predictive value |
|---|---|---|
| Persistent homology (H1) | **independent** (corr −0.37) | **none** (AUC ~0.53, no rise) |
| Ollivier–Ricci curvature | **redundant** (corr +0.91) | **real** (AUC 0.67, rises pre-crash) |

So the geometric lens faces a genuine tension: the topological object is
*independent but uninformative*, while the curvature object is *informative but
redundant with the spectrum*. **There is no free lunch — the "geometric" information
that actually predicts fragility is essentially the same information the spectral
lens already captures (synchronization), while the truly independent geometric
information (loops) does not predict.** That is a clean, defensible, non-obvious
finding about the geometry of market fragility — and a better contribution than a
naïve "curvature works!" claim would have been.

**Defensible sentence for the paper:** *"Discrete Ollivier–Ricci curvature reproduces
the known pre-crash rise (Sandhu et al.) and is a strong standalone fragility signal,
but it is ~0.91 correlated with the spectral market mode and adds no independent
predictive value; conversely the topologically independent coordinate (persistent
homology) carries no predictive signal — revealing that predictive geometric
fragility and spectral synchronization are, on this data, the same phenomenon."*
