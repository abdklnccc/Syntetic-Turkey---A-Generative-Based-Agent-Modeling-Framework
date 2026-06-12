import json
import os
import shutil
import tempfile
import time
import unittest
from collections import Counter
from pathlib import Path


class ConfigLoaderTests(unittest.TestCase):
    def test_config_fallback_loads_env_file_when_python_dotenv_is_unavailable(self):
        import config

        previous = os.environ.pop("OPENAI_API_KEY", None)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                env_path = Path(tmp) / ".env"
                env_path.write_text(
                    "\n".join(
                        [
                            "# local test env",
                            "OPENAI_API_KEY='sk-test-from-dotenv'",
                            "IGNORED_EMPTY=",
                        ]
                    ),
                    encoding="utf-8",
                )

                config._load_env_file(env_path)

                self.assertEqual(os.environ["OPENAI_API_KEY"], "sk-test-from-dotenv")
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous

    def test_load_all_configs_reads_source_truth_files(self):
        from loaders.config_loader import load_all_configs

        bundle = load_all_configs()

        self.assertEqual(bundle.voter_config["meta"]["prototype_agent_count"], 50)
        self.assertEqual(len(bundle.voter_archetypes), 12)
        self.assertEqual(len(bundle.simulation_ticks), 35)
        self.assertIn("agents", bundle.political_agents)
        self.assertIn("credibility", bundle.credibility_matrix)
        self.assertIn("events", bundle.politician_event_responses)
        self.assertIn("periods", bundle.movement_state_machine)

    def test_load_all_configs_reads_2018_baseline_sampling_profile(self):
        from loaders.config_loader import load_all_configs

        bundle = load_all_configs()
        profile = bundle.baseline_sampling_profile

        self.assertEqual(profile["meta"]["recommended_sample_size"], 300)
        self.assertEqual(sum(profile["recommended_300_agent_party_distribution"].values()), 300)
        self.assertEqual(sum(profile["recommended_300_agent_presidential_distribution"].values()), 300)
        self.assertEqual(sum(profile["recommended_300_agent_archetype_totals"].values()), 300)


class SoulGenerationTests(unittest.TestCase):
    def test_generate_souls_creates_50_json_souls_with_required_schema(self):
        from loaders.config_loader import load_all_configs
        from scripts.generate_souls_from_config import generate_souls

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            souls = generate_souls(load_all_configs(), output_dir=out_dir, seed=12345)

            files = sorted(out_dir.glob("*.json"))
            self.assertEqual(len(files), 50)
            self.assertEqual(len(souls), 50)

            sample = json.loads(files[0].read_text(encoding="utf-8"))
            for key in [
                "identity",
                "persona",
                "numeric_profile",
                "election_2023_state",
                "simulation_metadata",
            ]:
                self.assertIn(key, sample)

            self.assertIn("archetype_id", sample["identity"])
            self.assertIn("political_worldview", sample["numeric_profile"])
            self.assertIn("first_round_vote_intention", sample["election_2023_state"])
            self.assertIn("runoff_vote_intention", sample["election_2023_state"])

    def test_diverse_soul_selection_spreads_small_samples_across_archetypes(self):
        from agents.soul_loader import load_all_souls
        from loaders.config_loader import load_all_configs
        from scripts.generate_souls_from_config import generate_souls

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            generate_souls(load_all_configs(), output_dir=out_dir, seed=12345)

            souls = load_all_souls(souls_dir=out_dir, limit=5, selection_strategy="diverse")

            archetypes = {soul["identity"]["archetype_id"] for soul in souls.values()}
            self.assertGreaterEqual(len(archetypes), 5)

    def test_soul_loader_ignores_noncanonical_duplicate_copy_files(self):
        from agents.soul_loader import load_all_souls
        from loaders.config_loader import load_all_configs
        from scripts.generate_souls_from_config import generate_souls

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            generate_souls(load_all_configs(), output_dir=out_dir, seed=12345)
            shutil.copyfile(out_dir / "agent_001.json", out_dir / "agent_001 2.json")

            souls = load_all_souls(souls_dir=out_dir, limit=50, selection_strategy="sequential")

            self.assertEqual(len(souls), 50)
            self.assertIn("agent_001", souls)
            self.assertIn("agent_050", souls)

    def test_generate_souls_can_use_2018_baseline_300_profile(self):
        from loaders.config_loader import load_all_configs
        from scripts.generate_souls_from_config import generate_souls

        expected_archetypes = {
            "A1": 58,
            "A2": 32,
            "A3": 33,
            "A4": 19,
            "A5": 29,
            "A6": 30,
            "A7": 25,
            "A8": 18,
            "A9": 15,
            "A10": 14,
            "A11": 16,
            "A12": 11,
        }
        expected_parties = {
            "AKP": 128,
            "CHP": 68,
            "HDP_DEM": 35,
            "MHP": 33,
            "IYI": 30,
            "Other_small_parties": 6,
        }
        expected_presidential = {
            "Erdogan": 158,
            "Muharrem_Ince": 92,
            "Selahattin_Demirtas": 25,
            "Meral_Aksener": 22,
            "Temel_Karamollaoglu": 3,
        }

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            souls = generate_souls(
                load_all_configs(),
                output_dir=out_dir,
                seed=12345,
                population_profile="baseline_2018_300",
            )

            files = sorted(out_dir.glob("*.json"))
            self.assertEqual(len(files), 300)
            self.assertEqual(len(souls), 300)
            self.assertEqual(
                Counter(soul["identity"]["archetype_id"] for soul in souls),
                expected_archetypes,
            )
            self.assertEqual(
                Counter(soul["simulation_metadata"]["baseline_2018"]["party_2018"] for soul in souls),
                expected_parties,
            )
            self.assertEqual(
                Counter(
                    soul["simulation_metadata"]["baseline_2018"]["presidential_vote_2018"]
                    for soul in souls
                ),
                expected_presidential,
            )

            sample = souls[0]
            baseline = sample["simulation_metadata"]["baseline_2018"]
            self.assertEqual(sample["simulation_metadata"]["population_profile"], "baseline_2018_300")
            self.assertIn("sampling frame", baseline["note"])
            self.assertIn("not a deterministic future vote rule", baseline["note"])
            self.assertIn("baseline_2018_memory_summary", sample["persona"])

    def test_voter_prompt_includes_2018_baseline_memory_when_present(self):
        from agents.citizen_agent import TurkishCitizenAgent
        from llm.provider import MockLLMProvider
        from loaders.config_loader import load_all_configs
        from scripts.generate_souls_from_config import generate_souls

        with tempfile.TemporaryDirectory() as tmp:
            soul = generate_souls(
                load_all_configs(),
                output_dir=Path(tmp),
                seed=12345,
                population_profile="baseline_2018_300",
            )[0]

        agent = TurkishCitizenAgent(soul, MockLLMProvider())
        prompt = agent._prompt(
            {
                "tick_id": "T001",
                "date": "2018-06-24",
                "title": "2018 baseline",
                "category": "baseline",
                "summary": "Post-election baseline.",
                "notes_for_llm_agents": "Use only 2018 knowledge.",
            },
            visible_broadcasts=[],
            social_context=[],
            decision_kind="normal",
        )

        self.assertIn("2018 BASELINE MEMORY", prompt)
        self.assertIn("party vote:", prompt)
        self.assertIn("presidential vote:", prompt)
        self.assertIn("not a future vote rule", prompt)


class ElectionTimelineTests(unittest.TestCase):
    def test_tick_plan_inserts_decisions_before_result_reveals(self):
        from loaders.config_loader import load_all_configs
        from simulation.tick_engine import build_election_safe_tick_plan

        plan = build_election_safe_tick_plan(load_all_configs().simulation_ticks)
        ids = [tick["tick_id"] for tick in plan]

        self.assertLess(ids.index("T030A_first_round_vote_decision"), ids.index("T030B_first_round_result_revealed"))
        self.assertLess(ids.index("T035A_runoff_vote_decision"), ids.index("T035B_final_result_revealed"))
        self.assertNotIn("T030", ids)
        self.assertNotIn("T035", ids)

        first_decision = plan[ids.index("T030A_first_round_vote_decision")]
        runoff_decision = plan[ids.index("T035A_runoff_vote_decision")]
        self.assertTrue(first_decision["synthetic_decision"])
        self.assertTrue(runoff_decision["synthetic_decision"])
        self.assertEqual(first_decision["hidden_result_tick_id"], "T030")
        self.assertEqual(runoff_decision["hidden_result_tick_id"], "T035")

    def test_2018_baseline_does_not_receive_2023_campaign_broadcasts(self):
        from agents.political_broadcast_agent import PoliticalBroadcastAgent
        from loaders.config_loader import load_all_configs

        bundle = load_all_configs()
        broadcaster = PoliticalBroadcastAgent(bundle)
        first_tick = bundle.simulation_ticks[0]

        broadcasts = broadcaster.broadcasts_for_tick(first_tick)

        self.assertEqual(first_tick["tick_id"], "T001")
        self.assertEqual(broadcasts, [])

    def test_agent_thought_formatter_shows_reflection_and_vote_leans(self):
        from simulation.tick_engine import format_agent_thought

        class Agent:
            agent_id = "agent_001"
            name = "Synthetic voter 001"
            identity = {"archetype_name": "Devout Anatolian Loyalist"}

        decision = {
            "reflection": "I trust stability but prices make me uneasy.",
            "party_preference": {"AKP": 0.7, "CHP": 0.1},
            "first_round_vote_intention": {"Erdogan": 0.8, "Kilicdaroglu": 0.2},
            "runoff_vote_intention": {"Erdogan": 0.75, "Kilicdaroglu": 0.25},
            "turnout_probability": 0.91,
            "confidence": "medium",
        }

        output = format_agent_thought(Agent(), decision, visible_broadcast_count=2)

        self.assertIn("agent_001", output)
        self.assertIn("Devout Anatolian Loyalist", output)
        self.assertIn("I trust stability", output)
        self.assertIn("first=Erdogan", output)
        self.assertIn("runoff=Erdogan", output)
        self.assertIn("broadcasts=2", output)

    def test_agent_run_order_groups_decisions_by_agent(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        with tempfile.TemporaryDirectory() as tmp:
            engine = TickEngine(
                provider=MockLLMProvider(),
                max_agents=2,
                max_ticks=2,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
                run_order="agent",
            )
            engine.run()

            observed = [(row["agent_id"], row["tick_id"]) for row in engine.metrics.trajectories]
            self.assertEqual(
                observed,
                [
                    ("agent_001", "T001"),
                    ("agent_001", "T002"),
                    ("agent_002", "T001"),
                    ("agent_002", "T002"),
                ],
            )

    def test_parallel_agents_overlap_within_tick(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        class SlowProvider(MockLLMProvider):
            def complete_json(self, prompt, *, schema_name, context):
                time.sleep(0.2)
                return super().complete_json(prompt, schema_name=schema_name, context=context)

        with tempfile.TemporaryDirectory() as tmp:
            start = time.perf_counter()
            engine = TickEngine(
                provider=SlowProvider(),
                max_agents=3,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                parallel_agents=True,
                max_workers=3,
            )
            engine.run()
            elapsed = time.perf_counter() - start

            self.assertEqual(len(engine.metrics.trajectories), 3)
            self.assertLess(elapsed, 0.5)

    def test_parallel_agent_failure_reports_agent_and_tick(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        class FailingProvider(MockLLMProvider):
            def complete_json(self, prompt, *, schema_name, context):
                if context["soul"]["identity"]["agent_id"] == "agent_002":
                    raise RuntimeError("simulated provider failure")
                return super().complete_json(prompt, schema_name=schema_name, context=context)

        with tempfile.TemporaryDirectory() as tmp:
            engine = TickEngine(
                provider=FailingProvider(),
                max_agents=2,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
                parallel_agents=True,
                max_workers=2,
            )

            with self.assertRaisesRegex(RuntimeError, "agent_002.*T001.*simulated provider failure"):
                engine.run()

    def test_continue_on_agent_error_records_marked_fallback_decision(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        class FailingProvider(MockLLMProvider):
            def complete_json(self, prompt, *, schema_name, context):
                if context["soul"]["identity"]["agent_id"] == "agent_002":
                    raise RuntimeError("simulated provider failure")
                return super().complete_json(prompt, schema_name=schema_name, context=context)

        with tempfile.TemporaryDirectory() as tmp:
            engine = TickEngine(
                provider=FailingProvider(),
                max_agents=2,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
                parallel_agents=True,
                max_workers=2,
                continue_on_agent_error=True,
            )

            engine.run()

            self.assertEqual(len(engine.metrics.trajectories), 2)
            fallback = next(row for row in engine.metrics.trajectories if row["agent_id"] == "agent_002")
            self.assertEqual(fallback["confidence"], "low")
            self.assertIn("provider_error", fallback["reason_codes"])
            self.assertIn("agent error fallback", fallback["reflection"])

    def test_openai_provider_retries_transient_completion_failure(self):
        from llm.provider import OpenAIProvider

        class Message:
            content = '{"ok": true}'

        class Choice:
            message = Message()

        class Response:
            choices = [Choice()]

        class FakeCompletions:
            def __init__(self):
                self.attempts = 0

            def create(self, **_kwargs):
                self.attempts += 1
                if self.attempts == 1:
                    raise RuntimeError("temporary upstream error")
                return Response()

        class FakeChat:
            def __init__(self):
                self.completions = FakeCompletions()

        class FakeClient:
            def __init__(self):
                self.chat = FakeChat()

        provider = OpenAIProvider.__new__(OpenAIProvider)
        provider.client = FakeClient()
        provider.model = "test-model"
        provider.max_retries = 2
        provider.retry_base_seconds = 0

        result = provider.complete_json("prompt", schema_name="test", context={})

        self.assertEqual(result, {"ok": True})
        self.assertEqual(provider.client.chat.completions.attempts, 2)

    def test_resume_from_log_skips_restored_decisions_and_continues(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        with tempfile.TemporaryDirectory() as tmp:
            first = TickEngine(
                provider=MockLLMProvider(),
                max_agents=2,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
            )
            first.run()

            resumed = TickEngine(
                provider=MockLLMProvider(),
                max_agents=2,
                max_ticks=2,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
                resume_from_log=first.log_path,
            )
            resumed.run()

            counts = Counter((row["tick_id"], row["agent_id"]) for row in resumed.metrics.trajectories)
            self.assertEqual(len(resumed.metrics.trajectories), 4)
            self.assertEqual(counts[("T001", "agent_001")], 1)
            self.assertEqual(counts[("T001", "agent_002")], 1)
            self.assertEqual(counts[("T002", "agent_001")], 1)
            self.assertEqual(counts[("T002", "agent_002")], 1)

    def test_resume_from_partial_tick_runs_only_missing_agents(self):
        from llm.provider import MockLLMProvider
        from simulation.tick_engine import TickEngine

        class CountingProvider(MockLLMProvider):
            def __init__(self):
                super().__init__()
                self.calls = 0

            def complete_json(self, prompt, *, schema_name, context):
                self.calls += 1
                return super().complete_json(prompt, schema_name=schema_name, context=context)

        with tempfile.TemporaryDirectory() as tmp:
            first = TickEngine(
                provider=MockLLMProvider(),
                max_agents=1,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
            )
            first.run()

            provider = CountingProvider()
            resumed = TickEngine(
                provider=provider,
                max_agents=2,
                max_ticks=1,
                output_dir=Path(tmp),
                verbose=False,
                agent_selection="sequential",
                resume_from_log=first.log_path,
            )
            resumed.run()

            observed = sorted((row["tick_id"], row["agent_id"]) for row in resumed.metrics.trajectories)
            self.assertEqual(observed, [("T001", "agent_001"), ("T001", "agent_002")])
            self.assertEqual(provider.calls, 1)


class RunEntrypointTests(unittest.TestCase):
    def test_run_entrypoint_builds_mock_parallel_engine_from_cli_args(self):
        from llm.provider import MockLLMProvider
        from run import build_engine, parse_args

        args = parse_args(
            [
                "--mock",
                "--max-agents",
                "5",
                "--max-ticks",
                "2",
                "--parallel-agents",
                "--max-workers",
                "3",
                "--continue-on-agent-error",
                "--disable-social",
            ]
        )
        engine = build_engine(args)

        self.assertIsInstance(engine.provider, MockLLMProvider)
        self.assertEqual(engine.max_agents, 5)
        self.assertEqual(engine.max_ticks, 2)
        self.assertTrue(engine.parallel_agents)
        self.assertEqual(engine.max_workers, 3)
        self.assertTrue(engine.continue_on_agent_error)
        self.assertTrue(engine.disable_social)


if __name__ == "__main__":
    unittest.main()
