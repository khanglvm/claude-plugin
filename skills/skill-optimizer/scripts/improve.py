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
EVAL_MODEL = "sonnet"       # primary eval model
EVAL_MODEL_2 = "haiku"      # secondary eval model (cross-model cancels self-enhancement bias)
IMPROVE_MODEL = "sonnet"    # model for improvement edits
MODEL_PROFILE = "balanced"  # quality | balanced | budget | auto

# Model profiles: presets for eval/improve model selection
# quality  = opus+sonnet  (best accuracy, highest cost, opus 1M context for large files)
# balanced = sonnet+haiku (good accuracy, moderate cost — default)
# budget   = haiku+haiku  (fastest, cheapest, lower accuracy)
# auto     = pick per-criterion based on complexity signals
MODEL_PROFILES = {
    "quality":  {"eval": "opus",   "eval_2": "sonnet", "improve": "opus"},
    "balanced": {"eval": "sonnet", "eval_2": "haiku",  "improve": "sonnet"},
    "budget":   {"eval": "haiku",  "eval_2": "haiku",  "improve": "haiku"},
}

# Auto-routing thresholds: criterion signals → model tier
# Complexity signals checked: target file total lines, checklist item count,
# number of target files, weight
AUTO_ROUTE_OPUS_THRESHOLD = 800     # total target file lines above this → opus
AUTO_ROUTE_HAIKU_THRESHOLD = 200    # total target file lines below this → haiku

# Ensure data dirs exist
DATA_DIR.mkdir(exist_ok=True)
CALIBRATION_DIR = SKILL_DIR / "calibration"
CALIBRATION_DIR.mkdir(exist_ok=True)


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
        # Migrate: add tracking fields if missing
        if "failures" not in state:
            state["failures"] = {}
        if "parked" not in state:
            state["parked"] = []
        if "graduated" not in state:
            state["graduated"] = []
        if "high_streak" not in state:
            state["high_streak"] = {}  # {cid: consecutive_cycles_at_9_10}
        return state
    return {"run_number": 0, "scores": {}, "best_total": 0, "failures": {},
            "parked": [], "graduated": [], "high_streak": {}}


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


def run_claude(prompt: str, allowed_tools: str = "Read,Grep,Glob", timeout: int = 300,
               model: str = None, max_turns: int = None, cwd: str = None) -> str:
    """Run claude CLI in non-interactive mode."""
    if model is None:
        model = IMPROVE_MODEL
    if cwd is None:
        cwd = str(Path.cwd())
    cmd = [
        CLAUDE_BIN, "-p", prompt,
        "--allowedTools", allowed_tools,
        "--dangerously-skip-permissions",
        "--model", model
    ]
    if max_turns is not None:
        cmd += ["--max-turns", str(max_turns)]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )
        if result.returncode != 0 and result.stderr:
            print(f"    [WARN] claude stderr: {result.stderr[:200]}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR: {e}]"


def auto_route_model(skill_path: str, criterion: dict, role: str = "eval") -> str:
    """Auto-select model based on criterion complexity signals.
    role: 'eval' (primary eval), 'eval_2' (secondary eval), 'improve' (edit agent).
    Complexity signals: total target file lines, checklist items, weight, file count.
    Higher complexity → stronger model (opus has 1M context for large inputs)."""
    target_files = criterion.get("target_files", [])
    checklist = criterion.get("checklist", [])
    weight = criterion.get("weight", 5)

    # Compute total lines across target files
    total_lines = 0
    for tf in target_files:
        fpath = os.path.join(skill_path, tf)
        if os.path.exists(fpath):
            try:
                result = subprocess.run(["wc", "-l", fpath], capture_output=True, text=True)
                total_lines += int(result.stdout.strip().split()[0])
            except (ValueError, IndexError):
                pass

    # Complexity score: weighted combination of signals
    complexity = total_lines
    if len(checklist) >= 6:
        complexity += 200  # many checklist items = harder to evaluate accurately
    if len(target_files) >= 3:
        complexity += 200  # cross-file evaluation = harder
    if weight >= 9:
        complexity += 200  # high-weight = want higher accuracy

    if complexity >= AUTO_ROUTE_OPUS_THRESHOLD:
        tier = {"eval": "opus", "eval_2": "sonnet", "improve": "opus"}
    elif complexity <= AUTO_ROUTE_HAIKU_THRESHOLD:
        tier = {"eval": "haiku", "eval_2": "haiku", "improve": "sonnet"}
    else:
        tier = {"eval": "sonnet", "eval_2": "haiku", "improve": "sonnet"}

    model = tier.get(role, "sonnet")
    return model


def resolve_eval_models(skill_path: str, criterion: dict) -> tuple[str, str]:
    """Resolve primary and secondary eval models based on profile.
    Returns (primary_model, secondary_model)."""
    if MODEL_PROFILE == "auto":
        return (auto_route_model(skill_path, criterion, "eval"),
                auto_route_model(skill_path, criterion, "eval_2"))
    return EVAL_MODEL, EVAL_MODEL_2


def resolve_improve_model(skill_path: str, criterion: dict) -> str:
    """Resolve improve model based on profile."""
    if MODEL_PROFILE == "auto":
        return auto_route_model(skill_path, criterion, "improve")
    return IMPROVE_MODEL


def get_modified_files(skill_path: str) -> set:
    """Get files modified in working tree relative to HEAD."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--relative", "HEAD", "--", "."],
        capture_output=True, text=True, cwd=skill_path
    )
    if result.stdout.strip():
        return {f.strip() for f in result.stdout.strip().split("\n") if f.strip()}
    return set()


def precompute_file_facts(skill_path: str, target_files: list[str]) -> str:
    """Run deterministic bash checks to pre-compute facts eval agents need.
    Prevents LLM arithmetic errors on line counts, pattern matches, etc."""
    facts = []
    for tf in target_files:
        fpath = os.path.join(skill_path, tf)
        if not os.path.exists(fpath):
            facts.append(f"- {tf}: FILE DOES NOT EXIST")
            continue
        # Line count
        result = subprocess.run(["wc", "-l", fpath], capture_output=True, text=True)
        line_count = result.stdout.strip().split()[0] if result.stdout.strip() else "?"
        # Section/heading count
        result = subprocess.run(["grep", "-c", "^#", fpath], capture_output=True, text=True)
        heading_count = result.stdout.strip() or "0"
        # Code block count
        result = subprocess.run(["grep", "-c", "^```", fpath], capture_output=True, text=True)
        code_blocks = int(result.stdout.strip() or "0") // 2
        facts.append(f"- {tf}: {line_count} lines, {heading_count} headings, {code_blocks} code blocks")
    return "\n".join(facts) if facts else "No target files found"


# Conservative weights: low (0.4) is at most 0.5x of high (1.0).
# Cross-model disagreement of 3+ points forces confidence to "low" regardless of individual model self-reports.
# Binary checklist criteria are always assigned "high" confidence — no self-report needed.
CONFIDENCE_WEIGHTS = {"high": 1.0, "medium": 0.7, "low": 0.4}

# Anti-gaming: score jump threshold that triggers verification
ANTIGAMING_JUMP_THRESHOLD = 5


def evaluate_binary_checklist(skill_config: dict, criterion_id: str, criterion: dict) -> dict:
    """Evaluate criterion using deterministic binary PASS/FAIL per checklist item.
    Score = sum of passed item points, capped at 10. High confidence by design.
    Used when criterion has a 'checklist' field — opt-in per criterion."""
    import re
    skill_path = skill_config["skill_path"]
    checklist = criterion["checklist"]  # list of {"item": str, "points": int}
    target_files = criterion.get("target_files", [])
    file_facts = precompute_file_facts(skill_path, target_files)
    max_points = sum(c["points"] for c in checklist)

    items_text = "\n".join(
        f"  {i+1}. [{c['points']}pt] {c['item']}" for i, c in enumerate(checklist)
    )

    prompt = f"""CRITERION: {criterion_id} — {criterion['name']}

## Checklist Items (scoring rubric — PASS or FAIL each one):
{items_text}

---
You are a binary quality auditor. Read the target files, then judge each item above.
TARGET: {skill_path} (files: {' '.join(target_files)})

## Pre-Computed File Facts (verified via bash — trust these numbers):
{file_facts}

---

## Evaluation Rules:
- Read ALL target files FIRST. Then evaluate each item above.
- PASS = the item is clearly, demonstrably present with substance.
- FAIL = absent, superficial, or only partially present.
- No partial credit. Each item is binary.
- Do NOT invent evidence. If you can't find it, it's FAIL.

Return ONLY this JSON array (one entry per item, same order):
[{{"item": 1, "verdict": "PASS|FAIL", "evidence": "<brief>"}}]"""

    m1, _ = resolve_eval_models(skill_path, criterion)
    if MODEL_PROFILE == "auto":
        print(f"    [{criterion_id}] auto-routed → {m1}")
    output = run_claude(prompt, allowed_tools="Read", timeout=180,
                        model=m1, max_turns=5)

    # Parse binary verdicts
    passed_points = 0
    verdicts = []
    array_match = re.search(r'\[.*\]', output, re.DOTALL)
    if array_match:
        try:
            items = json.loads(array_match.group())
            for i, item_result in enumerate(items):
                if i < len(checklist):
                    verdict = str(item_result.get("verdict", "FAIL")).upper()
                    if verdict == "PASS":
                        passed_points += checklist[i]["points"]
                    verdicts.append(f"{i+1}:{verdict}")
        except json.JSONDecodeError:
            pass

    if not verdicts:
        # Parse failed — try regex fallback
        for i, c in enumerate(checklist):
            pattern = rf'(?:item.*?{i+1}|{i+1}\.).*?(PASS|FAIL)'
            match = re.search(pattern, output, re.IGNORECASE)
            if match and match.group(1).upper() == "PASS":
                passed_points += c["points"]
                verdicts.append(f"{i+1}:PASS")
            else:
                verdicts.append(f"{i+1}:FAIL")

    score = min(10, round(passed_points / max_points * 10)) if max_points > 0 else 0
    print(f"    [{criterion_id}] binary: {' '.join(verdicts)} → {score}/10 ({passed_points}/{max_points}pts)")
    return {"score": score, "confidence": "high", "weighted_score": score * 1.0}


def evaluate_criterion(skill_config: dict, criterion_id: str, criterion: dict,
                       fallback_score: int | None = None) -> dict:
    """Evaluate a single criterion via claude CLI.
    Returns dict: {"score": 0-10, "confidence": "high|medium|low", "weighted_score": float}.
    If criterion has 'checklist' field, uses binary PASS/FAIL mode (more deterministic).
    On parse failure or timeout, returns fallback_score instead of 0."""
    import re

    # Binary checklist mode — opt-in per criterion
    if "checklist" in criterion:
        return evaluate_binary_checklist(skill_config, criterion_id, criterion)

    skill_path = skill_config["skill_path"]
    eval_prompt = criterion["eval_prompt"].replace("{skill_path}", skill_path)
    target_files = criterion.get("target_files", [])
    target_files_str = " ".join(target_files)

    # Pre-compute deterministic facts so the LLM doesn't need to count
    file_facts = precompute_file_facts(skill_path, target_files)

    prompt = f"""You are a rigorous skill quality auditor. Score using EVIDENCE-BASED methodology.

CRITERION: {criterion_id} — {criterion['name']}

EVALUATION INSTRUCTIONS:
{eval_prompt}

TARGET: {skill_path} (files: {target_files_str})

## Pre-Computed File Facts (verified via bash — trust these numbers):
{file_facts}

## Mandatory Scoring Protocol

**Step 1 — Deep Read**: Read EVERY target file completely. Do not skim or assume content exists.

**Step 2 — Evidence Collection**: For EACH checklist item in the evaluation instructions:
- Search for specific text, code, or structure that satisfies it
- If not found after thorough search, mark as UNMET

**Step 3 — Cross-Validation**: Re-examine your evidence:
- Does it ACTUALLY satisfy the criterion, or is it superficially related?
- Are you giving credit for intention rather than implementation?

**Step 4 — Counter-Evidence**: Actively look for things that LOWER the score.

**Step 5 — Score Assignment** (DEFAULT IS 0 — earn every point):
- 0-2: Missing or fundamentally broken
- 3-4: Present but superficial, major gaps
- 5-6: Functional with notable gaps
- 7-8: Strong with minor gaps only
- 9-10: ALL checklist items verified with evidence (rare)

RULES:
- Absent evidence = 0 for that item. No benefit of the doubt.
- When uncertain, score LOWER.
- Score 8+ requires ALL major checklist items verified.
- Use the pre-computed file facts above for line counts and structure — do NOT estimate.

## Confidence Level
Rate your OWN confidence in the accuracy of this score:
- **high**: All checklist items were clearly verifiable (present or absent). No ambiguity.
- **medium**: Some items were ambiguous or required interpretation.
- **low**: Major uncertainty — file contents were unexpected, criteria was vague, or you're guessing.

Return ONLY this JSON:
{{"score": <0-10>, "confidence": "<high|medium|low>", "evidence": ["<item: evidence or UNMET>"], "counter_evidence": ["<issue>"], "reasoning": "<2-3 sentences>"}}"""

    def _parse_result(output: str) -> dict | None:
        """Parse score + confidence from claude output."""
        # Try line-by-line JSON parse
        for line in output.split("\n"):
            line = line.strip()
            if "{" in line and "score" in line:
                try:
                    data = json.loads(line)
                    score = min(10, max(0, int(data.get("score", 0))))
                    confidence = data.get("confidence", "medium")
                    if confidence not in CONFIDENCE_WEIGHTS:
                        confidence = "medium"
                    if "evidence" in data:
                        print(f"    [{criterion_id}] evidence={len(data.get('evidence', []))} conf={confidence}")
                    return {"score": score, "confidence": confidence}
                except json.JSONDecodeError:
                    pass
        # Try extracting outermost JSON block containing "score" (multi-line)
        json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', output, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                score = min(10, max(0, int(data.get("score", 0))))
                confidence = data.get("confidence", "medium")
                if confidence not in CONFIDENCE_WEIGHTS:
                    confidence = "medium"
                return {"score": score, "confidence": confidence}
            except (json.JSONDecodeError, ValueError):
                pass
        # Regex fallback for "score": N
        numbers = re.findall(r'"score"\s*:\s*(\d+)', output)
        if numbers:
            return {"score": min(10, max(0, int(numbers[0]))), "confidence": "low"}
        return None

    # Cross-model dual-sample: different models cancel self-enhancement bias
    # Model capability weights for consensus (higher = more trusted)
    MODEL_CAPABILITY = {"opus": 1.0, "sonnet": 0.85, "haiku": 0.65}
    m1, m2 = resolve_eval_models(skill_path, criterion)

    if MODEL_PROFILE == "auto":
        print(f"    [{criterion_id}] auto-routed → {m1}+{m2}")
    output1 = run_claude(prompt, allowed_tools="Read", timeout=180,
                         model=m1, max_turns=5)
    output2 = run_claude(prompt, allowed_tools="Read", timeout=180,
                         model=m2, max_turns=5)

    r1 = _parse_result(output1)
    r2 = _parse_result(output2)

    if r1 is not None and r2 is not None:
        disagreement = abs(r1["score"] - r2["score"])
        w1 = MODEL_CAPABILITY.get(m1, 0.7)
        w2 = MODEL_CAPABILITY.get(m2, 0.7)

        if disagreement >= 3:
            # High disagreement — weighted average by model capability, confidence low
            score = round((r1["score"] * w1 + r2["score"] * w2) / (w1 + w2))
            confidence = "low"
            print(f"    [{criterion_id}] CROSS-MODEL DISAGREE: {m1}={r1['score']} vs {m2}={r2['score']} → weighted={score} conf=low")
        else:
            # Agreement zone — conservative min, best confidence
            score = min(r1["score"], r2["score"])
            c1w = CONFIDENCE_WEIGHTS.get(r1["confidence"], 0.7)
            c2w = CONFIDENCE_WEIGHTS.get(r2["confidence"], 0.7)
            confidence = r1["confidence"] if c1w <= c2w else r2["confidence"]
    elif r1 is not None:
        score, confidence = r1["score"], r1["confidence"]
    elif r2 is not None:
        score, confidence = r2["score"], r2["confidence"]
    else:
        if fallback_score is not None:
            print(f"    [WARN] Could not parse score for {criterion_id}, using previous: {fallback_score}")
            return {"score": fallback_score, "confidence": "low",
                    "weighted_score": fallback_score * CONFIDENCE_WEIGHTS["low"]}
        print(f"    [WARN] Could not parse score for {criterion_id}, no fallback")
        return {"score": 0, "confidence": "low", "weighted_score": 0.0}

    weighted = score * CONFIDENCE_WEIGHTS.get(confidence, 0.7)
    return {"score": score, "confidence": confidence, "weighted_score": round(weighted, 2)}


def verify_score_jump(skill_config: dict, criterion_id: str, criterion: dict,
                      pre_score: int, post_score: int) -> int:
    """Anti-gaming: re-evaluate with rephrased prompt when score jumps 5+ points.
    Returns verified score (may be lower than post_score)."""
    jump = post_score - pre_score
    if jump < ANTIGAMING_JUMP_THRESHOLD:
        return post_score

    print(f"    [ANTIGAMING] {criterion_id} jumped {pre_score}→{post_score} (+{jump}). Verifying...")
    skill_path = skill_config["skill_path"]
    target_files = " ".join(criterion.get("target_files", []))
    original_eval = criterion["eval_prompt"].replace("{skill_path}", skill_path)

    # Rephrased verification prompt — different framing, same substance
    verify_prompt = f"""You are a skeptical quality auditor performing a VERIFICATION check.

A previous evaluation scored this criterion {post_score}/10. Your job is to verify this independently.

CRITERION: {criterion_id} — {criterion['name']}
TARGET: {skill_path} (files: {target_files})

WHAT TO CHECK (same rubric, different words):
{original_eval}

VERIFICATION RULES:
- Read ALL target files. Score based on what you ACTUALLY find.
- Do NOT assume the previous score is correct. Start from scratch.
- Look specifically for SUPERFICIAL content that checks boxes without substance.
- Check: is content genuinely useful, or just placeholder text that matches keywords?
- A file that exists but contains only boilerplate/padding scores lower than one with dense, actionable content.

Return ONLY: {{"score": <0-10>, "confidence": "<high|medium|low>", "reasoning": "<why>"}}"""

    import re
    m1, _ = resolve_eval_models(skill_path, criterion)
    output = run_claude(verify_prompt, allowed_tools="Read", timeout=180,
                        model=m1, max_turns=5)

    # Parse verification score
    for line in output.split("\n"):
        line = line.strip()
        if "{" in line and "score" in line:
            try:
                data = json.loads(line)
                v_score = min(10, max(0, int(data.get("score", 0))))
                gap = abs(post_score - v_score)
                if gap >= 3:
                    # Significant disagreement — use average, rounded down
                    verified = (post_score + v_score) // 2
                    print(f"    [ANTIGAMING] Verification disagrees: {post_score} vs {v_score} → using {verified}")
                    return verified
                print(f"    [ANTIGAMING] Verification confirmed: {v_score} (gap={gap})")
                return min(post_score, v_score)
            except json.JSONDecodeError:
                pass

    json_match = re.search(r'"score"\s*:\s*(\d+)', output)
    if json_match:
        v_score = min(10, max(0, int(json_match.group(1))))
        return min(post_score, v_score)

    print(f"    [ANTIGAMING] Verification parse failed, keeping original score")
    return post_score


def evaluate_all(skill_config: dict, parallel: int = 2, previous_scores: dict = None,
                  cycle: int = 1, state: dict = None) -> dict:
    """Evaluate criteria with tiered frequency scheduling.
    Hot (0-6): every cycle. Warm (7-8): every 2nd. Cold/graduated (9-10): every 5th.
    Context engineering: selection — eval tokens proportional to improvement potential.
    previous_scores: {cid: int|dict} used as fallback on parse failure."""
    criteria = skill_config["criteria"]
    results = {}
    prev = previous_scores or {}
    eval_state = state or {}

    # Determine which criteria to eval this cycle
    to_eval = {}
    skipped = []
    for cid, cdef in criteria.items():
        prev_score = get_score(prev.get(cid, 0))
        tier = get_eval_tier(cid, prev_score, eval_state)
        if should_eval_this_cycle(cid, tier, cycle):
            to_eval[cid] = cdef
        else:
            # Carry forward previous score
            if cid in prev:
                results[cid] = prev[cid] if isinstance(prev[cid], dict) else {
                    "score": prev[cid], "confidence": "medium",
                    "weighted_score": prev[cid] * CONFIDENCE_WEIGHTS["medium"]
                }
            skipped.append(f"{cid}({tier})")

    if skipped:
        print(f"    Skipped (tiered): {', '.join(skipped)}")
    print(f"    Evaluating {len(to_eval)}/{len(criteria)} criteria this cycle")

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {}
        for cid, cdef in to_eval.items():
            prev_val = prev.get(cid)
            fallback = prev_val["score"] if isinstance(prev_val, dict) else prev_val
            future = executor.submit(evaluate_criterion, skill_config, cid, cdef, fallback)
            futures[future] = cid

        for future in as_completed(futures):
            cid = futures[future]
            try:
                result = future.result()
                results[cid] = result
                conf_tag = f" conf={result['confidence']}" if result.get("confidence") else ""
                print(f"    {cid} ({criteria[cid]['name']}): {result['score']}/10{conf_tag}")
            except Exception as e:
                results[cid] = {"score": 0, "confidence": "low", "weighted_score": 0.0}
                print(f"    {cid}: ERROR - {e}")

    return results


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
    # Normalize: if using confidence, effective max is weight * 10 * 1.0
    return round(weighted / total_weight * 10, 2) if not use_confidence else round(weighted / total_weight * 10, 2)


COOLDOWN_CYCLES = 3       # Cycles to skip after consecutive failures
MAX_CONSECUTIVE_FAILS = 3 # Consecutive reverts before cooldown kicks in
PARK_THRESHOLD = 6        # Total failures before parking the criterion

# --- Criteria Lifecycle (Context Engineering) ---
GRADUATE_THRESHOLD = 3    # Consecutive cycles at 9-10 before graduation
GRADUATE_SPOT_CHECK = 5   # Re-eval graduated criteria every N cycles
MAX_ACTIVE_CRITERIA = 15  # Cap on active (non-graduated, non-parked) criteria
WARM_TIER_INTERVAL = 2    # Eval warm (7-8) criteria every N cycles
COLD_TIER_INTERVAL = 5    # Eval cold/graduated (9-10) criteria every N cycles


def pick_weakest_criterion(scores: dict, criteria: dict, state: dict) -> str | None:
    """Pick the criterion with lowest score, respecting cooldown and parked status.
    Prioritizes low-confidence scores (unreliable evals need re-targeting)."""
    run_num = state["run_number"]
    failures = state.get("failures", {})
    parked = state.get("parked", [])

    graduated = state.get("graduated", [])

    weighted_scores = {}
    for cid, cdef in criteria.items():
        if cid in parked or cid in graduated:
            continue
        fail_info = failures.get(cid, {})
        cooldown_until = fail_info.get("cooldown_until", 0)
        if run_num < cooldown_until:
            continue

        score = get_score(scores.get(cid, 0))
        conf = get_confidence(scores.get(cid, 0))
        # Lower score + higher weight = higher priority
        # Low confidence adds a small boost (uncertain scores deserve re-examination)
        conf_boost = 1.2 if conf == "low" else 1.0
        priority = (10 - score) * cdef["weight"] * conf_boost
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


def update_graduation(state: dict, scores: dict, criteria: dict):
    """Graduate criteria scoring 9-10 for GRADUATE_THRESHOLD consecutive cycles.
    Context engineering: compaction — remove solved criteria from hot eval path."""
    high_streak = state.setdefault("high_streak", {})
    graduated = state.setdefault("graduated", [])

    for cid in list(criteria.keys()):
        if cid in graduated or cid in state.get("parked", []):
            continue
        score = get_score(scores.get(cid, 0))
        if score >= 9:
            high_streak[cid] = high_streak.get(cid, 0) + 1
            if high_streak[cid] >= GRADUATE_THRESHOLD and cid not in graduated:
                graduated.append(cid)
                print(f"  [GRADUATED] {cid} ({criteria[cid]['name']}) — scored 9+ for {GRADUATE_THRESHOLD} cycles")
        else:
            high_streak[cid] = 0

    # Un-graduate if a spot-check reveals regression below 7
    for cid in list(graduated):
        score = get_score(scores.get(cid, 0))
        if score < 7:
            graduated.remove(cid)
            high_streak[cid] = 0
            print(f"  [UNGRADUATED] {cid} regressed to {score} — back in active rotation")


def get_eval_tier(cid: str, score: int, state: dict) -> str:
    """Classify criterion into eval tier for frequency-based scheduling.
    Context engineering: selection — evaluate proportional to improvement potential."""
    if cid in state.get("graduated", []):
        return "cold"
    if score >= 7:
        return "warm"
    return "hot"


def should_eval_this_cycle(cid: str, tier: str, cycle: int) -> bool:
    """Determine if criterion should be evaluated this cycle based on tier."""
    if tier == "hot":
        return True
    if tier == "warm":
        return cycle % WARM_TIER_INTERVAL == 0
    if tier == "cold":
        return cycle % COLD_TIER_INTERVAL == 0
    return True


def check_criteria_overlap(existing: dict, candidate: dict) -> bool:
    """Detect overlap between candidate criterion and existing criteria.
    Context engineering: compression — prevent redundant criteria from inflating eval cost.
    Returns True if candidate overlaps with any existing criterion."""
    cand_files = set(candidate.get("target_files", []))
    cand_name = candidate.get("name", "").lower()

    stop_words = {"and", "the", "of", "in", "for", "with", "a", "an", "is", "to"}

    for cid, cdef in existing.items():
        existing_files = set(cdef.get("target_files", []))
        if not cand_files or not existing_files:
            continue
        file_overlap = len(cand_files & existing_files) / max(len(cand_files), 1)
        if file_overlap > 0.5:
            # Check name similarity — 1 shared domain word enough with high file overlap
            existing_name = cdef.get("name", "").lower()
            cand_words = set(cand_name.split()) - stop_words
            existing_words = set(existing_name.split()) - stop_words
            shared_words = cand_words & existing_words
            if shared_words:
                print(f"  [OVERLAP] Candidate '{candidate['name']}' overlaps with {cid} "
                      f"({cdef['name']}) — files: {file_overlap:.0%}, shared: {shared_words}")
                return True
    return False


def enforce_active_cap(skill_config: dict, state: dict):
    """Enforce MAX_ACTIVE_CRITERIA cap on non-graduated, non-parked criteria.
    Context engineering: selection — bound eval cost per cycle.
    Archives lowest-weight graduated criteria if discovery pushes over cap."""
    criteria = skill_config["criteria"]
    graduated = state.get("graduated", [])
    parked = state.get("parked", [])
    active = [cid for cid in criteria if cid not in graduated and cid not in parked]

    if len(active) <= MAX_ACTIVE_CRITERIA:
        return

    overflow = len(active) - MAX_ACTIVE_CRITERIA
    # Sort active by (score desc, weight asc) — graduate the highest-scoring, lowest-weight first
    scores = state.get("scores", {})
    candidates = sorted(active,
                        key=lambda c: (-get_score(scores.get(c, 0)), criteria[c]["weight"]))

    for cid in candidates[:overflow]:
        score = get_score(scores.get(cid, 0))
        if score >= 7:  # Only force-graduate if reasonably solved
            graduated.append(cid)
            print(f"  [CAP] Force-graduated {cid} (score={score}, weight={criteria[cid]['weight']}) "
                  f"— active cap {MAX_ACTIVE_CRITERIA} exceeded")
        else:
            break  # Don't graduate low-scoring criteria


def research_criterion(skill_config: dict, criterion_id: str, criterion: dict) -> str:
    """Run research agent to describe target file contents + gather external context.
    Returns structured summary. Agent does NOT know what criterion is being improved."""
    skill_path = skill_config["skill_path"]
    target_files = ", ".join(criterion.get("target_files", []))

    # Pre-compute file facts for the research agent too
    file_facts = precompute_file_facts(skill_path, criterion.get("target_files", []))

    research_prompt = f"""You are a technical documentation analyst. Analyze these files objectively.

FILES TO ANALYZE (at {skill_path}): {target_files}

## Pre-Computed File Stats:
{file_facts}

## Tasks (in order):
1. Read each file completely.
2. For each file: main sections/headings, format (tables/prose/lists), content density.
3. Key content: topics covered, patterns/examples, concrete values vs vague advice.
4. Cross-file: inconsistencies, duplicate content, unresolved references.
5. Gaps: thin sections, placeholder-like content, missing cross-references.
6. Use Bash to run quick validation checks:
   - Grep for TODO/FIXME/placeholder markers
   - Check if referenced file paths actually exist
   - Count unique entries/patterns vs total lines (density check)

Be FACTUAL. Do not suggest improvements. Do not evaluate quality. Just describe.
Keep summary under 500 words. Use bullet points, not prose."""

    research_model = resolve_improve_model(skill_path, criterion)
    output = run_claude(
        research_prompt,
        allowed_tools="Read,Bash,Grep,Glob",
        timeout=180,
        model=research_model,
        max_turns=5,
        cwd=skill_path
    )

    if "[ERROR" in output or "[TIMEOUT]" in output:
        return ""
    return output


def domain_research(skill_config: dict) -> str:
    """Research best practices for the skill's domain via web search.
    Called during criteria creation to ground criteria in external knowledge."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]

    # Read SKILL.md first few lines to understand the domain
    skill_md = Path(skill_path) / "SKILL.md"
    description = ""
    if skill_md.exists():
        lines = skill_md.read_text().split("\n")[:20]
        description = "\n".join(lines)

    research_prompt = f"""You are a domain expert researcher. A Claude Code skill named '{skill_name}' needs improvement.

SKILL DESCRIPTION (first 20 lines of SKILL.md):
{description}

## Research Tasks:
1. Search the web for best practices in this skill's domain.
   - What do experts recommend for this type of tool/workflow?
   - What are common pitfalls or anti-patterns?
   - What quality standards exist (accessibility, performance, correctness)?
2. Search for competing tools, similar skills, or established frameworks.
   - How do they handle the same problem?
   - What features do they emphasize?
3. Search for user feedback patterns on similar tools.
   - What do users complain about most?
   - What do users praise?
4. If the skill references specific technologies (CSS, Tailwind, fonts, etc.):
   - Search for correctness standards (valid CSS, real font names, existing classes)
   - Search for up-to-date documentation

## Output Format:
Return a structured report:
### Domain Best Practices
- [finding 1]
- [finding 2]

### Competitive Landscape
- [tool/framework]: [key differentiator]

### Common Pitfalls
- [pitfall 1]

### Technical Validation Standards
- [standard 1]

### Suggested Criteria Themes
Based on the above research, suggest 3-5 criterion themes that would be valuable to evaluate.
Each theme should have: name, what to check, why it matters.

Keep total output under 600 words. Prioritize actionable findings over comprehensive coverage."""

    # Domain research benefits from larger context (opus 1M) for web content
    domain_model = "opus" if MODEL_PROFILE in ("quality", "auto") else EVAL_MODEL
    output = run_claude(
        research_prompt,
        allowed_tools="Read,WebSearch,WebFetch,Bash",
        timeout=300,
        model=domain_model,
        max_turns=8,
        cwd=skill_path
    )

    if "[ERROR" in output or "[TIMEOUT]" in output:
        print(f"  [DOMAIN RESEARCH] Failed or timed out")
        return ""
    return output


# --- Ground Truth Calibration ---
# Pipeline: acquire (load gold) → process (eval) → parse (score) → render (drift report)

def load_calibration(skill_name: str) -> dict | None:
    """Acquire: Load gold standard scores for a skill. Returns {cid: expected_score} or None."""
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
    """Run calibration check: evaluate gold criteria and compare to expected scores.
    Returns drift report: {cid: {"expected": int, "actual": int, "drift": int, "drifted": bool}}."""
    skill_name = skill_config["skill_name"]
    gold = load_calibration(skill_name)
    if not gold:
        return {}

    print(f"\n  [CALIBRATE] Checking eval calibration against {len(gold)} gold standards...")
    criteria = skill_config["criteria"]
    report = {}

    # Process: evaluate only gold criteria
    for cid, expected_score in gold.items():
        if cid not in criteria:
            print(f"    [CALIBRATE] {cid}: criterion no longer exists, skipping")
            continue
        # Parse: evaluate and extract score
        result = evaluate_criterion(skill_config, cid, criteria[cid])
        actual = get_score(result)
        drift = abs(actual - expected_score)
        drifted = drift >= 3

        # Render: report per criterion
        status = "DRIFT" if drifted else "OK"
        print(f"    [{status}] {cid}: expected={expected_score} actual={actual} (drift={drift})")
        report[cid] = {
            "expected": expected_score,
            "actual": actual,
            "drift": drift,
            "drifted": drifted,
            "confidence": get_confidence(result)
        }

    # Render: summary
    drifted_count = sum(1 for r in report.values() if r["drifted"])
    if drifted_count > 0:
        print(f"\n  [CALIBRATE] WARNING: {drifted_count}/{len(report)} criteria drifted 3+ points")
        print(f"  [CALIBRATE] Eval prompts may need recalibration, or gold standards need updating")
    else:
        print(f"\n  [CALIBRATE] All {len(report)} gold standards within tolerance")

    # Save drift report
    report_path = DATA_DIR / f"calibration-report-{skill_name}.json"
    with open(report_path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "report": report}, f, indent=2)

    return report


def create_calibration_from_current(skill_config: dict, state: dict):
    """Snapshot current scores as gold standard for future calibration.
    Only includes high-confidence scores to avoid enshrining noise."""
    skill_name = skill_config["skill_name"]
    scores = state.get("scores", {})
    gold = {}
    for cid, val in scores.items():
        conf = get_confidence(val)
        if conf == "high":
            gold[cid] = get_score(val)

    if not gold:
        # Fall back to medium confidence if no high-confidence scores
        for cid, val in scores.items():
            if get_confidence(val) in ("high", "medium"):
                gold[cid] = get_score(val)

    if gold:
        save_calibration(skill_name, gold)
        print(f"  [CALIBRATE] Created gold standard with {len(gold)} criteria")
    else:
        print(f"  [CALIBRATE] No scores available to create gold standard. Run a baseline eval first.")


def improve_criterion(skill_config: dict, criterion_id: str, criterion: dict,
                      current_score: int, state: dict = None) -> bool:
    """Run an improvement agent for a specific criterion. Returns True if files changed."""
    skill_path = skill_config["skill_path"]
    skill_name = skill_config["skill_name"]
    target_files = ", ".join(criterion.get("target_files", []))

    # Step 1: Unbiased research
    print(f"    [RESEARCH] Gathering objective file summary...")
    research_summary = research_criterion(skill_config, criterion_id, criterion)
    if not research_summary:
        research_summary = "(research agent failed — read files directly)"

    # Step 2: Build requirements from eval_prompt or checklist (reframe scoring → directives)
    if "checklist" in criterion:
        checklist_items = "\n".join(
            f"  - [{c['points']}pt] {c['item']}" for c in criterion["checklist"]
        )
        requirements = (
            "The evaluator checks the following binary PASS/FAIL items "
            "(treat as edit directives — each must be clearly present):\n\n"
            + checklist_items
        )
    else:
        eval_text = criterion['eval_prompt'].replace('{skill_path}', skill_path)
        requirements = (
            "The following are requirements the evaluator checks for "
            "(reframed from scoring rubric — treat as edit directives):\n\n"
            + eval_text
        )

    # Step 3: Load past failed attempts from results JSONL
    failed_attempts = "None"
    if state:
        results_path = DATA_DIR / f"results-{skill_name}.jsonl"
        if results_path.exists():
            recent_fails = []
            for line in results_path.read_text().strip().split("\n"):
                try:
                    entry = json.loads(line)
                    if entry.get("target") == criterion_id and not entry.get("kept"):
                        recent_fails.append(
                            f"- Run #{entry.get('run')}: score {entry.get('pre_score')} → "
                            f"{entry.get('post_score')} (reason: {entry.get('reason', 'no improvement')})"
                        )
                except (json.JSONDecodeError, KeyError):
                    pass
            if recent_fails:
                failed_attempts = "\n".join(recent_fails[-3:])

    improve_prompt = f"""You are improving the '{skill_name}' Claude Code skill.

## Current State (from independent research)
{research_summary}

## What Needs Improvement
Criterion: {criterion['name']} (current score: {current_score}/10)
Target files: {target_files}

Requirements (what the evaluator checks for):
{requirements}

## Previous Failed Attempts (avoid repeating these)
{failed_attempts}

## Edit Directives
1. Read the target files to verify the research summary
2. Identify specific gaps based on the requirements above
3. Make targeted edits to fill those gaps
4. Keep changes minimal and focused — don't restructure
5. Preserve existing content quality

RULES:
- Edit existing files, don't create new ones (unless target doesn't exist yet)
- Keep files under 300 lines each
- Don't remove existing good content"""

    improve_model = resolve_improve_model(skill_path, criterion)
    output = run_claude(
        improve_prompt,
        allowed_tools="Read,Edit",
        timeout=300,
        model=improve_model,
        max_turns=10,
        cwd=skill_path
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

    refine_model = resolve_improve_model(skill_path, criterion)
    output = run_claude(refine_prompt, allowed_tools="Read,Grep,Glob", timeout=180,
                        model=refine_model, max_turns=5)

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


DISCOVER_INTERVAL = 5  # Run criteria discovery every N cycles


def discover_criteria(skill_config: dict, state: dict) -> list[dict]:
    """Spawn agent to propose new criteria based on current skill state + domain knowledge.
    Returns list of proposed criteria dicts (not yet added to config)."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]
    existing_criteria = skill_config["criteria"]
    scores = state.get("scores", {})

    # Summarize existing criteria for context
    existing_summary = []
    for cid, cdef in existing_criteria.items():
        s = get_score(scores.get(cid, 0))
        existing_summary.append(f"- {cid} ({cdef['name']}): score={s}/10, weight={cdef['weight']}")
    existing_text = "\n".join(existing_summary)

    # Find next available criterion ID
    existing_ids = list(existing_criteria.keys())
    prefix = existing_ids[0][0] if existing_ids else "C"
    max_num = max(int(cid[len(prefix):]) for cid in existing_ids if cid[len(prefix):].isdigit())
    next_id_start = max_num + 1

    discover_prompt = f"""You are a skill quality analyst discovering NEW evaluation criteria.

SKILL: {skill_name} at {skill_path}
Read the SKILL.md and 2-3 reference files to understand the skill's purpose and content.

## Existing Criteria (do NOT duplicate these):
{existing_text}

## Your Task:
1. Read the skill files to understand what it does.
2. Identify 1-3 quality dimensions NOT covered by existing criteria.
   Focus on:
   - Functional correctness (does the output actually work?)
   - Usability gaps (confusing flow, missing guidance)
   - Cross-file consistency (contradictions between files)
   - Structural issues (file organization, context budget)
   - Domain-specific standards that existing criteria miss
3. For each proposed criterion, define it precisely.

## Rules:
- Do NOT propose criteria that overlap with existing ones.
- Each criterion must be evaluable by reading files (no runtime testing).
- Prefer criteria with BINARY checklist items over subjective quality judgments.
- Weight: 5-8 for nice-to-have, 9-10 for critical quality dimensions.

Return ONLY a JSON array (no markdown, no explanation):
[{{"id": "{prefix}{next_id_start}", "name": "Criterion Name", "weight": 7, "target_files": ["SKILL.md"], "eval_prompt": "Read {{skill_path}}/SKILL.md. Score 0-10: [specific checklist]..."}}]

Return empty array [] if no new criteria are needed."""

    # Discovery benefits from stronger model (creative analysis task)
    discover_model = "opus" if MODEL_PROFILE in ("quality", "auto") else EVAL_MODEL
    output = run_claude(
        discover_prompt,
        allowed_tools="Read,Grep,Glob",
        timeout=180,
        model=discover_model,
        max_turns=5,
        cwd=skill_path
    )

    # Parse proposals
    import re
    proposals = []
    # Try to find JSON array
    array_match = re.search(r'\[.*\]', output, re.DOTALL)
    if array_match:
        try:
            items = json.loads(array_match.group())
            if isinstance(items, list):
                for item in items:
                    if all(k in item for k in ("id", "name", "weight", "target_files", "eval_prompt")):
                        proposals.append(item)
        except json.JSONDecodeError:
            pass

    return proposals


def apply_discovered_criteria(skill_config: dict, state: dict, proposals: list[dict]):
    """Add discovered criteria to the criteria JSON and in-memory config."""
    if not proposals:
        return
    skill_name = skill_config["skill_name"]
    criteria_path = CRITERIA_DIR / f"{skill_name}.json"

    added = 0
    for prop in proposals:
        cid = prop["id"]
        if cid in skill_config["criteria"]:
            print(f"  [DISCOVER] Skipping {cid} — already exists")
            continue
        # Context engineering: compression — check overlap before adding
        if check_criteria_overlap(skill_config["criteria"], prop):
            print(f"  [DISCOVER] Skipping {cid} — overlaps with existing criterion")
            continue
        skill_config["criteria"][cid] = {
            "name": prop["name"],
            "weight": prop["weight"],
            "target_files": prop["target_files"],
            "eval_prompt": prop["eval_prompt"]
        }
        added += 1
        print(f"  [DISCOVER] Added {cid}: {prop['name']} (weight={prop['weight']})")

    # Enforce active cap after discovery
    if added > 0 and state:
        enforce_active_cap(skill_config, state)

    # Persist to disk
    with open(criteria_path) as f:
        config = json.load(f)
    config["criteria"] = skill_config["criteria"]
    with open(criteria_path, "w") as f:
        json.dump(config, f, indent=2)


def run_cycle(skill_name: str, skill_config: dict, state: dict, parallel: int, auto_refine: bool = False) -> dict:
    """Run one improvement cycle: evaluate → improve weakest → re-evaluate → keep/revert."""
    run_num = state["run_number"] + 1
    state["run_number"] = run_num
    log_seq = state.get("log_seq", 0) + 1
    state["log_seq"] = log_seq
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

    # Step 1: Evaluate current state (tiered — hot every cycle, warm/cold less often)
    print(f"\n  [1/6] Evaluating current state...")
    scores = evaluate_all(skill_config, parallel=parallel,
                          previous_scores=state.get("scores"),
                          cycle=run_num, state=state)
    total = compute_weighted_total(scores, skill_config["criteria"])
    raw_total = compute_weighted_total(scores, skill_config["criteria"], use_confidence=False)
    print(f"\n  Weighted score: {total}/10 (raw: {raw_total}/10)")

    # Graduation check — promote criteria stable at 9-10
    update_graduation(state, scores, skill_config["criteria"])

    # Score stability detection: flag criteria with high eval noise
    prev_scores = state.get("scores", {})
    for cid in scores:
        if cid in prev_scores:
            old_s = get_score(prev_scores[cid])
            new_s = get_score(scores[cid])
            # Only flag if criterion wasn't targeted last run (untouched = should be stable)
            last_target = state.get("last_target")
            if cid != last_target and abs(old_s - new_s) >= 3:
                print(f"  [NOISE] {cid} shifted {old_s}→{new_s} untouched — eval instability")

    # Sync state with actual evaluated scores (prevents state drift)
    state["scores"] = scores
    state["best_total"] = total

    # Criteria discovery: every N cycles, propose new criteria
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

    # Auto-refine check: if criterion is about to hit cooldown, refine proactively
    if auto_refine and fail_info.get("consecutive", 0) == MAX_CONSECUTIVE_FAILS - 1:
        print(f"  [REFINE] Proactive refinement — next failure would trigger cooldown")
        refine_criterion(skill_config, target_cid, target_cdef, state)
        # Re-read the (possibly updated) criterion
        target_cdef = skill_config["criteria"][target_cid]

    # Step 3: Snapshot files (for revert)
    skill_path = skill_config["skill_path"]

    # Step 3: Improve
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

    # Step 4: Selective re-evaluation (only criteria with overlapping target files)
    print(f"\n  [4/6] Selective re-evaluation...")
    modified = get_modified_files(skill_path)
    if modified:
        print(f"    Modified files: {', '.join(modified)}")

    # Find criteria whose target_files overlap with modified files
    criteria_to_reeval = {target_cid}  # Always re-eval the target
    for cid, cdef in skill_config["criteria"].items():
        if cid == target_cid:
            continue
        cid_files = set(cdef.get("target_files", []))
        if cid_files & modified:
            criteria_to_reeval.add(cid)

    # Full re-eval every 5th cycle to catch cumulative drift
    if run_num % 5 == 0:
        criteria_to_reeval = set(skill_config["criteria"].keys())
        print(f"    Full re-eval (every 5th cycle)")
    else:
        print(f"    Re-evaluating {len(criteria_to_reeval)}/{len(skill_config['criteria'])} criteria")

    # Re-evaluate affected criteria
    new_scores = dict(scores)  # Start with current scores
    for cid in criteria_to_reeval:
        cdef = skill_config["criteria"][cid]
        fallback = get_score(scores.get(cid))
        result_dict = evaluate_criterion(skill_config, cid, cdef, fallback_score=fallback)
        new_scores[cid] = result_dict
        if cid == target_cid:
            new_score = get_score(result_dict)

    new_total = compute_weighted_total(new_scores, skill_config["criteria"])

    # Step 5: Anti-gaming verification for large score jumps
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
                "weighted_score": verified_score * CONFIDENCE_WEIGHTS.get(
                    get_confidence(new_scores.get(target_cid, 0)), 0.7)
            }
            new_score = verified_score
            new_total = compute_weighted_total(new_scores, skill_config["criteria"])
            target_improved = new_score > current_score
    else:
        print(f"\n  [5/6] Anti-gaming check skipped (jump={new_score - current_score})")

    # Step 6: Keep/revert decision with regression detection
    total_regressed = new_total < total

    if target_improved and not total_regressed:
        print(f"\n  IMPROVED: {target_cid} {current_score} → {new_score} (total: {total} → {new_total})")
        state["scores"] = new_scores
        state["best_total"] = new_total
        record_success(state, target_cid)
        kept = True

        # Auto-commit to protect from next cycle's revert
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
    # Store CLI options for hot-reload and discovery
    skill_config["_cli_skill_path"] = skill_path
    skill_config["_discover_interval"] = discover_interval
    state = load_state(skill_name)
    if hours is not None:
        end_time = datetime.now() + timedelta(hours=hours)
    elif max_loops is None:
        end_time = datetime.now() + timedelta(hours=1.0)
    else:
        end_time = None  # No time limit, loop count only
    cycle = 0
    all_blocked_streak = 0

    clear_stop(skill_name)  # Clear any stale stop file

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
          f"{len(graduated)} graduated | {len(parked)} parked | cap: {MAX_ACTIVE_CRITERIA}")
    print(f"  Auto-refine: {'ON' if auto_refine else 'OFF'}")
    if MODEL_PROFILE == "auto":
        print(f"  Profile: auto (per-criterion routing: opus/sonnet/haiku based on complexity)")
    else:
        print(f"  Profile: {MODEL_PROFILE} | Eval: {EVAL_MODEL}+{EVAL_MODEL_2} | Improve: {IMPROVE_MODEL}")
    print(f"  Tiered eval: hot=every cycle, warm=every {WARM_TIER_INTERVAL}, cold=every {COLD_TIER_INTERVAL}")
    if end_time:
        print(f"  End time: {end_time.strftime('%H:%M:%S')}")
    print(f"{'#'*60}")

    # Pre-loop calibration check (if gold standard exists)
    cal_report = check_calibration(skill_config, parallel)
    if cal_report:
        drifted = [cid for cid, r in cal_report.items() if r["drifted"]]
        if drifted:
            print(f"  [CALIBRATE] Drifted criteria: {', '.join(drifted)}")
            print(f"  [CALIBRATE] Proceeding with loop — but eval_prompts for these may be unreliable")

    while True:
        # Check termination conditions
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

        # Detect all-blocked deadlock
        if result.get("action") == "all_blocked":
            all_blocked_streak += 1
            if all_blocked_streak >= 3:
                print(f"\n  [HALT] All criteria blocked for {all_blocked_streak} consecutive cycles.")
                print(f"  Refine criteria manually or re-run with --auto-refine")
                break
        else:
            all_blocked_streak = 0

        # Wait for cycle interval, checking for stop requests periodically
        wait = max(0, cycle_minutes * 60 - elapsed)
        remaining = (end_time - datetime.now()).total_seconds() if end_time else float('inf')
        if wait > 0 and remaining > wait:
            print(f"  Waiting {wait:.0f}s until next cycle...")
            wait_end = time.time() + wait
            while time.time() < wait_end:
                time.sleep(min(10, max(0.1, wait_end - time.time())))
                if check_stop_requested(skill_name):
                    break

    # Clean up stop file and print final summary
    clear_stop(skill_name)
    failures = state.get("failures", {})
    parked = state.get("parked", [])
    final_scores = state.get("scores", {})
    print(f"\n{'='*60}")
    print(f"  AUTORESEARCH COMPLETE: {skill_name}")
    print(f"  Total runs: {state['run_number']}")
    print(f"  Final score: {state.get('best_total', 0)}/10")
    # Per-criterion scores with confidence
    print(f"  Scores:")
    for cid in sorted(final_scores.keys()):
        s = get_score(final_scores[cid])
        c = get_confidence(final_scores[cid])
        print(f"    {cid}: {s}/10 (conf={c})")
    # Confidence distribution
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


def main():
    global EVAL_MODEL, EVAL_MODEL_2, IMPROVE_MODEL, MAX_ACTIVE_CRITERIA, MODEL_PROFILE
    parser = argparse.ArgumentParser(description="Skill Autoresearch Loop")
    parser.add_argument("--skill", required=True, help="Skill name (matches criteria/<name>.json)")
    parser.add_argument("--skill-path", default=None, help="Path to skill folder (overrides criteria JSON path)")
    parser.add_argument("--hours", type=float, default=None,
                        help="Duration in hours (default: 1, or unlimited if --max-loops set)")
    parser.add_argument("--parallel", type=int, default=2, help="Max parallel eval agents")
    parser.add_argument("--cycle-minutes", type=int, default=0, help="Minutes per cycle")
    parser.add_argument("--auto-refine", action="store_true",
                        help="Auto-refine stuck eval_prompts instead of just parking them")
    parser.add_argument("--max-loops", type=int, default=None,
                        help="Max improvement cycles (default: unlimited, time-limited only)")
    parser.add_argument("--stop", action="store_true",
                        help="Signal a running loop to stop after current cycle")
    parser.add_argument("--unpark", nargs="*", metavar="CID",
                        help="Unpark specific criteria (or all if no IDs given)")
    parser.add_argument("--profile", choices=["quality", "balanced", "budget", "auto"],
                        default="balanced",
                        help="Model profile: quality (opus+sonnet), balanced (sonnet+haiku), "
                             "budget (haiku+haiku), auto (per-criterion routing). Default: balanced")
    parser.add_argument("--eval-model", default=None,
                        help="Primary eval model override (default: set by --profile)")
    parser.add_argument("--eval-model-2", default=None,
                        help="Secondary eval model override (default: set by --profile)")
    parser.add_argument("--improve-model", default=None,
                        help="Improve model override (default: set by --profile)")
    parser.add_argument("--no-multi-sample", action="store_true", help="Disable dual-sample scoring")
    parser.add_argument("--discover-interval", type=int, default=DISCOVER_INTERVAL,
                        help=f"Run criteria discovery every N cycles (0=disabled, default: {DISCOVER_INTERVAL})")
    parser.add_argument("--domain-research", action="store_true",
                        help="Run domain research before starting the loop (grounds criteria in external knowledge)")
    parser.add_argument("--calibrate", choices=["create", "check"],
                        help="Create gold standard from current scores (create) or check eval drift (check)")
    parser.add_argument("--max-active", type=int, default=MAX_ACTIVE_CRITERIA,
                        help=f"Max active criteria cap (default: {MAX_ACTIVE_CRITERIA})")
    parser.add_argument("--graduate", nargs="*", metavar="CID",
                        help="Manually graduate criteria (or list graduated if no IDs)")
    args = parser.parse_args()

    # Handle --stop: signal a running loop to terminate
    if args.stop:
        request_stop(args.skill)
        return

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

    # Handle --graduate: manually graduate criteria or list graduated
    if args.graduate is not None:
        state = load_state(args.skill)
        graduated = state.setdefault("graduated", [])
        if not args.graduate:  # No IDs = list graduated
            if graduated:
                print(f"  Graduated: {', '.join(graduated)}")
            else:
                print(f"  No graduated criteria")
        else:
            for cid in args.graduate:
                if cid not in graduated:
                    graduated.append(cid)
                    state.setdefault("high_streak", {})[cid] = GRADUATE_THRESHOLD
                    print(f"  Graduated: {cid}")
                else:
                    print(f"  Already graduated: {cid}")
        save_state(args.skill, state)
        if not args.hours and not args.max_loops:
            return  # Standalone command

    # Apply model profile, then individual overrides
    if args.max_active != MAX_ACTIVE_CRITERIA:
        MAX_ACTIVE_CRITERIA = args.max_active
    MODEL_PROFILE = args.profile
    if args.profile != "auto" and args.profile in MODEL_PROFILES:
        profile = MODEL_PROFILES[args.profile]
        EVAL_MODEL = profile["eval"]
        EVAL_MODEL_2 = profile["eval_2"]
        IMPROVE_MODEL = profile["improve"]
    # Individual flags override profile settings
    if args.eval_model:
        EVAL_MODEL = args.eval_model
    if args.eval_model_2:
        EVAL_MODEL_2 = args.eval_model_2
    if args.improve_model:
        IMPROVE_MODEL = args.improve_model

    # Handle --calibrate: create or check gold standard (standalone, no loop)
    if args.calibrate:
        config = load_criteria(args.skill, args.skill_path)
        if args.calibrate == "create":
            state = load_state(args.skill)
            if not state.get("scores"):
                print(f"  [CALIBRATE] No scores in state. Run a baseline eval first.")
                return
            create_calibration_from_current(config, state)
        elif args.calibrate == "check":
            check_calibration(config, args.parallel)
        return

    # Optional: domain research before loop
    if args.domain_research:
        config = load_criteria(args.skill, args.skill_path)
        print(f"\n  [DOMAIN RESEARCH] Researching best practices for '{args.skill}'...")
        report = domain_research(config)
        if report:
            report_path = DATA_DIR / f"domain-research-{args.skill}.md"
            report_path.write_text(report)
            print(f"  [DOMAIN RESEARCH] Report saved to {report_path}")
            print(f"  [DOMAIN RESEARCH] Review and use to refine criteria before running the loop.")
        else:
            print(f"  [DOMAIN RESEARCH] No results (web search may have failed)")

    run_loop(args.skill, args.hours, args.parallel, args.cycle_minutes,
             args.skill_path, args.auto_refine, args.max_loops, args.discover_interval)


if __name__ == "__main__":
    main()
