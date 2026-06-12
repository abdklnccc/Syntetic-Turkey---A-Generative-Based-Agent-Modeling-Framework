import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from agents.citizen_agent import TurkishCitizenAgent
from agents.political_broadcast_agent import PoliticalBroadcastAgent
from agents.soul_loader import load_all_souls
from llm.provider import LLMProvider, make_provider
from loaders.config_loader import ConfigBundle, load_all_configs
from validation.metrics import MetricsCollector


def _decision_tick(source: dict[str, Any], tick_id: str, title: str, decision_kind: str) -> dict[str, Any]:
    return {
        "tick_id": tick_id,
        "date": source["date"],
        "date_range": source.get("date_range"),
        "title": title,
        "category": "election_decision",
        "summary": "Synthetic voter decision tick. Actual election result is hidden from agents.",
        "date_fence": f"Only information available before polls close on {source['date']} should be visible to agents.",
        "affected_dimensions": {},
        "emotional_impact": {},
        "candidate_effect_hint": {},
        "affected_archetypes": [],
        "notes_for_llm_agents": (
            "Choose based on persona, memory, media exposure, campaign context, and uncertainty. "
            "Do not mention or infer the actual result."
        ),
        "sources": [],
        "synthetic_decision": True,
        "decision_kind": decision_kind,
        "hidden_result_tick_id": source["tick_id"],
    }


def _reveal_tick(source: dict[str, Any], tick_id: str) -> dict[str, Any]:
    revealed = dict(source)
    revealed["tick_id"] = tick_id
    revealed["synthetic_decision"] = False
    revealed["reveals_result_tick_id"] = source["tick_id"]
    return revealed


def build_election_safe_tick_plan(ticks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for tick in ticks:
        tick_id = tick["tick_id"]
        if tick_id == "T030":
            plan.append(
                _decision_tick(
                    tick,
                    "T030A_first_round_vote_decision",
                    "First-round presidential vote decision",
                    "first_round_vote",
                )
            )
            plan.append(_reveal_tick(tick, "T030B_first_round_result_revealed"))
        elif tick_id == "T035":
            plan.append(
                _decision_tick(
                    tick,
                    "T035A_runoff_vote_decision",
                    "Runoff presidential vote decision",
                    "runoff_vote",
                )
            )
            plan.append(_reveal_tick(tick, "T035B_final_result_revealed"))
        else:
            normal = dict(tick)
            normal["synthetic_decision"] = False
            normal["decision_kind"] = "normal"
            plan.append(normal)
    return plan


def _top_key(values: dict[str, Any]) -> str:
    if not values:
        return "?"
    return max(values, key=values.get)


def format_agent_thought(agent, decision: dict[str, Any], visible_broadcast_count: int) -> str:
    first = _top_key(decision.get("first_round_vote_intention", {}))
    runoff = _top_key(decision.get("runoff_vote_intention", {}))
    party = _top_key(decision.get("party_preference", {}))
    turnout = float(decision.get("turnout_probability", 0.0))
    reflection = str(decision.get("reflection", "")).strip()
    archetype = agent.identity.get("archetype_name", "?")
    return (
        f"  [{agent.agent_id}] {agent.name} | {archetype}\n"
        f"    lean: party={party} first={first} runoff={runoff} "
        f"turnout={turnout:.2f} confidence={decision.get('confidence', '?')} "
        f"broadcasts={visible_broadcast_count}\n"
        f"    reflection: {reflection}"
    )


class TickEngine:
    def __init__(
        self,
        provider: LLMProvider | None = None,
        bundle: ConfigBundle | None = None,
        max_agents: int | None = None,
        max_ticks: int | None = None,
        disable_social: bool = False,
        auto_generate_souls: bool = False,
        output_dir: Path | None = None,
        verbose: bool = True,
        show_agent_thoughts: bool = False,
        agent_selection: str = "diverse",
        run_order: str = "tick",
        parallel_agents: bool = False,
        max_workers: int | None = None,
        continue_on_agent_error: bool = False,
        resume_from_log: Path | str | None = None,
        population_profile: str = "prototype_50",
    ):
        if run_order not in {"tick", "agent"}:
            raise ValueError("run_order must be 'tick' or 'agent'")
        self.bundle = bundle or load_all_configs()
        self.provider = provider or make_provider()
        self.max_agents = max_agents
        self.max_ticks = max_ticks
        self.disable_social = disable_social
        self.auto_generate_souls = auto_generate_souls
        self.output_dir = output_dir or config.OUTPUTS_DIR
        self.verbose = verbose
        self.show_agent_thoughts = show_agent_thoughts
        self.agent_selection = agent_selection
        self.run_order = run_order
        self.parallel_agents = parallel_agents
        self.max_workers = max_workers
        self.continue_on_agent_error = continue_on_agent_error
        self.resume_from_log = Path(resume_from_log) if resume_from_log else None
        self.population_profile = population_profile
        self.agents: dict[str, TurkishCitizenAgent] = {}
        self.broadcast_agent = PoliticalBroadcastAgent(self.bundle, provider=self.provider)
        self.metrics = MetricsCollector(actual_results=self.bundle.actual_results)
        self.log_path = config.LOGS_DIR / f"run_2023_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jsonl"
        self.social_posts: list[str] = []
        self.restored_decisions: set[tuple[str, str]] = set()
        self.restored_social_posts_by_tick: dict[str, list[str]] = defaultdict(list)

    def initialise(self) -> None:
        limit = self.max_agents if self.max_agents is not None else config.NUM_AGENTS
        souls = load_all_souls(
            limit=limit,
            auto_generate=self.auto_generate_souls,
            selection_strategy=self.agent_selection,
            auto_generate_population_profile=self.population_profile,
        )
        self.agents = {
            agent_id: TurkishCitizenAgent(soul, provider=self.provider)
            for agent_id, soul in souls.items()
        }
        if not self.agents:
            raise RuntimeError("No agents initialised")

    def run(self) -> dict[str, Any]:
        self.initialise()
        tick_plan = build_election_safe_tick_plan(self.bundle.simulation_ticks)
        if config.NUM_TICKS:
            tick_plan = tick_plan[: config.NUM_TICKS]
        if self.max_ticks is not None:
            tick_plan = tick_plan[: self.max_ticks]
        if self.resume_from_log:
            if self.run_order != "tick":
                raise RuntimeError("--resume-from-log is only supported with --run-order tick")
            self._restore_from_log(tick_plan)

        self._print(
            f"Running {len(self.agents)} agents across {len(tick_plan)} ticks "
            f"({len(self.agents) * len(tick_plan)} voter decisions, order={self.run_order}, "
            f"parallel_agents={self.parallel_agents})."
        )
        if self.run_order == "agent" and not self.disable_social:
            self._print("Agent-major mode uses empty peer social context to preserve each agent's chronology.")
        if self.run_order == "agent" and self.parallel_agents:
            self._print("Parallel agents is ignored in agent-major mode.")
        if self.run_order == "agent":
            self._run_agent_major(tick_plan)
        else:
            self._run_tick_major(tick_plan)
        summary = self.metrics.write_outputs(self.output_dir)
        self._log({"type": "evaluation_summary", **summary})
        return summary

    def _run_tick_major(self, tick_plan: list[dict[str, Any]]) -> None:
        for index, tick in enumerate(tick_plan, start=1):
            self._run_tick(tick, tick_index=index, total_ticks=len(tick_plan))

    def _run_agent_major(self, tick_plan: list[dict[str, Any]]) -> None:
        broadcast_by_tick: dict[str, list[dict[str, Any]]] = {}
        for tick in tick_plan:
            broadcasts = self.broadcast_agent.broadcasts_for_tick(tick)
            broadcast_by_tick[tick["tick_id"]] = broadcasts
            self.metrics.record_broadcasts(tick["tick_id"], broadcasts)

        total_agents = len(self.agents)
        total_ticks = len(tick_plan)
        for agent_index, agent in enumerate(self.agents.values(), start=1):
            self._print(
                f"[agent {agent_index}/{total_agents}] {agent.agent_id} - "
                f"{agent.identity.get('archetype_name', '')}"
            )
            for tick_index, tick in enumerate(tick_plan, start=1):
                broadcasts = broadcast_by_tick[tick["tick_id"]]
                self._print(
                    f"  [{tick_index}/{total_ticks}] {tick['tick_id']} {tick.get('date', '')} - "
                    f"{tick.get('title', '')} | broadcasts={len(broadcasts)}"
                )
                self._run_agent_tick(agent, tick, broadcasts, social_context=[])
            self._print(f"  completed {total_ticks}/{total_ticks} ticks for {agent.agent_id}")

    def _run_tick(self, tick: dict[str, Any], tick_index: int, total_ticks: int) -> None:
        broadcasts = self.broadcast_agent.broadcasts_for_tick(tick)
        self.metrics.record_broadcasts(tick["tick_id"], broadcasts)
        self._log({"type": "tick_start", "tick_id": tick["tick_id"], "title": tick.get("title"), "broadcast_count": len(broadcasts)})
        self._print(
            f"[{tick_index}/{total_ticks}] {tick['tick_id']} {tick.get('date', '')} - "
            f"{tick.get('title', '')} | broadcasts={len(broadcasts)}"
        )

        restored_posts = list(self.restored_social_posts_by_tick.get(tick["tick_id"], []))
        next_social_posts: list[str] = restored_posts
        total_agents = len(self.agents)
        pending_agents = [
            agent
            for agent in self.agents.values()
            if (tick["tick_id"], agent.agent_id) not in self.restored_decisions
        ]
        restored_count = total_agents - len(pending_agents)
        if restored_count:
            self._print(f"  restored {restored_count}/{total_agents} agents from resume log")
        if not pending_agents:
            self._print(f"  completed {total_agents}/{total_agents} agents")
            if not self.disable_social:
                self.social_posts = next_social_posts[-config.SOCIAL_FEED_SIZE * max(1, len(self.agents)) :]
            return
        if self.parallel_agents:
            next_social_posts.extend(self._run_tick_parallel(tick, broadcasts, pending_agents))
            self._print(f"  completed {total_agents}/{total_agents} agents")
            if not self.disable_social:
                self.social_posts = next_social_posts[-config.SOCIAL_FEED_SIZE * max(1, len(self.agents)) :]
            return

        for agent_index, agent in enumerate(pending_agents, start=1):
            if self.show_agent_thoughts:
                self._print(f"  agent {agent_index}/{len(pending_agents)}: {agent.agent_id}")
            else:
                self._print(f"  agent {agent_index}/{len(pending_agents)}: {agent.agent_id}", end="\r")
            social_context = [] if self.disable_social else self._social_context_for(agent.agent_id)
            decision = self._run_agent_tick(agent, tick, broadcasts, social_context=social_context)
            if not self.disable_social:
                next_social_posts.append(agent.social_summary())
        if not self.show_agent_thoughts:
            self._print(" " * 80, end="\r")
        self._print(f"  completed {total_agents}/{total_agents} agents")
        if not self.disable_social:
            self.social_posts = next_social_posts[-config.SOCIAL_FEED_SIZE * max(1, len(self.agents)) :]

    def _run_tick_parallel(
        self,
        tick: dict[str, Any],
        broadcasts: list[dict[str, Any]],
        agents: list[TurkishCitizenAgent] | None = None,
    ) -> list[str]:
        agents_to_run = agents or list(self.agents.values())
        max_workers = self.max_workers or min(12, max(1, len(agents_to_run)))
        next_social_posts: list[str] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for agent in agents_to_run:
                social_context = [] if self.disable_social else self._social_context_for(agent.agent_id)
                future = executor.submit(
                    self._decide_agent_tick,
                    agent,
                    tick,
                    broadcasts,
                    social_context,
                )
                futures[future] = agent

            completed = 0
            total_agents = len(futures)
            for future in as_completed(futures):
                agent = futures[future]
                try:
                    visible, decision = future.result()
                except Exception as exc:
                    visible, decision = self._handle_agent_error(agent, tick, broadcasts, exc)
                completed += 1
                self._record_agent_decision(agent, tick, visible, decision)
                if self.show_agent_thoughts:
                    self._print(format_agent_thought(agent, decision, len(visible)))
                else:
                    self._print(f"  completed {completed}/{total_agents}: {agent.agent_id}", end="\r")
                if not self.disable_social:
                    next_social_posts.append(agent.social_summary())
        if not self.show_agent_thoughts:
            self._print(" " * 80, end="\r")
        return next_social_posts

    def _run_agent_tick(
        self,
        agent: TurkishCitizenAgent,
        tick: dict[str, Any],
        broadcasts: list[dict[str, Any]],
        social_context: list[str],
    ) -> dict[str, Any]:
        try:
            visible, decision = self._decide_agent_tick(agent, tick, broadcasts, social_context)
        except Exception as exc:
            visible, decision = self._handle_agent_error(agent, tick, broadcasts, exc)
        self._record_agent_decision(agent, tick, visible, decision)
        if self.show_agent_thoughts:
            self._print(format_agent_thought(agent, decision, len(visible)))
        return decision

    def _decide_agent_tick(
        self,
        agent: TurkishCitizenAgent,
        tick: dict[str, Any],
        broadcasts: list[dict[str, Any]],
        social_context: list[str],
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        agent.advance_tick(tick["tick_id"], tick["date"])
        visible = self.broadcast_agent.visible_broadcasts_for_soul(broadcasts, agent.soul, max_items=5)
        decision = agent.decide_after_event(
            event=tick,
            visible_broadcasts=visible,
            social_context=social_context,
            decision_kind=tick.get("decision_kind", "normal"),
        )
        return visible, decision

    def _record_agent_decision(
        self,
        agent: TurkishCitizenAgent,
        tick: dict[str, Any],
        visible: list[dict[str, Any]],
        decision: dict[str, Any],
    ) -> None:
        decision_kind = tick.get("decision_kind", "normal")
        self.metrics.record_decision(agent, tick, decision, visible)
        self._log(
            {
                "type": "decision",
                "tick_id": tick["tick_id"],
                "agent_id": agent.agent_id,
                "decision_kind": decision_kind,
                "decision": decision,
                "visible_broadcasts": visible,
            }
        )

    def _restore_from_log(self, tick_plan: list[dict[str, Any]]) -> None:
        if not self.resume_from_log or not self.resume_from_log.exists():
            raise RuntimeError(f"Resume log not found: {self.resume_from_log}")

        tick_by_id = {tick["tick_id"]: tick for tick in tick_plan}
        restored = 0
        unknown_agents: set[str] = set()
        duplicate_pairs: set[tuple[str, str]] = set()

        with self.resume_from_log.open("r", encoding="utf-8") as fh:
            for line_number, line in enumerate(fh, start=1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Malformed JSON in resume log line {line_number}: {exc}") from exc
                if entry.get("type") != "decision":
                    continue

                tick_id = entry.get("tick_id")
                agent_id = entry.get("agent_id")
                if tick_id not in tick_by_id:
                    continue
                if agent_id not in self.agents:
                    unknown_agents.add(str(agent_id))
                    continue

                pair = (str(tick_id), str(agent_id))
                if pair in self.restored_decisions:
                    duplicate_pairs.add(pair)
                    continue

                tick = tick_by_id[str(tick_id)]
                agent = self.agents[str(agent_id)]
                decision = entry.get("decision")
                if not isinstance(decision, dict):
                    raise RuntimeError(f"Resume log decision missing or malformed at line {line_number}")
                visible = entry.get("visible_broadcasts", [])
                if not isinstance(visible, list):
                    visible = []

                agent.advance_tick(tick["tick_id"], tick["date"])
                restored_decision = agent.apply_decision(
                    event=tick,
                    decision=decision,
                    decision_kind=tick.get("decision_kind", "normal"),
                )
                self.metrics.record_decision(agent, tick, restored_decision, visible)
                self.restored_decisions.add(pair)
                self.restored_social_posts_by_tick[tick["tick_id"]].append(
                    self._social_summary_from_decision(agent, restored_decision)
                )
                restored += 1

        if unknown_agents:
            sample = ", ".join(sorted(unknown_agents)[:5])
            raise RuntimeError(
                f"Resume log contains agent IDs not loaded in this run: {sample}. "
                "Use the same or larger --max-agents/--agent-selection settings as the original run."
            )
        if duplicate_pairs:
            sample = ", ".join(f"{tick}/{agent}" for tick, agent in sorted(duplicate_pairs)[:5])
            raise RuntimeError(f"Resume log contains duplicate agent decisions: {sample}")

        self._print(f"Restored {restored} saved voter decisions from {self.resume_from_log}")

    def _social_summary_from_decision(self, agent: TurkishCitizenAgent, decision: dict[str, Any]) -> str:
        reflection = str(decision.get("reflection", "")).strip()
        return f"{agent.name} ({agent.identity['archetype_name']}): {reflection[:180]}"

    def _handle_agent_error(
        self,
        agent: TurkishCitizenAgent,
        tick: dict[str, Any],
        broadcasts: list[dict[str, Any]],
        exc: Exception,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        message = (
            f"Agent {agent.agent_id} failed on {tick['tick_id']} "
            f"({tick.get('title', '')}): {type(exc).__name__}: {exc}"
        )
        self._log(
            {
                "type": "agent_error",
                "tick_id": tick["tick_id"],
                "agent_id": agent.agent_id,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "continued": self.continue_on_agent_error,
            }
        )
        if not self.continue_on_agent_error:
            raise RuntimeError(message) from exc

        self._print(f"  warning: {message}; using low-confidence fallback")
        visible = self.broadcast_agent.visible_broadcasts_for_soul(broadcasts, agent.soul, max_items=5)
        decision = agent.fallback_decision_after_error(
            event=tick,
            error=exc,
            decision_kind=tick.get("decision_kind", "normal"),
        )
        return visible, decision

    def _social_context_for(self, agent_id: str) -> list[str]:
        if not self.social_posts:
            return []
        return self.social_posts[: config.SOCIAL_FEED_SIZE]

    def _log(self, entry: dict[str, Any]) -> None:
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _print(self, message: str, end: str = "\n") -> None:
        if self.verbose:
            print(message, end=end, flush=True)
