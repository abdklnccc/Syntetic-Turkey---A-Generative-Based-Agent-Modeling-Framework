"""Mode-vote aggregation under three tie-handling rules.

Computes simulated first-round (T030A) and runoff (T035A) mode-vote shares under:
  (1) the canonical key order used by metrics.py (Erdogan first),
  (2) the reverse canonical order (Erdogan last),
  (3) random tie-break with 10,000 Monte Carlo samples (mean + 95% percentile interval).

Also enumerates tied agents by tie composition.

Outputs:
  outputs/tie_handling_sensitivity.md   (Markdown tables for the manuscript)
  outputs/tie_handling_sensitivity.csv  (long-format CSV)
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "outputs" / "agent_trajectories.csv"
OUT_MD = ROOT / "outputs" / "tie_handling_sensitivity.md"
OUT_CSV = ROOT / "outputs" / "tie_handling_sensitivity.csv"

DECISION_FIRST = "T030A_first_round_vote_decision"
DECISION_RUNOFF = "T035A_runoff_vote_decision"

# Canonical key orders (see memory/beliefs.py and metrics.py)
FIRST_CANONICAL = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"]
RUNOFF_CANONICAL = ["Erdogan", "Kilicdaroglu", "Abstain_Invalid_Undecided"]

LABELS = {
    "Erdogan": "Erdoğan",
    "Kilicdaroglu": "Kılıçdaroğlu",
    "Sinan_Ogan": "S. Oğan",
    "Muharrem_Ince": "M. İnce",
    "Other": "Other",
    "Undecided": "Undecided",
    "Abstain_Invalid_Undecided": "Abstain / Invalid / Undec.",
}

ACTUAL_FIRST_PCT = {"Erdogan": 49.52, "Kilicdaroglu": 44.88, "Sinan_Ogan": 5.17, "Muharrem_Ince": 0.43}
ACTUAL_RUNOFF_PCT = {"Erdogan": 52.18, "Kilicdaroglu": 47.82}

N_MC = 10_000
SEED = 42


def get_distribution_columns(round_name: str, keys: list[str]) -> list[str]:
    prefix = "first_round_" if round_name == "first_round" else "runoff_"
    return [prefix + k for k in keys]


def find_tied_winners(prob_row: pd.Series, keys: list[str]) -> list[str]:
    """Return the list of candidates sharing the maximum probability for one agent."""
    vals = prob_row.values
    max_v = vals.max()
    if max_v <= 0:
        # Degenerate row — fall back to all keys (extremely unlikely after normalization)
        return list(keys)
    return [k for k, v in zip(keys, vals) if v == max_v]


def break_tie_by_order(tied: list[str], order: list[str]) -> str:
    """Return the candidate in `tied` that appears earliest in `order`."""
    for k in order:
        if k in tied:
            return k
    return tied[0]


def aggregate_share(winners: list[str], keys: list[str]) -> dict[str, float]:
    """Return percent share of each candidate among `winners`."""
    n = len(winners)
    if n == 0:
        return {k: 0.0 for k in keys}
    counts = Counter(winners)
    return {k: 100.0 * counts.get(k, 0) / n for k in keys}


def monte_carlo_random_tiebreak(tied_lists: list[list[str]], keys: list[str],
                                 n_iter: int = N_MC, seed: int = SEED) -> dict[str, tuple[float, float, float]]:
    """Run Monte Carlo random tie-break. Returns {candidate: (mean_pct, lo_pct, hi_pct)}."""
    rng = np.random.default_rng(seed)
    n = len(tied_lists)
    pct_counts = {k: np.empty(n_iter, dtype=np.float64) for k in keys}
    for it in range(n_iter):
        counts = {k: 0 for k in keys}
        for tied in tied_lists:
            choice = tied[rng.integers(0, len(tied))]
            counts[choice] += 1
        for k in keys:
            pct_counts[k][it] = 100.0 * counts[k] / n
    out = {}
    for k in keys:
        arr = pct_counts[k]
        out[k] = (
            float(arr.mean()),
            float(np.percentile(arr, 2.5)),
            float(np.percentile(arr, 97.5)),
        )
    return out


def tie_composition_summary(per_agent_tied: list[list[str]]) -> list[dict]:
    """Aggregate tied-agent groups by tie-set composition (only real ties, i.e. len > 1)."""
    only_ties = [tuple(sorted(t)) for t in per_agent_tied if len(t) > 1]
    counts = Counter(only_ties)
    return [
        {"tied_candidates": " + ".join(LABELS.get(c, c) for c in combo),
         "n_agents": n,
         "size_of_tie": len(combo)}
        for combo, n in counts.most_common()
    ]


def analyse_round(df: pd.DataFrame, tick_id: str, round_name: str, canonical: list[str]) -> dict:
    rows = df[df["tick_id"] == tick_id]
    cols = get_distribution_columns(round_name, canonical)
    prob = rows[cols].copy()
    prob.columns = canonical  # rename to the bare candidate keys
    per_agent_tied = [find_tied_winners(prob.iloc[i], canonical) for i in range(len(prob))]

    # Rule 1: canonical order (Erdogan first)
    canon_winners = [break_tie_by_order(t, canonical) for t in per_agent_tied]
    canon_share = aggregate_share(canon_winners, canonical)

    # Rule 2: reverse canonical (Erdogan last)
    reverse_order = list(reversed(canonical))
    reverse_winners = [break_tie_by_order(t, reverse_order) for t in per_agent_tied]
    reverse_share = aggregate_share(reverse_winners, canonical)

    # Rule 3: random tie-break, Monte Carlo
    mc_results = monte_carlo_random_tiebreak(per_agent_tied, canonical)

    n_total = len(rows)
    n_tied = sum(1 for t in per_agent_tied if len(t) > 1)
    tie_table = tie_composition_summary(per_agent_tied)

    return {
        "tick_id": tick_id,
        "round_name": round_name,
        "canonical": canonical,
        "n_total": n_total,
        "n_tied": n_tied,
        "n_untied": n_total - n_tied,
        "canon_share": canon_share,
        "reverse_share": reverse_share,
        "mc": mc_results,  # candidate -> (mean, lo, hi)
        "tie_table": tie_table,
    }


def render_markdown(first: dict, runoff: dict) -> str:
    lines = []
    lines.append("# Mode-vote sensitivity to tie handling")
    lines.append("")
    lines.append(f"Computed from `outputs/agent_trajectories.csv`. Random tie-break uses {N_MC:,} Monte Carlo samples (seed={SEED}).")
    lines.append("")
    lines.append(f"- **First-round agents tied at top (T030A):** {first['n_tied']} of {first['n_total']} ({100*first['n_tied']/first['n_total']:.1f}%)")
    lines.append(f"- **Runoff agents tied at top (T035A):** {runoff['n_tied']} of {runoff['n_total']} ({100*runoff['n_tied']/runoff['n_total']:.1f}%)")
    lines.append("")

    def render_round(r: dict, actual: dict[str, float]):
        lines.append(f"## {r['tick_id']} ({'first round' if r['round_name']=='first_round' else 'runoff'})")
        lines.append("")
        # main results table
        header = ["Candidate", "Actual (YSK) %"]
        header += ["Rule 1: canonical (Erdoğan first) %",
                   "Rule 2: reverse (Erdoğan last) %",
                   f"Rule 3: random tie-break — mean % [95% interval]"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for c in r["canonical"]:
            label = LABELS.get(c, c)
            actual_str = f"{actual.get(c, 0):.2f}" if c in actual else "—"
            canon_v = r["canon_share"][c]
            rev_v = r["reverse_share"][c]
            mc_m, mc_lo, mc_hi = r["mc"][c]
            lines.append(f"| {label} | {actual_str} | {canon_v:.2f} | {rev_v:.2f} | {mc_m:.2f}  [{mc_lo:.2f}, {mc_hi:.2f}] |")
        lines.append("")

        # winners summary
        winner_canon = max(r["canon_share"], key=r["canon_share"].get)
        winner_rev = max(r["reverse_share"], key=r["reverse_share"].get)
        winner_mc_means = {c: r["mc"][c][0] for c in r["canonical"]}
        winner_mc = max(winner_mc_means, key=winner_mc_means.get)
        lines.append(f"*Winner under rule 1:* **{LABELS[winner_canon]}** — *rule 2:* **{LABELS[winner_rev]}** — *rule 3 (mean):* **{LABELS[winner_mc]}**.")
        lines.append("")

        # tie composition
        if r["tie_table"]:
            lines.append(f"### Tied-agent breakdown ({r['n_tied']} agents)")
            lines.append("")
            lines.append("| Tied candidates | Tie size | Agents |")
            lines.append("| --- | --- | --- |")
            for row in r["tie_table"]:
                lines.append(f"| {row['tied_candidates']} | {row['size_of_tie']} | {row['n_agents']} |")
            lines.append("")
        else:
            lines.append("*(No tied agents in this round.)*")
            lines.append("")

    render_round(first, ACTUAL_FIRST_PCT)
    render_round(runoff, ACTUAL_RUNOFF_PCT)

    lines.append("## Notes")
    lines.append("")
    lines.append("- Rule 1 (canonical order) is the rule used by `validation/metrics.py`. It corresponds to `max(distribution, key=distribution.get)` on a dict whose insertion order is `[Erdoğan, Kılıçdaroğlu, Sinan Oğan, M. İnce, Other, Undecided]` for the first round and `[Erdoğan, Kılıçdaroğlu, Abstain/Invalid/Undecided]` for the runoff.")
    lines.append("- Rule 2 reverses this ordering, so Erdoğan loses every tie he is part of.")
    lines.append("- Rule 3 is a Monte Carlo random tie-break: each tied agent independently picks one of their tied candidates uniformly at random; the table reports the mean and 2.5 / 97.5 percentile of each candidate's share across the simulation runs.")
    lines.append("- Untied agents are unaffected by any of these rules. Differences across rules are driven only by the tied agents enumerated above.")
    lines.append("")
    return "\n".join(lines)


def render_csv(first: dict, runoff: dict) -> pd.DataFrame:
    rows = []
    for r, actual in [(first, ACTUAL_FIRST_PCT), (runoff, ACTUAL_RUNOFF_PCT)]:
        for c in r["canonical"]:
            mc_m, mc_lo, mc_hi = r["mc"][c]
            rows.append({
                "tick_id": r["tick_id"],
                "round": r["round_name"],
                "candidate": c,
                "candidate_label": LABELS.get(c, c),
                "actual_pct": actual.get(c, np.nan),
                "rule_1_canonical_pct": r["canon_share"][c],
                "rule_2_reverse_pct": r["reverse_share"][c],
                "rule_3_random_mean_pct": mc_m,
                "rule_3_random_ci_low_pct": mc_lo,
                "rule_3_random_ci_high_pct": mc_hi,
                "n_total_agents": r["n_total"],
                "n_tied_agents": r["n_tied"],
            })
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(CSV)
    first = analyse_round(df, DECISION_FIRST, "first_round", FIRST_CANONICAL)
    runoff = analyse_round(df, DECISION_RUNOFF, "runoff", RUNOFF_CANONICAL)

    md = render_markdown(first, runoff)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)} ({len(md):,} chars)")

    csv_df = render_csv(first, runoff)
    csv_df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(csv_df)} rows)")

    # Also echo the headline table to stdout for the chat
    print()
    print(md)


if __name__ == "__main__":
    main()
