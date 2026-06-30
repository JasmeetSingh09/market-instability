"""
Run the full "Three Lenses on Market Instability" framework end to end:
  1. Spectral  — Random Matrix Theory      (../rmt_portfolio/rmt.py)
  2. Geometric — Topological Data Analysis  (../tda_crash_detection/tda_crash.py)
  3. Temporal  — Hawkes manipulation detector (../hawkes_pump_detection/detect.py)

Each sub-project is self-contained and tested; this just orchestrates them and
prints one combined report. (It is slow — each stage downloads data and fits.)
"""

import os
import sys
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))

STAGES = [
    ("1. SPECTRAL  — Random Matrix Theory (covariance noise -> better portfolios)",
     "1_spectral_rmt", "rmt.py"),
    ("2. GEOMETRIC — Topological Data Analysis (a rigorous crash-warning audit)",
     "2_geometric_tda", "tda_crash.py"),
    ("3. TEMPORAL  — Hawkes processes (self-excitation -> manipulation detection)",
     "3_temporal_hawkes", "detect.py"),
]


def main():
    print("#" * 72)
    print("#  THREE MATHEMATICAL LENSES ON MARKET INSTABILITY")
    print("#  spectral (RMT)  +  geometric (TDA)  +  temporal (Hawkes)")
    print("#" * 72)
    for title, folder, script in STAGES:
        path = os.path.join(BASE, folder)
        print("\n" + "=" * 72)
        print(f"  {title}")
        print("=" * 72)
        if not os.path.exists(os.path.join(path, script)):
            print(f"  [skipped] {folder}/{script} not found")
            continue
        subprocess.run([sys.executable, script], cwd=path)
    print("\n" + "#" * 72)
    print("#  DONE — see each folder's README.md for the written-up findings.")
    print("#" * 72)


if __name__ == "__main__":
    main()
