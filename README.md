# Synthetic Turkey

Synthetic Turkey is a source-grounded LLM-agent simulation pipeline applied to the 2023 Turkish presidential election as a methodological test. It is not an election prediction model.

## Repository Purpose

This repository supports the Bachelor’s thesis and contains source code, configuration files, synthetic voter-agent files, saved outputs, analysis scripts, and reproducibility instructions for inspecting the reported run or launching a new run.

## Important Disclaimer

- The dataset is fully synthetic.
- No human-subject data are included.
- The saved output comes from the reported OpenAI baseline run.
- Live reruns may not reproduce identical values because LLM outputs can vary and provider model snapshots may change.
- This repository supports inspection and methodological reproducibility, not validated election prediction.

## Repository Structure

- `voter_source_of_truth/`: voter archetype definitions and the 2018 baseline sampling profile.
- `political_agent/`: political actor personas, broadcast frames, credibility matrix, and movement state machine.
- `events/`: raw 2018-2023 event timeline.
- `souls/`: 300 generated synthetic voter-agent JSON files.
- `db/`: saved belief and episodic memory archives.
- `outputs/`: canonical saved baseline outputs, generated figures, dashboards, and analysis tables.
- `logs/`: JSONL run logs and metrics summaries.
- `agents/`: citizen-agent and political-broadcast-agent logic.
- `simulation/`: tick engine, election-safe timeline expansion, parallel execution, resume handling.
- `llm/`: mock and OpenAI provider adapters.
- `memory/`: affective, belief, and episodic memory stores.
- `validation/`: output export and evaluation metrics.
- `scripts/`: soul generation, audits, chart generation, dashboards, and sensitivity analysis.
- `loaders/`: JSON/YAML config loading and validation.
- `docs/`: thesis notes, manuscript artifacts, and source literature.

## Data and Configuration

The repository includes 12 voter archetypes, 300 synthetic agents, a 2018 baseline sampling profile, 35 raw event ticks expanded to 37 processed ticks, controlled political broadcasts, a credibility matrix, memory and belief archives, and the output trajectory table.

The core configuration files are:

- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`
- `events/simulation_ticks.json`
- `political_agent/political_agents.yaml`
- `political_agent/political_personas.yaml`
- `political_agent/politician_event_responses.yaml`
- `political_agent/credibility_matrix.yaml`
- `political_agent/movement_state_machine.yaml`
- `actual_results_2023.yaml`
- `config.py`

## Reported Baseline Run

- Provider: OpenAI
- Model: `gpt-4o-mini`
- Temperature: `0.45`
- Token budget: `900`
- Population seed: `20230528`
- Agents: `300`
- Processed ticks: `37`
- Expected analytical output: `11,100` rows
- Primary output: `outputs/agent_trajectories.csv`

Main figures, tables, and audits are generated from `outputs/` by the scripts in `scripts/`, especially `section_d_fresh_audit.py`, `section_k_generate_charts.py`, `tie_handling_sensitivity.py`, and `analyze_simulation_results.py`.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## API Configuration

Copy the example environment file and add your own key:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
OPENAI_API_KEY=your_api_key_here
```

Never commit `.env`.

## How to Inspect the Reported Results

The saved thesis baseline can be inspected without rerunning OpenAI calls:

```bash
python3 scripts/section_d_fresh_audit.py
python3 scripts/section_k_generate_charts.py
python3 scripts/tie_handling_sensitivity.py
python3 scripts/analyze_simulation_results.py
```

These commands read existing files in `outputs/` and `souls/`. They do not call OpenAI.

If Matplotlib or fontconfig reports a non-writable cache directory, set a temporary cache path:

```bash
MPLCONFIGDIR=/private/tmp/matplotlib-syntetic-turkey python3 scripts/section_k_generate_charts.py
```

## How to Rerun the Simulation

First ensure the 300-agent baseline population exists or regenerate it:

```bash
python3 scripts/generate_souls_from_config.py --population-profile baseline_2018_300
```

The default runtime paths are `outputs/`, `logs/`, `db/`, and `outputs/broadcast_cache/`. A full rerun can overwrite saved output and memory files if those defaults are used. For thesis-safe reruns, use separate directories:

```bash
mkdir -p outputs/reruns/openai_baseline/broadcast_cache
mkdir -p logs/reruns/openai_baseline
mkdir -p db_reruns/openai_baseline

OUTPUTS_DIR=outputs/reruns/openai_baseline \
BROADCAST_CACHE_DIR=outputs/reruns/openai_baseline/broadcast_cache \
LOGS_DIR=logs/reruns/openai_baseline \
DB_DIR=db_reruns/openai_baseline \
NUM_AGENTS=300 \
python3 run.py \
  --provider openai \
  --population-profile baseline_2018_300 \
  --parallel-agents \
  --max-workers 5 \
  --continue-on-agent-error \
  --output-dir outputs/reruns/openai_baseline
```

Useful alternatives:

```bash
mkdir -p outputs/reruns/mock_smoke/broadcast_cache
mkdir -p logs/reruns/mock_smoke
mkdir -p db_reruns/mock_smoke

OUTPUTS_DIR=outputs/reruns/mock_smoke \
BROADCAST_CACHE_DIR=outputs/reruns/mock_smoke/broadcast_cache \
LOGS_DIR=logs/reruns/mock_smoke \
DB_DIR=db_reruns/mock_smoke \
python3 run.py --mock --max-agents 5 --max-ticks 5 --output-dir outputs/reruns/mock_smoke
```

Resume a compatible interrupted OpenAI run by adding the original log path:

```bash
OUTPUTS_DIR=outputs/reruns/openai_baseline \
BROADCAST_CACHE_DIR=outputs/reruns/openai_baseline/broadcast_cache \
LOGS_DIR=logs/reruns/openai_baseline \
DB_DIR=db_reruns/openai_baseline \
NUM_AGENTS=300 \
python3 run.py \
  --provider openai \
  --population-profile baseline_2018_300 \
  --parallel-agents \
  --max-workers 5 \
  --continue-on-agent-error \
  --resume-from-log logs/reruns/openai_baseline/run_2023_YYYYMMDD_HHMMSS.jsonl \
  --output-dir outputs/reruns/openai_baseline
```

`--continue-on-agent-error` records a low-confidence fallback row if an agent call fails after retries. `--parallel-agents` runs agents within a tick concurrently. `--max-workers` controls worker count.

## Expected Output

A successful 300-agent run with 37 processed ticks should produce:

- `outputs/agent_trajectories.csv`
- `11,100` data rows
- `outputs/aggregate_candidate_intention.csv`
- `outputs/aggregate_party_preference.csv`
- `outputs/reflections.jsonl`
- `outputs/broadcasts.jsonl`
- `outputs/evaluation_summary.json`
- run logs under `logs/`

If rerun directories are used, the same filenames are written under the selected output directory, while logs and memory files are written under the configured `LOGS_DIR` and `DB_DIR`.

## Using the Pipeline With Your Own Data

To adapt the pipeline, create or modify:

1. Voter archetype configuration.
2. Baseline sampling profile.
3. Event timeline.
4. Political actor configuration.
5. Credibility matrix.
6. Broadcast response frames.
7. Optional movement/state-machine configuration.
8. Output schema and analysis scripts if needed.

At a high level, archetypes need numeric worldview, emotion, media, and behaviour vectors. The baseline profile must map population counts to archetypes. The event timeline must include dated events. Candidate keys must match the JSON schema. Party and runoff keys must remain consistent across configs, prompts, validators, memory stores, and analysis scripts.

## Reproducibility Notes

Saved outputs reproduce the thesis analysis. Live OpenAI reruns may differ because completions are stochastic and model snapshots can change. The tie-handling Monte Carlo only measures uncertainty from tie-breaking inside a completed run. Repeated full runs would be needed to estimate run-to-run variance.

See `REPRODUCIBILITY.md` for a shorter verification checklist.

## Citation

If you use this repository, please cite:

Abdullah Kılınç, “Synthetic Turkey: A Source-Grounded Generative Agent-Based Simulation of the 2023 Turkish Presidential Election,” Bachelor’s thesis, Marmara University, 2026.
