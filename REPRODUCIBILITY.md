# Reproducibility Notes

This repository supports two different reproducibility tasks.

## Reproduce the Saved Thesis Analysis

Use the committed saved outputs. This does not require OpenAI API calls.

```bash
python3 scripts/section_d_fresh_audit.py
python3 scripts/section_k_generate_charts.py
python3 scripts/tie_handling_sensitivity.py
python3 scripts/analyze_simulation_results.py
```

The key saved file is `outputs/agent_trajectories.csv`.

If Matplotlib or fontconfig reports a non-writable cache directory while generating figures, set `MPLCONFIGDIR` to a writable temporary directory, for example `/private/tmp/matplotlib-syntetic-turkey`.

To verify the reported panel shape:

```bash
awk -F, 'NR==1 {print NF}' outputs/agent_trajectories.csv
awk -F, 'END {print NR-1}' outputs/agent_trajectories.csv
```

Expected values:

- Columns: `38`
- Data rows: `11100`

## Rerun the Simulation

Rerunning the pipeline requires an OpenAI API key in `.env`:

```bash
cp .env.example .env
```

Use separate rerun directories to avoid overwriting the saved thesis baseline:

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

## Why Exact Numerical Reproduction Is Not Guaranteed

The saved output reproduces the thesis analysis. A live OpenAI rerun generates a new run, not a bitwise replay. Outputs may differ because LLM sampling is stochastic, upstream model snapshots can change, and long multi-agent runs compound small generation differences over ticks.

The tie-handling sensitivity script estimates uncertainty from tie-breaking within the saved completed run. It does not measure full run-to-run variance. Estimating run-to-run variance would require repeated complete simulation runs.
