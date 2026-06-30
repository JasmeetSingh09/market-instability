# Topological Early-Warning Signals for Indian Stock-Market Crashes

**ISEF category:** Mathematics → *Geometry & Topology* (with Probability & Statistics)
**Status:** working prototype / proof-of-concept

---

## The research question
Standard crash warnings rely on **volatility**. This project asks a *mathematical*
question instead:

> Does the **shape** (topology) of the market — the geometric structure of how
> stocks move together — change *before* a crash, in a way that volatility does
> **not** already capture?

The object of study is the **persistent homology** of a financial point cloud.
The market data is just the experimental vehicle; the contribution is mathematical.

## Method
1. Take 10 large, liquid NSE stocks across sectors. Each trading day is a point
   `(r₁,…,r₁₀)` of that day's log-returns, so a sliding 50-day window is a
   **point cloud of 50 points in ℝ¹⁰**.
2. For each window compute the **H₁ persistence diagram** (topological "loops")
   via the Vietoris–Rips filtration (`ripser`).
3. Summarise each diagram by the **L¹/L² norms of its loop lifespans**.
4. Crucially, compute the signal **two ways**:
   - *raw* returns, and
   - *window-standardized* returns (scale removed) → **pure geometric structure**.
5. Label a day "pre-crash" if the Nifty 50 falls > 10% over the next 20 days, and
   measure each signal's early-warning power by **AUC**, benchmarked against
   rolling volatility.

## Key findings (honest — this is a CRITICAL AUDIT)
We tested the popular claim *"TDA predicts market crashes"* as rigorously as we
could, across multiple constructions, and the claim **does not survive** on
Indian markets once confounds and period are controlled.

| Test (fair, full period incl. 2008) | AUC | Verdict |
|---|---|---|
| Rolling volatility (baseline) | **0.780** | — |
| Best topological signal (persistent entropy) | 0.743 | below baseline |
| Volatility + best topology | 0.795 | lift **+0.015** |
| 95% bootstrap CI of the lift | **[−0.008, +0.040]** | **not significant** |

**What we found — and how rigor mattered at each step:**
1. **Naive TDA norms are volatility in disguise** (0.5–0.6 correlated with it).
   Most applications skip this control; we didn't.
2. **A principled construction (persistent homology of the correlation-distance
   matrix of ~24–38 stocks) looked promising** — topology AUC 0.73 vs volatility
   0.61, *significant* — **but that was a period artifact.** That stock set
   silently started in late-2008, excluding the Lehman crash where volatility is
   strongest.
3. **On the fair, full period (2007–2024, incl. 2008), the edge disappears:**
   the topological lift over volatility is **+0.015 and statistically
   insignificant** (bootstrap CI includes 0).
4. **As an actionable strategy it does not help:** a cost-aware de-risking rule on
   the topological signal *underperforms* buy-and-hold and does not reduce drawdown.

## Conclusion
On Indian markets, **topological early-warning signals do not add statistically
significant value beyond volatility** for crash prediction, once you control for
(a) the volatility confound and (b) the evaluation period. The apparent successes
reported informally are explained by these two effects. This is a negative result —
but a **rigorously established** one, and correcting an over-claimed technique is
legitimate science.

**Methodological contribution (the real takeaway):** the *protocol* — isolating the
scale-free signal, benchmarking against volatility out-of-sample, catching the
period artifact, and bootstrap-testing the lift — is exactly the rigor missing from
descriptive TDA-finance papers.

## Why this is a strong *Mathematics* project
- The core object is **persistent homology** (real algebraic topology), not "an app."
- It demonstrates **methodological rigor**: controlling for a confound (volatility),
  deriving the correct sign from a mechanism, and reporting an honest, modest effect.
- It includes an honest **critical finding** (debunking the naive claim) *and* a
  genuine positive one — exactly the scientific maturity judges reward.

## Files
- `tda_crash.py` — full pipeline (data → persistent homology → evaluation → figure)
- `tda_results.csv` — per-day signals
- `tda_figure.png` — Nifty 50 with crash periods + the two warning signals

## Open directions (for the full research, with the professor)
- **Persistence landscapes / images** instead of lifespan norms (richer summaries).
- **Time-delay embedding** of a single index (the other Gidea–Katz construction).
- **Wasserstein distance** between consecutive diagrams as a "topological change rate."
- More assets / sectors; out-of-sample and cross-market (US, HK) validation.
- Formal statistical test of the +0.015 lift (bootstrap CI / DeLong test on AUCs).

## Reference
Gidea & Katz (2018), *Topological Data Analysis of Financial Time Series:
Landscapes of Crashes*, Physica A — the foundational paper this extends to Indian markets.
