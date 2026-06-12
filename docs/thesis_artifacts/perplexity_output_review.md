# Perplexity Thesis Draft Review

Reviewed file:

`Synthetic Turkey  An LLM-First Agent-Based Simulation of the 2023 Turkish Presidential Election.md`

Review date: 2026-05-16

## Verdict

The Perplexity output is useful as a thesis scaffold. It correctly captures the broad research framing, the LLM-first principle, the 300-agent run, the no-prediction stance, the main result pattern, and the strongest interpretation: the system is a diagnostic research prototype whose aggregate result is imperfect but analytically valuable.

It should not be submitted directly. It contains several implementation inaccuracies, some overconfident literature claims, unstable Perplexity upload links, and a few places where raw and normalized election percentages are mixed together. Treat it as a strong first draft outline, not as the final thesis text.

## Strong Parts To Keep

- The executive summary is very close to the right thesis framing.
- The literature review structure is sensible: ABM, LLM social agents, synthetic respondents, Turkish politics, media/polarization.
- The method chapter captures the core architecture: souls, event ticks, broadcasts, credibility filtering, memory, date fencing, JSON decision schema, evaluation.
- The results chapter correctly foregrounds run integrity: 300 agents, 37 ticks, 11,100 decisions, 0 final provider-error fallbacks.
- The discussion is honest about the main failure: Kılıçdaroğlu over-consolidation and Oğan under-production.
- The limitations section is exactly the right kind of defensive academic framing: single run, API cost, LLM bias, prompt sensitivity, non-representativeness, no prediction claims.

## Must-Fix Technical Issues

### 1. Memory storage is described incorrectly

The draft says each memory entry is appended to the agent soul file. In the actual code, episodic memories are stored in `db/{agent_id}_episodic_2023.json` through `memory/episodic.py`. Soul files are the fixed persona baseline, not the live memory log.

Correct wording:

> Each agent maintains file-backed episodic memory in `db/`, separate from the fixed soul JSON. At each tick, the voter reflection is written as a memory entry and later retrieved through a simple relevance/recency/importance mechanism.

Relevant code:

- `memory/episodic.py`
- `agents/citizen_agent.py`

### 2. Decision schema is simplified incorrectly

The draft describes singular fields such as `vote_intention` and `runoff_intention`. The actual LLM output schema uses probability distributions:

- `party_preference`
- `first_round_vote_intention`
- `runoff_vote_intention`
- scalar trust/emotion/turnout values
- `reason_codes`
- `confidence`
- `reflection`

Correct wording:

> The LLM returns strict JSON containing candidate-level probability distributions for first-round and runoff preferences rather than a single deterministic vote label. Top choices are derived later by aggregation code.

Relevant code:

- `agents/citizen_agent.py`
- `memory/beliefs.py`
- `validation/metrics.py`

### 3. Tick list has inaccuracies

The draft's tick summary compresses or mislabels some ticks. The actual current event timeline is:

- `T001` to `T015`: June 2018 through HDP treasury aid freeze.
- `T016` to `T022`: earthquake sequence.
- `T023` to `T029`: opposition/campaign sequence.
- Synthetic decision/reveal splits:
  - `T030A_first_round_vote_decision`
  - `T030B_first_round_result_revealed`
  - `T035A_runoff_vote_decision`
  - `T035B_final_result_revealed`

Do not say the earthquake sequence starts at `T017`; it starts at `T016`.

Relevant file:

- `events/simulation_ticks.json`

### 4. Result tables mix raw and normalized percentages

The draft sometimes puts raw simulated percentages in the table, then labels the gap as normalized.

Use two clearly separated concepts:

Raw output, including undecided/abstain:

- First round: Erdoğan 41.539, Kılıçdaroğlu 49.133, Oğan 1.372, İnce 0.000, Other 0.367, Undecided 7.589.
- Runoff: Erdoğan 41.801, Kılıçdaroğlu 49.061, Abstain/Invalid/Undecided 9.138.

Valid-vote normalized comparison:

- First round: Erdoğan about 45.1, Kılıçdaroğlu about 53.4, Oğan about 1.5, İnce 0.0.
- Runoff: Erdoğan about 46.0, Kılıçdaroğlu about 54.0.

The MAE values in `evaluation_summary.json` use normalized named-candidate comparisons, not the raw undecided-inclusive values.

Relevant files:

- `outputs/evaluation_summary.json`
- `validation/metrics.py`
- `outputs/synthetic_turkey_results_dashboard.html`

### 5. Broadcast power multipliers after 2023 should be removed or reframed

The draft mentions post-2023 examples such as Kılıçdaroğlu after losing the CHP chair and Akşener after the 2024 local election collapse. These may exist in broader political-agent config, but they are outside the current MVP run, which ends with the 28 May 2023 runoff reveal.

For this thesis, keep the broadcast discussion inside the 2018-2023 simulation window.

### 6. The limitation "simulation window ends before election results" is misleading

The decision prompts end before voters see the relevant election results. But the simulation itself includes result-reveal ticks after decisions:

- `T030B_first_round_result_revealed`
- `T035B_final_result_revealed`

Correct wording:

> The decision ticks are fenced before actual result revelation; actual results are revealed only afterward for reflection and evaluation.

## Must-Fix Citation Issues

### 1. Perplexity upload links are not thesis citations

The references section contains long `ppl-ai-file-upload.s3.amazonaws.com` links to uploaded local project files. These links are temporary, ugly, and not appropriate for a thesis bibliography.

Replace them with either:

- Appendix references, for local project artifacts.
- Repository/file references, if submitting the codebase.
- Proper bibliographic entries for external academic sources.

Example:

> Appendix A: 2018 Baseline Sampling Profile (`voter_source_of_truth/2018_baseline_sampling_profile.yaml`)

### 2. External literature claims need manual verification

The Perplexity draft includes useful literature, but do not trust every source blindly. Before final thesis submission, manually verify:

- Exact paper titles.
- Author names.
- Publication years.
- Whether the paper is peer-reviewed, preprint, blog, or commentary.
- Whether quoted performance numbers are accurate.
- Whether a 2025/2026 source is acceptable for the thesis timeline.

Most important sources to verify carefully:

- Park et al. generative agents.
- Argyle et al. "silicon samples."
- Santurkar et al. synthetic public opinion criticism.
- Taubenfeld et al. LLM debate bias.
- Any FlockVote reference.
- Any source claiming exact Turkish affective polarization or voter loyalty patterns.

### 3. Use stable election-result sources

For the official 2023 result benchmark, cite a stable official or high-quality source, not just the generated project file. The project file can be cited as the internal evaluation configuration, but the official result should be independently sourced.

## Recommended Rewrite Plan

### Step 1: Convert this from "Perplexity draft" to "Chapter skeleton"

Keep the structure:

1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion
6. Limitations
7. Conclusion
8. Appendices

But mark each subsection as one of:

- `KEEP`
- `REWRITE FROM PROJECT FILES`
- `VERIFY WITH LITERATURE`
- `MOVE TO APPENDIX`

### Step 2: Replace all implementation claims with local evidence

Use these local files as the authoritative method evidence:

- `docs/thesis_artifacts/technical_scope_progress_report.md`
- `docs/thesis_artifacts/2018_baseline_300_population.md`
- `docs/thesis_artifacts/300_agent_openai_final_run.md`
- `docs/thesis_artifacts/300_agent_openai_dashboard_interpretation.md`
- `outputs/evaluation_summary.json`
- `outputs/agent_trajectories.csv`
- `events/simulation_ticks.json`
- `agents/citizen_agent.py`
- `simulation/tick_engine.py`
- `validation/metrics.py`

### Step 3: Rebuild the methods chapter directly from the codebase

The methods chapter should describe what the code actually does, not what sounds plausible:

- Config loading.
- Soul generation.
- Soul schema.
- LLM prompt construction.
- Provider abstraction.
- OpenAI model used: `gpt-4o-mini`.
- Election result leakage prevention.
- Broadcast filtering.
- Memory storage in `db/`.
- Metrics export.
- Dashboard generation.

### Step 4: Keep results honest

Use this core sentence:

> The simulation succeeded as an end-to-end LLM-first research pipeline but failed as an accurate aggregate election reproduction, overestimating Kılıçdaroğlu and underestimating both Erdoğan and Oğan.

That sentence is academically stronger than trying to make the result look more accurate than it is.

### Step 5: Turn limitations into contribution

The most thesis-worthy angle is not "the model predicted Turkey." It is:

> A source-grounded LLM voter simulation can produce coherent, inspectable political reasoning, and its aggregate errors reveal where LLM social simulation struggles: nationalist protest behavior, non-Western conservative subjectivity, turnout translation, and prompt-sensitive cross-pressure.

## Suggested Next Artifact

Create a cleaned thesis working draft:

`docs/thesis_artifacts/thesis_working_draft.md`

It should reuse the Perplexity structure but replace the inaccurate method/result claims with code-verified claims from the project. It should also convert Perplexity's temporary links into proper local appendices and stable academic references.

## Bottom Line

This is a good Perplexity output. It is especially useful for discovering the thesis narrative and chapter organization.

But before using it academically:

- Correct the technical mismatches.
- Separate raw vs normalized results.
- Remove unstable Perplexity links.
- Verify external literature manually.
- Rebuild the methodology section from the actual codebase.

After those corrections, this can become a strong thesis draft.
