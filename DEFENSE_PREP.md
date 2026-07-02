# Defense Preparation — Can you prove this is genuinely yours?

> This is a STUDY GUIDE, not a script. For each item: understand the concept,
> then explain it **in your own words, at a whiteboard, without notes.** If you
> can't, that's your study list — not something to memorize. Judges (and the
> professor) will probe until they find what you don't understand. The goal is
> that there's nothing to find.

---

## The five questions you must answer cold

### Q1 — What question were you trying to answer?
> *"When does a market stop behaving as many independent assets and become one
> synchronized, fragile system — and which mathematical signatures of that
> fragility are universal across markets?"*
- Be able to say **why this is a better question than "can I predict crashes?"**
  (Answer: crashes largely resist prediction; characterizing fragility is
  honest and answerable.)

### Q2 — Why did you choose these methods? (**requires the math**)
For EACH, you must explain what it measures and *why it fits*:
- **RMT / Marchenko–Pastur:** which covariance eigenvalues are real signal vs
  noise. *Whiteboard test: what is an eigenvalue of a correlation matrix? What
  does λ₊ = σ²(1+√q)² mean, and why does a big q make the matrix noisier?*
- **TDA / persistent homology:** the shape/topology of the correlation structure.
  *Whiteboard test: what is a persistence diagram? what does a "loop" mean here?*
- **Hawkes process:** self-excitation — do shocks trigger shocks. *Whiteboard
  test: write λ(t) = μ + Σ α e^(−β(t−tᵢ)); what is the branching ratio n = α/β,
  and why does n→1 mean instability?*
- **Bootstrap CI:** why report a confidence interval instead of one number?
- **Cross-validation vs in-sample:** why is the 0.589 CV AUC more honest than the
  0.693 in-sample AUC? (Overfitting — in-sample sees the answer.)
- **Ablation:** why test each lens alone and in combinations?

### Q3 — What did you discover?
State the honest findings and where each is shown:
- RMT: cleaning is essential; RMT ≈ Ledoit-Wolf (LW slightly better with data). `rmt_research.py`
- TDA: does **not** significantly beat volatility — robust across 9 crash defs. `tda_research.py`
- Hawkes: detects volume-matched pumps (AUC>0.9 for n≥0.3); volume is blind. `hawkes_research.py`
- Multi-market: self-excitation ~0.6 everywhere; cleaning helps everywhere. `multimarket.py`
- Composite: does **not** reliably beat simple risk measures out-of-sample. `fragility_space.py`
- Complementarity: Temporal is distinct; Spectral ≈ Geometric (0.97); staged timing. `complementarity.py`

### Q4 — Why does that discovery matter?
- Honest characterization of fragility > overclaimed prediction.
- Practically: cleaning covariance genuinely lowers risk; self-excitation is a
  real, universal manipulation signal.
- Scientifically: a rigorous demonstration of what does and doesn't work — and
  the honesty (reporting nulls) is itself the contribution.

### Q5 — How is it different from what was already known? (**requires the lit review**)
- You did **not** invent RMT/TDA/Hawkes. The claimed contribution is the
  *integrated cross-market characterization* and the *complementarity/timing*
  findings. Whether that is novel depends on the literature review — **do it with
  the professor and be ready to name the closest prior work and how you differ.**

---

## Concepts you MUST be able to explain at a whiteboard
- [ ] What an eigenvalue/eigenvector is (start with 3Blue1Brown "Essence of LA")
- [ ] Why a covariance matrix has eigenvalues and what the big one means (market mode)
- [ ] Marchenko–Pastur: the noise band, and why cleaning helps
- [ ] Ledoit–Wolf shrinkage (in one sentence) and why it beats raw sample covariance
- [ ] A persistence diagram / what persistent homology measures
- [ ] The Hawkes intensity equation and the branching ratio
- [ ] Bootstrap confidence intervals (resampling → distribution → CI)
- [ ] In-sample vs cross-validated AUC (and why the gap = overfitting)
- [ ] Why your composite does NOT beat volatility (and the 2008 period artifact)
- [ ] The complementarity result (2 effective dimensions, staged timing)

## The honesty test
If an expert asks *"did you understand this, or did a tool produce it?"* — the
answer is decided by whether you can explain the checklist above **unaided.**
That, not the code, is what makes the work genuinely yours. Start with the math.
