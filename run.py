from __future__ import annotations

import argparse
import json
from pathlib import Path

import config
from llm.provider import make_provider
from simulation.tick_engine import TickEngine


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Synthetic Turkey voter-agent simulation.",
    )
    parser.add_argument("--mock", action="store_true", help="Use the deterministic local mock provider.")
    parser.add_argument("--provider", choices=["mock", "openai"], default=None, help="LLM provider to use.")
    parser.add_argument("--max-agents", type=int, default=None, help="Limit the number of loaded agents.")
    parser.add_argument("--max-ticks", type=int, default=None, help="Limit the number of processed ticks.")
    parser.add_argument("--disable-social", action="store_true", help="Disable peer social context between agents.")
    parser.add_argument("--generate-souls", action="store_true", help="Generate souls if none exist.")
    parser.add_argument("--show-agent-thoughts", action="store_true", help="Print each agent reflection as it runs.")
    parser.add_argument(
        "--agent-selection",
        choices=["diverse", "sequential"],
        default="diverse",
        help="How to select a limited subset of souls.",
    )
    parser.add_argument(
        "--run-order",
        choices=["tick", "agent"],
        default="tick",
        help="Run all agents per tick or all ticks per agent.",
    )
    parser.add_argument("--parallel-agents", action="store_true", help="Run agents within each tick in parallel.")
    parser.add_argument("--max-workers", type=int, default=None, help="Worker count for --parallel-agents.")
    parser.add_argument(
        "--continue-on-agent-error",
        action="store_true",
        help="Record a low-confidence fallback row when one agent provider call fails.",
    )
    parser.add_argument("--resume-from-log", type=Path, default=None, help="Resume completed decisions from a JSONL run log.")
    parser.add_argument(
        "--population-profile",
        choices=["prototype_50", "baseline_2018_300"],
        default="prototype_50",
        help="Soul-generation profile to use when --generate-souls creates a population.",
    )
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for CSV/JSONL/JSON outputs.")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output from the engine.")
    args = parser.parse_args(argv)
    if args.mock and args.provider and args.provider != "mock":
        parser.error("--mock cannot be combined with --provider openai")
    return args


def provider_name(args: argparse.Namespace) -> str:
    if args.mock:
        return "mock"
    return args.provider or config.LLM_PROVIDER


def build_engine(args: argparse.Namespace) -> TickEngine:
    return TickEngine(
        provider=make_provider(provider_name(args)),
        max_agents=args.max_agents,
        max_ticks=args.max_ticks,
        disable_social=args.disable_social,
        auto_generate_souls=args.generate_souls,
        output_dir=args.output_dir,
        verbose=not args.quiet,
        show_agent_thoughts=args.show_agent_thoughts,
        agent_selection=args.agent_selection,
        run_order=args.run_order,
        parallel_agents=args.parallel_agents,
        max_workers=args.max_workers,
        continue_on_agent_error=args.continue_on_agent_error,
        resume_from_log=args.resume_from_log,
        population_profile=args.population_profile,
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    engine = build_engine(args)
    summary = engine.run()
    print(
        json.dumps(
            {
                "output_dir": str(engine.output_dir),
                "log_path": str(engine.log_path),
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
