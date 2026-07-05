"""
real_data_validation.py (Improvement #4) — take the Hawkes detector to REAL data.

The detection metrics elsewhere are on simulation. Here we fit the Hawkes model
on REAL crypto (hourly) in consecutive weekly windows and ask: does the estimated
branching ratio rise during the windows containing the most violent, clustered
price action (the real-world signature manipulation would produce)?

HONEST SCOPE. This is a real-DATA step, not full validation: the extreme episodes
are a *proxy* for manipulation, not SEC-labelled spoofing or verified Telegram
pump events. A labelled dataset remains the definitive next step. But moving from
"works on simulation" to "the signal responds to real market bursts" is progress.
"""

import numpy as np
import yfinance as yf
from hawkes import fit_hawkes

COINS = ["DOGE-USD", "SHIB-USD", "XRP-USD"]
WIN_HOURS = 168   # one-week windows


def analyse(coin):
    px = yf.download(coin, period="720d", interval="1h",
                     auto_adjust=True, progress=False)["Close"].squeeze().dropna()
    if len(px) < 3 * WIN_HOURS:
        return None
    r = np.log(px / px.shift(1)).dropna()
    thr = r.abs().quantile(0.95)                  # "extreme move" threshold
    vals = r.values
    br, severity = [], []
    for s in range(0, len(vals) - WIN_HOURS, WIN_HOURS):
        seg = vals[s:s + WIN_HOURS]
        ev = np.where(np.abs(seg) > thr)[0].astype(float)
        if len(ev) < 5:
            continue
        f = fit_hawkes(ev, float(WIN_HOURS))
        if f and np.isfinite(f[3]):
            br.append(min(f[3], 0.999))
            severity.append(float(np.max(np.abs(seg))))   # window severity
    return np.array(br), np.array(severity)


def run():
    print("Fitting Hawkes on REAL crypto in weekly windows (branching ratio vs severity)\n")
    print(f"{'coin':>10} {'weeks':>6} {'corr(n, severity)':>18} "
          f"{'n: calm weeks':>14} {'n: violent weeks':>16}")
    for coin in COINS:
        out = analyse(coin)
        if out is None:
            print(f"{coin:>10}   data unavailable"); continue
        br, sev = out
        if len(br) < 8:
            print(f"{coin:>10}   too few windows"); continue
        corr = np.corrcoef(br, sev)[0, 1]
        hi = sev >= np.percentile(sev, 70)        # most violent 30% of weeks
        lo = sev <= np.percentile(sev, 30)        # calmest 30%
        print(f"{coin:>10} {len(br):>6} {corr:>18.2f} "
              f"{br[lo].mean():>14.2f} {br[hi].mean():>16.2f}")

    print("\nReading: a POSITIVE corr(n, severity) and a higher branching ratio in the")
    print("most violent weeks means the detector's core quantity behaves as expected on")
    print("REAL data — self-excitation rises when real price action clusters violently.")
    print("Honest limit: proxy episodes, not labelled pumps; labelled data is the next step.")


if __name__ == "__main__":
    run()
