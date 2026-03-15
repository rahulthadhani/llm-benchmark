import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# ── Load scored results ──────────────────────────────────────────────
df = pd.read_csv("results/scored_results.csv")

os.makedirs("results", exist_ok=True)

# ── Color palette (one color per strategy) ───────────────────────────
COLORS = {
    "zero_shot":        "#4F8EF7",
    "few_shot":         "#F7874F",
    "chain_of_thought": "#4FBF67",
    "role_prompting":   "#A44FF7",
}

STRATEGY_LABELS = {
    "zero_shot":        "Zero-shot",
    "few_shot":         "Few-shot",
    "chain_of_thought": "Chain-of-thought",
    "role_prompting":   "Role prompting",
}

# ════════════════════════════════════════════════════════════════════
# Chart 1 — Overall accuracy per strategy (horizontal bar chart)
# ════════════════════════════════════════════════════════════════════
overall = (
    df.groupby("strategy")["score"]
    .mean()
    .rename(index=STRATEGY_LABELS)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(
    overall.index,
    overall.values,
    color=[COLORS[k] for k in df.groupby("strategy")["score"].mean().sort_values().index],
    height=0.5,
    edgecolor="none",
)

# Add value labels on bars
for bar, val in zip(bars, overall.values):
    ax.text(
        val + 0.01, bar.get_y() + bar.get_height() / 2,
        f"{val:.0%}", va="center", fontsize=11
    )

ax.set_xlim(0, 1.15)
ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
ax.set_xlabel("Mean accuracy", fontsize=11)
ax.set_title("Overall accuracy by prompting strategy", fontsize=13, pad=12)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("results/chart_overall.png", dpi=150)
plt.close()
print("Saved: results/chart_overall.png")


# ════════════════════════════════════════════════════════════════════
# Chart 2 — Accuracy per strategy per category (grouped bar chart)
# ════════════════════════════════════════════════════════════════════
pivot = (
    df.groupby(["category", "strategy"])["score"]
    .mean()
    .unstack("strategy")
    .rename(columns=STRATEGY_LABELS)
)

fig, ax = plt.subplots(figsize=(10, 5))
pivot.plot(
    kind="bar",
    ax=ax,
    color=[COLORS[k] for k in pivot.columns.map(
        {v: k for k, v in STRATEGY_LABELS.items()}
    )],
    width=0.7,
    edgecolor="none",
)

ax.set_ylim(0, 1.2)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
ax.set_xlabel("Category", fontsize=11)
ax.set_ylabel("Mean accuracy", fontsize=11)
ax.set_title("Accuracy by category and prompting strategy", fontsize=13, pad=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=11)
ax.legend(title="Strategy", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("results/chart_by_category.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: results/chart_by_category.png")


# ════════════════════════════════════════════════════════════════════
# Chart 3 — Heatmap: strategy × category
# ════════════════════════════════════════════════════════════════════
heatmap_data = (
    df.groupby(["strategy", "category"])["score"]
    .mean()
    .unstack("category")
    .rename(index=STRATEGY_LABELS)
)

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".0%",
    cmap="YlGn",
    linewidths=0.5,
    linecolor="#e0e0e0",
    vmin=0,
    vmax=1,
    ax=ax,
    cbar_kws={"format": mtick.PercentFormatter(xmax=1)},
)
ax.set_title("Accuracy heatmap — strategy vs category", fontsize=13, pad=12)
ax.set_xlabel("Category", fontsize=11)
ax.set_ylabel("Strategy", fontsize=11)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("results/chart_heatmap.png", dpi=150)
plt.close()
print("Saved: results/chart_heatmap.png")


# ════════════════════════════════════════════════════════════════════
# Summary table
# ════════════════════════════════════════════════════════════════════
print("\n--- Full summary table ---")
summary = (
    df.groupby(["strategy", "category"])["score"]
    .mean()
    .round(2)
    .unstack("category")
    .rename(index=STRATEGY_LABELS)
)
print(summary.to_string())
print("\nDone. All charts saved to results/")