from __future__ import annotations

import csv
import json
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
SOULS = ROOT / "souls"
TRAJECTORIES = OUTPUTS / "agent_trajectories.csv"
DASHBOARD = OUTPUTS / "deep_analysis_dashboard.html"

CANDIDATES = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"]
RUNOFF = ["Erdogan", "Kilicdaroglu", "Abstain_Invalid_Undecided"]
PARTIES = ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP", "YRP", "Other", "Undecided"]

FIRST_TICK = "T001"
FIRST_ROUND_TICK = "T030A_first_round_vote_decision"
RUNOFF_TICK = "T035A_runoff_vote_decision"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_souls() -> dict[str, dict[str, Any]]:
    souls: dict[str, dict[str, Any]] = {}
    for path in sorted(SOULS.glob("agent_*.json")):
        if len(path.stem) != len("agent_001"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        souls[data["identity"]["agent_id"]] = data
    return souls


def baseline_value(soul: dict[str, Any], key: str) -> str:
    meta = soul.get("simulation_metadata", {}).get("baseline_2018", {})
    numeric = soul.get("numeric_profile", {}).get("baseline_2018", {})
    return str(meta.get(key) or numeric.get(key) or "Unknown")


def f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else 0.0


def top_key(row: dict[str, str], prefix: str, keys: list[str]) -> str:
    return max(keys, key=lambda key: f(row, f"{prefix}{key}"))


def count_rows(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(Counter(row.get(field, "Unknown") or "Unknown" for row in rows))


def transition_counts(
    agent_ids: list[str],
    source_by_agent: dict[str, str],
    target_by_agent: dict[str, str],
) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str]] = Counter()
    for agent_id in agent_ids:
        counts[(source_by_agent.get(agent_id, "Unknown"), target_by_agent.get(agent_id, "Unknown"))] += 1
    return [
        {"source": source, "target": target, "value": value}
        for (source, target), value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def mean_series(rows: list[dict[str, str]], prefix: str, keys: list[str]) -> dict[str, float]:
    if not rows:
        return {key: 0.0 for key in keys}
    return {key: round(mean(f(row, f"{prefix}{key}") for row in rows) * 100, 3) for key in keys}


def sorted_ticks(rows: list[dict[str, str]]) -> list[str]:
    ticks: OrderedDict[str, None] = OrderedDict()
    for row in rows:
        ticks.setdefault(row["tick_id"], None)
    return list(ticks)


def pct_change(start: float, end: float) -> float:
    return round(end - start, 2)


def build_data() -> dict[str, Any]:
    souls = load_souls()
    rows = read_csv(TRAJECTORIES)
    tick_ids = sorted_ticks(rows)
    rows_by_tick: dict[str, list[dict[str, str]]] = defaultdict(list)
    rows_by_agent: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_tick[row["tick_id"]].append(row)
        rows_by_agent[row["agent_id"]].append(row)

    first_rows = rows_by_tick[FIRST_TICK]
    final_first_rows = rows_by_tick[FIRST_ROUND_TICK]
    final_party_rows = rows_by_tick[RUNOFF_TICK]
    final_runoff_rows = rows_by_tick[RUNOFF_TICK]
    agent_ids = sorted(souls)

    baseline_candidate = {
        agent_id: baseline_value(souls[agent_id], "presidential_vote_2018") for agent_id in agent_ids
    }
    baseline_party = {
        agent_id: baseline_value(souls[agent_id], "party_2018_internal_key") for agent_id in agent_ids
    }
    final_candidate = {row["agent_id"]: row["first_round_top"] for row in final_first_rows}
    final_runoff = {row["agent_id"]: row["runoff_top"] for row in final_runoff_rows}
    final_party = {row["agent_id"]: row["party_top"] for row in final_party_rows}

    archetypes = sorted({souls[agent_id]["identity"]["archetype_name"] for agent_id in agent_ids})
    grouped_by_tick_arch: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped_by_tick_arch[(row["tick_id"], row["archetype_name"])].append(row)

    archetype_series: dict[str, Any] = {}
    archetype_rows: list[dict[str, Any]] = []
    for archetype in archetypes:
        series_candidate = {key: [] for key in CANDIDATES}
        series_runoff = {key: [] for key in RUNOFF}
        series_party = {key: [] for key in PARTIES}
        for tick in tick_ids:
            cohort = grouped_by_tick_arch[(tick, archetype)]
            candidate_avg = mean_series(cohort, "first_round_", CANDIDATES)
            runoff_avg = mean_series(cohort, "runoff_", RUNOFF)
            party_avg = mean_series(cohort, "party_", PARTIES)
            for key in CANDIDATES:
                series_candidate[key].append(candidate_avg[key])
            for key in RUNOFF:
                series_runoff[key].append(runoff_avg[key])
            for key in PARTIES:
                series_party[key].append(party_avg[key])

        archetype_agent_ids = [
            agent_id for agent_id in agent_ids if souls[agent_id]["identity"]["archetype_name"] == archetype
        ]
        first_cohort = [row for row in final_first_rows if row["agent_id"] in set(archetype_agent_ids)]
        party_cohort = [row for row in final_party_rows if row["agent_id"] in set(archetype_agent_ids)]
        baseline_c = Counter(baseline_candidate[agent_id] for agent_id in archetype_agent_ids)
        baseline_p = Counter(baseline_party[agent_id] for agent_id in archetype_agent_ids)
        latest_c = Counter(row["first_round_top"] for row in first_cohort)
        latest_p = Counter(row["party_top"] for row in party_cohort)
        archetype_rows.append(
            {
                "archetype": archetype,
                "n": len(archetype_agent_ids),
                "candidate_2018_top": baseline_c.most_common(1)[0][0],
                "candidate_2018_count": baseline_c.most_common(1)[0][1],
                "candidate_2023_top": latest_c.most_common(1)[0][0],
                "candidate_2023_count": latest_c.most_common(1)[0][1],
                "party_2018_top": baseline_p.most_common(1)[0][0],
                "party_2018_count": baseline_p.most_common(1)[0][1],
                "party_2023_top": latest_p.most_common(1)[0][0],
                "party_2023_count": latest_p.most_common(1)[0][1],
                "erdogan_probability_shift": pct_change(series_candidate["Erdogan"][0], series_candidate["Erdogan"][tick_ids.index(FIRST_ROUND_TICK)]),
                "kilicdaroglu_probability_shift": pct_change(series_candidate["Kilicdaroglu"][0], series_candidate["Kilicdaroglu"][tick_ids.index(FIRST_ROUND_TICK)]),
                "akp_probability_shift": pct_change(series_party["AKP"][0], series_party["AKP"][tick_ids.index(RUNOFF_TICK)]),
                "chp_probability_shift": pct_change(series_party["CHP"][0], series_party["CHP"][tick_ids.index(RUNOFF_TICK)]),
            }
        )
        archetype_series[archetype] = {
            "candidate": series_candidate,
            "runoff": series_runoff,
            "party": series_party,
        }

    agent_series: dict[str, Any] = {}
    for agent_id, agent_rows in rows_by_agent.items():
        soul = souls[agent_id]
        agent_series[agent_id] = {
            "archetype": soul["identity"]["archetype_name"],
            "city": soul["identity"].get("city", ""),
            "baseline_candidate": baseline_candidate[agent_id],
            "baseline_party": baseline_party[agent_id],
            "final_candidate": final_candidate.get(agent_id, "Unknown"),
            "final_party": final_party.get(agent_id, "Unknown"),
            "candidate": {
                key: [round(f(row, f"first_round_{key}") * 100, 3) for row in agent_rows] for key in CANDIDATES
            },
            "party": {key: [round(f(row, f"party_{key}") * 100, 3) for row in agent_rows] for key in PARTIES},
        }

    aggregate_candidate = {tick: mean_series(rows_by_tick[tick], "first_round_", CANDIDATES) for tick in tick_ids}
    aggregate_party = {tick: mean_series(rows_by_tick[tick], "party_", PARTIES) for tick in tick_ids}

    return {
        "meta": {
            "agents": len(agent_ids),
            "ticks": len(tick_ids),
            "firstTick": FIRST_TICK,
            "firstRoundTick": FIRST_ROUND_TICK,
            "runoffTick": RUNOFF_TICK,
            "firstRoundDate": final_first_rows[0]["sim_date"],
            "runoffDate": final_runoff_rows[0]["sim_date"],
        },
        "tickIds": tick_ids,
        "tickDates": [rows_by_tick[tick][0]["sim_date"] for tick in tick_ids],
        "keys": {"candidates": CANDIDATES, "runoff": RUNOFF, "parties": PARTIES},
        "counts": {
            "candidate2018": dict(Counter(baseline_candidate.values())),
            "candidate2023": count_rows(final_first_rows, "first_round_top"),
            "runoff2023": dict(Counter(final_runoff.values())),
            "party2018": dict(Counter(baseline_party.values())),
            "party2023": count_rows(final_party_rows, "party_top"),
        },
        "weighted": {
            "initialCandidate": mean_series(first_rows, "first_round_", CANDIDATES),
            "finalCandidate": mean_series(final_first_rows, "first_round_", CANDIDATES),
            "initialParty": mean_series(first_rows, "party_", PARTIES),
            "finalParty": mean_series(final_party_rows, "party_", PARTIES),
        },
        "transitions": {
            "candidate": transition_counts(agent_ids, baseline_candidate, final_candidate),
            "party": transition_counts(agent_ids, baseline_party, final_party),
        },
        "aggregate": {
            "candidate": aggregate_candidate,
            "party": aggregate_party,
        },
        "archetypes": archetypes,
        "archetypeSeries": archetype_series,
        "archetypeRows": sorted(archetype_rows, key=lambda row: (-row["n"], row["archetype"])),
        "agentSeries": agent_series,
    }


def html_document(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Synthetic Turkey 300-Agent Deep Analysis</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {{
      --ink: #172033;
      --muted: #647084;
      --line: #dfe5ee;
      --paper: #f7f8fb;
      --panel: #ffffff;
      --red: #b4232a;
      --blue: #246bce;
      --violet: #6f43c0;
      --teal: #178b89;
      --amber: #b7791f;
      --green: #2f855a;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--paper); }}
    header {{ background: #172033; color: white; padding: 28px 36px 22px; border-bottom: 4px solid #c8a454; }}
    header h1 {{ margin: 0; font-size: clamp(24px, 3vw, 38px); letter-spacing: 0; }}
    header p {{ margin: 10px 0 0; max-width: 1100px; color: #d8dee9; line-height: 1.55; }}
    main {{ padding: 24px 36px 44px; }}
    .toolbar {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-bottom: 18px; }}
    .pill {{ border: 1px solid var(--line); background: white; color: var(--ink); padding: 9px 12px; border-radius: 8px; font-weight: 700; cursor: pointer; }}
    .pill.active {{ background: #172033; color: white; border-color: #172033; }}
    .metrics {{ display: grid; grid-template-columns: repeat(5, minmax(140px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .metric {{ background: white; border: 1px solid var(--line); border-radius: 8px; padding: 14px; min-height: 88px; }}
    .metric span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    .metric strong {{ display: block; font-size: 24px; margin-top: 8px; }}
    section {{ display: none; }}
    section.active {{ display: block; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 16px; }}
    .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px; min-width: 0; }}
    .panel.wide {{ grid-column: 1 / -1; }}
    .panel h2 {{ margin: 0 0 4px; font-size: 18px; }}
    .panel p {{ margin: 4px 0 12px; color: var(--muted); line-height: 1.45; }}
    .chart {{ width: 100%; min-height: 430px; }}
    .chart.tall {{ min-height: 620px; }}
    .controls {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin: 10px 0 12px; }}
    select, input {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; background: white; color: var(--ink); min-width: 220px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid #edf1f6; text-align: left; white-space: nowrap; }}
    th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; background: #fbfcfe; position: sticky; top: 0; }}
    .table-wrap {{ overflow: auto; max-height: 560px; border: 1px solid var(--line); border-radius: 8px; }}
    .note {{ border-left: 4px solid #c8a454; background: #fffaf0; padding: 12px 14px; color: #5f4b18; line-height: 1.45; margin-bottom: 16px; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .metrics, .grid {{ grid-template-columns: 1fr; }}
      .panel.wide {{ grid-column: auto; }}
      .chart {{ min-height: 360px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Synthetic Turkey 300-Agent Deep Analysis Dashboard</h1>
    <p>Interactive thesis dashboard for the latest 300-agent run. It compares the synthetic 2018 baseline persona memory with the simulated 2023 election state, and traces how probability weights moved across candidates, runoff options, and parties through all ticks.</p>
  </header>
  <main>
    <nav class="toolbar" aria-label="Dashboard sections">
      <button class="pill active" data-tab="overview">Vote Shifts</button>
      <button class="pill" data-tab="probabilities">Persona Probabilities</button>
      <button class="pill" data-tab="agents">Agent Explorer</button>
      <button class="pill" data-tab="tables">Thesis Tables</button>
    </nav>
    <div class="metrics" id="metrics"></div>
    <div class="note">Counts are top-choice agent counts. Weighted charts are mean probability mass, so they can tell a different story than top-choice counts when agents are uncertain or split.</div>

    <section id="overview" class="active">
      <div class="grid">
        <div class="panel"><h2>2018 Presidential Baseline vs 2023 First Round</h2><p>Top-choice count comparison from persona baseline memory to simulated 2023 first-round decision.</p><div id="candidateCounts" class="chart"></div></div>
        <div class="panel"><h2>2018 Party Baseline vs 2023 Party Preference</h2><p>Party top-choice counts at the runoff decision tick compared with 2018 baseline party votes.</p><div id="partyCounts" class="chart"></div></div>
        <div class="panel wide"><h2>Presidential Vote Flow: 2018 to 2023</h2><p>Each band shows how many agents moved from their 2018 presidential anchor to their 2023 first-round simulated top choice.</p><div id="candidateSankey" class="chart tall"></div></div>
        <div class="panel wide"><h2>Party Vote Flow: 2018 to 2023</h2><p>Each band shows movement from 2018 party vote memory to final simulated party preference.</p><div id="partySankey" class="chart tall"></div></div>
        <div class="panel wide"><h2>Population Probability Weight Over Ticks</h2><p>Mean probability mass across all 300 agents, not just final top choices.</p><div id="aggregateProbabilities" class="chart"></div></div>
      </div>
    </section>

    <section id="probabilities">
      <div class="grid">
        <div class="panel wide">
          <h2>Persona Cohort Trajectories</h2>
          <p>Select an archetype/persona cohort to see how its probability weight changed through the simulated timeline.</p>
          <div class="controls"><select id="archetypeSelect"></select></div>
          <div id="archetypeCandidate" class="chart"></div>
          <div id="archetypeParty" class="chart"></div>
        </div>
        <div class="panel wide"><h2>Candidate Probability Shift by Persona</h2><p>Final first-round probability minus T001 probability, in percentage points.</p><div id="candidateHeatmap" class="chart tall"></div></div>
        <div class="panel wide"><h2>Party Probability Shift by Persona</h2><p>Final party probability at runoff tick minus T001 probability, in percentage points.</p><div id="partyHeatmap" class="chart tall"></div></div>
      </div>
    </section>

    <section id="agents">
      <div class="grid">
        <div class="panel wide">
          <h2>Individual Agent Probability Trace</h2>
          <p>This keeps the thesis audit trail visible: every synthetic voter has an inspectable probability history.</p>
          <div class="controls"><select id="agentSelect"></select></div>
          <div id="agentMeta"></div>
          <div id="agentCandidate" class="chart"></div>
          <div id="agentParty" class="chart"></div>
        </div>
      </div>
    </section>

    <section id="tables">
      <div class="grid">
        <div class="panel wide"><h2>Persona-Level 2018 to 2023 Summary</h2><p>Dominant baseline and final choices per persona cohort, with probability-point movement for Erdoğan/Kılıçdaroğlu and AKP/CHP.</p><div class="table-wrap"><table id="archetypeTable"></table></div></div>
        <div class="panel wide"><h2>Largest Presidential Transition Cells</h2><p>Most common 2018 presidential anchor to 2023 first-round top-choice transitions.</p><div class="table-wrap"><table id="candidateTransitionTable"></table></div></div>
        <div class="panel wide"><h2>Largest Party Transition Cells</h2><p>Most common 2018 party baseline to 2023 party top-choice transitions.</p><div class="table-wrap"><table id="partyTransitionTable"></table></div></div>
      </div>
    </section>
  </main>

  <script id="dashboard-data" type="application/json">{payload}</script>
  <script>
    const data = JSON.parse(document.getElementById('dashboard-data').textContent);
    const palette = {{
      Erdogan: '#b4232a', Kilicdaroglu: '#246bce', Sinan_Ogan: '#6f43c0', Muharrem_Ince: '#178b89',
      Other: '#7a8494', Undecided: '#a0a7b4', Abstain_Invalid_Undecided: '#697386',
      AKP: '#b4232a', CHP: '#246bce', MHP: '#6f43c0', IYI: '#1c7c9f', DEM_HDP_YSP: '#2f855a',
      YRP: '#b7791f'
    }};
    if (!window.Plotly) {{
      window.Plotly = {{
        react: (id, traces, layout) => window.Plotly.newPlot(id, traces, layout),
        newPlot: (id, traces, layout = {{}}) => {{
          const el = typeof id === 'string' ? document.getElementById(id) : id;
          const width = Math.max(680, el.clientWidth || 900);
          const height = el.classList.contains('tall') ? 620 : 430;
          const m = {{l: 64, r: 28, t: 28, b: 82, ...(layout.margin || {{}})}};
          const plotW = width - m.l - m.r;
          const plotH = height - m.t - m.b;
          const esc = value => String(value).replace(/[&<>"]/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[ch]));
          const sx = i => m.l + (plotW * i / Math.max(1, ((traces[0]?.x || data.tickIds).length - 1)));
          const svg = parts => '<svg viewBox="0 0 ' + width + ' ' + height + '" width="100%" height="' + height + '" role="img">' + parts.join('') + '</svg>';
          const grid = (maxY = 100, suffix = '%') => {{
            const parts = [];
            for (let y = 0; y <= maxY; y += maxY / 5) {{
              const py = m.t + plotH - (plotH * y / maxY);
              parts.push('<line x1="' + m.l + '" y1="' + py + '" x2="' + (m.l + plotW) + '" y2="' + py + '" stroke="#edf1f6"/>');
              parts.push('<text x="' + (m.l - 12) + '" y="' + (py + 4) + '" text-anchor="end" font-size="11" fill="#647084">' + Math.round(y) + suffix + '</text>');
            }}
            return parts;
          }};
          if (traces[0]?.type === 'bar') {{
            const keys = traces[0].x;
            const maxY = Math.max(1, ...traces.flatMap(t => t.y));
            const parts = grid(Math.ceil(maxY / 20) * 20, '');
            const slot = plotW / keys.length;
            const barW = slot * 0.68 / traces.length;
            traces.forEach((trace, ti) => {{
              trace.y.forEach((value, i) => {{
                const x = m.l + i * slot + slot * 0.16 + ti * barW;
                const h = plotH * value / (Math.ceil(maxY / 20) * 20);
                const y = m.t + plotH - h;
                const color = Array.isArray(trace.marker?.color) ? trace.marker.color[i] : (trace.marker?.color || '#246bce');
                parts.push('<rect x="' + x + '" y="' + y + '" width="' + Math.max(2, barW - 3) + '" height="' + h + '" rx="3" fill="' + color + '"><title>' + esc(trace.name + ' · ' + keys[i] + ': ' + value) + '</title></rect>');
              }});
            }});
            keys.forEach((key, i) => parts.push('<text x="' + (m.l + i * slot + slot / 2) + '" y="' + (m.t + plotH + 24) + '" text-anchor="middle" font-size="11" fill="#647084" transform="rotate(-28 ' + (m.l + i * slot + slot / 2) + ' ' + (m.t + plotH + 24) + ')">' + esc(key) + '</text>'));
            traces.forEach((trace, i) => parts.push('<text x="' + (m.l + i * 150) + '" y="' + (height - 18) + '" font-size="12" fill="#172033">■ ' + esc(trace.name) + '</text>'));
            el.innerHTML = svg(parts);
            return Promise.resolve();
          }}
          if (traces[0]?.type === 'heatmap') {{
            const trace = traces[0], rows = trace.y, cols = trace.x;
            const vals = trace.z.flat();
            const maxAbs = Math.max(1, ...vals.map(v => Math.abs(v)));
            const cellW = plotW / cols.length, cellH = plotH / rows.length;
            const color = v => v < 0 ? 'rgba(180,35,42,' + (0.18 + 0.72 * Math.abs(v) / maxAbs) + ')' : 'rgba(36,107,206,' + (0.18 + 0.72 * Math.abs(v) / maxAbs) + ')';
            const parts = [];
            rows.forEach((row, ri) => cols.forEach((col, ci) => {{
              const v = trace.z[ri][ci];
              parts.push('<rect x="' + (m.l + ci * cellW) + '" y="' + (m.t + ri * cellH) + '" width="' + cellW + '" height="' + cellH + '" fill="' + color(v) + '" stroke="#fff"><title>' + esc(row + ' · ' + col + ': ' + v + ' pp') + '</title></rect>');
              if (Math.abs(v) >= 8) parts.push('<text x="' + (m.l + ci * cellW + cellW / 2) + '" y="' + (m.t + ri * cellH + cellH / 2 + 4) + '" text-anchor="middle" font-size="10" fill="#172033">' + v.toFixed(0) + '</text>');
            }}));
            rows.forEach((row, i) => parts.push('<text x="' + (m.l - 10) + '" y="' + (m.t + i * cellH + cellH / 2 + 4) + '" text-anchor="end" font-size="11" fill="#647084">' + esc(row.slice(0, 30)) + '</text>'));
            cols.forEach((col, i) => parts.push('<text x="' + (m.l + i * cellW + cellW / 2) + '" y="' + (m.t + plotH + 24) + '" text-anchor="middle" font-size="11" fill="#647084" transform="rotate(-24 ' + (m.l + i * cellW + cellW / 2) + ' ' + (m.t + plotH + 24) + ')">' + esc(col) + '</text>'));
            el.innerHTML = svg(parts);
            return Promise.resolve();
          }}
          if (traces[0]?.type === 'sankey') {{
            const links = traces[0].link;
            const labels = traces[0].node.label;
            const left = labels.map((label, i) => [label, i]).filter(([label]) => label.startsWith('2018'));
            const right = labels.map((label, i) => [label, i]).filter(([label]) => label.startsWith('2023'));
            const yFor = (arr, idx) => m.t + 28 + arr.findIndex(([, i]) => i === idx) * 54;
            const maxV = Math.max(1, ...links.value);
            const parts = [];
            links.value.forEach((value, i) => {{
              const y1 = yFor(left, links.source[i]), y2 = yFor(right, links.target[i]);
              const sw = 1 + 18 * value / maxV;
              parts.push('<path d="M' + (m.l + 190) + ',' + y1 + ' C' + (m.l + 320) + ',' + y1 + ' ' + (width - m.r - 320) + ',' + y2 + ' ' + (width - m.r - 190) + ',' + y2 + '" fill="none" stroke="rgba(36,107,206,.28)" stroke-width="' + sw + '"><title>' + esc(labels[links.source[i]] + ' → ' + labels[links.target[i]] + ': ' + value) + '</title></path>');
            }});
            left.forEach(([label, i]) => parts.push('<text x="' + m.l + '" y="' + (yFor(left, i) + 4) + '" font-size="12" fill="#172033">' + esc(label) + '</text>'));
            right.forEach(([label, i]) => parts.push('<text x="' + (width - m.r - 180) + '" y="' + (yFor(right, i) + 4) + '" font-size="12" fill="#172033">' + esc(label) + '</text>'));
            el.innerHTML = svg(parts);
            return Promise.resolve();
          }}
          const maxY = Math.max(10, ...traces.flatMap(t => t.y || []));
          const yMax = layout.yaxis?.range?.[1] || Math.ceil(maxY / 10) * 10;
          const parts = grid(yMax, '%');
          traces.forEach(trace => {{
            const pts = trace.y.map((value, i) => {{
              const x = sx(i);
              const y = m.t + plotH - (plotH * value / yMax);
              return [x, y, value];
            }});
            parts.push('<polyline fill="none" stroke="' + (trace.line?.color || '#246bce') + '" stroke-width="2.6" points="' + pts.map(p => p[0] + ',' + p[1]).join(' ') + '"><title>' + esc(trace.name) + '</title></polyline>');
          }});
          (traces[0]?.x || data.tickIds).forEach((key, i) => {{ if (i % 4 === 0 || i === data.tickIds.length - 1) parts.push('<text x="' + sx(i) + '" y="' + (m.t + plotH + 24) + '" text-anchor="middle" font-size="10" fill="#647084">' + esc(key.split('_')[0]) + '</text>'); }});
          traces.forEach((trace, i) => parts.push('<text x="' + (m.l + (i % 4) * 185) + '" y="' + (height - 36 + Math.floor(i / 4) * 16) + '" font-size="11" fill="' + (trace.line?.color || '#246bce') + '">■ ' + esc(trace.name) + '</text>'));
          el.innerHTML = svg(parts);
          return Promise.resolve();
        }}
      }};
    }}
    const layoutBase = {{
      paper_bgcolor: '#ffffff', plot_bgcolor: '#ffffff', font: {{family: 'Inter, Arial, sans-serif', color: '#172033'}},
      margin: {{l: 60, r: 24, t: 28, b: 70}}, hovermode: 'x unified',
      legend: {{orientation: 'h', y: -0.2}},
      xaxis: {{gridcolor: '#edf1f6', tickangle: -35}},
      yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%'}}
    }};
    const config = {{responsive: true, displaylogo: false, modeBarButtonsToRemove: ['lasso2d', 'select2d']}};
    function label(name) {{ return name.replaceAll('_', ' '); }}
    function valuesFor(keys, obj) {{ return keys.map(k => obj[k] || 0); }}
    function tracesFromSeries(series, keys) {{
      return keys.map(key => ({{
        type: 'scatter', mode: 'lines+markers', name: label(key), x: data.tickIds,
        y: series[key], line: {{width: 3, color: palette[key]}}, marker: {{size: 5}},
        customdata: data.tickDates, hovertemplate: '%{{customdata}}<br>' + label(key) + ': %{{y:.2f}}%<extra></extra>'
      }}));
    }}
    function barCompare(elementId, keys, first, second, firstName, secondName) {{
      Plotly.newPlot(elementId, [
        {{type: 'bar', name: firstName, x: keys.map(label), y: valuesFor(keys, first), marker: {{color: '#697386'}}}},
        {{type: 'bar', name: secondName, x: keys.map(label), y: valuesFor(keys, second), marker: {{color: keys.map(k => palette[k] || '#246bce')}}}}
      ], {{...layoutBase, barmode: 'group', yaxis: {{gridcolor: '#edf1f6', title: 'Agents'}}, legend: {{orientation: 'h', y: -0.24}}}}, config);
    }}
    function sankey(elementId, transitions, titlePrefix) {{
      const labels = [];
      const index = new Map();
      function idx(value, side) {{
        const text = side + ': ' + label(value);
        if (!index.has(text)) {{ index.set(text, labels.length); labels.push(text); }}
        return index.get(text);
      }}
      Plotly.newPlot(elementId, [{{
        type: 'sankey',
        arrangement: 'snap',
        node: {{label: labels, pad: 16, thickness: 16, color: labels.map(v => palette[v.split(': ')[1]?.replaceAll(' ', '_')] || '#8b95a5')}},
        link: {{
          source: transitions.map(t => idx(t.source, '2018')),
          target: transitions.map(t => idx(t.target, '2023')),
          value: transitions.map(t => t.value),
          color: 'rgba(36, 107, 206, 0.22)'
        }}
      }}], {{...layoutBase, title: {{text: titlePrefix, font: {{size: 14}}}}, margin: {{l: 12, r: 12, t: 36, b: 12}}}}, config);
    }}
    function heatmap(elementId, keys, field, finalTick) {{
      const z = data.archetypes.map(arch => keys.map(key => {{
        const series = data.archetypeSeries[arch][field][key];
        return +(series[data.tickIds.indexOf(finalTick)] - series[0]).toFixed(2);
      }}));
      Plotly.newPlot(elementId, [{{
        type: 'heatmap', x: keys.map(label), y: data.archetypes, z,
        colorscale: [[0, '#b4232a'], [0.5, '#fff7ed'], [1, '#246bce']],
        zmid: 0, colorbar: {{title: 'pp'}}, hovertemplate: '%{{y}}<br>%{{x}}: %{{z:.2f}} pp<extra></extra>'
      }}], {{...layoutBase, margin: {{l: 230, r: 40, t: 20, b: 80}}, yaxis: {{automargin: true}}}}, config);
    }}
    function table(elementId, rows, columns) {{
      const head = '<thead><tr>' + columns.map(c => '<th>' + c.label + '</th>').join('') + '</tr></thead>';
      const body = '<tbody>' + rows.map(row => '<tr>' + columns.map(c => '<td>' + (row[c.key] ?? '') + '</td>').join('') + '</tr>').join('') + '</tbody>';
      document.getElementById(elementId).innerHTML = head + body;
    }}
    function updateArchetype() {{
      const arch = document.getElementById('archetypeSelect').value;
      Plotly.react('archetypeCandidate', tracesFromSeries(data.archetypeSeries[arch].candidate, data.keys.candidates),
        {{...layoutBase, title: {{text: arch + ' candidate probability weights'}}, yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%', range: [0, 100]}}}}, config);
      Plotly.react('archetypeParty', tracesFromSeries(data.archetypeSeries[arch].party, data.keys.parties),
        {{...layoutBase, title: {{text: arch + ' party probability weights'}}, yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%', range: [0, 100]}}}}, config);
    }}
    function updateAgent() {{
      const id = document.getElementById('agentSelect').value;
      const agent = data.agentSeries[id];
      document.getElementById('agentMeta').innerHTML = '<p><strong>' + id + '</strong> · ' + agent.archetype + ' · ' + agent.city +
        ' · 2018: ' + label(agent.baseline_candidate) + ' / ' + label(agent.baseline_party) +
        ' · 2023: ' + label(agent.final_candidate) + ' / ' + label(agent.final_party) + '</p>';
      Plotly.react('agentCandidate', tracesFromSeries(agent.candidate, data.keys.candidates),
        {{...layoutBase, title: {{text: id + ' candidate probabilities'}}, yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%', range: [0, 100]}}}}, config);
      Plotly.react('agentParty', tracesFromSeries(agent.party, data.keys.parties),
        {{...layoutBase, title: {{text: id + ' party probabilities'}}, yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%', range: [0, 100]}}}}, config);
    }}
    function init() {{
      document.querySelectorAll('.pill').forEach(button => {{
        button.addEventListener('click', () => {{
          document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
          document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
          button.classList.add('active');
          document.getElementById(button.dataset.tab).classList.add('active');
          setTimeout(() => window.dispatchEvent(new Event('resize')), 20);
        }});
      }});
      document.getElementById('metrics').innerHTML = [
        ['Agents', data.meta.agents], ['Ticks', data.meta.ticks], ['First-round date', data.meta.firstRoundDate],
        ['Runoff date', data.meta.runoffDate], ['Erdogan 2018 to 2023', (data.counts.candidate2018.Erdogan || 0) + ' → ' + (data.counts.candidate2023.Erdogan || 0)],
        ['Kilicdaroglu 2023 top', data.counts.candidate2023.Kilicdaroglu || 0], ['AKP 2018 to 2023', (data.counts.party2018.AKP || 0) + ' → ' + (data.counts.party2023.AKP || 0)],
        ['CHP 2018 to 2023', (data.counts.party2018.CHP || 0) + ' → ' + (data.counts.party2023.CHP || 0)], ['Weighted Erdogan shift', (data.weighted.finalCandidate.Erdogan - data.weighted.initialCandidate.Erdogan).toFixed(1) + ' pp'],
        ['Weighted CHP shift', (data.weighted.finalParty.CHP - data.weighted.initialParty.CHP).toFixed(1) + ' pp']
      ].map(([k,v]) => '<div class="metric"><span>' + k + '</span><strong>' + v + '</strong></div>').join('');

      barCompare('candidateCounts', data.keys.candidates, data.counts.candidate2018, data.counts.candidate2023, '2018 baseline', '2023 first round');
      barCompare('partyCounts', data.keys.parties, data.counts.party2018, data.counts.party2023, '2018 baseline', '2023 simulated');
      sankey('candidateSankey', data.transitions.candidate, '2018 presidential baseline → 2023 first-round top choice');
      sankey('partySankey', data.transitions.party, '2018 party baseline → 2023 party top choice');
      Plotly.newPlot('aggregateProbabilities', [
        ...tracesFromSeries(Object.fromEntries(data.keys.candidates.map(k => [k, data.tickIds.map(t => data.aggregate.candidate[t][k])])), data.keys.candidates),
        ...tracesFromSeries(Object.fromEntries(data.keys.parties.slice(0, 6).map(k => [k, data.tickIds.map(t => data.aggregate.party[t][k])])), data.keys.parties.slice(0, 6)).map(t => ({{...t, visible: 'legendonly'}}))
      ], {{...layoutBase, yaxis: {{gridcolor: '#edf1f6', ticksuffix: '%', range: [0, 60]}}}}, config);

      const archSelect = document.getElementById('archetypeSelect');
      archSelect.innerHTML = data.archetypes.map(a => '<option>' + a + '</option>').join('');
      archSelect.addEventListener('change', updateArchetype);
      updateArchetype();
      heatmap('candidateHeatmap', data.keys.candidates, 'candidate', data.meta.firstRoundTick);
      heatmap('partyHeatmap', data.keys.parties, 'party', data.meta.runoffTick);

      const agentSelect = document.getElementById('agentSelect');
      agentSelect.innerHTML = Object.keys(data.agentSeries).sort().map(id => '<option>' + id + '</option>').join('');
      agentSelect.addEventListener('change', updateAgent);
      updateAgent();

      table('archetypeTable', data.archetypeRows, [
        {{key: 'archetype', label: 'Persona'}}, {{key: 'n', label: 'n'}},
        {{key: 'candidate_2018_top', label: '2018 pres. top'}}, {{key: 'candidate_2018_count', label: '2018 pres. n'}},
        {{key: 'candidate_2023_top', label: '2023 pres. top'}}, {{key: 'candidate_2023_count', label: '2023 pres. n'}},
        {{key: 'party_2018_top', label: '2018 party top'}}, {{key: 'party_2018_count', label: '2018 party n'}},
        {{key: 'party_2023_top', label: '2023 party top'}}, {{key: 'party_2023_count', label: '2023 party n'}},
        {{key: 'erdogan_probability_shift', label: 'Erdogan pp'}}, {{key: 'kilicdaroglu_probability_shift', label: 'Kilicdaroglu pp'}},
        {{key: 'akp_probability_shift', label: 'AKP pp'}}, {{key: 'chp_probability_shift', label: 'CHP pp'}}
      ]);
      table('candidateTransitionTable', data.transitions.candidate.slice(0, 40), [
        {{key: 'source', label: '2018 presidential'}}, {{key: 'target', label: '2023 first round'}}, {{key: 'value', label: 'agents'}}
      ]);
      table('partyTransitionTable', data.transitions.party.slice(0, 50), [
        {{key: 'source', label: '2018 party'}}, {{key: 'target', label: '2023 party'}}, {{key: 'value', label: 'agents'}}
      ]);
    }}
    init();
  </script>
</body>
</html>
"""


def main() -> None:
    DASHBOARD.write_text(html_document(build_data()), encoding="utf-8")
    print(DASHBOARD)


if __name__ == "__main__":
    main()
