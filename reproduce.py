"""
reproduce.py — one command to regenerate every headline result in this project.

    python reproduce.py            # run all experiments in order
    python reproduce.py --quick    # skip the slow (ripser / long-history) ones

This is the "benchmark package" entry point: a reviewer or judge can clone the repo,
install requirements, and reproduce the tables and findings end to end. Each block
prints its own honest result (including the nulls). Network access to Yahoo Finance is
required; runtimes are noted per block.
"""

import os
import sys
import time
import runpy
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))

QUICK = "--quick" in sys.argv

# (module, one-line description, slow?)  slow = ripser / long download
EXPERIMENTS = [
    ("redundancy_analysis",     "Proposition T~1-1/(NR^2): derive + validate + breakdown", False),
    ("geometric_independence",  "Geometric lens: PH is independent (-0.37) but not predictive", True),
    ("geometric_role",          "Does topology separate regimes? (honest null)", True),
    ("ricci_curvature",         "Ollivier-Ricci curvature: predictive but redundant (+0.91)", True),
    ("rq_a_regime_divergence",  "RQ-A: spectral-topology coupling is regime-dependent (discovery)", True),
    ("cross_market_prediction", "9 markets x baselines + bootstrap CIs: no predictive edge (0/9)", False),
    ("crisis_trajectories",     "Do crises share a path? Heterogeneous (2nd discovery)", False),
    ("multimarket",             "Universality: self-excitation ~0.6, cleaning helps everywhere", False),
    ("3_temporal_hawkes/branching_criticality",
                                "Branching criticality: crashes don't approach n=1 (null)", False),
]


def main():
    print("=" * 78)
    print(" REPRODUCING: A Multi-Lens Framework for Characterizing Market Fragility")
    print(" (mode:", "QUICK — skipping slow experiments" if QUICK else "FULL", ")")
    print("=" * 78)
    results = []
    for mod, desc, slow in EXPERIMENTS:
        if QUICK and slow:
            print(f"\n[skip] {mod:38s} {desc}")
            results.append((mod, "skipped"))
            continue
        print("\n" + "-" * 78)
        print(f"[run ] {mod}\n       {desc}")
        print("-" * 78)
        t0 = time.time()
        try:
            path = os.path.join(HERE, mod + ".py")
            folder = os.path.dirname(path)
            # let subfolder scripts import their local modules (e.g. hawkes.py)
            if folder not in sys.path:
                sys.path.insert(0, folder)
            runpy.run_path(path, run_name="__main__")
            results.append((mod, f"ok ({time.time()-t0:.0f}s)"))
        except Exception:
            traceback.print_exc()
            results.append((mod, "ERROR"))

    print("\n" + "=" * 78)
    print(" SUMMARY")
    print("=" * 78)
    for mod, status in results:
        print(f"  {status:>12}  {mod}")
    print("\nHeadline findings (see DISCOVERY_AND_PLAN.md and FRAGILITY_THEOREM.md):")
    print("  * Proposition T ~ 1 - 1/(NR^2) holds under a dominant market mode (bounded).")
    print("  * Geometric lens: topology independent but not predictive; curvature")
    print("    predictive but ~0.91 redundant with spectral -> no free lunch.")
    print("  * EMPIRICAL FINDING 1: spectral-topology coupling is regime-dependent")
    print("    (-0.09 calm -> -0.36 crisis).")
    print("  * EMPIRICAL FINDING 2: crises do NOT share a common path through Fragility")
    print("    Space (heterogeneous classes of crises).")
    print("  * Across 9 markets, NO significant out-of-sample predictive edge over simple")
    print("    baselines (bootstrap CIs include 0). Characterization, not prediction.")


if __name__ == "__main__":
    main()
