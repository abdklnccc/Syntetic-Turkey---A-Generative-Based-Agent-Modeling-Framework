"""Section D — fresh quantitative audit of the canonical 300-agent run.

Reads only raw simulation output. Does not rely on any pre-computed analysis
table or dashboard. Designed to be re-run by future readers.
"""

import ast
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "outputs" / "agent_trajectories.csv"
REFL = ROOT / "outputs" / "reflections.jsonl"
SOULS_DIR = ROOT / "souls"

# Actual 2023 results (YSK valid-vote shares). Kept inline so this audit is self-contained.
ACTUAL_FIRST = {
    "Erdogan": 49.52,
    "Kilicdaroglu": 44.88,
    "Sinan_Ogan": 5.17,
    "Muharrem_Ince": 0.43,
}
ACTUAL_RUNOFF = {"Erdogan": 52.18, "Kilicdaroglu": 47.82}

DECISION_TICK_FIRST = "T030A_first_round_vote_decision"
DECISION_TICK_RUNOFF = "T035A_runoff_vote_decision"


def banner(s):
    print("\n" + "=" * 78)
    print(s)
    print("=" * 78)


def load_panel():
    df = pd.read_csv(CSV)
    return df


def parse_codes(s):
    if pd.isna(s):
        return []
    try:
        return ast.literal_eval(s)
    except Exception:
        return [str(s)]


def section_1_panel_sanity(df):
    banner("D.1  PANEL STRUCTURE")
    print(f"Rows: {len(df):,}")
    print(f"Unique agents: {df['agent_id'].nunique()}")
    print(f"Unique ticks: {df['tick_id'].nunique()}")
    print(f"Unique archetypes: {df['archetype_name'].nunique()}")
    print(f"Date range: {df['sim_date'].min()} -> {df['sim_date'].max()}")
    counts = df.groupby("agent_id").size()
    print(f"Decisions per agent: min={counts.min()}, max={counts.max()}, mean={counts.mean():.1f}")
    arch_counts = df.drop_duplicates("agent_id").groupby("archetype_name").size().sort_values(ascending=False)
    print("\nAgents per archetype:")
    for name, n in arch_counts.items():
        print(f"  {name:42s} {n:4d}")
    expected = 300 * 37
    if len(df) != expected:
        print(f"\nWARNING: row count {len(df)} != expected {expected}")
    return arch_counts


def mean_prob_dist(rows, cols):
    """Mean of probability columns; renormalize to sum to 100 (in percentage points)."""
    means = rows[cols].mean()
    return {c.split("_", 2)[-1] if c.startswith("first_round_") or c.startswith("runoff_") else c.split("_", 1)[-1]: round(float(means[c]) * 100, 3) for c in cols}


def section_2_headline(df):
    banner("D.2  HEADLINE VOTE DISTRIBUTIONS — RECOMPUTED FROM RAW CSV")
    fr_cols = ["first_round_Erdogan", "first_round_Kilicdaroglu", "first_round_Sinan_Ogan",
               "first_round_Muharrem_Ince", "first_round_Other", "first_round_Undecided"]
    ro_cols = ["runoff_Erdogan", "runoff_Kilicdaroglu", "runoff_Abstain_Invalid_Undecided"]

    fr_rows = df[df["tick_id"] == DECISION_TICK_FIRST]
    ro_rows = df[df["tick_id"] == DECISION_TICK_RUNOFF]
    print(f"First-round decision tick rows: {len(fr_rows)}  (expect 300)")
    print(f"Runoff decision tick rows: {len(ro_rows)}  (expect 300)")

    # --- Mean-probability distribution
    print("\n[A] Mean-probability distribution at decision tick (each agent's prob averaged):")
    fr_mp = (fr_rows[fr_cols].mean() * 100).round(3)
    ro_mp = (ro_rows[ro_cols].mean() * 100).round(3)
    print("  First round:")
    for c in fr_cols:
        label = c.replace("first_round_", "")
        print(f"    {label:18s} {fr_mp[c]:7.3f} %")
    print(f"    SUM                {fr_mp.sum():7.3f}")
    print("  Runoff:")
    for c in ro_cols:
        label = c.replace("runoff_", "")
        print(f"    {label:30s} {ro_mp[c]:7.3f} %")
    print(f"    SUM                            {ro_mp.sum():7.3f}")

    # --- Mode-vote (count of first_round_top)
    print("\n[B] Mode-vote distribution (count of each agent's argmax):")
    fr_mode = fr_rows["first_round_top"].value_counts()
    ro_mode = ro_rows["runoff_top"].value_counts()
    print("  First round (count of first_round_top):")
    for k, n in fr_mode.items():
        print(f"    {k:18s} {n:4d}  ({100*n/len(fr_rows):.2f} %)")
    print("  Runoff (count of runoff_top):")
    for k, n in ro_mode.items():
        print(f"    {k:30s} {n:4d}  ({100*n/len(ro_rows):.2f} %)")

    return fr_rows, ro_rows, fr_mp, ro_mp, fr_mode, ro_mode


def section_3_mae(fr_mp, ro_mp):
    banner("D.3  ACCURACY — TWO WAYS OF SCORING")
    # [A] Absolute percentage-point gap (no renormalization)
    print("[A] Absolute-pp gap (sim minus actual, NOT renormalized):")
    print(f"  {'Candidate':18s} {'Sim':>8s} {'Actual':>8s} {'Gap':>8s}")
    for k, actual in ACTUAL_FIRST.items():
        sim_key = f"first_round_{k}"
        sim_pct = float(fr_mp[sim_key])
        print(f"  {k:18s} {sim_pct:8.3f} {actual:8.3f} {sim_pct-actual:+8.3f}")
    sim_und = float(fr_mp.get("first_round_Undecided", 0))
    sim_oth = float(fr_mp.get("first_round_Other", 0))
    print(f"  {'Undecided':18s} {sim_und:8.3f} {0.0:8.3f} {sim_und:+8.3f}")
    print(f"  {'Other':18s} {sim_oth:8.3f} {0.0:8.3f} {sim_oth:+8.3f}")
    print()
    print("[B] Renormalized 4-candidate MAE (matches metrics.py convention):")
    sim4 = {k: float(fr_mp[f"first_round_{k}"]) for k in ACTUAL_FIRST}
    sim4_total = sum(sim4.values())
    sim4_norm = {k: 100 * v / sim4_total for k, v in sim4.items()}
    actual4_total = sum(ACTUAL_FIRST.values())
    actual4_norm = {k: 100 * v / actual4_total for k, v in ACTUAL_FIRST.items()}
    mae_first = mean(abs(sim4_norm[k] - actual4_norm[k]) for k in ACTUAL_FIRST)
    print(f"  Renormalized MAE first round: {mae_first:.3f}")
    sim2 = {k: float(ro_mp[f"runoff_{k}"]) for k in ACTUAL_RUNOFF}
    sim2_total = sum(sim2.values())
    sim2_norm = {k: 100 * v / sim2_total for k, v in sim2.items()}
    actual2_total = sum(ACTUAL_RUNOFF.values())
    actual2_norm = {k: 100 * v / actual2_total for k, v in ACTUAL_RUNOFF.items()}
    mae_runoff = mean(abs(sim2_norm[k] - actual2_norm[k]) for k in ACTUAL_RUNOFF)
    print(f"  Renormalized MAE runoff:      {mae_runoff:.3f}")
    print()
    print("[C] Winner check:")
    sim_winner_first = max(sim4_norm, key=sim4_norm.get)
    actual_winner_first = max(actual4_norm, key=actual4_norm.get)
    sim_winner_runoff = max(sim2_norm, key=sim2_norm.get)
    actual_winner_runoff = max(actual2_norm, key=actual2_norm.get)
    print(f"  First-round winner: simulated={sim_winner_first}, actual={actual_winner_first}  ->  match: {sim_winner_first==actual_winner_first}")
    print(f"  Runoff      winner: simulated={sim_winner_runoff}, actual={actual_winner_runoff}  ->  match: {sim_winner_runoff==actual_winner_runoff}")


def section_4_archetype(df, fr_rows, ro_rows):
    banner("D.4  PER-ARCHETYPE VOTE BREAKDOWN")
    archs = fr_rows["archetype_name"].unique()
    print(f"{'Archetype':42s} {'N':>4s}  First-round counts                Runoff counts")
    print("-" * 130)
    rows_for_table = []
    for arch in sorted(archs, key=lambda a: -fr_rows[fr_rows["archetype_name"] == a]["agent_id"].nunique()):
        fr_a = fr_rows[fr_rows["archetype_name"] == arch]
        ro_a = ro_rows[ro_rows["archetype_name"] == arch]
        n = fr_a["agent_id"].nunique()
        fr_c = Counter(fr_a["first_round_top"])
        ro_c = Counter(ro_a["runoff_top"])
        fr_str = ", ".join(f"{k}:{v}" for k, v in fr_c.most_common())
        ro_str = ", ".join(f"{k}:{v}" for k, v in ro_c.most_common())
        print(f"{arch:42s} {n:4d}  {fr_str:40s}  {ro_str}")
        rows_for_table.append({"archetype": arch, "n": n, "first_round": dict(fr_c), "runoff": dict(ro_c)})
    return rows_for_table


def section_5_archetype_mean_probs(df, fr_rows, ro_rows):
    banner("D.5  PER-ARCHETYPE MEAN PROBABILITIES AT DECISION TICKS")
    fr_cols = ["first_round_Erdogan", "first_round_Kilicdaroglu", "first_round_Sinan_Ogan",
               "first_round_Other", "first_round_Undecided"]
    print(f"{'Archetype':42s}  {'Erd':>6s}  {'Kil':>6s}  {'Ogan':>6s}  {'Und':>6s}  {'Oth':>6s}")
    for arch in sorted(fr_rows["archetype_name"].unique()):
        a = fr_rows[fr_rows["archetype_name"] == arch]
        m = a[fr_cols].mean() * 100
        print(f"{arch:42s}  {m['first_round_Erdogan']:6.2f}  {m['first_round_Kilicdaroglu']:6.2f}  "
              f"{m['first_round_Sinan_Ogan']:6.2f}  {m['first_round_Undecided']:6.2f}  {m['first_round_Other']:6.2f}")


def section_6_demographics(df, fr_rows, ro_rows):
    banner("D.6  DEMOGRAPHIC BREAKDOWNS (joining souls files)")
    demo = []
    for f in sorted(SOULS_DIR.glob("agent_*.json")):
        s = json.loads(f.read_text())
        demo.append({
            "agent_id": s["identity"]["agent_id"],
            "city": s["identity"].get("city", "?"),
            "region": s["identity"].get("region", "?"),
            "education": s["identity"].get("education_level", "?"),
            "income": s["identity"].get("income_bracket", "?"),
            "age": s["identity"].get("age", -1),
            "gender": s["identity"].get("gender", "?"),
            "archetype_id": s["identity"].get("archetype_id", "?"),
        })
    demo_df = pd.DataFrame(demo)
    print(f"Loaded {len(demo_df)} souls. Cities: {demo_df['city'].nunique()}, "
          f"regions: {demo_df['region'].nunique()}, education levels: {demo_df['education'].nunique()}")

    fr_join = fr_rows.merge(demo_df, on="agent_id", how="left")

    # by region
    print("\nFirst-round vote by region:")
    by_region = fr_join.groupby(["region", "first_round_top"]).size().unstack(fill_value=0)
    by_region["N"] = by_region.sum(axis=1)
    by_region = by_region.sort_values("N", ascending=False)
    print(by_region.to_string())

    # by education
    print("\nFirst-round vote by education:")
    by_edu = fr_join.groupby(["education", "first_round_top"]).size().unstack(fill_value=0)
    by_edu["N"] = by_edu.sum(axis=1)
    by_edu = by_edu.sort_values("N", ascending=False)
    print(by_edu.to_string())

    # by income
    print("\nFirst-round vote by income:")
    by_inc = fr_join.groupby(["income", "first_round_top"]).size().unstack(fill_value=0)
    by_inc["N"] = by_inc.sum(axis=1)
    by_inc = by_inc.sort_values("N", ascending=False)
    print(by_inc.to_string())

    # by age bracket
    fr_join["age_bracket"] = pd.cut(fr_join["age"], bins=[0, 30, 45, 60, 100], labels=["<=30", "31-45", "46-60", "60+"])
    print("\nFirst-round vote by age bracket:")
    by_age = fr_join.groupby(["age_bracket", "first_round_top"], observed=True).size().unstack(fill_value=0)
    by_age["N"] = by_age.sum(axis=1)
    print(by_age.to_string())

    # top cities (each gets at least 5 agents)
    city_counts = demo_df["city"].value_counts()
    top_cities = city_counts[city_counts >= 5].index.tolist()
    print(f"\nFirst-round vote by city (cities with >=5 agents, n={len(top_cities)}):")
    by_city = fr_join[fr_join["city"].isin(top_cities)].groupby(["city", "first_round_top"]).size().unstack(fill_value=0)
    by_city["N"] = by_city.sum(axis=1)
    by_city = by_city.sort_values("N", ascending=False)
    print(by_city.to_string())

    return demo_df


def section_7_transitions(df, fr_rows, ro_rows):
    banner("D.7  TRANSITION MATRICES")
    # T001 (the 2018 election event) is the simulation's earliest measured first-round leaning.
    t001 = df[df["tick_id"] == "T001"]
    print(f"T001 rows: {len(t001)}")

    # Build a per-agent T001 first_round_top vs T030A first_round_top
    a1 = t001[["agent_id", "first_round_top"]].rename(columns={"first_round_top": "t001_first"})
    a2 = fr_rows[["agent_id", "first_round_top"]].rename(columns={"first_round_top": "t030a_first"})
    trans = a1.merge(a2, on="agent_id")
    print("\nT001 first-round lean  ->  T030A first-round vote (counts):")
    mat = trans.groupby(["t001_first", "t030a_first"]).size().unstack(fill_value=0)
    print(mat.to_string())

    a3 = ro_rows[["agent_id", "runoff_top"]].rename(columns={"runoff_top": "t035a_runoff"})
    trans2 = a2.merge(a3, on="agent_id")
    print("\nT030A first-round vote  ->  T035A runoff vote (counts):")
    mat2 = trans2.groupby(["t030a_first", "t035a_runoff"]).size().unstack(fill_value=0)
    print(mat2.to_string())


def section_8_trajectories(df):
    banner("D.8  TRAJECTORIES — emotion, approval, trust (mean over agents per tick)")
    # ensure tick order
    tick_order = df["tick_id"].drop_duplicates().tolist()
    cols = ["anger", "fear", "hope", "sadness", "political_fatigue",
            "government_approval", "institutional_trust", "opposition_trust"]
    means = df.groupby("tick_id")[cols].mean()
    stds = df.groupby("tick_id")[cols].std()
    # reindex by simulation tick order
    means = means.reindex(tick_order)
    stds = stds.reindex(tick_order)

    print("Tick-by-tick mean (10-tick stride for readability):")
    print(f"{'tick':10s} {'anger':>6s} {'fear':>6s} {'hope':>6s} {'sad':>6s} {'fatig':>6s} {'gov_app':>8s} {'inst':>6s} {'opp':>6s}")
    for i, t in enumerate(tick_order):
        if i % 3 != 0 and i not in (16, 17, 18, 19, 20, 21, 22, 29, 30, 35, 36):
            continue
        m = means.loc[t]
        print(f"{t[:10]:10s} {m['anger']:6.3f} {m['fear']:6.3f} {m['hope']:6.3f} {m['sadness']:6.3f} {m['political_fatigue']:6.3f} {m['government_approval']:8.3f} {m['institutional_trust']:6.3f} {m['opposition_trust']:6.3f}")

    # Largest tick-to-tick deltas in each emotion + approval
    print("\nLargest |tick-to-tick delta| in mean state:")
    deltas = means.diff().abs()
    for c in cols:
        top = deltas[c].nlargest(3)
        labels = []
        for tick_id in top.index:
            labels.append(f"{tick_id[:10]}({top.loc[tick_id]:.3f})")
        print(f"  {c:22s} -> {', '.join(labels)}")

    return means, stds


def section_9_within_archetype_dispersion(df, fr_rows):
    banner("D.9  WITHIN-ARCHETYPE DISPERSION (homogenization check)")
    print("For each archetype, std of first_round_Erdogan probability at T030A.")
    print("Low std = the LLM gives every agent in this archetype roughly the same probability (homogenized).")
    print(f"{'Archetype':42s}  {'N':>4s}  {'mean Erd':>10s}  {'std Erd':>9s}  {'mean Kil':>10s}  {'std Kil':>9s}")
    for arch in sorted(fr_rows["archetype_name"].unique()):
        a = fr_rows[fr_rows["archetype_name"] == arch]
        n = len(a)
        if n < 2:
            continue
        print(f"{arch:42s}  {n:4d}  {a['first_round_Erdogan'].mean()*100:10.3f}  {a['first_round_Erdogan'].std()*100:9.3f}  "
              f"{a['first_round_Kilicdaroglu'].mean()*100:10.3f}  {a['first_round_Kilicdaroglu'].std()*100:9.3f}")


def section_10_broadcast_exposure(df, fr_rows):
    banner("D.10  BROADCAST EXPOSURE")
    # Total visible_broadcast_count across ticks per agent
    per_tick = df.groupby("tick_id")["visible_broadcast_count"].agg(["mean", "max", "count"])
    print("Broadcast exposure by tick (mean, max visible_broadcast_count):")
    for t, row in per_tick.iterrows():
        if row["mean"] > 0 or t in ("T030A_first_round_vote_decision", "T035A_runoff_vote_decision"):
            print(f"  {t:36s} mean={row['mean']:5.2f}  max={int(row['max']):2d}  n_rows={int(row['count'])}")

    # Does broadcast exposure predict vote shift at the decision tick?
    # Aggregate total broadcast count per agent over all ticks
    total_bc = df.groupby("agent_id")["visible_broadcast_count"].sum().rename("total_broadcasts_seen")
    fr_join = fr_rows.merge(total_bc.reset_index(), on="agent_id")
    print(f"\nMean total_broadcasts_seen per agent: {fr_join['total_broadcasts_seen'].mean():.2f}  "
          f"(min {fr_join['total_broadcasts_seen'].min()}, max {fr_join['total_broadcasts_seen'].max()})")
    # Correlate with first_round_Erdogan probability
    corr_erd = fr_join[["total_broadcasts_seen", "first_round_Erdogan"]].corr().iloc[0, 1]
    corr_kil = fr_join[["total_broadcasts_seen", "first_round_Kilicdaroglu"]].corr().iloc[0, 1]
    print(f"Pearson corr(total_broadcasts_seen, first_round_Erdogan)        = {corr_erd:+.3f}")
    print(f"Pearson corr(total_broadcasts_seen, first_round_Kilicdaroglu)  = {corr_kil:+.3f}")


def section_11_llm_artifacts(df):
    banner("D.11  LLM OUTPUT QUALITY ARTIFACTS")
    # short_code placeholder bug
    df["_codes"] = df["reason_codes"].apply(parse_codes)
    df["_has_short_code"] = df["_codes"].apply(lambda lst: "short_code" in lst)
    df["_has_provider_error"] = df["_codes"].apply(lambda lst: "provider_error" in lst)
    df["_starts_as_a"] = df["reflection"].fillna("").str.startswith("As a ")
    df["_reflection_len"] = df["reflection"].fillna("").str.len()

    n = len(df)
    pct = lambda x: 100 * x / n
    print(f"Total decisions: {n}")
    print(f"  with 'short_code' placeholder in reason_codes: {df['_has_short_code'].sum()}  ({pct(df['_has_short_code'].sum()):.2f} %)")
    print(f"  with 'provider_error' fallback:                {df['_has_provider_error'].sum()}  ({pct(df['_has_provider_error'].sum()):.2f} %)")
    print(f"  reflection starts with 'As a ':                {df['_starts_as_a'].sum()}  ({pct(df['_starts_as_a'].sum()):.2f} %)")
    print(f"  reflection length (chars): mean={df['_reflection_len'].mean():.1f}, median={df['_reflection_len'].median():.0f}, "
          f"min={df['_reflection_len'].min()}, max={df['_reflection_len'].max()}")
    print(f"  empty reflections: {(df['_reflection_len'] == 0).sum()}")

    print("\nConfidence distribution:")
    print(df["confidence"].value_counts(dropna=False).to_string())

    print("\nMost common reason codes (top 25):")
    flat = [c for lst in df["_codes"] for c in lst]
    for code, cnt in Counter(flat).most_common(25):
        print(f"  {code:40s} {cnt:6d}  ({100*cnt/n:.2f} %)")

    # frequency by tick of 'short_code'
    print("\n'short_code' incidence by tick (worst 5):")
    by_tick = df.groupby("tick_id")["_has_short_code"].mean().sort_values(ascending=False).head(5)
    for t, r in by_tick.items():
        print(f"  {t:36s} {r*100:.1f} %")


def section_12_diagnostic_decomp(fr_rows, ro_rows):
    banner("D.12  DIAGNOSTIC DECOMPOSITION — where the simulation went wrong")
    # By archetype: contribution to the Erdogan under-estimate.
    # Each archetype's first_round_Erdogan probability mean times its sample weight.
    n_total = len(fr_rows)
    arch_weights = fr_rows.groupby("archetype_name").size() / n_total
    arch_mean_erd = fr_rows.groupby("archetype_name")["first_round_Erdogan"].mean() * 100
    arch_mean_kil = fr_rows.groupby("archetype_name")["first_round_Kilicdaroglu"].mean() * 100
    arch_mean_ogan = fr_rows.groupby("archetype_name")["first_round_Sinan_Ogan"].mean() * 100
    arch_mean_und = fr_rows.groupby("archetype_name")["first_round_Undecided"].mean() * 100
    arch_contrib_erd = arch_weights * arch_mean_erd
    arch_contrib_kil = arch_weights * arch_mean_kil
    arch_contrib_ogan = arch_weights * arch_mean_ogan
    arch_contrib_und = arch_weights * arch_mean_und
    print(f"{'Archetype':42s} {'weight':>7s}  {'mean Erd':>9s}  {'contrib Erd':>12s}  {'contrib Kil':>12s}  {'contrib Ogan':>13s}  {'contrib Und':>12s}")
    for arch in arch_mean_erd.sort_values(ascending=False).index:
        print(f"{arch:42s} {arch_weights[arch]:7.3%}  {arch_mean_erd[arch]:9.2f}  "
              f"{arch_contrib_erd[arch]:12.3f}  {arch_contrib_kil[arch]:12.3f}  "
              f"{arch_contrib_ogan[arch]:13.3f}  {arch_contrib_und[arch]:12.3f}")
    print(f"{'TOTAL':42s} {arch_weights.sum():7.3%}  "
          f"{'':9s}  {arch_contrib_erd.sum():12.3f}  {arch_contrib_kil.sum():12.3f}  "
          f"{arch_contrib_ogan.sum():13.3f}  {arch_contrib_und.sum():12.3f}")

    # Where would Sinan Ogan's 5.17% have come from?
    print("\nIf Sinan Ogan's 5.17% had come from each archetype proportional to their MHP/IYI/A3 share:")
    print("(see archetype-by-archetype mean Ogan probabilities above for diagnosis)")


def main():
    df = load_panel()
    section_1_panel_sanity(df)
    fr_rows, ro_rows, fr_mp, ro_mp, fr_mode, ro_mode = section_2_headline(df)
    section_3_mae(fr_mp, ro_mp)
    section_4_archetype(df, fr_rows, ro_rows)
    section_5_archetype_mean_probs(df, fr_rows, ro_rows)
    section_6_demographics(df, fr_rows, ro_rows)
    section_7_transitions(df, fr_rows, ro_rows)
    section_8_trajectories(df)
    section_9_within_archetype_dispersion(df, fr_rows)
    section_10_broadcast_exposure(df, fr_rows)
    section_11_llm_artifacts(df)
    section_12_diagnostic_decomp(fr_rows, ro_rows)


if __name__ == "__main__":
    main()
