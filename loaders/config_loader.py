import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

import config


class ConfigLoadError(RuntimeError):
    """Raised when a source-of-truth config file is missing or malformed."""


@dataclass(frozen=True)
class ConfigBundle:
    voter_config: dict[str, Any]
    baseline_sampling_profile: dict[str, Any]
    political_agents: dict[str, Any]
    political_personas: dict[str, Any]
    credibility_matrix: dict[str, Any]
    politician_event_responses: dict[str, Any]
    movement_state_machine: dict[str, Any]
    simulation_ticks: list[dict[str, Any]]
    actual_results: dict[str, Any]

    @property
    def voter_archetypes(self) -> list[dict[str, Any]]:
        return self.voter_config["task_3_archetype_variables"]

    @property
    def voter_distribution(self) -> list[dict[str, Any]]:
        return self.voter_config["task_2_simulation_weights_50_agents"]["distribution"]


def _require_file(path: Path) -> Path:
    if not path.exists():
        raise ConfigLoadError(f"Required config file does not exist: {path}")
    if not path.is_file():
        raise ConfigLoadError(f"Required config path is not a file: {path}")
    return path


def load_json(path: Path) -> Any:
    path = _require_file(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigLoadError(f"Malformed JSON in {path}: {exc}") from exc


def load_yaml(path: Path) -> Any:
    path = _require_file(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"Malformed YAML in {path}: {exc}") from exc
    if data is None:
        raise ConfigLoadError(f"YAML config is empty: {path}")
    return data


def _require_keys(name: str, data: dict[str, Any], keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise ConfigLoadError(f"{name} missing required key(s): {', '.join(missing)}")


def _validate_bundle(bundle: ConfigBundle) -> None:
    _require_keys(
        "voter config",
        bundle.voter_config,
        ("meta", "task_2_simulation_weights_50_agents", "task_3_archetype_variables"),
    )
    _require_keys(
        "2018 baseline sampling profile",
        bundle.baseline_sampling_profile,
        (
            "meta",
            "recommended_300_agent_party_distribution",
            "recommended_300_agent_presidential_distribution",
            "recommended_300_agent_party_to_archetype_matrix",
            "recommended_300_agent_archetype_totals",
        ),
    )
    _require_keys("political agents config", bundle.political_agents, ("agents",))
    _require_keys("credibility matrix", bundle.credibility_matrix, ("credibility",))
    _require_keys("politician event responses", bundle.politician_event_responses, ("events",))
    _require_keys("movement state machine", bundle.movement_state_machine, ("periods",))
    _require_keys("actual results", bundle.actual_results, ("first_round", "runoff"))

    if not isinstance(bundle.simulation_ticks, list) or not bundle.simulation_ticks:
        raise ConfigLoadError("simulation_ticks.json must contain a non-empty list")

    expected_total = bundle.voter_config["meta"].get("prototype_agent_count")
    actual_total = sum(int(row.get("agents", 0)) for row in bundle.voter_distribution)
    if expected_total != actual_total:
        raise ConfigLoadError(
            f"Voter distribution sums to {actual_total}, expected {expected_total}"
        )

    baseline_expected = int(bundle.baseline_sampling_profile["meta"]["recommended_sample_size"])
    baseline_party_total = sum(
        int(value)
        for value in bundle.baseline_sampling_profile["recommended_300_agent_party_distribution"].values()
    )
    baseline_presidential_total = sum(
        int(value)
        for value in bundle.baseline_sampling_profile["recommended_300_agent_presidential_distribution"].values()
    )
    baseline_archetype_total = sum(
        int(value)
        for value in bundle.baseline_sampling_profile["recommended_300_agent_archetype_totals"].values()
    )
    if baseline_party_total != baseline_expected:
        raise ConfigLoadError(
            f"2018 baseline party distribution sums to {baseline_party_total}, expected {baseline_expected}"
        )
    if baseline_presidential_total != baseline_expected:
        raise ConfigLoadError(
            f"2018 baseline presidential distribution sums to {baseline_presidential_total}, "
            f"expected {baseline_expected}"
        )
    if baseline_archetype_total != baseline_expected:
        raise ConfigLoadError(
            f"2018 baseline archetype distribution sums to {baseline_archetype_total}, "
            f"expected {baseline_expected}"
        )


def load_all_configs() -> ConfigBundle:
    bundle = ConfigBundle(
        voter_config=load_json(config.VOTER_CONFIG_FILE),
        baseline_sampling_profile=load_yaml(config.BASELINE_SAMPLING_PROFILE_FILE),
        political_agents=load_yaml(config.POLITICAL_AGENTS_FILE),
        political_personas=load_yaml(config.POLITICAL_PERSONAS_FILE),
        credibility_matrix=load_yaml(config.CREDIBILITY_MATRIX_FILE),
        politician_event_responses=load_yaml(config.POLITICIAN_EVENT_RESPONSES_FILE),
        movement_state_machine=load_yaml(config.MOVEMENT_STATE_MACHINE_FILE),
        simulation_ticks=load_json(config.SIMULATION_TICKS_FILE),
        actual_results=load_yaml(config.ACTUAL_RESULTS_FILE),
    )
    _validate_bundle(bundle)
    return bundle
