# 300-Agent OpenAI Final Validation Run

Date prepared: 2026-05-16

## Status

Completed successfully from the clean T012 prefix.

The run preserved LLM-first voter reasoning. No prompts, personas, calibration parameters, configs, or deterministic vote rules were changed during this continuation. The contaminated quota-failure log was not resumed.

## Commands Run

Clean-prefix verification:

```bash
python3 - <<'PY'
# verified logs/run_2023_20260516_144449_clean_through_T012.jsonl
# 12 complete ticks, 3,600 decisions, 300 agents per tick, 0 provider_error rows
PY
```

Resume command:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error --resume-from-log logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

Final verification:

```bash
python3 - <<'PY'
# verified clean prefix + resumed JSONL + outputs/agent_trajectories.csv
PY
```

Dashboard rebuild:

```bash
python3 scripts/build_results_dashboard.py
```

Dashboard output:

```text
outputs/synthetic_turkey_results_dashboard.html
```

## Resume Accounting

Resume was used from:

```text
logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

The contaminated quota-failure log was deliberately not used:

```text
logs/run_2023_20260516_144449_113733.jsonl
```

Final resumed log:

```text
logs/run_2023_20260516_165048_164535.jsonl
```

Decision accounting:

- Total final decisions: 11,100
- OpenAI decisions reused from clean prefix: 3,600
- New OpenAI decisions completed in resumed run: 7,500
- Total agents: 300
- Total ticks: 37
- Provider-error fallback rows: 0
- Agent-error events: 0

The resumed JSONL records the 7,500 new decisions from T013 through T035B. The exported CSV contains the full combined 11,100-row trajectory.

## Output Verification

Verified final outputs:

- `outputs/agent_trajectories.csv`: 11,100 rows
- Unique agents: 300
- Unique ticks: 37
- Per-tick decisions: 300 for all 37 ticks
- `provider_error` rows in CSV: 0
- `outputs/first_round_vote_distribution.json`: exported
- `outputs/runoff_vote_distribution.json`: exported
- `outputs/evaluation_summary.json`: valid JSON

Evaluation summary:

- First-round MAE: 4.250
- Runoff MAE: 6.175
- First-round ranking accuracy: false
- Runoff ranking accuracy: false
- Mean turnout probability: 82.3
- Mean abstention probability: 17.7

## Final First-Round Distribution

Final OpenAI first-round distribution:

| Candidate | Share |
|---|---:|
| Erdogan | 41.539 |
| Kilicdaroglu | 49.133 |
| Sinan_Ogan | 1.372 |
| Muharrem_Ince | 0.000 |
| Other | 0.367 |
| Undecided | 7.589 |

## Final Runoff Distribution

Final OpenAI runoff distribution:

| Option | Share |
|---|---:|
| Erdogan | 41.801 |
| Kilicdaroglu | 49.061 |
| Abstain_Invalid_Undecided | 9.138 |

## Comparison To Partial T012 OpenAI Analysis

The clean T012 prefix showed strong early correction of the previous over-opposition pattern, but later campaign ticks shifted the run toward Kilicdaroglu.

| First-round option | T012 partial | Final T030 |
|---|---:|---:|
| Erdogan | 49.071 | 41.539 |
| Kilicdaroglu | 33.901 | 49.133 |
| Sinan_Ogan | 0.544 | 1.372 |
| Muharrem_Ince | 9.984 | 0.000 |
| Other | 0.380 | 0.367 |
| Undecided | 6.120 | 7.589 |

| Runoff option | T012 partial | Final T035 |
|---|---:|---:|
| Erdogan | 49.737 | 41.801 |
| Kilicdaroglu | 46.017 | 49.061 |
| Abstain/Invalid/Undecided | 4.247 | 9.138 |

The T012 partial result was closer on Erdogan strength. The completed campaign phase captures opposition consolidation and Ince withdrawal, but it over-shifts away from Erdogan and does not build enough Ogan support.

## Comparison To 300-Agent Mock Run

The 300-agent mock run remains a pipeline baseline, not the thesis voter brain.

| Metric | 300-agent mock | 300-agent OpenAI final |
|---|---:|---:|
| Erdogan first round | 35.694 | 41.539 |
| Kilicdaroglu first round | 44.409 | 49.133 |
| Sinan_Ogan first round | 7.681 | 1.372 |
| Undecided first round | 8.319 | 7.589 |
| Erdogan runoff | 51.397 | 41.801 |
| Kilicdaroglu runoff | 37.874 | 49.061 |
| Abstain/Invalid/Undecided runoff | 10.729 | 9.138 |
| First-round MAE | 4.874 | 4.250 |
| Runoff MAE | 5.394 | 6.175 |

OpenAI improves first-round MAE and Erdogan first-round support relative to mock, but loses the mock's visible Ogan pathway and produces a weaker Erdogan runoff.

## Comparison To Previous 50-Agent Run

No complete, clearly provenanced 50-agent OpenAI final run is available in the repository. The latest complete 50-agent baseline found is:

```text
logs/run_2023_20260516_102239.jsonl
```

Its reflection style appears mock-like, so it should be treated as an uncertain-provider comparison rather than confirmed OpenAI evidence.

| Metric | 50-agent complete baseline found | 300-agent OpenAI final |
|---|---:|---:|
| Erdogan first round | 28.908 | 41.539 |
| Kilicdaroglu first round | 49.744 | 49.133 |
| Sinan_Ogan first round | 7.051 | 1.372 |
| Erdogan runoff | 44.903 | 41.801 |
| Kilicdaroglu runoff | 43.322 | 49.061 |
| First-round MAE | 8.347 | 4.250 |
| Runoff MAE | 1.284 | 6.175 |

The 300-agent OpenAI run is much better on first-round Erdogan recovery than this 50-agent baseline, but worse on runoff balance and Ogan support.

## Sinan Ogan Support

Ogan support improved after the campaign ticks, but not enough.

Overall Ogan trajectory:

| Tick | Ogan first-round support |
|---|---:|
| T012 inflation phase | 0.544 |
| T023 Akşener leaves table | 0.206 |
| T024 opposition reunites | 0.160 |
| T027 HDP/YSP endorses Kilicdaroglu | 0.143 |
| T029 Ince withdrawal | 0.243 |
| T030 first-round vote | 1.372 |

The final increase is mainly from MHP-anchored voters:

| 2018 anchor | T012 Ogan | Final T030 Ogan |
|---|---:|---:|
| MHP | 1.212 | 7.323 |
| IYI | 0.833 | 0.000 |
| AKP | 0.375 | 1.328 |
| DEM/HDP/YSP | 1.429 | 0.000 |

Interpretation: the model can produce a nationalist protest pathway inside MHP, but it is too narrow. It does not create enough IYI-to-Ogan or broader anti-opposition nationalist protest behavior, so final Ogan support remains far below the real 5.17% and below the 300-agent mock's 7.681%.

## Erdogan/Kilicdaroglu Balance

The completed run improves first-round Erdogan support compared with the 50-agent complete baseline found in logs and the 300-agent mock run, but it does not fully preserve the strong Erdogan base seen at T012.

Final first-round anchor behavior:

| 2018 party anchor | n | Erdogan | Kilicdaroglu | Ogan | Undecided |
|---|---:|---:|---:|---:|---:|
| AKP | 128 | 76.654 | 12.669 | 1.328 | 9.271 |
| CHP | 68 | 0.000 | 100.000 | 0.000 | 0.000 |
| DEM/HDP/YSP | 35 | 0.000 | 90.000 | 0.000 | 8.571 |
| IYI | 30 | 3.333 | 84.833 | 0.000 | 11.833 |
| MHP | 33 | 74.444 | 5.455 | 7.323 | 11.566 |
| Other | 6 | 15.556 | 73.889 | 0.000 | 8.889 |

Positive signal: AKP and MHP anchors remain mostly Erdogan-leaning, and CHP/DEM anchors remain opposition-leaning without deterministic vote rules.

Weakness: Erdogan falls from 49.071 at T012 to 41.539 at T030, while Kilicdaroglu rises to 49.133. The campaign ticks appear to over-consolidate opposition support and understate Erdogan resilience.

## Kurdish Runoff And Ozdag Protocol Behavior

The model shows a visible Kurdish reluctance response to the nationalist runoff phase and the Ozdag protocol, but the final runoff vote still largely returns to anti-Erdogan strategic support.

DEM/HDP/YSP-anchored runoff trajectory:

| Tick | Erdogan | Kilicdaroglu | Abstain/Invalid/Undecided |
|---|---:|---:|---:|
| T027 HDP/YSP endorses Kilicdaroglu | 1.714 | 91.629 | 6.657 |
| T030B first-round result revealed | 0.000 | 94.286 | 5.714 |
| T031 nationalist turn | 0.000 | 81.429 | 18.571 |
| T032 Ogan endorses Erdogan | 2.857 | 90.714 | 6.429 |
| T033 Ozdag protocol | 2.381 | 82.381 | 15.238 |
| T034 Kurdish reluctance tick | 2.381 | 62.381 | 35.238 |
| T035 runoff vote decision | 0.000 | 87.143 | 12.857 |

Interpretation: the qualitative reflections are behaviorally credible. Kurdish political voters describe betrayal, conflict, and reduced hope after the Ozdag protocol, while many still reason that defeating Erdogan is strategically necessary. The final T035 vote decision is plausible in direction: low Erdogan support, high Kilicdaroglu support, and meaningful abstention risk.

Remaining weakness: turnout probability is too flat. The DEM/HDP/YSP-anchor mean turnout stayed around 82.77 across the runoff sequence even when abstention probability spiked in the vote intention vector. Future calibration should connect stated reluctance and abstention risk more consistently to turnout probability.

## Remaining Weaknesses

- Ogan support is still underproduced overall.
- IYI-anchored nationalist protest voting does not move to Ogan in the final first round.
- Erdogan/Kilicdaroglu balance worsens after T012; the campaign phase over-shifts toward Kilicdaroglu.
- Runoff Erdogan support is too low, and runoff ranking accuracy is false.
- Undecided remains high at the first-round vote decision.
- Turnout probabilities are too flat, especially for Kurdish runoff reluctance.
- Some blocs are too unanimous, especially CHP anchors at 100% Kilicdaroglu in the final first round.
- The first-round output still has no Ince support after withdrawal, which is directionally sensible but may be too complete.

## Next Calibration Recommendations

1. Keep this completed run as the first thesis-grade 300-agent OpenAI baseline.
2. Do not add deterministic vote rules to fix aggregate errors.
3. Review nationalist protest reasoning in MHP and IYI personas, especially how Ogan becomes salient before T030.
4. Review campaign-tick prompt context for over-consolidation around Kilicdaroglu after T024/T027.
5. Add a source-grounded calibration hypothesis for Erdogan resilience among AKP/MHP/conservative-disillusioned voters during the late campaign.
6. Improve turnout dynamics so abstention-risk reflections can affect turnout probability, especially for Kurdish runoff reluctance.
7. Re-run a smaller OpenAI calibration slice before spending on another full 300-agent run.
8. Use archetype-level diagnostics, not only aggregate distributions, when deciding whether prompt/persona calibration is thesis-defensible.

## Thesis Interpretation

This run is technically clean and thesis-usable as a baseline OpenAI validation result. It demonstrates that the 300-agent 2018 sampling frame and prompt memory preserve meaningful party-anchor behavior without deterministic vote forcing. The main empirical weakness is no longer a broken pipeline or missing Erdogan base early in the trajectory; it is late-campaign behavioral calibration, especially insufficient Ogan protest voting and excessive Kilicdaroglu consolidation.
