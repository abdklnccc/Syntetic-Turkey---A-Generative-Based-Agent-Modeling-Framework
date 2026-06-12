from __future__ import annotations

import json
import os
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib-syntetic-turkey")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
SOULS = ROOT / "souls"
TRAJECTORIES = OUTPUTS / "agent_trajectories.csv"
OUT = OUTPUTS / "notebook_analysis"
CHARTS = OUT / "charts"
TABLES = OUT / "tables"
NOTEBOOK = OUTPUTS / "deep_analysis_300_agents.ipynb"

CANDIDATES = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"]
PARTIES = ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP", "YRP", "Other", "Undecided"]
FIRST_TICK = "T001"
FIRST_ROUND_TICK = "T030A_first_round_vote_decision"
RUNOFF_TICK = "T035A_runoff_vote_decision"
COLORS = {
    "Erdogan": "#a61e24",
    "Kilicdaroglu": "#1f5fbf",
    "Sinan_Ogan": "#6f43c0",
    "Muharrem_Ince": "#188f9d",
    "AKP": "#a61e24",
    "CHP": "#1f5fbf",
    "MHP": "#6f43c0",
    "IYI": "#167a9d",
    "DEM_HDP_YSP": "#2f855a",
    "YRP": "#b7791f",
    "Other": "#737b88",
    "Undecided": "#a0a7b4",
}


def nice(text: str) -> str:
    return str(text).replace("_", " ")


def souls() -> dict[str, dict[str, Any]]:
    data = {}
    for path in sorted(SOULS.glob("agent_*.json")):
        if len(path.stem) == len("agent_001"):
            soul = json.loads(path.read_text(encoding="utf-8"))
            data[soul["identity"]["agent_id"]] = soul
    return data


def baseline(soul: dict[str, Any], key: str) -> str:
    meta = soul.get("simulation_metadata", {}).get("baseline_2018", {})
    numeric = soul.get("numeric_profile", {}).get("baseline_2018", {})
    return str(meta.get(key) or numeric.get(key) or "Unknown")


def style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.grid": True,
            "grid.color": "#edf1f6",
            "axes.edgecolor": "#d8dee8",
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
        }
    )


def save(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close()


def count_chart(before: Counter[str], after: Counter[str], keys: list[str], title: str, path: Path) -> None:
    x = np.arange(len(keys))
    width = 0.38
    _, ax = plt.subplots(figsize=(12, 6.2))
    ax.bar(x - width / 2, [before.get(k, 0) for k in keys], width, label="2018 baseline", color="#7b8495")
    ax.bar(x + width / 2, [after.get(k, 0) for k in keys], width, label="2023 simulated", color=[COLORS.get(k, "#1f5fbf") for k in keys])
    for i, key in enumerate(keys):
        ax.text(i - width / 2, before.get(key, 0) + 1, str(before.get(key, 0)), ha="center", fontsize=9)
        ax.text(i + width / 2, after.get(key, 0) + 1, str(after.get(key, 0)), ha="center", fontsize=9)
    ax.set_title(title, fontsize=15, pad=14)
    ax.set_ylabel("Agents")
    ax.set_xticks(x, [nice(k) for k in keys], rotation=25, ha="right")
    ax.legend(frameon=False, ncols=2)
    save(path)


def heatmap(table: pd.DataFrame, source: str, target: str, title: str, path: Path) -> None:
    matrix = table.pivot(index=source, columns=target, values="agents").fillna(0).astype(int)
    _, ax = plt.subplots(figsize=(max(8, 1.25 * len(matrix.columns) + 3), max(5, 0.65 * len(matrix.index) + 2)))
    image = ax.imshow(matrix.values, cmap="Blues")
    ax.set_title(title, fontsize=15, pad=14)
    ax.set_xlabel("2023 simulated top choice")
    ax.set_ylabel("2018 baseline")
    ax.set_xticks(np.arange(len(matrix.columns)), [nice(c) for c in matrix.columns], rotation=30, ha="right")
    ax.set_yticks(np.arange(len(matrix.index)), [nice(i) for i in matrix.index])
    max_value = max(1, int(matrix.values.max()))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = int(matrix.iat[i, j])
            if value:
                color = "white" if value > max_value * 0.45 else "#172033"
                ax.text(j, i, str(value), ha="center", va="center", color=color, fontsize=10, weight="bold")
    plt.colorbar(image, ax=ax, fraction=0.035, pad=0.03, label="Agents")
    save(path)


def probability_lines(prob: pd.DataFrame, keys: list[str], title: str, path: Path, ymax: int) -> None:
    _, ax = plt.subplots(figsize=(13.5, 6.8))
    x = np.arange(len(prob))
    for key in keys:
        ax.plot(x, prob[key], label=nice(key), color=COLORS.get(key), linewidth=2.6, marker="o", markersize=3.5)
    for tick, linestyle in [(FIRST_ROUND_TICK, "--"), (RUNOFF_TICK, ":")]:
        if tick in set(prob["tick_id"]):
            ax.axvline(prob.index[prob["tick_id"].eq(tick)][0], color="#263244", linestyle=linestyle, linewidth=1.2, alpha=0.7)
    shown = [i for i in range(len(prob)) if i % 4 == 0 or i == len(prob) - 1]
    ax.set_title(title, fontsize=15, pad=14)
    ax.set_ylabel("Mean probability weight (%)")
    ax.set_ylim(0, ymax)
    ax.set_xticks(shown, prob.loc[shown, "tick_id"], rotation=35, ha="right")
    ax.legend(frameon=False, ncols=3)
    save(path)


def shift_heatmap(shifts: pd.DataFrame, keys: list[str], title: str, path: Path) -> None:
    matrix = shifts.set_index("archetype_name")[keys]
    lim = max(5, float(np.abs(matrix.values).max()))
    _, ax = plt.subplots(figsize=(12, max(6, 0.5 * len(matrix.index) + 2)))
    image = ax.imshow(matrix.values, cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_title(title, fontsize=15, pad=14)
    ax.set_xticks(np.arange(len(keys)), [nice(k) for k in keys], rotation=30, ha="right")
    ax.set_yticks(np.arange(len(matrix.index)), matrix.index)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix.iat[i, j]:+.1f}", ha="center", va="center", fontsize=8.5)
    plt.colorbar(image, ax=ax, fraction=0.035, pad=0.03, label="percentage-point shift")
    save(path)


def small_multiples(prob: pd.DataFrame, keys: list[str], title: str, path: Path) -> None:
    personas = list(OrderedDict.fromkeys(prob["archetype_name"].tolist()))
    cols = 3
    rows = int(np.ceil(len(personas) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 3.45), sharex=True, sharey=True)
    axes = np.array(axes).reshape(-1)
    for ax, persona in zip(axes, personas):
        part = prob[prob["archetype_name"].eq(persona)].reset_index(drop=True)
        x = np.arange(len(part))
        for key in keys:
            ax.plot(x, part[key], color=COLORS.get(key), linewidth=1.9, label=nice(key))
        shown = [i for i in range(len(part)) if i in (0, len(part) - 1) or i % 12 == 0]
        ax.set_title(persona, fontsize=10.5)
        ax.set_ylim(0, 100)
        ax.set_xticks(shown, part.loc[shown, "tick_id"], rotation=30, ha="right", fontsize=8)
    for ax in axes[len(personas):]:
        ax.axis("off")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.suptitle(title, fontsize=16, fontweight="bold", x=0.02, ha="left")
    fig.legend(handles, labels, loc="lower center", ncols=len(keys), frameon=False)
    fig.subplots_adjust(bottom=0.08)
    save(path)


def md(source: str) -> dict[str, Any]:
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip().splitlines(True)}


def code(source: str) -> dict[str, Any]:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.strip().splitlines(True)}


def notebook(summary: dict[str, Any]) -> dict[str, Any]:
    cells = [
        md(f"""# Synthetic Turkey: 300-Agent Deep Analysis Notebook

Built from `outputs/agent_trajectories.csv` and the 300 canonical `souls/agent_*.json` files.

Run scope: **{summary['agents']} agents**, **{summary['ticks']} ticks**.

First-round decision tick: `{FIRST_ROUND_TICK}` ({summary['first_round_date']}).
Runoff decision tick: `{RUNOFF_TICK}` ({summary['runoff_date']}).

This notebook distinguishes top-choice counts from mean probability weights. Counts show the winning option per agent; probability weights show soft movement and uncertainty through the ticks."""),
        code("""from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "notebook_analysis" / "tables"
CHARTS = OUTPUTS / "notebook_analysis" / "charts"
trajectories = pd.read_csv(OUTPUTS / "agent_trajectories.csv")
trajectories.head()"""),
        md(f"""## 1. Initial Votes vs Latest Votes

Presidential top-choice counts:

- Erdoğan: `{summary['candidate2018'].get('Erdogan', 0)}` in 2018 → `{summary['candidate2023'].get('Erdogan', 0)}` in 2023.
- Muharrem İnce: `{summary['candidate2018'].get('Muharrem_Ince', 0)}` in 2018 → `{summary['candidate2023'].get('Muharrem_Ince', 0)}` in 2023.
- Kılıçdaroğlu: `{summary['candidate2023'].get('Kilicdaroglu', 0)}` in 2023 first-round top choices.

Party top-choice counts:

- AKP: `{summary['party2018'].get('AKP', 0)}` in 2018 → `{summary['party2023'].get('AKP', 0)}` in 2023.
- CHP: `{summary['party2018'].get('CHP', 0)}` in 2018 → `{summary['party2023'].get('CHP', 0)}` in 2023."""),
        md("![Presidential counts](notebook_analysis/charts/01_candidate_counts_2018_vs_2023.png)"),
        md("![Party counts](notebook_analysis/charts/02_party_counts_2018_vs_2023.png)"),
        md("## 2. Vote Flow Matrices\n\nThese are transition matrices from 2018 baseline memory to simulated 2023 top choices."),
        md("![Candidate transition matrix](notebook_analysis/charts/03_candidate_transition_matrix.png)"),
        md("![Party transition matrix](notebook_analysis/charts/04_party_transition_matrix.png)"),
        md("![First round to runoff matrix](notebook_analysis/charts/05_first_round_to_runoff_matrix.png)"),
        md("## 3. Population Probability Weights Through Ticks\n\nThese lines show mean probability mass across all 300 agents."),
        md("![Aggregate candidate timeline](notebook_analysis/charts/06_aggregate_candidate_probability_timeline.png)"),
        md("![Aggregate party timeline](notebook_analysis/charts/07_aggregate_party_probability_timeline.png)"),
        md("## 4. Persona-Level Probability Shifts\n\nFinal-minus-initial movement in percentage points for each persona cohort."),
        md("![Candidate shift heatmap](notebook_analysis/charts/08_persona_candidate_probability_shift_heatmap.png)"),
        md("![Party shift heatmap](notebook_analysis/charts/09_persona_party_probability_shift_heatmap.png)"),
        md("## 5. Full Persona Trajectories\n\nSmall multiples answer the missing thesis question directly for each persona cohort."),
        md("![Candidate persona small multiples](notebook_analysis/charts/10_persona_candidate_probability_small_multiples.png)"),
        md("![Party persona small multiples](notebook_analysis/charts/11_persona_party_probability_small_multiples.png)"),
        md("""## 6. Appendix Tables

Generated CSV tables:

- `persona_candidate_probabilities_by_tick.csv`
- `persona_party_probabilities_by_tick.csv`
- `persona_probability_shifts.csv`
- `candidate_transition_2018_to_2023.csv`
- `party_transition_2018_to_2023.csv`
- `persona_vote_summary.csv`"""),
        code("""pd.read_csv(TABLES / "persona_vote_summary.csv")"""),
        code("""pd.read_csv(TABLES / "candidate_transition_2018_to_2023.csv").head(20)"""),
        code("""pd.read_csv(TABLES / "party_transition_2018_to_2023.csv").head(20)"""),
        md("""## 7. Regenerate Everything

```bash
python3 scripts/build_deep_analysis_notebook.py
```"""),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    style()

    soul_data = souls()
    df = pd.read_csv(TRAJECTORIES)
    df["baseline_presidential_2018"] = df["agent_id"].map(
        {agent: baseline(soul, "presidential_vote_2018") for agent, soul in soul_data.items()}
    )
    df["baseline_party_2018"] = df["agent_id"].map(
        {agent: baseline(soul, "party_2018_internal_key") for agent, soul in soul_data.items()}
    )
    ticks = list(OrderedDict.fromkeys(df["tick_id"].tolist()))
    first_round = df[df["tick_id"].eq(FIRST_ROUND_TICK)]
    runoff = df[df["tick_id"].eq(RUNOFF_TICK)]
    final_agents = first_round[
        ["agent_id", "archetype_name", "baseline_presidential_2018", "first_round_top"]
    ].merge(
        runoff[["agent_id", "baseline_party_2018", "party_top", "runoff_top"]],
        on="agent_id",
        how="inner",
    )

    candidate2018 = Counter(final_agents["baseline_presidential_2018"])
    candidate2023 = Counter(final_agents["first_round_top"])
    party2018 = Counter(final_agents["baseline_party_2018"])
    party2023 = Counter(final_agents["party_top"])

    candidate_keys = list(OrderedDict.fromkeys([*candidate2018.keys(), *CANDIDATES]))
    count_chart(candidate2018, candidate2023, candidate_keys, "Presidential top-choice counts: 2018 baseline vs 2023 simulated first round", CHARTS / "01_candidate_counts_2018_vs_2023.png")
    count_chart(party2018, party2023, PARTIES, "Party top-choice counts: 2018 baseline vs 2023 simulated preference", CHARTS / "02_party_counts_2018_vs_2023.png")

    candidate_transitions = final_agents.groupby(["baseline_presidential_2018", "first_round_top"]).size().reset_index(name="agents").sort_values("agents", ascending=False)
    party_transitions = final_agents.groupby(["baseline_party_2018", "party_top"]).size().reset_index(name="agents").sort_values("agents", ascending=False)
    runoff_transitions = final_agents.groupby(["first_round_top", "runoff_top"]).size().reset_index(name="agents").sort_values("agents", ascending=False)
    heatmap(candidate_transitions, "baseline_presidential_2018", "first_round_top", "Presidential vote transition matrix: 2018 baseline to 2023 first round", CHARTS / "03_candidate_transition_matrix.png")
    heatmap(party_transitions, "baseline_party_2018", "party_top", "Party vote transition matrix: 2018 baseline to 2023 simulated preference", CHARTS / "04_party_transition_matrix.png")
    heatmap(runoff_transitions, "first_round_top", "runoff_top", "2023 first round top choice to runoff top choice", CHARTS / "05_first_round_to_runoff_matrix.png")

    agg_candidate = df.groupby(["tick_id", "sim_date"], sort=False)[[f"first_round_{k}" for k in CANDIDATES]].mean().reset_index()
    agg_candidate[CANDIDATES] = agg_candidate[[f"first_round_{k}" for k in CANDIDATES]] * 100
    agg_candidate = agg_candidate.drop(columns=[f"first_round_{k}" for k in CANDIDATES])
    agg_party = df.groupby(["tick_id", "sim_date"], sort=False)[[f"party_{k}" for k in PARTIES]].mean().reset_index()
    agg_party[PARTIES] = agg_party[[f"party_{k}" for k in PARTIES]] * 100
    agg_party = agg_party.drop(columns=[f"party_{k}" for k in PARTIES])
    probability_lines(agg_candidate, CANDIDATES, "Population candidate probability weights across ticks", CHARTS / "06_aggregate_candidate_probability_timeline.png", 60)
    probability_lines(agg_party, PARTIES, "Population party probability weights across ticks", CHARTS / "07_aggregate_party_probability_timeline.png", 50)

    persona_candidate = df.groupby(["archetype_name", "tick_id", "sim_date"], sort=False)[[f"first_round_{k}" for k in CANDIDATES]].mean().reset_index()
    persona_candidate[CANDIDATES] = persona_candidate[[f"first_round_{k}" for k in CANDIDATES]] * 100
    persona_candidate = persona_candidate.drop(columns=[f"first_round_{k}" for k in CANDIDATES])
    persona_party = df.groupby(["archetype_name", "tick_id", "sim_date"], sort=False)[[f"party_{k}" for k in PARTIES]].mean().reset_index()
    persona_party[PARTIES] = persona_party[[f"party_{k}" for k in PARTIES]] * 100
    persona_party = persona_party.drop(columns=[f"party_{k}" for k in PARTIES])

    first_candidate = persona_candidate[persona_candidate["tick_id"].eq(FIRST_TICK)].set_index("archetype_name")[CANDIDATES]
    final_candidate = persona_candidate[persona_candidate["tick_id"].eq(FIRST_ROUND_TICK)].set_index("archetype_name")[CANDIDATES]
    candidate_shift = (final_candidate - first_candidate).reset_index()
    first_party = persona_party[persona_party["tick_id"].eq(FIRST_TICK)].set_index("archetype_name")[PARTIES]
    final_party = persona_party[persona_party["tick_id"].eq(RUNOFF_TICK)].set_index("archetype_name")[PARTIES]
    party_shift = (final_party - first_party).reset_index()
    shift_heatmap(candidate_shift, CANDIDATES, "Persona candidate probability shifts: T001 to first-round decision", CHARTS / "08_persona_candidate_probability_shift_heatmap.png")
    shift_heatmap(party_shift, PARTIES, "Persona party probability shifts: T001 to runoff decision", CHARTS / "09_persona_party_probability_shift_heatmap.png")
    small_multiples(persona_candidate, ["Erdogan", "Kilicdaroglu", "Muharrem_Ince", "Sinan_Ogan"], "Candidate probability trajectories by persona cohort", CHARTS / "10_persona_candidate_probability_small_multiples.png")
    small_multiples(persona_party, ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP"], "Party probability trajectories by persona cohort", CHARTS / "11_persona_party_probability_small_multiples.png")

    summary_rows = []
    for persona, cohort in final_agents.groupby("archetype_name"):
        c18, c23 = Counter(cohort["baseline_presidential_2018"]), Counter(cohort["first_round_top"])
        p18, p23 = Counter(cohort["baseline_party_2018"]), Counter(cohort["party_top"])
        row = {
            "persona": persona,
            "agents": len(cohort),
            "presidential_2018_top": c18.most_common(1)[0][0],
            "presidential_2018_agents": c18.most_common(1)[0][1],
            "presidential_2023_top": c23.most_common(1)[0][0],
            "presidential_2023_agents": c23.most_common(1)[0][1],
            "party_2018_top": p18.most_common(1)[0][0],
            "party_2018_agents": p18.most_common(1)[0][1],
            "party_2023_top": p23.most_common(1)[0][0],
            "party_2023_agents": p23.most_common(1)[0][1],
        }
        for key in ["Erdogan", "Kilicdaroglu", "Muharrem_Ince", "Sinan_Ogan"]:
            row[f"{key}_candidate_pp_shift"] = round(float(candidate_shift.loc[candidate_shift["archetype_name"].eq(persona), key].iloc[0]), 2)
        for key in ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP"]:
            row[f"{key}_party_pp_shift"] = round(float(party_shift.loc[party_shift["archetype_name"].eq(persona), key].iloc[0]), 2)
        summary_rows.append(row)
    persona_summary = pd.DataFrame(summary_rows).sort_values(["agents", "persona"], ascending=[False, True])

    agg_candidate.to_csv(TABLES / "aggregate_candidate_probabilities_by_tick.csv", index=False)
    agg_party.to_csv(TABLES / "aggregate_party_probabilities_by_tick.csv", index=False)
    persona_candidate.to_csv(TABLES / "persona_candidate_probabilities_by_tick.csv", index=False)
    persona_party.to_csv(TABLES / "persona_party_probabilities_by_tick.csv", index=False)
    candidate_shift.merge(party_shift, on="archetype_name", suffixes=("_candidate_pp", "_party_pp")).to_csv(TABLES / "persona_probability_shifts.csv", index=False)
    candidate_transitions.to_csv(TABLES / "candidate_transition_2018_to_2023.csv", index=False)
    party_transitions.to_csv(TABLES / "party_transition_2018_to_2023.csv", index=False)
    runoff_transitions.to_csv(TABLES / "runoff_transition_2023.csv", index=False)
    persona_summary.to_csv(TABLES / "persona_vote_summary.csv", index=False)

    summary = {
        "agents": int(df["agent_id"].nunique()),
        "ticks": len(ticks),
        "first_round_date": str(first_round["sim_date"].iloc[0]),
        "runoff_date": str(runoff["sim_date"].iloc[0]),
        "candidate2018": dict(candidate2018),
        "candidate2023": dict(candidate2023),
        "party2018": dict(party2018),
        "party2023": dict(party2023),
    }
    (OUT / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    NOTEBOOK.write_text(json.dumps(notebook(summary), ensure_ascii=False, indent=2), encoding="utf-8")
    print(NOTEBOOK)
    print(OUT)


if __name__ == "__main__":
    main()
