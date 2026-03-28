"""Ground truth calibration — gold standard creation and drift detection."""

import json
from datetime import datetime

from .config import CALIBRATION_DIR, DATA_DIR
from .evaluation import evaluate_criterion
from .state import get_confidence, get_score


def load_calibration(skill_name: str) -> dict | None:
    """Load gold standard scores for a skill."""
    path = CALIBRATION_DIR / f"{skill_name}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def save_calibration(skill_name: str, gold: dict):
    """Write gold standard scores to calibration file."""
    path = CALIBRATION_DIR / f"{skill_name}.json"
    with open(path, "w") as f:
        json.dump(gold, f, indent=2)
    print(f"  [CALIBRATE] Saved gold standard to {path}")


def check_calibration(skill_config: dict, parallel: int = 2) -> dict:
    """Run calibration check: evaluate gold criteria and compare to expected scores."""
    skill_name = skill_config["skill_name"]
    gold = load_calibration(skill_name)
    if not gold:
        return {}

    print(f"\n  [CALIBRATE] Checking eval calibration against {len(gold)} gold standards...")
    criteria = skill_config["criteria"]
    report = {}

    for cid, expected_score in gold.items():
        if cid not in criteria:
            print(f"    [CALIBRATE] {cid}: criterion no longer exists, skipping")
            continue
        result = evaluate_criterion(skill_config, cid, criteria[cid])
        actual = get_score(result)
        drift = abs(actual - expected_score)
        drifted = drift >= 3

        status = "DRIFT" if drifted else "OK"
        print(f"    [{status}] {cid}: expected={expected_score} actual={actual} (drift={drift})")
        report[cid] = {
            "expected": expected_score,
            "actual": actual,
            "drift": drift,
            "drifted": drifted,
            "confidence": get_confidence(result)
        }

    drifted_count = sum(1 for r in report.values() if r["drifted"])
    if drifted_count > 0:
        print(f"\n  [CALIBRATE] WARNING: {drifted_count}/{len(report)} criteria drifted 3+ points")
        print(f"  [CALIBRATE] Eval prompts may need recalibration, or gold standards need updating")
    else:
        print(f"\n  [CALIBRATE] All {len(report)} gold standards within tolerance")

    report_path = DATA_DIR / f"calibration-report-{skill_name}.json"
    with open(report_path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "report": report}, f, indent=2)

    return report


def create_calibration_from_current(skill_config: dict, state: dict):
    """Snapshot current scores as gold standard. Only includes high-confidence scores."""
    skill_name = skill_config["skill_name"]
    scores = state.get("scores", {})
    gold = {}
    for cid, val in scores.items():
        conf = get_confidence(val)
        if conf == "high":
            gold[cid] = get_score(val)

    if not gold:
        for cid, val in scores.items():
            if get_confidence(val) in ("high", "medium"):
                gold[cid] = get_score(val)

    if gold:
        save_calibration(skill_name, gold)
        print(f"  [CALIBRATE] Created gold standard with {len(gold)} criteria")
    else:
        print(f"  [CALIBRATE] No scores available to create gold standard. Run a baseline eval first.")
