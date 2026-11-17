"""Roofline plot for batch-1 decode on existing hardware.

Reads ergebnisse/roofline.csv (device, memory bandwidth GB/s, peak TFLOPS) and draws
attainable TFLOPS = min(peak, bandwidth x arithmetic intensity) per device, with the
batch-1 decode point for 4-bit weights (2 FLOP per weight on 4.125 bits = 0.516 bytes: 3.88 FLOP/B).

    python roofline_plot.py                       # writes out/roofline.png and prints the table
    python roofline_plot.py --out ../ergebnisse/roofline_bestehende_hardware.png
"""
import argparse
import csv
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "ergebnisse" / "roofline.csv"
DECODE_AI = 2 / (4.125 / 8)  # FLOP per byte, batch 1, 4-bit weights plus one fp16 scale per 128
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(CSV))
    ap.add_argument("--out", default=str(HERE / "out" / "roofline.png"))
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv)))
    print(f"decode intensity {DECODE_AI:.2f} FLOP/B")
    print("| device | BW GB/s | peak TFLOPS | ridge FLOP/B | share of peak at decode |\n|---|---|---|---|---|")
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.color": "#e4e3df",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb"})
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ai = np.logspace(np.log10(0.3), np.log10(2000), 400)
    for i, r in enumerate(rows):
        bw, peak = float(r["bw_GBps"]), float(r["peak_TFLOPS"])
        ridge = peak * 1e3 / bw
        share = bw * DECODE_AI / 1e3 / peak
        print(f"| {r['device']} | {bw:,.0f} | {peak:g} ({r['peak_basis']}) | {ridge:.0f} | {100 * share:.1f}% |")
        ax.plot(ai, np.minimum(peak, bw * ai / 1e3), color=PAL[i % len(PAL)], lw=2,
                label=f"{r['device']} (ridge {ridge:.0f})")
    ax.axvline(DECODE_AI, color="#52514e", lw=1, ls="--")
    ax.text(DECODE_AI * 1.12, 0.12, f"batch-1 decode,\n4-bit weights:\n{DECODE_AI:.1f} FLOP/B", fontsize=8, color="#52514e")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("arithmetic intensity (FLOP/byte)"); ax.set_ylabel("attainable TFLOPS")
    ax.set_title("Roofline: batch-1 decode sits far left of every ridge point", loc="left", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
