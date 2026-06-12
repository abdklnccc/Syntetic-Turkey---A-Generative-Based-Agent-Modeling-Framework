# Political Broadcast Persona Method Report

Date: 2026-05-22

This document explains the new political-broadcast persona method added after the first 300-agent OpenAI run, what problem it tries to solve, which code and data files are involved, what currently works, what remains incomplete, and how it should be presented in the thesis.

## 1. Why This Change Was Needed

The completed 300-agent OpenAI run showed that the voter-agent layer was technically functional but politically too static in several important places. The most serious broadcast-related weakness was the runoff period. In the original baseline run, the runoff campaign ticks `T031`, `T032`, `T033`, `T034`, and `T035A_runoff_vote_decision` effectively reused the same broad political messaging structure. This made the final two-week campaign feel flat, even though the real 2023 runoff period contained distinct political shocks:

- Kılıçdaroğlu's nationalist and anti-refugee turn.
- Sinan Oğan's endorsement of Erdoğan.
- The Kılıçdaroğlu-Ümit Özdağ protocol.
- Kurdish voter reluctance and turnout anxiety.
- Erdoğan's nationalist consolidation strategy.

This mattered because the 2023 runoff result depended heavily on inter-round nationalist consolidation and Kurdish turnout risk. If each runoff tick gives voters the same broadcast environment, the LLM voter agents have too little differentiated political information to reason from. The simulation can still generate reflections, but it cannot generate strong behavioral movement.

The new method tries to improve this by giving political actors their own source-grounded persona "souls" and allowing an LLM to generate short, event-specific broadcasts in each actor's characteristic rhetorical style.

## 2. Core Method

The new method separates political broadcast generation into three layers.

### 2.1 Structured Political Science Layer

The YAML files still define the controlled research structure:

- Which political agents exist.
- Which agents are active for each event.
- Which voter groups they target.
- What broad message frame they should use.
- What expected political effect the message has.
- Which credibility score each voter archetype assigns to each political actor.

This layer remains deterministic because it is part of the experiment harness, not the voter brain. It prevents free-floating politician chatbots from inventing the political environment.

Relevant files:

- `political_agent/political_agents.yaml`
- `political_agent/politician_event_responses.yaml`
- `political_agent/credibility_matrix.yaml`
- `political_agent/movement_state_machine.yaml`

### 2.2 Political Persona Soul Layer

A new file, `political_agent/political_personas.yaml`, gives each major political speaker a rhetorical persona. Each persona includes:

- `display_name`
- `role`
- `rhetorical_identity`
- `voice`
- `speech_patterns`
- `contextual_guidance`

These are not direct quotations. They are paraphrased rhetorical characterizations intended to help the LLM produce more natural broadcasts. The file explicitly instructs the LLM not to use real direct quotes and not to mention the simulation.

Current persona coverage:

- Recep Tayyip Erdoğan
- Kemal Kılıçdaroğlu
- Ekrem İmamoğlu
- Devlet Bahçeli
- Meral Akşener
- HDP/YSP/DEM Kurdish movement collective voice
- Selahattin Demirtaş
- Pervin Buldan
- Mithat Sancar
- Sırrı Süreyya Önder
- Sinan Oğan

Current limitation: the project has 16 configured political agents in `political_agents.yaml`, but only 11 persona entries. Missing persona entries are:

- `bakirhan_tuncer`
- `bestas_meral_danis`
- `hatimogullari_tulay`
- `kisanak_gultan`
- `turk_ahmet`
- `zeydan_abdullah`

Also, `ogan_sinan` exists in `political_personas.yaml` but is not currently defined as an agent in `political_agents.yaml`, and no response block currently activates him in `politician_event_responses.yaml`.

### 2.3 LLM Broadcast Generation Layer

`agents/political_broadcast_agent.py` now builds a prompt for each active political actor. The prompt includes:

- Speaker identity.
- Event date.
- Current event title and summary.
- Political persona soul.
- Voice and speech patterns.
- Communication profile from `political_agents.yaml`.
- Intended effect and target voter groups from `politician_event_responses.yaml`.
- Kurdish movement state, when relevant.
- A temporal fence: only reference information available on or before the event date.

The LLM must return strict JSON:

```json
{
  "message": "2-3 sentence broadcast",
  "emotional_tone": ["tone1", "tone2"],
  "vote_shift_direction": "direction"
}
```

The generated `message` is then used as the political broadcast seen by voter agents after filtering by media diet and credibility.

## 3. What Changed in the Codebase

| File | Change | Purpose |
| --- | --- | --- |
| `political_agent/political_personas.yaml` | New file with politician persona souls | Gives LLM-generated broadcasts more authentic rhetorical character |
| `config.py` | Added `POLITICAL_PERSONAS_FILE` and `BROADCAST_CACHE_DIR` | Makes persona file and broadcast cache configurable |
| `loaders/config_loader.py` | Added `political_personas` to `ConfigBundle` | Loads persona souls with the rest of the source configs |
| `agents/political_broadcast_agent.py` | Added persona prompt construction, LLM broadcast generation, cache, and `llm_generated` field | Converts static message frames into LLM-generated political broadcasts |
| `simulation/tick_engine.py` | Passes the active provider into `PoliticalBroadcastAgent` | Lets the broadcast layer use the same provider path as voter agents |
| `llm/provider.py` | Mock provider now supports `schema_name == "political_broadcast"` | Allows mock-mode smoke tests without OpenAI calls |

## 4. What Works Right Now

The following parts are currently working:

- `load_all_configs()` successfully loads the new `political_personas.yaml`.
- The bundle contains 11 political persona souls.
- The broadcast agent can be constructed with either no provider, mock provider, or OpenAI provider.
- When a provider is passed, the broadcast agent attempts LLM generation.
- When no provider is passed, the system falls back to the old YAML `message_frame` behavior.
- `MockLLMProvider` returns valid JSON for `schema_name == "political_broadcast"`.
- The system still preserves the voter-side LLM-first principle: voter decisions are still made by the voter LLM using persona, memory, event, broadcasts, social context, and date fence.
- The Kurdish movement still uses `movement_state_machine.yaml` for dynamic party label/state context.

The method is therefore architecturally sound: deterministic code controls who speaks, when they speak, which voters can plausibly see the message, and how outputs are cached; the LLM writes the message text.

## 5. Critical Current Problem: Runoff Keys Are Mapped but Missing

The new `TICK_RESPONSE_MAP` in `agents/political_broadcast_agent.py` maps runoff ticks to separate event keys:

```python
"T031": "E10A_runoff_kilicdaroglu_nationalist_pivot",
"T032": "E10B_runoff_ogan_endorses_erdogan",
"T033": "E10C_runoff_ozdag_protocol_signed",
"T034": "E10D_runoff_kurdish_reluctance",
"T035A_runoff_vote_decision": "E10D_runoff_kurdish_reluctance",
```

This is the right design direction. However, the corresponding YAML event blocks do **not** currently exist in `political_agent/politician_event_responses.yaml`.

Current verification result:

| Tick | Mapped response key | Current broadcast count |
| --- | --- | --- |
| T031 | `E10A_runoff_kilicdaroglu_nationalist_pivot` | 0 |
| T032 | `E10B_runoff_ogan_endorses_erdogan` | 0 |
| T033 | `E10C_runoff_ozdag_protocol_signed` | 0 |
| T034 | `E10D_runoff_kurdish_reluctance` | 0 |
| T035A | `E10D_runoff_kurdish_reluctance` | 0 |
| T035B | `E10_2023_presidential_runoff` | 8 |

This means the intended fix for the static runoff is only half implemented. The Python map points to differentiated runoff events, but the YAML source-of-truth file does not yet define those events. As a result, a new full run would currently give no runoff broadcasts for the key decision ticks `T031` through `T035A`.

This must be fixed before another OpenAI run.

## 6. Other Current Limitations and Risks

### 6.1 Sinan Oğan Is Still Not Fully Operational

The persona file contains `ogan_sinan`, but:

- `ogan_sinan` is not in `political_agents.yaml`.
- `ogan_sinan` does not appear in `politician_event_responses.yaml`.
- `ogan_sinan` is not in `credibility_matrix.yaml`.
- No voter archetype currently represents a dedicated ATA/Oğan protest voter.

So the system still cannot properly model the Oğan endorsement cascade. Adding a persona alone is not enough. The simulation also needs:

- A political agent entry for Sinan Oğan.
- A credibility matrix row for Sinan Oğan.
- A T032 response block where he explicitly endorses Erdoğan.
- A voter population segment capable of supporting Oğan in the first round.

### 6.2 Cache Key Is Too Weak

The cache key is currently:

```python
tick_id::agent_id
```

This avoids repeated broadcast calls, which is good for cost. But it does not include:

- Persona file version.
- Event-response version.
- Prompt template version.
- Model name.
- Temperature.

If the persona or response YAML changes, the cache could serve old messages unless manually cleared. For research reproducibility, the cache should include a prompt/config hash or a cache metadata file.

### 6.3 LLM Failure Fallback Is Too Silent

If LLM broadcast generation fails, the code falls back to `message_frame`. This is good for robustness, but it currently hides the failure too much.

Important issue: the exported broadcast currently marks `llm_generated` as `self.provider is not None`. If the provider exists but generation fails and the system falls back to YAML, the flag may still say `llm_generated: true`. That would be misleading in the outputs.

Recommended fix:

- Return a field such as `generation_source: "llm" | "cache" | "yaml_fallback"`.
- Log provider failures.
- Export fallback status into `outputs/broadcasts.jsonl`.

### 6.4 Direct-Quote Risk

The prompt says not to use real direct quotes. This is good. However, the persona file includes some example phrases and rhetorical habits. The method should be described as paraphrased style simulation, not quote reproduction.

For the thesis, avoid saying the broadcasts reproduce real speeches. Better wording:

> Political broadcasts were generated as short, paraphrased rhetorical simulations grounded in structured political-agent profiles, not as direct quotations from real politicians.

### 6.5 Persona Source Grounding Needs Documentation

The voter personas are grounded in the voter source-of-truth files. The political personas are currently rhetorical summaries. They should be presented as expert-coded simulation profiles unless you later attach citations or a speech corpus.

This is acceptable for an MVP thesis if stated clearly, but it is a limitation:

- The personas increase qualitative realism.
- They are not independently validated discourse models.
- They should not be treated as exact replications of real politicians.

### 6.6 Broadcasts Remain Inputs, Not Deterministic Vote Rules

The broadcast system should not mechanically shift votes. It should provide political information to the voter LLM. This preserves the LLM-first rule. Any field such as `vote_shift_direction` should be framed as a grounding hint, not a deterministic transition rule.

## 7. Methodological Interpretation for the Thesis

This correction is best described as an improvement to the information environment of the simulation.

The first OpenAI run showed that voter agents could produce coherent individual reflections, but aggregate movement was too static in the runoff. The broadcast-persona method addresses this by making political communication more event-specific, actor-specific, and rhetorically differentiated.

The methodological contribution is not that political actors become unconstrained chatbots. Instead:

1. YAML files define the controlled political event structure.
2. Persona souls define each actor's rhetorical style.
3. The LLM generates short paraphrased broadcasts within those constraints.
4. Voter agents see only broadcasts made visible by media diet and credibility filtering.
5. Voter agents then reason from those broadcasts in their own LLM decision prompt.

This keeps the simulation LLM-first while avoiding uncontrolled political invention.

## 8. Recommended Fix Order Before Another OpenAI Run

### Priority 1: Add Missing Runoff YAML Blocks

Add these events to `political_agent/politician_event_responses.yaml`:

- `E10A_runoff_kilicdaroglu_nationalist_pivot`
- `E10B_runoff_ogan_endorses_erdogan`
- `E10C_runoff_ozdag_protocol_signed`
- `E10D_runoff_kurdish_reluctance`

Each should contain distinct active broadcasters and message frames. At minimum:

- Erdoğan
- Kılıçdaroğlu
- Bahçeli
- Akşener
- Sinan Oğan for `E10B`
- Kurdish movement / Demirtaş / Buldan for `E10D`

### Priority 2: Fully Add Sinan Oğan as a Political Agent

Add `ogan_sinan` to:

- `political_agent/political_agents.yaml`
- `political_agent/credibility_matrix.yaml`
- `political_agent/politician_event_responses.yaml`

This makes the Oğan endorsement visible as a real political communication event.

### Priority 3: Fix Broadcast Fallback Auditing

Replace the simple `llm_generated` boolean with a clearer field:

```json
{
  "generation_source": "llm | cache | yaml_fallback",
  "generation_error": null
}
```

This protects the thesis from accidentally reporting fallback messages as LLM-generated messages.

### Priority 4: Add Cache Versioning

Cache should be invalidated when any of these change:

- Persona YAML
- Event response YAML
- Prompt template
- OpenAI model
- Temperature

The simplest implementation is to include a short hash in the cache key.

### Priority 5: Add Regression Tests

Add tests asserting:

- `T031`, `T032`, `T033`, `T034`, and `T035A` each emit at least one broadcast.
- `T032` includes `ogan_sinan`.
- Failed LLM generation is exported as YAML fallback, not falsely marked as LLM-generated.
- Mock provider can generate political broadcasts without OpenAI.

## 9. What to Tell the Professor

Suggested concise explanation:

> After analyzing the first full 300-agent run, I found that the voter agents were technically coherent but the runoff information environment was too static. The simulation treated several distinct runoff events as if they had the same political message environment. To correct this, I introduced a political-agent persona layer. Political actors now have rhetorical persona souls, while YAML files still control who speaks, when they speak, and which voter groups are targeted. The LLM generates short paraphrased broadcasts in the actor's style, and voters receive only messages that pass credibility and media-diet filtering. This preserves the LLM-first design because voter decisions are still made by voter-agent reasoning, not deterministic vote shifts. The next required fix is to complete the missing runoff YAML event blocks and fully add Sinan Oğan as an active political agent, because the current code maps runoff ticks to new event keys that are not yet present in the source YAML.

## 10. Current Status

The persona-broadcast architecture is partially implemented and conceptually strong, but not yet ready for a new expensive full OpenAI run.

Working:

- Political persona file exists.
- Config loader loads it.
- Broadcast agent can build LLM prompts.
- Provider is passed into the broadcast agent.
- Mock provider supports broadcast JSON.
- Existing response keys can still produce broadcasts.

Not yet working:

- Differentiated runoff event keys are missing in `politician_event_responses.yaml`.
- T031-T035A currently produce zero broadcasts under the new mapping.
- Sinan Oğan persona exists but is not wired as an active political agent.
- Cache/fallback auditing needs improvement.

Therefore, the next research step should be a small implementation pass and mock verification, not a full OpenAI run.

## 11. Verification Notes

Local checks performed while preparing this report:

- `load_all_configs()` loads successfully.
- `political_personas.yaml` contains 11 persona entries and 339 lines.
- `political_agents.yaml` contains 16 configured political agents.
- Missing persona entries were identified for 6 configured political agents.
- `politician_event_responses.yaml` contains 17 event keys.
- The four new runoff response keys `E10A` through `E10D` are not present.
- Broadcast count check confirmed:
  - `T031`: 0 broadcasts
  - `T032`: 0 broadcasts
  - `T033`: 0 broadcasts
  - `T034`: 0 broadcasts
  - `T035A`: 0 broadcasts
  - `T035B`: 8 broadcasts

These findings should be treated as implementation evidence for the next development task.
