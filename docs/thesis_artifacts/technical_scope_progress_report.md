# Synthetic Turkey Technical Scope And Progress Report

Generated on: 2026-05-16  
Updated on: 2026-05-22  
Project path: `/Users/abdullahkilinc/Desktop/syntetic-turkey`  
Current thesis artifact status: completed 300-agent OpenAI baseline run, dashboard generated, results ready for thesis interpretation with limitations. This file now also includes the post-run aggregation-method clarification and the political-broadcast persona method update.

## 1. One-Paragraph Summary

Synthetic Turkey is an LLM-first agent-based voter simulation for the 2023 Turkish presidential election. The system starts from a June 2018 post-election baseline, exposes synthetic voter agents to a 2018-2023 political event timeline, filters political broadcasts by persona and media credibility, preserves memory across ticks, and asks an LLM to update each voter's emotions, beliefs, reflections, and candidate-level vote intention. The current completed run uses 300 source-grounded synthetic voters, 37 election-safe ticks, and 11,100 OpenAI voter-decision calls. The system is technically runnable end-to-end, produces structured outputs and a dashboard, and should be treated in the thesis as an experimental simulation baseline rather than a validated election-prediction model.

## 2. Research Scope

The current MVP scope is the 2023 Turkish presidential election, not the 2024 local elections.

Research question:

Can LLM-based synthetic voter agents, grounded in realistic Turkish voter personas, historical events, political broadcasts, memory, and social context, approximate voting behavior in the 2023 Turkish presidential election?

Simulation window:

- Start: June 2018 post-election baseline.
- End: 28 May 2023 presidential runoff result reveal.
- Main comparison target: actual 2023 presidential first-round and runoff candidate vote distributions.

Core design principle:

- The LLM is the voter brain.
- Deterministic code is only the experiment harness: config loading, soul generation, prompt construction, event order, broadcast filtering, date fencing, JSON validation, memory storage, aggregation, mock mode, and evaluation.
- The code must not mechanically apply event deltas as vote rules.

## 3. Source-Of-Truth Files

The implementation uses JSON/YAML files as source of truth. Markdown files are explanatory references.

Voter sources:

- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/Synthetic-Turkey-Simulation-Framework.md`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`

Voter-persona provenance note:

- The intended ideal source for voter-soul construction would have been direct microdata or detailed crosstabs from sources such as TUIK and KONDA.
- Those detailed datasets were not available in this project because relevant data products are paid, restricted, or not easily accessible as open research microdata.
- Therefore, the 12 voter archetypes were built through a secondary research synthesis process using Perplexity deep research mode and then encoded into the local source-of-truth voter files.
- This makes the personas research-informed and plausible, but not statistically validated survey-derived profiles.
- In the thesis, Perplexity should be described as a research-assistant tool used to synthesize accessible public/secondary information, not as a substitute for licensed raw TUIK/KONDA data.

Political agent sources:

- `political_agent/political_agents.yaml`
- `political_agent/political_personas.yaml`
- `political_agent/credibility_matrix.yaml`
- `political_agent/politician_event_responses.yaml`
- `political_agent/movement_state_machine.yaml`
- `political_agent/synthetic_turkey_agent_configuration.md`

Event sources:

- `events/simulation_ticks.json`
- `events/Synthetic Turkey - LLM Voter Agent Simulation  Full Event Tick Timeline 2018-2023.md`

Evaluation source:

- `actual_results_2023.yaml`

Actual 2023 reference values in `actual_results_2023.yaml`:

| Election stage | Erdogan | Kilicdaroglu | Sinan Ogan | Muharrem Ince |
| --- | ---: | ---: | ---: | ---: |
| First round | 49.52 | 44.88 | 5.17 | 0.43 |
| Runoff | 52.18 | 47.82 | n/a | n/a |

## 4. Current Architecture

Runtime and orchestration:

- `run.py`: CLI entry point. Supports mock/OpenAI provider mode, max-agent/tick smoke runs, parallel agents, resume-from-log, social disabling, and terminal thought display.
- `simulation/tick_engine.py`: main event loop. Loads agents and ticks, inserts election-safe decision/result split ticks, runs all agents per tick, supports parallel execution, resume, logs, and output export.

Configuration:

- `config.py`: central paths, provider settings, runtime folders, OpenAI settings, date range, memory settings, and `.env` loading fallback.
- `loaders/config_loader.py`: robust JSON/YAML config loader. Loads voter config, political agents, political personas, credibility matrix, event responses, movement state machine, simulation ticks, actual results, and 2018 baseline sampling profile.

Population and souls:

- `scripts/generate_souls_from_config.py`: generates either the original `prototype_50` debug population or the thesis `baseline_2018_300` population.
- `souls/agent_001.json` through `souls/agent_300.json`: current canonical generated voter souls.
- `agents/soul_loader.py`: loads canonical soul JSON files and ignores duplicate non-canonical copies such as `agent_021 2.json`.

Voter agent:

- `agents/citizen_agent.py`: builds the LLM voter prompt, includes persona/state/memory/date fence/current event/broadcasts/social context, validates strict JSON, updates belief/emotion/memory state, and supports fallback decision recording if provider errors are allowed.
- `memory/affective_state.py`: affective state.
- `memory/beliefs.py`: party and candidate preference state.
- `memory/episodic.py`: persistent episodic memory records.

LLM provider:

- `llm/provider.py`: provider abstraction.
- `MockLLMProvider`: local no-API test provider.
- `OpenAIProvider`: real OpenAI calls with retry handling.
- Current configured model in `config.py`: `gpt-4o-mini`.
- Current temperature: `0.45`.
- Current max tokens per decision: `900`.

Political broadcasts:

- `agents/political_broadcast_agent.py`: loads political agent config, persona souls, and event response frames; can generate controlled LLM-written political broadcasts; and filters visibility by voter media diet, archetype credibility, event date, and relevant source.
- `political_agent/political_personas.yaml`: post-run persona-soul layer for political speakers. It describes each speaker's rhetorical identity, voice, speech patterns, and contextual guidance. The file is intended to generate paraphrased political broadcasts, not direct quotations.
- `outputs/broadcast_cache/`: cache location for generated political broadcasts, so repeated runs do not need to regenerate the same event-speaker messages.
- `outputs/broadcasts.jsonl`: exported broadcast records.

Metrics and dashboard:

- `validation/metrics.py`: exports trajectories, candidate distributions, party preferences, reflections, broadcasts, and evaluation summary.
- `scripts/build_results_dashboard.py`: builds static dashboard HTML.
- `outputs/synthetic_turkey_results_dashboard.html`: current dashboard.

Tests:

- `tests/test_2023_mvp.py`: regression tests for config loading, soul generation, soul loading, election-safe tick handling, provider fallback, and MVP behavior.

### 4.1 How A Voter Soul Becomes A Prompt

Each voter begins as a JSON soul file under `souls/`. A soul is not just a demographic row. It contains identity, biography, worldview variables, affective baseline, media diet, behavioral tendencies, 2018 baseline memory, and starting 2023 candidate probabilities.

At runtime, `agents/citizen_agent.py` turns the soul into a prompt. The prompt is rebuilt every tick and includes:

- Temporal fence: the agent must only know information available up to the simulated date.
- Role instruction: the model must role-play as the voter, not as a political analyst.
- Identity: age, gender, city, region, education, income, employment, archetype.
- Persona text: biography, political identity, worldview, media diet, social context.
- 2018 baseline memory: a remembered 2018 party/presidential vote anchor, explicitly not a future vote rule.
- Numeric grounding: political worldview, media diet, and behavioral variables.
- Current belief and affect state: candidate probabilities, party preference, trust, approval, turnout, emotions.
- Short episodic memory summary from previous ticks.
- Current historical event.
- Visible political broadcasts after media/credibility filtering.
- Visible peer social context if enabled.
- Required strict JSON output schema.

The LLM then returns a structured voter decision. Deterministic code only validates and stores the result. It clamps numeric values to valid ranges and normalizes probability distributions, but it does not choose the vote for the agent.

### 4.2 Example Abbreviated Voter Prompt

This is a shortened example based on `souls/agent_001.json`, a Devout Anatolian Loyalist from Kayseri. The real prompt is longer because it includes full JSON numeric profiles, event data, visible broadcasts, and the complete output schema.

```text
You are this synthetic voter. You only know information available up to
the current simulated date: 2023-05-14. Do not use future knowledge.
Stay consistent with your persona, but you may gradually change your views if events affect you.

ROLE
Role-play as the synthetic voter below, not as a political analyst.
Reason from their identity, social context, media diet, and memory.

IDENTITY
agent_id: agent_001
archetype: A1 - Devout Anatolian Loyalist
age: 47
gender: Male
city/region: Kayseri / Central Anatolia
education: primary
income: middle
employment: farmer

PERSONA
biography: Synthetic voter from Kayseri generated from the Devout Anatolian Loyalist archetype.
political identity: Grounded in source archetype A1.
worldview summary: Worldview variables are inherited from the source configuration with bounded variation.
media diet summary: Media exposure is inherited from the archetype media_diet vector and filtered per tick.
social context summary: Peer context is synthetic and concise; social influence is handled by LLM reasoning.

2018 BASELINE MEMORY
In the June 2018 baseline sampling frame, this synthetic voter is grounded as having
cast party vote: AKP; presidential vote: Erdogan. This is persona memory and
sampling structure, not a future vote rule.

NUMERIC GROUNDING
political_worldview:
  government_approval: high
  institutional_trust: high
  opposition_trust: low
  secular_religious: strongly religious
  nationalist_cosmopolitan: strongly nationalist
media_diet:
  pro_government_media: high
  local_family_networks: high
  opposition_media: low
behavioral_variables:
  partisan_strength: high
  openness_to_persuasion: low
  turnout_likelihood: high
  leader_loyalty: high

CURRENT STATE
first-round candidate lean=Erdogan; runoff lean=Erdogan;
party lean=AKP; turnout probability around 0.87.
anger/fear/hope/sadness/political_fatigue from current affective state.

SHORT MEMORY
- Previous reflections from recent ticks, such as inflation, earthquake response,
  opposition unity, or campaign events.

CURRENT EVENT
{
  "tick_id": "T030A_first_round_vote_decision",
  "date": "2023-05-14",
  "title": "First-round presidential vote decision",
  "category": "election",
  "summary": "The voter must decide before seeing the official result."
}

VISIBLE POLITICAL BROADCASTS
[
  {
    "agent_name": "Recep Tayyip Erdogan",
    "party_or_movement": "AKP",
    "paraphrased_message": "...",
    "tone": ["combative", "nationalist"],
    "credibility_score": 0.85,
    "likely_effect": "mobilize_base"
  }
]

VISIBLE PEER SOCIAL CONTEXT
- Short summaries from a few other synthetic voters, if social mode is enabled.

TASK
Return strict JSON only. No markdown, no commentary.
decision_kind: first_round_vote

Required schema:
{
  "reflection": "1-3 sentence first-person reflection",
  "government_approval": 1-10 number,
  "institutional_trust": 1-10 number,
  "opposition_trust": 1-10 number,
  "anger": 0-1 number,
  "fear": 0-1 number,
  "hope": 0-1 number,
  "sadness": 0-1 number,
  "political_fatigue": 0-1 number,
  "party_preference": {"AKP": number, "...": number},
  "first_round_vote_intention": {"Erdogan": number, "Kilicdaroglu": number, "...": number},
  "runoff_vote_intention": {"Erdogan": number, "Kilicdaroglu": number, "Abstain_Invalid_Undecided": number},
  "turnout_probability": 0-1 number,
  "reason_codes": ["short_code"],
  "confidence": "low|medium|high"
}
```

### 4.3 How Political Agents Worked In The 50-Agent And 300-Agent Runs

In the completed 50-agent debug runs and the completed 300-agent OpenAI baseline run, political actors were not independent LLM agents producing new speeches in real time. They worked as controlled broadcast sources.

The process was:

1. `simulation_ticks.json` selected the current historical tick.
2. `agents/political_broadcast_agent.py` mapped the tick to a response key in `politician_event_responses.yaml`.
3. `politician_event_responses.yaml` supplied short `message_frame` values, tones, target groups, expected effects, and vote-shift-direction labels.
4. `movement_state_machine.yaml` supplied dynamic Kurdish movement labels/states, such as HDP/YSP period context.
5. `credibility_matrix.yaml` and each voter's media diet filtered which broadcasts each voter plausibly saw.
6. The voter LLM reasoned from the visible broadcasts and decided how to update beliefs, emotion, memory, and candidate intention.

Therefore, in the completed 50- and 300-agent simulations:

- Voter decisions were LLM-first.
- Political broadcasts were source-grounded but mostly deterministic YAML message frames.
- Political actors did not yet have full LLM-generated event reactions.
- Broadcasts did not mechanically shift votes; they were prompt inputs for voter reasoning.

This design was useful for the first MVP because it kept the information environment controlled. However, it also made some campaign moments too generic or static, especially the runoff.

### 4.4 Recommended Future Political-Agent Method

For later runs, the recommended improvement is to make political communication more LLM-generated while preserving source control.

Recommended design:

1. Keep deterministic YAML as the harness:
   - Which political actors speak.
   - Which event they respond to.
   - Which voter groups are targeted.
   - What broad frame and constraints apply.

2. Give each political actor a persona soul:
   - Rhetorical identity.
   - Voice.
   - Speech patterns.
   - Event-specific guidance.
   - Temporal fence.

3. Ask an LLM political-agent generator to produce a short paraphrased broadcast:
   - Not a direct quote.
   - Not generic.
   - Event-specific.
   - Consistent with the actor's public style.

4. Cache the generated broadcasts:
   - Generate once per tick-speaker pair.
   - Reuse for all voters after filtering.
   - Keep cost manageable.

5. Keep voter choice LLM-first:
   - The political-agent LLM writes the message.
   - The voter-agent LLM decides whether it persuades, mobilizes, backfires, or is ignored.
   - No deterministic vote shift is applied.

This is the intended path toward "real LLM political agents" without turning the system into uncontrolled chatbot role-play. The important boundary is that political agents generate communication, not final voter behavior.

## 5. CLI Features Currently Available

Generate 300 thesis population:

```bash
python3 scripts/generate_souls_from_config.py --population-profile baseline_2018_300
```

Run mock simulation:

```bash
python3 run.py --mock
```

Run 300-agent OpenAI simulation:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error
```

Resume from a clean previous log:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error --resume-from-log logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

Show agent reflections in terminal for a small run:

```bash
python3 run.py --provider openai --max-agents 5 --max-ticks 3 --show-agent-thoughts
```

Build dashboard:

```bash
python3 scripts/build_results_dashboard.py
```

## 6. Population Baseline

The first MVP population had 50 voters. That was useful for debugging, but it was too coarse for thesis analysis because one agent represented 2 percentage points and small blocs disappeared.

The current thesis population uses `voter_source_of_truth/2018_baseline_sampling_profile.yaml`.

Recommended sample size:

- 300 agents.
- One agent is roughly 0.33 percentage points.
- 300 agents keeps smaller blocs more visible while keeping cost manageable.
- Full 37-tick OpenAI run costs 11,100 voter-decision calls.

2018 party anchors used for the 300-agent population:

| Party/bloc anchor | Agent count |
| --- | ---: |
| AKP | 128 |
| CHP | 68 |
| HDP_DEM | 35 |
| MHP | 33 |
| IYI | 30 |
| Other small parties | 6 |
| Total | 300 |

2018 presidential anchors used as persona memory:

| Candidate anchor | Agent count |
| --- | ---: |
| Erdogan | 158 |
| Muharrem Ince | 92 |
| Selahattin Demirtas | 25 |
| Meral Aksener | 22 |
| Temel Karamollaoglu | 3 |
| Dogu Perincek | 0 |
| Total | 300 |

Archetype totals:

| Archetype | Count |
| --- | ---: |
| Devout Anatolian Loyalist | 58 |
| Secular Urban Professional | 32 |
| Conservative Economically Disillusioned | 33 |
| Alevi-CHP Loyalist | 19 |
| Kurdish Political Voter | 29 |
| Nationalist Grey Wolf (MHP core) | 30 |
| Moderate Nationalist (IYI) | 25 |
| Pious Disillusioned Islamist | 18 |
| Young Urban Protest Voter | 15 |
| Earthquake Zone Loyalist | 14 |
| Retired Protest Voter | 16 |
| Cosmopolitan Liberal | 11 |
| Total | 300 |

Important modeling note:

The 2018 anchors are stored as baseline memory and persona grounding. They are not deterministic vote rules for 2023. Voters still reason through the 2018-2023 timeline via the LLM prompt.

### 6.1 Persona Data Limitation: No Direct TUIK/KONDA Microdata

The original research ambition was to generate voter souls from stronger empirical population data, ideally including TUIK demographic data and KONDA-style political/social survey distributions. In practice, detailed individual-level or highly granular cross-tabulated datasets from these sources were not available for this project because they are paid, restricted, or not published as open microdata.

Because of this limitation, the 12 voter archetypes should not be presented as a direct statistical sample of Turkish voters. Instead, they should be described as synthetic, research-informed archetypes. Perplexity deep research mode was used to help synthesize publicly accessible and secondary information about Turkish voter blocs, including material that reflects widely discussed KONDA/TUIK-style demographic and political patterns. That gave the personas a plausible empirical grounding, but it did not provide raw respondent-level data.

Thesis-safe interpretation:

- The personas are plausible synthetic voter archetypes.
- They are informed by secondary research and public demographic/political knowledge.
- They are not direct reconstructions of KONDA respondents or TUIK microdata.
- This limits claims of statistical representativeness.
- The simulation should therefore be framed as an exploratory LLM-agent method experiment, not as a survey-weighted election model.

Suggested thesis wording:

> The ideal design would generate voter agents from licensed survey microdata and official demographic microdata. However, detailed KONDA and TUIK datasets were not available as open data for this project. Therefore, the voter personas were constructed as synthetic archetypes using a secondary research synthesis process, supported by Perplexity deep research, and then encoded into JSON/YAML source files. This provides plausible sociopolitical grounding but remains a limitation: the agents are not statistically representative survey respondents.

## 7. Election Leakage Prevention

The event timeline includes real 2023 election results. To prevent leakage, the engine splits result ticks into decision-before-result and result-reveal-after-decision phases.

Election-safe tick handling:

- Process ordinary ticks through `T029`.
- Insert `T030A_first_round_vote_decision` so voters decide first-round preference before seeing actual first-round results.
- Reveal `T030B_first_round_result_revealed` only after first-round decisions are recorded.
- Process runoff campaign ticks `T031` through `T034`.
- Insert `T035A_runoff_vote_decision` so voters decide runoff preference before seeing actual runoff result.
- Reveal `T035B_final_result_revealed` only after runoff decisions are recorded.

The prompt also includes a temporal fence:

The voter only knows information available up to the current simulated date and must not use future knowledge.

## 8. What Has Been Built So Far

Completed implementation areas:

- Robust source config loading for voter, political agent, credibility, movement, timeline, baseline, and actual-result files.
- Soul generation from source config.
- Original 50-agent debug population support.
- Thesis 300-agent 2018 baseline support.
- Canonical soul loading from `souls/`.
- Duplicate non-canonical soul-copy protection.
- Candidate-level voting schema for first round and runoff.
- Party-level preference retention for background analysis.
- Election-safe timeline with no result leakage before decision ticks.
- LLM provider abstraction.
- OpenAI provider mode.
- Mock provider mode.
- Parallel agent execution per tick.
- Resume-from-log support for interrupted long runs.
- Provider-error fallback support, clearly marked when used.
- Controlled political broadcast generation from YAML message frames.
- Post-run political-broadcast persona method: political agents now have persona souls that can guide LLM-generated, paraphrased broadcasts while YAML still controls who speaks, when they speak, and which voter groups they target.
- Broadcast cache path support for generated political messages.
- Voter-specific broadcast filtering.
- Optional social context.
- Terminal output for per-agent thoughts.
- Metrics export.
- Static dashboard export.
- Thesis-facing artifact documentation.

## 9. What Was Tested

Unit test suite:

```bash
python3 -m unittest tests.test_2023_mvp
```

Latest verification:

- 18 tests ran.
- 18 tests passed.

Soul generation and population checks:

```bash
python3 scripts/generate_souls_from_config.py --population-profile baseline_2018_300
```

Verified:

- `souls/` contains 300 canonical `agent_*.json` files.
- All generated souls use `population_profile=baseline_2018_300`.
- Party anchor counts match `2018_baseline_sampling_profile.yaml`.
- Presidential anchor counts match `2018_baseline_sampling_profile.yaml`.
- Archetype totals match `2018_baseline_sampling_profile.yaml`.
- Baseline memory is present.
- Baseline anchors are documented as memory and not deterministic rules.

Mock smoke tests:

```bash
NUM_AGENTS=300 python3 run.py --mock --max-agents 10 --max-ticks 3
```

Verified:

- 10 agents.
- 3 ticks.
- 30 mock decisions.
- Simulation completes.

Full mock test:

```bash
NUM_AGENTS=300 python3 run.py --mock
```

Verified:

- 300 agents.
- 37 ticks.
- 11,100 mock decisions.
- Simulation completes and exports outputs.

OpenAI smoke test:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --max-agents 20 --max-ticks 5 --parallel-agents --max-workers 5 --continue-on-agent-error
```

Verified:

- 20 agents.
- 5 ticks.
- 100 OpenAI voter decisions.
- 0 provider-error fallbacks.
- Output quality was coherent enough to proceed to larger run.

OpenAI full-run attempt that failed due to quota:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error
```

Result:

- OpenAI quota exhausted at `T013`.
- Partial contaminated log: `logs/run_2023_20260516_144449_113733.jsonl`.
- That log had 3,632 decisions, 15 provider-error fallbacks, and 12 complete ticks plus partial `T013`.
- This run is not used as final thesis output.

Clean prefix extracted:

- `logs/run_2023_20260516_144449_clean_through_T012.jsonl`
- 3,600 clean decisions.
- 300 agents.
- Ticks `T001` through `T012`.
- 0 provider-error fallbacks.

OpenAI resumed full run:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error --resume-from-log logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

Result:

- Completed remaining ticks from `T013` through `T035B_final_result_revealed`.
- Latest resumed log: `logs/run_2023_20260516_165048_164535.jsonl`.
- 7,500 new OpenAI decisions in the resumed log.
- 0 provider-error fallbacks in the resumed log.
- Final exported outputs combine the clean prefix and resumed run into a complete 300-agent, 37-tick output set.

Dashboard build:

```bash
python3 scripts/build_results_dashboard.py
```

Verified:

- Dashboard file exists at `outputs/synthetic_turkey_results_dashboard.html`.
- It contains summary cards, SVG charts, tables, method notes, calibration priorities, and thesis interpretation sections.

## 10. Current Output Inventory

Core output files:

- `outputs/agent_trajectories.csv`
- `outputs/aggregate_candidate_intention.csv`
- `outputs/aggregate_party_preference.csv`
- `outputs/reflections.jsonl`
- `outputs/broadcasts.jsonl`
- `outputs/first_round_vote_distribution.json`
- `outputs/runoff_vote_distribution.json`
- `outputs/evaluation_summary.json`
- `outputs/synthetic_turkey_results_dashboard.html`

Current counts:

| File | Count |
| --- | ---: |
| `outputs/agent_trajectories.csv` | 11,100 data rows plus header |
| `outputs/reflections.jsonl` | 11,100 rows |
| `outputs/broadcasts.jsonl` | 115 rows |
| Canonical souls | 300 files |
| Unique agents in trajectories | 300 |
| Unique ticks in trajectories | 37 |
| Provider-error rows in final trajectories | 0 |

Run logs to preserve:

- `logs/run_2023_20260516_144449_clean_through_T012.jsonl`: clean prefix from T001-T012.
- `logs/run_2023_20260516_165048_164535.jsonl`: resumed OpenAI completion from T013-T035B.
- `logs/run_2023_20260516_144449_113733.jsonl`: quota-interrupted contaminated run, kept only as process evidence, not final thesis output.

## 11. Final OpenAI Result Summary

Raw final first-round distribution from `outputs/evaluation_summary.json`:

| Candidate/state | Simulated percent |
| --- | ---: |
| Erdogan | 41.539 |
| Kilicdaroglu | 49.133 |
| Sinan Ogan | 1.372 |
| Muharrem Ince | 0.000 |
| Other | 0.367 |
| Undecided | 7.589 |

Raw final runoff distribution:

| Candidate/state | Simulated percent |
| --- | ---: |
| Erdogan | 41.801 |
| Kilicdaroglu | 49.061 |
| Abstain/Invalid/Undecided | 9.138 |

Evaluation metrics:

| Metric | Value |
| --- | ---: |
| First-round MAE | 4.250 |
| Runoff MAE | 6.175 |
| First-round ranking accuracy | false |
| Runoff ranking accuracy | false |
| Mean turnout probability | 82.3 |
| Mean abstention probability | 17.7 |

Approximate valid-vote normalized comparison:

| Stage | Simulated Erdogan | Actual Erdogan | Simulated Kilicdaroglu | Actual Kilicdaroglu |
| --- | ---: | ---: | ---: | ---: |
| First round, valid major candidates | about 45.1 | 49.52 | about 53.4 | 44.88 |
| Runoff, excluding abstain/invalid/undecided | about 46.0 | 52.18 | about 54.0 | 47.82 |

Interpretation:

- The model moved in the right technical direction: it produced coherent agent-level decisions across 11,100 LLM calls without fallbacks in the final output.
- It preserved strong pro-government blocs such as Devout Anatolian Loyalists, MHP-core nationalists, and Earthquake Zone Loyalists.
- It captured opposition consolidation among secular, Alevi-CHP, Kurdish, young urban, and liberal archetypes.
- It still over-consolidates Kilicdaroglu and underestimates Erdogan in probability-weighted final candidate distributions.
- It strongly underproduces the Sinan Ogan first-round pathway.
- It treats Muharrem Ince as effectively zero after withdrawal, which is plausible directionally but lower than the official 0.43.
- It produces meaningful abstain/invalid/undecided runoff probability, especially relevant for Kurdish and fatigue dynamics, but this also complicates direct comparison to official valid-vote results.

### 11.1 Aggregation Method Clarification: Probability-Weighted Intention vs Top-Choice Ballot

The final result tables above use the probability-weighted candidate distributions exported by `validation/metrics.py`. This is an important methodological detail. Each voter agent does not output only one candidate; it outputs a probability distribution over candidates. The evaluation summary averages those probabilities across all agents.

For example, if one voter outputs:

```json
{
  "Erdogan": 0.58,
  "Kilicdaroglu": 0.25,
  "Undecided": 0.17
}
```

the probability-weighted method counts this as:

- 0.58 Erdogan voter-equivalents.
- 0.25 Kilicdaroglu voter-equivalents.
- 0.17 undecided voter-equivalents.

The top-choice ballot method would instead count the same agent as:

- 1 Erdogan vote.

This distinction explains an apparent contradiction in the report. The archetype table below shows that more agents have Erdogan as their top candidate, yet the exported probability-weighted distribution gives Kilicdaroglu a higher total score.

Final first-round decision tick, `T030A_first_round_vote_decision`:

| Aggregation method | Erdogan | Kilicdaroglu | Sinan Ogan | Other/undecided |
| --- | ---: | ---: | ---: | ---: |
| Top-choice agent count | 164 agents | 136 agents | 0 agents | 0 agents |
| Top-choice percent of agents | 54.7 | 45.3 | 0.0 | 0.0 |
| Probability-weighted voter-equivalents | 124.62 | 147.40 | 4.12 | 23.87 |
| Probability-weighted percent | 41.539 | 49.133 | 1.372 | 7.956 |

Final runoff decision tick, `T035A_runoff_vote_decision`:

| Aggregation method | Erdogan | Kilicdaroglu | Abstain/invalid/undecided |
| --- | ---: | ---: | ---: |
| Top-choice agent count | 166 agents | 133 agents | 1 agent |
| Top-choice percent of agents | 55.3 | 44.3 | 0.3 |
| Probability-weighted voter-equivalents | 125.40 | 147.18 | 27.41 |
| Probability-weighted percent | 41.801 | 49.061 | 9.138 |

Why this happens:

- Erdogan has more top-choice agents.
- But many Erdogan-leading agents express uncertainty, giving some probability mass to Kilicdaroglu, Ogan, or undecided.
- Kilicdaroglu-leading agents are more concentrated and give almost no probability mass back to Erdogan.
- Therefore, Erdogan wins the top-choice count, while Kilicdaroglu wins the probability-weighted score.

This is not a data error. It is an aggregation-method difference.

For thesis reporting, both views should be shown:

- Top-choice ballot result: closer to an election-like one-agent-one-vote interpretation.
- Probability-weighted intention result: useful for measuring hesitation, uncertainty, and latent preference.

Recommended thesis wording:

> The simulation produced two analytically distinct election summaries. Under a top-choice ballot interpretation, Erdogan had more final first-round and runoff supporters. Under the probability-weighted intention interpretation used by the metrics module, Kilicdaroglu received more aggregate probability mass because pro-Erdogan agents expressed more uncertainty. This reveals a methodological fragility: simulation conclusions depend on whether LLM outputs are interpreted as final ballots or as probabilistic voter intentions.

## 12. Archetype-Level Final Pattern

Top candidate counts from `outputs/evaluation_summary.json`:

| Archetype | Count | First-round top pattern | Runoff top pattern |
| --- | ---: | --- | --- |
| Devout Anatolian Loyalist | 58 | 58 Erdogan | 58 Erdogan |
| Conservative Economically Disillusioned | 33 | 32 Erdogan, 1 Kilicdaroglu | 33 Erdogan |
| Nationalist Grey Wolf (MHP core) | 30 | 30 Erdogan | 30 Erdogan |
| Earthquake Zone Loyalist | 14 | 14 Erdogan | 14 Erdogan |
| Pious Disillusioned Islamist | 18 | 16 Erdogan, 2 Kilicdaroglu | 16 Erdogan, 2 Kilicdaroglu |
| Retired Protest Voter | 16 | 8 Erdogan, 8 Kilicdaroglu | 8 Erdogan, 8 Kilicdaroglu |
| Moderate Nationalist (IYI) | 25 | 6 Erdogan, 19 Kilicdaroglu | 7 Erdogan, 18 Kilicdaroglu |
| Secular Urban Professional | 32 | 32 Kilicdaroglu | 32 Kilicdaroglu |
| Alevi-CHP Loyalist | 19 | 19 Kilicdaroglu | 19 Kilicdaroglu |
| Kurdish Political Voter | 29 | 29 Kilicdaroglu | 28 Kilicdaroglu, 1 abstain/invalid/undecided |
| Young Urban Protest Voter | 15 | 15 Kilicdaroglu | 15 Kilicdaroglu |
| Cosmopolitan Liberal | 11 | 11 Kilicdaroglu | 11 Kilicdaroglu |

This pattern is useful for thesis analysis because it shows where the simulation behaves credibly and where calibration is still weak.

Most important calibration gaps:

- Ogan pathway is too weak among nationalist voters.
- Kilicdaroglu consolidation is too strong among moderate opposition and some cross-pressured groups.
- Erdogan resilience in the final distribution remains too low, despite loyalist archetypes staying aligned.
- Numeric emotion and trust trajectories appear flatter than the reflections suggest.
- Some `reason_codes` are generic, such as `short_code`, which limits later qualitative coding.

## 13. Output Quality Assessment

Strengths:

- End-to-end run completed with real OpenAI decisions.
- Final output has 0 provider-error fallback rows.
- Voter reflections are generally coherent and event-aware.
- Personas maintain broad ideological consistency over time.
- The event split prevents election result leakage before vote decisions.
- Broadcast generation is controlled by source YAML rather than free-form politician agents.
- The dashboard makes results explainable for a thesis supervisor.
- The 300-agent baseline is much more defensible than the earlier 50-agent debug population.

Weaknesses:

- The 12 voter personas are synthetic archetypes informed by secondary research, not direct profiles generated from licensed TUIK/KONDA microdata.
- This is a single full OpenAI run, not a multi-seed statistical experiment.
- The simulation is expensive and took about 8 hours, so uncertainty intervals are not available from repeated runs.
- The result is not calibrated enough to claim strong predictive accuracy.
- Candidate ranking is wrong in both first round and runoff under the probability-weighted metric. Under the top-choice ballot interpretation, Erdogan has more final first-round and runoff top-choice agents.
- Ogan support is especially under-modeled.
- Some small-party and cross-pressured voter behavior remains underrepresented.
- Numeric states are less dynamic than natural-language reflections.
- The model should be framed as a research prototype and methodological experiment.

## 14. Political Broadcast Persona Method Update

This section merges the post-run political-broadcast persona method into the main technical report. It documents a methodological correction made after analyzing the completed 300-agent OpenAI baseline run.

### 14.1 Why This Change Was Needed

The completed run showed that the voter-agent layer was technically functional, but the political-information environment was too static in key moments. The most serious case was the runoff period. The real 2023 runoff campaign included several distinct political shocks:

- Kilicdaroglu's nationalist and anti-refugee turn.
- Sinan Ogan's endorsement of Erdogan.
- The Kilicdaroglu-Umit Ozdag protocol.
- Kurdish voter reluctance and turnout anxiety after the protocol.
- Erdogan's targeted nationalist consolidation messaging.

In the baseline run, the runoff communication environment was not differentiated enough. This limited the ability of voter agents to reason through the inter-round dynamics that mattered in the real election.

The correction introduces political-agent persona souls so that political broadcasts can be generated by an LLM in the style of each political actor while still remaining constrained by source YAML files.

### 14.2 Design Principle

The change preserves the LLM-first voter rule.

The political broadcast layer is still part of the experiment harness. It does not deterministically shift votes. It only creates the information environment that voter agents may see.

The revised method has three layers:

1. Structured YAML control:
   - Defines which political actors exist.
   - Defines who broadcasts at which event.
   - Defines message frames, target voter groups, expected effects, and credibility.

2. Political persona souls:
   - Define rhetorical identity, voice, speech patterns, and contextual guidance.
   - Help the LLM generate less generic political messages.
   - Do not reproduce real speeches or direct quotations.

3. Voter-side reasoning:
   - Broadcasts are filtered by media diet and credibility.
   - Voter agents receive only plausible visible messages.
   - The voter LLM decides how to react.

### 14.3 New Political Persona Source File

New file:

- `political_agent/political_personas.yaml`

It contains persona entries for 11 political speakers:

- Recep Tayyip Erdogan
- Kemal Kilicdaroglu
- Ekrem Imamoglu
- Devlet Bahceli
- Meral Aksener
- HDP/YSP/DEM Kurdish movement collective voice
- Selahattin Demirtas
- Pervin Buldan
- Mithat Sancar
- Sirri Sureyya Onder
- Sinan Ogan

Each persona includes:

- `display_name`
- `role`
- `rhetorical_identity`
- `voice`
- `speech_patterns`
- `contextual_guidance`

Important limitation:

These political persona souls are expert-coded rhetorical summaries for simulation purposes. They should not be described as validated discourse models or as reproductions of real speeches. They are intended to guide paraphrased, plausible, short political broadcasts.

### 14.4 Code Changes

| File | Change | Purpose |
| --- | --- | --- |
| `political_agent/political_personas.yaml` | New persona-soul file | Gives each political speaker a rhetorical style guide |
| `config.py` | Added `POLITICAL_PERSONAS_FILE` and `BROADCAST_CACHE_DIR` | Makes persona file and broadcast cache configurable |
| `loaders/config_loader.py` | Added `political_personas` to `ConfigBundle` | Loads political personas with other source configs |
| `agents/political_broadcast_agent.py` | Added persona prompt construction, LLM broadcast generation, cache, and `llm_generated` field | Converts static message frames into LLM-generated political broadcasts |
| `simulation/tick_engine.py` | Passes active provider into `PoliticalBroadcastAgent` | Allows broadcast generation to use mock or OpenAI provider |
| `llm/provider.py` | Mock provider supports `schema_name == "political_broadcast"` | Allows local smoke tests without API calls |

### 14.5 Broadcast Prompt Method

For each active broadcaster, `agents/political_broadcast_agent.py` builds a prompt containing:

- Speaker identity.
- Event date.
- Event title and summary.
- Persona rhetorical identity.
- Voice and speech patterns.
- Communication profile from `political_agents.yaml`.
- Target voter groups and intended effect from `politician_event_responses.yaml`.
- Kurdish movement state when relevant.
- Temporal fence requiring only information available up to the event date.

The LLM is instructed to return strict JSON:

```json
{
  "message": "2-3 sentence broadcast",
  "emotional_tone": ["tone1", "tone2"],
  "vote_shift_direction": "direction"
}
```

The generated message is then passed into the existing voter-specific filtering system.

### 14.6 Broadcast Cache

Generated political broadcasts are cached in:

- `outputs/broadcast_cache/`

The current cache key format is:

```text
tick_id::agent_id
```

This reduces cost because the same political message does not need to be regenerated for every voter. In a 300-agent run, a broadcast should be generated once per event-speaker pair, then reused after filtering.

Current limitation:

The cache key does not yet include a hash of the persona YAML, response YAML, model, temperature, or prompt template. If the persona or response configs change, old cached messages may remain valid by filename but invalid by method. Before a new serious OpenAI run, cache versioning or manual cache clearing should be used.

### 14.7 What Works Right Now

Verified current state:

- `load_all_configs()` loads successfully.
- `political_personas.yaml` contains 11 persona entries.
- `political_agents.yaml` contains 16 configured political agents.
- `politician_event_responses.yaml` contains 17 event response keys.
- The broadcast agent can be constructed with the mock provider.
- The mock provider returns valid JSON for `schema_name == "political_broadcast"`.
- Existing response keys still produce broadcasts.

The architecture is therefore conceptually sound, but some wiring is incomplete.

### 14.8 Critical Current Problem: Runoff Keys Are Mapped But Missing

The current `TICK_RESPONSE_MAP` in `agents/political_broadcast_agent.py` maps runoff ticks to distinct response keys:

```python
"T031": "E10A_runoff_kilicdaroglu_nationalist_pivot",
"T032": "E10B_runoff_ogan_endorses_erdogan",
"T033": "E10C_runoff_ozdag_protocol_signed",
"T034": "E10D_runoff_kurdish_reluctance",
"T035A_runoff_vote_decision": "E10D_runoff_kurdish_reluctance",
```

This is the correct design direction, but those event keys are not currently present in `political_agent/politician_event_responses.yaml`.

Current verified broadcast counts under the new mapping:

| Tick | Mapped response key | Current broadcast count |
| --- | --- | ---: |
| T031 | `E10A_runoff_kilicdaroglu_nationalist_pivot` | 0 |
| T032 | `E10B_runoff_ogan_endorses_erdogan` | 0 |
| T033 | `E10C_runoff_ozdag_protocol_signed` | 0 |
| T034 | `E10D_runoff_kurdish_reluctance` | 0 |
| T035A | `E10D_runoff_kurdish_reluctance` | 0 |
| T035B | `E10_2023_presidential_runoff` | 8 |

This means the intended runoff correction is only half implemented. The Python code points to differentiated runoff events, but the YAML source file does not yet define them. A new full OpenAI run should not be started until this is fixed, because `T031` through `T035A` would currently have no runoff broadcasts.

### 14.9 Sinan Ogan Is Still Not Fully Operational

The persona file includes `ogan_sinan`, but the rest of the political-agent pipeline does not yet fully activate him.

Current gaps:

- `ogan_sinan` is not configured in `political_agents.yaml`.
- `ogan_sinan` does not appear in `politician_event_responses.yaml`.
- `ogan_sinan` does not have a row in `credibility_matrix.yaml`.
- No dedicated voter archetype currently represents an ATA/Ogan nationalist protest voter.

This matters because the first full OpenAI run strongly underproduced Ogan support. A persona alone is not enough. To model the Ogan pathway, the system needs:

- A Sinan Ogan political-agent entry.
- Credibility scores by voter archetype.
- A `T032` event response where Ogan endorses Erdogan.
- Voter souls capable of making Ogan their first-round top choice.

### 14.10 Broadcast Fallback Auditing Risk

If LLM broadcast generation fails, the code falls back to the YAML `message_frame`. This is useful for robustness, but the exported audit field is currently too simple.

Current risk:

- The output uses `llm_generated` based mainly on whether a provider exists.
- If a provider exists but generation fails and the system falls back to YAML, the output could be misleading.

Recommended improvement:

```json
{
  "generation_source": "llm | cache | yaml_fallback",
  "generation_error": null
}
```

This would make the broadcast output more defensible in the thesis.

### 14.11 Recommended Fix Order Before Any New Full Run

Priority 1: add missing runoff YAML blocks:

- `E10A_runoff_kilicdaroglu_nationalist_pivot`
- `E10B_runoff_ogan_endorses_erdogan`
- `E10C_runoff_ozdag_protocol_signed`
- `E10D_runoff_kurdish_reluctance`

Priority 2: fully add Sinan Ogan:

- Add `ogan_sinan` to `political_agents.yaml`.
- Add credibility matrix scores.
- Add him to `T032` responses.
- Add or adapt voter population support for an Ogan pathway.

Priority 3: improve broadcast audit fields:

- Replace or supplement `llm_generated` with `generation_source`.
- Log fallback errors.

Priority 4: improve cache versioning:

- Include a hash of persona YAML, response YAML, prompt template, model, and temperature.

Priority 5: add regression tests:

- Assert `T031`, `T032`, `T033`, `T034`, and `T035A` each emit at least one broadcast.
- Assert `T032` includes `ogan_sinan`.
- Assert failed LLM generation is marked as fallback.
- Assert mock provider can generate political-broadcast JSON.

### 14.12 Thesis Interpretation

Suggested wording:

> After analyzing the first full 300-agent run, I found that the voter agents were technically coherent but the runoff information environment was too static. The simulation treated several distinct runoff events as if they had the same political message environment. To correct this, I introduced a political-agent persona layer. Political actors now have rhetorical persona souls, while YAML files still control who speaks, when they speak, and which voter groups are targeted. The LLM generates short paraphrased broadcasts in the actor's style, and voters receive only messages that pass credibility and media-diet filtering. This preserves the LLM-first design because voter decisions are still made by voter-agent reasoning, not deterministic vote shifts. The next required fix is to complete the missing runoff YAML event blocks and fully add Sinan Ogan as an active political agent.

Current status:

- The persona-broadcast architecture is a strong methodological improvement.
- It is partially implemented.
- It is not yet ready for a new expensive OpenAI run because the differentiated runoff YAML blocks are missing.

## 15. How To Use This In The Thesis

Recommended framing:

- Present the project as a method-building thesis, not as an election forecast.
- Treat the 300-agent OpenAI run as a full baseline experiment.
- Be transparent that the voter archetypes were created from secondary research synthesis rather than direct paid TUIK/KONDA microdata.
- Emphasize that the result is technically complete and empirically evaluable.
- Explain that the model approximates some bloc-level behavior but fails on final aggregate ranking.
- Use the mismatch as a research finding: LLM-first synthetic voters can produce coherent political reasoning but still require careful calibration and validation to approximate polarized electoral outcomes.

Suggested thesis claims that are defensible:

- A source-grounded LLM voter simulation can be built end-to-end using personas, events, broadcasts, memory, social context, and date fencing.
- The system can run at thesis-scale with 300 agents and 37 ticks.
- The 12 voter archetypes are plausible synthetic profiles informed by secondary research, but they are not statistically representative survey-derived personas.
- The final run produced 11,100 structured voter decisions with no provider fallbacks.
- Agent-level qualitative output is useful for interpreting why blocs move or remain stable.
- Aggregate outputs are not yet accurate enough for prediction claims.
- The model overestimates opposition consolidation under probability-weighted aggregation and underestimates nationalist third-candidate behavior.

Suggested thesis language to avoid:

- Do not claim that the model predicts the 2023 election.
- Do not claim that the 300 agents are statistically representative of all Turkish voters.
- Do not claim that the voter souls were generated directly from raw TUIK or KONDA microdata.
- Do not claim causal effects from individual events unless supported by additional analysis.
- Do not hide the fact that this is one full run.

## 16. Files Added Or Changed During The Build

Important implementation files:

- `config.py`: added paths, OpenAI settings, `.env` fallback, runtime settings.
- `loaders/config_loader.py`: added strict JSON/YAML config loading.
- `political_agent/political_personas.yaml`: added post-run political-agent persona souls for LLM-generated, paraphrased broadcasts.
- `scripts/generate_souls_from_config.py`: added config-based soul generation and `baseline_2018_300`.
- `agents/soul_loader.py`: loads all canonical JSON souls and ignores duplicate copy files.
- `agents/citizen_agent.py`: added new soul schema support, LLM-first prompt, strict JSON decision schema, validation, memory update, fallback decision path.
- `agents/political_broadcast_agent.py`: controlled broadcast generation, persona-guided LLM broadcast generation, broadcast caching, and voter-level filtering.
- `llm/provider.py`: provider abstraction, OpenAI provider, mock provider, retries.
- `simulation/tick_engine.py`: event loop, election-safe tick plan, parallel agents, resume, logging.
- `memory/beliefs.py`: candidate-level and party-level preference handling.
- `memory/affective_state.py`: affective variables.
- `memory/episodic.py`: memory storage and retrieval.
- `validation/metrics.py`: output exports and evaluation metrics.
- `scripts/build_results_dashboard.py`: dashboard generator.
- `run.py`: CLI flags for mock/OpenAI, parallelism, resume, thoughts, social disabling.
- `README.md`: setup, run commands, scope, outputs, limitations.
- `requirements.txt`: dependency list.
- `tests/test_2023_mvp.py`: regression tests.

Important thesis artifacts:

- `docs/goal.md`: long-running Codex goal instructions.
- `docs/thesis_artifacts/2018_baseline_300_population.md`: population method and verification.
- `docs/thesis_artifacts/300_agent_openai_run.md`: OpenAI validation and quota issue.
- `docs/thesis_artifacts/300_agent_openai_partial_quality_analysis.md`: clean prefix quality and resume recommendation.
- `docs/thesis_artifacts/300_agent_openai_final_run.md`: final run report.
- `docs/thesis_artifacts/300_agent_openai_dashboard_interpretation.md`: dashboard interpretation.
- `docs/thesis_artifacts/political_broadcast_persona_method_report.md`: earlier standalone persona-broadcast report, now merged into this consolidated report.
- `docs/thesis_artifacts/technical_scope_progress_report.md`: this consolidated report.

## 17. Current Project State

The project is at a usable thesis-baseline stage.

Current completed state:

- 300 canonical souls exist.
- Full OpenAI output exists.
- Dashboard exists.
- Unit tests pass.
- Final output has no provider-error fallbacks.
- The completed 300-agent baseline output is technically ready to be analyzed and written up.
- The post-run political-broadcast persona architecture is partially implemented but should not be used for a new expensive OpenAI run until the missing runoff YAML response blocks are added.

The project is not yet at a fully calibrated predictive stage.

Most useful next work, if more development is possible:

- Improve nationalist/Ogan modeling.
- Complete the missing `E10A`-`E10D` runoff broadcast response blocks.
- Fully wire `ogan_sinan` as a political agent with credibility scores and event responses.
- Improve cross-pressured AKP-to-opposition and opposition-to-Erdogan behavior.
- Improve numeric affect/trust dynamics so they respond more visibly to event content.
- Replace generic `reason_codes` with a controlled reason-code taxonomy.
- Add a cheaper calibration workflow using small OpenAI runs before any future full run.
- Add weighted-agent or post-stratification analysis so the same expensive run can be analyzed more flexibly.
- Add reflection-level qualitative coding for thesis chapters.

## 18. Reproducibility Checklist

Before reproducing the current full experiment:

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Set OpenAI key in `.env` or environment:

```bash
export OPENAI_API_KEY=...
```

3. Generate 300 souls:

```bash
python3 scripts/generate_souls_from_config.py --population-profile baseline_2018_300
```

4. Run unit tests:

```bash
python3 -m unittest tests.test_2023_mvp
```

5. Run a small smoke test first:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --max-agents 20 --max-ticks 5 --parallel-agents --max-workers 5 --continue-on-agent-error
```

6. If using the post-run political-broadcast persona architecture, verify runoff broadcast wiring before any full run:

```bash
python3 - <<'PY'
from loaders.config_loader import load_all_configs
from agents.political_broadcast_agent import PoliticalBroadcastAgent
from llm.provider import MockLLMProvider

bundle = load_all_configs()
broadcaster = PoliticalBroadcastAgent(bundle, provider=MockLLMProvider())
for tick in bundle.simulation_ticks:
    if tick["tick_id"] in {"T031", "T032", "T033", "T034"}:
        print(tick["tick_id"], len(broadcaster.broadcasts_for_tick(tick)))
print("T035A", len(broadcaster.broadcasts_for_tick({
    "tick_id": "T035A_runoff_vote_decision",
    "date": "2023-05-28",
    "title": "Runoff presidential vote decision",
})))
PY
```

All five printed counts should be greater than zero before a new serious OpenAI run.

7. Run full OpenAI experiment only after smoke success:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error
```

8. If quota or connection fails, resume only from a clean log with 0 provider-error rows.

9. Rebuild dashboard:

```bash
python3 scripts/build_results_dashboard.py
```

## 19. Final Thesis Position

This project has reached the point where it can support a thesis chapter on method design, implementation, and baseline evaluation. The strongest contribution is not that the system perfectly reproduces the 2023 election. The strongest contribution is that it demonstrates a full LLM-first simulation pipeline with source-grounded personas, event exposure, political broadcast filtering, memory, date fencing, structured outputs, and empirical comparison against real election results.

The final result should be written honestly:

- The simulation is technically complete.
- The agent behavior is qualitatively interpretable.
- The aggregate result is imperfect.
- The mismatch reveals where LLM-based political simulations need calibration, validation, and careful sampling.

That is a valid thesis result because the failure modes are measurable, explainable, and connected to the research question.
