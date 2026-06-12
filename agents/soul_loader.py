import json
from pathlib import Path
from typing import Any

import config


class SoulLoadError(RuntimeError):
    pass


REQUIRED_TOP_LEVEL = {
    "identity",
    "persona",
    "numeric_profile",
    "election_2023_state",
    "simulation_metadata",
}


def validate_soul(soul: dict[str, Any], path: Path | None = None) -> None:
    missing = REQUIRED_TOP_LEVEL - set(soul)
    if missing:
        label = f" in {path}" if path else ""
        raise SoulLoadError(f"Soul{label} missing top-level fields: {', '.join(sorted(missing))}")
    identity = soul["identity"]
    if "agent_id" not in identity or "archetype_id" not in identity:
        raise SoulLoadError(f"Soul {path or identity} missing identity.agent_id or identity.archetype_id")


def load_soul(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise SoulLoadError(f"Soul file does not exist: {path}")
    try:
        soul = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SoulLoadError(f"Malformed soul JSON in {path}: {exc}") from exc
    validate_soul(soul, path)
    return soul


def load_all_souls(
    souls_dir: Path | None = None,
    limit: int | None = None,
    auto_generate: bool = False,
    selection_strategy: str = "sequential",
    auto_generate_population_profile: str = "prototype_50",
) -> dict[str, dict[str, Any]]:
    souls_dir = souls_dir or config.SOULS_DIR
    souls_dir.mkdir(exist_ok=True)
    files = _canonical_soul_files(souls_dir)

    if not files and auto_generate:
        from scripts.generate_souls_from_config import generate_souls

        generate_souls(output_dir=souls_dir, population_profile=auto_generate_population_profile)
        files = _canonical_soul_files(souls_dir)

    if not files:
        raise SoulLoadError(
            f"No JSON souls found in {souls_dir}. Run: python3 scripts/generate_souls_from_config.py"
        )

    loaded = []
    for path in files:
        soul = load_soul(path)
        if path.stem == soul["identity"]["agent_id"]:
            loaded.append(soul)
    if limit is None:
        limit = config.NUM_AGENTS
    selected_souls = _select_souls(loaded, limit=limit, strategy=selection_strategy)

    souls: dict[str, dict[str, Any]] = {}
    for soul in selected_souls:
        agent_id = soul["identity"]["agent_id"]
        souls[agent_id] = soul
    return souls


def _canonical_soul_files(souls_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in souls_dir.glob("agent_*.json")
        if path.stem.startswith("agent_") and path.stem.removeprefix("agent_").isdigit()
    )


def _select_souls(
    souls: list[dict[str, Any]],
    limit: int | None,
    strategy: str = "sequential",
) -> list[dict[str, Any]]:
    if not limit:
        return souls
    if strategy == "sequential":
        return souls[:limit]
    if strategy != "diverse":
        raise SoulLoadError(f"Unknown soul selection strategy: {strategy}")

    by_archetype: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for soul in souls:
        archetype_id = soul["identity"]["archetype_id"]
        if archetype_id not in by_archetype:
            by_archetype[archetype_id] = []
            order.append(archetype_id)
        by_archetype[archetype_id].append(soul)

    selected: list[dict[str, Any]] = []
    while len(selected) < limit:
        added = False
        for archetype_id in order:
            bucket = by_archetype[archetype_id]
            if bucket:
                selected.append(bucket.pop(0))
                added = True
                if len(selected) >= limit:
                    break
        if not added:
            break
    return selected
