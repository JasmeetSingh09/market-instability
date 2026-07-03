"""
complementarity.py — DON'T assert the three lenses are complementary; SHOW it.

The thesis claims spectral (R), geometric (T), and temporal (H) are three
complementary views of one phenomenon. A reviewer rightly asks: prove it. We test
complementarity three ways:

  1. REDUNDANCY  — pairwise correlation of the three signals. Weak correlation =
     they carry different information (complementary); high = redundant.
  2. UNIQUE VALUE — leave-one-out: does removing a lens lower crash-warning AUC?
     If so, that lens explains variance the other two do not.
  3. TIMING       — before a crash, which lens peaks first? Different lead times =
     they respond to different stages of fragility.
"""

import numpy as np
import pandas as pd
from fragility_space import build, auc, z

rng = np.random.default_rng(0)


def run():
    df = build()
    y = df["crash"].values
    S = df[["R", "T", "H"]]

    print("=== 1. REDUNDANCY: pairwise correlation of the three lenses ===")
    corr = S.corr()
    print(corr.round(2).to_string())
    off = [abs(corr.iloc[0, 1]), abs(corr.iloc[0, 2]), abs(corr.iloc[1, 2])]
    print(f"  mean |correlation| = {np.mean(off):.2f}  "
          f"-> {'weak (complementary)' if np.mean(off) < 0.5 else 'overlapping'}")

    print("\n=== 2. UNIQUE VALUE: leave-one-out crash-warning AUC ===")
    full = z(df["R"]) + z(df["T"]) + z(df["H"])
    auc_full = auc(full, y)
    print(f"  all three (R+T+H): AUC = {auc_full:.3f}")
    for drop in ["R", "T", "H"]:
        keep = [c for c in ["R", "T", "H"] if c != drop]
        partial = sum(z(df[c]) for c in keep)
        a = auc(partial, y)
        print(f"  drop {drop}: AUC = {a:.3f}   (change {a - auc_full:+.3f} -> "
              f"{'adds unique info' if a < auc_full - 0.005 else 'little unique info'})")

    print("\n=== 3. TIMING: which lens peaks first before a crash? ===")
    crash = df["crash"].values
    onsets = np.where(np.diff(crash) == 1)[0] + 1
    idx = df.index
    leads = {"R": [], "T": [], "H": []}
    zsig = {c: z(df[c]).values for c in ["R", "T", "H"]}
    for o in onsets:
        lb = slice(max(0, o - 40), o)                 # 40 trading days before onset
        if o - max(0, o - 40) < 10:
            continue
        for c in ["R", "T", "H"]:
            seg = zsig[c][lb]
            if len(seg):
                peak_pos = int(np.argmax(seg))         # where the signal peaked
                leads[c].append((o - max(0, o - 40)) - peak_pos)  # trading days before onset
    if all(leads[c] for c in leads):
        n = len(leads["R"])
        print(f"  crashes analysed: {n}")
        for c, name in [("R", "Spectral"), ("T", "Geometric"), ("H", "Temporal")]:
            arr = np.array(leads[c], float)
            bs = [np.mean(rng.choice(arr, len(arr), replace=True)) for _ in range(2000)]
            lo, hi = np.percentile(bs, [2.5, 97.5])
            print(f"  {name:9s}: {arr.mean():.0f} days [95% CI {lo:.0f},{hi:.0f}]")

        # Is 'structure leads temporal' statistically real? paired test.
        struct = (np.array(leads["R"], float) + np.array(leads["T"], float)) / 2
        temporal = np.array(leads["H"], float)
        diff = struct - temporal                                  # >0 => structure earlier
        # paired bootstrap CI of the mean difference
        bd = [np.mean(rng.choice(diff, len(diff), replace=True)) for _ in range(5000)]
        lo, hi = np.percentile(bd, [2.5, 97.5])
        # permutation test: randomly flip the sign of each paired diff
        obs = diff.mean()
        perm = [np.mean(diff * rng.choice([-1, 1], len(diff))) for _ in range(5000)]
        pval = np.mean(np.abs(perm) >= abs(obs))
        print(f"\n  Structure-minus-temporal lead: {obs:+.0f} days "
              f"[95% CI {lo:+.0f},{hi:+.0f}], permutation p = {pval:.3f}")
        sig = (lo > 0 or hi < 0) and pval < 0.05
        print(f"  -> staged timing (structure BEFORE temporal) is "
              f"{'STATISTICALLY SIGNIFICANT' if sig else 'suggestive but NOT significant'} "
              f"(n={n} crashes — small sample).")

    print("\nVerdict: weak inter-lens correlation + each lens adding unique AUC +")
    print("distinct lead times are evidence of complementarity — but the lead-time")
    print("DIFFERENCE is only claimed as significant if the test above says so.")


if __name__ == "__main__":
    run()
