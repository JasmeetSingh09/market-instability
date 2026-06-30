# Research Paper Skeleton — "Three Mathematical Lenses on Market Instability"

> **How to use this file.** This is a *scaffold*, not the paper. The abstract is a
> draft to react to and rewrite in your own voice. Each section lists what belongs
> there and slots in the results we already have. Anything marked **[YOU WRITE]** is
> yours to write and must reflect your own understanding — you will be interviewed
> on every equation, so do not include anything you cannot explain at a whiteboard.

---

## Working title
*Three Mathematical Lenses on Market Instability: Spectral, Geometric, and
Temporal Signatures of Systemic Fragility in Indian and Crypto Markets*

## Abstract (draft — ~230 words; rewrite in your voice)
Financial markets are most dangerous when they stop behaving as a collection of
independent assets and begin to act as a single, synchronized system — the regime
in which crashes and coordinated manipulation occur. This work asks whether that
loss of independence can be detected, and characterizes it through three distinct
branches of mathematics applied to Indian equity (NSE) and cryptocurrency data.
First, using **Random Matrix Theory**, we show that the overwhelming majority of a
market correlation matrix is statistical noise: empirical eigenvalues fall inside
the Marchenko–Pastur band, and cleaning the noise eigenvalues yields global
minimum-variance portfolios with lower, more stable, and more honestly-estimated
out-of-sample risk than the raw sample covariance — an advantage that grows
monotonically with the noise ratio q = N/T, exactly as theory predicts. Second,
using **Topological Data Analysis** (persistent homology of the correlation
structure), we conduct a rigorous out-of-sample audit and find that, once the
volatility confound and major crashes such as 2008 are properly included,
topological early-warning signals do **not** add statistically significant
predictive power over simple volatility — a cautionary, negative result that
corrects optimistic prior claims. Third, modeling extreme events as a
**Hawkes self-exciting point process**, we show that real markets exhibit strong
self-excitation (Bitcoin branching ratio ≈ 0.77) and that the branching ratio
detects volume-matched "stealth" pump-and-dumps that volume-based surveillance
cannot. Together these lenses give a spectral, geometric, and temporal
characterization of market fragility.

**Keywords:** random matrix theory, persistent homology, Hawkes processes,
systemic risk, market manipulation.

---

## 1. Introduction  **[YOU WRITE]**
- The problem: systemic risk / loss of independence (motivate with 2008, 2020, crypto pumps).
- The gap: most student/retail work uses black-box ML; we use principled mathematics.
- The contribution: one unifying question, three mathematical lenses; honest results
  (two positive, one negative).
- One paragraph roadmap of the paper.

## 2. Background & Related Work  **[YOU WRITE — with these anchors]**
- **RMT:** Marchenko–Pastur (1967); Laloux, Cizeau, Bouchaud, Potters (1999).
- **TDA:** persistent homology; Gidea & Katz (2018); Kulkarni et al. (2023); Rai et al. (2024).
- **Hawkes:** Hawkes (1971); Bacry, Mastromatteo & Muzy (2015).
- State clearly what is *new here*: the controlled, out-of-sample, cost-aware
  comparison and the unified three-lens framing.

## 3. Data
- NSE: ~37 liquid stocks, 2010–2024 (list, source = Yahoo Finance, daily adjusted).
- Crypto: BTC-USD 5-min bars, 60 days.
- Preprocessing: log returns, alignment, crash labelling (Nifty −10% over 20 days).
- **[YOU WRITE]** a short data-quality / limitations note.

## 4. Method 1 — Spectral (Random Matrix Theory)
- Theory: MP law, band edges λ± = σ²(1±√q)², branching of eigenvalues into noise vs signal.
- Cleaning: keep eigenvectors above λ₊, replace sub-band eigenvalues by their average (trace-preserving).
- Portfolio: global minimum variance w ∝ Σ⁻¹1; walk-forward, monthly rebalance, 10 bps cost.
- **Figure:** `rmt_eigenvalue_spectrum.png`.
- **[YOU WRITE]** derivation of why σ² = 1 − λ_max/N and the GMV solution.

## 5. Method 2 — Geometric (Topological Data Analysis)
- Construction: rolling correlation matrix → distance d_ij = √(2(1−ρ_ij)) → Vietoris–Rips → H0/H1.
- Summaries: L1/L2 lifespan norms, persistent entropy, Wasserstein change-rate.
- Evaluation: AUC vs volatility baseline; the volatility confound; bootstrap significance; the 2008 period control.
- **Figure:** `tda_persistence_diagram.png`, `tda_figure.png`.

## 6. Method 3 — Temporal (Hawkes Processes)
- Model: λ(t) = μ + Σ α e^(−β(t−tᵢ)); branching ratio n = α/β.
- Estimation: exact log-likelihood (O(N) recursion), MLE; Ogata-thinning simulation.
- Experiment: volume-matched normal (Poisson) vs pump (Hawkes); branching-ratio AUC vs volume AUC.
- **Figure:** `hawkes_intensity.png`.
- **[YOU WRITE]** the log-likelihood derivation (you WILL be asked this).

## 7. Results
| Lens | Key quantitative result |
|---|---|
| RMT | cleaned vs raw GMV: realised vol 14.3%→13.2%, Sharpe 1.35→1.37; RMT edge grows with q (at q=0.93, raw Sharpe −0.13 vs RMT 1.41) |
| TDA | best topology + volatility lift = +0.015 AUC, 95% CI [−0.008, +0.040] → **not significant**; de-risk strategy underperforms buy-and-hold |
| Hawkes | BTC branching ratio ≈ 0.77; branching-ratio AUC 1.00 vs volume AUC ≈ 0.39 on volume-matched pumps (simulation) |

## 8. Discussion  **[YOU WRITE]**
- Why two lenses carry signal and one does not — interpret.
- The unifying theme: synchronization / loss of independence.
- Practical implications (portfolio risk; market surveillance for regulators).

## 9. Limitations  **[YOU WRITE — be honest, judges reward this]**
- Hawkes AUC = 1.00 is on clean simulations; real labelled pump data needed.
- Univariate Hawkes; daily data for RMT/TDA (not intraday microstructure).
- Yahoo Finance data quality; survivorship bias in the stock list.
- TDA result is for these specific constructions; landscapes/RIE estimators untested.

## 10. Conclusion & Future Work  **[YOU WRITE]**
- Restate the three findings and the honest mixed verdict.
- Future: multivariate Hawkes, rotationally-invariant (Ledoit–Péché) estimators,
  larger universe to push q higher, labelled manipulation dataset.

## References
- Marchenko & Pastur (1967). *Distribution of eigenvalues for some sets of random matrices.*
- Laloux, Cizeau, Bouchaud, Potters (1999). *Noise dressing of financial correlation matrices.*
- Gidea & Katz (2018). *Topological data analysis of financial time series: Landscapes of crashes.*
- Hawkes (1971). *Spectra of some self-exciting and mutually exciting point processes.*
- Bacry, Mastromatteo, Muzy (2015). *Hawkes processes in finance.*
- López de Prado (2018). *Advances in Financial Machine Learning.* (for the cross-validation / DSR rigor)

---

### Honesty checklist before submission
- [ ] Every equation in the paper — can you derive it on a whiteboard?
- [ ] Every figure — can you explain what each axis and point means?
- [ ] The negative TDA result is reported as prominently as the positive ones.
- [ ] Limitations are specific, not generic.
- [ ] You wrote the prose; the scaffold/code was a tool, like a calculator.
