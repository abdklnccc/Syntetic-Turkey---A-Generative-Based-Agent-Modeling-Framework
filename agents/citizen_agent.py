import json
from typing import Any

from llm.provider import LLMProvider
from memory.affective_state import AffectiveState
from memory.beliefs import (
    FIRST_ROUND_KEYS,
    PARTY_KEYS,
    RUNOFF_KEYS,
    BeliefStore,
    normalize_distribution,
)
from memory.episodic import EpisodicMemory


class VoterDecisionError(RuntimeError):
    pass


class TurkishCitizenAgent:
    def __init__(self, soul: dict[str, Any], provider: LLMProvider):
        self.soul = soul
        self.identity = soul["identity"]
        self.persona = soul["persona"]
        self.numeric_profile = soul["numeric_profile"]
        self.agent_id = self.identity["agent_id"]
        self.name = self.identity.get("display_name", self.agent_id)
        self.provider = provider
        self.affect = AffectiveState(baseline=self.numeric_profile.get("emotional_baseline", {}))
        self.episodic = EpisodicMemory(agent_id=self.agent_id)
        self.beliefs = BeliefStore(agent_id=self.agent_id, soul=soul)
        self.current_tick = "T000"
        self.current_date = "2018-06-24"
        self.last_decision: dict[str, Any] | None = None

    def advance_tick(self, tick_id: str, sim_date: str) -> None:
        self.current_tick = tick_id
        self.current_date = sim_date
        numeric_tick = int("".join(ch for ch in tick_id if ch.isdigit()) or 0)
        self.episodic.current_tick = numeric_tick

    def _temporal_fence(self) -> str:
        return (
            f"You are this synthetic voter. You only know information available up to "
            f"the current simulated date: {self.current_date}. Do not use future knowledge. "
            "Stay consistent with your persona, but you may gradually change your views if events affect you."
        )

    def _memory_summary(self) -> str:
        memories = self.episodic.retrieve("recent political events voting decision", n=5)
        if not memories:
            return "No prior simulation memories yet."
        return "\n".join(f"- {m['content']}" for m in memories)

    def _prompt(
        self,
        event: dict[str, Any],
        visible_broadcasts: list[dict[str, Any]],
        social_context: list[str],
        decision_kind: str,
    ) -> str:
        visible = json.dumps(visible_broadcasts, ensure_ascii=False, indent=2)
        social = "\n".join(f"- {item}" for item in social_context) or "No peer context this tick."
        worldview = json.dumps(self.numeric_profile["political_worldview"], ensure_ascii=False)
        media = json.dumps(self.numeric_profile["media_diet"], ensure_ascii=False)
        behavior = json.dumps(self.numeric_profile["behavioral_variables"], ensure_ascii=False)
        event_text = {
            "tick_id": event.get("tick_id"),
            "date": event.get("date"),
            "title": event.get("title"),
            "category": event.get("category"),
            "summary": event.get("summary"),
            "notes_for_llm_agents": event.get("notes_for_llm_agents"),
        }
        return f"""
{self._temporal_fence()}

ROLE
Role-play as the synthetic voter below, not as a political analyst. Reason from their identity, social context, media diet, and memory.

IDENTITY
agent_id: {self.agent_id}
archetype: {self.identity['archetype_id']} - {self.identity['archetype_name']}
age: {self.identity['age']}
gender: {self.identity['gender']}
city/region: {self.identity['city']} / {self.identity['region']}
education: {self.identity['education_level']}
income: {self.identity['income_bracket']}
employment: {self.identity['employment_status']}

PERSONA
biography: {self.persona['short_biography']}
political identity: {self.persona['political_identity_summary']}
worldview summary: {self.persona['worldview_summary']}
media diet summary: {self.persona['media_diet_summary']}
social context summary: {self.persona['social_context_summary']}

2018 BASELINE MEMORY
{self.persona.get('baseline_2018_memory_summary', 'No explicit individual 2018 vote anchor is attached to this soul.')}

NUMERIC GROUNDING
political_worldview: {worldview}
media_diet: {media}
behavioral_variables: {behavior}

CURRENT STATE
{self.beliefs.to_context_string()}
{self.affect.to_context_string()}

SHORT MEMORY
{self._memory_summary()}

CURRENT EVENT
{json.dumps(event_text, ensure_ascii=False, indent=2)}

VISIBLE POLITICAL BROADCASTS
{visible}

VISIBLE PEER SOCIAL CONTEXT
{social}

TASK
Return strict JSON only. No markdown, no commentary.
decision_kind: {decision_kind}

Required schema:
{{
  "reflection": "1-3 sentence first-person reflection",
  "government_approval": 1-10 number,
  "institutional_trust": 1-10 number,
  "opposition_trust": 1-10 number,
  "anger": 0-1 number,
  "fear": 0-1 number,
  "hope": 0-1 number,
  "sadness": 0-1 number,
  "political_fatigue": 0-1 number,
  "party_preference": {{"AKP": number, "CHP": number, "MHP": number, "IYI": number, "DEM_HDP_YSP": number, "YRP": number, "Other": number, "Undecided": number}},
  "first_round_vote_intention": {{"Erdogan": number, "Kilicdaroglu": number, "Sinan_Ogan": number, "Muharrem_Ince": number, "Other": number, "Undecided": number}},
  "runoff_vote_intention": {{"Erdogan": number, "Kilicdaroglu": number, "Abstain_Invalid_Undecided": number}},
  "turnout_probability": 0-1 number,
  "reason_codes": ["short_code"],
  "confidence": "low|medium|high"
}}
""".strip()

    def decide_after_event(
        self,
        event: dict[str, Any],
        visible_broadcasts: list[dict[str, Any]],
        social_context: list[str],
        decision_kind: str = "normal",
    ) -> dict[str, Any]:
        prompt = self._prompt(event, visible_broadcasts, social_context, decision_kind)
        decision = self.provider.complete_json(
            prompt,
            schema_name="voter_decision",
            context={
                "soul": self.soul,
                "event": event,
                "current_beliefs": self.beliefs.current,
                "current_affect": self.affect.to_dict(),
                "visible_broadcasts": visible_broadcasts,
                "decision_kind": decision_kind,
            },
        )
        return self.apply_decision(event, decision, decision_kind)

    def apply_decision(self, event: dict[str, Any], decision: dict[str, Any], decision_kind: str) -> dict[str, Any]:
        decision = self._validate_decision(decision)
        self.beliefs.update_from_decision(decision, tick_id=event["tick_id"], sim_date=event["date"])
        self.affect.update_from_decision(decision)
        self.episodic.observe(
            content=f"[{event['tick_id']}] {event.get('title', '')}: {decision.get('reflection', '')}",
            importance=8.0 if decision_kind != "normal" else 5.0,
            sim_tick=int("".join(ch for ch in event["tick_id"] if ch.isdigit()) or 0),
            source_type="reflection",
            affective_multiplier=1.0,
        )
        self.last_decision = decision
        return decision

    def fallback_decision_after_error(
        self,
        event: dict[str, Any],
        error: Exception,
        decision_kind: str = "normal",
    ) -> dict[str, Any]:
        current = self.beliefs.current
        affect = self.affect.to_dict()
        decision = {
            "reflection": (
                "agent error fallback: LLM provider failed for this tick, so the simulation "
                "preserved this voter's prior belief state and marked confidence low."
            ),
            "government_approval": current["government_approval"],
            "institutional_trust": current["institutional_trust"],
            "opposition_trust": current["opposition_trust"],
            "anger": affect["anger"],
            "fear": affect["fear"],
            "hope": affect["hope"],
            "sadness": affect["sadness"],
            "political_fatigue": affect["political_fatigue"],
            "party_preference": dict(current["party_preference"]),
            "first_round_vote_intention": dict(current["first_round_vote_intention"]),
            "runoff_vote_intention": dict(current["runoff_vote_intention"]),
            "turnout_probability": current["turnout_probability"],
            "reason_codes": ["provider_error", type(error).__name__, decision_kind],
            "confidence": "low",
        }
        return self.apply_decision(event, decision, decision_kind)

    def _validate_decision(self, decision: dict[str, Any]) -> dict[str, Any]:
        required = [
            "reflection",
            "government_approval",
            "institutional_trust",
            "opposition_trust",
            "anger",
            "fear",
            "hope",
            "sadness",
            "political_fatigue",
            "party_preference",
            "first_round_vote_intention",
            "runoff_vote_intention",
            "turnout_probability",
            "reason_codes",
            "confidence",
        ]
        missing = [key for key in required if key not in decision]
        if missing:
            raise VoterDecisionError(f"Decision missing required key(s): {', '.join(missing)}")

        for key in ("government_approval", "institutional_trust", "opposition_trust"):
            decision[key] = round(min(10.0, max(1.0, float(decision[key]))), 6)
        for key in ("anger", "fear", "hope", "sadness", "political_fatigue", "turnout_probability"):
            decision[key] = round(min(1.0, max(0.0, float(decision[key]))), 6)

        decision["party_preference"] = normalize_distribution(decision["party_preference"], PARTY_KEYS)
        decision["first_round_vote_intention"] = normalize_distribution(
            decision["first_round_vote_intention"], FIRST_ROUND_KEYS
        )
        decision["runoff_vote_intention"] = normalize_distribution(decision["runoff_vote_intention"], RUNOFF_KEYS)
        if decision["confidence"] not in {"low", "medium", "high"}:
            decision["confidence"] = "medium"
        if not isinstance(decision["reason_codes"], list):
            decision["reason_codes"] = [str(decision["reason_codes"])]
        return decision

    def social_summary(self) -> str:
        if not self.last_decision:
            return f"{self.name}: no public reaction yet."
        reflection = str(self.last_decision.get("reflection", "")).strip()
        return f"{self.name} ({self.identity['archetype_name']}): {reflection[:180]}"
