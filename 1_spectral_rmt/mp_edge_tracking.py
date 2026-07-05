"""
mp_edge_tracking.py (Improvement #3) — beyond the market mode.

The spectral coordinate R = lambda_max/N tracks only the single largest ("market
mode") eigenvalue. But sectors often synchronise BEFORE the whole market does.
Random Matrix Theory gives a principled threshold: the Marchenko-Pastur upper
edge lambda_+ = sigma^2 (1 + sqrt(q))^2, q = N/W. Eigenvalues above lambda_+ are
statistically real structure, not noise.

We track  k_t = number of eigenvalues above lambda_+ EXCLUDING the market mode
(i.e. genuine sector/localised synchronisation), and test whether k_t provides
crash early-warning — and whether it LEADS the market-mode signal R.
"""

import numpy as np
import pandas as pd
import yfinance as yf

W, BENCH = 60, "^NSEI"
TICKERS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS","ITC.NS",
           "SBIN.NS","LT.NS","HINDUNILVR.NS","BHARTIARTL.NS","AXISBANK.NS","WIPRO.NS",
           "ONGC.NS","HCLTECH.NS","SUNPHARMA.NS","TATASTEEL.NS"]
rng = np.random.default_rng(0)


def auc(score, label):
    s = np.asarray(score, float); y = np.asarray(label, int)
    m = np.isfinite(s) & np.isfinite(y); s, y = s[m], y[m]
    pos, neg = (y == 1), (y == 0)
    if pos.sum() == 0 or neg.sum() == 0: return np.nan
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    a = (r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum())
    return max(a, 1 - a)


def build():
    px = yf.download(TICKERS + [BENCH], start="2010-01-01", end="2024-12-31",
                     auto_adjust=True, progress=False)["Close"]
    good = [t for t in TICKERS if px[t].notna().mean() > 0.9]
    px = px[good + [BENCH]].dropna()
    R_ = px[good].pct_change().dropna().values
    bench = px[BENCH].pct_change().dropna()
    dates = px[good].pct_change().dropna().index
    rows = []
    for e in range(W, len(R_)):
        win = R_[e - W:e]
        C = np.clip(np.corrcoef(win.T), -1, 1)
        vals = np.sort(np.linalg.eigvalsh(C))[::-1]           # descending
        N = len(vals)
        q = N / W
        sigma2 = max(1.0 - vals[0] / N, 1e-6)                 # variance outside market mode
        lam_plus = sigma2 * (1 + np.sqrt(q)) ** 2
        k = int(np.sum(vals[1:] > lam_plus))                 # sector modes above the noise edge
        R = vals[0] / N
        rows.append((dates[e], R, k, lam_plus))
    return pd.DataFrame(rows, columns=["date","R","k_edge","lam_plus"]).set_index("date"), bench


def run():
    print("Tracking eigenvalues above the Marchenko-Pastur edge ...")
    df, bench = build()
    fwd = bench.shift(-1).rolling(20).sum().shift(-19)
    df["crash"] = (fwd < -0.10).astype(int).reindex(df.index)
    df = df.dropna()
    y = df["crash"].values

    print(f"\n  avg # sector eigenvalues above lambda_+ : {df['k_edge'].mean():.2f} "
          f"(range {df['k_edge'].min()}-{df['k_edge'].max()})")

    print("\n=== Crash-warning AUC ===")
    print(f"  R (market mode, lambda_max/N) : AUC = {auc(df['R'], y):.3f}")
    print(f"  k_edge (# sector modes > lam+): AUC = {auc(df['k_edge'], y):.3f}")
    print(f"  R + k_edge (z-sum)            : AUC = {auc((df['R']-df['R'].mean())/df['R'].std() + (df['k_edge']-df['k_edge'].mean())/df['k_edge'].std(), y):.3f}")

    print("\n=== Does k_edge LEAD the market-mode signal before crashes? ===")
    onsets = np.where(np.diff(df['crash'].values) == 1)[0] + 1
    idx = df.index
    def lead(col):
        z = ((df[col]-df[col].mean())/df[col].std()).values
        thr = np.nanpercentile(z, 80); leads = []
        for o in onsets:
            lb = z[max(0,o-40):o]
            fire = np.where(lb > thr)[0]
            if len(fire): leads.append(len(lb) - fire[0])
        return np.mean(leads) if leads else np.nan
    print(f"  R      peaks ~{lead('R'):.0f} trading days before crash onset")
    print(f"  k_edge peaks ~{lead('k_edge'):.0f} trading days before crash onset")
    print("\n  Interpretation: if k_edge leads R, sector-level synchronisation (more")
    print("  eigenvalues escaping the MP noise band) is an EARLIER warning than the")
    print("  single market-mode eigenvalue absorbing all the variance.")


if __name__ == "__main__":
    run()
