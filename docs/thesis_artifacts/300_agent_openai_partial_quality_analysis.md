# 300-Agent OpenAI Partial Run Quality Analysis

Date: 2026-05-16

## Source Analyzed

Primary partial full-run log:

```text
logs/run_2023_20260516_144449_113733.jsonl
```

Clean resume prefix created from the same run:

```text
logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

The clean prefix contains:

- 12 complete clean ticks: `T001` through `T012`
- 3,600 OpenAI voter decisions
- 0 provider-error fallback decisions
- 300 agents per tick

The original partial full-run contains 15 provider-error fallback decisions on `T013` after OpenAI returned `429 insufficient_quota`. Those `T013` rows should not be used as thesis evidence.

## Technical Quality

The OpenAI run was technically healthy until quota exhaustion.

- Smoke test: 20 agents x 5 ticks = 100/100 decisions, 0 fallbacks.
- Full run clean prefix: 300 agents x 12 ticks = 3,600/3,600 clean decisions, 0 fallbacks.
- Reflection diversity at `T012`: 299 unique reflections out of 300 agents.
- Confidence at `T012`: 242 medium, 58 high, 0 low.
- Reflection length at `T012`: average 225 characters, range 161-341.

This indicates the provider path, JSON validation, persona grounding, and 300-agent concurrency are working. The blocker was account quota, not simulation code.

## Behavioral Direction

The 300-agent 2018 baseline is moving the simulation in the right direction compared with the earlier over-opposition behavior.

At `T012` (inflation/cost-of-living phase, before the 2023 campaign decision ticks), aggregate first-round intention was:

| Candidate | T012 OpenAI Partial |
|---|---:|
| Erdoğan | 49.07% |
| Kılıçdaroğlu | 33.90% |
| Sinan Oğan | 0.54% |
| Muharrem İnce | 9.98% |
| Other | 0.38% |
| Undecided | 6.12% |

Runoff intention at `T012`:

| Option | T012 OpenAI Partial |
|---|---:|
| Erdoğan | 49.74% |
| Kılıçdaroğlu | 46.02% |
| Abstain / invalid / undecided | 4.25% |

This is a major improvement over the earlier 50-agent OpenAI pattern where Kılıçdaroğlu was strongly over-predicted. The 2018 sampling frame is helping preserve the AKP/MHP/Erdoğan electorate.

## Baseline Anchor Behavior

At `T012`, 2018 anchors remain visible in the LLM decisions:

| 2018 Party Anchor | n | Erdoğan | Kılıçdaroğlu | Oğan | İnce | Undecided |
|---|---:|---:|---:|---:|---:|---:|
| AKP | 128 | 88.72% | 2.70% | 0.38% | 0.31% | 7.55% |
| CHP | 68 | 0.00% | 85.59% | 0.00% | 14.41% | 0.00% |
| HDP/DEM | 35 | 4.29% | 52.86% | 1.43% | 24.29% | 15.71% |
| İYİ | 30 | 0.83% | 64.17% | 0.83% | 34.17% | 0.00% |
| MHP | 33 | 93.03% | 0.91% | 1.21% | 0.00% | 4.24% |
| Other small parties | 6 | 20.00% | 33.33% | 0.00% | 16.67% | 30.00% |

This is encouraging because the LLM is not collapsing the whole electorate into a generic opposition/pro-government binary. However, some blocs need calibration.

## Main Positive Signals

1. **The Erdoğan base is no longer underrepresented early in the run.**  
   At `T012`, Erdoğan is near 49% in first-round intention and near 50% in runoff intention.

2. **The 2018 party/presidential anchors are influencing behavior without deterministic vote rules.**  
   AKP and MHP anchors remain overwhelmingly Erdoğan-leaning, CHP anchors remain opposition-leaning, and HDP/DEM anchors show both opposition alignment and some abstention/uncertainty.

3. **Reflection quality is strong.**  
   Reflections are mostly unique, event-specific, and persona-grounded. Economic grievance dominates `T012`, which is appropriate for the inflation/cost-of-living context.

4. **The system is worth continuing after quota restoration.**  
   The partial OpenAI evidence suggests the 300-agent baseline is correcting the previous over-opposition bias.

## Main Red Flags

1. **Sinan Oğan support is still missing in OpenAI behavior.**  
   At `T012`, Oğan is only 0.54% overall. MHP-anchored agents average only 1.21% Oğan, and İYİ-anchored agents average only 0.83% Oğan. The mock run had visible Oğan support, but this partial OpenAI run does not yet show the nationalist protest pathway.

2. **MHP core may be too Erdoğan-loyal before the 2023 campaign.**  
   MHP-anchored voters are 93.03% Erdoğan at `T012`. Some of that is plausible, but a realistic 2023 Oğan pathway requires a minority of nationalist voters to become protest-oriented after later campaign events.

3. **İYİ voters split between Kılıçdaroğlu and İnce, not Oğan.**  
   This may be plausible before Oğan's campaign becomes salient, but the later prompt/event handling must allow İYİ/MHP nationalist protest voters to discover Oğan after the relevant 2023 ticks.

4. **The early candidate schema still exposes future 2023 candidate labels before they are politically known.**  
   This is not necessarily fatal if interpreted as internal evaluation slots, but the prompt should eventually clarify that candidate probabilities before candidacy announcements are latent evaluation fields, not voter knowledge of future candidacies.

5. **Other-small-party anchors need review.**  
   The small-party group is only six agents, but its party preference behavior may not cleanly represent Saadet/HÜDA PAR/Vatan-style differences.

## Recommendation

Yes, it is reasonable to add OpenAI credits and continue. The partial run shows the 300-agent 2018 baseline is moving the system in the right direction, especially by restoring Erdoğan/AKP/MHP weight and improving reflection diversity.

Do **not** resume from the original quota-blocked log because it contains fallback rows on `T013`.

Use the clean prefix log instead:

```bash
NUM_AGENTS=300 python3 run.py --provider openai --parallel-agents --max-workers 5 --continue-on-agent-error --resume-from-log logs/run_2023_20260516_144449_clean_through_T012.jsonl
```

This should preserve the 3,600 clean OpenAI decisions already paid for and continue from `T013` with no fallback contamination. Remaining expected voter-decision calls are approximately:

```text
25 remaining ticks x 300 agents = 7,500 OpenAI voter decisions
```

## Next Calibration Focus After Full Run

After the full OpenAI run completes, evaluate:

- Whether Oğan support appears after nationalist campaign ticks.
- Whether MHP/İYİ nationalist voters diversify after 2023 opposition/campaign events.
- Whether Kurdish voters show turnout risk after the Özdağ protocol.
- Whether İnce support declines appropriately after withdrawal.
- Whether Erdoğan/Kılıçdaroğlu balance remains closer than the previous 50-agent run.

Do not change prompts before completing the clean full OpenAI run unless a hard blocker appears. The current partial evidence is strong enough to justify continuing.
