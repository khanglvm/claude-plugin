"""State management — load/save criteria, state, results, stop signals, and score utilities."""

import json
from datetime import datetime
from pathlib import Path

from .config import CRITERIA_DIR, DATA_DIR, CONFIDENCE_WEIGHTS


def load_criteria(skill_name: str, skill_path_override: str = None) -> dict:
    """Load criteria definitions for a skill."""
    path = CRITERIA_DIR / f"{skill_name}.json"
    with open(path) as f:
        config = json.load(f)
    if skill_path_override:
        config["skill_path"] = str(Path(skill_path_override).resolve())
    elif not Path(config["skill_path"]).is_absolute():
        config["skill_path"] = str(Path.cwd() / config["skill_path"])
    return config


def load_state(skill_name: str) -> dict:
    """Load or initialize state for a skill."""
    path = DATA_DIR / f"state-{skill_name}.json"
    if path.exists():
        with open(path) as f:
            state = json.load(f)
        # Migrate: add tracking fields if missing
        for key, default in [("failures", {}), ("parked", []),
                             ("graduated", []), ("high_streak", {})]:
            if key not in state:
                state[key] = default
        return state
    return {"run_number": 0, "scores": {}, "best_total": 0, "failures": {},
            "parked": [], "graduated": [], "high_streak": {}}


def save_state(skill_name: str, state: dict):
    """Persist state atomically — write to temp file, then rename."""
    path = DATA_DIR / f"state-{skill_name}.json"
    tmp = path.with_suffix(".tmp")
    try:
        content = json.dumps(state, indent=2)
        json.loads(content)  # validate before writing
        with open(tmp, "w") as f:
            f.write(content)
        tmp.rename(path)  # atomic on POSIX
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise


def log_result(skill_name: str, result: dict):
    """Append run result to JSONL log."""
    path = DATA_DIR / f"results-{skill_name}.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(result) + "\n")


# --- Stop signal ---

def check_stop_requested(skill_name: str) -> bool:
    """Check if a stop has been requested via stop file."""
    return (DATA_DIR / f"stop-{skill_name}.flag").exists()


def request_stop(skill_name: str):
    """Create stop file to signal the running loop to terminate."""
    stop_file = DATA_DIR / f"stop-{skill_name}.flag"
    stop_file.write_text(datetime.now().isoformat())
    print(f"  Stop requested for '{skill_name}'. Loop will halt after current cycle.")


def clear_stop(skill_name: str):
    """Remove stop file."""
    stop_file = DATA_DIR / f"stop-{skill_name}.flag"
    if stop_file.exists():
        stop_file.unlink()


# --- Score utilities ---

def get_score(val) -> int:
    """Extract raw score from either int or eval result dict."""
    if isinstance(val, dict):
        return val.get("score", 0)
    return val if isinstance(val, int) else 0


def get_confidence(val) -> str:
    """Extract confidence from eval result dict."""
    if isinstance(val, dict):
        return val.get("confidence", "medium")
    return "medium"


def compute_weighted_total(scores: dict, criteria: dict, use_confidence: bool = True) -> float:
    """Compute weighted total score. If use_confidence, applies confidence weighting."""
    total_weight = sum(c["weight"] for c in criteria.values())
    if total_weight == 0:
        return 0
    weighted = 0
    for cid, cdef in criteria.items():
        raw = get_score(scores.get(cid, 0))
        if use_confidence:
            conf = get_confidence(scores.get(cid, 0))
            conf_w = CONFIDENCE_WEIGHTS.get(conf, 0.7)
            weighted += raw * conf_w * cdef["weight"]
        else:
            weighted += raw * cdef["weight"]
    return round(weighted / total_weight * 10, 2)
