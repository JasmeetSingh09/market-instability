# Literature Review — template + starting papers (the novelty gate)

> This is the **highest-priority remaining task** and the one that decides
> novelty. I can give you the *structure* and the *starting papers* — but the
> actual review (reading them, finding the gap, judging what's new) must be
> **yours**, with the professor. That IS the research, and it's what lets you
> answer the judge's question: *"why hasn't someone already done this?"*

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
- Plerou et al. (2002) — RMT of the stock-return correlation matrix.
- Ledoit & Wolf (2004) — shrinkage covariance (your RMT-vs-LW baseline).

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
