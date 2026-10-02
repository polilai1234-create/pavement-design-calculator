"""
Generates an animated GIF showing how pavement layer thicknesses
change as traffic load (ESAL) increases, for a fixed subgrade CBR.

Run: python make_animation.py
Output: pavement_animation.gif
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import io

from pavement import design_pavement

CBR = 6  # fixed subgrade strength for the demo
esal_values = np.linspace(0.5, 10, 24)  # million ESALs, 24 frames

frames = []

for esal in esal_values:
    result = design_pavement(esal_millions=esal, cbr=CBR)

    layers = ["Surface", "Base", "Sub-base"]
    thicknesses = [result["surface_cm"], result["base_cm"], result["subbase_cm"]]
    colors = ["#2b2b2b", "#8a8a8a", "#c9b38c"]

    fig, ax = plt.subplots(figsize=(5, 6))
    bottom = 0
    for layer, t, c in zip(layers, thicknesses, colors):
        ax.bar(0, t, bottom=bottom, width=0.6, color=c, edgecolor="white", label=layer)
        ax.text(0, bottom + t / 2, f"{layer}\n{t} cm", ha="center", va="center",
                 color="white" if layer != "Sub-base" else "black", fontsize=10, fontweight="bold")
        bottom += t

    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 45)
    ax.set_xticks([])
    ax.set_ylabel("Depth (cm)")
    ax.set_title(f"Pavement Design\nESAL = {esal:.1f} million | CBR = {CBR}% | Total = {result['total_cm']} cm")
    ax.invert_yaxis()

    fig.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.08)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    img = imageio.imread(buf)[:, :, :3]  # drop alpha channel for consistency
    frames.append(img)

# Hold the last frame a bit longer, then loop
frames_out = frames + [frames[-1]] * 6

imageio.mimsave("pavement_animation.gif", frames_out, duration=0.15, loop=0)
print("Saved pavement_animation.gif")
