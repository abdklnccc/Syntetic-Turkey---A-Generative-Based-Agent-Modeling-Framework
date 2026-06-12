# 300-Agent OpenAI Validation Run

Date prepared: 2026-05-16

## Status

The OpenAI validation phase is partially complete and blocked by OpenAI account quota.

The 300-agent baseline population and the 300-agent mock output set were audited successfully before OpenAI execution. The `.env` API key path was then wired without printing or reading the secret value: `config.py` now has a fallback `.env` loader for environments where `python-dotenv` is not installed. No voter prompts, persona configs, calibration parameters, or deterministic vote rules were changed.

The 20-agent x 5-tick OpenAI smoke test passed with 100/100 decisions and no provider fallbacks. The full 300-agent OpenAI run started successfully but hit OpenAI `insufficient_quota` errors on tick 13, after 3,617 successful full-run OpenAI decisions. The process was stopped as soon as the quota failures appeared because continuing would have produced mostly low-confidence provider-error fallbacks rather than a valid OpenAI validation run.

## Commands Run

Initial active-output audit:

```bash
# checked souls/, outputs/agent_trajectories.csv, first/runoff distributions,
# and evaluation_summary.json
python3 - <<'PY'
# local structured audit script
PY
```

`.env` loading and test verification:

```bash
python3 -m unittest tests.test_2023_mvp
```

Successful OpenAI smoke command:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --max-agents 20 --max-ticks 5 --parallel-agents --max-workers 5 --continue-on-agent-error
```

Full OpenAI command:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error
```

Manual stop after quota blocker:

```bash
pkill -f 'run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error'
```

Final local test verification after the `.env` fallback fix:

```bash
python3 -m unittest tests.test_2023_mvp
```

Result: 18 tests passed.

## Resume Needed

Resume was not needed for the smoke test.

The full run was manually stopped because OpenAI returned hard quota errors, not because of a transient interruption. Resume was not attempted, because the latest full-run log already contains provider-error fallback decisions at tick 13. For a clean thesis run, restore OpenAI quota/billing first, then rerun the full OpenAI simulation from scratch or explicitly trim/resume from the clean prefix before the first fallback.

Latest full-run log:

```text
logs/run_2023_20260516_144449_113733.jsonl
```

Latest successful OpenAI smoke log:

```text
logs/run_2023_20260516_144131_994594.jsonl
```

## API Decisions Completed

OpenAI smoke run:

- 100 decision entries
- 20 unique agents
- 5 unique ticks
- 0 provider-error fallbacks

Full OpenAI run before quota stop:

- 3,632 decision entries logged
- 3,617 successful OpenAI decision completions
- 15 `provider_error` fallback decisions
- 300 unique agents reached at least one decision
- T001 through T012 completed for all 300 agents
- T013 stopped after 32 logged decisions

Total successful OpenAI voter-decision completions across the smoke run and partial full run: 3,717.

## Provider Errors Or Fallbacks

Smoke run: none.

Full run: 15 provider-error fallbacks, all on T013 (`İmamoğlu Sentenced to 2.5 Years — Opposition Rallies Around Him`).

The provider error was:

```text
Error code: 429 - insufficient_quota
```

The fallback decisions were clearly marked with `provider_error` reason codes and low-confidence fallback reflections. Because this was a quota exhaustion blocker, the partial full run should not be used as a final thesis output.

## Active Output Sets

Before OpenAI execution, the active output set was the completed 300-agent mock run:

- `outputs/agent_trajectories.csv`: 11,100 rows
- Unique agents: 300
- Unique ticks: 37
- First-round distribution exported
- Runoff distribution exported
- `evaluation_summary.json` valid

After the successful smoke test, `outputs/` contains the 20-agent x 5-tick OpenAI smoke output:

- `outputs/agent_trajectories.csv`: 100 rows
- Unique agents: 20
- Unique ticks: 5
- Provider-error rows: 0

The smoke output has zero first-round and runoff distributions because the 5-tick smoke does not reach the election-decision ticks T030 and T035. This is expected and not a vote-distribution failure.

The interrupted full run did not complete, so it did not export a final 11,100-row OpenAI output set.

## Smoke Test Qualitative Inspection

The smoke run passed the requested qualitative checks:

- All 20 x 5 = 100 decisions completed.
- No provider-error fallbacks appeared in the successful smoke log.
- Reflections were diverse and persona-grounded, including pro-Erdoğan stability concerns, Alevi/minority anxiety, Kurdish/HDP-democracy concerns, and opposition disappointment.
- The 2018 baseline memory was visible in the prompt path as historical party and presidential vote memory.
- The prompt explicitly framed the 2018 anchors as memory, not future vote rules.
- Vote distributions were not meaningfully testable in the smoke output because T030/T035 were not reached.

## Final First-Round Distribution

No final 300-agent OpenAI first-round distribution was produced. The full run stopped at T013, before the first-round election decision tick T030.

300-agent mock reference:

- Erdogan: 35.694
- Kilicdaroglu: 44.409
- Sinan_Ogan: 7.681
- Muharrem_Ince: 1.961
- Other: 1.936
- Undecided: 8.319

Current smoke output distribution is all zeros because the smoke run stopped before T030 and should not be interpreted as an election result.

## Final Runoff Distribution

No final 300-agent OpenAI runoff distribution was produced. The full run stopped at T013, before the runoff decision tick T035.

300-agent mock reference:

- Erdogan: 51.397
- Kilicdaroglu: 37.874
- Abstain_Invalid_Undecided: 10.729

Current smoke output distribution is all zeros because the smoke run stopped before T035 and should not be interpreted as a runoff result.

## Comparison To Previous Runs

### Previous 50-Agent Complete Baseline Found In Logs

The repository contains several complete 50-agent logs with 1,850 decisions, such as:

```text
logs/run_2023_20260516_102239.jsonl
```

Their reflection style matches the local mock provider pattern, so they should not be treated as confirmed prior OpenAI research runs without additional provenance.

Latest complete 50-agent baseline found:

- First round: Erdogan 28.908, Kilicdaroglu 49.744, Sinan_Ogan 7.051, Muharrem_Ince 2.359, Other 2.439, Undecided 9.498
- Runoff: Erdogan 44.903, Kilicdaroglu 43.322, Abstain_Invalid_Undecided 11.775
- First-round MAE: 8.347
- Runoff MAE: 1.284

The repository also contains an incomplete likely-OpenAI log:

```text
logs/run_2023_20260516_103556.jsonl
```

It has 1,660 decisions and no final `evaluation_summary`, so it should not be used as a completed comparison run.

### 300-Agent Mock Run

The validated 300-agent mock run is complete and useful for pipeline validation, but it is not the thesis voter brain.

- First round: Erdogan 35.694, Kilicdaroglu 44.409, Sinan_Ogan 7.681, Muharrem_Ince 1.961, Other 1.936, Undecided 8.319
- Runoff: Erdogan 51.397, Kilicdaroglu 37.874, Abstain_Invalid_Undecided 10.729
- First-round MAE: 4.874
- Runoff MAE: 5.394

### 300-Agent OpenAI Run

The 300-agent OpenAI run has no final comparison distribution yet. It reached 3,617 successful full-run OpenAI decisions, then quota exhaustion produced 15 marked fallback decisions on T013 and the run was stopped.

## Ogan Support

Ogan support cannot be evaluated for the 300-agent OpenAI condition because the full OpenAI run did not reach T030.

Mock-only comparison:

- 50-agent complete baseline found in logs: Sinan_Ogan 7.051
- 300-agent mock active baseline: Sinan_Ogan 7.681

The 300-agent mock population keeps Ogan support visible, but this is not evidence of improved LLM behavior. It is a pipeline/sample-resolution reference only.

## Erdogan/Kilicdaroglu Balance

Erdogan/Kilicdaroglu balance cannot be evaluated for the 300-agent OpenAI condition because the full OpenAI run did not reach T030 or T035.

Mock-only comparison:

- 50-agent complete baseline found in logs: Erdogan 28.908, Kilicdaroglu 49.744
- 300-agent mock active baseline: Erdogan 35.694, Kilicdaroglu 44.409

The 300-agent mock first-round balance is closer than the 50-agent baseline found in logs, mainly because Erdogan is less severely underrepresented. It still understates Erdogan and overstates Kilicdaroglu relative to the real first-round result, and the mock runoff overcorrects toward Erdogan. This is not an OpenAI validation conclusion.

## Remaining Weaknesses

- The full OpenAI validation is blocked by OpenAI `insufficient_quota`.
- No final 11,100-row 300-agent OpenAI output exists.
- No final OpenAI first-round or runoff distributions exist.
- The current `outputs/` directory contains the successful smoke output, not a completed full OpenAI output.
- The latest full-run JSONL contains 15 marked fallback decisions and should not be used as a clean thesis result.
- Prior complete 50-agent logs have uncertain provider provenance.
- Mock-mode comparisons remain useful for pipeline diagnostics only.

## Dashboard Status

The dashboard was not rebuilt after the quota-blocked full run. Rebuilding now would publish the 20-agent smoke output as the active dashboard, which would be misleading for thesis validation. Rebuild the dashboard only after a completed clean 300-agent OpenAI output set is active.

## Smallest Safe Fix

Restore or increase OpenAI account quota/billing for the API key already present in `.env`. No prompt change, persona change, calibration change, or deterministic vote rule is needed for this blocker.

After quota is restored, run a clean full OpenAI validation:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error
```

If a transient interruption occurs without provider fallbacks, resume from the latest clean JSONL log:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error --resume-from-log logs/<latest-clean-log>.jsonl
```

If resuming from `logs/run_2023_20260516_144449_113733.jsonl`, explicitly handle the 15 existing T013 fallback rows first; otherwise they will remain part of the resumed run.

## Next Calibration Recommendations

1. Fix OpenAI quota/billing and rerun the full 300-agent OpenAI simulation cleanly.
2. Consider reducing `--max-workers` only if rate limits appear after quota is restored; it will not fix `insufficient_quota`.
3. Require zero provider-error fallbacks for the thesis-grade OpenAI run, or explicitly mark and exclude any affected rows from final interpretation.
4. After a clean full run, verify 11,100 rows, 300 unique agents, 37 ticks, exported first-round/runoff distributions, and valid `evaluation_summary.json`.
5. Rebuild the dashboard only after the clean full OpenAI output set is active.
6. Compare Ogan support and Erdogan/Kilicdaroglu balance using the completed OpenAI distributions, not the partial T013 log.
7. Preserve LLM-first voter reasoning; use persona-memory and prompt calibration only when a defensible behavioral reason is found, and do not add deterministic vote rules.
