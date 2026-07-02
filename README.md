# Three Mathematical Lenses on Market Instability

*An integrated framework: when does a market stop being a collection of
independent parts and become one fragile, synchronized system?*

**ISEF category:** Mathematics (spans Algebra, Geometry & Topology, and
Probability & Statistics — a deliberately multi-disciplinary framework).

---

## The unifying question
A **healthy** market is *diverse*: assets move somewhat independently, so risk
diversifies and structure is rich. A **fragile** market **synchronizes** —
correlations spike, structure collapses, and behaviour becomes self-exciting.
This single phenomenon — the loss of independence — can be measured through
**three different branches of mathematics**, each a distinct "microscope":

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

## Run the whole framework
```
python run_all.py
```
Runs all three analyses in sequence and prints a combined report. (Each can also
be run on its own inside its folder.)

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

### Systemic Fragility Index (`fragility_index.py`) — a new composite metric
Fused the three lenses into one index: SFI = z(spectral market-mode share) +
z(geometric dimensional collapse) + z(temporal volatility-clustering).

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
