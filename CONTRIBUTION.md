# The Contribution — one thesis, everything else is evidence for it

> **Read this first.** This project has many parts (RMT, TDA, Hawkes, a proposition,
> branching criticality, Ricci curvature). That is a strength only if they serve
> ONE idea. This file states that one idea and shows how every other piece is
> *supporting evidence*, not a separate project. If a judge asks "what is your main
> contribution?", the answer is the single paragraph in §1 — nothing else.

---

## 1. The one-sentence contribution

> **We formalize systemic financial fragility as the progressive loss of
> statistical independence among assets, represented as a point in a low-dimensional
> "fragility space" with spectral, geometric, and temporal coordinates; and we
> rigorously establish what each representation does and does not contribute —
> finding that fragility can be *characterized* far more reliably than crashes can
> be *predicted*.**

That is the whole project. One framework, three coordinates, and an honest map of
their reach. Everything below is evidence for this sentence.

## 2. Why this is a single idea, not three methods

The unifying concept is **loss of statistical independence**. A healthy market is
many assets moving independently; a fragile market synchronizes into effectively one
degree of freedom. That *one* phenomenon leaves a fingerprint in three different
branches of mathematics:

| Coordinate | Branch | What "loss of independence" looks like |
|---|---|---|
| **R** — spectral | Random Matrix Theory | one eigenvalue (market mode) swallows the variance |
| **T** — geometric | topology / network geometry | the correlation structure collapses in shape |
| **H** — temporal | Hawkes / point processes | shocks stop arriving independently and self-excite |

The market state at time t is the point **F(t) = (R, T, H)** in a fragility space.
The contribution is this *space and its honest evaluation* — not any one lens.

> *Coordinates vs. experiments:* the fragility-space **coordinates** are cheap
> closed-form proxies (T = effective-rank/participation-ratio geometry; H = lag-1
> autocorrelation of squared returns). The deeper **experiments** use richer objects
> of the same lens — persistent homology and Ollivier–Ricci curvature for geometry,
> and the fitted Hawkes branching ratio for the temporal lens. The proxies place
> every window in the space; the experiments probe each lens in depth. See
> [`FRAMEWORK_AND_CONTRIBUTION.md`](FRAMEWORK_AND_CONTRIBUTION.md) Part 1.

## 3. How every piece supports the one thesis (the hierarchy)

**Core (the spine — this is the contribution):**
- The fragility space F = (R, T, H) and the claim *characterize ≫ predict*, backed
  by ablation, time-series cross-validation, bootstrap CIs, and multi-market tests.

**Supporting evidence for "the coordinates are real and complementary":**
- *Spectral works:* RMT cleaning lowers portfolio risk exactly as q = N/T grows.
- *Temporal is the most useful precursor:* it adds the most crash-warning lift and
  detects volume-matched manipulation that volume surveillance misses.
- *Structure precedes cascades:* geometric/spectral degradation leads temporal
  self-excitation by ~12 days (permutation p = 0.026) — a staged signature.

**Supporting evidence for "we know the LIMITS of each coordinate" (the honesty that
judges reward):**
- *The Proposition:* under a dominant market mode, T ≈ 1 − 1/(NR²), so spectral and
  the participation-ratio geometric proxy are analytically redundant — with derived
  breakdown conditions. (Explains *why* two coordinates can collapse to one.)
- *Geometric lens, tested honestly two ways:*
  - persistent homology (true topology) is **independent** of spectral (−0.37) but
    carries **no predictive** signal;
  - Ricci curvature **predicts** (rises pre-crash, AUC 0.67) but is **redundant**
    with spectral (+0.91).
  - → the non-obvious finding: *predictive geometric fragility and spectral
    synchronization are, on this data, the same phenomenon — there is no free lunch.*
- *Branching criticality:* the temporal coordinate is the criticality parameter of a
  Galton–Watson process (cascade size 1/(1−n) diverges at n=1); tested empirically,
  crashes do **not** approach criticality on daily data once volatility is controlled
  — an honest null that bounds the interpretation.

**Every supporting item answers a question a judge would ask about the spine.** None
of them is a separate headline. That is the discipline that keeps the project
coherent.

## 4. What is genuinely new (novelty, stated modestly)

Not new: RMT cleaning, persistent homology on markets, Hawkes in finance, Ricci
curvature for fragility (Sandhu 2016) — all exist. What is new *here* is the
**integration + honest evaluation**:
1. A single fragility-space formalism unifying the three lenses as coordinates.
2. The analytical **Proposition** (T ≈ 1 − 1/(NR²)) explaining spectral–geometric
   redundancy, with validated breakdown conditions.
3. The **head-to-head geometric test** revealing the independence-vs-informativeness
   trade-off (topology independent-but-uninformative; curvature informative-but-
   redundant).
4. The disciplined *characterize ≫ predict* conclusion, established with
   cross-validation and CIs and reported honestly across markets — including nulls.

This is a **synthesis-and-evaluation** contribution, not a new-theorem contribution.
Stated plainly, that is a competitive, defensible ISEF-finalist contribution — and
pretending it is more would be the fastest way to lose credibility.

## 5. The elevator answers (memorize these)

- **"What did you do?"** → the §1 sentence.
- **"What's the single most interesting finding?"** → "Predictive geometric fragility
  turned out to be the same information as spectral synchronization — the truly
  independent geometric signal (topology) doesn't predict, and the predictive one
  (curvature) isn't independent. So the market's fragility is effectively
  lower-dimensional than three lenses suggest."
- **"Why should anyone care?"** → risk management sees fragility building; regulators
  get a manipulation signal volume misses; and we honestly delimit where each tool
  works.
- **"What's the limitation?"** → crashes largely resist prediction; our value is
  characterization, and the temporal lens needs intraday data to test true
  microstructural self-excitation.

## 6. What NOT to do now (per the frozen-scope decision)

No new lenses, no quantum/chaos/entropy/GNN analogies. From here the only changes
allowed are: **better validation, cleaner proofs, better reproducibility, better
writing.** The project should get *clearer and more defensible*, not *bigger*.
