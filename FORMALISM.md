# Formalism & Contribution

Two "best-version" upgrades: (1) a rigorous definition of the fragility space as
a mathematical object, and (2) the sharpened scientific contribution.

---

## 1. The Fragility Space — formal definition

### Setup
Fix a rolling window of length W. Let X_t be the W x N matrix of asset returns
over the window ending at time t, and let C_t be its N x N sample correlation
matrix, with eigenvalues

    0 <= lambda_1 <= lambda_2 <= ... <= lambda_N ,      sum_i lambda_i = N

(the trace of a correlation matrix equals N). Write lambda_max = lambda_N.

### The three coordinates
We define three real-valued functions of the window, each a distinct
mathematical "signature" of the loss of statistical independence.

**Spectral coordinate (RMT).** Market-mode share:

    R(t) = lambda_max / N ,        R(t) in [1/N, 1].

R measures how much of the total variance is concentrated in the single leading
("market") eigenvalue. R -> 1 means one factor moves everything.

**Geometric coordinate (TDA-flavoured).** Dimensional collapse via the
participation ratio PR = (sum lambda_i)^2 / (sum lambda_i^2) = N^2 / (sum lambda_i^2):

    T(t) = 1 - PR(t)/N = 1 - N / (sum_i lambda_i^2) ,     T(t) in [0, 1 - 1/N].

T = 0 when all eigenvalues are equal (maximal effective dimension / diversity);
T -> 1 - 1/N when one eigenvalue carries everything (structure collapses to a
line). T measures how far the return geometry has collapsed toward low dimension.

**Temporal coordinate (Hawkes-flavoured).** Self-excitation via lag-1
autocorrelation of the squared window index-returns r_s = (1/N) sum_j X_{s,j}:

    H(t) = Corr( r_s^2 , r_{s+1}^2 ) over the window,     H(t) in [-1, 1].

H measures volatility clustering — the degree to which large moves trigger
further large moves (a proxy for the Hawkes branching ratio).

### The space
The **fragility space** is the image of the market-state map

    F : t  |-->  ( R(t), T(t), H(t) )  in  [1/N,1] x [0,1-1/N] x [-1,1]  subset R^3.

Each trading day is a point in R^3. Because the coordinates have different
natural scales, distances between states are measured with the **standardized
(z-scored) Euclidean metric** d(u,v) = || z(u) - z(v) ||_2, where z standardizes
each coordinate over the sample. This makes F a metric space in which one can
study:
- **regions:** a *healthy* region (low R, T, H — diverse, uncorrelated, no
  clustering) vs a *fragile* region (high R, T, H — synchronized, collapsed,
  self-exciting);
- **trajectories:** the path t |-> F(t) through the space over time;
- **cross-market comparison:** whether the fragile region sits in the same place
  for India, US, and crypto.

### A structural relation among the coordinates
R and T are not independent. Under a dominant-market-mode assumption
(sum lambda_i^2 ~ lambda_max^2) one has PR ~ 1/R^2 and hence

    T ~ 1 - 1 / (N R^2)          (Proposition; see redundancy_analysis.py)

so the (R, T) face of the space collapses toward a one-parameter curve exactly
when the market mode dominates — validated empirically (corr 0.94), and shown to
break down in calm markets. Thus F is effectively ~2-dimensional under stress
(a structural axis R~T, plus the temporal axis H) and more genuinely
3-dimensional in calm regimes.

---

## 2. The contribution (sharpened)

### One-sentence contribution (the spine of the paper)
> **We introduce a fragility space that represents each market state by three
> mathematical signatures — spectral market-mode dominance, geometric dimensional
> collapse, and temporal self-excitation — and show that structural fragility
> measurably and significantly *precedes* temporal self-exciting cascades before
> market stress, a staged signature of how markets lose statistical independence
> that we find consistent across equity and crypto markets.**

### Tightened abstract (~150 words)
Financial markets are most dangerous when they cease to behave as many
independent assets and act as one synchronized system. We formalize this "loss of
statistical independence" as a point in a three-dimensional *fragility space*
whose axes are spectral market-mode dominance (random matrix theory), geometric
dimensional collapse (participation ratio), and temporal self-excitation (Hawkes
clustering). Analyzing Indian, US, and cryptocurrency markets with walk-forward
evaluation and bootstrap confidence intervals, we report three findings: (i) the
spectral and geometric axes are redundant, which we explain by an analytical
proposition valid under a dominant market mode; (ii) structural fragility
statistically *precedes* temporal cascades by roughly two trading weeks before
market stress; and (iii) the combined signal characterizes fragility but does not
reliably *predict* crashes, matching the view that crises resist prediction.
Fragility is thus characterizable, cross-market, and staged — even where it is
not predictable.

### Why this framing is defensible
- It claims a **characterization**, not a crash predictor (honest; supported).
- Its headline is a **positive, significant, interpretable** result (the staged
  timing), not a null.
- It contains an **analytical proposition + validation + limits** (real applied
  math), not just experiments.
- It is **cross-market**, addressing generalization.
