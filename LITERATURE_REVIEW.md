# Literature Review — Systemic Market Fragility through Spectral, Geometric, and Temporal Lenses

> **Honest provenance.** The paper summaries below are drawn from abstracts and
> published descriptions (verified via search), not from a full read of every proof.
> Before submission, **Jasmeet + mentor must read the closest works in full** (marked
> ★) and confirm the positioning. That deeper reading is the research; this document
> is a rigorous, verified *scaffold and synthesis*, not a substitute for it.

---

## 1. Purpose and scope

This review situates the proposed Fragility Space framework relative to prior work in
four areas whose tools it uses — **spectral (Random Matrix Theory)**, **geometric
(network curvature)**, **topological (persistent homology)**, and **temporal
(self-exciting point processes)** — and relative to prior **integrated / systemic-risk**
frameworks. The goal is to state precisely *what is established* (so the project claims
none of it) and *where the narrow, defensible contribution lies*.

The central honesty of this review: **every individual tool is mature**, and recent
work is actively *combining* them. The contribution is therefore not any lens but a
specific synthesis — and the review is written to make that boundary unmistakable.

**Figure 1 (conceptual):** how the established tools relate to this work — see
[`fig_fragility_space_concept.svg`](fig_fragility_space_concept.svg). Each prior tool
has a *blind spot*; the framework carries all three coordinates together.

```
   EXISTING LITERATURE (each tool, its blind spot)            THIS WORK
   ─────────────────────────────────────────────
   Random Matrix Theory (spectral) ── blind to time ─┐
   Persistent Homology (topological) ── static ──────┤        Fragility Space
   Ricci Curvature (network geometry) ── graph-dep. ──┼──►     F = (R, T, H)
   Hawkes Processes (temporal) ── blind to geometry ─┘     (+ derived R–T relation,
                                                             + honest evaluation)
```

---

## 2. Spectral lens — Random Matrix Theory in finance

**Marchenko & Pastur (1967).** The foundational result: the eigenvalue distribution of
a large random covariance matrix converges to a known law with a sharp upper edge.
Eigenvalues inside the band are consistent with noise; those above it carry signal.

**Laloux, Cizeau, Bouchaud & Potters (1999), *Noise dressing of financial correlation
matrices*.** Showed empirically that the bulk of a financial correlation matrix's
eigenvalues fall inside the Marchenko–Pastur band (i.e. are noise), while a few large
eigenvalues — led by the **"market mode"** — lie above it. Cleaning the noise improves
portfolio risk estimates.

**Plerou, Gopikrishnan, Rosenow, Amaral, Guhr & Stanley (2002).** Extended the RMT
characterization of the stock-return correlation matrix, and used the **inverse
participation ratio (IPR)** of eigenvectors to measure localization — establishing the
participation-ratio family as a standard spectral descriptor.

**Bouchaud & Potters (2009), *Financial applications of RMT*; Roy & Vetterli (2007),
*The effective rank*.** The former reviews RMT/market-mode methods; the latter defines
the **effective rank**, the eigenvalue-based effective-dimensionality measure this
project uses as its coordinate T.

*Takeaway:* the market-mode largest eigenvalue and the participation-ratio / effective
rank are **standard**. The project claims neither; it uses them as coordinates.

*Limitation motivating integration:* RMT / participation-ratio methods characterize the
**dominant (linear) correlation structure** but are **static and cross-sectional** —
they say nothing about the **temporal triggering** of extreme events, and they do not
capture the **global geometric / topological organization** of the network beyond the
eigenvalue spectrum.

---

## 3. Geometric and topological lenses

### 3a. Topological Data Analysis (persistent homology)
★ **Gidea & Katz (2018), *Topological Data Analysis of Financial Time Series:
Landscapes of Crashes*, Physica A 491:820–834.** The canonical TDA-of-crashes paper:
sliding-window point clouds → Vietoris–Rips persistence → persistence landscapes,
whose L^p-norms **grow sharply before** the 2000 and 2008 crashes (US indices S&P 500,
DJIA, NASDAQ, Russell 2000). This is the direct precedent for using persistent homology
as a crash-precursor.

*(Recent, fast-moving:* multiple 2023–2026 works extend TDA early-warning — e.g.
persistence-landscape crisis detection with ~34-day lead on US indices, and
null-validated topological signatures. Jasmeet should scan 2025–2026 q-fin preprints,
because the topological-early-warning area is active and the novelty window is
narrowing.)*

### 3b. Network / discrete-geometry (Ricci curvature)
★ **Sandhu, Georgiou & Tannenbaum (2016), *Ricci curvature: An economic indicator for
market fragility and systemic risk*, Science Advances.** Represents the market as a
weighted graph and shows **Ricci curvature is negatively correlated with fragility** —
crashes are preceded by system-level curvature/robustness changes. This is the direct
precedent for the project's Ricci-curvature analysis; the project **reproduces**, and
does not claim, this result.

*Limitation motivating integration:* persistent homology captures topological evolution
but requires **choices of filtration, distance metric, and summary** (persistence
landscape vs. persistent entropy) whose interpretation is non-trivial; discrete
Ricci curvature captures network geometry but is **sensitive to graph construction**
(correlation threshold vs. minimum spanning tree) — a sensitivity Kulkarni/Pharasi
(P2) themselves note. Crucially, **both are static and geometric — neither encodes the
temporal self-excitation / triggering of extreme events.**

---

## 4. Temporal lens — self-exciting processes

**Hawkes (1971).** Original self-exciting point process; each event raises the
intensity of future events (branching ratio n = alpha/beta as the criticality
parameter).

★ **Bacry, Mastromatteo & Muzy (2015), *Hawkes processes in finance* (arXiv:1502.04592).**
The standard survey: Hawkes models capture volatility clustering, order-book dynamics,
and — via **mutual excitation** — contagion; calibrations frequently sit **near the
critical stability threshold** (n → 1).

**Aït-Sahalia, Cacho-Diaz & Laeven (~2010), *Modeling financial contagion using
mutually exciting jump processes* (NBER w15850).** Uses mutually-exciting jumps so a
shock in one asset raises jump intensity in others — self-excitation as a systemic-risk
/ contagion mechanism.

*Takeaway:* Hawkes-as-self-excitation and branching-ratio criticality are established.
The project claims neither the model nor criticality; it **integrates** the temporal
lens with the others and reports an honest null on daily-data criticality.

*Limitation motivating integration:* Hawkes models capture the **temporal contagion /
self-excitation** of events but not the **global geometric or topological organization**
of the cross-sectional correlation structure; and on daily (non-tick) data the branching
ratio can partly reflect ordinary volatility clustering rather than genuine
microstructural self-excitation.

---

## 5. Systemic-risk / integrated frameworks — the CLOSEST precedents

This is the decisive section: the works nearest to the project's *combination*.

★★ **[P1] Chakraborti, Sharma, Pharasi et al. (2021), *Phase separation and scaling in
correlation structures of financial markets*, J. Phys: Complexity (arXiv:1910.06242).**
Constructs a **phase space from eigenvalue-derived quantities** (eigen-entropy from
eigen-centralities) in which market events (bubbles, crashes) undergo order–disorder
**phase separation**. → *Anticipates the idea of a spectral "space" for market
transitions.* The project must NOT claim to have invented a spectral state-space.

★★ **[P2] Kulkarni, Pharasi et al. (2024), *Investigation of Indian stock markets using
topological data analysis and geometry-inspired network measures*, Physica A
(arXiv:2311.17016).** Combines **discrete Ricci curvature + persistent homology on
NSE/BSE** to assess fragility/systemic risk; finds persistent entropy more robust than
L1/L2 persistence-landscape norms. → *Large overlap with the project's geometric +
topological lens: same tools, same market, same purpose.* The project must NOT claim
novelty for Ricci + PH on Indian markets.

**Note:** P1 and P2 share authors (Pharasi/Chakraborti group) — a reviewer in this
subfield will know both. Cite and discuss them prominently.

*Other systemic-risk framing neighbours:* **Billio, Getmansky, Lo & Pelizzon (2012)**
(econometric connectedness / systemic risk); **Sornette** (crashes as critical
phenomena / log-periodic precursors). Neither integrates the three specific lenses.

---

## 6. Synthesis — what is established vs. the gap

| Established in the literature | Reference(s) |
|---|---|
| Market-mode largest eigenvalue; noise vs signal | Marchenko–Pastur 1967; Laloux et al. 1999; Plerou 2002 |
| Participation ratio / effective rank as spectral descriptors | Plerou 2002; Roy–Vetterli 2007 |
| Persistent homology as crash precursor | Gidea–Katz 2018 |
| Ricci curvature as fragility indicator | Sandhu et al. 2016 |
| Hawkes self-excitation / branching-ratio criticality; contagion | Bacry et al. 2015; Aït-Sahalia et al. 2010 |
| A spectral "phase space" for market transitions | Chakraborti/Pharasi 2021 (P1) |
| Ricci + PH on Indian markets for fragility | Kulkarni/Pharasi 2024 (P2) |

**The motivation (complementary blind spots).** The limitations above are
*complementary*: the spectral lens is static and ignores temporal triggering; the
geometric/topological lenses are static and ignore self-excitation; the temporal lens
ignores global geometric organization. Each lens is blind to what the others see —
which is precisely why a framework that carries all three coordinates *together* can
say more than any one alone.

**Positioning (standard, safe phrasing).** *To the best of our knowledge, we did not
identify prior work that combines a spectral coordinate (with a derived closed-form
relationship), a topological/geometric coordinate, and a temporal (Hawkes) coordinate
in one framework and then evaluates honestly what each lens does and does not add.*
P1 has the spectral space but no temporal/topological integration; P2 has
geometry+topology but no temporal lens and no analytic spectral-coordinate derivation;
Sandhu / Gidea–Katz are single-lens. (This is a "to the best of our knowledge" claim,
pending the full-text reads in Section 9 — not an assertion of exhaustive search.)

---

## 7. Positioning — what THIS work claims (narrow and defensible)

**Do NOT claim:** RMT, participation ratio / effective rank, persistent homology, Ricci
curvature, Hawkes processes, the Cauchy–Schwarz inequality, or "a spectral state-space"
— all established (Sections 2–5).

**Claim only these three, which the closest precedents lack:**
1. **Three-lens integration adding the temporal (Hawkes) coordinate** that P1 and P2 do
   not have.
2. **An analytical, within-framework derivation** of the relationship between the
   eigenvalue-based coordinates (exact identity + Cauchy–Schwarz bounds + an error term
   characterizing when the dominant-mode approximation holds) — the precedents are
   empirical.
3. **An honest cross-lens evaluation** (independence-vs-informativeness; what each lens
   does *not* add; nulls reported), rather than proposing any single measure as the
   contribution.

**Sharpened novelty statement (use this exact scope):**
> *"We propose an operational framework that integrates complementary spectral,
> temporal, and topological descriptors of market instability. Within this framework we
> derive explicit relationships among the spectral coordinates, characterize the
> approximation error theoretically, and empirically determine when the complementary
> topological and temporal analyses provide additional information."*

### "Why this work is different" (put this in the paper)
| Existing literature | This work |
|---|---|
| Spectral phase space alone (P1) | Adds **temporal (Hawkes)** and topological coordinates to the spectral view |
| TDA + Ricci geometry alone (P2, Sandhu) | Evaluates them **alongside** a spectral coordinate with a **derived** relationship — not as the contribution itself |
| Participation ratio / entropy as descriptive metrics | **Derives** explicit spectral-coordinate relationships and validates *when* they hold |
| Reports empirical crash indicators | Combines **theoretical derivation** + **empirical regime analysis** + honest cross-lens evaluation |

This asserts *combination and emphasis*, not "nobody has done this" — a safer, more
defensible claim.

---

## 8. The one-page defensibility test (write before submission)
Answer in writing (Jasmeet + mentor):
> *"If an expert hands us the five closest papers — P1 (Chakraborti/Pharasi 2021),
> P2 (Kulkarni/Pharasi 2024), Sandhu et al. 2016, Gidea–Katz 2018, Bacry et al. 2015 —
> and asks 'why isn't your work just a combination of these?', what is our
> evidence-backed answer?"*

If you can answer clearly in one page, the positioning is strong enough. The honest
answer centers on the three claims in Section 7 (temporal-lens integration + analytic
derivation + honest evaluation), since the precedents already cover the spectral-space
and geometry/topology pieces.

---

## 9. What remains for Jasmeet + mentor (the actual research)
1. **Read these seven in full** (not just abstracts) and revise this review against
   their actual **methods and limitations**: Laloux et al. (1999), Roy & Vetterli
   (2007), Gidea & Katz (2018), Sandhu et al. (2016), Bacry et al. (2015),
   Chakraborti et al. (2021, P1), Kulkarni et al. (2024, P2). Confirm each "how we
   differ" line survives contact with the method sections — **especially P2 (biggest
   overlap)**. The limitations attributed to prior work above are drawn from abstracts;
   verify them against the full text before relying on them in the paper.
2. **Scan 2025–2026 q-fin / arXiv preprints** for any newer integrated framework; the
   topological-early-warning and RMT-fragility areas are active and the window is
   narrowing.
3. **Write the Section 8 one-pager.** If a precedent turns out closer than expected,
   narrow the claim further — honestly, and now rather than at judging.

## References (verified; complete with DOIs/arXiv IDs during write-up)
- Marchenko & Pastur (1967). *Distribution of eigenvalues for some sets of random matrices.*
- Laloux, Cizeau, Bouchaud, Potters (1999). *Noise dressing of financial correlation matrices.* PRL.
- Plerou, Gopikrishnan, Rosenow, Amaral, Guhr, Stanley (2002). *Random matrix approach to cross correlations.* Phys. Rev. E.
- Bouchaud & Potters (2009). *Financial applications of random matrix theory.*
- Roy & Vetterli (2007). *The effective rank: a measure of effective dimensionality.* EUSIPCO.
- Gidea & Katz (2018). *TDA of financial time series: landscapes of crashes.* Physica A 491:820–834. arXiv:1703.04385.
- Sandhu, Georgiou, Tannenbaum (2016). *Ricci curvature: an economic indicator for market fragility and systemic risk.* Science Advances 2(5):e1501495.
- Hawkes (1971). *Spectra of some self-exciting and mutually exciting point processes.* Biometrika.
- Bacry, Mastromatteo, Muzy (2015). *Hawkes processes in finance.* arXiv:1502.04592.
- Aït-Sahalia, Cacho-Diaz, Laeven (2010). *Modeling financial contagion using mutually exciting jump processes.* NBER w15850.
- Chakraborti, Sharma, Pharasi et al. (2021). *Phase separation and scaling in correlation structures of financial markets.* J. Phys: Complexity. arXiv:1910.06242.  ★★
- Kulkarni, Pharasi et al. (2024). *Investigation of Indian stock markets using TDA and geometry-inspired network measures.* Physica A. arXiv:2311.17016.  ★★
- Billio, Getmansky, Lo, Pelizzon (2012). *Econometric measures of connectedness and systemic risk.* J. Financial Economics.
- Sornette. *Why Stock Markets Crash* (critical phenomena / log-periodic precursors).
