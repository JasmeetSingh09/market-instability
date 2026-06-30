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
