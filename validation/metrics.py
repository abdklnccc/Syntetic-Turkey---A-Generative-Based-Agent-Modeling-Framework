import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from memory.beliefs import FIRST_ROUND_KEYS, PARTY_KEYS, RUNOFF_KEYS


class MetricsCollector:
    def __init__(self, actual_results: dict[str, Any]):
        self.actual_results = actual_results
        self.trajectories: list[dict[str, Any]] = []
        self.reflections: list[dict[str, Any]] = []
        self.broadcasts: list[dict[str, Any]] = []

    def record_broadcasts(self, tick_id: str, broadcasts: list[dict[str, Any]]) -> None:
        for broadcast in broadcasts:
            self.broadcasts.append({"tick_id": tick_id, **broadcast})

    def record_decision(
        self,
        agent,
        tick: dict[str, Any],
        decision: dict[str, Any],
        visible_broadcasts: list[dict[str, Any]],
    ) -> None:
        row = {
            "tick_id": tick["tick_id"],
            "sim_date": tick["date"],
            "agent_id": agent.agent_id,
            "archetype_id": agent.identity["archetype_id"],
            "archetype_name": agent.identity["archetype_name"],
            "government_approval": decision["government_approval"],
            "institutional_trust": decision["institutional_trust"],
            "opposition_trust": decision["opposition_trust"],
            "anger": decision["anger"],
            "fear": decision["fear"],
            "hope": decision["hope"],
            "sadness": decision["sadness"],
            "political_fatigue": decision["political_fatigue"],
            "turnout_probability": decision["turnout_probability"],
            "first_round_top": max(decision["first_round_vote_intention"], key=decision["first_round_vote_intention"].get),
            "runoff_top": max(decision["runoff_vote_intention"], key=decision["runoff_vote_intention"].get),
            "party_top": max(decision["party_preference"], key=decision["party_preference"].get),
            "confidence": decision["confidence"],
            "reason_codes": decision.get("reason_codes", []),
            "reflection": decision.get("reflection", ""),
            "visible_broadcast_count": len(visible_broadcasts),
        }
        for key, value in decision["first_round_vote_intention"].items():
            row[f"first_round_{key}"] = value
        for key, value in decision["runoff_vote_intention"].items():
            row[f"runoff_{key}"] = value
        for key, value in decision["party_preference"].items():
            row[f"party_{key}"] = value
        self.trajectories.append(row)
        self.reflections.append(
            {
                "tick_id": tick["tick_id"],
                "sim_date": tick["date"],
                "agent_id": agent.agent_id,
                "archetype_id": agent.identity["archetype_id"],
                "reflection": decision["reflection"],
                "reason_codes": decision.get("reason_codes", []),
                "confidence": decision["confidence"],
            }
        )

    def aggregate_candidate_intention(self, tick_id: str, round_name: str) -> dict[str, float]:
        key_prefix = "first_round_" if round_name == "first_round" else "runoff_"
        keys = FIRST_ROUND_KEYS if round_name == "first_round" else RUNOFF_KEYS
        rows = [row for row in self.trajectories if row["tick_id"] == tick_id]
        if not rows:
            return {key: 0.0 for key in keys}
        result = {}
        for key in keys:
            result[key] = round(sum(row[f"{key_prefix}{key}"] for row in rows) / len(rows) * 100, 3)
        return result

    def aggregate_party_preference(self, tick_id: str | None = None) -> dict[str, float]:
        rows = self.trajectories
        if tick_id:
            rows = [row for row in rows if row["tick_id"] == tick_id]
        if not rows:
            return {key: 0.0 for key in PARTY_KEYS}
        latest_by_agent = {}
        for row in rows:
            latest_by_agent[row["agent_id"]] = row
        result = {}
        for key in PARTY_KEYS:
            result[key] = round(sum(row[f"party_{key}"] for row in latest_by_agent.values()) / len(latest_by_agent) * 100, 3)
        return result

    def final_vote_distributions(self) -> tuple[dict[str, float], dict[str, float]]:
        first_tick = "T030A_first_round_vote_decision"
        runoff_tick = "T035A_runoff_vote_decision"
        return (
            self.aggregate_candidate_intention(first_tick, "first_round"),
            self.aggregate_candidate_intention(runoff_tick, "runoff"),
        )

    def evaluation_summary(self) -> dict[str, Any]:
        first_dist, runoff_dist = self.final_vote_distributions()
        first_actual = self.actual_results["first_round"]
        runoff_actual = self.actual_results["runoff"]
        first_keys = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince"]
        runoff_keys = ["Erdogan", "Kilicdaroglu"]
        first_sim = self._normalize_percent({key: first_dist.get(key, 0.0) for key in first_keys}, first_keys)
        runoff_sim = self._normalize_percent({key: runoff_dist.get(key, 0.0) for key in runoff_keys}, runoff_keys)
        first_actual_norm = self._normalize_percent(first_actual, first_keys)
        runoff_actual_norm = self._normalize_percent(runoff_actual, runoff_keys)
        first_mae = sum(abs(first_sim[key] * 100 - first_actual_norm[key] * 100) for key in first_keys) / len(first_keys)
        runoff_mae = sum(abs(runoff_sim[key] * 100 - runoff_actual_norm[key] * 100) for key in runoff_keys) / len(runoff_keys)
        return {
            "first_round_distribution": first_dist,
            "runoff_distribution": runoff_dist,
            "first_round_mae": round(first_mae, 3),
            "runoff_mae": round(runoff_mae, 3),
            "first_round_ranking_accuracy": self._ranking_accuracy(first_sim, first_actual_norm),
            "runoff_ranking_accuracy": self._ranking_accuracy(runoff_sim, runoff_actual_norm),
            "archetype_vote_breakdown": self._archetype_breakdown(),
            "turnout_abstention_estimate": self._turnout_summary(),
            "emotion_trajectories": self._average_series(["anger", "fear", "hope", "sadness", "political_fatigue"]),
            "approval_trust_trajectories": self._average_series(
                ["government_approval", "institutional_trust", "opposition_trust"]
            ),
        }

    def write_outputs(self, output_dir: Path) -> dict[str, Any]:
        output_dir.mkdir(exist_ok=True)
        self._write_csv(output_dir / "agent_trajectories.csv", self.trajectories)
        self._write_aggregate_candidate(output_dir / "aggregate_candidate_intention.csv")
        self._write_aggregate_party(output_dir / "aggregate_party_preference.csv")
        self._write_jsonl(output_dir / "reflections.jsonl", self.reflections)
        self._write_jsonl(output_dir / "broadcasts.jsonl", self.broadcasts)
        first_dist, runoff_dist = self.final_vote_distributions()
        (output_dir / "first_round_vote_distribution.json").write_text(
            json.dumps(first_dist, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (output_dir / "runoff_vote_distribution.json").write_text(
            json.dumps(runoff_dist, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        summary = self.evaluation_summary()
        (output_dir / "evaluation_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return summary

    def _write_csv(self, path: Path, rows: list[dict[str, Any]]) -> None:
        if not rows:
            path.write_text("", encoding="utf-8")
            return
        fields = list(rows[0].keys())
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def _write_jsonl(self, path: Path, rows: list[dict[str, Any]]) -> None:
        with path.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _write_aggregate_candidate(self, path: Path) -> None:
        rows = []
        for tick_id in sorted({row["tick_id"] for row in self.trajectories}):
            first = self.aggregate_candidate_intention(tick_id, "first_round")
            runoff = self.aggregate_candidate_intention(tick_id, "runoff")
            rows.append({"tick_id": tick_id, **{f"first_{k}": v for k, v in first.items()}, **{f"runoff_{k}": v for k, v in runoff.items()}})
        self._write_csv(path, rows)

    def _write_aggregate_party(self, path: Path) -> None:
        rows = []
        for tick_id in sorted({row["tick_id"] for row in self.trajectories}):
            rows.append({"tick_id": tick_id, **self.aggregate_party_preference(tick_id)})
        self._write_csv(path, rows)

    def _ranking_accuracy(self, simulated: dict[str, float], actual: dict[str, float]) -> bool:
        return sorted(simulated, key=simulated.get, reverse=True) == sorted(actual, key=actual.get, reverse=True)

    def _archetype_breakdown(self) -> dict[str, Any]:
        first_rows = [row for row in self.trajectories if row["tick_id"] == "T030A_first_round_vote_decision"]
        runoff_rows = [row for row in self.trajectories if row["tick_id"] == "T035A_runoff_vote_decision"]
        grouped_first: dict[str, list[dict[str, Any]]] = defaultdict(list)
        grouped_runoff: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in first_rows:
            grouped_first[row["archetype_name"]].append(row)
        for row in runoff_rows:
            grouped_runoff[row["archetype_name"]].append(row)
        result = {}
        for archetype in sorted(set(grouped_first) | set(grouped_runoff)):
            first_items = grouped_first.get(archetype, [])
            runoff_items = grouped_runoff.get(archetype, [])
            result[archetype] = {
                "count": len({row["agent_id"] for row in first_items or runoff_items}),
                "first_round_top_counts": self._count_top(first_items, "first_round_top"),
                "runoff_top_counts": self._count_top(runoff_items, "runoff_top"),
            }
        return result

    def _count_top(self, rows: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[row[key]] += 1
        return dict(counts)

    def _turnout_summary(self) -> dict[str, float]:
        if not self.trajectories:
            return {"mean_turnout_probability": 0.0, "mean_abstention_probability": 0.0}
        latest = {}
        for row in self.trajectories:
            latest[row["agent_id"]] = row
        turnout = sum(row["turnout_probability"] for row in latest.values()) / len(latest)
        return {
            "mean_turnout_probability": round(turnout * 100, 3),
            "mean_abstention_probability": round((1.0 - turnout) * 100, 3),
        }

    def _average_series(self, keys: list[str]) -> dict[str, dict[str, float]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in self.trajectories:
            grouped[row["tick_id"]].append(row)
        result = {}
        for tick_id, rows in grouped.items():
            result[tick_id] = {key: round(sum(row[key] for row in rows) / len(rows), 3) for key in keys}
        return result

    def _normalize_percent(self, values: dict[str, Any], keys: list[str]) -> dict[str, float]:
        cleaned = {key: max(0.0, float(values.get(key, 0.0))) for key in keys}
        total = sum(cleaned.values())
        if total <= 0:
            return {key: 1.0 / len(keys) for key in keys}
        return {key: value / total for key, value in cleaned.items()}
