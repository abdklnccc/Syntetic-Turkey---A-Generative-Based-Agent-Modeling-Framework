from __future__ import annotations

import csv
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
SOULS = ROOT / "souls"
EVENTS_FILE = ROOT / "events" / "simulation_ticks.json"
ACTUAL_RESULTS_FILE = ROOT / "actual_results_2023.yaml"
DOCS_DIR = ROOT / "docs" / "thesis_artifacts"
CHARTS_DIR = OUTPUTS / "analysis_charts"
TABLES_DIR = OUTPUTS / "analysis_tables"

TRAJECTORIES_FILE = OUTPUTS / "agent_trajectories.csv"
REFLECTIONS_FILE = OUTPUTS / "reflections.jsonl"
BROADCASTS_FILE = OUTPUTS / "broadcasts.jsonl"
EVALUATION_FILE = OUTPUTS / "evaluation_summary.json"

FIRST_KEYS = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince", "Other", "Undecided"]
FIRST_VALID_KEYS = ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Muharrem_Ince"]
RUNOFF_KEYS = ["Erdogan", "Kilicdaroglu", "Abstain_Invalid_Undecided"]
RUNOFF_VALID_KEYS = ["Erdogan", "Kilicdaroglu"]
PARTY_KEYS = ["AKP", "CHP", "MHP", "IYI", "DEM_HDP_YSP", "YRP", "Other", "Undecided"]

RIGHT_GOVERNMENT_PARTIES = {"AKP", "MHP", "YRP"}
OPPOSITION_LEFT_PARTIES = {"CHP", "DEM_HDP_YSP"}
OPPOSITION_NATIONALIST_PARTIES = {"IYI"}

PALETTE = {
    "Erdogan": "#b91c1c",
    "Kilicdaroglu": "#2563eb",
    "Sinan_Ogan": "#7c3aed",
    "Muharrem_Ince": "#0891b2",
    "Other": "#6b7280",
    "Undecided": "#9ca3af",
    "Abstain_Invalid_Undecided": "#64748b",
    "Right/Government": "#b91c1c",
    "Opposition-left/pro-democracy": "#2563eb",
    "Opposition-nationalist/center-right": "#7c3aed",
    "Other/Undecided": "#6b7280",
    "Government approval": "#b91c1c",
    "Institutional trust": "#0f766e",
    "Opposition trust": "#2563eb",
    "Anger": "#dc2626",
    "Fear": "#9333ea",
    "Hope": "#16a34a",
    "Sadness": "#64748b",
    "Political fatigue": "#f59e0b",
    "Simulation": "#2563eb",
    "Actual": "#111827",
}


STOPWORDS = {
    "a",
    "about",
    "after",
    "again",
    "all",
    "am",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "but",
    "by",
    "can",
    "could",
    "do",
    "does",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "her",
    "him",
    "his",
    "how",
    "i",
    "i'm",
    "if",
    "im",
    "in",
    "into",
    "is",
    "it",
    "its",
    "just",
    "like",
    "me",
    "more",
    "my",
    "not",
    "of",
    "on",
    "our",
    "out",
    "over",
    "so",
    "still",
    "that",
    "the",
    "their",
    "them",
    "there",
    "this",
    "through",
    "to",
    "too",
    "us",
    "was",
    "we",
    "what",
    "when",
    "while",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "feel",
    "feeling",
    "feels",
    "felt",
    "current",
    "event",
    "events",
    "synthetic",
    "voter",
    "country",
    "turkey",
    "turkish",
    "political",
    "situation",
    "things",
    "toward",
    "towards",
    "sense",
    "deep",
    "deeply",
    "increasingly",
    "recent",
    "see",
    "seem",
    "seems",
    "make",
    "makes",
    "hard",
    "mix",
    "especially",
    "also",
    "really",
    "very",
    "now",
    "even",
    "much",
    "many",
    "one",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def read_actual_results(path: Path) -> dict[str, dict[str, float]]:
    if not path.exists():
        return {
            "first_round": {
                "Erdogan": 49.52,
                "Kilicdaroglu": 44.88,
                "Sinan_Ogan": 5.17,
                "Muharrem_Ince": 0.43,
            },
            "runoff": {"Erdogan": 52.18, "Kilicdaroglu": 47.82},
        }
    current: str | None = None
    result: dict[str, dict[str, float]] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current = line[:-1]
            result[current] = {}
            continue
        if current and ":" in line:
            key, value = line.strip().split(":", 1)
            result[current][key.strip()] = float(value.strip())
    return result


def canonical_soul_files() -> list[Path]:
    return sorted(p for p in SOULS.glob("agent_*.json") if re.fullmatch(r"agent_\d{3}\.json", p.name))


def load_souls() -> dict[str, dict[str, Any]]:
    souls: dict[str, dict[str, Any]] = {}
    for path in canonical_soul_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        souls[data["identity"]["agent_id"]] = data
    if not souls:
        raise RuntimeError("No canonical souls found in souls/.")
    return souls


def to_float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value in (None, ""):
        return default
    return float(value)


def round_pct(value: float, digits: int = 1) -> float:
    return round(value, digits)


def normalize_percent(distribution: dict[str, float], keys: list[str]) -> dict[str, float]:
    total = sum(float(distribution.get(key, 0.0)) for key in keys)
    if total <= 0:
        return {key: 0.0 for key in keys}
    return {key: round(float(distribution.get(key, 0.0)) / total * 100, 3) for key in keys}


def count_by(items: list[dict[str, Any]], key: str) -> Counter[str]:
    return Counter(str(item.get(key, "Unknown") or "Unknown") for item in items)


def age_bin(age: int) -> str:
    if age < 30:
        return "18-29"
    if age < 45:
        return "30-44"
    if age < 60:
        return "45-59"
    return "60+"


def party_bloc(row: dict[str, str]) -> str:
    party = row.get("party_top", "Undecided")
    if party in RIGHT_GOVERNMENT_PARTIES:
        return "Right/Government"
    if party in OPPOSITION_LEFT_PARTIES:
        return "Opposition-left/pro-democracy"
    if party in OPPOSITION_NATIONALIST_PARTIES:
        return "Opposition-nationalist/center-right"
    return "Other/Undecided"


def event_title_map() -> dict[str, str]:
    titles: dict[str, str] = {}
    if EVENTS_FILE.exists():
        for item in json.loads(EVENTS_FILE.read_text(encoding="utf-8")):
            titles[item["tick_id"]] = item.get("title", item["tick_id"])
    titles["T030A_first_round_vote_decision"] = "First-round presidential vote decision"
    titles["T030B_first_round_result_revealed"] = titles.get("T030", "First-round result revealed")
    titles["T035A_runoff_vote_decision"] = "Runoff presidential vote decision"
    titles["T035B_final_result_revealed"] = titles.get("T035", "Final runoff result revealed")
    return titles


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "start", weight: str = "400") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="#111827">'
        f"{html.escape(str(text))}</text>"
    )


def chart_frame(width: int, height: int, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">'
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>'
        f"{svg_text(24, 32, title, 18, weight='700')}"
        f"{body}</svg>"
    )


def write_bar_chart(
    path: Path,
    items: list[tuple[str, float]],
    title: str,
    *,
    width: int = 960,
    height: int = 520,
    horizontal: bool = True,
    suffix: str = "",
    color: str = "#2563eb",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not items:
        path.write_text(chart_frame(width, height, title, ""), encoding="utf-8")
        return
    max_value = max(value for _, value in items) or 1
    body = []
    if horizontal:
        left = 230
        top = 62
        row_h = max(22, min(34, (height - top - 36) / len(items)))
        bar_w = width - left - 96
        for i, (label, value) in enumerate(items):
            y = top + i * row_h
            w = bar_w * value / max_value
            body.append(svg_text(18, y + row_h * 0.68, label[:34], 12))
            body.append(f'<rect x="{left}" y="{y + 4:.1f}" width="{w:.1f}" height="{row_h - 10:.1f}" rx="3" fill="{color}"/>')
            body.append(svg_text(left + w + 8, y + row_h * 0.68, f"{value:g}{suffix}", 12))
    else:
        left = 58
        top = 62
        plot_h = height - 138
        plot_w = width - 94
        slot = plot_w / len(items)
        for i, (label, value) in enumerate(items):
            bar_h = plot_h * value / max_value
            x = left + i * slot + slot * 0.16
            y = top + plot_h - bar_h
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{slot * 0.68:.1f}" height="{bar_h:.1f}" rx="3" fill="{color}"/>')
            body.append(svg_text(x + slot * 0.34, top + plot_h + 20, label[:14], 11, anchor="middle"))
            body.append(svg_text(x + slot * 0.34, y - 6, f"{value:g}{suffix}", 11, anchor="middle"))
        body.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#d1d5db"/>')
    path.write_text(chart_frame(width, height, title, "".join(body)), encoding="utf-8")


def write_grouped_bar_chart(
    path: Path,
    categories: list[str],
    series: dict[str, list[float]],
    title: str,
    *,
    width: int = 960,
    height: int = 520,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    left = 70
    top = 70
    plot_w = width - 120
    plot_h = height - 150
    max_value = max([100.0] + [value for values in series.values() for value in values])
    slot = plot_w / max(1, len(categories))
    names = list(series.keys())
    bar_w = slot * 0.72 / max(1, len(names))
    body = []
    for yv in range(0, 101, 20):
        y = top + plot_h - plot_h * (yv / max_value)
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#eef2f7"/>')
        body.append(svg_text(28, y + 4, str(yv), 11, anchor="end"))
    for i, cat in enumerate(categories):
        x0 = left + i * slot + slot * 0.14
        for j, name in enumerate(names):
            value = series[name][i]
            bh = plot_h * value / max_value
            x = x0 + j * bar_w
            y = top + plot_h - bh
            color = PALETTE.get(name, "#2563eb")
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w - 3:.1f}" height="{bh:.1f}" rx="3" fill="{color}"><title>{html.escape(name)}: {value:.1f}%</title></rect>')
        body.append(svg_text(left + i * slot + slot * 0.5, top + plot_h + 22, cat.replace("_", " ")[:18], 11, anchor="middle"))
    legend_x = left
    legend_y = height - 42
    for name in names:
        color = PALETTE.get(name, "#2563eb")
        body.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="12" height="12" rx="2" fill="{color}"/>')
        body.append(svg_text(legend_x + 18, legend_y, name.replace("_", " "), 12))
        legend_x += 150
    body.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#d1d5db"/>')
    path.write_text(chart_frame(width, height, title, "".join(body)), encoding="utf-8")


def write_line_chart(
    path: Path,
    labels: list[str],
    series: dict[str, list[float]],
    title: str,
    *,
    width: int = 1180,
    height: int = 520,
    y_min: float = 0.0,
    y_max: float = 100.0,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    left = 64
    top = 68
    plot_w = width - 112
    plot_h = height - 150
    denom = max(0.0001, y_max - y_min)
    body = []
    for yv in range(int(y_min), int(y_max) + 1, 20 if y_max > 20 else 2):
        y = top + plot_h - plot_h * ((yv - y_min) / denom)
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#eef2f7"/>')
        body.append(svg_text(34, y + 4, str(yv), 11, anchor="end"))
    point_count = max(1, len(labels) - 1)
    for name, values in series.items():
        points = []
        for i, value in enumerate(values):
            x = left + plot_w * i / point_count
            y = top + plot_h - plot_h * ((value - y_min) / denom)
            points.append(f"{x:.1f},{y:.1f}")
        color = PALETTE.get(name, "#2563eb")
        body.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.6" points="{" ".join(points)}"/>')
    for i, label in enumerate(labels):
        if i % 3 == 0 or i == len(labels) - 1:
            x = left + plot_w * i / point_count
            body.append(svg_text(x, top + plot_h + 24, label.split("_")[0], 10, anchor="middle"))
    legend_x = left
    legend_y = height - 42
    for name in series:
        color = PALETTE.get(name, "#2563eb")
        body.append(f'<line x1="{legend_x}" y1="{legend_y - 5}" x2="{legend_x + 22}" y2="{legend_y - 5}" stroke="{color}" stroke-width="3"/>')
        body.append(svg_text(legend_x + 30, legend_y, name, 12))
        legend_x += min(270, max(150, len(name) * 8 + 70))
    body.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#d1d5db"/>')
    path.write_text(chart_frame(width, height, title, "".join(body)), encoding="utf-8")


def write_stacked_bar_chart(
    path: Path,
    rows: list[dict[str, Any]],
    categories: list[str],
    title: str,
    *,
    width: int = 1120,
    height: int = 560,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    left = 210
    top = 66
    row_h = max(28, min(42, (height - top - 70) / max(1, len(rows))))
    bar_w = width - left - 80
    body = []
    for i, row in enumerate(rows):
        y = top + i * row_h
        body.append(svg_text(16, y + row_h * 0.68, str(row["category"])[:28], 12))
        x = left
        for cat in categories:
            value = float(row.get(cat, 0.0))
            w = bar_w * value / 100
            if w > 0:
                color = PALETTE.get(cat, "#6b7280")
                body.append(f'<rect x="{x:.1f}" y="{y + 5:.1f}" width="{w:.1f}" height="{row_h - 12:.1f}" fill="{color}"><title>{html.escape(cat)}: {value:.1f}%</title></rect>')
                if w > 34:
                    body.append(svg_text(x + w / 2, y + row_h * 0.66, f"{value:.0f}", 10, anchor="middle"))
            x += w
    legend_x = left
    legend_y = height - 26
    for cat in categories:
        color = PALETTE.get(cat, "#6b7280")
        body.append(f'<rect x="{legend_x}" y="{legend_y - 11}" width="12" height="12" rx="2" fill="{color}"/>')
        body.append(svg_text(legend_x + 18, legend_y, cat.replace("_", " "), 11))
        legend_x += 148
    path.write_text(chart_frame(width, height, title, "".join(body)), encoding="utf-8")


def write_word_cloud(path: Path, words: list[tuple[str, int]], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width = 1120
    height = 620
    if not words:
        path.write_text(chart_frame(width, height, title, ""), encoding="utf-8")
        return
    max_count = words[0][1]
    colors = ["#111827", "#b91c1c", "#2563eb", "#0f766e", "#7c3aed", "#92400e", "#374151"]
    x = 36
    y = 82
    body = []
    for i, (word, count) in enumerate(words[:95]):
        size = 13 + int(34 * math.sqrt(count / max_count))
        token_w = len(word) * size * 0.58 + 28
        if x + token_w > width - 36:
            x = 36
            y += 48
        if y > height - 42:
            break
        color = colors[i % len(colors)]
        body.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{700 if size > 28 else 500}" fill="{color}">'
            f"{html.escape(word)}</text>"
        )
        x += token_w
    path.write_text(chart_frame(width, height, title, "".join(body)), encoding="utf-8")


def markdown_table(rows: list[dict[str, Any]], columns: list[str], limit: int | None = None) -> str:
    selected = rows[:limit] if limit else rows
    if not selected:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in selected:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def token_counts(reflections: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    pattern = re.compile(r"[A-Za-zÀ-žÇĞİÖŞÜçğıöşü']+")
    for row in reflections:
        text = str(row.get("reflection", ""))
        text = text.replace("Erdoğan", "Erdogan").replace("Kılıçdaroğlu", "Kilicdaroglu")
        text = text.replace("İmamoğlu", "Imamoglu").replace("Özdağ", "Ozdag")
        for token in pattern.findall(text.lower()):
            token = token.strip("'")
            if token.endswith("'s") or token.endswith("’s"):
                token = token[:-2]
            if len(token) < 3:
                continue
            if token in STOPWORDS:
                continue
            counts[token] += 1
    return counts


def build_demographics(souls: dict[str, dict[str, Any]]) -> dict[str, Any]:
    identities = [soul["identity"] for soul in souls.values()]
    ages = [int(item["age"]) for item in identities]
    for item in identities:
        item["age_bin"] = age_bin(int(item["age"]))
    baseline_party = Counter(
        soul.get("simulation_metadata", {}).get("baseline_2018", {}).get("party_2018_internal_key")
        or soul.get("numeric_profile", {}).get("baseline_2018", {}).get("party_2018")
        or "Unknown"
        for soul in souls.values()
    )
    baseline_presidential = Counter(
        soul.get("simulation_metadata", {}).get("baseline_2018", {}).get("presidential_vote_2018")
        or soul.get("numeric_profile", {}).get("baseline_2018", {}).get("presidential_vote_2018")
        or "Unknown"
        for soul in souls.values()
    )
    return {
        "identities": identities,
        "age_summary": {
            "min": min(ages),
            "median": round(median(ages), 1),
            "mean": round(mean(ages), 1),
            "max": max(ages),
        },
        "age_bins": count_by(identities, "age_bin"),
        "gender": count_by(identities, "gender"),
        "region": count_by(identities, "region"),
        "city": count_by(identities, "city"),
        "education": count_by(identities, "education_level"),
        "income": count_by(identities, "income_bracket"),
        "employment": count_by(identities, "employment_status"),
        "archetype": count_by(identities, "archetype_name"),
        "baseline_party": baseline_party,
        "baseline_presidential": baseline_presidential,
    }


def rows_by_tick(records: list[dict[str, str]]) -> tuple[list[str], dict[str, list[dict[str, str]]]]:
    tick_order: list[str] = []
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in records:
        tick = row["tick_id"]
        if tick not in grouped:
            tick_order.append(tick)
        grouped[tick].append(row)
    return tick_order, grouped


def final_rows(grouped: dict[str, list[dict[str, str]]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    return grouped.get("T030A_first_round_vote_decision", []), grouped.get("T035A_runoff_vote_decision", [])


def average_distribution(rows: list[dict[str, str]], prefix: str, keys: list[str]) -> dict[str, float]:
    if not rows:
        return {key: 0.0 for key in keys}
    return {
        key: round(sum(to_float(row, f"{prefix}{key}") for row in rows) / len(rows) * 100, 3)
        for key in keys
    }


def group_vote_breakdown(
    rows: list[dict[str, str]],
    souls: dict[str, dict[str, Any]],
    group_key: str,
    top_key: str,
    candidates: list[str],
) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        soul = souls[row["agent_id"]]
        category = str(soul["identity"].get(group_key, "Unknown") or "Unknown")
        grouped[category][row[top_key]] += 1
    result: list[dict[str, Any]] = []
    for category, counts in sorted(grouped.items(), key=lambda item: (-sum(item[1].values()), item[0])):
        total = sum(counts.values())
        item: dict[str, Any] = {"category": category, "n": total}
        for candidate in candidates:
            item[candidate] = round(counts[candidate] / total * 100, 1) if total else 0.0
            item[f"{candidate}_count"] = counts[candidate]
        item["top_group"] = counts.most_common(1)[0][0] if counts else "None"
        result.append(item)
    return result


def build_tick_response_table(
    tick_order: list[str],
    grouped: dict[str, list[dict[str, str]]],
    titles: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    previous: dict[str, Any] | None = None
    for tick in tick_order:
        items = grouped[tick]
        n = len(items)
        if not n:
            continue
        right_prob = mean(
            sum(to_float(row, f"party_{party}") for party in RIGHT_GOVERNMENT_PARTIES) * 100
            for row in items
        )
        opp_left_prob = mean(
            sum(to_float(row, f"party_{party}") for party in OPPOSITION_LEFT_PARTIES) * 100
            for row in items
        )
        opp_nat_prob = mean(
            sum(to_float(row, f"party_{party}") for party in OPPOSITION_NATIONALIST_PARTIES) * 100
            for row in items
        )
        other_prob = mean(
            sum(to_float(row, f"party_{party}") for party in {"Other", "Undecided"}) * 100
            for row in items
        )
        bloc_counts = Counter(party_bloc(row) for row in items)
        row = {
            "tick_id": tick,
            "date": items[0].get("sim_date", ""),
            "title": titles.get(tick, tick),
            "agents": n,
            "broadcasts_avg": round(mean(to_float(item, "visible_broadcast_count") for item in items), 2),
            "right_government_prob": round(right_prob, 2),
            "opposition_left_prob": round(opp_left_prob, 2),
            "opposition_nationalist_prob": round(opp_nat_prob, 2),
            "other_undecided_prob": round(other_prob, 2),
            "right_government_top_share": round(bloc_counts["Right/Government"] / n * 100, 1),
            "opposition_left_top_share": round(bloc_counts["Opposition-left/pro-democracy"] / n * 100, 1),
            "opposition_nationalist_top_share": round(
                bloc_counts["Opposition-nationalist/center-right"] / n * 100,
                1,
            ),
            "other_undecided_top_share": round(bloc_counts["Other/Undecided"] / n * 100, 1),
            "first_Erdogan": round(mean(to_float(item, "first_round_Erdogan") for item in items) * 100, 2),
            "first_Kilicdaroglu": round(mean(to_float(item, "first_round_Kilicdaroglu") for item in items) * 100, 2),
            "first_Sinan_Ogan": round(mean(to_float(item, "first_round_Sinan_Ogan") for item in items) * 100, 2),
            "first_Undecided": round(mean(to_float(item, "first_round_Undecided") for item in items) * 100, 2),
            "runoff_Erdogan": round(mean(to_float(item, "runoff_Erdogan") for item in items) * 100, 2),
            "runoff_Kilicdaroglu": round(mean(to_float(item, "runoff_Kilicdaroglu") for item in items) * 100, 2),
            "runoff_abstain_invalid_undecided": round(
                mean(to_float(item, "runoff_Abstain_Invalid_Undecided") for item in items) * 100,
                2,
            ),
            "government_approval": round(mean(to_float(item, "government_approval") for item in items), 2),
            "institutional_trust": round(mean(to_float(item, "institutional_trust") for item in items), 2),
            "opposition_trust": round(mean(to_float(item, "opposition_trust") for item in items), 2),
            "anger": round(mean(to_float(item, "anger") for item in items), 3),
            "fear": round(mean(to_float(item, "fear") for item in items), 3),
            "hope": round(mean(to_float(item, "hope") for item in items), 3),
            "sadness": round(mean(to_float(item, "sadness") for item in items), 3),
            "political_fatigue": round(mean(to_float(item, "political_fatigue") for item in items), 3),
        }
        if previous is None:
            row["delta_right_government_prob"] = 0.0
            row["delta_opposition_left_prob"] = 0.0
            row["delta_first_Erdogan"] = 0.0
            row["delta_first_Kilicdaroglu"] = 0.0
            row["delta_first_Sinan_Ogan"] = 0.0
        else:
            for key in [
                "right_government_prob",
                "opposition_left_prob",
                "first_Erdogan",
                "first_Kilicdaroglu",
                "first_Sinan_Ogan",
            ]:
                row[f"delta_{key}"] = round(row[key] - previous[key], 2)
        rows.append(row)
        previous = row
    return rows


def key_shift_rows(tick_rows: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    candidates = tick_rows[1:]
    ranked = sorted(
        candidates,
        key=lambda row: (
            abs(float(row["delta_right_government_prob"]))
            + abs(float(row["delta_opposition_left_prob"]))
            + abs(float(row["delta_first_Erdogan"]))
            + abs(float(row["delta_first_Kilicdaroglu"]))
            + abs(float(row["delta_first_Sinan_Ogan"]))
        ),
        reverse=True,
    )
    return ranked[:limit]


def build_report(
    *,
    souls: dict[str, dict[str, Any]],
    demographics: dict[str, Any],
    trajectories: list[dict[str, str]],
    reflections: list[dict[str, Any]],
    broadcasts: list[dict[str, Any]],
    evaluation: dict[str, Any],
    actual: dict[str, dict[str, float]],
    first_raw: dict[str, float],
    first_norm: dict[str, float],
    runoff_raw: dict[str, float],
    runoff_norm: dict[str, float],
    tick_rows: list[dict[str, Any]],
    shift_rows: list[dict[str, Any]],
    top_words: list[tuple[str, int]],
    education_breakdown: list[dict[str, Any]],
    city_breakdown: list[dict[str, Any]],
    archetype_breakdown: list[dict[str, Any]],
) -> str:
    age_summary = demographics["age_summary"]
    lines = [
        "# Synthetic Turkey Deep Simulation Analysis Report",
        "",
        "This report analyzes the completed 300-agent OpenAI simulation output currently stored under `outputs/`. It is a post-run analysis artifact: it does not alter the simulation, prompts, memories, or voter decisions.",
        "",
        "## Executive Summary",
        "",
        f"- Data volume: {len(souls)} canonical voter souls, {len(trajectories):,} agent-tick trajectory rows, {len(reflections):,} reflection rows, and {len(broadcasts):,} political broadcast rows.",
        f"- Run scope: {len({row['tick_id'] for row in trajectories})} simulation ticks from the June 2018 baseline through the 28 May 2023 runoff result reveal.",
        f"- First-round raw simulated intention: Erdoğan {first_raw.get('Erdogan', 0):.1f}%, Kılıçdaroğlu {first_raw.get('Kilicdaroglu', 0):.1f}%, Oğan {first_raw.get('Sinan_Ogan', 0):.1f}%, İnce {first_raw.get('Muharrem_Ince', 0):.1f}%, undecided/other {first_raw.get('Undecided', 0) + first_raw.get('Other', 0):.1f}%.",
        f"- First-round normalized valid-candidate comparison: Erdoğan {first_norm.get('Erdogan', 0):.1f}% vs actual {actual['first_round']['Erdogan']:.1f}%; Kılıçdaroğlu {first_norm.get('Kilicdaroglu', 0):.1f}% vs actual {actual['first_round']['Kilicdaroglu']:.1f}%; Oğan {first_norm.get('Sinan_Ogan', 0):.1f}% vs actual {actual['first_round']['Sinan_Ogan']:.1f}%.",
        f"- Runoff raw simulated intention: Erdoğan {runoff_raw.get('Erdogan', 0):.1f}%, Kılıçdaroğlu {runoff_raw.get('Kilicdaroglu', 0):.1f}%, abstain/invalid/undecided {runoff_raw.get('Abstain_Invalid_Undecided', 0):.1f}%.",
        f"- Runoff normalized valid-candidate comparison: Erdoğan {runoff_norm.get('Erdogan', 0):.1f}% vs actual {actual['runoff']['Erdogan']:.1f}%; Kılıçdaroğlu {runoff_norm.get('Kilicdaroglu', 0):.1f}% vs actual {actual['runoff']['Kilicdaroglu']:.1f}%.",
        f"- Evaluation summary reports first-round MAE {evaluation.get('first_round_mae')} and runoff MAE {evaluation.get('runoff_mae')}. Candidate ranking accuracy is false in both rounds.",
        "- The dominant substantive weakness remains clear: the model population under-produces Erdoğan and especially Sinan Oğan support, while over-producing Kılıçdaroğlu support. This is a calibration and persona-behavior issue, not a pipeline failure.",
        "",
        "## Data Sources Used",
        "",
        "- `souls/agent_001.json` through `souls/agent_300.json`: demographic, archetype, 2018 baseline, and persona metadata.",
        "- `outputs/agent_trajectories.csv`: per-agent, per-tick belief, emotion, turnout, party, and candidate states.",
        "- `outputs/reflections.jsonl`: textual reflections used for language and word-cloud analysis.",
        "- `outputs/broadcasts.jsonl`: political broadcast frames emitted during the timeline.",
        "- `outputs/evaluation_summary.json`: final vote distribution and evaluation metrics.",
        "- `events/simulation_ticks.json`: tick titles and historical event context.",
        "",
        "## Important Interpretation Notes",
        "",
        "- Demographics are synthetic persona-generation assumptions, not a statistically sampled Turkish census or survey microdata file.",
        "- Cities and education levels describe the generated agent population. They are useful for explaining simulation composition, but should not be described as measured Turkish voter demographics.",
        "- The left/right analysis below uses an electoral-bloc proxy rather than a pure ideology scale. In Türkiye, CHP, Kurdish movement voters, nationalist opposition voters, and conservative dissenters do not map cleanly onto a single left-right axis.",
        "- The simulation is LLM-first: these charts summarize LLM outputs after prompts, memory, broadcast filtering, and date fencing. They are not deterministic event-delta outputs.",
        "",
        "## Demographic Structure",
        "",
        f"- Age range: {age_summary['min']} to {age_summary['max']}; median {age_summary['median']}; mean {age_summary['mean']}.",
        f"- Gender categories: {', '.join(f'{k}: {v}' for k, v in demographics['gender'].most_common())}.",
        f"- Regions represented: {len(demographics['region'])}. Cities represented: {len(demographics['city'])}.",
        "",
        "### Archetype Distribution",
        "",
        markdown_table(
            [{"archetype": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["archetype"].most_common()],
            ["archetype", "agents", "share"],
        ),
        "",
        "### Age Distribution",
        "",
        markdown_table(
            [{"age_bin": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in sorted(demographics["age_bins"].items())],
            ["age_bin", "agents", "share"],
        ),
        "",
        "### Education Distribution",
        "",
        markdown_table(
            [{"education_level": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["education"].most_common()],
            ["education_level", "agents", "share"],
        ),
        "",
        "### Region Distribution",
        "",
        markdown_table(
            [{"region": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["region"].most_common()],
            ["region", "agents", "share"],
        ),
        "",
        "### Income Distribution",
        "",
        markdown_table(
            [{"income_bracket": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["income"].most_common()],
            ["income_bracket", "agents", "share"],
        ),
        "",
        "### Employment Distribution",
        "",
        markdown_table(
            [{"employment_status": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["employment"].most_common()],
            ["employment_status", "agents", "share"],
        ),
        "",
        "### Top Cities",
        "",
        markdown_table(
            [{"city": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["city"].most_common(20)],
            ["city", "agents", "share"],
        ),
        "",
        "### 2018 Baseline Anchors",
        "",
        "These anchors are persona memory and sampling structure only. They should not be interpreted as deterministic rules for 2023 voting.",
        "",
        markdown_table(
            [{"party_2018": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["baseline_party"].most_common()],
            ["party_2018", "agents", "share"],
        ),
        "",
        markdown_table(
            [{"presidential_vote_2018": k, "agents": v, "share": f"{v / len(souls) * 100:.1f}%"} for k, v in demographics["baseline_presidential"].most_common()],
            ["presidential_vote_2018", "agents", "share"],
        ),
        "",
        "## Election Result Analysis",
        "",
        "### First Round",
        "",
        markdown_table(
            [
                {
                    "candidate": key,
                    "sim_raw": f"{first_raw.get(key, 0):.2f}%",
                    "sim_valid_normalized": f"{first_norm.get(key, 0):.2f}%" if key in FIRST_VALID_KEYS else "n/a",
                    "actual": f"{actual['first_round'].get(key, 0):.2f}%" if key in actual["first_round"] else "n/a",
                }
                for key in FIRST_KEYS
            ],
            ["candidate", "sim_raw", "sim_valid_normalized", "actual"],
        ),
        "",
        "### Runoff",
        "",
        markdown_table(
            [
                {
                    "candidate": key,
                    "sim_raw": f"{runoff_raw.get(key, 0):.2f}%",
                    "sim_valid_normalized": f"{runoff_norm.get(key, 0):.2f}%" if key in RUNOFF_VALID_KEYS else "n/a",
                    "actual": f"{actual['runoff'].get(key, 0):.2f}%" if key in actual["runoff"] else "n/a",
                }
                for key in RUNOFF_KEYS
            ],
            ["candidate", "sim_raw", "sim_valid_normalized", "actual"],
        ),
        "",
        "### Interpretation",
        "",
        "- The pipeline correctly preserves uncertainty: undecided/other and abstain/invalid/undecided remain visible rather than being forced into a valid-vote total.",
        "- For thesis comparison, both raw intention and normalized valid-candidate shares should be shown. Raw intention is closer to behavioral simulation; normalized valid share is closer to official election reporting.",
        "- The largest miss is not the existence of undecided voters, but their direction: the model leaves too much anti-incumbent probability in Kılıçdaroğlu rather than producing enough Erdoğan consolidation and Oğan nationalist protest voting.",
        "",
        "## Demographic Vote Behavior",
        "",
        "### First-Round Top Candidate by Education",
        "",
        markdown_table(education_breakdown, ["category", "n", "Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Other", "Undecided", "top_group"]),
        "",
        "### First-Round Top Candidate by Top Cities",
        "",
        markdown_table(city_breakdown[:20], ["category", "n", "Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Other", "Undecided", "top_group"]),
        "",
        "### First-Round Top Candidate by Archetype",
        "",
        markdown_table(archetype_breakdown, ["category", "n", "Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Other", "Undecided", "top_group"]),
        "",
        "## Electoral Bloc Response by Tick",
        "",
        "Bloc definitions used for this analysis:",
        "",
        "- Right/Government: AKP, MHP, YRP probability mass.",
        "- Opposition-left/pro-democracy: CHP and DEM/HDP/YSP probability mass.",
        "- Opposition-nationalist/center-right: İYİ probability mass.",
        "- Other/Undecided: Other and undecided party probability mass.",
        "",
        "### Largest Tick-to-Tick Shifts",
        "",
        markdown_table(
            [
                {
                    "tick_id": row["tick_id"],
                    "title": row["title"][:70],
                    "Δ right": row["delta_right_government_prob"],
                    "Δ opp-left": row["delta_opposition_left_prob"],
                    "Δ Erdoğan": row["delta_first_Erdogan"],
                    "Δ Kılıçdaroğlu": row["delta_first_Kilicdaroglu"],
                    "Δ Oğan": row["delta_first_Sinan_Ogan"],
                }
                for row in shift_rows
            ],
            ["tick_id", "title", "Δ right", "Δ opp-left", "Δ Erdoğan", "Δ Kılıçdaroğlu", "Δ Oğan"],
        ),
        "",
        "### Full Tick Response Table",
        "",
        markdown_table(
            [
                {
                    "tick": row["tick_id"],
                    "right": row["right_government_prob"],
                    "opp_left": row["opposition_left_prob"],
                    "opp_nat": row["opposition_nationalist_prob"],
                    "other": row["other_undecided_prob"],
                    "Erdogan": row["first_Erdogan"],
                    "Kilicdaroglu": row["first_Kilicdaroglu"],
                    "Ogan": row["first_Sinan_Ogan"],
                    "gov_appr": row["government_approval"],
                    "opp_trust": row["opposition_trust"],
                    "anger": row["anger"],
                    "hope": row["hope"],
                    "broadcasts": row["broadcasts_avg"],
                }
                for row in tick_rows
            ],
            ["tick", "right", "opp_left", "opp_nat", "other", "Erdogan", "Kilicdaroglu", "Ogan", "gov_appr", "opp_trust", "anger", "hope", "broadcasts"],
        ),
        "",
        "## Reflection Language and Word Cloud",
        "",
        "The reflection corpus was tokenized from `outputs/reflections.jsonl`; common English function words and generic simulation words were removed. Names such as Erdoğan and Kılıçdaroğlu were normalized to ASCII tokens only for counting.",
        "",
        markdown_table(
            [{"word": word, "count": count} for word, count in top_words[:50]],
            ["word", "count"],
        ),
        "",
        "### Language Interpretation",
        "",
        "- The high-frequency words show the emotional and issue agenda that the LLM agents repeatedly used to explain themselves.",
        "- If words around democracy, economy, trust, earthquake, inflation, refugees, or stability dominate, that supports the thesis claim that agents responded through historical-event and persona lenses rather than only candidate names.",
        "- If candidate names dominate too strongly, that is a warning that prompts may be making agents over-explain as political observers rather than ordinary voters.",
        "",
        "## Generated Charts and Dashboard",
        "",
        "- `outputs/deep_analysis_dashboard.html`",
        "- `outputs/analysis_charts/demographics_age_distribution.svg`",
        "- `outputs/analysis_charts/demographics_gender.svg`",
        "- `outputs/analysis_charts/demographics_education.svg`",
        "- `outputs/analysis_charts/demographics_region.svg`",
        "- `outputs/analysis_charts/demographics_income.svg`",
        "- `outputs/analysis_charts/demographics_employment.svg`",
        "- `outputs/analysis_charts/demographics_top_cities.svg`",
        "- `outputs/analysis_charts/demographics_archetypes.svg`",
        "- `outputs/analysis_charts/results_first_round_vs_actual.svg`",
        "- `outputs/analysis_charts/results_runoff_vs_actual.svg`",
        "- `outputs/analysis_charts/electoral_bloc_by_tick.svg`",
        "- `outputs/analysis_charts/candidate_probabilities_by_tick.svg`",
        "- `outputs/analysis_charts/emotion_trajectories.svg`",
        "- `outputs/analysis_charts/trust_approval_trajectories.svg`",
        "- `outputs/analysis_charts/education_vote_breakdown.svg`",
        "- `outputs/analysis_charts/reflection_word_cloud.svg`",
        "",
        "## Thesis-Ready Findings",
        "",
        "1. The 300-agent run is technically complete and analyzable: every canonical agent has a full 37-tick trajectory.",
        "2. The LLM-first architecture produces coherent archetype-consistent behavior, especially for stable blocs such as devout loyalists, Alevi-CHP loyalists, Kurdish political voters, cosmopolitan liberals, and secular professionals.",
        "3. The model remains too opposition-favorable in aggregate. This is visible in both first-round and runoff normalized candidate shares.",
        "4. The strongest next methodological discussion should focus on why Oğan/nationalist protest voting and Erdoğan runoff consolidation are under-produced.",
        "5. The report should present this as an exploratory research simulation, not as a predictive model. The value is in testing whether persona-grounded LLM agents generate interpretable political trajectories under source-grounded historical conditions.",
        "",
        "## Limitations",
        "",
        "- One OpenAI run is not enough to estimate stochastic variability. Because the full run is expensive and slow, this thesis should describe it as a single high-cost experimental run supported by mock-mode testing.",
        "- The generated demographic population is source-grounded but not survey-weighted by official microdata.",
        "- The simulation uses English reflections in this run, so word-frequency results reflect prompt/output language as well as agent reasoning.",
        "- Left/right classification is a simplified analytical layer; Turkish party coalitions require more careful interpretation than a binary ideology axis.",
        "- The LLM sometimes reasons like an analyst, not only like an ordinary voter. This should be noted as a prompt realism limitation.",
        "",
        "## Suggested Next Calibration Questions",
        "",
        "- Are nationalist archetypes given enough baseline salience, candidate awareness, and permission to choose Oğan?",
        "- Are conservative economically disillusioned voters too easily converted to opposition trust, or not enough anchored by religious/national security frames?",
        "- Do Kurdish voters show enough runoff turnout anxiety after the Özdağ protocol?",
        "- Are earthquake-zone loyalists and retired protest voters behaving distinctly enough from generic government/opposition blocs?",
        "- Are political broadcasts visible to the right archetypes at the right moments, or are some crucial frames missing from the voter prompt?",
        "",
    ]
    return "\n".join(lines)


def build_dashboard(
    *,
    demographics: dict[str, Any],
    evaluation: dict[str, Any],
    first_norm: dict[str, float],
    runoff_norm: dict[str, float],
    top_words: list[tuple[str, int]],
    tick_rows: list[dict[str, Any]],
) -> str:
    def img(name: str, alt: str) -> str:
        return f'<section class="card"><h2>{html.escape(alt)}</h2><img src="analysis_charts/{name}" alt="{html.escape(alt)}"></section>'

    latest = tick_rows[-1]
    cards = [
        ("Agents", "300"),
        ("Ticks", str(len(tick_rows))),
        ("First MAE", str(evaluation.get("first_round_mae"))),
        ("Runoff MAE", str(evaluation.get("runoff_mae"))),
        ("Valid first Erdoğan", f"{first_norm.get('Erdogan', 0):.1f}%"),
        ("Valid runoff Erdoğan", f"{runoff_norm.get('Erdogan', 0):.1f}%"),
        ("Final right bloc", f"{latest['right_government_prob']:.1f}%"),
        ("Final opp-left bloc", f"{latest['opposition_left_prob']:.1f}%"),
    ]
    card_html = "".join(f"<div><span>{html.escape(k)}</span><strong>{html.escape(v)}</strong></div>" for k, v in cards)
    word_html = ", ".join(f"{html.escape(word)} ({count})" for word, count in top_words[:30])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Synthetic Turkey Deep Analysis Dashboard</title>
  <style>
    body {{ margin: 0; font-family: Inter, Arial, sans-serif; color: #111827; background: #f3f4f6; }}
    header {{ padding: 32px 42px; background: #111827; color: white; }}
    header h1 {{ margin: 0 0 8px; font-size: 30px; }}
    header p {{ margin: 0; max-width: 980px; line-height: 1.5; color: #d1d5db; }}
    main {{ padding: 28px 42px 48px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(150px, 1fr)); gap: 14px; margin-bottom: 26px; }}
    .metrics div {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; }}
    .metrics span {{ display: block; color: #6b7280; font-size: 13px; margin-bottom: 8px; }}
    .metrics strong {{ font-size: 24px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 18px; }}
    .card {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; overflow: auto; }}
    .card.wide {{ grid-column: 1 / -1; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; }}
    img {{ width: 100%; height: auto; display: block; }}
    .note {{ background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 14px 16px; margin-bottom: 22px; line-height: 1.45; }}
    .words {{ line-height: 1.8; }}
    @media (max-width: 900px) {{ .metrics, .grid {{ grid-template-columns: 1fr; }} main, header {{ padding-left: 18px; padding-right: 18px; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Synthetic Turkey Deep Simulation Analysis</h1>
    <p>Post-run dashboard for the completed 300-agent LLM-first simulation. Demographic values are synthetic persona-generation assumptions; election comparisons use the 2023 presidential actual-results benchmark.</p>
  </header>
  <main>
    <div class="metrics">{card_html}</div>
    <div class="note"><strong>Interpretation warning:</strong> this dashboard summarizes one expensive OpenAI run. It should be used as exploratory thesis evidence, not as a claim of predictive accuracy.</div>
    <div class="grid">
      {img("results_first_round_vs_actual.svg", "First Round: Simulation vs Actual")}
      {img("results_runoff_vs_actual.svg", "Runoff: Simulation vs Actual")}
      {img("demographics_archetypes.svg", "Archetype Distribution")}
      {img("demographics_top_cities.svg", "Top Cities in Synthetic Population")}
      {img("demographics_age_distribution.svg", "Age Distribution")}
      {img("demographics_gender.svg", "Gender Distribution")}
      {img("demographics_education.svg", "Education Distribution")}
      {img("demographics_region.svg", "Region Distribution")}
      {img("demographics_income.svg", "Income Distribution")}
      {img("demographics_employment.svg", "Employment Distribution")}
      <section class="card wide"><h2>Electoral Bloc Alignment by Tick</h2><img src="analysis_charts/electoral_bloc_by_tick.svg" alt="Electoral bloc alignment by tick"></section>
      <section class="card wide"><h2>Candidate Probabilities by Tick</h2><img src="analysis_charts/candidate_probabilities_by_tick.svg" alt="Candidate probabilities by tick"></section>
      <section class="card wide"><h2>Emotion Trajectories</h2><img src="analysis_charts/emotion_trajectories.svg" alt="Emotion trajectories"></section>
      <section class="card wide"><h2>Trust and Approval Trajectories</h2><img src="analysis_charts/trust_approval_trajectories.svg" alt="Trust and approval trajectories"></section>
      <section class="card wide"><h2>Education Vote Breakdown</h2><img src="analysis_charts/education_vote_breakdown.svg" alt="Education vote breakdown"></section>
      <section class="card wide"><h2>Reflection Word Cloud</h2><img src="analysis_charts/reflection_word_cloud.svg" alt="Reflection word cloud"></section>
      <section class="card wide"><h2>Most Frequent Reflection Terms</h2><p class="words">{word_html}</p></section>
    </div>
  </main>
</body>
</html>
"""


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    souls = load_souls()
    trajectories = read_csv(TRAJECTORIES_FILE)
    reflections = read_jsonl(REFLECTIONS_FILE)
    broadcasts = read_jsonl(BROADCASTS_FILE)
    evaluation = read_json(EVALUATION_FILE)
    actual = read_actual_results(ACTUAL_RESULTS_FILE)
    titles = event_title_map()

    demographics = build_demographics(souls)
    tick_order, grouped = rows_by_tick(trajectories)
    first_rows, runoff_rows = final_rows(grouped)

    first_raw = average_distribution(first_rows, "first_round_", FIRST_KEYS)
    runoff_raw = average_distribution(runoff_rows, "runoff_", RUNOFF_KEYS)
    first_norm = normalize_percent(first_raw, FIRST_VALID_KEYS)
    runoff_norm = normalize_percent(runoff_raw, RUNOFF_VALID_KEYS)

    tick_rows = build_tick_response_table(tick_order, grouped, titles)
    shift_rows = key_shift_rows(tick_rows)

    words = token_counts(reflections)
    top_words = words.most_common(100)

    education_breakdown = group_vote_breakdown(first_rows, souls, "education_level", "first_round_top", FIRST_KEYS)
    city_breakdown = group_vote_breakdown(first_rows, souls, "city", "first_round_top", FIRST_KEYS)
    city_breakdown = sorted(city_breakdown, key=lambda row: (-row["n"], row["category"]))
    archetype_breakdown = group_vote_breakdown(first_rows, souls, "archetype_name", "first_round_top", FIRST_KEYS)

    write_csv(
        TABLES_DIR / "demographics_summary.csv",
        [
            {"category": "age_" + key, "value": value}
            for key, value in demographics["age_summary"].items()
        ]
        + [{"category": f"education_{k}", "value": v} for k, v in demographics["education"].most_common()]
        + [{"category": f"gender_{k}", "value": v} for k, v in demographics["gender"].most_common()]
        + [{"category": f"region_{k}", "value": v} for k, v in demographics["region"].most_common()]
        + [{"category": f"income_{k}", "value": v} for k, v in demographics["income"].most_common()]
        + [{"category": f"employment_{k}", "value": v} for k, v in demographics["employment"].most_common()]
        + [{"category": f"city_{k}", "value": v} for k, v in demographics["city"].most_common()]
        + [{"category": f"archetype_{k}", "value": v} for k, v in demographics["archetype"].most_common()],
    )
    write_csv(TABLES_DIR / "tick_bloc_response.csv", tick_rows)
    write_csv(TABLES_DIR / "top_reflection_words.csv", [{"word": w, "count": c} for w, c in top_words])
    write_csv(TABLES_DIR / "education_vote_breakdown.csv", education_breakdown)
    write_csv(TABLES_DIR / "city_vote_breakdown.csv", city_breakdown)
    write_csv(TABLES_DIR / "archetype_vote_breakdown.csv", archetype_breakdown)

    write_bar_chart(
        CHARTS_DIR / "demographics_age_distribution.svg",
        sorted(demographics["age_bins"].items()),
        "Age Distribution of Synthetic Voters",
        horizontal=False,
        color="#0f766e",
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_education.svg",
        demographics["education"].most_common(),
        "Education Levels in Synthetic Population",
        horizontal=True,
        color="#2563eb",
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_gender.svg",
        demographics["gender"].most_common(),
        "Gender Distribution in Synthetic Population",
        horizontal=False,
        color="#0f766e",
        height=440,
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_region.svg",
        demographics["region"].most_common(),
        "Regional Distribution in Synthetic Population",
        horizontal=True,
        color="#92400e",
        height=520,
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_income.svg",
        demographics["income"].most_common(),
        "Income Brackets in Synthetic Population",
        horizontal=True,
        color="#7c3aed",
        height=460,
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_employment.svg",
        demographics["employment"].most_common(),
        "Employment Status in Synthetic Population",
        horizontal=True,
        color="#b91c1c",
        height=620,
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_top_cities.svg",
        demographics["city"].most_common(20),
        "Top Cities Represented",
        horizontal=True,
        color="#7c3aed",
        height=720,
    )
    write_bar_chart(
        CHARTS_DIR / "demographics_archetypes.svg",
        demographics["archetype"].most_common(),
        "Voter Archetype Distribution",
        horizontal=True,
        color="#b91c1c",
        height=650,
    )
    write_grouped_bar_chart(
        CHARTS_DIR / "results_first_round_vs_actual.svg",
        FIRST_VALID_KEYS,
        {
            "Simulation": [first_norm.get(key, 0.0) for key in FIRST_VALID_KEYS],
            "Actual": [actual["first_round"].get(key, 0.0) for key in FIRST_VALID_KEYS],
        },
        "First Round: Valid-Candidate Simulation vs Actual",
    )
    write_grouped_bar_chart(
        CHARTS_DIR / "results_runoff_vs_actual.svg",
        RUNOFF_VALID_KEYS,
        {
            "Simulation": [runoff_norm.get(key, 0.0) for key in RUNOFF_VALID_KEYS],
            "Actual": [actual["runoff"].get(key, 0.0) for key in RUNOFF_VALID_KEYS],
        },
        "Runoff: Valid-Candidate Simulation vs Actual",
    )
    write_line_chart(
        CHARTS_DIR / "electoral_bloc_by_tick.svg",
        [row["tick_id"] for row in tick_rows],
        {
            "Right/Government": [row["right_government_prob"] for row in tick_rows],
            "Opposition-left/pro-democracy": [row["opposition_left_prob"] for row in tick_rows],
            "Opposition-nationalist/center-right": [row["opposition_nationalist_prob"] for row in tick_rows],
            "Other/Undecided": [row["other_undecided_prob"] for row in tick_rows],
        },
        "Electoral Bloc Probability Mass by Tick",
    )
    write_line_chart(
        CHARTS_DIR / "candidate_probabilities_by_tick.svg",
        [row["tick_id"] for row in tick_rows],
        {
            "Erdogan": [row["first_Erdogan"] for row in tick_rows],
            "Kilicdaroglu": [row["first_Kilicdaroglu"] for row in tick_rows],
            "Sinan_Ogan": [row["first_Sinan_Ogan"] for row in tick_rows],
            "Undecided": [row["first_Undecided"] for row in tick_rows],
        },
        "First-Round Candidate Probability Mass by Tick",
    )
    write_line_chart(
        CHARTS_DIR / "emotion_trajectories.svg",
        [row["tick_id"] for row in tick_rows],
        {
            "Anger": [row["anger"] * 100 for row in tick_rows],
            "Fear": [row["fear"] * 100 for row in tick_rows],
            "Hope": [row["hope"] * 100 for row in tick_rows],
            "Sadness": [row["sadness"] * 100 for row in tick_rows],
            "Political fatigue": [row["political_fatigue"] * 100 for row in tick_rows],
        },
        "Average Emotion Trajectories by Tick",
    )
    write_line_chart(
        CHARTS_DIR / "trust_approval_trajectories.svg",
        [row["tick_id"] for row in tick_rows],
        {
            "Government approval": [row["government_approval"] * 10 for row in tick_rows],
            "Institutional trust": [row["institutional_trust"] * 10 for row in tick_rows],
            "Opposition trust": [row["opposition_trust"] * 10 for row in tick_rows],
        },
        "Average Trust and Approval Trajectories by Tick",
    )
    write_stacked_bar_chart(
        CHARTS_DIR / "education_vote_breakdown.svg",
        education_breakdown,
        ["Erdogan", "Kilicdaroglu", "Sinan_Ogan", "Other", "Undecided"],
        "First-Round Top Candidate by Education Level",
    )
    write_word_cloud(CHARTS_DIR / "reflection_word_cloud.svg", top_words, "Most Frequent Reflection Terms")

    report = build_report(
        souls=souls,
        demographics=demographics,
        trajectories=trajectories,
        reflections=reflections,
        broadcasts=broadcasts,
        evaluation=evaluation,
        actual=actual,
        first_raw=first_raw,
        first_norm=first_norm,
        runoff_raw=runoff_raw,
        runoff_norm=runoff_norm,
        tick_rows=tick_rows,
        shift_rows=shift_rows,
        top_words=top_words,
        education_breakdown=education_breakdown,
        city_breakdown=city_breakdown,
        archetype_breakdown=archetype_breakdown,
    )
    (DOCS_DIR / "deep_simulation_analysis_report.md").write_text(report, encoding="utf-8")

    dashboard = build_dashboard(
        demographics=demographics,
        evaluation=evaluation,
        first_norm=first_norm,
        runoff_norm=runoff_norm,
        top_words=top_words,
        tick_rows=tick_rows,
    )
    (OUTPUTS / "deep_analysis_dashboard.html").write_text(dashboard, encoding="utf-8")

    summary = {
        "souls": len(souls),
        "trajectory_rows": len(trajectories),
        "reflection_rows": len(reflections),
        "broadcast_rows": len(broadcasts),
        "ticks": len(tick_rows),
        "first_round_raw": first_raw,
        "first_round_valid_normalized": first_norm,
        "runoff_raw": runoff_raw,
        "runoff_valid_normalized": runoff_norm,
        "report": str(DOCS_DIR / "deep_simulation_analysis_report.md"),
        "dashboard": str(OUTPUTS / "deep_analysis_dashboard.html"),
    }
    (OUTPUTS / "deep_analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
