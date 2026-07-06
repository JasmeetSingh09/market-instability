# An Econophysics Fragility Space for Financial Markets: Spectral, Structural, and Temporal Signatures of Loss of Independence

*Sample research-paper draft — for review by the strategist/mentor.*
*Author: Jasmeet Singh. Mentor: [TBD].*

---

## COVER NOTE FOR THE STRATEGIST (delete before submission)

**What this is.** A single, coherent applied-mathematics project: we define a
three-coordinate "fragility space" for financial markets and rigorously evaluate
what each coordinate does and does not reveal. It combines Random Matrix Theory,
topology/network geometry, and self-exciting point processes under one thesis.

**Why it is good (honest version).**
1. *One clear contribution*, not ten demos: fragility = loss of statistical
   independence, made a measurable geometric object F = (R, T, H).
2. *Real mathematical depth*: an analytically derived proposition (T ≈ 1 − 1/(NR²))
   with validated breakdown conditions; optimal-transport (Ollivier–Ricci) curvature;
   branching-process criticality of the Hawkes lens.
3. *Statistical rigor uncommon at high-school level*: bootstrap confidence intervals,
   time-series cross-validation, ablation studies, permutation tests, multi-market
   replication, and explicit false-positive-rate reporting.
4. *Intellectual honesty judges reward*: we report negative results as prominently as
   positive ones, and we caught and corrected our own overclaims (e.g., a redundant
   proxy, a "critical transition" that vanishes under a volatility control).

**Why it is ISEF-worthy (and the honest ceiling).** It is a competitive
finalist-level *synthesis-and-evaluation* contribution: rigorous, multi-market,
theoretically motivated, honestly reported. It is **not** a new-theorem or
new-algorithm breakthrough, which is what typically wins top mathematics Grand
Awards. Realistic expectation: competitive at ISEF, plausible for category/special
awards depending on the field and the interview; a Grand Award is possible but should
not be predicted. The strongest remaining levers are the **literature review**
(establishing novelty), the **write-up**, and the student's **defense** of every
derivation — not more code.

---

## Abstract

Financial markets are most dangerous when they cease to behave as many independent
assets and begin to act as a single, synchronized system. We formalize this loss of
statistical independence as a point in a low-dimensional **fragility space**
F(t) = (R, T, H), whose coordinates measure the phenomenon through three distinct
branches of mathematics: **spectral** (Random Matrix Theory; market-mode dominance
R), **geometric** (topology and network geometry; structural collapse T), and
**temporal** (Hawkes self-exciting processes; self-excitation H). Studying this space
across Indian equity, U.S. equity, and cryptocurrency markets (2010–2024), we
establish four results. (1) The spectral and a participation-ratio geometric proxy
are *analytically* redundant under a dominant market mode — we derive
T ≈ 1 − 1/(NR²) and validate its regime-dependent breakdown. (2) Replacing the proxy
with genuine persistent homology yields a geometric coordinate that is statistically
independent of the spectrum (correlation −0.37) but carries no predictive signal,
whereas discrete Ollivier–Ricci curvature predicts crashes (rises significantly
before them) but is 0.91-correlated with the spectrum — revealing a fundamental
independence-versus-informativeness trade-off in market geometry. (3) Structural
degradation significantly *precedes* temporal self-excitation (+12 trading days,
permutation p = 0.026), a staged signature of destabilization. (4) The temporal
coordinate, interpreted as the criticality parameter of an equivalent
branching process, detects volume-matched manipulation that volume-based surveillance
misses; but crashes do not exhibit branching-process critical slowing down on daily
data once volatility is controlled. Consistent with efficient markets, the framework
**characterizes** fragility but does not reliably **predict** crashes out-of-sample —
a boundary we establish with cross-validation and confidence intervals throughout.

**Keywords:** systemic risk, random matrix theory, persistent homology, Ricci
curvature, Hawkes processes, branching criticality.

---

## 1. Introduction

Systemic financial crises — 2008, the March 2020 COVID crash, repeated cryptocurrency
collapses — share a qualitative signature: assets that normally diversify one another
suddenly move together, and risk that appeared spread out concentrates into a single
mode. Intuitively, the market loses *statistical independence*. This paper asks
whether that loss of independence can be made a precise, measurable object, and what
its measurement can and cannot tell us.

Most quantitative approaches to crash detection are either single-method (one
statistic, one lens) or black-box machine learning. We take a different route: we
treat "loss of independence" as one phenomenon visible through three mathematically
distinct microscopes, and we build a common coordinate system — a **fragility
space** — in which each market state is a single point. The scientific value is not
any one lens but the *integration* and, crucially, the *honest evaluation* of what
each coordinate contributes.

Our central finding is deliberately unglamorous and, we argue, correct: fragility can
be **characterized** — its structure, its geometry, its staging over time — far more
reliably than crashes can be **predicted**. We reach this conclusion only after
subjecting every positive-looking result to volatility controls, cross-validation,
and confidence intervals, and we report the resulting negative results as prominently
as the positive ones.

**Econophysics perspective.** We adopt an econophysics framing: markets are treated
as complex systems of many interacting components whose collective, emergent behaviour
— not the rational choices of individual agents — determines systemic stability. This
is a matter of method, not rebranding: the three lenses are established
statistical-physics tools (Random Matrix Theory from Wigner's nuclear spectra; Hawkes
self-excitation from earthquake-aftershock dynamics; phase-space description of complex
systems). The framing does two things. First, it sets the correct expectation: like
physics, we measure the *stability of a system*, not tomorrow's price — so
"characterize, not predict" is the intended goal, not a shortfall. Second, it justifies
why *these* three lenses: each is a physically motivated coordinate of one phenomenon,
the loss of statistical independence. We keep the physics disciplined — we do not claim
literal Bose–Einstein condensation or Ising magnetization, we do not "reject
equilibrium economics," and we do not claim to prove phase transitions or predict
crashes; physical language is used only where the underlying mathematics supports it.

**Contributions.**
1. A formal fragility space F = (R, T, H) unifying spectral, geometric, and temporal
   signatures of loss of independence (Section 3).
2. An analytical proposition explaining spectral–geometric redundancy, with derived
   breakdown conditions (Section 4).
3. A head-to-head evaluation of two geometric coordinates revealing an
   independence-versus-informativeness trade-off (Section 5).
4. A staged-timing result: structure precedes temporal cascades (Section 6).
5. A branching-criticality interpretation of the temporal lens, with an honest
   empirical null and an applied manipulation-detection result (Section 7).

## 2. Data

- **Indian equities (NSE):** 16 large-cap constituents, daily adjusted closes,
  2010–2024 (Yahoo Finance). Nifty (^NSEI) as the market benchmark.
- **U.S. equities and cryptocurrency:** parallel universes for multi-market
  replication (Section 8).
- **Returns:** daily simple/log returns; rolling windows of W = 60 trading days.
- **Crash labels:** a window is "pre-crash" if the benchmark's forward 20-day return
  is below −10%.
- **Limitations:** daily data (not intraday microstructure); current-constituent
  survivorship bias; Yahoo Finance data quality. These are revisited in Section 9.

## 3. The Fragility Space

At each time t, from a trailing window of W daily returns for N assets we form the
sample correlation matrix C_t, with eigenvalues 0 ≤ λ_1 ≤ ... ≤ λ_N summing to N
(the trace constraint). We define three coordinates.

**Spectral coordinate (market-mode dominance).**
  R_t = λ_N / N, range [1/N, 1]. R = 1/N when all modes are equal (maximal
  diversity); R → 1 when one mode dominates (full synchronization). *Econophysics
  reading:* the Marchenko–Pastur bulk represents noise-like collective fluctuation,
  while outlier eigenvalues represent genuine market-wide collective modes.

**Geometric coordinate (structural collapse).** Two candidate definitions are
compared in Section 5: (i) a participation-ratio proxy T = 1 − PR/N with
PR = N²/Σλ² (eigenvalue-based), and (ii) genuine persistent homology of the
correlation-distance point cloud (topology-based). *Econophysics reading:* rising T
resembles a transition from distributed, independent motion toward synchronized
collective motion (a phase-transition *analogy*, not a proven physical transition).

**Temporal coordinate (self-excitation).** As the light coordinate we use a cheap
daily proxy, H_t = lag-1 autocorrelation of squared returns in the window (H = 0 for
independent shocks; larger H for clustering/self-excitation). The richer object of
the same lens — the fitted Hawkes branching ratio n = α/β and its
branching-criticality interpretation — is studied separately as the temporal
experiment (Section 7). We keep the proxy coordinate and the fitted-Hawkes
experiment distinct throughout. *Econophysics reading:* Hawkes clustering captures
cascade-like behaviour, similar to aftershock dynamics and self-organized criticality
in complex systems.

The map F : t ↦ (R_t, T_t, H_t) places every market state in the unit cube, with a
robust pole near (1/N, 0, 0) and a fragile pole near (1, 1−1/N, ~1). We describe this
as a **market-state phase space** — the state space of the system in the
complex-systems sense. (We deliberately do *not* call it a "microstructure" phase
space: the data are mostly daily, not order-book/tick data.) The remainder of the
paper studies the structure of this space and the reach of each coordinate.

**Crash-warning benchmark (2010–2024, NSE).** As a summary, the weighted index
SFI = z(R) + z(T) + z(H) attains crash-warning AUC 0.69, versus spectral 0.65,
geometric 0.63, temporal 0.58, and a plain-volatility baseline 0.53. However
(Section 4, Section 9), this apparent edge is not statistically robust and is partly
an artifact of the sample period; the honest conclusion is characterization, not
prediction.

## 4. Proposition: Why Spectral and Geometric (Proxy) Coordinates Collapse

Empirically corr(R, T_proxy) = 0.97 — the two coordinates are nearly redundant. We
explain this analytically rather than merely observe it.

**Proposition (Dominant Market-Mode Approximation).** With R = λ_N/N and
T = 1 − PR/N, PR = N²/Σλ², if one eigenvalue dominates the spectrum
(Σλ² ≈ λ_N²), then PR ≈ 1/R² and therefore

  **T ≈ 1 − 1/(N R²).**

*Derivation.* T = 1 − (N²/Σλ²)/N = 1 − N/Σλ². Writing Σλ² = λ_N² + S and dropping S
under dominance gives Σλ² ≈ (NR)², hence T ≈ 1 − N/(N²R²) = 1 − 1/(NR²). ∎

Under this assumption T is an explicit increasing function of R, forcing the two to
co-move. **Validation:** corr(T, predicted-T) = 0.94, explaining the empirical 0.97.
**Breakdown conditions:** the neglected term's relative size is bounded by
((1−R)/R)², so the approximation is excellent when the market mode dominates
(mean error 0.06 in turbulent regimes) and poor otherwise (0.72 in calm regimes) —
a prediction the data confirm. This is an analytical approximation with validated
limits — a proposition, not a theorem — and it tells us the *effective* fragility
space is closer to two-dimensional than three whenever the proxy is used.

## 5. Two Geometries: An Independence–Informativeness Trade-off

The Section-4 redundancy is an artifact of defining the geometric coordinate from
eigenvalues. We therefore test genuinely geometric definitions.

**Persistent homology (topology).** Using the correlation distance
d_ij = √(2(1−ρ_ij)) and the H1 persistence of the resulting point cloud, the
topological coordinate correlates only **−0.37** with R (versus +0.97 for the
proxy) — a genuinely distinct measurement. A correlation of −0.37 is *not*
statistical independence; the correct statement is that topology is weakly-to-
moderately correlated with the spectrum and captures distinct information. However,
in an ablation over {spectral, topology, temporal}, adding topology does not improve
crash-warning AUC (spectral 0.649; spectral+topology 0.641), and within matched
spectral quintiles topology does not separate forward behaviour (partial correlations
≈ −0.05). Topology is **independent but not predictive**.

**Ollivier–Ricci curvature (network geometry).** We model the market as a
correlation-weighted network and compute discrete Ollivier–Ricci curvature
κ(x,y) = 1 − W₁(m_x, m_y)/d(x,y), where W₁ is the Wasserstein-1 (optimal-transport)
distance between lazy-random-walk neighbourhood distributions, solved exactly as a
transportation linear program. Average curvature **rises significantly before
crashes** (pre-crash minus baseline +0.017, 95% CI [+0.003, +0.032]), reproducing the
fragility signal reported by Sandhu et al. (2016), and curvature alone attains AUC
0.670 (versus spectral 0.667). But curvature correlates **+0.91** with R and adds no
independent predictive value. Curvature is **predictive but not independent**.

**The trade-off (a central finding).**

| Geometric coordinate | Independence from spectral | Predictive value |
|---|---|---|
| Persistent homology (H1) | independent (−0.37) | none (AUC ≈ 0.53) |
| Ollivier–Ricci curvature | redundant (+0.91) | real (AUC 0.67, rises pre-crash) |

The geometric information that *predicts* fragility is essentially the same
information the spectral lens already captures (synchronization), while the geometric
information that is *genuinely independent* (topological loops) does not predict.
There is no free lunch: on this data, predictive geometric fragility and spectral
synchronization are the same phenomenon.

## 6. Staged Timing: Structure Precedes Cascades

Testing the ordering of the three signatures before crashes, geometric and spectral
degradation peak ~22–24 trading days before onset, whereas temporal self-excitation
peaks ~11 days out. The structure-minus-temporal lead is **+12 days, 95% CI [+3, +20],
permutation p = 0.026** — statistically significant: structural collapse precedes
temporal self-exciting cascades. This staged signature is a genuine, interpretable
statement about *how* fragility unfolds, though it rests on n = 13 crashes and should
be re-checked on more markets.

## 7. The Temporal Lens: Branching Criticality and Manipulation

**Model.** Extreme events are modelled as a Hawkes process with intensity
λ(t) = μ + Σ α e^(−β(t−t_i)); the branching ratio n = α/β is estimated by maximum
likelihood.

**Branching-criticality interpretation.** Via the cluster representation, a Hawkes
process is equivalent to a Galton–Watson branching process whose mean offspring
number is exactly n. The expected cascade size from one shock is
1 + n + n² + ... = 1/(1−n), which **diverges as n → 1** — a genuine phase transition
separating a stable (subcritical, n < 1) regime from an explosive one, and the exact
condition for Hawkes stationarity. Approaching n = 1 is the point-process form of
critical slowing down (AR(1) → 1, variance → ∞).

**Empirical test (honest null).** On daily NSE data we tracked n, lag-1
autocorrelation, and variance before crashes with bootstrap CIs, volatility controls,
and false-positive-rate reporting. The branching ratio does *not* approach 1 before
crashes (mean n ≈ 0.13, strongly subcritical), and every apparent pre-crash signal
**vanishes once volatility is controlled**, with false-positive rates at the base
rate. Conclusion: crashes do not exhibit clean branching-process critical slowing
down at the daily scale — consistent with a volatility-driven rather than a
critical-transition account. Genuine self-excitation, if present, would require
intraday/order-book data.

**Applied result (manipulation detection).** On volume-matched simulations, the
branching ratio detects "stealth" pump-and-dumps that volume-based surveillance
misses: branching-ratio PR-AUC ≈ 0.99 (base rate 0.15) with false-positive rate 0.00
at 80% recall, versus volume PR-AUC ≈ 0.39. Real cryptocurrencies self-excite
(Bitcoin n ≈ 0.6). This is the framework's clearest societal application, currently
validated on simulation pending labelled real-world pump data.

## 8. Multi-Market Replication

Across Indian equities, U.S. equities, and cryptocurrency, extreme-move
self-excitation is remarkably consistent (branching ratio n ≈ 0.57–0.60), and
Random-Matrix covariance cleaning lowers global-minimum-variance portfolio volatility
in every market (largest reduction in the noisiest market, crypto). Universal
behaviour (self-excitation, benefit of cleaning) is thus separated from
market-specific behaviour (crypto's higher volatility and larger cleaning benefit).

## 9. Limitations

- **Prediction ceiling.** Out-of-sample, cross-validated crash-warning AUC (0.589) is
  well below in-sample (0.693), and a trivial average-correlation benchmark (0.630)
  matches the full composite. The framework characterizes; it does not predict.
- **Period artifact.** 2010–2024 excludes 2008, weakening the volatility benchmark;
  conclusions lean on the cross-market and structural results, not the raw AUCs.
- **Daily-data caveat.** The Hawkes branching ratio on daily data may partly reflect
  ordinary volatility clustering rather than microstructural self-excitation.
- **Sample sizes.** The staged-timing result uses n = 13 crashes.
- **Simulation.** The manipulation result awaits labelled real pump data.
- **Survivorship bias.** Current constituents.

## 10. Conclusion

We introduced a fragility space that unifies spectral, geometric, and temporal
signatures of a market's loss of statistical independence, and we evaluated it with
uncommon rigor. The framework's value is a precise, honest map of what each
mathematical lens contributes: spectral dominance and temporal self-excitation carry
real signal; the two are staged in time; the geometric lens faces an
independence-versus-informativeness trade-off; and, across markets, fragility is
characterizable but crashes remain largely unpredictable. The project's contribution
is this integration and its disciplined evaluation — including the negative results —
rather than a claim to predict the unpredictable.

## References (seed list — to be completed in the literature review)

- Marchenko & Pastur (1967). *Distribution of eigenvalues for some sets of random matrices.*
- Laloux, Cizeau, Bouchaud & Potters (1999). *Noise dressing of financial correlation matrices.*
- Gidea & Katz (2018). *Topological data analysis of financial time series: Landscapes of crashes.*
- Sandhu, Georgiou & Tannenbaum (2016). *Ricci curvature: An economic indicator for market fragility and systemic risk.* Science Advances.
- Ollivier (2009). *Ricci curvature of Markov chains on metric spaces.*
- Hawkes (1971). *Spectra of some self-exciting and mutually exciting point processes.*
- Bacry, Mastromatteo & Muzy (2015). *Hawkes processes in finance.*
- Kulkarni et al. (2023); Rai et al. (2024) — recent TDA-of-markets work (to position novelty).
