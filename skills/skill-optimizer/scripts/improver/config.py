"""Constants, model profiles, and runtime configuration."""

from dataclasses import dataclass, field
from pathlib import Path

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent.parent  # skill-optimizer/
DATA_DIR = SKILL_DIR / "data"
CRITERIA_DIR = SKILL_DIR / "criteria"
CALIBRATION_DIR = SKILL_DIR / "calibration"
CLAUDE_BIN = "claude"

# Ensure data dirs exist
DATA_DIR.mkdir(exist_ok=True)
CALIBRATION_DIR.mkdir(exist_ok=True)

# --- Model Profiles ---
MODEL_PROFILES = {
    "quality":  {"eval": "opus",   "eval_2": "sonnet", "improve": "opus"},
    "balanced": {"eval": "sonnet", "eval_2": "haiku",  "improve": "sonnet"},
    "budget":   {"eval": "haiku",  "eval_2": "haiku",  "improve": "haiku"},
}

# Auto-routing thresholds
AUTO_ROUTE_OPUS_THRESHOLD = 800
AUTO_ROUTE_HAIKU_THRESHOLD = 200

# --- Confidence ---
CONFIDENCE_WEIGHTS = {"high": 1.0, "medium": 0.7, "low": 0.4}
ANTIGAMING_JUMP_THRESHOLD = 5

# --- Criteria Lifecycle ---
COOLDOWN_CYCLES = 3
MAX_CONSECUTIVE_FAILS = 3
PARK_THRESHOLD = 6
GRADUATE_THRESHOLD = 3
GRADUATE_SPOT_CHECK = 5
WARM_TIER_INTERVAL = 2
COLD_TIER_INTERVAL = 5
DISCOVER_INTERVAL = 5


@dataclass
class RuntimeConfig:
    """Mutable runtime config — set once in CLI, read everywhere."""
    eval_model: str = "sonnet"
    eval_model_2: str = "haiku"
    improve_model: str = "sonnet"
    model_profile: str = "balanced"
    max_active_criteria: int = 15


# Singleton — import and mutate from cli.py, read from everywhere else
runtime = RuntimeConfig()
