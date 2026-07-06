# Literature Review — template + starting papers (the novelty gate)

> This is the **highest-priority remaining task** and the one that decides
> novelty. I can give you the *structure* and the *starting papers* — but the
> actual review (reading them, finding the gap, judging what's new) must be
> **yours**, with the professor. That IS the research, and it's what lets you
> answer the judge's question: *"why hasn't someone already done this?"*

---

## Precise novelty positioning (READ FIRST — do NOT claim the tools)

A quick literature check confirms the individual ingredients are **standard**, so we
must **not** claim any of them:
- **Effective rank / participation ratio / IPR** are well-established measures of
  spectral dimensionality (Roy & Vetterli 2007; used on financial correlation
  matrices by Plerou et al. 2002; Bouchaud & Potters).
- Using the **largest eigenvalue as the "market mode"** is standard financial RMT
  (Laloux/Bouchaud/Potters 1999; Plerou et al. 2002).
- The **inequality** (S ≥ μ²/(N−1)) is elementary Cauchy–Schwarz / power-mean.

So the wrong question is *"Did I discover a new inequality/theorem?"* (answer: no —
that won't survive expert scrutiny). The **right question** is:

> *"Is this specific combination — the Fragility-Space definitions, the
> within-framework derivation, the error characterization, and the multi-regime
> empirical validation — already present together in the literature?"*

Many strong papers invent no new mathematics; they combine known mathematics in a
novel way to answer a scientific question. That is the claim to make.

**Prior work → what THIS work adds (the table judges want):**

| Prior work | What it establishes | What this work adds |
|---|---|---|
| Effective rank / participation ratio (Roy–Vetterli 2007; Plerou 2002) | eigenvalue-based effective dimensionality | uses it as a **coordinate** in a broader fragility framework + derives closed-form relationships to the market-mode coordinate |
| Financial RMT (Laloux/Bouchaud/Potters 1999; Plerou 2002) | largest eigenvalue = market mode; noise vs signal | **connects** the market-mode coordinate to the effective-rank coordinate via explicit bounds + an error term, and compares theory to observed regimes |
| Hawkes in finance (Bacry et al. 2015) | self-exciting event dynamics | integrates Hawkes as one **coordinate** alongside spectral/topological, not in isolation |
| Persistent homology (Gidea–Katz 2018) | topological structure of markets | evaluates it as an **independent empirical lens** (corr with spectral only −0.37) — explicitly NOT implied by the spectral theory |

**The novelty statement to defend (memorize this exact scope):**
> *"We introduce the Fragility Space framework integrating spectral, temporal, and
> topological measures of market instability; derive rigorous closed-form
> relationships between the spectral coordinates **within that framework**;
> characterize when the dominant-mode approximation is accurate; and validate those
> predictions empirically across market regimes. We claim ownership of the framework,
> the integration, the within-framework derivation, and the validation — NOT of RMT,
> participation ratio, Hawkes, persistent homology, or the Cauchy–Schwarz inequality."*

**Still required before final submission:** a *thorough* search (Jasmeet + mentor) to
confirm this exact combination hasn't been published together. If a close precedent
turns up, narrow the claim accordingly — better to learn now than at judging.

---

## How to do it (the process)
1. **Read each paper's abstract + intro + conclusion** (not every proof).
2. For each, fill the matrix below: which lenses did they use, which markets,
   did they do cross-market / complementarity / lead-time / a fragility space?
3. **Find the 2–3 CLOSEST papers** to yours.
4. For each closest paper, write one sentence: *"They did X; we differ by doing Y."*
5. Your **novelty claim** is the intersection of what NONE of them did.

## The matrix (fill this in)
| Paper (author, year) | RMT | TDA | Hawkes | Multi-market | Complementarity | Lead-time | Unified "space" | What they did | **How we differ** |
|---|---|---|---|---|---|---|---|---|---|
| Marchenko & Pastur 1967 | ✓ | | | | | | | RMT noise band (pure math) | applied + integrated |
| Laloux/Bouchaud/Potters 1999 | ✓ | | | | | | | RMT cleaning of financial covariance | ... |
| Plerou et al 2002 | ✓ | | | | | | | RMT of stock correlations | ... |
| Gidea & Katz 2018 | | ✓ | | | | | | TDA landscapes of crashes | ... |
| Kulkarni et al 2023 | | ✓ | | | | | | TDA on Indian NSE/BSE | ... |
| Rai et al 2024 | | ✓ | | | | | | TDA extreme events, Indian | ... |
| Bacry/Mastromatteo/Muzy 2015 | | | ✓ | | | | | Hawkes processes in finance (survey) | ... |
| Kamps & Kleinberg 2018 | | | | | | | | crypto pump-and-dump detection | ... |
| Billio et al 2012 | | | | | | | | econometric systemic-risk / connectedness | ... |
| Sornette (crashes as critical phenomena) | | | | | | | | crashes as phase transitions | ... |
| *(add more as you find them)* | | | | | | | | | |

## Starting papers to look up (seed list — find more from their citations)
**Spectral / RMT in finance**
- Marchenko & Pastur (1967) — the noise band.
- Laloux, Cizeau, Bouchaud, Potters (1999) — *Noise dressing of financial correlation matrices.*
- Plerou et al. (2002) — RMT of the stock-return correlation matrix (uses IPR of eigenvectors).
- Ledoit & Wolf (2004) — shrinkage covariance (your RMT-vs-LW baseline).
- Bouchaud & Potters (2009) — *Financial applications of RMT* (participation ratio / market mode).
- Guhr, Müller-Groeling, Weidenmüller (1998) — RMT review (IPR / localization background).

**Effective rank / participation ratio (the concession references — cite these)**
- Roy & Vetterli (2007) — *The effective rank: a measure of effective dimensionality* (defines the concept you use as coordinate T).
- (Participation ratio / IPR appear throughout the RMT-finance papers above — these
  establish that the *measure* is standard, so your novelty is its *use in the
  framework*, not the measure itself.)

**Geometric / TDA in finance**
- Gidea & Katz (2018) — *TDA of financial time series: landscapes of crashes.*
- Kulkarni et al. (2023), Rai et al. (2024) — TDA on Indian markets (closest to your TDA).

**Temporal / Hawkes + manipulation**
- Hawkes (1971) — original self-exciting processes.
- Bacry, Mastromatteo, Muzy (2015) — Hawkes in finance (survey).
- Kamps & Kleinberg (2018); Xu & Livshits (2019) — crypto pump-and-dump detection.

**Systemic risk / fragility / connectedness (your framing's neighbours)**
- Billio, Getmansky, Lo, Pelizzon (2012) — connectedness & systemic risk.
- Diebold & Yilmaz — connectedness measures.
- Sornette — crashes as critical phenomena / phase transitions.

## Where to search
- **Google Scholar** (search: "topological data analysis financial crash", "random
  matrix theory portfolio", "Hawkes market manipulation", "systemic fragility").
- **arXiv q-fin** (quantitative finance preprints).
- **SSRN** (finance working papers).
- Follow the **citation trails** of the closest papers (both directions).

## The output you need
Two things, in your own words:
1. **A filled matrix** (above).
2. **A novelty paragraph:** *"The closest prior work is [X, Y]. They studied [...].
   To our knowledge, no prior work [combines all three lenses across multiple
   markets / tests their complementarity / establishes the staged lead-time /
   derives the spectral-geometric redundancy]. That is our contribution."*

**Do this honestly.** If you find someone already did most of it, that's crucial to
know *now* — and you narrow your claim to what's genuinely left. That honesty is
exactly what a strong researcher (and a judge) respects.
