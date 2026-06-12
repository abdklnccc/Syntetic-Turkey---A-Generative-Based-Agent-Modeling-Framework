import json
from typing import Any

from config import DB_DIR


PARTY_KEYS = ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP", "YRP", "Other", "Undecided"]
FIRST_ROUND_KEYS = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"]
RUNOFF_KEYS = ["Erdogan", "Kilicdaroglu", "Abstain_Invalid_Undecided"]


def clamp01(value: float) -> float:
    return round(min(1.0, max(0.0, float(value))), 6)


def normalize_distribution(values: dict[str, Any] | None, keys: list[str]) -> dict[str, float]:
    values = values or {}
    cleaned = {key: clamp01(float(values.get(key, 0.0))) for key in keys}
    total = sum(cleaned.values())
    if total <= 0:
        return {key: round(1.0 / len(keys), 6) for key in keys}
    return {key: round(value / total, 6) for key, value in cleaned.items()}


class BeliefStore:
    def __init__(self, agent_id: str, soul: dict[str, Any]):
        self.agent_id = agent_id
        self.path = DB_DIR / f"{agent_id}_beliefs_2023.json"
        profile = soul["numeric_profile"]["political_worldview"]
        election = soul["election_2023_state"]
        self.history: list[dict[str, Any]] = []
        self.current: dict[str, Any] = {
            "government_approval": float(profile.get("government_approval", 5.0)),
            "institutional_trust": float(profile.get("institutional_trust", 5.0)),
            "opposition_trust": float(profile.get("opposition_trust", 5.0)),
            "party_preference": normalize_distribution(
                soul["numeric_profile"].get("initial_party_vote_intention"), PARTY_KEYS
            ),
            "first_round_vote_intention": normalize_distribution(
                election.get("first_round_vote_intention"), FIRST_ROUND_KEYS
            ),
            "runoff_vote_intention": normalize_distribution(
                election.get("runoff_vote_intention"), RUNOFF_KEYS
            ),
            "turnout_probability": clamp01(election.get("turnout_probability", 0.75)),
            "current_candidate_preference": election.get("current_candidate_preference", "Undecided"),
            "current_party_preference": election.get("current_party_preference", "Undecided"),
        }

    def update_from_decision(self, decision: dict[str, Any], tick_id: str, sim_date: str) -> None:
        for key in ("government_approval", "institutional_trust", "opposition_trust"):
            if key in decision:
                self.current[key] = round(min(10.0, max(1.0, float(decision[key]))), 6)

        if "party_preference" in decision:
            self.current["party_preference"] = normalize_distribution(decision["party_preference"], PARTY_KEYS)
            self.current["current_party_preference"] = max(
                self.current["party_preference"], key=self.current["party_preference"].get
            )

        if "first_round_vote_intention" in decision:
            self.current["first_round_vote_intention"] = normalize_distribution(
                decision["first_round_vote_intention"], FIRST_ROUND_KEYS
            )
            self.current["current_candidate_preference"] = max(
                self.current["first_round_vote_intention"],
                key=self.current["first_round_vote_intention"].get,
            )

        if "runoff_vote_intention" in decision:
            self.current["runoff_vote_intention"] = normalize_distribution(
                decision["runoff_vote_intention"], RUNOFF_KEYS
            )

        if "turnout_probability" in decision:
            self.current["turnout_probability"] = clamp01(decision["turnout_probability"])

        snapshot = self.snapshot(tick_id=tick_id, sim_date=sim_date)
        snapshot["reason_codes"] = decision.get("reason_codes", [])
        snapshot["confidence"] = decision.get("confidence", "medium")
        self.history.append(snapshot)
        self._save()

    def get(self, key: str, default=None):
        return self.current.get(key, default)

    def to_context_string(self) -> str:
        first = self.current["first_round_vote_intention"]
        runoff = self.current["runoff_vote_intention"]
        return (
            f"Government approval={self.current['government_approval']:.1f}/10; "
            f"institutional trust={self.current['institutional_trust']:.1f}/10; "
            f"opposition trust={self.current['opposition_trust']:.1f}/10; "
            f"party preference={self.current['current_party_preference']}; "
            f"first-round candidate lean={max(first, key=first.get)}; "
            f"runoff lean={max(runoff, key=runoff.get)}; "
            f"turnout probability={self.current['turnout_probability']:.2f}."
        )

    def snapshot(self, tick_id: str, sim_date: str) -> dict[str, Any]:
        return {
            "tick_id": tick_id,
            "sim_date": sim_date,
            "agent_id": self.agent_id,
            **self.current,
        }

    def _save(self) -> None:
        self.path.write_text(
            json.dumps({"current": self.current, "history": self.history}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
