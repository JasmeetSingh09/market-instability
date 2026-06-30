"""
Validate the Hawkes manipulation detector:

  PART A — REAL DATA: fit a Hawkes process to extreme price-move times of a real
           crypto asset and show markets genuinely self-excite (branching ratio > 0).

  PART B — DETECTION POWER: the key experiment. Generate "normal" episodes
           (Poisson) and "pump" episodes (Hawkes) that are VOLUME-MATCHED — same
           expected number of events, only difference is the pump is CLUSTERED.
           Show that a volume detector is blind (AUC ~ 0.5) while the Hawkes
           branching ratio detects the manipulation (AUC >> 0.5).
"""

import numpy as np
import yfinance as yf
from hawkes import fit_hawkes, simulate_hawkes, simulate_poisson, rng


def auc(score, label):
    score, label = np.asarray(score, float), np.asarray(label, int)
    m = np.isfinite(score)
    score, label = score[m], label[m]
    pos, neg = score[label == 1], score[label == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    return (ranks[label == 1].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


# ---------------------------------------------------------------------------
# PART A — real crypto: do extreme price moves self-excite?
# ---------------------------------------------------------------------------
def real_data_check(ticker="BTC-USD"):
    print(f"\n=== PART A: REAL DATA — {ticker} (5-min bars, ~60 days) ===")
    px = yf.download(ticker, interval="5m", period="60d",
                     auto_adjust=True, progress=False)["Close"].squeeze().dropna()
    ret = np.log(px / px.shift(1)).dropna()
    thr = ret.abs().quantile(0.95)                  # "events" = extreme moves
    minutes = (px.index - px.index[0]).total_seconds().values / 60.0
    event_times = minutes[1:][ret.abs().values > thr]
    T = minutes[-1]
    print(f"  {len(event_times)} extreme-move events over {T/60/24:.0f} days")
    fit = fit_hawkes(event_times, T)
    if fit:
        mu, alpha, beta, n = fit
        print(f"  Fitted Hawkes: mu={mu:.4f}, alpha={alpha:.4f}, beta={beta:.4f}")
        print(f"  -> BRANCHING RATIO n = {n:.2f}  "
              f"({'self-exciting (events cluster!)' if n > 0.1 else 'near-Poisson'})")
        print(f"     i.e. each extreme move triggers ~{n:.2f} further moves on average.")
    return fit


# ---------------------------------------------------------------------------
# PART B — can Hawkes catch a VOLUME-MATCHED stealth pump?
# ---------------------------------------------------------------------------
def detection_experiment(n_ep=40, T_ep=200.0, base_rate=0.6, n_pump=0.7):
    """
    Normal episode  : Poisson(rate)            -> events spread evenly
    Pump episode    : Hawkes(mu,alpha,beta)    -> SAME expected count, but clustered
      Expected Hawkes count = mu*T/(1-n); set mu = rate*(1-n) to match volume.
    """
    print("\n=== PART B: DETECTION POWER (volume-matched stealth pumps) ===")
    beta = 1.0
    alpha = n_pump * beta
    mu_pump = base_rate * (1 - n_pump)            # volume-matched background

    n_hat, vol_count, label = [], [], []
    for _ in range(n_ep):
        # normal
        ev = simulate_poisson(base_rate, T_ep)
        f = fit_hawkes(ev, T_ep)
        if f: n_hat.append(f[3]); vol_count.append(len(ev)); label.append(0)
        # pump (same expected volume, clustered)
        ev = simulate_hawkes(mu_pump, alpha, beta, T_ep)
        f = fit_hawkes(ev, T_ep)
        if f: n_hat.append(f[3]); vol_count.append(len(ev)); label.append(1)

    n_hat, vol_count, label = map(np.array, (n_hat, vol_count, label))
    print(f"  episodes: {int((label==0).sum())} normal, {int((label==1).sum())} pump "
          f"(designed to have the SAME volume)")
    print(f"  avg events  — normal {vol_count[label==0].mean():.0f}, "
          f"pump {vol_count[label==1].mean():.0f}  (matched on purpose)")
    auc_vol = auc(vol_count, label)
    auc_haw = auc(n_hat, label)
    print(f"\n  Volume detector        : AUC = {auc_vol:.3f}  "
          f"({'blind, as expected' if abs(auc_vol-0.5) < 0.1 else 'sees some'})")
    print(f"  Hawkes branching ratio : AUC = {auc_haw:.3f}  "
          f"({'DETECTS the manipulation' if auc_haw > 0.7 else 'weak'})")
    print(f"\n  -> Hawkes branching ratio beats volume by "
          f"{auc_haw - auc_vol:+.3f} AUC on volume-matched stealth pumps.")
    print(f"     avg n_hat — normal {n_hat[label==0].mean():.2f}, "
          f"pump {n_hat[label==1].mean():.2f}")


if __name__ == "__main__":
    real_data_check("BTC-USD")
    detection_experiment()
