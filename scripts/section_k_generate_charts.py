"""Section K — generate publication-quality charts from the canonical run.

Reads only outputs/agent_trajectories.csv and souls/.
Writes outputs/audit_charts/<name>.svg and .png for each figure.
No API calls. Free to re-run.
"""

import ast
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "outputs" / "agent_trajectories.csv"
SOULS_DIR = ROOT / "souls"
OUT = ROOT / "outputs" / "audit_charts"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Style ----------
# Springer style: no in-figure titles or captions; all text within 8-12 pt.
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "legend.title_fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# Common font sizes used by individual chart helpers (all within 8-12 pt).
FS_VALUE = 8        # numeric value labels above/inside bars
FS_TICK = 9         # tick labels
FS_LEGEND = 9       # legend entries
FS_AXIS = 10        # axis labels

COLORS = {
    "Erdogan": "#B22222",
    "Kilicdaroglu": "#1f77b4",
    "Sinan_Ogan": "#2ca02c",
    "Muharrem_Ince": "#ff7f0e",
    "Other": "#c7c7c7",
    "Undecided": "#7f7f7f",
    "Abstain_Invalid_Undecided": "#7f7f7f",
    "sim_mean": "#4c72b0",
    "sim_mode": "#c44e52",
    "actual": "#222222",
}

LABELS = {
    "Erdogan": "Erdoğan",
    "Kilicdaroglu": "Kılıçdaroğlu",
    "Sinan_Ogan": "S. Oğan",
    "Muharrem_Ince": "M. İnce",
    "Other": "Other",
    "Undecided": "Undecided",
    "Abstain_Invalid_Undecided": "Abstain/Undec.",
}

ACTUAL_FIRST = {"Erdogan": 49.52, "Kilicdaroglu": 44.88, "Sinan_Ogan": 5.17, "Muharrem_Ince": 0.43}
ACTUAL_RUNOFF = {"Erdogan": 52.18, "Kilicdaroglu": 47.82}
DECISION_FIRST = "T030A_first_round_vote_decision"
DECISION_RUNOFF = "T035A_runoff_vote_decision"

# Event annotations on trajectories — used for caption-style legends only.
EVENT_NOTES = [
    ("T002", "Lira crisis"),
    ("T005", "Istanbul rerun"),
    ("T007", "COVID"),
    ("T009", "HDP closure"),
    ("T010", "Lira free-fall"),
    ("T012", "80% inflation"),
    ("T013", "Imamoglu sentenced"),
    ("T016", "Earthquake"),
    ("T023", "Aksener leaves"),
    ("T029", "Ince withdraws"),
    ("T030A_first_round_vote_decision", "First round"),
    ("T035A_runoff_vote_decision", "Runoff"),
]

# Event clusters drawn as subtle vertical bands on trajectory charts.
EVENT_BANDS = [
    (["T002"], "#fdd0a2", "Lira crisis 2018"),
    (["T004", "T005"], "#cbe0ed", "Istanbul mayoral"),
    (["T010", "T011", "T012"], "#fdc08a", "Lira / 80% inflation"),
    (["T016", "T017", "T018", "T019", "T020", "T021", "T022"], "#f5b7b1", "Earthquake & response"),
    (["T030A_first_round_vote_decision", "T030B_first_round_result_revealed"], "#b8e6b8", "First round"),
    (["T035A_runoff_vote_decision", "T035B_final_result_revealed"], "#b8e6b8", "Runoff"),
]


def short_tick(t):
    """Compact tick label: T001-T029 verbatim; decision/reveal ticks lose the long suffix."""
    return t.split("_")[0] if "_" in t else t


def set_tick_axis(ax, tick_order, fontsize=FS_TICK, rotation=55):
    """Apply readable tick labels at the bottom: all 37 ticks shown, no truncation issues."""
    x = np.arange(len(tick_order))
    ax.set_xticks(x)
    ax.set_xticklabels([short_tick(t) for t in tick_order], rotation=rotation, ha="right",
                       fontsize=fontsize, rotation_mode="anchor")
    ax.tick_params(axis="x", which="major", pad=2)


def draw_event_bands(ax, tick_order, alpha=0.45):
    """Draw subtle background bands marking the major event clusters."""
    legend_handles = []
    for tick_ids, color, label in EVENT_BANDS:
        indices = [tick_order.index(t) for t in tick_ids if t in tick_order]
        if not indices:
            continue
        ax.axvspan(min(indices) - 0.45, max(indices) + 0.45,
                   facecolor=color, alpha=alpha, edgecolor="none", zorder=0)
        legend_handles.append(Patch(facecolor=color, alpha=alpha, edgecolor="none", label=label))
    return legend_handles


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print(f"saved  {name}")


def load_panel():
    return pd.read_csv(CSV)


def load_souls():
    rows = []
    for f in sorted(SOULS_DIR.glob("agent_*.json")):
        s = json.loads(f.read_text())
        rows.append({
            "agent_id": s["identity"]["agent_id"],
            "city": s["identity"].get("city", "?"),
            "region": s["identity"].get("region", "?"),
            "education": s["identity"].get("education_level", "?"),
            "income": s["identity"].get("income_bracket", "?"),
            "age": s["identity"].get("age", -1),
            "gender": s["identity"].get("gender", "?"),
        })
    return pd.DataFrame(rows)


def grouped_bar(ax, groups, series_dict, colors, ylabel, ymax=None):
    n_groups = len(groups)
    n_series = len(series_dict)
    width = 0.78 / n_series
    x = np.arange(n_groups)
    for i, (name, vals) in enumerate(series_dict.items()):
        bars = ax.bar(x + i * width - (n_series - 1) * width / 2, vals,
                      width=width, color=colors[name], label=name, edgecolor="white", linewidth=0.6)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + (ymax or max(vals) * 1.05) * 0.012,
                    f"{v:.1f}", ha="center", va="bottom", fontsize=FS_VALUE, color="#333")
    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=FS_TICK)
    ax.set_ylabel(ylabel, fontsize=FS_AXIS)
    if ymax:
        ax.set_ylim(0, ymax)
    ax.legend(loc="upper right", fontsize=FS_LEGEND)


# ============================================================
# K.1 Mode-vote vs mean-probability vs actual — the centerpiece
# ============================================================

def chart_k1_winner_comparison(df):
    fr = df[df["tick_id"] == DECISION_FIRST]
    ro = df[df["tick_id"] == DECISION_RUNOFF]
    fr_cols = ["first_round_Erdogan", "first_round_Kilicdaroglu", "first_round_Sinan_Ogan",
               "first_round_Muharrem_Ince", "first_round_Other", "first_round_Undecided"]
    ro_cols = ["runoff_Erdogan", "runoff_Kilicdaroglu", "runoff_Abstain_Invalid_Undecided"]

    fr_meanp = (fr[fr_cols].mean() * 100).to_dict()
    fr_meanp = {k.replace("first_round_", ""): v for k, v in fr_meanp.items()}
    fr_mode_counts = Counter(fr["first_round_top"])
    fr_mode = {k: 100 * fr_mode_counts[k] / len(fr) for k in fr_meanp}

    ro_meanp = (ro[ro_cols].mean() * 100).to_dict()
    ro_meanp = {k.replace("runoff_", ""): v for k, v in ro_meanp.items()}
    ro_mode_counts = Counter(ro["runoff_top"])
    ro_mode = {k: 100 * ro_mode_counts[k] / len(ro) for k in ro_meanp}

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    # First round
    cats = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince"]
    labels = [LABELS[c] for c in cats]
    actual = [ACTUAL_FIRST[c] for c in cats]
    mp = [fr_meanp.get(c, 0) for c in cats]
    mv = [fr_mode.get(c, 0) for c in cats]
    grouped_bar(axes[0], labels,
                {"Actual": actual, "Sim. mean-prob.": mp, "Sim. mode-vote": mv},
                {"Actual": COLORS["actual"], "Sim. mean-prob.": COLORS["sim_mean"], "Sim. mode-vote": COLORS["sim_mode"]},
                "First-round vote share (%)", ymax=70)
    # Runoff
    cats2 = ["Erdogan", "Kilicdaroglu"]
    labels2 = [LABELS[c] for c in cats2]
    actual2 = [ACTUAL_RUNOFF[c] for c in cats2]
    mp2 = [ro_meanp.get(c, 0) for c in cats2]
    mv2 = [ro_mode.get(c, 0) for c in cats2]
    grouped_bar(axes[1], labels2,
                {"Actual": actual2, "Sim. mean-prob.": mp2, "Sim. mode-vote": mv2},
                {"Actual": COLORS["actual"], "Sim. mean-prob.": COLORS["sim_mean"], "Sim. mode-vote": COLORS["sim_mode"]},
                "Runoff vote share (%)", ymax=70)
    save(fig, "k1_winner_comparison")


# ============================================================
# K.2 First-round and K.3 Runoff bar charts (cleaner single-panel)
# ============================================================

def chart_k2_first_round_bars(df):
    fr = df[df["tick_id"] == DECISION_FIRST]
    cols = ["first_round_Erdogan", "first_round_Kilicdaroglu", "first_round_Sinan_Ogan",
            "first_round_Muharrem_Ince", "first_round_Other", "first_round_Undecided"]
    sim = (fr[cols].mean() * 100)
    labels = [LABELS[c.replace("first_round_", "")] for c in cols]
    actual = [ACTUAL_FIRST.get(c.replace("first_round_", ""), 0) for c in cols]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(labels))
    w = 0.38
    b1 = ax.bar(x - w/2, actual, w, label="Actual (YSK)", color=COLORS["actual"], edgecolor="white", linewidth=0.6)
    b2 = ax.bar(x + w/2, sim, w, label="Simulated (mean-prob.)", color=COLORS["sim_mean"], edgecolor="white", linewidth=0.6)
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            if v < 0.1:
                continue
            ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}", ha="center", va="bottom", fontsize=FS_VALUE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FS_TICK)
    ax.set_ylabel("First-round vote share (%)", fontsize=FS_AXIS)
    ax.set_ylim(0, max(max(actual), max(sim)) * 1.18)
    ax.legend(loc="upper right", fontsize=FS_LEGEND)
    save(fig, "k2_first_round_bars")


def chart_k3_runoff_bars(df):
    ro = df[df["tick_id"] == DECISION_RUNOFF]
    cols = ["runoff_Erdogan", "runoff_Kilicdaroglu", "runoff_Abstain_Invalid_Undecided"]
    sim = (ro[cols].mean() * 100)
    labels = [LABELS[c.replace("runoff_", "")] for c in cols]
    actual_map = dict(ACTUAL_RUNOFF)
    actual_map["Abstain_Invalid_Undecided"] = 0
    actual = [actual_map.get(c.replace("runoff_", ""), 0) for c in cols]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    x = np.arange(len(labels))
    w = 0.38
    b1 = ax.bar(x - w/2, actual, w, label="Actual (YSK)", color=COLORS["actual"], edgecolor="white", linewidth=0.6)
    b2 = ax.bar(x + w/2, sim, w, label="Simulated (mean-prob.)", color=COLORS["sim_mean"], edgecolor="white", linewidth=0.6)
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            if v < 0.1:
                continue
            ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:.1f}", ha="center", va="bottom", fontsize=FS_VALUE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FS_TICK)
    ax.set_ylabel("Runoff vote share (%)", fontsize=FS_AXIS)
    ax.set_ylim(0, 60)
    ax.legend(loc="upper right", fontsize=FS_LEGEND)
    save(fig, "k3_runoff_bars")


# ============================================================
# K.4 Per-archetype first-round vote breakdown
# ============================================================

def chart_k4_archetype_breakdown(df):
    fr = df[df["tick_id"] == DECISION_FIRST]
    # order archetypes by population size
    archs = fr["archetype_name"].value_counts()
    arch_names = archs.index.tolist()
    # count first-round_top per archetype
    rows = []
    for a in arch_names:
        sub = fr[fr["archetype_name"] == a]
        counts = Counter(sub["first_round_top"])
        n = len(sub)
        rows.append({
            "archetype": a, "N": n,
            "Erdogan": counts.get("Erdogan", 0) / n * 100,
            "Kilicdaroglu": counts.get("Kilicdaroglu", 0) / n * 100,
            "Sinan_Ogan": counts.get("Sinan_Ogan", 0) / n * 100,
            "Other": (counts.get("Other", 0) + counts.get("Undecided", 0) + counts.get("Muharrem_Ince", 0)) / n * 100,
        })
    d = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(11, 6))
    y = np.arange(len(d))
    left = np.zeros(len(d))
    for c in ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Other"]:
        vals = d[c].values
        ax.barh(y, vals, left=left, height=0.62, color=COLORS.get(c, "#aaa"),
                edgecolor="white", linewidth=0.5, label=LABELS.get(c, c))
        for i, v in enumerate(vals):
            if v >= 7:
                ax.text(left[i] + v / 2, y[i], f"{int(round(v))}%", ha="center", va="center",
                        color="white", fontsize=9, fontweight="bold")
        left += vals
    ax.set_yticks(y)
    ax.set_yticklabels([f"{a}  (N={n})" for a, n in zip(d["archetype"], d["N"])], fontsize=FS_TICK)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of archetype voting for candidate (%)", fontsize=FS_AXIS)
    ax.legend(loc="lower right", ncol=4, fontsize=FS_LEGEND, bbox_to_anchor=(1, -0.18))
    save(fig, "k4_archetype_breakdown")


# ============================================================
# K.5 Contribution decomposition — where the simulated 41.5% / 49.1% comes from
# ============================================================

def chart_k5_contribution(df):
    fr = df[df["tick_id"] == DECISION_FIRST]
    archs = fr["archetype_name"].value_counts()
    arch_order = archs.index.tolist()
    weights = (archs / archs.sum()).to_dict()
    contrib = []
    for a in arch_order:
        sub = fr[fr["archetype_name"] == a]
        for c in ["Erdogan", "Kilicdaroglu", "Sinan_Ogan"]:
            contrib.append({
                "archetype": a,
                "candidate": c,
                "contrib_pp": float(sub[f"first_round_{c}"].mean()) * 100 * weights[a],
            })
    cd = pd.DataFrame(contrib)
    # Pivot for stacked bar
    piv = cd.pivot(index="archetype", columns="candidate", values="contrib_pp").loc[arch_order]
    fig, ax = plt.subplots(figsize=(11, 6))
    y = np.arange(len(piv))
    bottom = np.zeros(len(piv))
    for c in ["Erdogan", "Kilicdaroglu", "Sinan_Ogan"]:
        v = piv[c].values
        ax.barh(y, v, left=bottom, height=0.6, color=COLORS[c], edgecolor="white", linewidth=0.6,
                label=LABELS[c])
        for i, val in enumerate(v):
            if val >= 0.8:
                ax.text(bottom[i] + val / 2, y[i], f"{val:.1f}", ha="center", va="center",
                        color="white", fontsize=8.5, fontweight="bold")
        bottom += v
    ax.set_yticks(y)
    ax.set_yticklabels(piv.index, fontsize=FS_TICK)
    ax.invert_yaxis()
    ax.set_xlabel("Contribution to simulated first-round vote share (percentage points)", fontsize=FS_AXIS)
    ax.legend(loc="lower right", fontsize=FS_LEGEND)
    save(fig, "k5_contribution_decomposition")


# ============================================================
# K.6 Within-archetype dispersion (the homogenization figure)
# ============================================================

def chart_k6_dispersion(df):
    fr = df[df["tick_id"] == DECISION_FIRST]
    arch_order = fr["archetype_name"].value_counts().index.tolist()
    fig, ax = plt.subplots(figsize=(11, 6.2))
    data_erd = []
    data_kil = []
    labels_ = []
    for a in arch_order:
        sub = fr[fr["archetype_name"] == a]
        data_erd.append(sub["first_round_Erdogan"].values * 100)
        data_kil.append(sub["first_round_Kilicdaroglu"].values * 100)
        labels_.append(f"{a}\n(N={len(sub)})")
    y = np.arange(len(arch_order)) * 1.3
    for i, (e, k) in enumerate(zip(data_erd, data_kil)):
        # scatter dots
        ax.scatter(e, np.full_like(e, y[i] - 0.22) + np.random.uniform(-0.07, 0.07, size=len(e)),
                   color=COLORS["Erdogan"], s=18, alpha=0.45, edgecolor="none")
        ax.scatter(k, np.full_like(k, y[i] + 0.22) + np.random.uniform(-0.07, 0.07, size=len(k)),
                   color=COLORS["Kilicdaroglu"], s=18, alpha=0.45, edgecolor="none")
        # mean markers
        ax.plot([np.mean(e)], [y[i] - 0.22], marker="D", color=COLORS["Erdogan"],
                markersize=9, markeredgecolor="white", markeredgewidth=1.2)
        ax.plot([np.mean(k)], [y[i] + 0.22], marker="D", color=COLORS["Kilicdaroglu"],
                markersize=9, markeredgecolor="white", markeredgewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels_, fontsize=FS_TICK)
    ax.invert_yaxis()
    ax.set_xlim(-3, 103)
    ax.set_xlabel("Probability assigned to candidate at T030A (%)", fontsize=FS_AXIS)
    handles = [
        Patch(color=COLORS["Erdogan"], label=LABELS["Erdogan"] + "  (each dot = one agent)"),
        Patch(color=COLORS["Kilicdaroglu"], label=LABELS["Kilicdaroglu"] + "  (each dot = one agent)"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=FS_LEGEND)
    save(fig, "k6_within_archetype_dispersion")


# ============================================================
# K.7 Emotion trajectories
# ============================================================

def chart_k7_emotion_trajectories(df):
    tick_order = df["tick_id"].drop_duplicates().tolist()
    means = df.groupby("tick_id")[["anger", "fear", "hope", "sadness", "political_fatigue"]].mean().reindex(tick_order)
    fig, ax = plt.subplots(figsize=(14, 6.2))
    x = np.arange(len(tick_order))
    palette = {"anger": "#c44e52", "fear": "#8172b3", "hope": "#55a868",
               "sadness": "#4c72b0", "political_fatigue": "#dd8452"}
    band_handles = draw_event_bands(ax, tick_order)
    for col in means.columns:
        ax.plot(x, means[col], label=col.replace("_", " "), linewidth=2, color=palette[col], zorder=3)
    set_tick_axis(ax, tick_order)
    ax.set_xlim(-0.5, len(tick_order) - 0.5)
    ax.set_ylim(0.4, 1.0)
    ax.set_ylabel("Mean emotion score (0–1, averaged over 300 agents)", fontsize=FS_AXIS)
    ax.set_xlabel("Simulation tick", fontsize=FS_AXIS)
    line_leg = ax.legend(loc="upper left", ncol=5, fontsize=FS_LEGEND)
    ax.add_artist(line_leg)
    if band_handles:
        ax.legend(handles=band_handles, loc="lower left", ncol=3, fontsize=FS_LEGEND,
                  title="Event clusters", title_fontsize=FS_LEGEND)
    save(fig, "k7_emotion_trajectories")


# ============================================================
# K.8 Approval / trust trajectories
# ============================================================

def chart_k8_approval_trust(df):
    tick_order = df["tick_id"].drop_duplicates().tolist()
    means = df.groupby("tick_id")[["government_approval", "institutional_trust", "opposition_trust"]].mean().reindex(tick_order)
    fig, ax = plt.subplots(figsize=(14, 6.2))
    x = np.arange(len(tick_order))
    palette = {
        "government_approval": "#B22222",
        "institutional_trust": "#7f7f7f",
        "opposition_trust": "#1f77b4",
    }
    band_handles = draw_event_bands(ax, tick_order)
    for col in means.columns:
        ax.plot(x, means[col], label=col.replace("_", " "), linewidth=2.2, color=palette[col], zorder=3)
    set_tick_axis(ax, tick_order)
    ax.set_xlim(-0.5, len(tick_order) - 0.5)
    ax.set_ylim(3.5, 5.0)
    ax.set_ylabel("Mean score (1–10, averaged over 300 agents)", fontsize=FS_AXIS)
    ax.set_xlabel("Simulation tick", fontsize=FS_AXIS)
    line_leg = ax.legend(loc="upper right", fontsize=FS_LEGEND)
    ax.add_artist(line_leg)
    if band_handles:
        ax.legend(handles=band_handles, loc="lower left", ncol=3, fontsize=FS_LEGEND,
                  title="Event clusters", title_fontsize=FS_LEGEND)
    save(fig, "k8_approval_trust")


# ============================================================
# K.9 Demographics 4-panel
# ============================================================

def chart_k9_demographics(df, souls):
    fr = df[df["tick_id"] == DECISION_FIRST]
    j = fr.merge(souls, on="agent_id", how="left")
    j["age_bracket"] = pd.cut(j["age"], bins=[0, 30, 45, 60, 100], labels=["≤30", "31-45", "46-60", "60+"])

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    def panel(ax, key, group_label, order=None, max_cats=10):
        sub = j.groupby([key, "first_round_top"], observed=True).size().unstack(fill_value=0)
        sub["N"] = sub.sum(axis=1)
        sub = sub.sort_values("N", ascending=False)
        if order is not None:
            sub = sub.reindex(order)
        sub = sub.head(max_cats)
        cats = sub.index.astype(str).tolist()
        e = sub.get("Erdogan", pd.Series(0, index=sub.index)).values / sub["N"].values * 100
        k = sub.get("Kilicdaroglu", pd.Series(0, index=sub.index)).values / sub["N"].values * 100
        y = np.arange(len(cats))
        ax.barh(y, e, height=0.7, color=COLORS["Erdogan"], edgecolor="white", linewidth=0.6, label=LABELS["Erdogan"])
        ax.barh(y, k, height=0.7, left=e, color=COLORS["Kilicdaroglu"], edgecolor="white", linewidth=0.6, label=LABELS["Kilicdaroglu"])
        for i, (ev, kv, nv) in enumerate(zip(e, k, sub["N"].values)):
            if ev >= 10:
                ax.text(ev / 2, y[i], f"{int(round(ev))}%", ha="center", va="center", color="white",
                        fontsize=FS_VALUE, fontweight="bold")
            if kv >= 10:
                ax.text(ev + kv / 2, y[i], f"{int(round(kv))}%", ha="center", va="center", color="white",
                        fontsize=FS_VALUE, fontweight="bold")
            ax.text(101, y[i], f"N={int(nv)}", ha="left", va="center", fontsize=FS_VALUE, color="#444")
        ax.set_yticks(y)
        ax.set_yticklabels(cats, fontsize=FS_TICK)
        ax.invert_yaxis()
        ax.set_xlim(0, 115)
        ax.set_xlabel(f"{group_label}: % voting candidate (mode-vote)", fontsize=FS_AXIS)

    panel(axes[0, 0], "region", "Region")
    edu_order = ["graduate", "university", "university_student", "vocational", "high_school", "primary"]
    panel(axes[0, 1], "education", "Education", order=[e for e in edu_order if e in j["education"].unique()])
    panel(axes[1, 0], "age_bracket", "Age bracket", order=["≤30", "31-45", "46-60", "60+"])
    panel(axes[1, 1], "city", "City (top 10 by N)", max_cats=10)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=FS_LEGEND, bbox_to_anchor=(0.5, -0.01))
    save(fig, "k9_demographics")


# ============================================================
# K.10 Transition matrix: T001 lean → T030A vote
# ============================================================

def chart_k10_transition(df):
    t001 = df[df["tick_id"] == "T001"][["agent_id", "first_round_top"]].rename(columns={"first_round_top": "t001"})
    t030a = df[df["tick_id"] == DECISION_FIRST][["agent_id", "first_round_top"]].rename(columns={"first_round_top": "t030a"})
    j = t001.merge(t030a, on="agent_id")
    mat = j.groupby(["t001", "t030a"]).size().unstack(fill_value=0)
    rows = [r for r in ["Erdogan", "Kilicdaroglu", "Muharrem_Ince", "Sinan_Ogan", "Other", "Undecided"] if r in mat.index]
    cols = [c for c in ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"] if c in mat.columns]
    mat = mat.loc[rows, cols]
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    im = ax.imshow(mat.values, cmap="Reds", aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([LABELS[c] for c in cols], rotation=30, ha="right", fontsize=FS_TICK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([LABELS[r] for r in rows], fontsize=FS_TICK)
    ax.set_xlabel("T030A first-round vote (mode)", fontsize=FS_AXIS)
    ax.set_ylabel("T001 first-round lean (mode)", fontsize=FS_AXIS)
    for i in range(len(rows)):
        for j_ in range(len(cols)):
            v = int(mat.values[i, j_])
            if v == 0:
                continue
            ax.text(j_, i, str(v), ha="center", va="center",
                    color=("white" if v > mat.values.max() / 2 else "black"), fontsize=10, fontweight="semibold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, label="Agent count")
    cbar.ax.yaxis.label.set_size(FS_AXIS)
    cbar.ax.tick_params(labelsize=FS_TICK)
    ax.grid(False)
    save(fig, "k10_transition_t001_to_t030a")


# ============================================================
# K.11 Schema-placeholder bug rate by tick
# ============================================================

def chart_k11_placeholder_bug(df):
    def has_short(s):
        try:
            return "short_code" in ast.literal_eval(s)
        except Exception:
            return False
    df = df.copy()
    df["_short"] = df["reason_codes"].apply(has_short)
    tick_order = df["tick_id"].drop_duplicates().tolist()
    rates = df.groupby("tick_id")["_short"].mean().reindex(tick_order) * 100
    fig, ax = plt.subplots(figsize=(14, 5.6))
    x = np.arange(len(rates))
    colors = ["#c44e52" if v > 50 else ("#dd8452" if v > 25 else "#9ec3df") for v in rates.values]
    ax.bar(x, rates.values, color=colors, edgecolor="white", linewidth=0.6)
    ax.axhline(rates.mean(), color="black", linewidth=1.2, linestyle="--", alpha=0.7,
               label=f"Overall mean = {rates.mean():.1f}%")
    # value labels on top of each bar
    for xi, v in zip(x, rates.values):
        if v > 1:
            ax.text(xi, v + 1.5, f"{v:.0f}", ha="center", va="bottom", fontsize=FS_VALUE, color="#333")
    set_tick_axis(ax, tick_order)
    ax.set_xlim(-0.5, len(tick_order) - 0.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of decisions with 'short_code' placeholder", fontsize=FS_AXIS)
    ax.set_xlabel("Simulation tick", fontsize=FS_AXIS)
    # legend includes color scale
    legend_patches = [
        Patch(color="#c44e52", label=">50%"),
        Patch(color="#dd8452", label="25-50%"),
        Patch(color="#9ec3df", label="<25%"),
    ]
    leg1 = ax.legend(handles=legend_patches, loc="upper left", fontsize=FS_LEGEND, title="Bug rate", title_fontsize=FS_LEGEND)
    ax.add_artist(leg1)
    ax.legend(loc="upper right", fontsize=FS_LEGEND)
    save(fig, "k11_placeholder_bug_rate")


# ============================================================
# K.12 Bootstrap 95% CI on headline numbers
# ============================================================

def chart_k12_bootstrap_ci(df):
    rng = np.random.default_rng(42)
    fr = df[df["tick_id"] == DECISION_FIRST]
    ro = df[df["tick_id"] == DECISION_RUNOFF]
    n_boot = 1000
    def boot(rows, col):
        vals = rows[col].values
        idx = rng.integers(0, len(vals), size=(n_boot, len(vals)))
        means = vals[idx].mean(axis=1) * 100
        return means.mean(), np.percentile(means, 2.5), np.percentile(means, 97.5)
    def boot_mode(rows, top_col, candidate):
        vals = (rows[top_col] == candidate).astype(int).values
        idx = rng.integers(0, len(vals), size=(n_boot, len(vals)))
        means = vals[idx].mean(axis=1) * 100
        return means.mean(), np.percentile(means, 2.5), np.percentile(means, 97.5)

    rows = []
    for cand in ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince"]:
        m_mp, lo_mp, hi_mp = boot(fr, f"first_round_{cand}")
        m_mv, lo_mv, hi_mv = boot_mode(fr, "first_round_top", cand)
        rows.append({"round": "First round", "cand": cand, "metric": "Mean-prob.",
                     "mean": m_mp, "lo": lo_mp, "hi": hi_mp,
                     "actual": ACTUAL_FIRST.get(cand, 0)})
        rows.append({"round": "First round", "cand": cand, "metric": "Mode-vote",
                     "mean": m_mv, "lo": lo_mv, "hi": hi_mv,
                     "actual": ACTUAL_FIRST.get(cand, 0)})
    for cand in ["Erdogan", "Kilicdaroglu"]:
        m_mp, lo_mp, hi_mp = boot(ro, f"runoff_{cand}")
        m_mv, lo_mv, hi_mv = boot_mode(ro, "runoff_top", cand)
        rows.append({"round": "Runoff", "cand": cand, "metric": "Mean-prob.",
                     "mean": m_mp, "lo": lo_mp, "hi": hi_mp,
                     "actual": ACTUAL_RUNOFF.get(cand, 0)})
        rows.append({"round": "Runoff", "cand": cand, "metric": "Mode-vote",
                     "mean": m_mv, "lo": lo_mv, "hi": hi_mv,
                     "actual": ACTUAL_RUNOFF.get(cand, 0)})
    d = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, round_name in zip(axes, ["First round", "Runoff"]):
        sub = d[d["round"] == round_name]
        cands = sub["cand"].drop_duplicates().tolist()
        x = np.arange(len(cands))
        w = 0.32
        for i, metric in enumerate(["Mean-prob.", "Mode-vote"]):
            ss = sub[sub["metric"] == metric].set_index("cand").loc[cands]
            color = COLORS["sim_mean"] if metric == "Mean-prob." else COLORS["sim_mode"]
            ax.errorbar(x + (i - 0.5) * w, ss["mean"], yerr=[ss["mean"] - ss["lo"], ss["hi"] - ss["mean"]],
                        fmt="o", color=color, label=metric, capsize=4, markersize=7, linewidth=1.6)
        # actual as horizontal mark
        ss = sub[sub["metric"] == "Mean-prob."].set_index("cand").loc[cands]
        ax.scatter(x, ss["actual"], marker="_", s=300, color=COLORS["actual"], linewidth=3, label="Actual (YSK)", zorder=5)
        ax.set_xticks(x)
        ax.set_xticklabels([LABELS[c] for c in cands], fontsize=FS_TICK)
        ax.set_ylabel(f"{round_name} vote share (%)", fontsize=FS_AXIS)
        ax.set_ylim(0, 70)
        ax.legend(loc="upper right", fontsize=FS_LEGEND)
    save(fig, "k12_bootstrap_ci")


# ============================================================
# K.13 Broadcast exposure
# ============================================================

def chart_k13_broadcast_exposure(df):
    per_tick = df.groupby("tick_id")["visible_broadcast_count"].mean()
    tick_order = df["tick_id"].drop_duplicates().tolist()
    per_tick = per_tick.reindex(tick_order)
    fig, ax = plt.subplots(figsize=(14, 5.4))
    x = np.arange(len(per_tick))
    colors = ["#4c72b0" if v > 0 else "#cccccc" for v in per_tick.values]
    ax.bar(x, per_tick.values, color=colors, edgecolor="white", linewidth=0.6)
    for xi, v in zip(x, per_tick.values):
        if v > 0:
            ax.text(xi, v + 0.08, f"{v:.1f}", ha="center", va="bottom", fontsize=FS_VALUE, color="#333")
    set_tick_axis(ax, tick_order)
    ax.set_xlim(-0.5, len(tick_order) - 0.5)
    ax.set_ylabel("Mean visible_broadcast_count (cap = 5)", fontsize=FS_AXIS)
    ax.set_xlabel("Simulation tick", fontsize=FS_AXIS)
    ax.set_ylim(0, 6)
    legend_patches = [
        Patch(color="#4c72b0", label="Tick has political broadcasts"),
        Patch(color="#cccccc", label="No broadcasts this tick"),
    ]
    ax.legend(handles=legend_patches, loc="upper left", fontsize=FS_LEGEND)
    save(fig, "k13_broadcast_exposure")


def main():
    df = load_panel()
    souls = load_souls()
    chart_k1_winner_comparison(df)
    chart_k2_first_round_bars(df)
    chart_k3_runoff_bars(df)
    chart_k4_archetype_breakdown(df)
    chart_k5_contribution(df)
    chart_k6_dispersion(df)
    chart_k7_emotion_trajectories(df)
    chart_k8_approval_trust(df)
    chart_k9_demographics(df, souls)
    chart_k10_transition(df)
    chart_k11_placeholder_bug(df)
    chart_k12_bootstrap_ci(df)
    chart_k13_broadcast_exposure(df)


if __name__ == "__main__":
    main()
