"""Standalone scientific figures from measured JSON; no re-estimated metrics."""
import json
from pathlib import Path

from .data import ROOT


def render_figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    public = ROOT / "artifacts/public"
    output = public / "figures"
    output.mkdir(exist_ok=True)
    colors = {"BantengPanel": "#087e72", "Global-MAF": "#315779", "Random-mean": "#c38e37"}
    for name in ["dryad", "figshare"]:
        data = json.loads((public / f"{name}_benchmark.json").read_text())
        pop = data["population"]
        fig, ax = plt.subplots(figsize=(9, 6), constrained_layout=True)
        for breed in pop["includedBreeds"]:
            points = [p for p in pop["points"] if p["breed"] == breed]
            if points:
                ax.scatter([p["pc1"] for p in points], [p["pc2"] for p in points], s=30, label=f"{breed} (n={len(points)})", alpha=.8)
        for p in pop["points"]:
            if p["atypicalReview"]:
                ax.scatter(p["pc1"], p["pc2"], s=120, facecolors="none", edgecolors="black", linewidth=1.3)
                ax.annotate(p["sampleId"], (p["pc1"], p["pc2"]), fontsize=7, xytext=(4, 5), textcoords="offset points")
        v = pop["explainedVarianceRatio"]
        ax.set(xlabel=f"PC1 ({v[0]:.1%})", ylabel=f"PC2 ({v[1]:.1%})", title=f"{name.title()}: descriptive PCA, {pop['nMarkers']} spaced SNPs")
        ax.legend(fontsize=8, loc="best"); ax.grid(alpha=.15)
        fig.text(.5, -.015, "Full-cohort descriptive projection; rings mark review candidates, not confirmed introgression", ha="center", fontsize=8)
        for ext in ["svg", "png"]:
            fig.savefig(output / f"{name}_pca.{ext}", dpi=160, bbox_inches="tight")
        plt.close(fig)
        ancestry = data["ancestry"]
        fig, axes = plt.subplots(1, len(ancestry["donorBreeds"]), figsize=(11, 4.5), squeeze=False, constrained_layout=True)
        for ax, donor in zip(axes[0], ancestry["donorBreeds"]):
            for method, color in colors.items():
                r = [r for r in ancestry["results"] if r["donorBreed"] == donor and r["method"] == method]
                r.sort(key=lambda z: z["size"])
                ax.plot([s["size"] for s in r], [s["maeMean"] for s in r], ".-", color=color, label=method)
            ax.set(xlabel="SNPs", ylabel="Mean absolute error of q", title=f"Bali / {donor} references")
            ax.set_ylim(bottom=0); ax.grid(alpha=.15); ax.legend(fontsize=8)
        fig.suptitle(f"{name.title()}: S1 unlinked Mendelian simulation (not real-cattle validation)", fontsize=12)
        for ext in ["svg", "png"]:
            fig.savefig(output / f"{name}_ancestry.{ext}", dpi=160, bbox_inches="tight")
        plt.close(fig)
    return output
