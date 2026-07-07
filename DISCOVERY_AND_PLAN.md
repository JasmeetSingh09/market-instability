# Discovery, Research Questions & Pre-Registered Plan

*The reviewer's challenge: "What is the single sentence no other paper can honestly
claim, but yours can?" and "don't decide the conclusion before the data." This file
answers the first and pre-registers the experiments for the second — questions and
success criteria written BEFORE running them, so the data decides.*

> **Ownership rule (non-negotiable).** Every experiment below must be run, understood,
> and defensible by Jasmeet. The plan is the scaffold; the science is his. Nothing
> here asserts a result we have not measured.

---

## 1. The candidate discovery (already in the repo — articulate this)

The strongest single, non-obvious finding we already have is NOT a new theorem — it is
a structural fact about market fragility:

> **Discovery sentence (defensible today):** *"On the data studied, the geometric
> information that predicts fragility is essentially the same information the spectral
> lens already carries (synchronization): the topologically **independent** signal
> (persistent homology, corr ≈ −0.37 with spectral) does **not** predict crashes,
> while the geometric signal that **does** predict (Ricci curvature) is ≈0.91
> redundant with the spectral market mode. Predictive geometric fragility and spectral
> synchronization are, empirically, the same phenomenon."*

Why this qualifies as a discovery (not a restatement): prior work treats spectral,
topological, and curvature measures as *complementary* lenses. We show — with a
head-to-head evaluation — that for *prediction*, the "independent" lens is
uninformative and the "informative" lens is redundant. That trade-off is the thing
"nobody noticed," and it is measured, not asserted.

**This is the sentence to lead the paper and the interview with.** Everything below
tests whether it holds more broadly, and whether the temporal lens is the true
exception.

---

## 2. Research questions — pre-registered (hypothesis + design + ALL possible outcomes)

For each: we state the hypothesis, the exact experiment, and — critically — we commit
to reporting **whichever** outcome occurs, including the null.

### RQ-A. Why do spectral and topological measures diverge in calm markets?
- **Hypothesis:** in calm regimes, correlation-based spectral measures are dominated by
  noise/broad factors while topology tracks local structure, so they *diverge*; in
  crises both saturate (synchronization) and *converge*.
- **Design:** compute R and true-persistent-homology T over rolling windows; split into
  calm / stressed / crisis by realized vol terciles; measure corr(R, T) within each
  regime and the lead-lag.
- **Pre-committed outcomes (report any):** (i) they converge only in crises; (ii) they
  diverge in calm; (iii) one leads the other; (iv) no regime dependence (null).
- **RESULT (`rq_a_regime_divergence.py`, NSE 2010–2024, vol terciles):** the coupling is
  **regime-dependent and monotonic** — corr(R, T) = **−0.09 (calm)** → **−0.23
  (stressed)** → **−0.36 (crisis)**. Outcome (i)+(ii): they are **nearly independent in
  calm markets and only couple under stress.** *Refined discovery:* the
  spectral–geometric redundancy is a **crisis phenomenon**; in calm markets the
  topological lens carries genuinely distinct information. (To verify next: does this
  replicate across markets (§3), and does the calm-market topological signal give any
  early warning before R moves?) — Jasmeet to reproduce and own before it enters the
  paper.

### RQ-B. When does Hawkes add information eigenvalues cannot?
- **Hypothesis:** the temporal (Hawkes) lens adds unique warning when self-excitation
  rises *before* the correlation structure changes (e.g. flash crashes, FTX).
- **Design:** around labeled events, compare the timing of (a) spectral R change, (b)
  Hawkes branching-ratio change, (c) combined. Test whether Hawkes leads spectral, with
  bootstrap CIs and a false-positive check on non-event windows.
- **Pre-committed outcomes:** (i) Hawkes consistently leads → temporal lens is the real
  exception to §1; (ii) Hawkes coincident/lagging (null); (iii) mixed by event type.

### RQ-C. Is there a universal fragility transition across markets?
- **Hypothesis:** normalized Fragility trajectories share a common shape before crises.
- **Design:** normalize F=(R,T,H) per market; align windows to each crisis onset; look
  for a common pre-crisis trajectory across asset classes.
- **Pre-committed outcomes:** (i) a shared trajectory exists (report it); (ii) it does
  not — behaviour is market-specific (equally publishable null).

---

## 3. Cross-market benchmark (the standardized dataset)

Compute the *same* quantities (R, effective-rank T, true-PH topology, Ricci curvature,
Hawkes n, Fragility Index) on every market, with labeled crisis windows:

| Market | Period | Key events |
|---|---|---|
| S&P 500 | 1990–2025 | Dot-com, GFC, COVID |
| Nasdaq | 1995–2025 | Tech bubble |
| Nikkei 225 | 1990–2025 | Asian crisis, Abenomics |
| FTSE 100 | 1990–2025 | Brexit, COVID |
| Hang Seng | 1990–2025 | Asian crisis, 2015 |
| Bitcoin | 2013–2025 | Terra/LUNA, FTX |
| Gold | 1990–2025 | Safe-haven regimes |
| US Treasuries | 1990–2025 | 2013 taper, 2022 rate shock |

**Scientific question:** does Fragility Space behave *consistently* across
fundamentally different asset classes, or is it market-specific? Either answer is a
result.

---

## 4. Predictive evaluation protocol (define metrics BEFORE running)

To avoid the "decide the conclusion first" trap, fix the rules now:

- **Warning rule:** a warning fires when the Fragility Index exceeds threshold θ
  (θ chosen on a held-out/earlier period, never on the test crisis).
- **Baselines (must beat these to claim anything):** rolling volatility, VIX (where
  available), dominant eigenvalue R alone, effective rank alone, Hawkes n alone,
  average correlation.
- **Metrics:** lead time (days before onset), false-positive rate on non-crisis
  windows, precision, recall, ROC-AUC / PR-AUC, all with bootstrap CIs.
- **Honest framing:** the question is *"does Fragility Space give earlier or more
  reliable warning than established indicators?"* — NOT "it predicts crashes." If it
  does not beat the baselines, that is the finding, reported as prominently.

---

## 5. Prioritized roadmap (what's mine to scaffold vs. YOURS to own)

| # | Task | Owner | In frozen scope? |
|---|---|---|---|
| 1 | Articulate the §1 discovery sentence in the paper/abstract | **Jasmeet** (I help word it) | writing ✓ |
| 2 | Read the 7 closest papers in full; refine novelty map | **Jasmeet + mentor** | lit review ✓ |
| 3 | Cross-market benchmark pipeline (§3) | I scaffold; **Jasmeet runs & explains** | better validation ✓ |
| 4 | Predictive-vs-baselines evaluation (§4) | I scaffold; **Jasmeet interprets** | better validation ✓ |
| 5 | RQ-A/B/C experiments | I scaffold one at a time; **Jasmeet owns each** | validation ✓ |
| 6 | The one memorable figure (3D Fragility trajectory) | I build; **Jasmeet explains** | figures ✓ |
| 7 | Mock hostile interviews (300+ Qs) | I ask; **Jasmeet answers** | interview prep ✓ |

**Guardrails carried from the whole project:** claim only the framework/integration/
derivation/evaluation (not the tools); "to the best of our knowledge" phrasing; report
every null; and — above all — Jasmeet must be able to defend every line, or it does not
go in the paper.

---

## 6. The immediate next step
Build **Task 3/4 as ONE honest experiment at a time**, starting with the cross-market
computation of the coordinates (so RQ-A and the benchmark share the same pipeline).
Each experiment ships with its result reported honestly — null or not — and Jasmeet
walks through the code before it counts as "his."
