"""Main autoresearch loop — run_cycle and run_loop orchestration."""

import subprocess
import time
from datetime import datetime, timedelta

from .config import (
    COLD_TIER_INTERVAL, DISCOVER_INTERVAL, MAX_CONSECUTIVE_FAILS,
    WARM_TIER_INTERVAL, runtime,
)
from .agents import (
    apply_discovered_criteria, discover_criteria, improve_criterion,
    refine_criterion,
)
from .calibration import check_calibration
from .evaluation import (
    evaluate_all, get_modified_files, evaluate_criterion,
    verify_score_jump, ANTIGAMING_JUMP_THRESHOLD,
)
from .lifecycle import (
    pick_weakest_criterion, record_failure, record_success,
    update_graduation,
)
from .state import (
    check_stop_requested, clear_stop, compute_weighted_total,
    get_confidence, get_score, load_criteria, load_state,
    log_result, save_state,
)


def run_cycle(skill_name: str, skill_config: dict, state: dict,
              parallel: int, auto_refine: bool = False) -> dict:
    """Run one improvement cycle: evaluate -> improve weakest -> re-evaluate -> keep/revert."""
    run_num = state["run_number"] + 1
    state["run_number"] = run_num
    log_seq = state.get("log_seq", 0) + 1
    state["log_seq"] = log_seq
    timestamp = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"  Run #{run_num} — {skill_name} — {timestamp}")
    print(f"{'='*60}")

    # Hot-reload criteria from disk
    try:
        fresh_config = load_criteria(skill_name, skill_config.get("_cli_skill_path"))
        skill_config["criteria"] = fresh_config["criteria"]
    except Exception:
        pass

    # Step 1: Evaluate current state
    print(f"\n  [1/6] Evaluating current state...")
    scores = evaluate_all(skill_config, parallel=parallel,
                          previous_scores=state.get("scores"),
                          cycle=run_num, state=state)
    total = compute_weighted_total(scores, skill_config["criteria"])
    raw_total = compute_weighted_total(scores, skill_config["criteria"], use_confidence=False)
    print(f"\n  Weighted score: {total}/10 (raw: {raw_total}/10)")

    update_graduation(state, scores, skill_config["criteria"])

    # Score stability detection
    prev_scores = state.get("scores", {})
    for cid in scores:
        if cid in prev_scores:
            old_s = get_score(prev_scores[cid])
            new_s = get_score(scores[cid])
            last_target = state.get("last_target")
            if cid != last_target and abs(old_s - new_s) >= 3:
                print(f"  [NOISE] {cid} shifted {old_s}→{new_s} untouched — eval instability")

    state["scores"] = scores
    state["best_total"] = total

    # Criteria discovery
    discover_interval = skill_config.get("_discover_interval", DISCOVER_INTERVAL)
    if discover_interval > 0 and run_num % discover_interval == 0:
        print(f"\n  [DISCOVER] Running criteria discovery (every {discover_interval} cycles)...")
        proposals = discover_criteria(skill_config, state)
        if proposals:
            apply_discovered_criteria(skill_config, state, proposals)
            save_state(skill_name, state)
        else:
            print(f"  [DISCOVER] No new criteria proposed")

    # Show lifecycle status
    failures = state.get("failures", {})
    parked = state.get("parked", [])
    graduated = state.get("graduated", [])
    active_cooldowns = [cid for cid, info in failures.items()
                        if info.get("cooldown_until", 0) > run_num and cid not in parked]
    active_count = len([c for c in skill_config["criteria"]
                        if c not in graduated and c not in parked])
    if graduated:
        print(f"  Graduated: {', '.join(graduated)}")
    if parked:
        print(f"  Parked: {', '.join(parked)}")
    if active_cooldowns:
        print(f"  On cooldown: {', '.join(active_cooldowns)}")
    print(f"  Active: {active_count}/{len(skill_config['criteria'])} criteria")

    # Step 2: Pick weakest criterion
    target_cid = pick_weakest_criterion(scores, skill_config["criteria"], state)

    if target_cid is None:
        print(f"\n  All criteria are parked or on cooldown. Nothing to improve.")
        if auto_refine and parked:
            refine_cid = parked[0]
            refine_cdef = skill_config["criteria"].get(refine_cid)
            if refine_cdef:
                refined = refine_criterion(skill_config, refine_cid, refine_cdef, state)
                if refined:
                    save_state(skill_name, state)
                    return {"run": run_num, "timestamp": timestamp, "skill": skill_name,
                            "action": "refined_criteria", "target": refine_cid, "kept": False,
                            "log_seq": log_seq}
        result = {
            "run": run_num, "timestamp": timestamp, "skill": skill_name,
            "action": "all_blocked", "kept": False,
            "total_pre": total, "total_post": total,
            "log_seq": log_seq
        }
        log_result(skill_name, result)
        save_state(skill_name, state)
        return result

    target_cdef = skill_config["criteria"][target_cid]
    current_score = get_score(scores.get(target_cid, 0))
    current_conf = get_confidence(scores.get(target_cid, 0))
    fail_info = failures.get(target_cid, {})
    state["last_target"] = target_cid
    print(f"\n  [2/6] Targeting: {target_cid} ({target_cdef['name']}) — score {current_score}/10 conf={current_conf}"
          f" (fails: {fail_info.get('consecutive', 0)}/{fail_info.get('total', 0)})")

    # Auto-refine check
    if auto_refine and fail_info.get("consecutive", 0) == MAX_CONSECUTIVE_FAILS - 1:
        print(f"  [REFINE] Proactive refinement — next failure would trigger cooldown")
        refine_criterion(skill_config, target_cid, target_cdef, state)
        target_cdef = skill_config["criteria"][target_cid]

    # Step 3: Improve
    skill_path = skill_config["skill_path"]
    print(f"\n  [3/6] Running improvement agent (research + improve)...")
    success = improve_criterion(skill_config, target_cid, target_cdef, current_score, state)

    if not success:
        print(f"  Improvement agent failed. Skipping.")
        record_failure(state, target_cid)
        result = {
            "run": run_num, "timestamp": timestamp, "skill": skill_name,
            "target": target_cid, "pre_score": current_score,
            "post_score": current_score, "total_pre": total, "total_post": total,
            "kept": False, "reason": "agent_failed", "log_seq": log_seq
        }
        log_result(skill_name, result)
        save_state(skill_name, state)
        return result

    # Step 4: Selective re-evaluation
    print(f"\n  [4/6] Selective re-evaluation...")
    modified = get_modified_files(skill_path)
    if modified:
        print(f"    Modified files: {', '.join(modified)}")

    criteria_to_reeval = {target_cid}
    for cid, cdef in skill_config["criteria"].items():
        if cid == target_cid:
            continue
        cid_files = set(cdef.get("target_files", []))
        if cid_files & modified:
            criteria_to_reeval.add(cid)

    if run_num % 5 == 0:
        criteria_to_reeval = set(skill_config["criteria"].keys())
        print(f"    Full re-eval (every 5th cycle)")
    else:
        print(f"    Re-evaluating {len(criteria_to_reeval)}/{len(skill_config['criteria'])} criteria")

    new_scores = dict(scores)
    for cid in criteria_to_reeval:
        cdef = skill_config["criteria"][cid]
        fallback = get_score(scores.get(cid))
        result_dict = evaluate_criterion(skill_config, cid, cdef, fallback_score=fallback)
        new_scores[cid] = result_dict
        if cid == target_cid:
            new_score = get_score(result_dict)

    new_total = compute_weighted_total(new_scores, skill_config["criteria"])

    # Step 5: Anti-gaming verification
    target_improved = new_score > current_score
    if target_improved and (new_score - current_score) >= ANTIGAMING_JUMP_THRESHOLD:
        print(f"\n  [5/6] Anti-gaming verification (jump={new_score - current_score})...")
        verified_score = verify_score_jump(
            skill_config, target_cid, target_cdef, current_score, new_score
        )
        if verified_score < new_score:
            new_scores[target_cid] = {
                "score": verified_score,
                "confidence": get_confidence(new_scores.get(target_cid, 0)),
                "weighted_score": verified_score * 1.0
            }
            new_score = verified_score
            new_total = compute_weighted_total(new_scores, skill_config["criteria"])
            target_improved = new_score > current_score
    else:
        print(f"\n  [5/6] Anti-gaming check skipped (jump={new_score - current_score})")

    # Step 6: Keep/revert decision
    total_regressed = new_total < total

    if target_improved and not total_regressed:
        print(f"\n  IMPROVED: {target_cid} {current_score} → {new_score} (total: {total} → {new_total})")
        state["scores"] = new_scores
        state["best_total"] = new_total
        record_success(state, target_cid)
        kept = True
        commit_msg = f"autoresearch: improve {target_cid} ({target_cdef['name']}) {current_score}->{new_score}"
        subprocess.run(["git", "add", "."], capture_output=True, cwd=skill_path)
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, cwd=skill_path)
        print(f"  Committed: {commit_msg}")
    elif target_improved and total_regressed:
        print(f"\n  REGRESSION: {target_cid} {current_score} → {new_score}, but total {total} → {new_total}. Reverting...")
        for f in modified:
            subprocess.run(["git", "checkout", "HEAD", "--", f], capture_output=True, cwd=skill_path)
        record_failure(state, target_cid)
        kept = False
    else:
        print(f"\n  NO IMPROVEMENT: {target_cid} {current_score} → {new_score}. Reverting...")
        for f in modified:
            subprocess.run(["git", "checkout", "HEAD", "--", f], capture_output=True, cwd=skill_path)
        record_failure(state, target_cid)
        kept = False

    result = {
        "run": run_num, "timestamp": timestamp, "skill": skill_name,
        "target": target_cid, "target_name": target_cdef["name"],
        "pre_score": current_score, "post_score": new_score,
        "pre_confidence": current_conf, "post_confidence": get_confidence(new_scores.get(target_cid, 0)),
        "total_pre": total, "total_post": new_total if kept else total,
        "kept": kept, "all_scores": {k: get_score(v) for k, v in (new_scores if kept else scores).items()},
        "log_seq": log_seq
    }
    log_result(skill_name, result)
    save_state(skill_name, state)
    return result


def run_loop(skill_name: str, hours: float, parallel: int, cycle_minutes: int = 0,
             skill_path: str = None, auto_refine: bool = False, max_loops: int = None,
             discover_interval: int = DISCOVER_INTERVAL):
    """Main autoresearch loop for a single skill."""
    skill_config = load_criteria(skill_name, skill_path)
    skill_config["_cli_skill_path"] = skill_path
    skill_config["_discover_interval"] = discover_interval
    state = load_state(skill_name)
    if hours is not None:
        end_time = datetime.now() + timedelta(hours=hours)
    elif max_loops is None:
        end_time = datetime.now() + timedelta(hours=1.0)
    else:
        end_time = None
    cycle = 0
    all_blocked_streak = 0

    clear_stop(skill_name)

    duration_str = f"{hours}h" if hours else "unlimited"
    loops_str = f"{max_loops} loops" if max_loops else "unlimited"
    graduated = state.get("graduated", [])
    parked = state.get("parked", [])
    active_count = len([c for c in skill_config["criteria"]
                        if c not in graduated and c not in parked])

    print(f"\n{'#'*60}")
    print(f"  AUTORESEARCH: {skill_name}")
    print(f"  Duration: {duration_str} | Max loops: {loops_str} | Parallel evals: {parallel}")
    print(f"  Criteria: {len(skill_config['criteria'])} total | {active_count} active | "
          f"{len(graduated)} graduated | {len(parked)} parked | cap: {runtime.max_active_criteria}")
    print(f"  Auto-refine: {'ON' if auto_refine else 'OFF'}")
    if runtime.model_profile == "auto":
        print(f"  Profile: auto (per-criterion routing: opus/sonnet/haiku based on complexity)")
    else:
        print(f"  Profile: {runtime.model_profile} | Eval: {runtime.eval_model}+{runtime.eval_model_2} | Improve: {runtime.improve_model}")
    print(f"  Tiered eval: hot=every cycle, warm=every {WARM_TIER_INTERVAL}, cold=every {COLD_TIER_INTERVAL}")
    if end_time:
        print(f"  End time: {end_time.strftime('%H:%M:%S')}")
    print(f"{'#'*60}")

    cal_report = check_calibration(skill_config, parallel)
    if cal_report:
        drifted = [cid for cid, r in cal_report.items() if r["drifted"]]
        if drifted:
            print(f"  [CALIBRATE] Drifted criteria: {', '.join(drifted)}")
            print(f"  [CALIBRATE] Proceeding with loop — but eval_prompts for these may be unreliable")

    while True:
        if end_time and datetime.now() >= end_time:
            print(f"\n  [TIME] Duration limit reached. Stopping.")
            break
        if max_loops is not None and cycle >= max_loops:
            print(f"\n  [LIMIT] Reached max loops ({max_loops}). Stopping.")
            break
        if check_stop_requested(skill_name):
            print(f"\n  [CANCELLED] Stop requested. Halting loop.")
            clear_stop(skill_name)
            break

        cycle += 1
        cycle_start = time.time()

        result = run_cycle(skill_name, skill_config, state, parallel, auto_refine)

        elapsed = time.time() - cycle_start

        print(f"\n  Cycle {cycle} complete in {elapsed:.0f}s")
        if end_time:
            remaining = (end_time - datetime.now()).total_seconds()
            print(f"  Time remaining: {remaining/60:.1f} min")
        if max_loops:
            print(f"  Loops remaining: {max_loops - cycle}")
        print(f"  Score: {state.get('best_total', 0)}/10")

        if result.get("action") == "all_blocked":
            all_blocked_streak += 1
            if all_blocked_streak >= 3:
                print(f"\n  [HALT] All criteria blocked for {all_blocked_streak} consecutive cycles.")
                print(f"  Refine criteria manually or re-run with --auto-refine")
                break
        else:
            all_blocked_streak = 0

        wait = max(0, cycle_minutes * 60 - elapsed)
        remaining = (end_time - datetime.now()).total_seconds() if end_time else float('inf')
        if wait > 0 and remaining > wait:
            print(f"  Waiting {wait:.0f}s until next cycle...")
            wait_end = time.time() + wait
            while time.time() < wait_end:
                time.sleep(min(10, max(0.1, wait_end - time.time())))
                if check_stop_requested(skill_name):
                    break

    # Final summary
    clear_stop(skill_name)
    failures = state.get("failures", {})
    parked = state.get("parked", [])
    final_scores = state.get("scores", {})
    print(f"\n{'='*60}")
    print(f"  AUTORESEARCH COMPLETE: {skill_name}")
    print(f"  Total runs: {state['run_number']}")
    print(f"  Final score: {state.get('best_total', 0)}/10")
    print(f"  Scores:")
    for cid in sorted(final_scores.keys()):
        s = get_score(final_scores[cid])
        c = get_confidence(final_scores[cid])
        print(f"    {cid}: {s}/10 (conf={c})")
    conf_counts = {"high": 0, "medium": 0, "low": 0}
    for v in final_scores.values():
        conf_counts[get_confidence(v)] = conf_counts.get(get_confidence(v), 0) + 1
    print(f"  Confidence: high={conf_counts['high']} medium={conf_counts['medium']} low={conf_counts['low']}")
    low_conf = [cid for cid, v in final_scores.items() if get_confidence(v) == "low"]
    if low_conf:
        print(f"  Low-confidence criteria: {', '.join(low_conf)}")
        print(f"  Tip: Rewrite eval_prompts for these to be more deterministic/binary")
    graduated = state.get("graduated", [])
    if graduated:
        print(f"  Graduated criteria: {', '.join(graduated)} (solved — spot-checked only)")
    if parked:
        print(f"  Parked criteria: {', '.join(parked)}")
    stuck = [cid for cid, info in failures.items()
             if info.get("total", 0) >= 3 and cid not in parked]
    if stuck:
        print(f"  Struggling criteria: {', '.join(stuck)}")
        print(f"  Tip: Review eval_prompts in criteria/{skill_name}.json for these")
    active_count = len([c for c in skill_config["criteria"]
                        if c not in graduated and c not in parked])
    print(f"  Active/Graduated/Parked: {active_count}/{len(graduated)}/{len(parked)}")
    print(f"{'='*60}")
