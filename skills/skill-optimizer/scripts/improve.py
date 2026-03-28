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
            state = json.load(f)
        # Migrate: add failures tracking if missing
        if "failures" not in state:
            state["failures"] = {}
        if "parked" not in state:
            state["parked"] = []
        return state
    return {"run_number": 0, "scores": {}, "best_total": 0, "failures": {}, "parked": []}


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


COOLDOWN_CYCLES = 3       # Cycles to skip after consecutive failures
MAX_CONSECUTIVE_FAILS = 3 # Consecutive reverts before cooldown kicks in
PARK_THRESHOLD = 6        # Total failures before parking the criterion


def pick_weakest_criterion(scores: dict, criteria: dict, state: dict) -> str | None:
    """Pick the criterion with lowest score, respecting cooldown and parked status."""
    run_num = state["run_number"]
    failures = state.get("failures", {})
    parked = state.get("parked", [])

    weighted_scores = {}
    for cid, cdef in criteria.items():
        # Skip parked criteria
        if cid in parked:
            continue
        # Skip criteria on cooldown
        fail_info = failures.get(cid, {})
        cooldown_until = fail_info.get("cooldown_until", 0)
        if run_num < cooldown_until:
            continue

        score = scores.get(cid, 0)
        # Lower score + higher weight = higher priority
        priority = (10 - score) * cdef["weight"]
        weighted_scores[cid] = priority

    if not weighted_scores:
        return None
    return max(weighted_scores, key=weighted_scores.get)


def record_failure(state: dict, cid: str):
    """Track a failed improvement attempt. Sets cooldown or parks the criterion."""
    failures = state.setdefault("failures", {})
    info = failures.setdefault(cid, {"consecutive": 0, "total": 0, "cooldown_until": 0})
    info["consecutive"] += 1
    info["total"] += 1

    if info["total"] >= PARK_THRESHOLD:
        parked = state.setdefault("parked", [])
        if cid not in parked:
            parked.append(cid)
            print(f"  [PARKED] {cid} after {info['total']} total failures — skipping until criteria refined")
    elif info["consecutive"] >= MAX_CONSECUTIVE_FAILS:
        info["cooldown_until"] = state["run_number"] + COOLDOWN_CYCLES
        print(f"  [COOLDOWN] {cid} for {COOLDOWN_CYCLES} cycles (consecutive: {info['consecutive']})")


def record_success(state: dict, cid: str):
    """Reset consecutive failure counter on success."""
    failures = state.setdefault("failures", {})
    if cid in failures:
        failures[cid]["consecutive"] = 0


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


def refine_criterion(skill_config: dict, cid: str, criterion: dict, state: dict) -> bool:
    """Auto-refine a stuck criterion's eval_prompt. Returns True if criteria file updated."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]
    fail_info = state.get("failures", {}).get(cid, {})

    print(f"  [REFINE] Auto-refining eval_prompt for {cid} ({criterion['name']})...")

    refine_prompt = f"""You are improving a skill evaluation criterion that is stuck — it keeps scoring low but the improvement agent can't figure out how to fix it. The eval_prompt is likely too vague, unreachable, or poorly calibrated.

CRITERION: {cid} — {criterion['name']}
WEIGHT: {criterion['weight']}
TARGET FILES: {', '.join(criterion.get('target_files', []))}
CURRENT EVAL_PROMPT:
{criterion['eval_prompt']}

FAILURE HISTORY: {fail_info.get('total', 0)} total failures, {fail_info.get('consecutive', 0)} consecutive

SKILL LOCATION: {skill_path}

Read the target files at {skill_path} to understand what the skill actually contains.

Then rewrite the eval_prompt to be:
1. More specific — concrete checklist items, not vague qualities
2. Achievable — scoring criteria the improvement agent can actually address
3. Well-calibrated — current content should score at least 3-4, not 0
4. Actionable — each checklist item maps to a specific edit

Return ONLY a JSON object:
{{"refined_eval_prompt": "<new eval_prompt text>", "reasoning": "<why the old one was stuck>"}}
Nothing else."""

    output = run_claude(refine_prompt, allowed_tools="Read,Grep,Glob", timeout=180)

    # Parse the refined prompt
    try:
        for line in output.split("\n"):
            line = line.strip()
            if "{" in line and "refined_eval_prompt" in line:
                try:
                    data = json.loads(line)
                    new_prompt = data.get("refined_eval_prompt")
                    if new_prompt and len(new_prompt) > 20:
                        # Update criteria file
                        criteria_path = CRITERIA_DIR / f"{skill_name}.json"
                        with open(criteria_path) as f:
                            config = json.load(f)
                        old_prompt = config["criteria"][cid]["eval_prompt"]
                        config["criteria"][cid]["eval_prompt"] = new_prompt
                        with open(criteria_path, "w") as f:
                            json.dump(config, f, indent=2)
                        # Update in-memory config
                        skill_config["criteria"][cid]["eval_prompt"] = new_prompt
                        # Reset failure counters — give it a fresh start
                        state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
                        if cid in state.get("parked", []):
                            state["parked"].remove(cid)
                        reason = data.get("reasoning", "N/A")
                        print(f"  [REFINE] Updated eval_prompt for {cid}")
                        print(f"  [REFINE] Reason: {reason}")
                        print(f"  [REFINE] Old: {old_prompt[:80]}...")
                        print(f"  [REFINE] New: {new_prompt[:80]}...")
                        return True
                except json.JSONDecodeError:
                    pass
        # Try multiline JSON parse
        import re
        match = re.search(r'\{[^{}]*"refined_eval_prompt"\s*:\s*"((?:[^"\\]|\\.)*)?"', output, re.DOTALL)
        if match:
            new_prompt = match.group(1).replace('\\"', '"').replace('\\n', '\n')
            if new_prompt and len(new_prompt) > 20:
                criteria_path = CRITERIA_DIR / f"{skill_name}.json"
                with open(criteria_path) as f:
                    config = json.load(f)
                config["criteria"][cid]["eval_prompt"] = new_prompt
                with open(criteria_path, "w") as f:
                    json.dump(config, f, indent=2)
                skill_config["criteria"][cid]["eval_prompt"] = new_prompt
                state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
                if cid in state.get("parked", []):
                    state["parked"].remove(cid)
                print(f"  [REFINE] Updated eval_prompt for {cid} (fallback parse)")
                return True
    except Exception as e:
        print(f"  [REFINE] Failed to parse refinement output: {e}")

    print(f"  [REFINE] Could not refine {cid} — parking it")
    return False


def run_cycle(skill_name: str, skill_config: dict, state: dict, parallel: int, auto_refine: bool = False) -> dict:
    """Run one improvement cycle: evaluate → improve weakest → re-evaluate → keep/revert."""
    run_num = state["run_number"] + 1
    state["run_number"] = run_num
    timestamp = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"  Run #{run_num} — {skill_name} — {timestamp}")
    print(f"{'='*60}")

    # Hot-reload criteria from disk (allows mid-loop manual edits)
    try:
        fresh_config = load_criteria(skill_name, skill_config.get("_cli_skill_path"))
        skill_config["criteria"] = fresh_config["criteria"]
    except Exception:
        pass  # Keep current criteria if reload fails

    # Step 1: Evaluate current state
    print(f"\n  [1/4] Evaluating current state...")
    scores = evaluate_all(skill_config, parallel=parallel)
    total = compute_weighted_total(scores, skill_config["criteria"])
    print(f"\n  Current weighted score: {total}/10")

    # Show cooldown/parked status
    failures = state.get("failures", {})
    parked = state.get("parked", [])
    active_cooldowns = [cid for cid, info in failures.items()
                        if info.get("cooldown_until", 0) > run_num and cid not in parked]
    if parked:
        print(f"  Parked: {', '.join(parked)}")
    if active_cooldowns:
        print(f"  On cooldown: {', '.join(active_cooldowns)}")

    # Step 2: Pick weakest criterion (respecting cooldown/parked)
    target_cid = pick_weakest_criterion(scores, skill_config["criteria"], state)

    if target_cid is None:
        print(f"\n  All criteria are parked or on cooldown. Nothing to improve.")
        if auto_refine and parked:
            # Try to refine a parked criterion to unblock
            refine_cid = parked[0]
            refine_cdef = skill_config["criteria"].get(refine_cid)
            if refine_cdef:
                refined = refine_criterion(skill_config, refine_cid, refine_cdef, state)
                if refined:
                    save_state(skill_name, state)
                    return {"run": run_num, "timestamp": timestamp, "skill": skill_name,
                            "action": "refined_criteria", "target": refine_cid, "kept": False}
        result = {
            "run": run_num, "timestamp": timestamp, "skill": skill_name,
            "action": "all_blocked", "kept": False,
            "total_pre": total, "total_post": total
        }
        log_result(skill_name, result)
        save_state(skill_name, state)
        return result

    target_cdef = skill_config["criteria"][target_cid]
    current_score = scores.get(target_cid, 0)
    fail_info = failures.get(target_cid, {})
    print(f"\n  [2/4] Targeting: {target_cid} ({target_cdef['name']}) — score {current_score}/10"
          f" (fails: {fail_info.get('consecutive', 0)}/{fail_info.get('total', 0)})")

    # Auto-refine check: if criterion is about to hit cooldown, refine proactively
    if auto_refine and fail_info.get("consecutive", 0) == MAX_CONSECUTIVE_FAILS - 1:
        print(f"  [REFINE] Proactive refinement — next failure would trigger cooldown")
        refine_criterion(skill_config, target_cid, target_cdef, state)
        # Re-read the (possibly updated) criterion
        target_cdef = skill_config["criteria"][target_cid]

    # Step 3: Snapshot files (for revert)
    skill_path = skill_config["skill_path"]

    # Step 4: Improve
    print(f"\n  [3/4] Running improvement agent...")
    success = improve_criterion(skill_config, target_cid, target_cdef, current_score)

    if not success:
        print(f"  Improvement agent failed. Skipping.")
        record_failure(state, target_cid)
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
        record_success(state, target_cid)
    else:
        print(f"\n  NO IMPROVEMENT: {target_cid} {current_score} → {new_score}. Reverting...")
        revert_cmd = f"cd '{skill_path}' && git checkout -- . 2>/dev/null; true"
        subprocess.run(revert_cmd, shell=True, capture_output=True)
        record_failure(state, target_cid)

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


def run_loop(skill_name: str, hours: float, parallel: int, cycle_minutes: int = 10,
             skill_path: str = None, auto_refine: bool = False):
    """Main autoresearch loop for a single skill."""
    skill_config = load_criteria(skill_name, skill_path)
    # Store CLI skill_path for hot-reload
    skill_config["_cli_skill_path"] = skill_path
    state = load_state(skill_name)
    end_time = datetime.now() + timedelta(hours=hours)
    cycle = 0
    all_blocked_streak = 0

    print(f"\n{'#'*60}")
    print(f"  AUTORESEARCH: {skill_name}")
    print(f"  Duration: {hours}h | Parallel evals: {parallel}")
    print(f"  Criteria: {len(skill_config['criteria'])}")
    print(f"  Auto-refine: {'ON' if auto_refine else 'OFF'}")
    print(f"  End time: {end_time.strftime('%H:%M:%S')}")
    print(f"{'#'*60}")

    while datetime.now() < end_time:
        cycle += 1
        cycle_start = time.time()

        result = run_cycle(skill_name, skill_config, state, parallel, auto_refine)

        elapsed = time.time() - cycle_start
        remaining = (end_time - datetime.now()).total_seconds()

        print(f"\n  Cycle {cycle} complete in {elapsed:.0f}s")
        print(f"  Time remaining: {remaining/60:.1f} min")
        print(f"  Score: {state.get('best_total', 0)}/10")

        # Detect all-blocked deadlock
        if result.get("action") == "all_blocked":
            all_blocked_streak += 1
            if all_blocked_streak >= 3:
                print(f"\n  [HALT] All criteria blocked for {all_blocked_streak} consecutive cycles.")
                print(f"  Refine criteria manually or re-run with --auto-refine")
                break
        else:
            all_blocked_streak = 0

        # Wait for cycle interval
        wait = max(0, cycle_minutes * 60 - elapsed)
        if wait > 0 and remaining > wait:
            print(f"  Waiting {wait:.0f}s until next cycle...")
            time.sleep(wait)

    # Final summary
    failures = state.get("failures", {})
    parked = state.get("parked", [])
    print(f"\n{'='*60}")
    print(f"  AUTORESEARCH COMPLETE: {skill_name}")
    print(f"  Total runs: {state['run_number']}")
    print(f"  Final score: {state.get('best_total', 0)}/10")
    print(f"  Scores: {json.dumps(state.get('scores', {}), indent=2)}")
    if parked:
        print(f"  Parked criteria: {', '.join(parked)}")
    stuck = [cid for cid, info in failures.items()
             if info.get("total", 0) >= 3 and cid not in parked]
    if stuck:
        print(f"  Struggling criteria: {', '.join(stuck)}")
        print(f"  Tip: Review eval_prompts in criteria/{skill_name}.json for these")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Skill Autoresearch Loop")
    parser.add_argument("--skill", required=True, help="Skill name (matches criteria/<name>.json)")
    parser.add_argument("--skill-path", default=None, help="Path to skill folder (overrides criteria JSON path)")
    parser.add_argument("--hours", type=float, default=1.0, help="Duration in hours")
    parser.add_argument("--parallel", type=int, default=2, help="Max parallel eval agents")
    parser.add_argument("--cycle-minutes", type=int, default=8, help="Minutes per cycle")
    parser.add_argument("--auto-refine", action="store_true",
                        help="Auto-refine stuck eval_prompts instead of just parking them")
    parser.add_argument("--unpark", nargs="*", metavar="CID",
                        help="Unpark specific criteria (or all if no IDs given)")
    args = parser.parse_args()

    # Handle --unpark before running
    if args.unpark is not None:
        state = load_state(args.skill)
        if not args.unpark:  # --unpark with no args = unpark all
            unparked = state.get("parked", [])
            state["parked"] = []
            for cid in unparked:
                if cid in state.get("failures", {}):
                    state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
            print(f"  Unparked all: {', '.join(unparked) if unparked else '(none were parked)'}")
        else:
            for cid in args.unpark:
                if cid in state.get("parked", []):
                    state["parked"].remove(cid)
                if cid in state.get("failures", {}):
                    state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
                print(f"  Unparked: {cid}")
        save_state(args.skill, state)

    run_loop(args.skill, args.hours, args.parallel, args.cycle_minutes, args.skill_path, args.auto_refine)


if __name__ == "__main__":
    main()
