"""
HERO VISUAL #3 — the Hawkes conditional intensity lambda(t).

A timeline of trade-events that is calm (Poisson) -> a self-exciting PUMP
(Hawkes burst) -> calm again. The conditional intensity lambda(t) stays flat
during normal trading but EXPLODES during the pump, because each event triggers
the next. This is the visual signature of coordinated manipulation that a plain
volume count would miss.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hawkes import simulate_hawkes, simulate_poisson, rng

ALPHA, BETA = 0.9, 1.0          # branching ratio n = 0.9 (strong self-excitation)
MU_BG = 0.4

# calm -> pump -> calm
calm1 = simulate_poisson(MU_BG, 80)
pump = 80 + simulate_hawkes(0.15, ALPHA, BETA, 50)
calm2 = 130 + simulate_poisson(MU_BG, 70)
events = np.sort(np.concatenate([calm1, pump, calm2]))

# conditional intensity on a fine grid
grid = np.linspace(0, 200, 3000)
lam = np.array([MU_BG + ALPHA * np.sum(np.exp(-BETA * (t - events[events < t])))
                for t in grid])

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.axvspan(80, 130, color="red", alpha=0.10, label="pump window (self-exciting)")
ax.plot(grid, lam, color="darkorange", lw=1.6, label=r"conditional intensity $\lambda(t)$")
ax.plot(events, np.full_like(events, -0.3), "|", color="steelblue",
        markersize=8, label="trade events")
ax.axhline(MU_BG, color="gray", ls="--", lw=1, label=r"background rate $\mu$")
ax.set_title("Hawkes self-excitation: intensity explodes during a pump\n"
             r"(each event triggers the next; branching ratio $n=\alpha/\beta=0.9$)")
ax.set_xlabel("time"); ax.set_ylabel(r"intensity $\lambda(t)$ (events / unit time)")
ax.legend(loc="upper right"); ax.set_ylim(-0.6, None)
plt.tight_layout()
plt.savefig("hawkes_intensity.png", dpi=140)
print(f"events: {len(events)} | peak intensity {lam.max():.1f} vs background {MU_BG}")
print("Saved hawkes_intensity.png")
