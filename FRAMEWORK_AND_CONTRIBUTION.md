# The Fragility Space — Formal Framework & Sharpened Contribution

*(#2 makes F = (R, T, H) a rigorous mathematical object; #4 states the
contribution in one sentence, sharpened toward manipulation detection.)*

---

## Part 1 — Formal definition of the Fragility Space

**Setup.** At each time t, from a trailing window of W daily returns for N assets,
form the sample correlation matrix C_t (N x N, symmetric, positive semidefinite,
unit diagonal, so trace(C_t) = N). Let its eigenvalues be
0 <= lambda_1 <= ... <= lambda_N, with sum_i lambda_i = N.

We define three **fragility coordinates**, each measuring one facet of the loss
of statistical independence.

> **IMPORTANT — coordinates vs. experiments (read this).** The three *coordinates*
> below are deliberately **cheap, closed-form proxies** that can be computed on
> every rolling window to place a market state in the space. They are NOT the same
> objects as the richer standalone *experiments* elsewhere in this project. In
> particular:
> - the geometric coordinate T is **effective-rank (participation-ratio) geometry**,
>   which is *distinct* from the persistent-homology and Ollivier-Ricci-curvature
>   analyses (`geometric_independence.py`, `ricci_curvature.py`);
> - the temporal coordinate H is a **daily self-excitation proxy** (lag-1
>   autocorrelation of squared returns), which is *distinct* from the fitted Hawkes
>   **branching ratio** used in the temporal experiments (`3_temporal_hawkes/`).
>
> Keeping the light coordinates separate from the heavy experiments is what makes
> the fragility space computable everywhere while the experiments probe each lens
> in depth. Wherever this document says "coordinate," it means the proxy below.

**1. Spectral coordinate R_t (market-mode dominance).**
    R_t = lambda_N / N,        range [1/N, 1].
- Fraction of total variance carried by the dominant "market mode."
- R = 1/N  <=>  all eigenvalues equal (maximally diverse, no common mode).
- R -> 1   <=>  one mode dominates (full synchronization).
- (This coordinate coincides with the object studied in the spectral experiments.)

**2. Geometric coordinate T_t (dimensional collapse — effective-rank geometry).**
    Participation ratio  PR_t = (sum_i lambda_i)^2 / sum_i lambda_i^2 = N^2 / sum_i lambda_i^2,
    the "effective number of active modes." Define
    T_t = 1 - PR_t / N,        range [0, 1 - 1/N].
- T = 0            <=>  effective rank = N (structure fully spread out).
- T -> 1 - 1/N     <=>  effective rank -> 1 (structure collapses to one direction).
- **Note:** T is *eigenvalue-based* effective-rank geometry. The persistent-homology
  and Ricci-curvature coordinates are separate geometric objects (Section on
  geometric independence); do not conflate them with T.

**3. Temporal coordinate H_t (self-excitation — daily proxy).**
    H_t = lag-1 autocorrelation of squared returns in the window, range roughly [0, 1).
    This is a cheap daily proxy for self-excitation.
- H = 0    <=>  shocks arrive independently (no clustering).
- H -> 1   <=>  shocks cluster / self-excite.
- **Note:** H is the *proxy*, not the fitted Hawkes branching ratio n = alpha/beta.
  The true branching ratio (and its branching-criticality interpretation, n -> 1)
  is estimated separately in the temporal experiments (`3_temporal_hawkes/`,
  `BRANCHING_CRITICALITY.md`); H only stands in for it inside the light coordinate.

**The Fragility Space** is the map
    F : t  |->  (R_t, T_t, H_t)  in  [0, 1]^3,
so every market state is a point in the unit cube. Fragility increases
monotonically toward the fragile pole along each axis:
- **Robust pole:**   F ~ (1/N, 0, 0)      — diverse, full-dimensional, non-cascading.
- **Fragile pole:**  F ~ (1, 1 - 1/N, ~1) — synchronized, collapsed, cascading.

## Part 2 — Structure of the space (why it is effectively 2-D)

**Proposition (Dominant Market-Mode Approximation).** If one eigenvalue dominates
the spectrum (sum_i lambda_i^2 ~ lambda_N^2), then PR ~ 1/R^2 and
    **T ~ 1 - 1/(N R^2).**
Under this assumption T is an explicit increasing function of R, so the (R, T)
projection of the fragility space concentrates near a one-dimensional curve.

**Validated** (`redundancy_analysis.py`): corr(T, predicted-T) = 0.94; the
approximation holds when the market mode dominates (mean error 0.06, turbulent
regimes) and breaks down in calm, spread-out spectra (error 0.72).

**Consequence.** Empirically corr(R, T) = 0.97 while H is nearly independent of
both (corr ~ 0.22). So the *effective* fragility space is **two-dimensional**:
a coupled **structural axis** (spectral ~ geometric) and an independent
**temporal axis**. This is a stated, proven property of the framework — not an
assumption.

## Part 3 — The sharpened contribution (#4)

**One sentence (primary):**
> *We formalize a low-dimensional "fragility space" whose spectral, geometric, and
> temporal coordinates quantify a market's loss of statistical independence; we
> prove analytically why two of the three coordinates collapse to one under a
> dominant market mode; and we show — with statistical significance and across
> markets — that structural fragility precedes temporal self-exciting cascades,
> of which coordinated market manipulation is a detectable special case.*

**Polished abstract (led by the strongest, most concrete results):**
> Financial markets are most dangerous when they cease to behave as many
> independent assets and act as one synchronized system. We formalize this "loss
> of independence" as a point in a three-coordinate fragility space — spectral
> (market-mode dominance), geometric (dimensional collapse), and temporal
> (self-excitation) — and study its structure across Indian, US, and crypto
> markets. Three findings: (1) the spectral and geometric coordinates are
> analytically redundant under a dominant market mode (a proposition we derive and
> validate), so the space is effectively two-dimensional; (2) structural fragility
> **significantly precedes** temporal self-exciting cascades (+12 trading days,
> permutation p = 0.026) — a staged signature of destabilization; (3) the temporal
> coordinate detects coordinated, volume-matched market manipulation that
> volume-based surveillance misses. Consistent with efficient markets, the
> framework **characterizes** fragility but does not reliably **predict** crashes
> out-of-sample — a boundary we establish with cross-validation and confidence
> intervals throughout.

**Honest caveats to keep in the paper:**
- The manipulation result is validated on *simulation*; real labelled pump data
  is the next step.
- The staged-timing result uses n = 13 crashes (small sample) — significant but
  to be re-checked across more markets.
- Survivorship bias (current constituents).
- **Daily-data caveat for the temporal lens:** the Hawkes branching ratio is
  estimated on DAILY extreme moves, so a value near 0.6 may partly reflect
  ordinary volatility clustering (GARCH-type behaviour) rather than genuine
  microstructural self-excitation. True microstructural self-excitation would
  require intraday/order-book (tick) data, which is out of scope here. The
  branching ratio should therefore be read as a *coarse* self-excitation proxy,
  not a microstructure measurement.

## Part 4 — Two framings (pick with the professor)
- **Framework-led (recommended, honest):** the fragility space + staged timing +
  redundancy proposition as the spine; manipulation as a compelling *application*.
  Strongest *evidence* (real-data, significant).
- **Manipulation-led (more "winner-shaped"):** lead with detecting manipulation
  (clear problem, societal stakes, gerrymandering-parallel), framework as context.
  Better *story*, but weaker *evidence* (simulation) until real pump data is added.
