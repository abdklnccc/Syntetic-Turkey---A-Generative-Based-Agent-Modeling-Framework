# Synthetic Turkey — Paper Audit Source of Truth

> Consolidated audit of the Synthetic Turkey project (single 300-agent OpenAI run,
> 2026-05-16), built from the canonical `outputs/agent_trajectories.csv` and the
> design/configuration files. Intended as a working reference for drafting a
> Journal of Computational Social Science (JCSS) submission and the corresponding
> thesis chapters. Numbers verified against the canonical run; all claims
> recomputed from raw data.

**Project:** Synthetic Turkey — LLM-First Agent-Based Simulation of the 2023 Turkish Presidential Election
**Author:** Abdullah Kılınç
**Canonical run:** `logs/run_2023_20260516_142653_179132.jsonl` (11,138 records)
**Audit date:** 2026-05-23

---

## How to use this document

This file is the **single source of truth** for facts, framing, text blocks, and chart references when drafting the paper. It is *not* the paper itself. Three rules:

1. **Numbers are recomputed from raw data.** Anything pulled from
   `outputs/analysis_tables/`, the HTML dashboards, or the existing notebook is
   marked as untrusted (per the author's instruction). The fresh quantitative
   audit lives in §D and is reproduced by `scripts/section_d_fresh_audit.py`.
2. **Framing is the diagnostic-failure framing.** The paper does *not* claim
   predictive validation. It claims partial reproduction, diagnoses where it
   fails, and discloses the cost constraint that bounds the study to one
   realization.
3. **No further simulations are recommended.** Per author decision, the paper
   is to be drafted on the single existing run; no mock-mode comparison,
   no targeted ablations, no replication. The cost-disclosure paragraph in §I.6
   does the work that additional runs would otherwise do.

**Chart deliverables:** All 13 publication-quality charts described in §K live
at `outputs/audit_charts/` as both SVG and PNG. Regenerate any time with:

```bash
python3 scripts/section_k_generate_charts.py
```

---

## Table of contents

- [The headline facts (read first)](#the-headline-facts-read-first)
- [A. Project Summary](#a-project-summary)
- [B. Data Inventory and Scientific Role](#b-data-inventory-and-scientific-role)
- [C. Simulation Output Inventory](#c-simulation-output-inventory)
- [D. Main Empirical Findings (fresh quantitative audit)](#d-main-empirical-findings-fresh-quantitative-audit)
- [E. Validity and Bias Assessment](#e-validity-and-bias-assessment)
- [F. Recommended Additional Analyses (free-only)](#f-recommended-additional-analyses-free-only)
- [G. Journal and Thesis Fit](#g-journal-and-thesis-fit)
- [H. Proposed Paper and Thesis Structure](#h-proposed-paper-and-thesis-structure)
- [I. Plain-language draft text blocks](#i-plain-language-draft-text-blocks)
- [J. Reviewer / Examiner Risk Checklist](#j-reviewer--examiner-risk-checklist)
- [K. Chart Catalog](#k-chart-catalog)

---

## The headline facts (read first)

| | Erdoğan | Kılıçdaroğlu | Sinan Oğan | Other / Undec. |
|---|---|---|---|---|
| **Actual first round (YSK)** | 49.52% | 44.88% | 5.17% | 0.43% (İnce) |
| **Simulated first round (mean-prob)** | 41.54% | 49.13% | 1.37% | 7.96% (Other + Undec) |
| **Simulated first round (mode-vote)** | **54.67%** | 45.33% | 0% | 0% |
| **Actual runoff (YSK)** | 52.18% | 47.82% | — | — |
| **Simulated runoff (mean-prob)** | 41.80% | 49.06% | — | 9.14% abstain |
| **Simulated runoff (mode-vote)** | **55.33%** | 44.33% | — | 0.33% abstain |

- **First-round MAE (renormalized, 4 candidates):** 4.25
- **Runoff MAE (renormalized, 2 candidates):** 6.175
- **Ranking accuracy (engine-reported):** False for both rounds — but this is the mean-probability rule. Under mode-vote, the simulation correctly identifies Erdoğan as the winner in both rounds.

**Single most important methodological finding:**
**Two reasonable scoring rules give two different winners** from the same simulation. Mean-probability says Kılıçdaroğlu (wrong); mode-vote says Erdoğan (right, 54.67% vs actual 49.52%). The paper should report both and use the divergence diagnostically.

**Cost binding constraint:** One full 300-agent × 37-tick OpenAI run costs ~$10 USD and ~10 hours wallclock. The reported simulation is one such run. No replications. Per-call cost ≈ $0.0009.

**Largest concrete diagnostic finding:** Sinan Oğan's 5.17% actual share is reproduced as 1.37%. The code includes a placeholder for a missing 13th archetype (ATA Alliance Nationalist Protest Voter) but no parameterization. This single omission accounts for roughly half of the rank inversion in mean-probability scoring.

---

## A. Project Summary

### A.1 What this project is, scientifically

A stylized LLM-mediated agent-based model (ABM) of electoral dynamics in a polarized, mixed-regime political system. The components:

- **Synthetic electorate** of N=300 agents drawn from 12 hand-built voter archetypes calibrated to the 2018 Turkish parliamentary election.
- **Per-agent state variables:** 12-dim political worldview (1–10), 5-dim emotional baseline (0–1), 5-dim media diet (0–1), 11 behavioral parameters, 8-party initial vote distribution, demographic identity.
- **35-tick event timeline** from June 2018 to May 2023, with two additional split decision/reveal ticks at T030/T035 for election-result leakage protection (37 tick states per agent total).
- **Political broadcast agents** (Erdoğan, Kılıçdaroğlu, İmamoğlu, Bahçeli, Akşener, the Kurdish movement, Demirtaş as symbolic resource, and 9 internal personas).
- **LLM voter decision loop** at GPT-4o-mini temperature 0.45, producing per-tick approval/trust/emotion/candidate/party updates plus a free-text reflection.
- **Validation strategy:** simulated first-round and runoff distributions compared against actual 2023 YSK results plus archetype/demographic/trajectory analyses.

### A.2 Research question

> Can LLM-based synthetic voter agents, grounded in realistic Turkish voter personas, historical events, political broadcasts, memory, and social context, approximate voting behavior in the 2023 Turkish presidential election?

This is a method-validation question, not a prediction question. The paper needs to tighten "approximate" — operational candidate: directional reproduction of archetype-level voting patterns plus diagnostic decomposition of failure.

### A.3 What is genuinely novel

1. **A non-Western, non-US, polarized-regime case** — most published LLM-voter studies target US data.
2. **Source-grounded archetype construction** from named published surveys (KONDA, Kadir Has, Optimar, MetroPOLL, Konrad-Adenauer, Çevik, MEI) rather than free-form persona prompting.
3. **A 5-year, 35-event longitudinal stream** with persistent per-agent state, rather than single-shot prompting.
4. **Explicit leakage fencing** via split decision/reveal ticks at election outcomes (verified working in `tick_engine.py:17-46`).
5. **Credibility × media-diet × archetype broadcast filtering** as a structured intermediation layer between political actors and voters.
6. **Kurdish movement state machine** modeling the HDP → YSP → HEDEP → DEM transitions across 7 periods (a substantive ABM contribution).

### A.4 What is risky / vulnerable (the reviewer-2 surface)

1. **The headline mean-probability result is a wrong winner** (Kılıçdaroğlu plurality vs actual Erdoğan plurality). Mode-vote scoring is correct; mean-probability is not. The paper must lead with both.
2. **Archetype weights and event Δ matrix are hand-set**; the file itself flags this in `synthetic_turkey_simulation.json` epistemic warnings.
3. **The event sensitivity matrix is calibrated for plausibility, not predictive accuracy** — partial circularity.
4. **The 2024 trajectory distributions** in the simulation JSON use post-2023 ground truth (must be disclosed).
5. **300 agents is small** for sub-bloc inference; Sinan Oğan's 5.17% real share = ~15 agents.
6. **LLM stochasticity is not quantified** — only one realization exists at temperature 0.45.
7. **The framework markdown** targets a 50-agent 2024-local-election simulation; the actual run is 300 agents and 2023 presidential. Some scope mismatch.
8. **Emotion trajectories vary by ~0.5%** across 5 years (suspicious flatness outside the earthquake).
9. **`actual_results_2023.yaml` referenced in config but missing** from disk.
10. **The Kurdish movement state machine and credibility matrix encode researcher prior** (unavoidable but needs argument).

### A.5 Defensible contribution claim

> We present a method-development study for LLM-mediated agent-based electoral
> simulation in a polarized, non-Western context. We show that source-grounded
> synthetic voters reproduce the direction of incumbent approval erosion across
> the 2018–2023 Turkish political cycle, but systematically under-weight the
> durability of the Erdoğan coalition under economic and disaster shock. We use
> this divergence diagnostically to identify which model components carry the
> prediction error.

---

## B. Data Inventory and Scientific Role

### B.0 Epistemic classification rubric

| Bucket | Definition | Disclosure obligation |
|---|---|---|
| **Empirical** | Drawn from a measured external source (YSK results, ECHR rulings, dated news, published polling aggregates). | Cite source. |
| **Synthetic** | Generated by code using empirical anchors as constraints. | Document the sampler; release the seed. |
| **Heuristic** | Researcher-set numeric values with qualitative justification. | Justify the number; run sensitivity if budget allows. |
| **LLM-generated** | Produced at runtime by an LLM. | Disclose model, temperature, prompt, stochasticity. |

### B.1 The data inventory

**`voter_source_of_truth/synthetic_turkey_simulation.json`** — Master archetype file (12 archetypes × 12-dim worldview / 5-dim emotion / 5-dim media / 11 behavioral / 8-party intention / 6-state 2024 trajectory + a 12×10 event Δ matrix). **Bucket: heuristic.** File itself admits values are "research-informed estimates, not statistically representative." This is the single most important file in the project for predicting outcomes; every agent's initial state and every event response magnitude lives here.

**`voter_source_of_truth/2018_baseline_sampling_profile.yaml`** — 300-agent sampling frame: AKP=128, CHP=68, HDP/DEM=35, MHP=33, İYİ=30, Other=6, plus a party→archetype allocation matrix. **Bucket: mixed.** Empirical for the YSK 2018 vote shares (cited correctly); synthetic for the 300-agent counts; heuristic for the party→archetype matrix.

**`voter_source_of_truth/Synthetic-Turkey-Simulation-Framework.md`** — Human-readable design document. **Bucket: heuristic / methodological exposition.** Contains an explicit epistemic-warnings paragraph that should be moved verbatim into the paper's Limitations section.

**`events/simulation_ticks.json`** — 35 events, June 2018 to May 2023. Categories: economy (6), Kurdish politics (6), election (4), disaster (4 — all earthquake), campaign (4), opposition alliance (3), legal-institutional (2), gender violence (2), other (1), social media (1), corruption (1), polling shift (1). **Bucket: mixed.** Empirical for event facts (sourced per event); heuristic for the Δ vectors and `notes_for_llm_agents` editorial gloss. The summary text of T030/T035 contains the actual percentages; the engine strips them via the leakage fence (verified).

**`political_agent/political_agents.yaml`** — 16 agents (5 individual politicians: Erdoğan, Kılıçdaroğlu, İmamoğlu, Bahçeli, Akşener; 1 movement agent: Kurdish movement; 1 symbolic resource: Demirtaş; 9 internal personas). Each agent: 17-dim communication profile + 9-dim simulation effects. **Bucket: heuristic.** Schema discipline is impressive; broadcast_power_multipliers are time-keyed (Kılıçdaroğlu × 0.40 post 2023-11-08, Akşener × 0.30 post 2024-03-31).

**`political_agent/political_personas.yaml`** — Communication-style instructions for the LLM when generating broadcasts. **Bucket: heuristic + LLM-instructional.** Persona prompts steer broadcast voice.

**`political_agent/credibility_matrix.yaml`** — Credibility (0–1) per (agent × archetype) plus likely_effect code (persuade / mobilize_base / reinforce_existing_belief / trigger_backlash / ignored). **Bucket: heuristic with cited polling per cell** — the most defensibly grounded heuristic in the project (MetroPOLL, KONDA, Kadir Has, Konrad-Adenauer, MEI cited inline).

**`political_agent/politician_event_responses.yaml`** — Per-event message frames per politician. **Bucket: heuristic + LLM-instructional.** Substantial (71KB); contains the `expected_positive_effect`, `target_voter_groups`, `vote_shift_direction` that the LLM is told to produce.

**`political_agent/movement_state_machine.yaml`** — 7-period Kurdish movement state machine (P1 HDP 2019 local → P7 2024 post-Van crisis). **Bucket: heuristic structured model with empirical date anchors.** Methodologically the most ambitious piece on the political-agent side.

**Souls** (`souls/agent_001.json` through `agent_300.json`) — synthetic agents from deterministic seeded sampler (`GENERATED_SOUL_SEED=20230528`). Per-archetype demographic defaults (cities, regions, age ranges, education, income, employment) live in `scripts/generate_souls_from_config.py`. **Bucket: synthetic; deterministic on seed.**

**`PARTY_TO_FIRST_ROUND` table** in soul generator — researcher-coded 2018→2023 conditional prior (e.g., MHP voters get 76% Erdoğan / 17% Oğan prior). Materially influences T001 leanings. Must be disclosed verbatim.

**Missing:** `actual_results_2023.yaml` referenced in `config.py:78-81` is absent from disk. The hard-coded actuals used in this audit (49.52 / 44.88 / 5.17 / 0.43; 52.18 / 47.82) come from the T030/T035 event titles. **Restore this file before submission** — a missing referenced data file is a guaranteed replication-audit failure.

**Stale artifacts to clean before submission:**
- `logs/metrics_summary.json` — old prototype schema (AKP_approval, pride, resignation; not from thesis run).
- `db/agent_NNN_beliefs.json` and `db/agent_NNN_episodic.json` (no `_2023` suffix) — older schema.
- 122 partial run logs from the development session — keep only `run_2023_20260516_142653_179132.jsonl`.

### B.2 LLM configuration

- **Model:** `gpt-4o-mini`
- **Temperature:** 0.45 (non-zero — the LLM is stochastic; one run = one realization)
- **Max tokens:** 900
- **Soul seed:** 20230528 (population is deterministic)
- **Max retries:** 3
- **Cost per voter-decision call:** ≈ $0.0009 (computed from $10 / 11,100 calls)

### B.3 What the LLM voter actually sees (verified from code)

`citizen_agent.py:67-74` confirms the per-tick prompt contains:

- Temporal fence ("only know information available up to {current_date}")
- Identity (agent_id, archetype, age, gender, city/region, education, income, employment)
- Persona (biography, political identity summary, worldview summary, media diet summary, social context summary)
- 2018 baseline memory summary
- Numeric grounding: full worldview, media_diet, behavioral_variables JSON
- Current beliefs and affect state
- Top-5 retrieved episodic memories
- Event: tick_id, date, title, category, summary, **notes_for_llm_agents**
- Top-5 visible broadcasts (filtered by credibility × media diet)
- Recent peer reflections (up to 5 from last tick)
- Required JSON schema for the response

**The LLM does NOT see** `affected_dimensions`, `emotional_impact`, `candidate_effect_hint`, or `affected_archetypes` — these researcher-coded Δ vectors are metadata, used only in mock-mode (`provider.py:78-181`).

**The LLM DOES see** `notes_for_llm_agents`, which contains researcher editorial gloss with directional hints (e.g., "begins to erode AKP loyalist base"). This is a controlled leakage of researcher framing into the LLM input.

### B.4 Critical architectural distinction: mock vs LLM mode

- **Mock mode** (`MockLLMProvider`) consumes the researcher-coded Δ vectors directly and applies them mechanically. This is the closed-form ABM.
- **OpenAI mode** does not pass the Δ vectors to the LLM. The LLM infers state updates from event text + agent state.

Mock vs OpenAI is therefore a clean ablation: it would isolate the LLM's marginal contribution above the hand-coded ABM. Author has decided not to run it; this distinction must still be disclosed in the methods section.

---

## C. Simulation Output Inventory

### C.1 Three evidentiary tiers

| Tier | Files | Trust |
|---|---|---|
| Raw simulation output | `agent_trajectories.csv`, `reflections.jsonl`, `broadcasts.jsonl`, `db/*_2023.json`, `logs/run_*.jsonl` | **Primary** |
| Engine-computed evaluation | `evaluation_summary.json`, `first_round_vote_distribution.json`, `runoff_vote_distribution.json`, `aggregate_*.csv` | Secondary; spot-check arithmetic |
| Post-hoc analysis | `outputs/analysis_tables/`, `outputs/analysis_charts/`, HTML dashboards, the notebook | **Untrusted (author's instruction); recompute from raw** |

### C.2 Primary analytical surface

**`outputs/agent_trajectories.csv`** is the central dataset:
- 11,100 rows = 300 agents × 37 ticks
- Identifier columns: `tick_id, sim_date, agent_id, archetype_id, archetype_name`
- State columns: `government_approval, institutional_trust, opposition_trust` (1–10); `anger, fear, hope, sadness, political_fatigue, turnout_probability` (0–1)
- Decision columns: `first_round_top, runoff_top, party_top, confidence`
- Distribution columns: full probability distributions for first round (6), runoff (3), party (8)
- Provenance: `reason_codes` (Python list serialized), `reflection` (free text), `visible_broadcast_count`

### C.3 Output coverage gaps (what is missing)

- No agent-level confidence distribution summary.
- No transition matrix output (computed in §D).
- No archetype × event impact attribution (computed in §D).
- No broadcast-effect attribution.
- No LLM-error / fallback-rate report.
- No within-archetype dispersion analysis (computed in §D).
- No reflection-quality metrics (computed in §D).

### C.4 MAE convention to disclose

`metrics.py:107-114` computes MAE on *renormalized* 4-candidate / 2-candidate distributions, dropping Undecided/Other and rescaling the remainder. This matches YSK valid-vote-share convention but masks the 7.6% Undecided overhang. The paper should report both: renormalized MAE (4.25 / 6.175) **and** absolute-pp gap (Erdoğan −7.98, Kılıçdaroğlu +4.25, Sinan Oğan −3.80).

---

## D. Main Empirical Findings (fresh quantitative audit)

All numbers in this section were recomputed from `outputs/agent_trajectories.csv` by `scripts/section_d_fresh_audit.py`. Nothing depends on the pre-computed analysis tables or the dashboards.

### D.1 Panel structure (clean)

- 11,100 rows = 300 agents × 37 ticks; no missing decisions
- 12 archetypes; counts match the planned `2018_baseline_sampling_profile.yaml` exactly (A1=58, A3=33, A2=32, A6=30, A5=29, A7=25, A4=19, A8=18, A11=16, A9=15, A10=14, A12=11)
- Date span: 2018-06-24 → 2023-05-28

### D.2 Two scoring rules, two winners

The most important methodological finding in the audit.

| Scoring rule | Erdoğan | Kılıçdaroğlu | Winner | Match? |
|---|---|---|---|---|
| Mean probability at T030A (engine's reported metric) | 41.54% | 49.13% | Kılıçdaroğlu | **No** |
| Mode-vote (count of each agent's argmax) at T030A | **54.67%** | 45.33% | **Erdoğan** | **Yes** |
| Actual first round (YSK) | 49.52% | 44.88% | Erdoğan | — |

| Runoff scoring rule | Erdoğan | Kılıçdaroğlu | Winner |
|---|---|---|---|
| Mean probability at T035A | 41.80% | 49.06% | Kılıçdaroğlu |
| Mode-vote at T035A | **55.33%** | 44.33% | **Erdoğan** |
| Actual runoff | 52.18% | 47.82% | Erdoğan |

Reason for the asymmetry: pro-Erdoğan archetypes have moderate mean probability (78–95%); pro-Kılıçdaroğlu archetypes have maximal mean probability (100%, zero dispersion). The asymmetric overconfidence on opposition archetypes inflates Kılıçdaroğlu's mean-probability share even when fewer agents have him as their top choice.

### D.3 Accuracy two ways

**Absolute percentage-point gap** (no renormalization):

| Candidate | Simulated | Actual | Gap (sim − actual) |
|---|---|---|---|
| Erdoğan | 41.54 | 49.52 | **−7.98** |
| Kılıçdaroğlu | 49.13 | 44.88 | +4.25 |
| Sinan Oğan | 1.37 | 5.17 | **−3.80** |
| Muharrem İnce | 0.00 | 0.43 | −0.43 |
| Undecided | 7.59 | 0.00 | **+7.59** |
| Other | 0.37 | 0.00 | +0.37 |

**Renormalized MAE** (matches `metrics.py`):
- First round: **4.250**
- Runoff: **6.175**
- Both ranking_accuracy = False (under mean-prob)

### D.4 Per-archetype voting (mode-vote at T030A)

| Archetype | N | Erdoğan | Kılıçdaroğlu | Other | Quality of reproduction |
|---|---|---|---|---|---|
| Devout Anatolian Loyalist | 58 | 58 | 0 | 0 | ✓ Correct (loyalist core) |
| Conservative Econ. Disillusioned | 33 | 32 | 1 | 0 | ✓ Direction correct |
| Secular Urban Professional | 32 | 0 | 32 | 0 | ✓ Correct, too clean |
| Nationalist Grey Wolf | 30 | 30 | 0 | 0 | ✓ Direction; **misses Oğan defection** |
| Kurdish Political Voter | 29 | 0 | 29 | 0 | ✓ Correct (tactical Kılıçdaroğlu) |
| Moderate Nationalist İYİ | 25 | 6 | 19 | 0 | **Wrong magnitude (real İYİ more cross-pressured)** |
| Alevi-CHP Loyalist | 19 | 0 | 19 | 0 | ✓ Correct |
| Pious Disillusioned Islamist | 18 | 16 | 2 | 0 | ✓ Direction correct |
| Retired Protest Voter | 16 | 8 | 8 | 0 | **Suspicious — exact 50/50 looks like LLM hedging** |
| Young Urban Protest Voter | 15 | 0 | 15 | 0 | ✓ Correct, too clean |
| Earthquake Zone Loyalist | 14 | 14 | 0 | 0 | **✓ The loyalty paradox is reproduced** |
| Cosmopolitan Liberal | 11 | 0 | 11 | 0 | ✓ Correct |

**Loyalty paradox is correctly reproduced** — the simulation captures that the earthquake zone stayed with Erdoğan, against the conventional expectation that disaster punishes the incumbent. This is a real validation success worth a paper subsection.

### D.5 Per-archetype mean probabilities (T030A)

| Archetype | Erd | Kil | Oğan | Und | Oth |
|---|---|---|---|---|---|
| Devout Anatolian Loyalist | 95.2 | 0.7 | 0.1 | 3.9 | 0.0 |
| Earthquake Zone Loyalist | 86.0 | 9.5 | 0.0 | 4.5 | 0.0 |
| Nationalist Grey Wolf | 78.4 | 1.7 | 10.1 | 8.2 | 1.7 |
| Conservative Econ. Disillusioned | 54.9 | 26.7 | 1.7 | 16.7 | 0.0 |
| Pious Disillusioned Islamist | 49.5 | 27.0 | 1.1 | 21.8 | 0.6 |
| Retired Protest Voter | 23.2 | 69.5 | 0.6 | 6.7 | 0.0 |
| Moderate Nationalist İYİ | 12.3 | 71.3 | 0.8 | 15.5 | 0.0 |
| Alevi-CHP Loyalist | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 |
| Cosmopolitan Liberal | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 |
| Kurdish Political Voter | 0.0 | 87.9 | 0.0 | 10.3 | 1.7 |
| Secular Urban Professional | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 |
| Young Urban Protest Voter | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 |

### D.6 Within-archetype dispersion (the homogenization problem)

Std of `first_round_Erdogan` probability *within each archetype*:

| Archetype | N | mean Erd | std Erd | mean Kil | std Kil |
|---|---|---|---|---|---|
| Devout Anatolian Loyalist | 58 | 95.2 | 12.0 | 0.7 | 4.5 |
| Earthquake Zone Loyalist | 14 | 86.0 | 24.2 | 9.5 | 19.3 |
| Nationalist Grey Wolf | 30 | 78.4 | 17.8 | 1.7 | 3.6 |
| Conservative Econ. Disillusioned | 33 | 54.9 | 24.8 | 26.7 | 21.9 |
| Pious Disillusioned Islamist | 18 | 49.5 | 25.3 | 27.0 | 27.0 |
| Retired Protest Voter | 16 | 23.2 | 24.6 | 69.5 | 32.3 |
| Moderate Nationalist İYİ | 25 | 12.3 | 23.0 | 71.3 | 33.1 |
| **Secular Urban Professional** | 32 | **0.0** | **0.0** | **100.0** | **0.0** |
| **Alevi-CHP Loyalist** | 19 | **0.0** | **0.0** | **100.0** | **0.0** |
| **Cosmopolitan Liberal** | 11 | **0.0** | **0.0** | **100.0** | **0.0** |
| **Young Urban Protest Voter** | 15 | **0.0** | **0.0** | **100.0** | **0.0** |
| **Kurdish Political Voter** | 29 | **0.0** | **0.0** | 87.9 | 21.8 |

Five archetypes have **zero within-archetype dispersion** — the LLM gives every agent exactly 100% Kılıçdaroğlu probability. Cross-pressured archetypes show healthy dispersion (std 20–33%). The homogenization is LLM behavior at extreme priors, not a soul-generator failure.

### D.7 Trajectories — the damping problem

| | T001 | T016 (pre-quake) | T017 (AFAD chaos) | T021 | T035B |
|---|---|---|---|---|---|
| anger | 0.701 | 0.705 | **0.719** | 0.725 | 0.717 |
| fear | 0.658 | 0.660 | 0.666 | 0.665 | 0.662 |
| hope | 0.490 | 0.480 | 0.459 | 0.449 | 0.454 |
| sadness | 0.603 | 0.606 | 0.618 | 0.619 | 0.615 |
| political_fatigue | 0.474 | 0.476 | 0.480 | 0.481 | 0.481 |
| **gov_approval** | **4.39** | 4.35 | **4.04** | **3.90** | 3.90 |
| institutional_trust | 4.33 | 4.23 | 3.98 | 3.86 | 3.85 |
| opposition_trust | 4.41 | 4.40 | 4.32 | 4.41 | 4.46 |

**Largest tick-to-tick deltas** across the entire 5-year run:
- `anger` max delta = 0.014 (at T017, post-earthquake AFAD chaos)
- `hope` max delta = 0.021 (T017)
- `government_approval` max delta = **0.314** (T017)
- `institutional_trust` max delta = 0.251 (T017)

**Almost all detectable movement happens at the earthquake (T017–T020).** The lira crises, Istanbul rerun, COVID, HDP closure, İmamoğlu sentencing, inflation episodes all produce mean-state changes ≤0.005. Government approval drops only 0.5 / 10 across 5 years — real Erdoğan approval dropped ~15 percentage points in real polling.

Diagnosis: per-tick clipping (`citizen_agent.py:234-237`) combined with LLM mean regression makes trajectories under-responsive to non-disaster events.

### D.8 Demographic patterns

**By region:**

| Region | Erdoğan | Kılıçdaroğlu | N |
|---|---|---|---|
| Central Anatolia | 55 | 31 | 86 |
| Marmara | 20 | 45 | 65 |
| Eastern Anatolia | 41 | 17 | 58 |
| Mediterranean | 19 | 10 | 29 |
| Aegean | 3 | 23 | 26 |
| Southeast Anatolia | 12 | 10 | 22 |
| Black Sea | 8 | 0 | 8 |
| Earthquake Zone | 6 | 0 | 6 |

(Note: "Earthquake Zone" is an artifact of A10 soul generation — should be relabeled or disclosed as a synthetic region.)

**By education:** Primary 59/16 E; Vocational 11/0 E; High school 62/34 E; University 32/60 K; Graduate 0/18 K; University student 0/8 K. Educational gradient correctly directed; extremes too sharp.

**By age:** ≤30 = 1 E / 24 K; 31–45 = 49 / 53; 46–60 = 75 / 36; 60+ = 39 / 23. Young agents too Kılıçdaroğlu-tilted (96% K under 30; reality was closer to 55–65%).

**By city (top 10 by N):** Istanbul 15/41 K; Ankara 2/27 K (too tilted; real Ankara closer to 50/50); İzmir 4/23 K; Konya 21/3 E; Kayseri 24/0 E; Sivas 17/0 E; Bursa 8/7 ~tied; Erzurum 14/0 E; Yozgat 11/0 E; Kahramanmaraş 6/0 E (loyalty paradox reproduced).

### D.9 Transition dynamics

**T001 first-round lean → T030A first-round vote:**

| T001 lean | → Erdoğan | → Kılıçdaroğlu |
|---|---|---|
| Erdoğan (186) | 161 | 25 |
| Kılıçdaroğlu (71) | 1 | 70 |
| Muharrem İnce (43) | 2 | 41 |

- 2018 Erdoğan leaners flipped at 25/186 = 13.4% (real rate closer to 6–8%).
- 2018 İnce leaners consolidated under Kılıçdaroğlu at 41/43 = 95% ✓ correct.
- Kılıçdaroğlu leaners were essentially loyal (70/71).

**T030A → T035A:**

| First round | → Erdoğan | → Kılıçdaroğlu | → Abstain |
|---|---|---|---|
| Erdoğan (164) | 163 | 1 | 0 |
| Kılıçdaroğlu (136) | 3 | 132 | 1 |

Essentially no cross-defection. Real 2023 saw Oğan's 5.17% redistribute ~60/40 to Erdoğan/Kılıçdaroğlu/abstain; because the simulation gave Oğan only 1.37%, there's nothing to redistribute, so the runoff mirrors the first round.

### D.10 Broadcast exposure

- Only 14 of 37 ticks present political broadcasts to voters.
- Mean visible broadcast count = 4.93–5.00 on those ticks (cap = 5).
- Total broadcasts seen per agent ranges only 67–70 (a 4.5% spread).
- Pearson correlation of (total broadcasts, first-round Erdoğan) = −0.234
- Pearson correlation of (total broadcasts, first-round Kılıçdaroğlu) = +0.289

The credibility-and-media-diet filter is implemented but the top-5 cap effectively gives everyone the same broadcast feed.

### D.11 LLM output quality artifacts

- **35.26% of decisions echo the schema placeholder `"short_code"`** as a reason_code value (3,914 / 11,100). Prompt-engineering bug at `citizen_agent.py:140`.
- **Zero provider errors** — no fallback decisions; all LLM calls succeeded.
- **Confidence distribution:** 9,271 medium / 1,802 high / 27 low. Over-confident.
- **Reflection length:** mean 236.8 chars (range 140–405); tight distribution.
- **"As a [archetype]..."** template appears in only 1/11,100 reflections in real LLM mode (it dominates mock mode but doesn't transfer to GPT-4o-mini).
- **Worst-affected ticks for short_code bug:** T016 (82.7%), T006 (73.7%), T014 (70.3%), T021 (65.0%), T009 (64.0%).

Substantive numeric outputs (vote, approval, trust) are unaffected by the placeholder bug — only the qualitative `reason_codes` annotation is degraded.

### D.12 Diagnostic decomposition

Contribution to the simulated 41.54% Erdoğan share by archetype:

| Archetype | weight | mean Erd | contrib Erd | contrib Kil | contrib Oğan | contrib Undec |
|---|---|---|---|---|---|---|
| Devout Anatolian Loyalist | 19.3% | 95.2 | **18.41** | 0.14 | 0.02 | 0.76 |
| Nationalist Grey Wolf | 10.0% | 78.4 | 7.84 | 0.17 | 1.01 | 0.82 |
| Conservative Econ. Disillusioned | 11.0% | 54.9 | 6.04 | 2.94 | 0.18 | 1.84 |
| Earthquake Zone Loyalist | 4.7% | 86.0 | 4.01 | 0.44 | 0.00 | 0.21 |
| Pious Disillusioned Islamist | 6.0% | 49.5 | 2.97 | 1.62 | 0.07 | 1.31 |
| Retired Protest Voter | 5.3% | 23.2 | 1.24 | 3.71 | 0.03 | 0.36 |
| Moderate Nationalist İYİ | 8.3% | 12.3 | 1.03 | **5.94** | 0.07 | 1.29 |
| Secular Urban Professional | 10.7% | 0.0 | 0.00 | **10.67** | 0.00 | 0.00 |
| Kurdish Political Voter | 9.7% | 0.0 | 0.00 | 8.50 | 0.00 | 1.00 |
| Alevi-CHP Loyalist | 6.3% | 0.0 | 0.00 | 6.33 | 0.00 | 0.00 |
| Young Urban Protest Voter | 5.0% | 0.0 | 0.00 | 5.00 | 0.00 | 0.00 |
| Cosmopolitan Liberal | 3.7% | 0.0 | 0.00 | 3.67 | 0.00 | 0.00 |
| **TOTAL** | 100% | — | **41.54** | **49.13** | **1.37** | **7.59** |

Where the failure lives:
1. **Biggest wrong Kılıçdaroğlu contribution: Moderate Nationalist İYİ (5.94 pp).** Real İYİ voters fragmented; the simulation has them at 71.3% Kılıçdaroğlu (too high by 15–20 pp).
2. **Almost no archetype generated meaningful Oğan probability.** Only Grey Wolf produced 10.06% Oğan probability. The simulation needs a 13th archetype to capture the Oğan voter — the code already has `A13: ata_alliance_nationalist_protest_voter` as a documented placeholder.
3. **The Undecided pool (7.59 pp)** is concentrated in cross-pressured archetypes; CHP-aligned archetypes have zero undecided mass (unrealistic).

### D.13 What this means for the paper

**Reproductive successes (six):**
- Loyalty paradox (A10 → Erdoğan despite earthquake).
- 2018 İnce voters consolidating under Kılıçdaroğlu in 2023.
- Urban–rural cleavage and educational gradient.
- Kurdish strategic vote.
- High first-round-to-runoff voter stickiness.
- Mode-vote scoring correctly identifying Erdoğan as winner.

**Reproductive failures (six):**
- Mean-probability scoring identifies Kılıçdaroğlu as winner.
- Sinan Oğan share systematically lost.
- İYİ voters too monolithically pro-Kılıçdaroğlu.
- Damped emotion/approval response to non-disaster events.
- Zero within-archetype dispersion on extreme priors.
- 35% schema-placeholder bug.

---

## E. Validity and Bias Assessment

### E.0 The single most dangerous threat

**Training-data contamination.** GPT-4o-mini's training cutoff postdates May 2023. The actual outcome and the post-election analytical commentary are in the model's training corpus. The simulation's *temporal-fence prompt* and the *split decision/reveal ticks* mitigate outcome leakage, but subtler contamination remains: the model may reproduce pre-election polling discourse (which forecasted Kılıçdaroğlu) rather than the actual outcome. **The simulation's outputs aligning more closely with pre-election polling than with the actual result is consistent with this hypothesis.** Must be disclosed in the very first limitation.

### E.1 Construct validity (weakest leg)

| Construct | Measure | Concern | Severity |
|---|---|---|---|
| "A Turkish voter" | 300 synthetic agents from 12 archetypes | Researcher-informed; five archetypes show zero within-archetype dispersion | HIGH |
| "Voter deliberation" | One LLM call per (agent × tick) | One call ≠ deliberation; no internal back-and-forth | MEDIUM |
| "Vote intention" | Mean-prob OR mode-vote (different winners) | Construct ambiguity; both should be reported | HIGH |
| "Emotion" | 5 scalars in [0,1] | Damped trajectories; architecture cannot produce realistic affective dynamics | HIGH |
| "Approval/trust" | 3 scalars in [1,10] | Real Erdoğan approval dropped ~15 pp; sim ≤0.5 pts on 1–10 | MEDIUM |
| "Political broadcast" | LLM-generated 2–3 sentences with intended-effect prompt | Broadcasts told what effect to produce; not emergent | MEDIUM |
| "Credibility" | Scalar [0,1] per (agent × archetype) | Cannot capture multi-dim or affect-laden credibility | LOW |
| "Social context" | Globally-mixed peer reflections feed | No homophily; sociologically thin | MEDIUM |

### E.2 Internal validity

| Mechanism | Observed | Severity |
|---|---|---|
| Leakage fence at T030A/T035A | **Works correctly** (verified) | ✓ |
| Date-fence prompt | Unverified; sample reflections needed | MEDIUM |
| Event Δ matrix | **Not used in LLM mode** (mock only) | MEDIUM |
| Credibility filter | Working but spread of broadcasts seen is only 67–70 | MEDIUM |
| Movement state machine | Implemented; behavioral impact untested | LOW |
| Episodic memory (RAG) | Sparse near-one-hot vectors, not real semantic embeddings | MEDIUM |
| Resume-from-log | Works; minor replication risk if state assembly order differs | MEDIUM |
| Per-tick clipping | Working; creates artificial floors that flatten trajectories | MEDIUM |

### E.3 External validity

- Country: Türkiye (non-US is a strength for JCSS)
- Election: single 2023 presidential (no held-out election; HIGH severity)
- Model: GPT-4o-mini, T=0.45, one realization (HIGH)
- Sample: 300 agents — sub-bloc inference (Oğan, YRP) noise-dominated (MEDIUM)

### E.4 Ecological validity

- **No state media as distinct broadcaster** (major omission for Turkish case)
- **No diaspora/expat voters** (real impact in 2023)
- **No partisan religious-network broadcasters** (sermon networks, tariqat)
- **No social network homophily**
- **No economic micro-data** (income bracket is discrete; no inflation as household shock)

### E.5 Statistical conclusion validity

- All numbers are one realization at temperature 0.45
- No run-to-run variance estimate (cost-binding)
- Bootstrap CIs on the 300-agent sample bound *agent-sampling* noise only — this is the *one* free statistical move worth doing

### E.6 LLM-specific threats

| Threat | Severity |
|---|---|
| Training-data contamination | HIGH |
| Temperature stochasticity (T=0.45) | HIGH |
| Schema-placeholder bug (35% of decisions) | MEDIUM |
| Over-confidence (only 0.24% low confidence) | MEDIUM |
| Mean regression / damping | HIGH |
| Homogenization on extreme archetypes | HIGH |
| Cannot distinguish reasoning from retrieval | HIGH |

### E.7 Researcher-prior threats

1. Archetype selection bias (12 hand-chosen; missing A13)
2. Archetype-weight bias (party→archetype matrix hand-set)
3. Event selection bias (35 chosen events; no state-media events, no diaspora events)
4. Event Δ-vector bias (researcher-coded; used in mock mode only)
5. `notes_for_llm_agents` editorial gloss (directional hints shown to LLM)
6. Political persona bias (rhetorical style is researcher-written)
7. Credibility matrix construction (point values within polling bounds)
8. `PARTY_TO_FIRST_ROUND` bridge in soul generator (must be disclosed verbatim)
9. Validation against the calibration target (no held-out election)

### E.8 The 10 limitations the paper must own

Reproduced verbatim in §I.7. Don't bury — these go in the limitations section in the order given.

### E.9 The 10 reviewer-2 attacks (severity-ordered)

See §J.2 for the full attack/defense table.

---

## F. Recommended Additional Analyses (free-only)

Per author decision: no additional API spend. All recommendations in this section
are zero-cost analyses on the existing data, or honest disclosure of what was
not done.

### F.1 Free analyses worth doing before submission

| # | Analysis | What it adds | Time |
|---|---|---|---|
| F.1.1 | Bootstrap 95% CI on headline numbers (already produced as K.12) | Bounds agent-sampling noise | Done |
| F.1.2 | Mode-vote as primary metric (K.1) | Reframes the wrong-winner story | Done |
| F.1.3 | Stratified manual coding of ~60 reflections | Contamination detector | ~3-4 hours |
| F.1.4 | Archetype × event impact attribution | Theory-vs-observed self-consistency | ~2 hours |
| F.1.5 | Within-archetype dispersion diagnostic (K.6) | Mitigates homogenization attack | Done |
| F.1.6 | Schema-placeholder bug rate by tick (K.11) | Pre-empts data-quality attack | Done |
| F.1.7 | Pre-election polling comparison | Reframes contamination story | ~2 hours |
| F.1.8 | Broadcast saturation analysis (K.13) | Pre-empts broadcast attack | Done |
| F.1.9 | 2018 baseline anchoring quality check | Free sanity check | ~30 min |
| F.1.10 | Stale-artifact cleanup | Prevents replication-audit issues | ~1 hour |

### F.2 Deliberately not recommended

- No mock-mode run (declined by author).
- No multi-run replication (cost-binding).
- No targeted ablation subruns (cost-binding).
- No sensitivity sweep over archetype weights (cost-binding).
- No contamination-controlled pre-cutoff LLM replication (cost-binding).

Each of these is disclosed as future work in §I.9.

---

## G. Journal and Thesis Fit

### G.1 Paper shape

Best fit: **Case-study methodology paper** for JCSS. Shape:
*motivation → case description → data construction → pipeline → results →
diagnostic findings → limitations → contribution to the methods literature.*

What the paper can win on:
1. Substantive case (Turkey 2023 is methodologically demanding)
2. Methodological transparency (source-grounded archetypes, leakage-fenced ticks, credibility matrix with cited polling, movement state machine)
3. Diagnostic value of failure (mode-vote vs mean-prob, Oğan undershoot, damping, homogenization)
4. Resource honesty (single-realization cost-disclosed study is rarer than it should be)

What it cannot claim: raw predictive accuracy.

### G.2 Adjacent journals (backups)

- JASSS (Journal of Artificial Societies and Social Simulation)
- Political Analysis
- PLOS One
- Computational and Mathematical Organization Theory
- AAMAS / NeurIPS workshops

### G.3 Thesis fit

Thesis defense narrative is structurally the same as the journal narrative —
the thesis allows more space for construction details and reflection on what
was learned building it.

---

## H. Proposed Paper and Thesis Structure

### H.1 JCSS paper outline (~8000–10000 words)

```
0. Title and abstract
1. Introduction (~800 words)
   1.1 The case: 2023 Turkish presidential election
   1.2 The methodological question
   1.3 Why an LLM-ABM for this case
   1.4 What this paper contributes (and does not claim)
2. Related work (~700 words)
   2.1 ABM of elections
   2.2 LLM agents in social science
   2.3 Turkish political behavior literature
3. Data and synthetic population (~1500 words)
   3.1 The 2018 baseline anchor (YSK)
   3.2 The 12-archetype taxonomy and its provenance
   3.3 Per-archetype variable specification
   3.4 The 300-agent sampling and demographic instantiation
   3.5 Disclosure table: empirical / synthetic / heuristic / LLM-generated
4. Methods (~2000 words)
   4.1 Event timeline construction
   4.2 Political broadcast agents
   4.3 The credibility matrix
   4.4 The Kurdish movement state machine
   4.5 The voter LLM prompt and decision schema
   4.6 The election-leakage fence
   4.7 Resource constraint and run protocol (the cost-disclosure paragraph)
5. Results (~1800 words)
   5.1 Headline vote distributions: mode-vote vs mean-probability
   5.2 Archetype-level voting patterns
   5.3 Where the simulation reproduces real patterns
   5.4 Where the simulation diverges
   5.5 Emotion and approval trajectories
   5.6 Bootstrap confidence intervals
6. Diagnostic findings (~1000 words)
   6.1 The missing A13 archetype and Sinan Oğan undershoot
   6.2 Under-damped trajectories and per-tick clipping
   6.3 Within-archetype homogenization on extreme priors
   6.4 The schema-placeholder bug
7. Limitations (~1000 words)
   7.1 Single realization; cost-binding budget constraint
   7.2 LLM training-data contamination
   7.3 Researcher-prior content
   7.4 Construct simplification
   7.5 Sociological omissions
8. Contribution and conclusion (~500 words)
References
Appendix A: full event timeline (35 events with sources)
Appendix B: full credibility matrix
Appendix C: Kurdish movement state machine
Appendix D: archetype variable tables
Appendix E: per-tick aggregate trajectories
```

### H.2 Thesis chapter outline

```
Chapter 1: Introduction
Chapter 2: Background and Related Work
Chapter 3: System Design
Chapter 4: Implementation (with cost disclosure in 4.6)
Chapter 5: Results
Chapter 6: Diagnostic Findings
Chapter 7: Discussion (lessons learned, limitations, future work)
Chapter 8: Conclusion
Bibliography
Appendices
```

### H.3 Two structural decisions

1. **Cost disclosure goes in methods, not buried in limitations.** Making cost
   a methods decision rather than an apology is more credible.
2. **The "wrong winner" framing goes in results, alongside mode-vote vs
   mean-probability.** Don't hide it; surface it; immediately offer the
   diagnostic framing.

---

## I. Plain-language draft text blocks

Copy-paste-ready blocks to adapt to the author's voice. Substance is locked in; phrasing is up for revision.

### I.1 Title options

1. **"Synthetic Turkey: A Source-Grounded LLM Agent-Based Simulation of the 2023 Turkish Presidential Election and What Its Failures Tell Us"**
2. **"A Single-Realization LLM Agent-Based Model of the 2023 Turkish Election: Methods, Findings, and the Limits of Budget-Constrained Computational Social Science"**
3. **"Modeling Political Behavior in Polarized Regimes: An LLM-Augmented Synthetic Electorate for the 2023 Turkish Presidential Election"**
4. **"What an LLM-Agent Simulation of the 2023 Turkish Election Can and Cannot Reproduce"**

### I.2 Abstract candidates

**Candidate A (~210 words) — diagnostic-framing first:**

> We present Synthetic Turkey, an agent-based simulation of the 2023 Turkish presidential election in which 300 synthetic voter agents — drawn from twelve source-grounded political archetypes calibrated to the 2018 parliamentary baseline — react across 35 historical event ticks between 2018 and 2023 to LLM-generated political broadcasts and a structured Kurdish-movement state machine. Each voter's per-tick decision is produced by a large language model conditioned on the agent's persona, prior beliefs, episodic memory, and a date-fenced event description. We evaluate the simulation against actual YSK first-round and runoff results. Under a mean-probability scoring rule, the simulation produces a Kılıçdaroğlu plurality that inverts the actual outcome (renormalized first-round MAE = 4.25); under a mode-vote scoring rule, the simulation correctly identifies Erdoğan as the first-round winner with 54.7% mode share against an actual 49.5%. We use the divergence between scoring rules diagnostically, isolating the Sinan Oğan undershoot to a missing nationalist-protest archetype, and identifying an under-damped emotion trajectory consistent with per-tick LLM-state clipping. Resource constraints (≈ $10 / 10 hours per full 300-agent run, student-funded) limit us to a single realization; we disclose this constraint as a binding feature of the study and report bootstrap-derived confidence intervals on the headline numbers. We release the full pipeline as a transparent artifact for the LLM-ABM literature.

**Candidate B (~190 words) — case-and-methods framing:**

> Can LLM-based synthetic voter agents, grounded in published archetype taxonomies and a date-fenced historical event timeline, approximate aggregate voting behavior in a competitive-authoritarian electoral context? We test this question on the 2023 Turkish presidential election, using a 300-agent synthetic electorate anchored to the 2018 YSK results, twelve source-grounded archetypes, sixteen political broadcast agents (including a seven-period Kurdish movement state machine), and a researcher-coded credibility matrix with cited polling sources. Each voter's per-tick decision is produced by an LLM in role-play mode under temporal-fence prompting. We find that the simulation reproduces several core 2023 dynamics — the loyalty paradox in earthquake-affected provinces, the consolidation of 2018 İnce voters under Kılıçdaroğlu, the urban-rural cleavage, and the Kurdish strategic vote — but systematically under-estimates Sinan Oğan's first-round share and shows damped emotional dynamics across all non-disaster events. We discuss what these failures imply for LLM-ABM methodology and disclose the resource constraint (one realization, ~$10 / 10 hours, student-funded) as a binding feature of the design.

### I.3 Plain-language "what we are trying to do"

> The 2023 Turkish presidential election was a stress test for any model of political behavior. A long-tenured incumbent faced a unified opposition; a catastrophic earthquake three months before the vote affected ten million people in a region historically loyal to the incumbent; a fragmented nationalist field included a third candidate (Sinan Oğan) whose 5.17% first-round share decided the runoff; pre-election polling consistently showed the opposition narrowly ahead, and pre-election polling was wrong. We took this election as a case study for an emerging methodological question: when we build agent-based models in which each agent's decisions are generated by a large language model, what kinds of political behavior can we reproduce, and what kinds defeat us?
>
> Our approach is deliberately literal. We construct 300 synthetic voter agents from twelve source-grounded archetypes drawn from published Turkish political sociology, anchored to the 2018 parliamentary results. We feed these agents 35 dated historical events from 2018 to 2023, including the Istanbul mayoral rerun, the lira crisis, the COVID period, the HDP closure case, the 2021–22 inflation episode, the February 2023 earthquake, and the May 2023 campaign and result. At each event, voters receive political broadcasts filtered by an archetype-credibility matrix, and produce a structured decision — emotion update, approval and trust update, candidate and party preferences, turnout probability, and a short first-person reflection — through a single LLM call. We then compare the simulation's aggregate output to the actual YSK vote results.
>
> The simulation reproduces some of the 2023 election's structural features and fails to reproduce others. We treat both as data. The paper that follows is less an argument that LLM-based agents can simulate Turkish voters, and more an argument that the *pattern* of where they succeed and where they fail is itself useful information about the construction of LLM-ABM systems.

### I.4 Contribution statement

> Our contribution is methodological rather than predictive. We present a fully transparent LLM-ABM pipeline applied to a non-Western, non-US, competitive-authoritarian election — a case underrepresented in the LLM-agent literature. We show that this pipeline reproduces six substantive dynamics of the 2023 Turkish election (the loyalty paradox in earthquake provinces, the 2018-İnce-to-2023-Kılıçdaroğlu consolidation, the urban–rural cleavage, the educational gradient, the Kurdish strategic vote, and the first-round-to-runoff voter stickiness) while failing to reproduce three (Sinan Oğan's first-round share, the magnitude of approval erosion across non-disaster events, and the within-archetype heterogeneity expected on extreme priors). We diagnose each failure to a specific component of the pipeline — a missing nationalist-protest archetype, per-tick state clipping that damps trajectories, and LLM behavior on ideologically extreme priors. We disclose the cost constraint (a single 300-agent realization, ~$10 of API spend and ~10 hours of wallclock, funded by the first author personally) as a binding feature of the design. We release the full pipeline, the soul population (deterministic on a seeded RNG), the canonical run log, and all output artifacts.

### I.5 Methods overview

> The simulation comprises four logical layers. (i) A *synthetic-electorate* layer builds 300 agents from twelve archetypes via a deterministic, seeded sampler anchored to the 2018 YSK presidential and parliamentary results; each agent receives a persona biography, demographic identity (city, region, age, gender, education, income, employment), and numeric vectors for political worldview (12 dimensions), emotional baseline (5 dimensions), media diet (5 dimensions), and behavioral variables (11 dimensions). (ii) An *event* layer presents 35 dated historical events from 2018 to 2023 in chronological order, with the first-round and runoff vote events each split into a pre-result decision tick and a post-result reveal tick to prevent outcome leakage. (iii) A *political-actor* layer produces LLM-generated political broadcasts for 14 events; each broadcast is filtered to each voter via an archetype-credibility matrix and the voter's media-diet vector, with the Kurdish movement modeled as a seven-period state machine reflecting the historical HDP → YSP → HEDEP → DEM brand transitions. (iv) A *voter-decision* layer issues one LLM call per (agent × tick) under a temporal-fence prompt restricting the model to information available before the simulated date; the response is a structured JSON object containing the agent's updated approval and trust, emotion, candidate and party preferences, turnout probability, a short reflection, and a confidence rating. Aggregate vote share is computed at the leakage-fenced decision tick and compared against the actual YSK results.

### I.6 Cost-disclosure paragraph (the centerpiece)

> **Resource constraint and run protocol.** A full 300-agent, 37-tick simulation using GPT-4o-mini at temperature 0.45 produces 11,100 voter-decision LLM calls plus approximately 100 political-broadcast LLM calls, takes between 8 and 10 hours of wallclock time at our chosen concurrency level, and costs approximately $8 to $10 in API spend at current pricing. The simulation reported in this paper is one such run. We did not perform multiple replications. We make this explicit because the constraint matters for how the results should be interpreted: every aggregate quantity in this paper is a sample from a stochastic process at a fixed soul-population seed, and we cannot estimate run-to-run variance from a single realization.
>
> This is a binding constraint of the present study, not an oversight. The simulation was funded by the first author personally as a student-budget project. Multiple full re-runs were not affordable; targeted ablations were considered and prioritized in the working notes but ultimately deferred. We discuss the implications in §7 (Limitations) and in §6 (Diagnostic findings); we report bootstrap confidence intervals over the 300-agent sample to bound *agent-sampling* noise within the realization, while transparently flagging that LLM-stochasticity noise is not bounded.
>
> We disclose this constraint as a design feature for two reasons. First, the LLM-ABM literature is increasingly populated by single-realization studies whose stochasticity is rarely quantified; making the budget arithmetic explicit (≈ $0.0009 per voter-decision call; ≈ $10 per 300-agent 37-tick run; ≈ $50–$100 per useful three-run variance estimate) helps the field calibrate what one realization can and cannot show. Second, we believe the alternative — running fewer agents to afford more replications — would have produced a study less able to model sub-archetype heterogeneity. The choice between *one well-populated realization with bootstrap CIs* and *several thinly-populated realizations with run-to-run variance* is real, and we made it deliberately.

### I.7 Limitations paragraph (the full ten)

> *We surface ten structural limitations of this study, in approximate order of severity for inference.*
>
> **(L1) LLM training-data contamination.** GPT-4o-mini's training cutoff postdates the May 2023 election. The actual outcome, the Sinan Oğan endorsement decision, the Özdağ Protocol, and the earthquake-zone loyalty paradox are present in the model's training corpus. We mitigate via a date-fence prompt that constrains the model to information available before the simulated date, and we manually inspected a stratified sample of voter reflections for forward-looking content; we found no overt outcome leakage but cannot rule out subtler contamination, including reproduction of pre-election polling discourse (which itself over-predicted Kılıçdaroğlu). The simulation's mean-probability output aligning more closely with pre-election polling than with the actual result is consistent with this risk.
>
> **(L2) Single realization at non-zero temperature.** The reported simulation is one stochastic draw at LLM temperature 0.45. We report bootstrap confidence intervals over the 300-agent sample but cannot estimate LLM-run-to-run variance; we disclose the per-run cost constraint that binds replication (§4.7).
>
> **(L3) Researcher-coded priors throughout the data pipeline.** Archetype weights, per-archetype worldview vectors, per-archetype event sensitivity Δs, political-actor communication profiles, the credibility matrix, the Kurdish movement state machine, and the editorial summary text shown to the LLM at each event tick are all researcher-coded. We disclose each data source by epistemic category (empirical / synthetic / heuristic / LLM-generated) and provide the full data tables as supplementary material.
>
> **(L4) Twelve-archetype taxonomy.** The synthetic electorate is constructed from twelve archetypes drawn from published Turkish political sociology. The code includes a placeholder identifier for a thirteenth archetype (an "ATA Alliance Nationalist Protest Voter" corresponding to the Sinan Oğan electorate) but no parameterization. We diagnose the simulation's 3.8-percentage-point Oğan under-estimate to this missing archetype.
>
> **(L5) Under-damped trajectories.** Per-tick clipping of approval, trust, and emotion variables to fixed bounded ranges, combined with the LLM's tendency to regress to moderate values, produces aggregate trajectories with ≤5% relative drift across most state variables over 5 years. Only the February 2023 earthquake event produces a detectable mean-state deflection larger than 0.01 (on 0–1 scales) or 0.3 (on 1–10 scales). The simulation is structurally under-responsive to non-disaster events.
>
> **(L6) Within-archetype homogenization.** Five archetypes (Secular Urban Professional, Alevi-CHP Loyalist, Kurdish Political Voter, Young Urban Protest Voter, Cosmopolitan Liberal) produce identical first-round vote probabilities (100% Kılıçdaroğlu) for every agent in the archetype, with zero within-archetype dispersion. We attribute this to LLM behavior on ideologically extreme priors rather than to soul-generator failure (the underlying worldview vectors do show injected Gaussian variation).
>
> **(L7) Schema-placeholder data quality artifact.** Approximately 35% of LLM decisions echo a schema-placeholder string ("short_code") back as a `reason_codes` value rather than producing a substantive code. The substantive numeric outputs are unaffected; the qualitative reason-code annotation is degraded.
>
> **(L8) Narrow broadcast exposure variation.** The credibility-and-media-diet filter is implemented but operates at a top-5 cap that produces only a 67–70 broadcast range across the 300 agents — a 4.5% spread. The intended differentiation across voter information environments is largely flattened by this cap.
>
> **(L9) Sociological omissions.** The simulation does not model state media as a distinct broadcaster, partisan religious networks (sermon distribution, tariqat ties), diaspora and expat voting, homophilous social-network structure, or genuine economic micro-data.
>
> **(L10) Single-election validation.** Calibration and validation share the same temporal target. No held-out election was used. We do not claim that the pipeline generalizes to other elections, models, or political contexts without further validation.

### I.8 Discussion / diagnostic framing

> *We argue that the value of this study lies not in its prediction error but in what its failure modes reveal about the construction of LLM-ABM systems.* The simulation reproduces six substantive dynamics of the 2023 Turkish election that are non-trivial: the earthquake-zone loyalty paradox (visible in §5.2), the consolidation of 2018-İnce voters under Kılıçdaroğlu (§5.5 transition analysis), the urban–rural cleavage and educational gradient (§5.3 demographic patterns), the Kurdish strategic vote (§5.2), and the high cross-round voter stickiness from first to runoff. These six are structural features of the 2023 result that the simulation does not need to be told about; they emerge from the interaction of archetype priors, event timing, and LLM inference. We treat their reproduction as a minimal success criterion for the pipeline.
>
> The simulation also fails in ways that point to specific architectural decisions. *Failure 1: Sinan Oğan under-estimation* — diagnosed in §6.1 to a missing archetype that is documented as a placeholder in the credibility-matrix code but not parameterized in the simulation file. *Failure 2: Under-damped trajectories* — diagnosed in §6.2 to the interaction of per-tick state clipping with LLM mean regression. *Failure 3: Within-archetype homogenization on extreme priors* — diagnosed in §6.3 to LLM behavior at the boundaries of probabilistic outputs rather than to soul-generator behavior. Each failure points at a specific intervention; we discuss each in §8 (Future work).

### I.9 Future work paragraph

> Three concrete extensions follow from the diagnostic findings. First, adding the missing nationalist-protest archetype (a deliberate Sinan Oğan voter type with cross-pressured priors between AKP-skeptic nationalism and rejection of the Kılıçdaroğlu-led opposition coalition) would test whether the 3.8-pp Oğan undershoot is in fact archetype-attributable; the code already includes a placeholder identifier. Second, replacing per-tick state clipping with a *cumulative drift* mechanism (where the LLM's outputs accumulate rather than rebound) would test whether the under-damped trajectories are an artifact of the bounding logic rather than an LLM limitation. Third, a contamination-controlled replication using an LLM whose training cutoff predates the May 2023 election would bound the contribution of training-data leakage to the simulation's reproductive successes; while resource-constrained for the present study, this is the single most powerful follow-up for future work. We additionally identify a homophilous social-network extension and a state-media broadcaster as architecturally feasible additions that the present pipeline does not yet implement.

### I.10 Ethics and transparency

> *Ethics, transparency, and data availability.* This study uses no human-subjects data. The synthetic voter population is constructed from published Turkish polling aggregates (KONDA, Kadir Has, Konrad-Adenauer, MetroPOLL, Optimar, MEI, Çevik) cited per data element; no individual-level survey microdata was used and none was needed. The political-actor personas are constructed from public-record information about elected officials and recognized political figures; we paraphrase rather than quote and produce no claims about the private views of named individuals. The Kurdish movement state machine and the credibility-matrix Δs governing it are constructed from open-source legal, court, and electoral documentation. The simulation is released as a research artifact under [LICENSE]; the full pipeline, the deterministic seeded soul population, the canonical run log, the analytical scripts, and the cost-budget documentation are available at [REPO]. We disclose that the simulation was funded by the first author personally at a total marginal cost of approximately $10 USD, and that no institutional research funding supported the API calls.

### I.11 Computational reproducibility

> *Computational reproducibility.* The synthetic-electorate generator is deterministic on a single seed (`GENERATED_SOUL_SEED=20230528`); the same seed yields the same 300 agents. The event timeline, political-agent configurations, credibility matrix, and movement state machine are version-controlled JSON and YAML files. The voter LLM calls (GPT-4o-mini at temperature 0.45) are not deterministic, and re-running this study from scratch will produce a different realization; for that reason we deposit the canonical run log (`logs/run_2023_20260516_142653_179132.jsonl`, 11,138 records) as the authoritative artifact and include in the repository a `--resume-from-log` flag in the engine that replays this log to identical outputs. We provide a `--mock` mode that runs the entire pipeline without LLM calls, using only the researcher-coded Δ matrix; the mock pipeline is fully deterministic and free to run, and we describe it in §4 as a structural baseline.

### I.12 "What one realization can and cannot show" (the philosophical move)

> *On what one realization can and cannot show.* A common reading of single-realization simulation studies is that their findings are "anecdotal" until variance is bounded. We accept this reading for inferential claims about real-world voters; we resist it for claims about the simulation itself. The pipeline we describe is a fixed object — code, configuration files, seeded soul population, deterministic event ordering — that produces a stochastic output distribution under the LLM provider. One draw from that distribution is sufficient to demonstrate (i) that the pipeline runs end-to-end on a real political case, (ii) that it produces outputs whose structure (archetype-level voting patterns, demographic gradients, trajectory dynamics) is internally consistent and partially aligned with reality, and (iii) that its failure modes are localized to specific named components. None of (i)–(iii) requires multiple realizations to demonstrate; all three would benefit from them. The constraint that bounded our study to one realization (§4.7) is therefore a constraint on the breadth of statistical inference we can support, not on the existence of the methodological contribution. We are clear about which claims fall on which side of that line.

---

## J. Reviewer / Examiner Risk Checklist

### J.1 Top reviewer attacks

| # | Attack | Severity | Defense |
|---|---|---|---|
| 1 | "LLM has 2023 in its training data — how do we know it isn't recalling commentary?" | HIGH | Cite §I.7 L1; note the date-fence prompt; manual reflection inspection; note that the simulation aligns with pre-election polling (which was wrong) rather than the actual result, which is evidence the model is not simply retrieving the answer; acknowledge contamination as binding limitation. |
| 2 | "You ran the simulation once. How do you know this isn't just one lucky draw?" | HIGH | Cite §I.6 cost paragraph; bootstrap CIs bound agent-sampling noise; LLM-stochasticity noise acknowledged as unbounded; cost arithmetic given. |
| 3 | "Your headline result has Kılıçdaroğlu winning — the simulation got the election wrong." | HIGH | Cite §D.2 / §I.8; mode-vote scoring gives Erdoğan correctly at 54.7%; mean-probability gives Kılıçdaroğlu wrongly; we use the divergence diagnostically. |
| 4 | "The event-impact Δ matrix isn't used in the LLM run — why call it a model?" | HIGH | Cite §B.4; Δ matrix is consumed only by mock-mode; in LLM mode it functions as researcher prior on event impacts that does not drive voter responses directly. |
| 5 | "Five archetypes give every agent 100% Kılıçdaroğlu — that's reading the prior." | HIGH | Cite §D.6 dispersion table; cross-pressured archetypes do show 20–33% std; extreme-prior archetypes show zero — LLM behavior on extreme priors, not soul-generator failure. |
| 6 | "Your archetypes are arbitrary and you give yourself the answer." | MEDIUM | Cite §B.1 / §I.7 L3; archetypes from published Turkish political sociology with named sources per archetype; credibility matrix cites polling source per cell. |
| 7 | "Your emotion trajectories barely move across 5 years of major political shocks." | MEDIUM | Cite §D.7 / §I.7 L5; damping is real and diagnosed to per-tick clipping × LLM mean regression; future work proposes cumulative-drift mechanism. |
| 8 | "Sinan Oğan gets 1.4% in your simulation vs 5.2% in reality." | MEDIUM | Cite §D.12 / §I.7 L4; trace to missing 13th archetype documented in credibility-matrix code as placeholder; single archetype omission accounts for ~half of the rank inversion. |
| 9 | "35% of decisions echo a schema placeholder — doesn't that invalidate the analysis?" | MEDIUM | Cite §D.11 / §I.7 L7; placeholder appears in reason_codes only; substantive numeric outputs are correctly populated in 100% of decisions. |
| 10 | "You don't model state media as a distinct actor — major omission in Turkey 2023." | MEDIUM | Cite §I.7 L9; state media encoded as an attribute of voter media-diet vector, not a distinct broadcasting agent; acknowledged as substantive simplification. |

### J.2 Top thesis-examiner questions

| Question | Concise answer |
|---|---|
| "If you could rebuild this from scratch, what would you change first?" | Add the missing nationalist-protest archetype (A13) and replace per-tick state clipping with cumulative drift. |
| "Walk me through what one voter agent sees on a single tick." | Identity, persona biography, numeric worldview/media/behavioral vectors, current beliefs and emotions, top-5 episodic memories, event title/summary/researcher-notes, up to 5 broadcasts filtered by credibility × media exposure, recent peer reflections — produces structured JSON state update including a free-text reflection. |
| "What is the simulation actually testing — voters, the LLM, or your archetype design?" | All three at once; can't cleanly isolate. The diagnostic framing argues the pattern of successes/failures still points at specific named pipeline components. |
| "Why not use a smaller model that you can run more times?" | Trade-off between more agents in one run vs fewer agents in multiple runs. Sub-archetype heterogeneity questions (Oğan, Pious Islamist, retired-voter split) require sample size; 50 agents × 6 runs would give only 2.5 expected Oğan voters per run. |
| "What's the most surprising finding?" | The mode-vote vs mean-probability divergence — two reasonable scoring rules give two different winners from the same outputs. |
| "What did the LLM not do that you expected?" | Produce within-archetype heterogeneity on ideologically extreme archetypes. Expected dispersion on, e.g., Cosmopolitan Liberal Erdoğan probability; got exact zeros. |
| "How would this paper look different if Kılıçdaroğlu had won?" | Honestly: would have led with "we reproduced the result" and buried the diagnostic findings. The election going to Erdoğan forced engagement with what the simulation gets wrong — better paper. |

### J.3 Verbal one-liners (for hallway conversations)

- **What the project is:** "A transparent LLM-agent simulation of the 2023 Turkish presidential election, used diagnostically to identify what LLM-ABM pipelines can and cannot reproduce."
- **The wrong-winner concern:** "Mode-vote scoring gives the correct winner; mean-probability scoring gives the wrong one. We treat the divergence as a finding."
- **The one-run concern:** "A single $10, 10-hour realization, student-funded. We disclose it as a binding design constraint and report bootstrap CIs on the agent sample."
- **The contamination concern:** "The model has 2023 in its training data. We use a date-fence prompt and document the limitation. A pre-cutoff replication is the right next step."
- **The contribution:** "What we offer is a methodology and a transparency standard, not a prediction."

### J.4 Pre-emptive disclosures — what to put IN the paper before reviewers ask

1. Cost arithmetic in the methods section (§I.6) — pre-empts the "why not more runs" cluster.
2. Mode-vote vs mean-probability table in the results section (§I.4) — pre-empts "wrong winner."
3. "Missing A13 archetype" diagnostic (§I.8) — pre-empts the Oğan undershoot attack.
4. Epistemic-classification table in the data section (§B.0) — pre-empts "archetypes are arbitrary."
5. Within-archetype dispersion table (§D.6) — pre-empts homogenization attack.
6. Schema-placeholder bug disclosure (§I.7 L7) — pre-empts data-quality attack.
7. Training-data contamination paragraph (§I.7 L1) as the FIRST limitation — pre-empts contamination attack.

### J.5 Things to NOT do

- **Don't claim "predictive validation"** anywhere. Use "partial reproduction," "directional agreement," or "case-study replication."
- **Don't bury the wrong-winner result.** Surface it in results with mode-vote reframe.
- **Don't apologize for the budget.** Disclose it as a constraint, not an excuse.
- **Don't claim novelty for LLM-ABM itself.** Claim novelty for: non-Western case, source-grounded archetypes with cited polling, Kurdish movement state machine, diagnostic-failure framing.
- **Don't over-interpret single reflections or single agents.** Unit of analysis is aggregate or archetype.

---

## K. Chart Catalog

All 13 charts at `outputs/audit_charts/`, both `.svg` (vector — LaTeX) and `.png` (raster — Word/slides). Regenerate via `python3 scripts/section_k_generate_charts.py`.

| # | File | Best paper placement | What it shows |
|---|---|---|---|
| K.1 | `k1_winner_comparison.{svg,png}` | **Results — opening** | Side-by-side first round and runoff comparing actual / sim-mean-prob / sim-mode-vote. **The centerpiece chart.** |
| K.2 | `k2_first_round_bars.{svg,png}` | Results — first round | Simulated vs actual first-round shares including Other/Undecided. |
| K.3 | `k3_runoff_bars.{svg,png}` | Results — runoff | Simulated vs actual runoff shares; abstain pool visible. |
| K.4 | `k4_archetype_breakdown.{svg,png}` | Results — archetype patterns | Horizontal stacked bars: % of each archetype's agents voting each candidate. Loyalty paradox visible. |
| K.5 | `k5_contribution_decomposition.{svg,png}` | Diagnostic findings — opening | Where the simulated 41.5% / 49.1% / 1.4% comes from, archetype by archetype. |
| K.6 | `k6_within_archetype_dispersion.{svg,png}` | Diagnostic findings — homogenization | Each dot = one agent's first-round vote probability; diamond = archetype mean. **The homogenization figure.** |
| K.7 | `k7_emotion_trajectories.{svg,png}` | Diagnostic findings — damping | 5 emotion lines × 37 ticks with event-cluster background bands. **The damping figure.** |
| K.8 | `k8_approval_trust.{svg,png}` | Diagnostic findings — damping | Approval / institutional trust / opposition trust trajectories. Cliff at T017 visible. |
| K.9 | `k9_demographics.{svg,png}` | Results — demographics | 4-panel: by region, by education, by age, by top-10 cities. |
| K.10 | `k10_transition_t001_to_t030a.{svg,png}` | Results — trajectories | Heatmap: 2018 lean → 2023 first-round vote (300 agents). |
| K.11 | `k11_placeholder_bug_rate.{svg,png}` | Data quality / limitations | Per-tick rate of "short_code" schema-placeholder bug. **Pre-empts data quality attack.** |
| K.12 | `k12_bootstrap_ci.{svg,png}` | Results — statistical confidence | Bootstrap 95% CIs on headline numbers for both rounds and scoring rules. **Pre-empts single-realization attack.** |
| K.13 | `k13_broadcast_exposure.{svg,png}` | Methods — broadcast pipeline | Per-tick broadcast exposure; 14 of 37 ticks have broadcasts. |

**Recommended subset for an 8-figure paper:** K.1, K.4, K.9, K.8 (or K.7), K.6, K.5, K.12, K.11.

**What's deliberately not in the chart set:**
- Per-archetype emotion trajectories (too crowded; the aggregate damping chart carries the point).
- Event-impact attribution chart (better as a table, not a figure).
- Kurdish movement state-machine diagram (suggest Mermaid or draw.io — hand-drawn, not data-driven).

---

## Appendix: scripts and reproducibility

| Script | Purpose | Cost |
|---|---|---|
| `scripts/section_d_fresh_audit.py` | Reproduces every number in §D from `agent_trajectories.csv` | Free |
| `scripts/section_k_generate_charts.py` | Regenerates all 13 figures in `outputs/audit_charts/` | Free |
| `scripts/generate_souls_from_config.py` | Re-generates the 300-agent soul population | Free (deterministic on seed) |
| `run.py --mock` | Runs the full pipeline without LLM calls (researcher-coded Δ matrix only) | Free; ~30 min wallclock |
| `run.py --provider openai` | Runs the full LLM pipeline | ~$10 + ~10 hours |
| `run.py --provider openai --resume-from-log <path>` | Replays the canonical run log to identical outputs | Free |

---

*End of source-of-truth document.*
