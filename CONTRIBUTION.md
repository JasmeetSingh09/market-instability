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

## 6. Claim discipline — say these, never say those

A defense checklist. Every claim below is exactly what the evidence supports; the
"avoid" list is where past drafts (and stale copies) overreached.

**Claims to make (supported):**
- We **characterize** fragility; we do **not** claim reliable crash prediction
  (out-of-sample CV AUC 0.589; a trivial avg-correlation benchmark matches the composite).
- The spectral coordinate and the **participation-ratio geometric proxy** are
  analytically linked under a dominant market mode — the Proposition T ≈ 1 − 1/(NR²),
  validated (corr 0.94) with derived breakdown conditions.
- The geometric lens shows an **independence-vs-informativeness trade-off**: true
  persistent homology is weakly-correlated with spectral (−0.37) but not predictive;
  Ollivier–Ricci curvature predicts (rises pre-crash, AUC 0.67) but is redundant with
  spectral (+0.91).
- Structural degradation **precedes** temporal clustering (+12 trading days,
  permutation p = 0.026) in the current tests (n = 13 crashes — small sample).
- A fitted **Hawkes** module detects *simulated* volume-matched pump-and-dumps that
  volume surveillance misses; real labelled pump data is still needed.
- On daily data, crashes do **not** approach branching-process criticality (n → 1)
  once volatility is controlled — an honest null (mean n ≈ 0.13).

**Claims to avoid (unsupported / overreach):**
- Do **not** say the fragility index reliably beats volatility for crash prediction.
- Do **not** call the participation-ratio coordinate "TDA," and do **not** call daily
  squared-return autocorrelation a true Hawkes branching ratio (coordinate ≠ experiment).
- Do **not** say the geometric lens is "statistically independent" — −0.37 is not
  independence; say "weakly-to-moderately correlated / complementary."
- Do **not** claim Ricci curvature adds *independent* predictive value (it is +0.91
  redundant with the spectral lens).
- Do **not** say manipulation detection is proven on real markets (it is simulation).
- Do **not** imply RMT, TDA, Hawkes, or Ricci curvature are new — the novelty is the
  integrated characterization and its honest evaluation.

## 6b. Synthesis — the conclusion table (this IS the paper's conclusion)

The central question is no longer *"does Fragility Space predict crashes?"* (it does
not, significantly). It is *"what does the framework reveal that existing methods do
not?"* The whole project reduces to four answered questions:

| Question | Answer | Evidence |
|---|---|---|
| Is fragility predictable? | No significant improvement over simple baselines | 9-market bootstrap CIs all include 0 |
| Is fragility universal across crises? | No — crises are heterogeneous | Crisis-trajectory correlations ≈ 0 |
| Is the spectral lens alone enough? | No — its coupling to geometry is regime-dependent | corr(R,T): −0.09 calm → −0.36 crisis |
| Why multiple lenses, then? | Each captures behaviour the others miss | cross-lens evaluation (below) |

## 6c. What each lens reveals that existing methods cannot (the discussion spine)

For every finding, the scientifically valuable question is *why couldn't a standard
method already tell us this?*

- **Regime-dependent coupling (Finding 1):** *volatility* cannot reveal it — volatility
  is a single scalar with no notion of the *relationship between* two structural
  descriptors; *PCA* cannot, because PCA gives the spectrum but not its link to the
  independent topological signal. Only holding spectral and topological coordinates
  *together* exposes that their agreement is a crisis phenomenon.
- **Crisis heterogeneity (Finding 2):** *volatility/VIX* cannot reveal it — every crisis
  looks like "high volatility," so a scalar cannot distinguish crisis *types*; the
  multi-coordinate trajectory can show that the *path* differs.
- **No predictive edge (Finding 3):** *Hawkes alone* cannot establish this — it took the
  honest composite-vs-baselines evaluation, across markets, to show the framework's
  value is characterization, not prediction. The negative result is itself the
  contribution.

**The one-paragraph identity of the paper (embrace the evolution):**
> *"We investigate how different mathematical perspectives describe systemic market
> fragility. Some relationships strengthen during crises (spectral–geometric coupling),
> some vanish in calm markets, crises do not share a universal trajectory, and widely
> used predictive intuitions do not generalize across markets. Our contribution is an
> interpretable framework that makes those distinctions explicit."*

## 7. What NOT to do now (per the frozen-scope decision)

No new lenses, no quantum/chaos/entropy/GNN analogies. From here the only changes
allowed are: **better validation, cleaner proofs, better reproducibility, better
writing.** The project should get *clearer and more defensible*, not *bigger*.
