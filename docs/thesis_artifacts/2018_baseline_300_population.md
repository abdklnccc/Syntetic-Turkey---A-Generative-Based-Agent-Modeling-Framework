# 2018 Baseline 300-Agent Population

Date prepared: 2026-05-16

## Purpose

This artifact documents the thesis-facing 300-agent electorate baseline for the Synthetic Turkey 2023 presidential election simulation. The change uses `voter_source_of_truth/2018_baseline_sampling_profile.yaml` as the population sampling frame while preserving the project rule that voter decisions are made by LLM reasoning, not deterministic vote rules.

## Source And Method

The source profile is `voter_source_of_truth/2018_baseline_sampling_profile.yaml`. It anchors the synthetic voter pool to the 24 June 2018 parliamentary and presidential election baseline using:

- `recommended_300_agent_party_distribution`
- `recommended_300_agent_presidential_distribution`
- `recommended_300_agent_party_to_archetype_matrix`
- `recommended_300_agent_archetype_totals`

`scripts/generate_souls_from_config.py --population-profile baseline_2018_300` expands the party-to-archetype matrix into 300 one-agent sampling rows. Each generated soul receives:

- a source archetype from `voter_source_of_truth/synthetic_turkey_simulation.json`
- a 2018 parliamentary party anchor
- a 2018 presidential vote anchor
- archetype-specific demographic assumptions with seeded variation
- initial party/candidate belief distributions used as starting state
- explicit metadata that the 2018 anchors are memory and sampling structure, not future vote rules

The generated souls were verified against the YAML profile:

- Party anchors: AKP 128, CHP 68, HDP_DEM 35, MHP 33, IYI 30, Other_small_parties 6
- Presidential anchors: Erdogan 158, Muharrem_Ince 92, Selahattin_Demirtas 25, Meral_Aksener 22, Temel_Karamollaoglu 3, Dogu_Perincek 0
- Archetype totals: A1 58, A2 32, A3 33, A4 19, A5 29, A6 30, A7 25, A8 18, A9 15, A10 14, A11 16, A12 11

## Why 300 Agents Instead Of 50

The original 50-agent prototype is useful for debugging, but it is too coarse for thesis calibration. One 50-agent voter equals 2 percentage points, which makes small blocs such as Saadet/Felicity-like voters, nationalist protest pathways, and cross-pressured Kurdish or conservative-disillusioned voters easy to lose.

At 300 agents, one voter equals about 0.33 percentage points. This is still not a statistically representative national sample, but it gives enough resolution to keep small and cross-pressured blocs visible while remaining feasible for local mock runs and manageable OpenAI calibration runs. A full 37-tick, 300-agent run requires about 11,100 voter-decision calls.

## LLM-First Boundary

The 2018 party and presidential anchors are persona memory. They are not deterministic 2023 vote rules.

The simulation may deterministically load configs, generate souls, construct prompts, filter broadcasts, validate JSON, maintain memory, aggregate outputs, and run mock mode. It must not deterministically force final 2023 voter choices from 2018 anchors. `agents/citizen_agent.py` includes the baseline memory in the voter prompt as historical grounding, and the voter decision schema still requires an LLM-style reasoning output over persona, memory, media exposure, event context, broadcasts, social context, affect, and uncertainty.

No deterministic voting rule was added in this work. A loader robustness fix was added so non-canonical duplicate copy files such as `agent_001 2.json` are ignored; this prevents stale local files from reducing the loaded agent count, but it does not affect voter reasoning.

## Verification Run Log

Commands run on 2026-05-16:

```bash
python3 scripts/generate_souls_from_config.py --population-profile baseline_2018_300
python3 -m unittest tests.test_2023_mvp
NUM_AGENTS=300 python3 run.py --mock --max-agents 10 --max-ticks 3
NUM_AGENTS=300 python3 run.py --mock
```

Verification evidence:

- Soul generation reported 300 `baseline_2018_300` souls in `souls/`.
- Direct YAML verification confirmed 300 files, 300 souls, `population_profile=baseline_2018_300`, matching party anchors, matching presidential anchors, matching archetype totals, and baseline memory/non-rule notes on every generated soul.
- Unit tests: 17 tests passed with `python3 -m unittest tests.test_2023_mvp`.
- Smoke mock: 10 agents x 3 ticks = 30 mock voter decisions.
- Full mock: 300 agents x 37 ticks = 11,100 mock voter decisions.
- Latest full mock log: `logs/run_2023_20260516_142653_179132.jsonl` with 37 `tick_start` entries, 11,100 `decision` entries, and one `evaluation_summary`.
- Output check: `outputs/agent_trajectories.csv` contains 11,100 rows, 300 unique agents, and 37 unique ticks.

Final full mock output summary:

- First round: Erdogan 35.694, Kilicdaroglu 44.409, Sinan_Ogan 7.681, Muharrem_Ince 1.961, Other 1.936, Undecided 8.319
- Runoff: Erdogan 51.397, Kilicdaroglu 37.874, Abstain_Invalid_Undecided 10.729
- First-round MAE: 4.874
- Runoff MAE: 5.394
- First-round ranking accuracy: false
- Runoff ranking accuracy: true

These are mock-mode diagnostics only. Mock mode is a local testing substitute and should not be presented as the research voter brain.

## Limitations

- The 300-agent population is a sampling frame, not a survey sample.
- Demographic details are archetype-specific simulation assumptions when the source configs do not provide exact distributions.
- The 2018 baseline anchors improve historical grounding but do not solve behavioral calibration by themselves.
- The current mock output still overstates Kilicdaroglu in the first round and should not be treated as a thesis result.
- `Dogu_Perincek` rounds to zero at N=300, matching the source profile guidance; explicit Vatan/Perincek representation would require higher N or weighted agents.
- Mock mode uses deterministic local heuristics and is only suitable for pipeline testing.

## Next Calibration Steps

- Run a real OpenAI pilot with a small slice, then compare against the mock pipeline for schema, leakage, and trajectory sanity.
- Review Ogan support by MHP/IYI/nationalist archetype and tune prompts or source-grounded persona memory only if a defensible behavioral reason is identified.
- Examine Kurdish voter trajectories around HDP closure, Green Left/YSP substitution, first-round result reveal, and runoff nationalist protocol events.
- Compare archetype-level first-round and runoff breakdowns against known 2023 behavior without forcing the aggregate result.
- Add thesis dashboard captures for the 300-agent run: candidate distribution, runoff distribution, archetype breakdown, turnout/abstention, emotion trajectories, and trust trajectories.
