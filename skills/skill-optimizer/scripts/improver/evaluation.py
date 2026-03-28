"""Evaluation — binary checklist, scalar scoring, cross-model ensemble, anti-gaming."""

import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import ANTIGAMING_JUMP_THRESHOLD, CONFIDENCE_WEIGHTS, runtime
from .models import resolve_eval_models
from .runner import run_claude
from .state import get_confidence, get_score


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
    """Run deterministic bash checks to pre-compute facts eval agents need."""
    facts = []
    for tf in target_files:
        fpath = os.path.join(skill_path, tf)
        if not os.path.exists(fpath):
            facts.append(f"- {tf}: FILE DOES NOT EXIST")
            continue
        result = subprocess.run(["wc", "-l", fpath], capture_output=True, text=True)
        line_count = result.stdout.strip().split()[0] if result.stdout.strip() else "?"
        result = subprocess.run(["grep", "-c", "^#", fpath], capture_output=True, text=True)
        heading_count = result.stdout.strip() or "0"
        result = subprocess.run(["grep", "-c", "^```", fpath], capture_output=True, text=True)
        code_blocks = int(result.stdout.strip() or "0") // 2
        facts.append(f"- {tf}: {line_count} lines, {heading_count} headings, {code_blocks} code blocks")
    return "\n".join(facts) if facts else "No target files found"


def evaluate_binary_checklist(skill_config: dict, criterion_id: str, criterion: dict) -> dict:
    """Evaluate criterion using deterministic binary PASS/FAIL per checklist item."""
    skill_path = skill_config["skill_path"]
    checklist = criterion["checklist"]
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
    if runtime.model_profile == "auto":
        print(f"    [{criterion_id}] auto-routed → {m1}")
    output = run_claude(prompt, allowed_tools="Read", timeout=180,
                        model=m1, max_turns=5)

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


def _parse_result(output: str) -> dict | None:
    """Parse score + confidence from claude output."""
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
                    print(f"    evidence={len(data.get('evidence', []))} conf={confidence}")
                return {"score": score, "confidence": confidence}
            except json.JSONDecodeError:
                pass
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
    numbers = re.findall(r'"score"\s*:\s*(\d+)', output)
    if numbers:
        return {"score": min(10, max(0, int(numbers[0]))), "confidence": "low"}
    return None


def evaluate_criterion(skill_config: dict, criterion_id: str, criterion: dict,
                       fallback_score: int | None = None) -> dict:
    """Evaluate a single criterion via claude CLI. Cross-model dual-sample scoring."""
    if "checklist" in criterion:
        return evaluate_binary_checklist(skill_config, criterion_id, criterion)

    skill_path = skill_config["skill_path"]
    eval_prompt = criterion["eval_prompt"].replace("{skill_path}", skill_path)
    target_files = criterion.get("target_files", [])
    target_files_str = " ".join(target_files)
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

    MODEL_CAPABILITY = {"opus": 1.0, "sonnet": 0.85, "haiku": 0.65}
    m1, m2 = resolve_eval_models(skill_path, criterion)

    if runtime.model_profile == "auto":
        print(f"    [{criterion_id}] auto-routed → {m1}+{m2}")
    output1 = run_claude(prompt, allowed_tools="Read", timeout=180, model=m1, max_turns=5)
    output2 = run_claude(prompt, allowed_tools="Read", timeout=180, model=m2, max_turns=5)

    r1 = _parse_result(output1)
    r2 = _parse_result(output2)

    if r1 is not None and r2 is not None:
        disagreement = abs(r1["score"] - r2["score"])
        w1 = MODEL_CAPABILITY.get(m1, 0.7)
        w2 = MODEL_CAPABILITY.get(m2, 0.7)

        if disagreement >= 3:
            score = round((r1["score"] * w1 + r2["score"] * w2) / (w1 + w2))
            confidence = "low"
            print(f"    [{criterion_id}] CROSS-MODEL DISAGREE: {m1}={r1['score']} vs {m2}={r2['score']} → weighted={score} conf=low")
        else:
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
    """Anti-gaming: re-evaluate with rephrased prompt when score jumps 5+ points."""
    jump = post_score - pre_score
    if jump < ANTIGAMING_JUMP_THRESHOLD:
        return post_score

    print(f"    [ANTIGAMING] {criterion_id} jumped {pre_score}→{post_score} (+{jump}). Verifying...")
    skill_path = skill_config["skill_path"]
    target_files = " ".join(criterion.get("target_files", []))
    original_eval = criterion["eval_prompt"].replace("{skill_path}", skill_path)

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

    m1, _ = resolve_eval_models(skill_path, criterion)
    output = run_claude(verify_prompt, allowed_tools="Read", timeout=180,
                        model=m1, max_turns=5)

    for line in output.split("\n"):
        line = line.strip()
        if "{" in line and "score" in line:
            try:
                data = json.loads(line)
                v_score = min(10, max(0, int(data.get("score", 0))))
                gap = abs(post_score - v_score)
                if gap >= 3:
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
    """Evaluate criteria with tiered frequency scheduling."""
    from .lifecycle import get_eval_tier, should_eval_this_cycle

    criteria = skill_config["criteria"]
    results = {}
    prev = previous_scores or {}

    to_eval = {}
    skipped = []
    for cid, cdef in criteria.items():
        prev_score = get_score(prev.get(cid, 0))
        tier = get_eval_tier(cid, prev_score, state or {})
        if should_eval_this_cycle(cid, tier, cycle):
            to_eval[cid] = cdef
        else:
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
