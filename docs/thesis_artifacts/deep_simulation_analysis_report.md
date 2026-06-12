# Synthetic Turkey Deep Simulation Analysis Report

This report analyzes the completed 300-agent OpenAI simulation output currently stored under `outputs/`. It is a post-run analysis artifact: it does not alter the simulation, prompts, memories, or voter decisions.

## Executive Summary

- Data volume: 300 canonical voter souls, 11,100 agent-tick trajectory rows, 11,100 reflection rows, and 115 political broadcast rows.
- Run scope: 37 simulation ticks from the June 2018 baseline through the 28 May 2023 runoff result reveal.
- First-round raw simulated intention: Erdoğan 41.5%, Kılıçdaroğlu 49.1%, Oğan 1.4%, İnce 0.0%, undecided/other 8.0%.
- First-round normalized valid-candidate comparison: Erdoğan 45.1% vs actual 49.5%; Kılıçdaroğlu 53.4% vs actual 44.9%; Oğan 1.5% vs actual 5.2%.
- Runoff raw simulated intention: Erdoğan 41.8%, Kılıçdaroğlu 49.1%, abstain/invalid/undecided 9.1%.
- Runoff normalized valid-candidate comparison: Erdoğan 46.0% vs actual 52.2%; Kılıçdaroğlu 54.0% vs actual 47.8%.
- Evaluation summary reports first-round MAE 4.25 and runoff MAE 6.175. Candidate ranking accuracy is false in both rounds.
- The dominant substantive weakness remains clear: the model population under-produces Erdoğan and especially Sinan Oğan support, while over-producing Kılıçdaroğlu support. This is a calibration and persona-behavior issue, not a pipeline failure.

## Data Sources Used

- `souls/agent_001.json` through `souls/agent_300.json`: demographic, archetype, 2018 baseline, and persona metadata.
- `outputs/agent_trajectories.csv`: per-agent, per-tick belief, emotion, turnout, party, and candidate states.
- `outputs/reflections.jsonl`: textual reflections used for language and word-cloud analysis.
- `outputs/broadcasts.jsonl`: political broadcast frames emitted during the timeline.
- `outputs/evaluation_summary.json`: final vote distribution and evaluation metrics.
- `events/simulation_ticks.json`: tick titles and historical event context.

## Important Interpretation Notes

- Demographics are synthetic persona-generation assumptions, not a statistically sampled Turkish census or survey microdata file.
- Cities and education levels describe the generated agent population. They are useful for explaining simulation composition, but should not be described as measured Turkish voter demographics.
- The left/right analysis below uses an electoral-bloc proxy rather than a pure ideology scale. In Türkiye, CHP, Kurdish movement voters, nationalist opposition voters, and conservative dissenters do not map cleanly onto a single left-right axis.
- The simulation is LLM-first: these charts summarize LLM outputs after prompts, memory, broadcast filtering, and date fencing. They are not deterministic event-delta outputs.

## Demographic Structure

- Age range: 19 to 77; median 49.0; mean 48.6.
- Gender categories: Female: 151, Male: 149.
- Regions represented: 8. Cities represented: 25.

### Archetype Distribution

| archetype | agents | share |
| --- | --- | --- |
| Devout Anatolian Loyalist | 58 | 19.3% |
| Conservative Economically Disillusioned | 33 | 11.0% |
| Secular Urban Professional | 32 | 10.7% |
| Nationalist Grey Wolf (MHP core) | 30 | 10.0% |
| Kurdish Political Voter | 29 | 9.7% |
| Moderate Nationalist (İYİ) | 25 | 8.3% |
| Alevi-CHP Loyalist | 19 | 6.3% |
| Pious Disillusioned Islamist | 18 | 6.0% |
| Retired Protest Voter | 16 | 5.3% |
| Young Urban Protest Voter | 15 | 5.0% |
| Earthquake Zone Loyalist | 14 | 4.7% |
| Cosmopolitan Liberal | 11 | 3.7% |

### Age Distribution

| age_bin | agents | share |
| --- | --- | --- |
| 18-29 | 19 | 6.3% |
| 30-44 | 99 | 33.0% |
| 45-59 | 116 | 38.7% |
| 60+ | 66 | 22.0% |

### Education Distribution

| education_level | agents | share |
| --- | --- | --- |
| high_school | 96 | 32.0% |
| university | 92 | 30.7% |
| primary | 75 | 25.0% |
| graduate | 18 | 6.0% |
| vocational | 11 | 3.7% |
| university_student | 8 | 2.7% |

### Region Distribution

| region | agents | share |
| --- | --- | --- |
| Central Anatolia | 86 | 28.7% |
| Marmara | 65 | 21.7% |
| Eastern Anatolia | 58 | 19.3% |
| Mediterranean | 29 | 9.7% |
| Aegean | 26 | 8.7% |
| Southeast Anatolia | 22 | 7.3% |
| Black Sea | 8 | 2.7% |
| Earthquake Zone | 6 | 2.0% |

### Income Distribution

| income_bracket | agents | share |
| --- | --- | --- |
| middle | 136 | 45.3% |
| lower_middle | 95 | 31.7% |
| upper_middle | 30 | 10.0% |
| working_class | 21 | 7.0% |
| pensioner_low | 7 | 2.3% |
| upper | 6 | 2.0% |
| student | 5 | 1.7% |

### Employment Distribution

| employment_status | agents | share |
| --- | --- | --- |
| worker | 49 | 16.3% |
| retired | 46 | 15.3% |
| small_business_owner | 40 | 13.3% |
| public_sector | 25 | 8.3% |
| farmer | 22 | 7.3% |
| professional | 19 | 6.3% |
| tradesperson | 16 | 5.3% |
| manager | 13 | 4.3% |
| academic | 12 | 4.0% |
| service_worker | 11 | 3.7% |
| student | 11 | 3.7% |
| driver | 9 | 3.0% |
| security | 8 | 2.7% |
| early_career_professional | 7 | 2.3% |
| imam_or_religious_worker | 6 | 2.0% |
| teacher | 3 | 1.0% |
| creative_worker | 2 | 0.7% |
| unemployed | 1 | 0.3% |

### Top Cities

| city | agents | share |
| --- | --- | --- |
| Istanbul | 56 | 18.7% |
| Ankara | 29 | 9.7% |
| Izmir | 27 | 9.0% |
| Kayseri | 24 | 8.0% |
| Konya | 24 | 8.0% |
| Sivas | 17 | 5.7% |
| Bursa | 15 | 5.0% |
| Erzurum | 14 | 4.7% |
| Yozgat | 11 | 3.7% |
| Mersin | 8 | 2.7% |
| Malatya | 7 | 2.3% |
| Antalya | 7 | 2.3% |
| Eskisehir | 7 | 2.3% |
| Kahramanmaras | 6 | 2.0% |
| Mardin | 6 | 2.0% |
| Diyarbakir | 6 | 2.0% |
| Gaziantep | 5 | 1.7% |
| Osmaniye | 5 | 1.7% |
| Tunceli | 5 | 1.7% |
| Van | 5 | 1.7% |

### 2018 Baseline Anchors

These anchors are persona memory and sampling structure only. They should not be interpreted as deterministic rules for 2023 voting.

| party_2018 | agents | share |
| --- | --- | --- |
| AKP | 128 | 42.7% |
| CHP | 68 | 22.7% |
| DEM_HDP_YSP | 35 | 11.7% |
| MHP | 33 | 11.0% |
| IYI | 30 | 10.0% |
| Other | 6 | 2.0% |

| presidential_vote_2018 | agents | share |
| --- | --- | --- |
| Erdogan | 158 | 52.7% |
| Muharrem_Ince | 92 | 30.7% |
| Selahattin_Demirtas | 25 | 8.3% |
| Meral_Aksener | 22 | 7.3% |
| Temel_Karamollaoglu | 3 | 1.0% |

## Election Result Analysis

### First Round

| candidate | sim_raw | sim_valid_normalized | actual |
| --- | --- | --- | --- |
| Erdogan | 41.54% | 45.13% | 49.52% |
| Kilicdaroglu | 49.13% | 53.38% | 44.88% |
| Sinan_Ogan | 1.37% | 1.49% | 5.17% |
| Muharrem_Ince | 0.00% | 0.00% | 0.43% |
| Other | 0.37% | n/a | n/a |
| Undecided | 7.59% | n/a | n/a |

### Runoff

| candidate | sim_raw | sim_valid_normalized | actual |
| --- | --- | --- | --- |
| Erdogan | 41.80% | 46.01% | 52.18% |
| Kilicdaroglu | 49.06% | 53.99% | 47.82% |
| Abstain_Invalid_Undecided | 9.14% | n/a | n/a |

### Interpretation

- The pipeline correctly preserves uncertainty: undecided/other and abstain/invalid/undecided remain visible rather than being forced into a valid-vote total.
- For thesis comparison, both raw intention and normalized valid-candidate shares should be shown. Raw intention is closer to behavioral simulation; normalized valid share is closer to official election reporting.
- The largest miss is not the existence of undecided voters, but their direction: the model leaves too much anti-incumbent probability in Kılıçdaroğlu rather than producing enough Erdoğan consolidation and Oğan nationalist protest voting.

## Demographic Vote Behavior

### First-Round Top Candidate by Education

| category | n | Erdogan | Kilicdaroglu | Sinan_Ogan | Other | Undecided | top_group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_school | 96 | 64.6 | 35.4 | 0.0 | 0.0 | 0.0 | Erdogan |
| university | 92 | 34.8 | 65.2 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| primary | 75 | 78.7 | 21.3 | 0.0 | 0.0 | 0.0 | Erdogan |
| graduate | 18 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| vocational | 11 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| university_student | 8 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |

### First-Round Top Candidate by Top Cities

| category | n | Erdogan | Kilicdaroglu | Sinan_Ogan | Other | Undecided | top_group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Istanbul | 56 | 26.8 | 73.2 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Ankara | 29 | 6.9 | 93.1 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Izmir | 27 | 14.8 | 85.2 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Kayseri | 24 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Konya | 24 | 87.5 | 12.5 | 0.0 | 0.0 | 0.0 | Erdogan |
| Sivas | 17 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Bursa | 15 | 53.3 | 46.7 | 0.0 | 0.0 | 0.0 | Erdogan |
| Erzurum | 14 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Yozgat | 11 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Mersin | 8 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Antalya | 7 | 71.4 | 28.6 | 0.0 | 0.0 | 0.0 | Erdogan |
| Eskisehir | 7 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Malatya | 7 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Diyarbakir | 6 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Kahramanmaras | 6 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Mardin | 6 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Gaziantep | 5 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Karabuk | 5 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Osmaniye | 5 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Tunceli | 5 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |

### First-Round Top Candidate by Archetype

| category | n | Erdogan | Kilicdaroglu | Sinan_Ogan | Other | Undecided | top_group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Devout Anatolian Loyalist | 58 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Conservative Economically Disillusioned | 33 | 97.0 | 3.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Secular Urban Professional | 32 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Nationalist Grey Wolf (MHP core) | 30 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Kurdish Political Voter | 29 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Moderate Nationalist (İYİ) | 25 | 24.0 | 76.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Alevi-CHP Loyalist | 19 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Pious Disillusioned Islamist | 18 | 88.9 | 11.1 | 0.0 | 0.0 | 0.0 | Erdogan |
| Retired Protest Voter | 16 | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Young Urban Protest Voter | 15 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |
| Earthquake Zone Loyalist | 14 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | Erdogan |
| Cosmopolitan Liberal | 11 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | Kilicdaroglu |

## Electoral Bloc Response by Tick

Bloc definitions used for this analysis:

- Right/Government: AKP, MHP, YRP probability mass.
- Opposition-left/pro-democracy: CHP and DEM/HDP/YSP probability mass.
- Opposition-nationalist/center-right: İYİ probability mass.
- Other/Undecided: Other and undecided party probability mass.

### Largest Tick-to-Tick Shifts

| tick_id | title | Δ right | Δ opp-left | Δ Erdoğan | Δ Kılıçdaroğlu | Δ Oğan |
| --- | --- | --- | --- | --- | --- | --- |
| T004 | March 2019 Local Elections — AKP Loses Ankara and Istanbul | -8.21 | 6.43 | -11.7 | 7.82 | 0.17 |
| T019 | EQ-D: Erdoğan Admits Response Problems, Visits Disaster Zone | 9.97 | -6.77 | 7.34 | -6.56 | 0.17 |
| T018 | EQ-C: Twitter/TikTok Banned During Earthquake Rescue — Public Outcry | -10.86 | 6.41 | -4.87 | 6.41 | -0.48 |
| T023 | OPP-A: Akşener Leaves Table of Six — Opposition Crisis | 4.26 | -9.27 | 6.59 | -5.37 | -0.21 |
| T016 | EQ-A: Kahramanmaraş Earthquake Day — 7.8 and 7.7 Magnitude Double Stri | -6.81 | 4.3 | -6.76 | 5.26 | 0.09 |
| T013 | İmamoğlu Sentenced to 2.5 Years — Opposition Rallies Around Him | -4.34 | 3.73 | -6.03 | 4.56 | -0.3 |
| T021 | EQ-F: Opposition Mayors Respond — CHP Aid vs. Government Aid Narrative | -2.87 | 5.28 | -3.44 | 4.8 | -0.07 |
| T012 | Inflation Peaks at 80%+ — Worst Cost-of-Living Crisis in 24 Years | 4.24 | -1.58 | 6.18 | -1.33 | -0.26 |
| T035B_final_result_revealed | FINAL: Presidential Runoff — Erdoğan Wins 52.18% vs Kılıçdaroğlu 47.82 | 3.15 | -3.18 | 2.84 | -2.24 | 1.46 |
| T015 | Constitutional Court Freezes HDP Treasury Aid | 3.22 | -1.15 | 6.02 | -2.27 | -0.11 |
| T024 | OPP-B: Opposition Reunites — Kılıçdaroğlu Nominated with İmamoğlu/Yava | 1.89 | -0.32 | 0.66 | 9.51 | -0.05 |
| T008 | Turkey Withdraws from Istanbul Convention on Women's Rights | 4.08 | -2.32 | 2.59 | -2.94 | 0.24 |

### Full Tick Response Table

| tick | right | opp_left | opp_nat | other | Erdogan | Kilicdaroglu | Ogan | gov_appr | opp_trust | anger | hope | broadcasts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | 51.99 | 36.04 | 10.01 | 1.96 | 50.48 | 22.94 | 1.21 | 4.39 | 4.41 | 0.701 | 0.49 | 0.0 |
| T002 | 51.58 | 34.88 | 9.87 | 3.67 | 52.49 | 25.0 | 1.14 | 4.39 | 4.41 | 0.701 | 0.49 | 0.0 |
| T003 | 52.76 | 36.94 | 9.73 | 0.57 | 54.14 | 25.03 | 0.94 | 4.39 | 4.41 | 0.701 | 0.49 | 0.0 |
| T004 | 44.55 | 43.37 | 10.72 | 1.36 | 42.44 | 32.85 | 1.11 | 4.39 | 4.4 | 0.701 | 0.489 | 5.0 |
| T005 | 46.68 | 41.46 | 9.93 | 1.94 | 42.94 | 34.47 | 0.88 | 4.39 | 4.41 | 0.703 | 0.487 | 5.0 |
| T006 | 49.64 | 39.29 | 9.28 | 1.79 | 48.67 | 34.3 | 0.61 | 4.38 | 4.41 | 0.703 | 0.487 | 0.0 |
| T007 | 45.56 | 40.99 | 10.16 | 3.29 | 46.39 | 36.63 | 0.26 | 4.38 | 4.41 | 0.703 | 0.487 | 5.0 |
| T008 | 49.64 | 38.67 | 9.21 | 2.48 | 48.98 | 33.69 | 0.5 | 4.38 | 4.41 | 0.703 | 0.487 | 0.0 |
| T009 | 51.49 | 38.36 | 9.12 | 1.04 | 51.44 | 33.4 | 0.51 | 4.38 | 4.41 | 0.703 | 0.487 | 0.0 |
| T010 | 47.64 | 39.98 | 9.48 | 2.9 | 45.88 | 34.47 | 0.46 | 4.38 | 4.41 | 0.703 | 0.486 | 0.0 |
| T011 | 45.74 | 40.07 | 9.47 | 4.72 | 42.89 | 35.23 | 0.8 | 4.36 | 4.4 | 0.705 | 0.481 | 0.0 |
| T012 | 49.98 | 38.49 | 9.19 | 2.34 | 49.07 | 33.9 | 0.54 | 4.36 | 4.4 | 0.705 | 0.481 | 0.0 |
| T013 | 45.64 | 42.22 | 9.17 | 2.97 | 43.04 | 38.46 | 0.24 | 4.36 | 4.4 | 0.705 | 0.481 | 0.0 |
| T014 | 48.11 | 39.76 | 9.36 | 2.77 | 45.12 | 35.26 | 0.47 | 4.36 | 4.4 | 0.705 | 0.481 | 0.0 |
| T015 | 51.33 | 38.61 | 9.05 | 1.0 | 51.14 | 32.99 | 0.36 | 4.36 | 4.4 | 0.705 | 0.481 | 0.0 |
| T016 | 44.52 | 42.91 | 9.36 | 3.21 | 44.38 | 38.25 | 0.45 | 4.35 | 4.4 | 0.705 | 0.48 | 4.93 |
| T017 | 47.87 | 39.16 | 9.14 | 3.83 | 42.83 | 36.44 | 0.85 | 4.04 | 4.32 | 0.719 | 0.459 | 0.0 |
| T018 | 37.01 | 45.57 | 11.17 | 6.26 | 37.96 | 42.85 | 0.37 | 4.02 | 4.31 | 0.719 | 0.459 | 4.93 |
| T019 | 46.98 | 38.8 | 9.57 | 4.65 | 45.3 | 36.29 | 0.54 | 3.99 | 4.31 | 0.719 | 0.458 | 0.0 |
| T020 | 45.53 | 40.23 | 9.25 | 4.99 | 40.36 | 38.54 | 0.34 | 3.93 | 4.3 | 0.723 | 0.451 | 0.0 |
| T021 | 42.66 | 45.51 | 8.34 | 3.48 | 36.92 | 43.34 | 0.27 | 3.9 | 4.41 | 0.725 | 0.449 | 0.0 |
| T022 | 37.78 | 47.84 | 9.85 | 4.53 | 35.42 | 44.55 | 0.42 | 3.9 | 4.42 | 0.725 | 0.449 | 4.93 |
| T023 | 42.04 | 38.57 | 14.1 | 5.3 | 42.01 | 39.18 | 0.21 | 3.9 | 4.36 | 0.725 | 0.446 | 0.0 |
| T024 | 43.93 | 38.25 | 14.1 | 3.72 | 42.67 | 48.69 | 0.16 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T025 | 45.84 | 42.3 | 8.59 | 3.27 | 46.21 | 49.06 | 0.07 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T026 | 46.78 | 40.56 | 8.94 | 3.71 | 44.93 | 48.04 | 0.45 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T027 | 47.35 | 41.09 | 8.59 | 2.97 | 46.25 | 49.3 | 0.14 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T028 | 46.73 | 40.38 | 8.49 | 4.4 | 44.76 | 49.19 | 0.26 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T029 | 47.9 | 42.07 | 7.53 | 2.49 | 44.28 | 48.99 | 0.24 | 3.9 | 4.48 | 0.725 | 0.453 | 0.0 |
| T030A_first_round_vote_decision | 43.62 | 44.76 | 6.99 | 4.63 | 41.54 | 49.13 | 1.37 | 3.9 | 4.48 | 0.725 | 0.453 | 5.0 |
| T030B_first_round_result_revealed | 45.59 | 45.09 | 7.13 | 2.19 | 39.84 | 50.41 | 5.03 | 3.9 | 4.47 | 0.725 | 0.453 | 5.0 |
| T031 | 45.91 | 43.48 | 6.73 | 3.88 | 43.52 | 46.99 | 2.04 | 3.9 | 4.47 | 0.725 | 0.453 | 5.0 |
| T032 | 45.45 | 42.78 | 6.98 | 4.79 | 40.35 | 46.9 | 2.11 | 3.9 | 4.47 | 0.725 | 0.459 | 5.0 |
| T033 | 44.67 | 44.58 | 6.9 | 3.85 | 40.74 | 46.75 | 2.12 | 3.9 | 4.47 | 0.725 | 0.459 | 5.0 |
| T034 | 42.74 | 45.74 | 6.47 | 5.06 | 40.74 | 46.25 | 1.15 | 3.9 | 4.47 | 0.725 | 0.459 | 5.0 |
| T035A_runoff_vote_decision | 45.89 | 43.67 | 6.22 | 4.22 | 42.56 | 48.93 | 1.57 | 3.9 | 4.47 | 0.725 | 0.459 | 5.0 |
| T035B_final_result_revealed | 49.04 | 40.49 | 6.01 | 4.45 | 45.4 | 46.69 | 3.03 | 3.91 | 4.46 | 0.717 | 0.454 | 5.0 |

## Reflection Language and Word Cloud

The reflection corpus was tokenized from `outputs/reflections.jsonl`; common English function words and generic simulation words were removed. Names such as Erdoğan and Kılıçdaroğlu were normalized to ASCII tokens only for counting.

| word | count |
| --- | --- |
| government | 6028 |
| erdogan | 5116 |
| anger | 4909 |
| opposition | 3697 |
| kilicdaroglu | 2587 |
| frustrated | 2295 |
| worry | 2213 |
| frustration | 2192 |
| hope | 2062 |
| sadness | 1966 |
| earthquake | 1834 |
| support | 1828 |
| future | 1687 |
| response | 1625 |
| against | 1507 |
| economic | 1434 |
| hdp | 1400 |
| worried | 1169 |
| nationalist | 1067 |
| elections | 1057 |
| crisis | 981 |
| values | 979 |
| rights | 965 |
| believe | 947 |
| trust | 928 |
| people | 875 |
| fear | 873 |
| decision | 873 |
| change | 859 |
| pension | 857 |
| akp | 851 |
| istanbul | 813 |
| votes | 807 |
| democracy | 800 |
| landscape | 782 |
| question | 745 |
| election | 734 |
| implications | 720 |
| women | 709 |
| effectively | 707 |
| withdrawal | 705 |
| shift | 704 |
| imamoglu | 687 |
| handling | 675 |
| leadership | 672 |
| aid | 670 |
| nce | 654 |
| betrayal | 644 |
| only | 636 |
| runoff | 624 |

### Language Interpretation

- The high-frequency words show the emotional and issue agenda that the LLM agents repeatedly used to explain themselves.
- If words around democracy, economy, trust, earthquake, inflation, refugees, or stability dominate, that supports the thesis claim that agents responded through historical-event and persona lenses rather than only candidate names.
- If candidate names dominate too strongly, that is a warning that prompts may be making agents over-explain as political observers rather than ordinary voters.

## Generated Charts and Dashboard

- `outputs/deep_analysis_dashboard.html`
- `outputs/analysis_charts/demographics_age_distribution.svg`
- `outputs/analysis_charts/demographics_gender.svg`
- `outputs/analysis_charts/demographics_education.svg`
- `outputs/analysis_charts/demographics_region.svg`
- `outputs/analysis_charts/demographics_income.svg`
- `outputs/analysis_charts/demographics_employment.svg`
- `outputs/analysis_charts/demographics_top_cities.svg`
- `outputs/analysis_charts/demographics_archetypes.svg`
- `outputs/analysis_charts/results_first_round_vs_actual.svg`
- `outputs/analysis_charts/results_runoff_vs_actual.svg`
- `outputs/analysis_charts/electoral_bloc_by_tick.svg`
- `outputs/analysis_charts/candidate_probabilities_by_tick.svg`
- `outputs/analysis_charts/emotion_trajectories.svg`
- `outputs/analysis_charts/trust_approval_trajectories.svg`
- `outputs/analysis_charts/education_vote_breakdown.svg`
- `outputs/analysis_charts/reflection_word_cloud.svg`

## Thesis-Ready Findings

1. The 300-agent run is technically complete and analyzable: every canonical agent has a full 37-tick trajectory.
2. The LLM-first architecture produces coherent archetype-consistent behavior, especially for stable blocs such as devout loyalists, Alevi-CHP loyalists, Kurdish political voters, cosmopolitan liberals, and secular professionals.
3. The model remains too opposition-favorable in aggregate. This is visible in both first-round and runoff normalized candidate shares.
4. The strongest next methodological discussion should focus on why Oğan/nationalist protest voting and Erdoğan runoff consolidation are under-produced.
5. The report should present this as an exploratory research simulation, not as a predictive model. The value is in testing whether persona-grounded LLM agents generate interpretable political trajectories under source-grounded historical conditions.

## Limitations

- One OpenAI run is not enough to estimate stochastic variability. Because the full run is expensive and slow, this thesis should describe it as a single high-cost experimental run supported by mock-mode testing.
- The generated demographic population is source-grounded but not survey-weighted by official microdata.
- The simulation uses English reflections in this run, so word-frequency results reflect prompt/output language as well as agent reasoning.
- Left/right classification is a simplified analytical layer; Turkish party coalitions require more careful interpretation than a binary ideology axis.
- The LLM sometimes reasons like an analyst, not only like an ordinary voter. This should be noted as a prompt realism limitation.

## Suggested Next Calibration Questions

- Are nationalist archetypes given enough baseline salience, candidate awareness, and permission to choose Oğan?
- Are conservative economically disillusioned voters too easily converted to opposition trust, or not enough anchored by religious/national security frames?
- Do Kurdish voters show enough runoff turnout anxiety after the Özdağ protocol?
- Are earthquake-zone loyalists and retired protest voters behaving distinctly enough from generic government/opposition blocs?
- Are political broadcasts visible to the right archetypes at the right moments, or are some crucial frames missing from the voter prompt?
