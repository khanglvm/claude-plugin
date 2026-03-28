"""Model routing — auto-select models based on criterion complexity."""

import os
import subprocess

from .config import (
    AUTO_ROUTE_HAIKU_THRESHOLD, AUTO_ROUTE_OPUS_THRESHOLD,
    runtime,
)


def auto_route_model(skill_path: str, criterion: dict, role: str = "eval") -> str:
    """Auto-select model based on criterion complexity signals.
    role: 'eval' (primary), 'eval_2' (secondary), 'improve' (edit agent)."""
    target_files = criterion.get("target_files", [])
    checklist = criterion.get("checklist", [])
    weight = criterion.get("weight", 5)

    total_lines = 0
    for tf in target_files:
        fpath = os.path.join(skill_path, tf)
        if os.path.exists(fpath):
            try:
                result = subprocess.run(["wc", "-l", fpath], capture_output=True, text=True)
                total_lines += int(result.stdout.strip().split()[0])
            except (ValueError, IndexError):
                pass

    complexity = total_lines
    if len(checklist) >= 6:
        complexity += 200
    if len(target_files) >= 3:
        complexity += 200
    if weight >= 9:
        complexity += 200

    if complexity >= AUTO_ROUTE_OPUS_THRESHOLD:
        tier = {"eval": "opus", "eval_2": "sonnet", "improve": "opus"}
    elif complexity <= AUTO_ROUTE_HAIKU_THRESHOLD:
        tier = {"eval": "haiku", "eval_2": "haiku", "improve": "sonnet"}
    else:
        tier = {"eval": "sonnet", "eval_2": "haiku", "improve": "sonnet"}

    return tier.get(role, "sonnet")


def resolve_eval_models(skill_path: str, criterion: dict) -> tuple[str, str]:
    """Resolve primary and secondary eval models based on profile."""
    if runtime.model_profile == "auto":
        return (auto_route_model(skill_path, criterion, "eval"),
                auto_route_model(skill_path, criterion, "eval_2"))
    return runtime.eval_model, runtime.eval_model_2


def resolve_improve_model(skill_path: str, criterion: dict) -> str:
    """Resolve improve model based on profile."""
    if runtime.model_profile == "auto":
        return auto_route_model(skill_path, criterion, "improve")
    return runtime.improve_model
