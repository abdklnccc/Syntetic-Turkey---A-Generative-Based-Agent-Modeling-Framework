# Synthetic Turkey Cleanup Report

This report records the GitHub-preparation cleanup for `/Users/abdullahkilinc/Desktop/syntetic-turkey` on 2026-06-12.

## Cleanup Policy

Protected thesis-critical data were not deleted or rewritten unless the user explicitly narrowed the scope. The canonical saved simulation output was preserved:

- `outputs/agent_trajectories.csv`
- 11,100 data rows
- 38 columns
- 300 voter souls in `souls/`
- 37 processed election-safe ticks from 35 raw event ticks

## A. Must Keep for Reproducibility

- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`
- `events/simulation_ticks.json`
- `political_broadcast_config/political_agents.yaml`
- `political_broadcast_config/political_personas.yaml`
- `political_broadcast_config/politician_event_responses.yaml`
- `political_broadcast_config/credibility_matrix.yaml`
- `political_broadcast_config/movement_state_machine.yaml`
- `souls/agent_001.json` through `souls/agent_300.json`
- `db/*_beliefs_2023.json`
- `db/*_episodic_2023.json`
- `outputs/agent_trajectories.csv`
- `outputs/aggregate_candidate_intention.csv`
- `outputs/aggregate_party_preference.csv`
- `outputs/reflections.jsonl`
- `outputs/broadcasts.jsonl`
- `outputs/evaluation_summary.json`
- `outputs/first_round_vote_distribution.json`
- `outputs/runoff_vote_distribution.json`
- `outputs/broadcast_cache/broadcasts.json`
- `logs/*.jsonl`
- `logs/metrics_summary.json`
- `agents/`, `simulation/`, `memory/`, `llm/`, `loaders/`, `validation/`
- `scripts/generate_souls_from_config.py`
- `config.py`, `run.py`, `requirements.txt`
- `README.md`, `REPRODUCIBILITY.md`, `.env.example`
- thesis documentation under `docs/`

## B. Keep but Document

- `docs/`: thesis/manuscript artifacts. Some documents still reference removed analysis dashboards or the old political config folder name because they are thesis artifacts and were not rewritten during source cleanup.
- `logs/`: about 73 MB in the initial inspection. Logs were kept for run traceability. If GitHub size becomes a concern, use Git LFS or publish logs as an external archived artifact rather than deleting them.
- `db/`: protected memory and belief archives, including a few older non-`_2023` files for agents 001-005.
- `social/`: minimal source package placeholder; kept because it is harmless and may be imported by future extensions.
- `.python-version`: local Python version hint; kept because it helps reproduce the development environment.

## C. Moved or Renamed

- `political_agent/` was renamed to `political_broadcast_config/` to clarify that these files configure broadcast speakers and message frames, not autonomous configured politician LLM agents.

No files were moved to `archive/`.

## D. Safe to Delete

The following local/cache/secret files were removed in the first cleanup pass:

- `./__pycache__/`
- `./agents/__pycache__/`
- `./llm/__pycache__/`
- `./loaders/__pycache__/`
- `./memory/__pycache__/`
- `./scripts/__pycache__/`
- `./simulation/__pycache__/`
- `./tests/__pycache__/`
- `./validation/__pycache__/`
- `./.DS_Store`
- `./docs/.DS_Store`
- `./docs/thesis_resources/.DS_Store`
- `./souls/.DS_Store`
- `./events/.DS_Store`
- `./voter_source_of_truth/.DS_Store`
- `./outputs/.DS_Store`
- `./outputs/analysis_charts/.DS_Store`
- `./.vscode/settings.json`
- `./.vscode/`

The following simulation-unrelated or generated analysis artifacts were removed in the second cleanup pass:

- `rag/`
- `voter_source_of_truth/Synthetic-Turkey-Simulation-Framework.md`
- `political_broadcast_config/synthetic_turkey_agent_configuration.md`
- `outputs/deep_analysis_dashboard.html`
- `outputs/deep_analysis_300_agents.ipynb`
- `outputs/deep_analysis_summary.json`
- `outputs/synthetic_turkey_results_dashboard.html`
- `outputs/tie_handling_sensitivity.csv`
- `outputs/tie_handling_sensitivity.md`
- `outputs/analysis_tables/`
- `outputs/analysis_charts/`
- `outputs/audit_charts/`
- `scripts/analyze_simulation_results.py`
- `scripts/build_deep_analysis_dashboard.py`
- `scripts/build_deep_analysis_notebook.py`
- `scripts/build_results_dashboard.py`
- `scripts/section_d_fresh_audit.py`
- `scripts/section_k_generate_charts.py`
- `scripts/tie_handling_sensitivity.py`

## E. Must Not Commit to GitHub

The real local environment file was removed and must stay untracked:

- `./.env`

`.gitignore` excludes `.env`, `.env.*` except `.env.example`, Python bytecode, test caches, virtual environments, OS/editor files, local scratch/cache folders, notebook checkpoints, and rerun scratch directories.

## Added or Updated

- Added `.gitignore`.
- Added `.env.example`.
- Added `actual_results_2023.yaml`.
- Added `run.py`.
- Added `REPRODUCIBILITY.md`.
- Rewrote `README.md` for a thesis-ready GitHub appendix.
- Added this cleanup report.
- Added a CLI entrypoint unit test in `tests/test_2023_mvp.py`.
- Added `numpy` and `matplotlib` to `requirements.txt`.
- Updated `config.py` to load political broadcast configuration from `political_broadcast_config/`.

## Files Required for Thesis Verification

- `outputs/agent_trajectories.csv`
- `outputs/evaluation_summary.json`
- `outputs/aggregate_candidate_intention.csv`
- `outputs/aggregate_party_preference.csv`
- `outputs/reflections.jsonl`
- `outputs/broadcasts.jsonl`
- `outputs/first_round_vote_distribution.json`
- `outputs/runoff_vote_distribution.json`
- `souls/agent_001.json` through `souls/agent_300.json`
- `db/*_beliefs_2023.json`
- `db/*_episodic_2023.json`
- `events/simulation_ticks.json`
- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`
- `political_broadcast_config/*.yaml`
- `run.py`
- `scripts/generate_souls_from_config.py`

## Remaining Issues

- Some thesis documents in `docs/` still mention removed generated analysis artifacts and the old political config folder name. They were kept unchanged as protected thesis documentation.
- `logs/` may be large for a public repository. Use Git LFS or an external archive if GitHub upload size becomes a concern.
- `docs/thesis_resources/` contains source PDFs. Confirm redistribution rights before making the GitHub repository public.
- Live OpenAI reruns can generate different values from the saved baseline because LLM sampling and model snapshots are not bitwise reproducible.
