import json
import random
import re
import time
from abc import ABC, abstractmethod
from typing import Any

import config
from memory.beliefs import FIRST_ROUND_KEYS, PARTY_KEYS, RUNOFF_KEYS, normalize_distribution


class LLMProviderError(RuntimeError):
    pass


class LLMProvider(ABC):
    @abstractmethod
    def complete_json(self, prompt: str, *, schema_name: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


def extract_json_object(raw: str) -> dict[str, Any]:
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", clean)
        if not match:
            raise
        return json.loads(match.group())


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str | None = None):
        if not config.OPENAI_API_KEY:
            raise LLMProviderError("OPENAI_API_KEY is required for --provider openai")
        from openai import OpenAI

        self.client = OpenAI(api_key=config.OPENAI_API_KEY, timeout=config.OPENAI_TIMEOUT_SECONDS)
        self.model = model or config.OPENAI_MODEL
        self.max_retries = config.OPENAI_MAX_RETRIES
        self.retry_base_seconds = config.OPENAI_RETRY_BASE_SECONDS

    def complete_json(self, prompt: str, *, schema_name: str, context: dict[str, Any]) -> dict[str, Any]:
        last_error = None
        max_retries = max(1, int(getattr(self, "max_retries", config.OPENAI_MAX_RETRIES)))
        retry_base = max(0.0, float(getattr(self, "retry_base_seconds", config.OPENAI_RETRY_BASE_SECONDS)))
        for attempt in range(max_retries):
            suffix = ""
            if attempt:
                suffix = "\n\nReturn one strict JSON object only. Do not include markdown or commentary."
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt + suffix}],
                    max_tokens=config.OPENAI_MAX_TOKENS,
                    temperature=config.OPENAI_TEMPERATURE,
                )
            except Exception as exc:
                last_error = exc
                if attempt < max_retries - 1:
                    time.sleep(retry_base * (attempt + 1))
                    continue
                break
            raw = response.choices[0].message.content or "{}"
            try:
                return extract_json_object(raw)
            except json.JSONDecodeError as exc:
                last_error = exc
                if attempt < max_retries - 1:
                    time.sleep(retry_base * (attempt + 1))
                    continue
        raise LLMProviderError(
            f"OpenAI completion failed for {schema_name} after {max_retries} attempt(s): {last_error}"
        ) from last_error


class MockLLMProvider(LLMProvider):
    """Valid local substitute for testing. It is not the research voter brain."""

    def __init__(self, seed: int = 20230528):
        self.rng = random.Random(seed)

    def complete_json(self, prompt: str, *, schema_name: str, context: dict[str, Any]) -> dict[str, Any]:
        if schema_name == "political_broadcast":
            return {
                "message": f"[mock broadcast from {context.get('agent_id', 'unknown')} at {context.get('tick_id', '?')}]",
                "emotional_tone": ["neutral"],
                "vote_shift_direction": "unspecified",
            }

        soul = context["soul"]
        current = context["current_beliefs"]
        event = context.get("event", {})
        kind = context.get("decision_kind", "normal")
        profile = soul["numeric_profile"]["political_worldview"]
        behavior = soul["numeric_profile"]["behavioral_variables"]
        emotion = soul["numeric_profile"]["emotional_baseline"]

        party_pref = dict(current.get("party_preference") or soul["numeric_profile"]["initial_party_vote_intention"])
        first_round = dict(current.get("first_round_vote_intention") or soul["election_2023_state"]["first_round_vote_intention"])
        runoff = dict(current.get("runoff_vote_intention") or soul["election_2023_state"]["runoff_vote_intention"])

        hint = event.get("candidate_effect_hint", {})
        affected = event.get("affected_archetypes", [])
        archetype_name = soul["identity"]["archetype_name"]
        salience = 0.05 if archetype_name in affected else 0.02
        if kind in {"first_round_vote", "runoff_vote"}:
            salience += 0.03

        for candidate, delta in hint.items():
            if candidate in first_round:
                first_round[candidate] = max(0.0, first_round[candidate] + float(delta) * salience)
            elif candidate == "Undecided_Abstain":
                first_round["Undecided"] = max(0.0, first_round["Undecided"] + float(delta) * salience)
                runoff["Abstain_Invalid_Undecided"] = max(
                    0.0,
                    runoff["Abstain_Invalid_Undecided"] + float(delta) * salience,
                )

        if event.get("category") == "economy":
            party_pref["AKP"] = max(0.0, party_pref.get("AKP", 0.0) - 0.02 * behavior.get("economic_sensitivity", 0.5))
            party_pref["Undecided"] = party_pref.get("Undecided", 0.0) + 0.015

        if "Kurdish" in event.get("category", "") or "HDP" in event.get("summary", ""):
            if soul["identity"]["archetype_id"] == "A5":
                runoff["Abstain_Invalid_Undecided"] += 0.04 * emotion.get("political_fatigue", 0.5)

        first_round = normalize_distribution(first_round, FIRST_ROUND_KEYS)
        runoff = normalize_distribution(runoff, RUNOFF_KEYS)
        party_pref = normalize_distribution(party_pref, PARTY_KEYS)

        event_emotion = event.get("emotional_impact", {})
        anger = min(1.0, max(0.0, float(emotion.get("anger", 0.4)) + 0.18 * float(event_emotion.get("anger", 0.0))))
        fear = min(1.0, max(0.0, float(emotion.get("fear", 0.4)) + 0.16 * float(event_emotion.get("fear", 0.0))))
        hope = min(1.0, max(0.0, float(emotion.get("hope", 0.4)) + 0.15 * float(event_emotion.get("hope", 0.0))))
        sadness = min(1.0, max(0.0, float(emotion.get("sadness", 0.4)) + 0.14 * float(event_emotion.get("sadness", 0.0))))
        fatigue = min(1.0, max(0.0, float(emotion.get("political_fatigue", 0.4)) + 0.12 * float(event_emotion.get("political_fatigue", 0.0))))

        government_approval = float(profile.get("government_approval", 5.0))
        opposition_trust = float(profile.get("opposition_trust", 5.0))
        institutional_trust = float(profile.get("institutional_trust", 5.0))
        dims = event.get("affected_dimensions", {})
        government_approval = min(10.0, max(1.0, government_approval + float(dims.get("government_approval", 0.0)) * 0.8))
        opposition_trust = min(10.0, max(1.0, opposition_trust + float(dims.get("opposition_trust", 0.0)) * 0.8))
        institutional_trust = min(10.0, max(1.0, institutional_trust + float(dims.get("institutional_trust", 0.0)) * 0.8))

        return {
            "reflection": self._reflection(soul, event, kind),
            "government_approval": round(government_approval, 3),
            "institutional_trust": round(institutional_trust, 3),
            "opposition_trust": round(opposition_trust, 3),
            "anger": round(anger, 6),
            "fear": round(fear, 6),
            "hope": round(hope, 6),
            "sadness": round(sadness, 6),
            "political_fatigue": round(fatigue, 6),
            "party_preference": party_pref,
            "first_round_vote_intention": first_round,
            "runoff_vote_intention": runoff,
            "turnout_probability": min(1.0, max(0.0, float(current.get("turnout_probability", behavior.get("turnout_likelihood", 0.75))))),
            "reason_codes": self._reason_codes(event, soul, kind),
            "confidence": "medium",
        }

    def _reflection(self, soul: dict[str, Any], event: dict[str, Any], kind: str) -> str:
        archetype = soul["identity"]["archetype_name"]
        title = event.get("title", "the current political moment")
        if kind == "first_round_vote":
            return f"As a {archetype}, I am deciding my first-round presidential vote based only on what I know before results are announced."
        if kind == "runoff_vote":
            return f"As a {archetype}, I am weighing the runoff choice before the final result is known."
        return f"As a {archetype}, I react to {title} through my existing identity, media exposure, and lived pressures."

    def _reason_codes(self, event: dict[str, Any], soul: dict[str, Any], kind: str) -> list[str]:
        codes = [event.get("category", "event")]
        if kind != "normal":
            codes.append(kind)
        codes.append(soul["identity"]["archetype_id"])
        return codes


def make_provider(name: str | None = None) -> LLMProvider:
    provider = (name or config.LLM_PROVIDER).lower()
    if provider == "mock":
        return MockLLMProvider()
    if provider == "openai":
        return OpenAIProvider()
    raise LLMProviderError(f"Unsupported provider: {provider}")
