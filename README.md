# A Unified Mathematical Framework for Characterizing Systemic Market Fragility
### Spectral, Geometric, and Temporal Analysis

*When does a market stop behaving as many independent assets and become one
synchronized, fragile system?*

---

## Contribution
> **We propose an operational framework for characterizing systemic market fragility
> through complementary spectral, geometric, and temporal coordinates. Within this
> framework we derive explicit relationships between the eigenvalue-based coordinates,
> characterize the approximation error, and evaluate the framework empirically across
> multiple market regimes.** We claim the *framework, the integration, the
> within-framework derivation, and the empirical evaluation* — not the underlying tools
> (RMT, participation ratio, persistent homology, Ricci curvature, Hawkes), which are
> established. See [`CONTRIBUTION.md`](CONTRIBUTION.md) and, for the closest prior work,
> [`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md).

---

## Definition (the heart of the thesis)
> **In this work, we operationalize systemic fragility as the progressive loss of
> statistical independence among market participants — manifested as (i) rising correlation
> and market-mode dominance, (ii) collapse of the geometric diversity of the
> return structure, and (iii) self-exciting cascades of extreme events.**

We investigate each manifestation using a complementary mathematical framework,
giving three "lenses" on the *same* phenomenon. (These are useful complementary
descriptions, not the only possible mathematical ones.)

## The unifying question
A **healthy** market is *diverse*: assets move somewhat independently, so risk
diversifies and structure is rich. A **fragile** market **synchronizes**. This
loss of independence is measured through **three branches of mathematics**, each
a distinct "microscope":

| Lens | Branch of math | The object studied | The instability signature |
|---|---|---|---|
| **1. Spectral** (RMT) | Linear algebra / RMT | eigenvalues of the covariance matrix | noise eigenvalues swamp the signal |
| **2. Geometric** (TDA) | Algebraic topology | shape of the correlation point cloud | topological loops collapse |
| **3. Temporal** (Hawkes) | Stochastic point processes | timing of extreme events | events become self-exciting (n → 1) |

Together they give a **spectral + geometric + temporal** characterization of the
same underlying fragility.

## The three components (each independently built & tested)

### 1. Spectral — Random Matrix Theory  (`../rmt_portfolio/`)
Marchenko–Pastur tells us which covariance eigenvalues are noise. Cleaning them
builds portfolios with **lower, more honest risk** than the raw sample
covariance, and the benefit **grows exactly as the noise ratio q = N/T grows**.
→ *Positive result; confirms theory.*

### 2. Geometric — Topological Data Analysis  (`../tda_crash_detection/`)
Persistent homology of the rolling correlation structure. As a crash nears,
correlations rise and topological loops vanish. **Rigorous finding:** once you
control for the volatility confound and include 2008, TDA does **not** add
statistically significant early-warning power over plain volatility.
→ *Honest negative result; a critical audit.*

### 3. Temporal — Hawkes Processes  (`../hawkes_pump_detection/`)
Extreme events modelled as a self-exciting point process. Real markets self-excite
(BTC branching ratio **n ≈ 0.77**), and the branching ratio detects **volume-matched
stealth pump-and-dumps** (AUC 1.0 on simulations) that volume-based surveillance
is blind to (AUC ≈ 0.4).
→ *Purposeful positive result; protects retail investors.*

## Why integrate them
- **One coherent thesis** beats three disconnected demos: every method measures
  *loss of independence / onset of synchronization* from a different angle.
- **Intellectual range:** algebra, topology, and stochastic processes in one
  framework — and the honesty to report a *positive*, a *negative*, and an
  *applied* result side by side.
- **Complementarity is the finding:** spectral noise (RMT) and temporal
  self-excitation (Hawkes) carry real signal; geometric topology (TDA), once
  controlled, does not — a nuanced, mature conclusion no single method gives.

## Reproduce every result (benchmark package)
```
python reproduce.py           # regenerate every headline table & finding
python reproduce.py --quick   # skip the slow ripser / long-history experiments
```
One command regenerates the Proposition validation, the geometric independence/role/
curvature results, the RQ-A regime discovery, the 9-market baseline comparison with
bootstrap CIs, the crisis-trajectory heterogeneity finding, and the branching-
criticality null. (Legacy `python run_all.py` still runs the original three lenses.)

## Folder map
```
code/
├── market_instability/      ← this integrated framework (thesis + runner)
├── rmt_portfolio/           ← 1. spectral  (RMT)
├── tda_crash_detection/     ← 2. geometric (TDA)
└── hawkes_pump_detection/   ← 3. temporal  (Hawkes)
```

## Honest framing
These are **research prototypes** that establish the direction and the core
results. The full ISEF paper (developed with the mentor/professor) would unify
the formal write-up, add labelled data where needed (esp. real pump events for
Hawkes), and extend each method (RIE estimators, multivariate Hawkes, etc.).

---

## Extensions toward research novelty

### Multi-market generalisation (`multimarket.py`)
Ran the lenses across **India equities, US equities, and crypto** to separate
universal from market-specific behaviour:

| Market | Hawkes branching ratio n (extreme moves) | GMV vol: sample → Ledoit-Wolf |
|---|---|---|
| India equities | 0.57 [0.44, 0.75] | 16.3% → 15.9% |
| US equities | 0.60 [0.45, 0.75] | 15.4% → 15.1% |
| Crypto | 0.59 [0.51, 0.71] | 58.7% → 55.4% |

**Findings.** *Universal:* extreme-move self-excitation is remarkably consistent
(n ≈ 0.57–0.60) across all three markets, and covariance cleaning lowers GMV
volatility everywhere. *Market-specific:* crypto is ~3–4× more volatile and
benefits **more** from cleaning (bigger vol reduction) — consistent with a noisier
covariance matrix.

### Integrated fragility framework (`fragility_index.py`, `fragility_space.py`)
We do NOT claim a novel "index" (combining indicators is common). The more
defensible framing: an **integrated framework that jointly analyzes the spectral,
geometric, and temporal signatures of fragility**, representing each market state
as a point in a 3-D **fragility space** F = (R, T, H). That space — not a
hand-weighted score — is the cleaner contribution: it enables clustering,
trajectories, regime changes, and cross-market comparison. The weighted index
SFI = z(R)+z(T)+z(H) is reported only as one summary of that space.

Crash-warning AUC (2010–2024): SFI 0.69, spectral 0.65, geometric 0.63,
temporal 0.58, **volatility 0.53**.

**Honest verdict (do NOT overclaim this):** the SFI's apparent edge over
volatility is **not statistically significant** (bootstrap 95% CI of the lift
includes 0), AND the volatility baseline is anomalously weak here **only because
2010–2024 excludes the 2008 crash** where volatility dominates — the same
period-artifact flagged for TDA. On a fair, 2008-inclusive test the edge would
very likely vanish. **Conclusion: the SFI is a concrete new metric, rigorously
tested, that does not reliably beat volatility for crash prediction** — the
honest, expected result given that crashes largely resist prediction.

### Ablation, fragility-space geometry & benchmark battery (`fragility_space.py`)
Treating the lenses as orthogonal dimensions F = (R, T, H) and testing rigorously:

| Model | AUC | 95% CI |
|---|---|---|
| R+T+H (in-sample) | 0.693 | [0.52, 0.82] |
| Fragility logistic (time-series CV, out-of-sample) | **0.589** | — |
| avg correlation (benchmark) | 0.630 | [0.51, 0.80] |
| volatility (benchmark) | 0.531 | [0.50, 0.71] |
| drawdown (benchmark) | 0.550 | [0.50, 0.71] |

**Findings (honest):** (1) all CIs overlap — no signature is statistically
distinguishable from another or from the benchmarks; (2) the cross-validated
out-of-sample AUC (0.589) is well below the in-sample figure (0.693), the usual
overfitting gap; (3) a trivial average-correlation benchmark (0.630) matches the
full three-lens composite. **Conclusion:** the composite carries only modest
crash-precursor information and does not reliably beat simple risk measures — so
the defensible contribution is *characterising* fragility across markets, not
predicting crashes. (Caveat: 2010–2024 excludes 2008, weakening the volatility
benchmark; conclusions should lean on the cross-market picture.)

---

## Are the three lenses actually complementary? (`complementarity.py`)
We test the thesis's core claim empirically rather than assert it.

**1. Redundancy (pairwise correlation).** Spectral & Geometric are **0.97
correlated — nearly redundant**; Temporal is weakly correlated with both
(~0.22). **2. Unique value (leave-one-out AUC).** Removing Temporal costs the
most (−0.052); removing Spectral or Geometric barely hurts (−0.014 each, since
they cover each other). **3. Timing (lead before crashes).** Geometric peaks ~24
trading days before onset [CI 17,31], Spectral ~22 [16,29], **Temporal ~11**
[5,19]. The structure-minus-temporal lead is **+12 days, 95% CI [+3,+20],
permutation p = 0.026 — statistically significant**: structural degradation
*precedes* temporal self-excitation (caveat: n=13 crashes, small sample; should
be re-checked across more markets).

**Honest conclusion:** the lenses are only *partially* complementary. **Temporal
(Hawkes) is genuinely distinct**; **Spectral and Geometric are largely redundant**
(≈2 effective dimensions, not 3, with these eigenvalue-based proxies — the true
TDA persistence signal may be more distinct, a limitation to check). The
**staged timing** (structural collapse ~22–24 days out, temporal self-excitation
~11 days out) is a genuine, interpretable finding about *how* fragility unfolds.

---

## Why are the spectral and geometric lenses redundant? (`redundancy_analysis.py`)
We move from *observing* the 0.97 R–T correlation to *explaining* it — stated
honestly as a proposition under an explicit assumption, then validated.

**Proposition (Dominant Market-Mode Approximation).** With R = λ_max/N and
T = 1 − PR/N (participation ratio PR = N²/Σλ²): IF one eigenvalue dominates
(Σλ² ≈ λ_max²), THEN PR ≈ 1/R² and **T ≈ 1 − 1/(N R²)** — so T becomes an explicit
increasing function of R, forcing the two measures to co-move.

**Validation.** corr(T, predicted-T) = **0.94**, which explains the empirical
corr(R, T) = 0.974. The absolute error is not small (~0.32 overall) — the
approximation captures the *direction*, not exact values.

**Breakdown conditions (a second contribution).** The error falls monotonically
as the market mode dominates: mean |error| = 0.72 (low dominance) → **0.06 (high
dominance)**; 0.48 in calm markets vs 0.16 in turbulent ones. So the relationship
**holds when the market mode dominates (crisis/turbulent regimes) and breaks down
in calm markets** with a spread-out spectrum.

This is an *analytical approximation + empirical validation + characterised
limits* — a defensible applied-mathematics result (a Proposition, not a theorem),
and a stronger contribution than reporting the correlation alone.

---

## Is the geometric lens a genuinely distinct measurement? (`geometric_independence.py`)
The earlier 0.97 spectral–geometric redundancy was an **artifact of the geometric
coordinate's definition**: the participation ratio PR = N^2/sum(lambda^2) is a
function of the eigenvalues, so it was really a *second spectral measure*. We test
a coordinate that is NOT eigenvalue-based — the persistent-homology (H1) signal of
the correlation-distance point cloud (topology / connectivity, not variance).

**(A) Correlation with the spectral coordinate R.**

| Geometric coordinate | corr with spectral R |
|---|---|
| Participation-ratio proxy (eigenvalue-based) | **+0.97** (near-redundant) |
| **Persistent homology H1 norm (true topology)** | **−0.37** (complementary) |
| Persistent entropy (true topology) | −0.38 (complementary) |

**(B) Ablation — does the true topological lens add *unique* crash-warning info?**
Correlation alone is weak evidence; the stronger test is whether the topological
feature improves a model *over the spectral lens alone*. We z-score and combine
{spectral R, true-topology T_tda, temporal H} and compare crash-warning AUC:

| Model | AUC |
|---|---|
| spectral only | 0.649 |
| geometric only (true topology) | 0.529 |
| temporal only | 0.582 |
| spectral + geometric | 0.641 |
| spectral + temporal | **0.679** |
| spectral + geometric + temporal | 0.669 |

**Honest reading (do NOT overclaim):** the true topological coordinate is
*informationally* complementary (corr −0.37, not redundant), **but it does not add
predictive lift** — spectral+geometric (0.641) is no better than spectral alone
(0.649), whereas the *temporal* lens does add lift (spectral+temporal 0.679). So
the correct claim is nuanced: replacing the proxy with real persistent homology
makes the geometric lens a **genuinely distinct measurement** (fixes the "two
spectral measures" problem), yet on *this* crash-prediction task it carries little
*unique predictive* value — consistent with the project's overall finding that
fragility can be characterized more reliably than crashes can be predicted.

**(C) Does topology have a role beyond prediction? (`geometric_role.py`)**
A fair follow-up: if it doesn't improve crash prediction, does topology at least
distinguish market states that *evolve* differently? We test whether, **conditional
on the same spectral signature R**, topology separates forward behaviour (forward
20-day vol and drawdown). Result — **also largely negative, reported honestly:**
partial corr(T_tda, forward vol | R) = −0.07 and (forward drawdown | R) = −0.04,
i.e. near zero. Within matched-R quintiles the forward outcomes of high- vs
low-topology states are nearly identical; the only flicker is the most-synchronized
quintile (forward vol 0.205 vs 0.165), a single bin that does not survive the
partial-correlation test. **Conclusion:** on daily Indian-equity data the
topological lens is a *mathematically distinct* measurement but does **not** carry
meaningful unique information about either crash timing or regime character. Its
value is conceptual/structural, not predictive; a genuine predictive role, if one
exists, would more likely appear on intraday data or in distinguishing specific
crisis morphologies — an honest limitation and future direction, not a claim.

**Careful wording (this matters):** a correlation of −0.37 is **NOT statistical
independence** — it means the topological summary is only **weakly-to-moderately
correlated** with the spectrum, i.e. it carries information that is **not merely a
restatement of the eigenvalues**. The defensible claim is that the three
coordinates are **complementary and capture distinct information**, *not* that they
are "independent." With this change the geometric lens is a genuinely different
mathematical object (topology/connectivity), so the framework can honestly present
**three mathematically distinct representations** — spectral, topological, temporal
— rather than two spectral measures plus one temporal. (The negative sign is
interpretable: as the market mode grows, correlations rise, the point cloud
collapses, and topological loops shrink.)
