#!/usr/bin/env python3 -u
"""
Skill Improver — Autoresearch Loop for Claude Code Skills
Karpathy-pattern: improve → evaluate → keep/revert → repeat

Usage:
    python3 improve.py --skill design-prompt --hours 1 --parallel 2
    python3 improve.py --skill proposal --hours 1 --parallel 2
    python3 improve.py --skill all --hours 2 --parallel 4
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent  # skill-optimizer/
DATA_DIR = SKILL_DIR / "data"
CRITERIA_DIR = SKILL_DIR / "criteria"
CLAUDE_BIN = "claude"
IMPROVE_MODEL = "sonnet"  # claude CLI model flag

# Ensure data dir exists
DATA_DIR.mkdir(exist_ok=True)


def load_criteria(skill_name: str, skill_path_override: str = None) -> dict:
    """Load criteria definitions for a skill."""
    path = CRITERIA_DIR / f"{skill_name}.json"
    with open(path) as f:
        config = json.load(f)
    # Override skill_path if provided via CLI
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
            return json.load(f)
    return {"run_number": 0, "scores": {}, "best_total": 0}


def save_state(skill_name: str, state: dict):
    """Persist state."""
    path = DATA_DIR / f"state-{skill_name}.json"
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def log_result(skill_name: str, result: dict):
    """Append run result to JSONL log."""
    path = DATA_DIR / f"results-{skill_name}.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(result) + "\n")


def run_claude(prompt: str, allowed_tools: str = "Read,Grep,Glob", timeout: int = 300) -> str:
    """Run claude CLI in non-interactive mode."""
    cmd = [
        CLAUDE_BIN, "-p", prompt,
        "--allowedTools", allowed_tools,
        "--dangerously-skip-permissions",
        "--model", IMPROVE_MODEL
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(Path.home())
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR: {e}]"


def evaluate_criterion(skill_config: dict, criterion_id: str, criterion: dict) -> int:
    """Evaluate a single criterion via claude CLI. Returns score 0-10."""
    import re
    skill_path = skill_config["skill_path"]
    eval_prompt = criterion["eval_prompt"].replace("{skill_path}", skill_path)
    target_files = " ".join(criterion.get("target_files", []))

    prompt = f"""You are a skill quality evaluator. Score this criterion precisely.

{eval_prompt}

Read the relevant files at {skill_path} ({target_files}) to evaluate.

Return ONLY a JSON object: {{"score": <0-10>, "reasoning": "<1-2 sentences>"}}
Nothing else."""

    output = run_claude(prompt, allowed_tools="Read,Grep,Glob", timeout=120)

    # Parse score from output
    try:
        for line in output.split("\n"):
            line = line.strip()
            if "{" in line and "score" in line:
                try:
                    data = json.loads(line)
                    return min(10, max(0, int(data.get("score", 0))))
                except json.JSONDecodeError:
                    pass
        numbers = re.findall(r'"score"\s*:\s*(\d+)', output)
        if numbers:
            return min(10, max(0, int(numbers[0])))
    except Exception:
        pass

    print(f"    [WARN] Could not parse score for {criterion_id}")
    return 0


def evaluate_all(skill_config: dict, parallel: int = 2) -> dict:
    """Evaluate all criteria for a skill. Returns {criterion_id: score}."""
    criteria = skill_config["criteria"]
    scores = {}

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {}
        for cid, cdef in criteria.items():
            future = executor.submit(evaluate_criterion, skill_config, cid, cdef)
            futures[future] = cid

        for future in as_completed(futures):
            cid = futures[future]
            try:
                score = future.result()
                scores[cid] = score
                print(f"    {cid} ({criteria[cid]['name']}): {score}/10")
            except Exception as e:
                scores[cid] = 0
                print(f"    {cid}: ERROR - {e}")

    return scores


def compute_weighted_total(scores: dict, criteria: dict) -> float:
    """Compute weighted total score."""
    total_weight = sum(c["weight"] for c in criteria.values())
    weighted = sum(scores.get(cid, 0) * cdef["weight"] for cid, cdef in criteria.items())
    return round(weighted / total_weight * 10, 2) if total_weight > 0 else 0


def pick_weakest_criterion(scores: dict, criteria: dict) -> str:
    """Pick the criterion with lowest score (weighted by importance)."""
    weighted_scores = {}
    for cid, cdef in criteria.items():
        score = scores.get(cid, 0)
        # Lower score + higher weight = higher priority
        priority = (10 - score) * cdef["weight"]
        weighted_scores[cid] = priority

    return max(weighted_scores, key=weighted_scores.get)


def improve_criterion(skill_config: dict, criterion_id: str, criterion: dict, current_score: int) -> bool:
    """Run an improvement agent for a specific criterion. Returns True if files changed."""
    skill_path = skill_config["skill_path"]
    skill_name = skill_config["skill_name"]
    target_files = ", ".join(criterion.get("target_files", []))

    improve_prompt = f"""You are improving the '{skill_name}' Claude Code skill.

TARGET: Improve criterion "{criterion['name']}" (current score: {current_score}/10)

SKILL LOCATION: {skill_path}
TARGET FILES: {target_files}

EVALUATION CRITERIA:
{criterion['eval_prompt'].replace('{skill_path}', skill_path)}

INSTRUCTIONS:
1. Read the target files listed above
2. Identify specific weaknesses based on the evaluation criteria
3. Make targeted edits to improve the score
4. Focus on the specific criterion — don't restructure everything
5. Keep changes minimal and focused
6. Preserve existing content quality while adding what's missing

RULES:
- Edit existing files, don't create new ones (unless the target file doesn't exist yet)
- Keep files under 300 lines each
- Don't remove existing good content
- Add specific, concrete improvements (CSS values, examples, checklists)
- If a file doesn't exist, create it with comprehensive content

Report what you changed at the end."""

    output = run_claude(
        improve_prompt,
        allowed_tools="Read,Write,Edit,Grep,Glob",
        timeout=300
    )

    return "[ERROR" not in output and "[TIMEOUT]" not in output


def run_cycle(skill_name: str, skill_config: dict, state: dict, parallel: int) -> dict:
    """Run one improvement cycle: evaluate → improve weakest → re-evaluate → keep/revert."""
    run_num = state["run_number"] + 1
    state["run_number"] = run_num
    timestamp = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"  Run #{run_num} — {skill_name} — {timestamp}")
    print(f"{'='*60}")

    # Step 1: Evaluate current state
    print(f"\n  [1/4] Evaluating current state...")
    scores = evaluate_all(skill_config, parallel=parallel)
    total = compute_weighted_total(scores, skill_config["criteria"])
    print(f"\n  Current weighted score: {total}/10")

    # Step 2: Pick weakest criterion
    target_cid = pick_weakest_criterion(scores, skill_config["criteria"])
    target_cdef = skill_config["criteria"][target_cid]
    current_score = scores.get(target_cid, 0)
    print(f"\n  [2/4] Targeting: {target_cid} ({target_cdef['name']}) — score {current_score}/10")

    # Step 3: Snapshot files (for revert)
    skill_path = skill_config["skill_path"]

    # Step 4: Improve
    print(f"\n  [3/4] Running improvement agent...")
    success = improve_criterion(skill_config, target_cid, target_cdef, current_score)

    if not success:
        print(f"  Improvement agent failed. Skipping.")
        result = {
            "run": run_num, "timestamp": timestamp, "skill": skill_name,
            "target": target_cid, "pre_score": current_score,
            "post_score": current_score, "total_pre": total, "total_post": total,
            "kept": False, "reason": "agent_failed"
        }
        log_result(skill_name, result)
        save_state(skill_name, state)
        return result

    # Step 5: Re-evaluate the improved criterion
    print(f"\n  [4/4] Re-evaluating {target_cid}...")
    new_score = evaluate_criterion(skill_config, target_cid, target_cdef)
    new_scores = {**scores, target_cid: new_score}
    new_total = compute_weighted_total(new_scores, skill_config["criteria"])

    improved = new_score > current_score
    kept = improved

    if improved:
        print(f"\n  IMPROVED: {target_cid} {current_score} → {new_score} (total: {total} → {new_total})")
        state["scores"] = new_scores
        state["best_total"] = new_total
    else:
        print(f"\n  NO IMPROVEMENT: {target_cid} {current_score} → {new_score}. Reverting...")
        # Revert changes
        revert_cmd = f"cd '{skill_path}' && git checkout -- . 2>/dev/null; true"
        subprocess.run(revert_cmd, shell=True, capture_output=True)

    result = {
        "run": run_num, "timestamp": timestamp, "skill": skill_name,
        "target": target_cid, "target_name": target_cdef["name"],
        "pre_score": current_score, "post_score": new_score,
        "total_pre": total, "total_post": new_total if improved else total,
        "kept": kept, "all_scores": new_scores if improved else scores
    }
    log_result(skill_name, result)
    save_state(skill_name, state)
    return result


def run_loop(skill_name: str, hours: float, parallel: int, cycle_minutes: int = 10, skill_path: str = None):
    """Main autoresearch loop for a single skill."""
    skill_config = load_criteria(skill_name, skill_path)
    state = load_state(skill_name)
    end_time = datetime.now() + timedelta(hours=hours)
    cycle = 0

    print(f"\n{'#'*60}")
    print(f"  AUTORESEARCH: {skill_name}")
    print(f"  Duration: {hours}h | Parallel evals: {parallel}")
    print(f"  Criteria: {len(skill_config['criteria'])}")
    print(f"  End time: {end_time.strftime('%H:%M:%S')}")
    print(f"{'#'*60}")

    while datetime.now() < end_time:
        cycle += 1
        cycle_start = time.time()

        result = run_cycle(skill_name, skill_config, state, parallel)

        elapsed = time.time() - cycle_start
        remaining = (end_time - datetime.now()).total_seconds()

        print(f"\n  Cycle {cycle} complete in {elapsed:.0f}s")
        print(f"  Time remaining: {remaining/60:.1f} min")
        print(f"  Score: {state.get('best_total', 0)}/10")

        # Wait for cycle interval
        wait = max(0, cycle_minutes * 60 - elapsed)
        if wait > 0 and remaining > wait:
            print(f"  Waiting {wait:.0f}s until next cycle...")
            time.sleep(wait)

    print(f"\n{'='*60}")
    print(f"  AUTORESEARCH COMPLETE: {skill_name}")
    print(f"  Total runs: {state['run_number']}")
    print(f"  Final score: {state.get('best_total', 0)}/10")
    print(f"  Scores: {json.dumps(state.get('scores', {}), indent=2)}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Skill Autoresearch Loop")
    parser.add_argument("--skill", required=True, help="Skill name (matches criteria/<name>.json)")
    parser.add_argument("--skill-path", default=None, help="Path to skill folder (overrides criteria JSON path)")
    parser.add_argument("--hours", type=float, default=1.0, help="Duration in hours")
    parser.add_argument("--parallel", type=int, default=2, help="Max parallel eval agents")
    parser.add_argument("--cycle-minutes", type=int, default=8, help="Minutes per cycle")
    args = parser.parse_args()

    run_loop(args.skill, args.hours, args.parallel, args.cycle_minutes, args.skill_path)


if __name__ == "__main__":
    main()
