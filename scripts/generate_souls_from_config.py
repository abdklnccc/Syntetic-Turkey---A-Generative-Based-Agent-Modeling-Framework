#!/usr/bin/env python3
import argparse
import json
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config
from loaders.config_loader import ConfigBundle, load_all_configs


FIRST_ROUND_KEYS = [
    "Erdogan",
    "Kilicdaroglu",
    "Sinan_Ogan",
    "Muharrem_Ince",
    "Other",
    "Undecided",
]
RUNOFF_KEYS = ["Erdogan", "Kilicdaroglu", "Abstain_Invalid_Undecided"]

PARTY_KEYS = ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP", "YRP", "Other", "Undecided"]

PARTY_ALIASES = {
    "HDP": "DEM_HDP_YSP",
    "DEM": "DEM_HDP_YSP",
    "YSP": "DEM_HDP_YSP",
    "HDP_DEM": "DEM_HDP_YSP",
    "Other_small_parties": "Other",
}

POPULATION_PROFILES = ("prototype_50", "baseline_2018_300")

BASELINE_2018_PRESIDENTIAL_ALLOCATIONS = {
    "AKP": {"Erdogan": 128},
    "CHP": {"Muharrem_Ince": 68},
    "HDP_DEM": {"Selahattin_Demirtas": 25, "Muharrem_Ince": 10},
    "MHP": {"Erdogan": 30, "Meral_Aksener": 3},
    "IYI": {"Meral_Aksener": 19, "Muharrem_Ince": 11},
    "Other_small_parties": {"Temel_Karamollaoglu": 3, "Muharrem_Ince": 3},
}

PARTY_TO_FIRST_ROUND = {
    "AKP": {"Erdogan": 0.92, "Kilicdaroglu": 0.02, "Sinan_Ogan": 0.03, "Muharrem_Ince": 0.01, "Other": 0.01, "Undecided": 0.01},
    "CHP": {"Erdogan": 0.01, "Kilicdaroglu": 0.88, "Sinan_Ogan": 0.02, "Muharrem_Ince": 0.05, "Other": 0.01, "Undecided": 0.03},
    "MHP": {"Erdogan": 0.76, "Kilicdaroglu": 0.03, "Sinan_Ogan": 0.17, "Muharrem_Ince": 0.01, "Other": 0.01, "Undecided": 0.02},
    "IYI": {"Erdogan": 0.04, "Kilicdaroglu": 0.64, "Sinan_Ogan": 0.22, "Muharrem_Ince": 0.03, "Other": 0.01, "Undecided": 0.06},
    "DEM_HDP_YSP": {"Erdogan": 0.03, "Kilicdaroglu": 0.72, "Sinan_Ogan": 0.01, "Muharrem_Ince": 0.03, "Other": 0.05, "Undecided": 0.16},
    "YRP": {"Erdogan": 0.56, "Kilicdaroglu": 0.05, "Sinan_Ogan": 0.08, "Muharrem_Ince": 0.02, "Other": 0.14, "Undecided": 0.15},
    "Other": {"Erdogan": 0.15, "Kilicdaroglu": 0.25, "Sinan_Ogan": 0.12, "Muharrem_Ince": 0.10, "Other": 0.20, "Undecided": 0.18},
    "Undecided": {"Erdogan": 0.25, "Kilicdaroglu": 0.25, "Sinan_Ogan": 0.12, "Muharrem_Ince": 0.08, "Other": 0.05, "Undecided": 0.25},
}

DEMOGRAPHIC_DEFAULTS = {
    "A1": {
        "cities": ["Konya", "Kayseri", "Sivas", "Erzurum", "Yozgat"],
        "regions": ["Central Anatolia", "Eastern Anatolia"],
        "age_range": (38, 72),
        "education": ["primary", "high_school"],
        "income": ["lower_middle", "middle"],
        "employment": ["small_business_owner", "worker", "farmer", "retired"],
    },
    "A2": {
        "cities": ["Istanbul", "Ankara", "Izmir"],
        "regions": ["Marmara", "Central Anatolia", "Aegean"],
        "age_range": (28, 58),
        "education": ["university", "graduate"],
        "income": ["middle", "upper_middle"],
        "employment": ["professional", "public_sector", "academic", "manager"],
    },
    "A3": {
        "cities": ["Istanbul", "Bursa", "Konya", "Gaziantep", "Kayseri"],
        "regions": ["Marmara", "Central Anatolia", "Southeast Anatolia"],
        "age_range": (35, 60),
        "education": ["primary", "high_school", "vocational"],
        "income": ["working_class", "lower_middle", "middle"],
        "employment": ["worker", "driver", "tradesperson", "service_worker"],
    },
    "A4": {
        "cities": ["Tunceli", "Istanbul", "Izmir", "Hatay", "Ankara"],
        "regions": ["Eastern Anatolia", "Marmara", "Aegean", "Mediterranean"],
        "age_range": (30, 70),
        "education": ["high_school", "university"],
        "income": ["lower_middle", "middle"],
        "employment": ["public_sector", "teacher", "retired", "worker"],
    },
    "A5": {
        "cities": ["Diyarbakir", "Van", "Mardin", "Istanbul", "Batman"],
        "regions": ["Southeast Anatolia", "Eastern Anatolia", "Marmara"],
        "age_range": (24, 68),
        "education": ["primary", "high_school", "university"],
        "income": ["working_class", "lower_middle", "middle"],
        "employment": ["student", "worker", "small_business_owner", "public_sector"],
    },
    "A6": {
        "cities": ["Osmaniye", "Sivas", "Kayseri", "Karabuk", "Mersin"],
        "regions": ["Mediterranean", "Central Anatolia", "Black Sea"],
        "age_range": (32, 68),
        "education": ["high_school", "university"],
        "income": ["lower_middle", "middle"],
        "employment": ["security", "tradesperson", "retired", "public_sector"],
    },
    "A7": {
        "cities": ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa"],
        "regions": ["Marmara", "Central Anatolia", "Aegean", "Mediterranean"],
        "age_range": (28, 62),
        "education": ["high_school", "university"],
        "income": ["middle", "upper_middle"],
        "employment": ["professional", "small_business_owner", "retired"],
    },
    "A8": {
        "cities": ["Konya", "Istanbul", "Sakarya", "Kayseri", "Malatya"],
        "regions": ["Central Anatolia", "Marmara", "Eastern Anatolia"],
        "age_range": (32, 68),
        "education": ["primary", "high_school", "university"],
        "income": ["lower_middle", "middle"],
        "employment": ["small_business_owner", "imam_or_religious_worker", "worker", "retired"],
    },
    "A9": {
        "cities": ["Istanbul", "Ankara", "Izmir", "Eskisehir"],
        "regions": ["Marmara", "Central Anatolia", "Aegean"],
        "age_range": (18, 30),
        "education": ["university_student", "university"],
        "income": ["student", "working_class", "middle"],
        "employment": ["student", "service_worker", "early_career_professional", "unemployed"],
    },
    "A10": {
        "cities": ["Kahramanmaras", "Adiyaman", "Malatya", "Hatay", "Gaziantep"],
        "regions": ["Earthquake Zone", "Southeast Anatolia", "Mediterranean"],
        "age_range": (34, 72),
        "education": ["primary", "high_school"],
        "income": ["lower_middle", "middle"],
        "employment": ["worker", "farmer", "small_business_owner", "retired"],
    },
    "A11": {
        "cities": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"],
        "regions": ["Marmara", "Central Anatolia", "Aegean", "Mediterranean"],
        "age_range": (60, 78),
        "education": ["primary", "high_school", "university"],
        "income": ["pensioner_low", "lower_middle", "middle"],
        "employment": ["retired"],
    },
    "A12": {
        "cities": ["Istanbul", "Ankara", "Izmir"],
        "regions": ["Marmara", "Central Anatolia", "Aegean"],
        "age_range": (26, 58),
        "education": ["university", "graduate"],
        "income": ["upper_middle", "upper"],
        "employment": ["professional", "academic", "creative_worker", "manager"],
    },
}


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    chars = []
    for char in normalized.casefold():
        if unicodedata.combining(char):
            continue
        if char.isalnum():
            chars.append(char)
        elif chars and chars[-1] != "_":
            chars.append("_")
    return "".join(chars).strip("_")


def _matrix_key(value: str) -> str:
    return _slugify(value)


def _normalize(values: dict[str, float], keys: list[str]) -> dict[str, float]:
    cleaned = {key: max(0.0, float(values.get(key, 0.0))) for key in keys}
    total = sum(cleaned.values())
    if total <= 0:
        return {key: 1.0 / len(keys) for key in keys}
    return {key: round(value / total, 6) for key, value in cleaned.items()}


def _bounded_normal(rng: random.Random, mean: float, low: float, high: float, sigma: float) -> float:
    return round(min(high, max(low, rng.gauss(mean, sigma))), 4)


def _vary_map(rng: random.Random, values: dict[str, float], low: float, high: float, sigma: float) -> dict[str, float]:
    return {key: _bounded_normal(rng, float(value), low, high, sigma) for key, value in values.items()}


def _convert_party_distribution(values: dict[str, float]) -> dict[str, float]:
    converted = {key: 0.0 for key in PARTY_KEYS}
    for raw_key, raw_value in values.items():
        key = PARTY_ALIASES.get(raw_key, raw_key)
        if key in converted:
            converted[key] += float(raw_value)
        else:
            converted["Other"] += float(raw_value)
    return _normalize(converted, PARTY_KEYS)


def _party_prior_from_2018_anchor(archetype_prior: dict[str, float], party_2018: str | None) -> dict[str, float]:
    if not party_2018:
        return archetype_prior
    party_key = PARTY_ALIASES.get(party_2018, party_2018)
    if party_key not in PARTY_KEYS:
        party_key = "Other"
    anchored = {key: value * 0.35 for key, value in archetype_prior.items()}
    anchored[party_key] = anchored.get(party_key, 0.0) + 0.65
    return _normalize(anchored, PARTY_KEYS)


def _candidate_prior_from_party(party_dist: dict[str, float]) -> dict[str, float]:
    result = {key: 0.0 for key in FIRST_ROUND_KEYS}
    for party, weight in party_dist.items():
        template = PARTY_TO_FIRST_ROUND.get(party, PARTY_TO_FIRST_ROUND["Other"])
        for candidate, value in template.items():
            result[candidate] += weight * value
    return _normalize(result, FIRST_ROUND_KEYS)


def _runoff_prior(first_round: dict[str, float], party_dist: dict[str, float]) -> dict[str, float]:
    erdogan = first_round["Erdogan"] + first_round["Sinan_Ogan"] * 0.58 + party_dist.get("YRP", 0.0) * 0.20
    kilicdaroglu = first_round["Kilicdaroglu"] + first_round["Muharrem_Ince"] * 0.55 + party_dist.get("DEM_HDP_YSP", 0.0) * 0.08
    abstain = first_round["Undecided"] * 0.75 + first_round["Other"] * 0.35
    return _normalize(
        {
            "Erdogan": erdogan,
            "Kilicdaroglu": kilicdaroglu,
            "Abstain_Invalid_Undecided": abstain,
        },
        RUNOFF_KEYS,
    )


def _baseline_2018_memory_summary(distribution_row: dict[str, Any]) -> str:
    baseline = distribution_row.get("baseline_2018")
    if not baseline:
        return "No explicit individual 2018 vote anchor is attached to this prototype soul."
    return (
        "In the June 2018 baseline sampling frame, this synthetic voter is grounded as having cast "
        f"party vote: {baseline['party_2018']}; presidential vote: "
        f"{baseline['presidential_vote_2018']}. This is persona memory and sampling structure, "
        "not a future vote rule."
    )


def _make_persona(
    archetype: dict[str, Any],
    demographic: dict[str, str | int],
    distribution_row: dict[str, Any],
) -> dict[str, str]:
    name = archetype["name"]
    city = demographic["city"]
    return {
        "short_biography": (
            f"Synthetic voter from {city} generated from the {name} archetype. "
            "This is not a real person and exists only for simulation."
        ),
        "political_identity_summary": f"Grounded in source archetype {archetype['id']} ({name}).",
        "worldview_summary": (
            "Worldview variables are inherited from the source configuration with bounded variation."
        ),
        "media_diet_summary": (
            "Media exposure is inherited from the archetype media_diet vector and filtered per tick."
        ),
        "social_context_summary": (
            "Peer context is synthetic and concise; social influence is handled by LLM reasoning."
        ),
        "baseline_2018_memory_summary": _baseline_2018_memory_summary(distribution_row),
    }


def _make_identity(
    rng: random.Random,
    agent_index: int,
    archetype: dict[str, Any],
    demographic_defaults: dict[str, Any],
) -> dict[str, Any]:
    age_low, age_high = demographic_defaults["age_range"]
    gender = rng.choice(["Female", "Male"])
    return {
        "agent_id": f"agent_{agent_index:03d}",
        "archetype_id": archetype["id"],
        "archetype_name": archetype["name"],
        "display_name": f"Synthetic voter {agent_index:03d}",
        "age": rng.randint(age_low, age_high),
        "gender": gender,
        "city": rng.choice(demographic_defaults["cities"]),
        "region": rng.choice(demographic_defaults["regions"]),
        "education_level": rng.choice(demographic_defaults["education"]),
        "income_bracket": rng.choice(demographic_defaults["income"]),
        "employment_status": rng.choice(demographic_defaults["employment"]),
    }


def build_soul(
    rng: random.Random,
    agent_index: int,
    archetype: dict[str, Any],
    distribution_row: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    demographic_defaults = DEMOGRAPHIC_DEFAULTS.get(archetype["id"], DEMOGRAPHIC_DEFAULTS["A3"])
    identity = _make_identity(rng, agent_index, archetype, demographic_defaults)
    persona = _make_persona(archetype, identity, distribution_row)

    archetype_party_preference = _convert_party_distribution(archetype["initial_vote_intention"])
    baseline_2018 = distribution_row.get("baseline_2018")
    party_preference = _party_prior_from_2018_anchor(
        archetype_party_preference,
        baseline_2018.get("party_2018_internal_key") if baseline_2018 else None,
    )
    first_round = _candidate_prior_from_party(party_preference)
    runoff = _runoff_prior(first_round, party_preference)

    numeric_profile = {
        "political_worldview": _vary_map(rng, archetype["political_worldview"], 1.0, 10.0, 0.55),
        "emotional_baseline": _vary_map(rng, archetype["emotional_baseline"], 0.0, 1.0, 0.07),
        "media_diet": _vary_map(rng, archetype["media_diet"], 0.0, 1.0, 0.06),
        "behavioral_variables": _vary_map(rng, archetype["behavioral_variables"], 0.0, 1.0, 0.06),
        "initial_party_vote_intention": party_preference,
        "future_background_metadata": {
            "trajectory_2024": archetype.get("trajectory_2024", {}),
            "note": "Future trajectory metadata is for evaluator calibration only and is never shown as voter knowledge.",
        },
    }
    if baseline_2018:
        numeric_profile["baseline_2018"] = {
            "party_2018": baseline_2018["party_2018"],
            "party_2018_internal_key": baseline_2018["party_2018_internal_key"],
            "presidential_vote_2018": baseline_2018["presidential_vote_2018"],
            "source": "voter_source_of_truth/2018_baseline_sampling_profile.yaml",
            "note": "Baseline memory/persona grounding only; not a deterministic future vote rule.",
        }

    current_party = max(party_preference, key=party_preference.get)
    current_candidate = max(first_round, key=first_round.get)
    election_state = {
        "first_round_vote_intention": first_round,
        "runoff_vote_intention": runoff,
        "turnout_probability": numeric_profile["behavioral_variables"].get("turnout_likelihood", 0.75),
        "current_candidate_preference": current_candidate,
        "current_party_preference": current_party,
    }

    soul = {
        "identity": identity,
        "persona": persona,
        "numeric_profile": numeric_profile,
        "election_2023_state": election_state,
        "simulation_metadata": {
            "source_archetype_weight": distribution_row["agents"],
            "source_archetype_percent": distribution_row["percent"],
            "uncertainty_level": distribution_row.get("uncertainty", "medium"),
            "generated_seed": seed,
            "demographic_defaults_source": "simulation assumptions supplied in MVP brief",
            "demographic_assumptions": demographic_defaults,
            "slug": _slugify(archetype["name"]),
            "note": "Synthetic persona, not a real person.",
            "population_profile": distribution_row.get("population_profile", "prototype_50"),
        },
    }
    if baseline_2018:
        soul["simulation_metadata"]["baseline_2018"] = {
            **baseline_2018,
            "source_profile": "voter_source_of_truth/2018_baseline_sampling_profile.yaml",
            "note": (
                "2018 party and presidential vote anchors are a sampling frame and persona memory, "
                "not a deterministic future vote rule."
            ),
        }
    return soul


def _archetype_id_by_matrix_key(bundle: ConfigBundle) -> dict[str, str]:
    result = {}
    for archetype in bundle.voter_archetypes:
        keys = {_matrix_key(archetype["name"])}
        if "(" in archetype["name"] and ")" in archetype["name"]:
            keys.add(_matrix_key(archetype["name"].replace("(", "").replace(")", "")))
        for key in keys:
            result[key] = archetype["id"]
    return result


def _presidential_queue_by_party(rng: random.Random, profile: dict[str, Any]) -> dict[str, list[str]]:
    expected_party_counts = {
        party: int(count)
        for party, count in profile["recommended_300_agent_party_distribution"].items()
    }
    expected_presidential = {
        candidate: int(count)
        for candidate, count in profile["recommended_300_agent_presidential_distribution"].items()
        if int(count) > 0
    }
    actual_presidential = Counter()
    queues: dict[str, list[str]] = {}
    for party, allocation in BASELINE_2018_PRESIDENTIAL_ALLOCATIONS.items():
        queue: list[str] = []
        for candidate, count in allocation.items():
            queue.extend([candidate] * int(count))
            actual_presidential[candidate] += int(count)
        if len(queue) != expected_party_counts.get(party):
            raise RuntimeError(
                f"2018 presidential anchor allocation for {party} has {len(queue)} agents, "
                f"expected {expected_party_counts.get(party)}"
            )
        rng.shuffle(queue)
        queues[party] = queue

    if actual_presidential != Counter(expected_presidential):
        raise RuntimeError(
            "2018 presidential anchor allocations do not match the baseline profile: "
            f"{dict(actual_presidential)} != {expected_presidential}"
        )
    return queues


def _baseline_2018_distribution(bundle: ConfigBundle, rng: random.Random) -> list[dict[str, Any]]:
    profile = bundle.baseline_sampling_profile
    matrix = profile["recommended_300_agent_party_to_archetype_matrix"]
    recommended_size = int(profile["meta"]["recommended_sample_size"])
    archetype_ids = _archetype_id_by_matrix_key(bundle)
    presidential_queues = _presidential_queue_by_party(rng, profile)
    rows: list[dict[str, Any]] = []

    for party_2018, archetype_counts in matrix.items():
        for archetype_key, count in archetype_counts.items():
            normalized_key = _matrix_key(archetype_key)
            if normalized_key not in archetype_ids:
                raise RuntimeError(f"Unknown 2018 baseline archetype key: {archetype_key}")
            for _ in range(int(count)):
                presidential_vote = presidential_queues[party_2018].pop()
                rows.append(
                    {
                        "id": archetype_ids[normalized_key],
                        "agents": 1,
                        "percent": round(100.0 / recommended_size, 6),
                        "uncertainty": "medium",
                        "population_profile": "baseline_2018_300",
                        "baseline_2018": {
                            "party_2018": party_2018,
                            "party_2018_internal_key": PARTY_ALIASES.get(party_2018, party_2018),
                            "presidential_vote_2018": presidential_vote,
                        },
                    }
                )

    remaining = {party: len(queue) for party, queue in presidential_queues.items() if queue}
    if remaining:
        raise RuntimeError(f"Unassigned 2018 presidential anchor votes remain: {remaining}")
    if len(rows) != recommended_size:
        raise RuntimeError(f"Built {len(rows)} baseline rows, expected {recommended_size}")

    expected_archetypes = {
        _matrix_key(key): int(value)
        for key, value in profile["recommended_300_agent_archetype_totals"].items()
    }
    actual_archetypes = Counter(row["id"] for row in rows)
    expected_by_id = {
        archetype_ids[key]: value
        for key, value in expected_archetypes.items()
    }
    if actual_archetypes != Counter(expected_by_id):
        raise RuntimeError(
            "2018 baseline archetype rows do not match the profile totals: "
            f"{dict(actual_archetypes)} != {expected_by_id}"
        )
    return rows


def _population_distribution(
    bundle: ConfigBundle,
    rng: random.Random,
    population_profile: str,
) -> tuple[list[dict[str, Any]], int]:
    if population_profile == "prototype_50":
        expected = int(bundle.voter_config["meta"]["prototype_agent_count"])
        return (
            [
                {
                    **row,
                    "population_profile": "prototype_50",
                }
                for row in bundle.voter_distribution
            ],
            expected,
        )
    if population_profile == "baseline_2018_300":
        rows = _baseline_2018_distribution(bundle, rng)
        return rows, int(bundle.baseline_sampling_profile["meta"]["recommended_sample_size"])
    raise ValueError(
        f"Unknown population profile: {population_profile}. "
        f"Expected one of: {', '.join(POPULATION_PROFILES)}"
    )


def generate_souls(
    bundle: ConfigBundle | None = None,
    output_dir: Path | None = None,
    seed: int | None = None,
    population_profile: str = "prototype_50",
) -> list[dict[str, Any]]:
    bundle = bundle or load_all_configs()
    output_dir = output_dir or config.SOULS_DIR
    seed = config.GENERATED_SOUL_SEED if seed is None else seed
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    archetypes = {row["id"]: row for row in bundle.voter_archetypes}
    distribution, expected_count = _population_distribution(bundle, rng, population_profile)
    souls: list[dict[str, Any]] = []
    agent_index = 1
    for dist in distribution:
        archetype = archetypes[dist["id"]]
        for _ in range(int(dist["agents"])):
            soul = build_soul(rng, agent_index, archetype, dist, seed)
            souls.append(soul)
            agent_index += 1

    if len(souls) != expected_count:
        raise RuntimeError(f"Generated {len(souls)} souls, expected {expected_count}")

    for stale in output_dir.glob("agent_*.json"):
        stale.unlink()
    for soul in souls:
        agent_id = soul["identity"]["agent_id"]
        path = output_dir / f"{agent_id}.json"
        path.write_text(json.dumps(soul, ensure_ascii=False, indent=2), encoding="utf-8")
    return souls


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate source-grounded voter souls.")
    parser.add_argument("--output-dir", type=Path, default=config.SOULS_DIR)
    parser.add_argument("--seed", type=int, default=config.GENERATED_SOUL_SEED)
    parser.add_argument(
        "--population-profile",
        choices=POPULATION_PROFILES,
        default="prototype_50",
        help="prototype_50 keeps the MVP/debug population; baseline_2018_300 uses the thesis baseline.",
    )
    args = parser.parse_args()

    souls = generate_souls(
        output_dir=args.output_dir,
        seed=args.seed,
        population_profile=args.population_profile,
    )
    print(f"Generated {len(souls)} {args.population_profile} souls in {args.output_dir}")


if __name__ == "__main__":
    main()
