# Synthetic Turkey Cleanup Report

This report was created before any destructive cleanup. The repository was inspected on 2026-06-12 from `/Users/abdullahkilinc/Desktop/syntetic-turkey`.

## Pre-Cleanup Findings

- The directory is not currently initialized as a Git repository, so `git status` reports `fatal: not a git repository`.
- The protected thesis-critical folders exist: `voter_source_of_truth/`, `political_agent/`, `events/`, `souls/`, `db/`, `outputs/`, `logs/`, `scripts/`, `validation/`, `agents/`, `simulation/`, `memory/`, and `llm/`.
- `outputs/agent_trajectories.csv` exists and contains 11,100 data rows and 38 columns.
- `souls/` contains 300 canonical `agent_*.json` synthetic voter-agent files.
- `db/` contains 300 `*_beliefs_2023.json` files, 300 `*_episodic_2023.json` files, and 5 older non-`_2023` belief/episodic files for agents 001-005. These older files are kept because `db/` is protected.
- `logs/` is about 73 MB. No individual file is larger than 20 MB. Logs are protected and were not removed.
- `README.md` referred to `run.py`, but `run.py` was missing. A stale `__pycache__/run...pyc` suggested a local entrypoint existed previously.
- `config.py` expects `actual_results_2023.yaml`, but that file was missing. The same actual-result constants appear in analysis scripts.
- A real `.env` file exists and contains an `OPENAI_API_KEY` variable. The value was not printed or copied.
- `scripts/build_results_dashboard.py` is a zero-byte file. It is kept because `scripts/` is protected and it may be an obsolete placeholder requiring thesis-owner review.

## A. Must Keep for Reproducibility

- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`
- `events/simulation_ticks.json`
- `political_agent/political_agents.yaml`
- `political_agent/political_personas.yaml`
- `political_agent/politician_event_responses.yaml`
- `political_agent/credibility_matrix.yaml`
- `political_agent/movement_state_machine.yaml`
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
- `outputs/analysis_tables/`
- `outputs/analysis_charts/`
- `outputs/audit_charts/`
- `logs/*.jsonl`
- `logs/metrics_summary.json`
- `agents/`, `simulation/`, `memory/`, `llm/`, `loaders/`, `validation/`
- `scripts/generate_souls_from_config.py`
- `scripts/analyze_simulation_results.py`
- `scripts/section_d_fresh_audit.py`
- `scripts/section_k_generate_charts.py`
- `scripts/tie_handling_sensitivity.py`
- `scripts/build_deep_analysis_dashboard.py`
- `scripts/build_deep_analysis_notebook.py`
- `config.py`
- `requirements.txt`
- `README.md`
- thesis documentation under `docs/`

## B. Keep but Document

- `docs/thesis_resources/*.pdf`: source literature for thesis context; kept even though this folder accounts for most of `docs/`.
- `docs/Synthetic_Turkey__a_source_grounded_generative_agent_based_simulation_of_the_2023_Turkish_presidential_election/`: manuscript/export artifacts; kept as thesis documentation.
- `outputs/deep_analysis_300_agents.ipynb`: generated notebook artifact; kept because it is useful for thesis inspection.
- `outputs/deep_analysis_dashboard.html` and `outputs/synthetic_turkey_results_dashboard.html`: generated inspection dashboards; kept.
- `outputs/broadcast_cache/broadcasts.json`: generated cache/output artifact; kept because it documents broadcast frames used by the run.
- `.python-version`: local Python version hint (`3.11.8`); kept because it helps reproduce the development environment.
- `rag/` and `social/`: currently minimal packages containing `__init__.py`; kept as source-tree placeholders.
- `tests/test_2023_mvp.py`: lightweight reproducibility and smoke tests; kept.
- `scripts/build_results_dashboard.py`: zero-byte placeholder; kept because it is inside protected `scripts/`.
- Legacy `db/agent_001_*` through `db/agent_005_*` files without `_2023`: kept because `db/` is protected.

## C. Move to `archive/`

No files were moved to `archive/`. The only ambiguous candidates are protected thesis artifacts or protected data/log folders, so they were left in place.

## D. Safe to Delete

Planned safe deletions before cleanup:

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

## E. Must Not Commit to GitHub

Planned deletion before cleanup:

- `./.env` because it contains a real `OPENAI_API_KEY` variable.

Planned Git ignore coverage:

- `.env` and `.env.*` except `.env.example`
- Python bytecode and test caches
- virtual environments
- OS/editor files
- local scratch/cache folders
- optional notebook checkpoints

## Cleanup Actions Performed

Removed exactly the planned local/cache/secret files:

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
- `./.env`

No thesis-critical input/output data, logs, generated agents, memory archives, analysis outputs, figures, or protected source folders were deleted.

Added or updated GitHub/reproducibility files:

- Added `.gitignore`.
- Added `.env.example`.
- Added `actual_results_2023.yaml`.
- Added `run.py`.
- Added `REPRODUCIBILITY.md`.
- Replaced `README.md` with thesis-ready repository documentation.
- Added this `CLEANUP_REPORT.md`.
- Added a CLI entrypoint unit test in `tests/test_2023_mvp.py`.
- Added `numpy` and `matplotlib` to `requirements.txt` because the audit/chart scripts import them.
- Updated one stale comment in `scripts/section_d_fresh_audit.py` that referred to the now-restored `actual_results_2023.yaml` as missing.

## Files Required for Thesis Verification

- `outputs/agent_trajectories.csv` with 11,100 data rows and 38 columns
- `outputs/evaluation_summary.json`
- `outputs/aggregate_candidate_intention.csv`
- `outputs/aggregate_party_preference.csv`
- `outputs/reflections.jsonl`
- `outputs/broadcasts.jsonl`
- `souls/agent_001.json` through `souls/agent_300.json`
- `db/*_beliefs_2023.json`
- `db/*_episodic_2023.json`
- `events/simulation_ticks.json`
- `voter_source_of_truth/synthetic_turkey_simulation.json`
- `voter_source_of_truth/2018_baseline_sampling_profile.yaml`
- `political_agent/*.yaml`
- `scripts/section_d_fresh_audit.py`
- `scripts/section_k_generate_charts.py`
- `scripts/tie_handling_sensitivity.py`

## Remaining Issues to Resolve

- The folder is still not initialized as a Git repository. `git status` will fail until `git init` or a clone/remote workflow is used.
- `logs/` is about 73 MB. It was kept because logs are protected. If GitHub size becomes a concern, use Git LFS or publish logs as an external archived artifact rather than deleting them.
- `docs/thesis_resources/` contains source PDFs and accounts for most of `docs/`. Confirm redistribution rights before pushing public GitHub releases.
- `scripts/build_results_dashboard.py` is zero bytes and appears obsolete, but it was kept because `scripts/` is protected.
- Five legacy `db/agent_00x_*` files without `_2023` remain. They were kept because `db/` is protected.
- Chart-generation scripts were import-checked but not executed during cleanup to avoid rewriting thesis figure files.
