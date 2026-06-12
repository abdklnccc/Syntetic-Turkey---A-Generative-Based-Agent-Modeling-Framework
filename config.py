import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency is declared, fallback keeps mock mode usable
    load_dotenv = None

ROOT = Path(__file__).parent


def _strip_env_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_env_file(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    loaded = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        os.environ[key] = _strip_env_value(value)
        loaded = True
    return loaded


if load_dotenv:
    load_dotenv(ROOT / ".env")
else:
    _load_env_file(ROOT / ".env")

# Core MVP scope: June 2018 baseline through the 28 May 2023 presidential runoff.
SIMULATION_START_DATE = "2018-06-24"
SIMULATION_END_DATE = "2023-05-29"

# Source-of-truth files.
VOTER_CONFIG_FILE = Path(os.getenv(
    "VOTER_CONFIG_FILE",
    ROOT / "voter_source_of_truth" / "synthetic_turkey_simulation.json",
))
POLITICAL_AGENTS_FILE = Path(os.getenv(
    "POLITICAL_AGENTS_FILE",
    ROOT / "political_broadcast_config" / "political_agents.yaml",
))
POLITICAL_PERSONAS_FILE = Path(os.getenv(
    "POLITICAL_PERSONAS_FILE",
    ROOT / "political_broadcast_config" / "political_personas.yaml",
))
CREDIBILITY_MATRIX_FILE = Path(os.getenv(
    "CREDIBILITY_MATRIX_FILE",
    ROOT / "political_broadcast_config" / "credibility_matrix.yaml",
))
POLITICIAN_EVENT_RESPONSES_FILE = Path(os.getenv(
    "POLITICIAN_EVENT_RESPONSES_FILE",
    ROOT / "political_broadcast_config" / "politician_event_responses.yaml",
))
MOVEMENT_STATE_MACHINE_FILE = Path(os.getenv(
    "MOVEMENT_STATE_MACHINE_FILE",
    ROOT / "political_broadcast_config" / "movement_state_machine.yaml",
))
SIMULATION_TICKS_FILE = Path(os.getenv(
    "SIMULATION_TICKS_FILE",
    ROOT / "events" / "simulation_ticks.json",
))
ACTUAL_RESULTS_FILE = Path(os.getenv(
    "ACTUAL_RESULTS_FILE",
    ROOT / "actual_results_2023.yaml",
))
BASELINE_SAMPLING_PROFILE_FILE = Path(os.getenv(
    "BASELINE_SAMPLING_PROFILE_FILE",
    ROOT / "voter_source_of_truth" / "2018_baseline_sampling_profile.yaml",
))

# Runtime paths.
SOULS_DIR = Path(os.getenv("SOULS_DIR", ROOT / "souls"))
LOGS_DIR = Path(os.getenv("LOGS_DIR", ROOT / "logs"))
DB_DIR = Path(os.getenv("DB_DIR", ROOT / "db"))
OUTPUTS_DIR = Path(os.getenv("OUTPUTS_DIR", ROOT / "outputs"))

BROADCAST_CACHE_DIR = Path(os.getenv("BROADCAST_CACHE_DIR", OUTPUTS_DIR / "broadcast_cache"))

for path in (SOULS_DIR, LOGS_DIR, DB_DIR, OUTPUTS_DIR, BROADCAST_CACHE_DIR):
    path.mkdir(exist_ok=True)

# LLM provider settings.
MOCK_LLM = os.getenv("MOCK_LLM", "1").lower() in {"1", "true", "yes", "on"}
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock" if MOCK_LLM else "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.45"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "900"))
OPENAI_TIMEOUT_SECONDS = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"))
OPENAI_MAX_RETRIES = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
OPENAI_RETRY_BASE_SECONDS = float(os.getenv("OPENAI_RETRY_BASE_SECONDS", "1.0"))

# Simulation parameters.
NUM_AGENTS = int(os.getenv("NUM_AGENTS", "50"))
NUM_TICKS = int(os.getenv("NUM_TICKS", "0"))  # 0 means all election-safe ticks.
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "8"))
MAX_TOKENS_WM = int(os.getenv("MAX_TOKENS_WM", "3500"))
RECENCY_DECAY = float(os.getenv("RECENCY_DECAY", "0.995"))
SOCIAL_FEED_SIZE = int(os.getenv("SOCIAL_FEED_SIZE", "5"))
GENERATED_SOUL_SEED = int(os.getenv("GENERATED_SOUL_SEED", "20230528"))
