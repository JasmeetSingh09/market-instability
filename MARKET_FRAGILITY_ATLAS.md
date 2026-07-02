# The Market Fragility Atlas — Research Plan

*Do different financial markets become fragile in the same way? A cross-market
study of the spectral, geometric, and temporal signatures of instability.*

> This is the RESEARCH PLAN (the roadmap), not the paper. It combines the
> integrated three-lens framework (the method) with a cross-market "atlas" (the
> question). It is the document to bring to the mentoring professor. Everything
> marked **[TO DO]** is genuine research still to be done — much of it by the
> student, so he can defend every choice.

---

## 1. Thesis
Markets are studied endlessly for *prediction*; far less for *how they fail*. We
do not attempt to predict crashes (we show, honestly, that they resist
prediction). Instead we **map the mathematical signatures of fragility and ask
which are universal across markets and which are market-specific** — building a
"Market Fragility Atlas."

## 2. Research questions
1. Which fragility signatures are **universal** across markets?
2. Which are **market-specific**?
3. Which signature **moves first** as instability builds?
4. Do the tools add information **beyond simple risk measures** (out-of-sample)?

## 3. Markets (the atlas)
| Market | Proxy universe |
|---|---|
| India | NIFTY large caps |
| US | S&P 500 large caps |
| Europe | STOXX / DAX + CAC constituents |
| Japan | Nikkei 225 constituents |
| Crypto | BTC, ETH + top assets |

Same rolling windows, same crash definitions, same estimation everywhere — so
cross-market differences reflect the *markets*, not the *pipeline*.

## 4. Method — three lenses = four signatures
Each market state becomes a point in a 3-D **fragility space** F = (R, T, H).
| Signature | Lens | What it captures |
|---|---|---|
| Eigenvalue spectrum + correlation collapse | **Spectral (RMT)** | market-mode dominance; Marchenko–Pastur noise vs signal |
| Network topology | **Geometric (TDA)** | collapse of correlation-structure geometry (persistent homology) |
| Self-excitation | **Temporal (Hawkes)** | do shocks trigger more shocks? (branching ratio) |

## 5. Evaluation (rigor — already the project's strength)
- Out-of-sample, walk-forward; the honest metric (realised risk, not Sharpe).
- **Bootstrap 95% confidence intervals** on every difference.
- **Time-series cross-validation** (report separately from in-sample).
- **Ablation** (each lens, each pair, all three).
- **Benchmark battery**: volatility, average correlation, drawdown (+ VIX for US).
- Permutation tests **[TO DO]**.

## 6. Status — done vs to-do (honest)
**Done (research-grade, with CIs):**
- RMT crossover study (RMT vs Ledoit-Wolf vs sample) — India.
- TDA robustness across 9 crash definitions — India (robust null).
- Hawkes intensity sweep with CIs.
- Multi-market (India/US/crypto): self-excitation ~0.6 everywhere; cleaning helps
  everywhere; crypto ~3–4x more volatile.
- Fragility space + ablation + benchmarks — India.

**To do (the atlas + the science):**
- **[TO DO]** Extend the full pipeline to **Europe and Japan** (complete the atlas).
- **[TO DO]** Run TDA/network topology per market (not just India).
- **[TO DO]** "Which moves first?" — lead-time comparison of the signatures.
- **[TO DO]** Permutation tests; VIX benchmark for the US.
- **[TO DO]** **Literature review** — verify novelty of the integration + the
  cross-market findings (with the professor).
- **[TO DO]** Write the paper (Introduction, Discussion, Limitations).

## 7. Honest positioning (the defensible contribution)
NOT "we invented RMT / we built a crash predictor." Instead:
> *"We present an integrated spectral/geometric/temporal framework and use it to
> map fragility across five markets, showing which signatures are universal and
> which are market-specific — and, honestly, that the framework characterises
> fragility without reliably predicting crashes out-of-sample."*

A characterisation contribution + a cross-market empirical finding. Whether it is
*novel* depends on the literature review.

## 8. Limitations (state them; judges reward it)
Survivorship bias (current constituents); daily data (no microstructure); Hawkes
validated on simulation, not labelled real pumps; crashes are rare (wide CIs);
"network topology" must be precisely defined and justified.

## 9. The five questions the student must answer (defense readiness)
1. What question were you trying to answer?
2. Why did you choose these methods (RMT, TDA, Hawkes, bootstrap, CV, ablation)?
3. What did you discover?
4. Why does that discovery matter?
5. How is it different from what was already known?

**Q2 requires understanding the mathematics. Q5 requires the literature review.
These — not more code — are the remaining work, and they must be the student's.**
