import json
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any

import config
from loaders.config_loader import ConfigBundle

if TYPE_CHECKING:
    from llm.provider import LLMProvider


ARCHETYPE_CREDIBILITY_IDS = {
    "A1": "devout_anatolian_loyalist",
    "A2": "secular_urban_professional",
    "A3": "conservative_economically_disillusioned",
    "A4": "alevi_chp_loyalist",
    "A5": "kurdish_political_voter",
    "A6": "nationalist_grey_wolf_core",
    "A7": "moderate_nationalist_opposition",
    "A8": "pious_disillusioned_islamist",
    "A9": "young_urban_protest_voter",
    "A10": "earthquake_zone_loyalist",
    "A11": "retired_protest_voter",
    "A12": "cosmopolitan_liberal_urban_professional",
    "A13": "ata_alliance_nationalist_protest_voter",
}

GOVERNMENT_AGENT_IDS = {"erdogan_recep_tayyip", "bahceli_devlet"}
OPPOSITION_AGENT_IDS = {
    "kilicdaroglu_kemal",
    "imamoglu_ekrem",
    "aksener_meral",
    "kurdish_movement_agent",
    "demirtas_selahattin",
    "buldan_pervin",
    "sancar_mithat",
    "onder_sirri_sureyya",
}

TICK_RESPONSE_MAP = {
    "T004": "E01_2019_istanbul_local",
    "T005": "E02_2019_istanbul_rerun",
    "T007": "E03_2019_kayyum",
    "T022": "E08_2023_earthquakes",
    "T030A_first_round_vote_decision": "E09_2023_presidential_r1",
    "T030B_first_round_result_revealed": "E09_2023_presidential_r1",
    "T031": "E10A_runoff_kilicdaroglu_nationalist_pivot",
    "T032": "E10B_runoff_ogan_endorses_erdogan",
    "T033": "E10C_runoff_ozdag_protocol_signed",
    "T034": "E10D_runoff_kurdish_reluctance",
    "T035A_runoff_vote_decision": "E10D_runoff_kurdish_reluctance",
    "T035B_final_result_revealed": "E10_2023_presidential_runoff",
}


def _parse_date(value: str) -> date:
    return date.fromisoformat(value[:10])


class KurdishMovementAgent:
    def __init__(self, bundle: ConfigBundle):
        self.periods = bundle.movement_state_machine["periods"]

    def state_for_date(self, sim_date: str) -> dict[str, Any]:
        current = _parse_date(sim_date)
        for period_id, period in self.periods.items():
            start = _parse_date(period["start_date"])
            end = _parse_date(period["end_date"])
            if start <= current <= end:
                return {"period_id": period_id, **period}
        return {}


def _build_broadcast_prompt(
    agent_id: str,
    display_name: str,
    persona: dict[str, Any],
    agent_cfg: dict[str, Any],
    response_cfg: dict[str, Any],
    tick: dict[str, Any],
    movement_state: dict[str, Any],
) -> str:
    comm_profile = agent_cfg.get("communication_profile", {})
    # Top 5 communication dimensions this politician favours
    top_dims = sorted(comm_profile.items(), key=lambda x: x[1], reverse=True)[:5]
    top_dims_str = ", ".join(f"{k}({v:.2f})" for k, v in top_dims)

    intended_effect = response_cfg.get("expected_positive_effect", "")
    intended_targets = response_cfg.get("target_voter_groups", [])
    vote_direction = response_cfg.get("vote_shift_direction", "")
    event_date = tick.get("date", "")
    event_title = tick.get("title", "")
    event_summary = tick.get("summary", tick.get("notes_for_llm_agents", ""))

    contextual_hint = ""
    if movement_state and agent_id == "kurdish_movement_agent":
        strategy = movement_state.get("state", {}).get("primary_strategy_state", "")
        party_label = movement_state.get("current_party_label", "")
        contextual_hint = f"\nCurrent party label: {party_label}. Current strategy: {strategy}."

    broadcast_instructions = (
        "Write 2-3 sentences maximum in their characteristic voice. "
        "Do NOT use real direct quotes. Paraphrase authentically in their register. "
        "No simulation meta-language. No markdown. "
        "Only reference information available on or before the event date."
    )

    return f"""You are generating a political broadcast for a simulation of Turkish politics.

SPEAKER: {display_name}
ROLE: {persona.get('role', '')}
EVENT DATE: {event_date}
EVENT: {event_title}
EVENT CONTEXT: {event_summary}{contextual_hint}

RHETORICAL IDENTITY:
{persona.get('rhetorical_identity', '').strip()}

VOICE AND REGISTER:
{persona.get('voice', '').strip()}

SPEECH PATTERNS (use these as style guide):
{chr(10).join('- ' + p for p in persona.get('speech_patterns', []))}

DOMINANT COMMUNICATION DIMENSIONS: {top_dims_str}

INTENDED POLITICAL EFFECT: {intended_effect}
INTENDED TARGET AUDIENCE: {', '.join(intended_targets) if intended_targets else 'general public'}
EXPECTED VOTE SHIFT: {vote_direction}

INSTRUCTIONS: {broadcast_instructions}

Return strict JSON only — no markdown, no commentary:
{{
  "message": "2-3 sentence broadcast in {display_name}'s authentic voice",
  "emotional_tone": ["tone1", "tone2"],
  "vote_shift_direction": "{vote_direction or 'unspecified'}"
}}""".strip()


class PoliticalBroadcastAgent:
    def __init__(
        self,
        bundle: ConfigBundle,
        provider: "LLMProvider | None" = None,
        cache_dir: Path | None = None,
    ):
        self.bundle = bundle
        self.provider = provider
        self.agent_config = bundle.political_agents["agents"]
        self.responses = bundle.politician_event_responses["events"]
        self.credibility = bundle.credibility_matrix["credibility"]
        self.personas = bundle.political_personas.get("personas", {})
        self.kurdish_movement = KurdishMovementAgent(bundle)
        self._cache_path = (cache_dir or config.BROADCAST_CACHE_DIR) / "broadcasts.json"
        self._cache: dict[str, dict[str, Any]] = self._load_cache()

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------

    def _load_cache(self) -> dict[str, dict[str, Any]]:
        if self._cache_path.exists():
            try:
                return json.loads(self._cache_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save_cache(self) -> None:
        self._cache_path.write_text(
            json.dumps(self._cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _cache_key(self, tick_id: str, agent_id: str) -> str:
        return f"{tick_id}::{agent_id}"

    # ------------------------------------------------------------------
    # LLM broadcast generation
    # ------------------------------------------------------------------

    def _generate_message_llm(
        self,
        agent_id: str,
        display_name: str,
        tick: dict[str, Any],
        agent_cfg: dict[str, Any],
        response_cfg: dict[str, Any],
        movement_state: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate an authentic broadcast via LLM, with cache."""
        key = self._cache_key(tick["tick_id"], agent_id)
        if key in self._cache:
            return self._cache[key]

        persona = self.personas.get(agent_id, {})
        if not persona:
            # No persona defined — fall back to YAML message_frame
            return {
                "message": response_cfg.get("message_frame", ""),
                "emotional_tone": response_cfg.get("emotional_tone", []),
                "vote_shift_direction": response_cfg.get("vote_shift_direction", ""),
            }

        prompt = _build_broadcast_prompt(
            agent_id=agent_id,
            display_name=display_name,
            persona=persona,
            agent_cfg=agent_cfg,
            response_cfg=response_cfg,
            tick=tick,
            movement_state=movement_state,
        )

        try:
            result = self.provider.complete_json(
                prompt,
                schema_name="political_broadcast",
                context={"agent_id": agent_id, "tick_id": tick["tick_id"]},
            )
            generated = {
                "message": str(result.get("message", response_cfg.get("message_frame", ""))),
                "emotional_tone": result.get("emotional_tone", response_cfg.get("emotional_tone", [])),
                "vote_shift_direction": result.get(
                    "vote_shift_direction", response_cfg.get("vote_shift_direction", "")
                ),
            }
        except Exception:
            # LLM failed — fall back to YAML message_frame silently
            generated = {
                "message": response_cfg.get("message_frame", ""),
                "emotional_tone": response_cfg.get("emotional_tone", []),
                "vote_shift_direction": response_cfg.get("vote_shift_direction", ""),
            }

        self._cache[key] = generated
        self._save_cache()
        return generated

    # ------------------------------------------------------------------
    # Main broadcast interface
    # ------------------------------------------------------------------

    def broadcasts_for_tick(self, tick: dict[str, Any]) -> list[dict[str, Any]]:
        response_key = self._response_key_for_tick(tick)
        if not response_key:
            return []
        response_event = self.responses.get(response_key, {})
        responses = response_event.get("responses", {})
        movement_state = self.kurdish_movement.state_for_date(tick["date"])
        broadcasts = []
        for agent_id, response_cfg in responses.items():
            if not response_cfg.get("does_agent_broadcast"):
                continue
            agent_cfg = self.agent_config.get(agent_id, {})
            display_name = self._display_name(agent_id)
            party = response_cfg.get("active_label") or agent_cfg.get("party_or_movement", "unknown")
            if agent_id == "kurdish_movement_agent" and movement_state:
                party = response_cfg.get("active_label") or movement_state.get("current_party_label", party)

            if self.provider is not None:
                generated = self._generate_message_llm(
                    agent_id=agent_id,
                    display_name=display_name,
                    tick=tick,
                    agent_cfg=agent_cfg,
                    response_cfg=response_cfg,
                    movement_state=movement_state,
                )
                message = generated["message"]
                emotional_tone = generated["emotional_tone"]
                vote_shift_direction = generated["vote_shift_direction"]
            else:
                message = response_cfg.get("message_frame", "")
                emotional_tone = response_cfg.get("emotional_tone", [])
                vote_shift_direction = response_cfg.get("vote_shift_direction", "")

            broadcasts.append(
                {
                    "tick_id": tick["tick_id"],
                    "source_event_key": response_key,
                    "agent_id": agent_id,
                    "agent_name": display_name,
                    "party_or_movement": party,
                    "message": message,
                    "tone": emotional_tone,
                    "target_voter_groups": response_cfg.get("target_voter_groups", []),
                    "expected_positive_effect": response_cfg.get("expected_positive_effect", ""),
                    "expected_backlash": response_cfg.get("expected_backlash", ""),
                    "vote_shift_direction": vote_shift_direction,
                    "movement_state": {
                        "period_id": movement_state.get("period_id"),
                        "current_party_label": movement_state.get("current_party_label"),
                        "primary_strategy_state": movement_state.get("state", {}).get(
                            "primary_strategy_state"
                        ),
                    }
                    if agent_id == "kurdish_movement_agent"
                    else {},
                    "llm_generated": self.provider is not None,
                }
            )
        return broadcasts

    def visible_broadcasts_for_soul(
        self,
        broadcasts: list[dict[str, Any]],
        soul: dict[str, Any],
        max_items: int = 5,
    ) -> list[dict[str, Any]]:
        archetype_id = soul["identity"]["archetype_id"]
        credibility_id = ARCHETYPE_CREDIBILITY_IDS.get(
            archetype_id, "conservative_economically_disillusioned"
        )
        media_diet = soul["numeric_profile"]["media_diet"]
        scored = []
        for broadcast in broadcasts:
            agent_id = broadcast["agent_id"]
            row = self.credibility.get(agent_id, {}).get(credibility_id, {})
            credibility = float(row.get("credibility", 0.1))
            likely_effect = row.get("likely_effect", "ignored")
            exposure = self._media_exposure(agent_id, media_diet)
            score = credibility * 0.65 + exposure * 0.35
            if likely_effect == "trigger_backlash":
                score += float(media_diet.get("social_media", 0.0)) * 0.08
            scored.append(
                (
                    score,
                    {
                        "agent_name": broadcast["agent_name"],
                        "party_or_movement": broadcast["party_or_movement"],
                        "paraphrased_message": broadcast["message"],
                        "tone": broadcast["tone"],
                        "credibility_score": round(credibility, 3),
                        "likely_effect": likely_effect,
                        "source_agent_id": agent_id,
                    },
                )
            )
        scored.sort(key=lambda item: item[0], reverse=True)
        return [item for _, item in scored[:max_items] if item["credibility_score"] >= 0.05]

    def _response_key_for_tick(self, tick: dict[str, Any]) -> str | None:
        tick_id = tick["tick_id"]
        if tick_id in TICK_RESPONSE_MAP:
            return TICK_RESPONSE_MAP[tick_id]
        title = tick.get("title", "").lower()
        tick_date = _parse_date(tick["date"])
        if "earthquake" in title or "kahramanmaras" in title or "deprem" in title:
            return "E08_2023_earthquakes"
        if tick_date >= date(2023, 5, 1) and "presidential" in title and "first round" in title:
            return "E09_2023_presidential_r1"
        if tick_date >= date(2023, 5, 1) and "runoff" in title:
            return "E10_2023_presidential_runoff"
        return None

    def _display_name(self, agent_id: str) -> str:
        persona = self.personas.get(agent_id, {})
        if persona.get("display_name"):
            return persona["display_name"]
        special = {
            "erdogan_recep_tayyip": "Recep Tayyip Erdoğan",
            "kilicdaroglu_kemal": "Kemal Kılıçdaroğlu",
            "imamoglu_ekrem": "Ekrem İmamoğlu",
            "bahceli_devlet": "Devlet Bahçeli",
            "aksener_meral": "Meral Akşener",
            "kurdish_movement_agent": "Kurdish movement",
            "demirtas_selahattin": "Selahattin Demirtaş",
            "buldan_pervin": "Pervin Buldan",
            "sancar_mithat": "Mithat Sancar",
            "onder_sirri_sureyya": "Sırrı Süreyya Öndər",
            "ogan_sinan": "Sinan Oğan",
        }
        return special.get(agent_id, agent_id.replace("_", " ").title())

    def _media_exposure(self, agent_id: str, media_diet: dict[str, float]) -> float:
        if agent_id in GOVERNMENT_AGENT_IDS:
            return float(media_diet.get("pro_government_media", 0.0))
        if agent_id in {"kurdish_movement_agent", "demirtas_selahattin", "buldan_pervin", "sancar_mithat"}:
            return max(
                float(media_diet.get("alternative_independent_media", 0.0)),
                float(media_diet.get("local_family_networks", 0.0)),
                float(media_diet.get("social_media", 0.0)),
            )
        if agent_id in OPPOSITION_AGENT_IDS:
            return max(
                float(media_diet.get("opposition_media", 0.0)),
                float(media_diet.get("social_media", 0.0)),
            )
        return float(media_diet.get("social_media", 0.0))
