"""Agent pipelines — research, improve, refine, discover criteria."""

import json
import re
from pathlib import Path

from .config import CRITERIA_DIR, DATA_DIR, DISCOVER_INTERVAL, runtime
from .evaluation import precompute_file_facts
from .lifecycle import check_criteria_overlap, enforce_active_cap
from .models import resolve_eval_models, resolve_improve_model
from .runner import run_claude
from .state import get_score


def research_criterion(skill_config: dict, criterion_id: str, criterion: dict) -> str:
    """Run research agent to describe target file contents objectively."""
    skill_path = skill_config["skill_path"]
    target_files = ", ".join(criterion.get("target_files", []))
    file_facts = precompute_file_facts(skill_path, criterion.get("target_files", []))

    research_prompt = f"""You are a technical documentation analyst. Analyze these files objectively.

FILES TO ANALYZE (at {skill_path}): {target_files}

## Pre-Computed File Facts (verified via bash — trust these numbers, do NOT estimate or count manually):
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
    """Research best practices for the skill's domain via web search."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]

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

    domain_model = "opus" if runtime.model_profile in ("quality", "auto") else runtime.eval_model
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


def improve_criterion(skill_config: dict, criterion_id: str, criterion: dict,
                      current_score: int, state: dict = None) -> bool:
    """Run an improvement agent for a specific criterion. Returns True if files changed."""
    skill_path = skill_config["skill_path"]
    skill_name = skill_config["skill_name"]
    target_files = ", ".join(criterion.get("target_files", []))

    print(f"    [RESEARCH] Gathering objective file summary...")
    research_summary = research_criterion(skill_config, criterion_id, criterion)
    if not research_summary:
        research_summary = "(research agent failed — read files directly)"

    file_facts = precompute_file_facts(skill_path, criterion.get("target_files", []))

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
        # Strip raw scoring scale language before embedding in improve prompt
        eval_text = re.sub(r'\n[ \t]*[-*]?[ \t]*\d+[-\u2013]\d+[ \t]*:.*', '', eval_text)
        eval_text = re.sub(r'(?i)score\s+\d+[-\u2013]\d+[^.\n]*\.?[ \t]*\n?', '', eval_text)
        requirements = (
            "The following are requirements the evaluator checks for "
            "(treat as edit directives — each must be clearly present):\n\n"
            + eval_text
        )

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

## Pre-Computed File Facts (verified via bash — trust these numbers, do NOT estimate or count manually):
{file_facts}

## What Needs Improvement
Criterion: {criterion['name']}
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
    """Auto-refine a stuck criterion's eval_prompt or checklist. Returns True if criteria file updated."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]
    fail_info = state.get("failures", {}).get(cid, {})

    is_checklist = "checklist" in criterion

    if is_checklist:
        print(f"  [REFINE] Auto-refining checklist for {cid} ({criterion['name']})...")
        checklist_text = "\n".join(
            f"  - [{c['points']}pt] {c['item']}" for c in criterion["checklist"]
        )
        current_eval_text = f"CURRENT CHECKLIST:\n{checklist_text}"
        return_format = (
            '{"refined_checklist": [{"item": "<description>", "points": <int>}], '
            '"reasoning": "<why the old checklist was stuck>"}'
        )
    else:
        print(f"  [REFINE] Auto-refining eval_prompt for {cid} ({criterion['name']})...")
        current_eval_text = f"CURRENT EVAL_PROMPT:\n{criterion['eval_prompt']}"
        return_format = (
            '{"refined_eval_prompt": "<new eval_prompt text>", '
            '"reasoning": "<why the old one was stuck>"}'
        )

    refine_prompt = f"""You are improving a skill evaluation criterion that is stuck — it keeps scoring low but the improvement agent can't figure out how to fix it. The {'checklist' if is_checklist else 'eval_prompt'} is likely too vague, unreachable, or poorly calibrated.

CRITERION: {cid} — {criterion['name']}
WEIGHT: {criterion['weight']}
TARGET FILES: {', '.join(criterion.get('target_files', []))}
{current_eval_text}

FAILURE HISTORY: {fail_info.get('total', 0)} total failures, {fail_info.get('consecutive', 0)} consecutive

SKILL LOCATION: {skill_path}

Read the target files at {skill_path} to understand what the skill actually contains.

Then rewrite the {'checklist items' if is_checklist else 'eval_prompt'} to be:
1. More specific — concrete checklist items, not vague qualities
2. Achievable — scoring criteria the improvement agent can actually address
3. Well-calibrated — current content should score at least 3-4, not 0
4. Actionable — each checklist item maps to a specific edit

Return ONLY a JSON object:
{return_format}
Nothing else."""

    refine_model = resolve_improve_model(skill_path, criterion)
    output = run_claude(refine_prompt, allowed_tools="Read,Grep,Glob", timeout=180,
                        model=refine_model, max_turns=5)

    try:
        parsed_data = None
        # Tier 1: line-by-line JSON parse
        search_key = "refined_checklist" if is_checklist else "refined_eval_prompt"
        for line in output.split("\n"):
            line = line.strip()
            if "{" in line and search_key in line:
                try:
                    parsed_data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    pass
        # Tier 2: regex block extraction
        if not parsed_data:
            json_match = re.search(r'\{[^{}]*"' + search_key + r'"', output, re.DOTALL)
            if json_match:
                # Find the full JSON object starting from this match
                start = json_match.start()
                brace_depth = 0
                for i in range(start, len(output)):
                    if output[i] == '{':
                        brace_depth += 1
                    elif output[i] == '}':
                        brace_depth -= 1
                        if brace_depth == 0:
                            try:
                                parsed_data = json.loads(output[start:i+1])
                            except json.JSONDecodeError:
                                pass
                            break

        if parsed_data:
            criteria_path = CRITERIA_DIR / f"{skill_name}.json"
            reason = parsed_data.get("reasoning", "N/A")

            if is_checklist:
                new_checklist = parsed_data.get("refined_checklist")
                if new_checklist and isinstance(new_checklist, list) and len(new_checklist) >= 2:
                    # Validate checklist items have required fields
                    valid = all("item" in c and "points" in c for c in new_checklist)
                    if valid:
                        with open(criteria_path) as f:
                            config = json.load(f)
                        config["criteria"][cid]["checklist"] = new_checklist
                        with open(criteria_path, "w") as f:
                            json.dump(config, f, indent=2)
                        skill_config["criteria"][cid]["checklist"] = new_checklist
                        state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
                        if cid in state.get("parked", []):
                            state["parked"].remove(cid)
                        print(f"  [REFINE] Updated checklist for {cid} ({len(new_checklist)} items)")
                        print(f"  [REFINE] Reason: {reason}")
                        return True
            else:
                new_prompt = parsed_data.get("refined_eval_prompt")
                if new_prompt and len(new_prompt) > 20:
                    with open(criteria_path) as f:
                        config = json.load(f)
                    config["criteria"][cid]["eval_prompt"] = new_prompt
                    with open(criteria_path, "w") as f:
                        json.dump(config, f, indent=2)
                    skill_config["criteria"][cid]["eval_prompt"] = new_prompt
                    state["failures"][cid] = {"consecutive": 0, "total": 0, "cooldown_until": 0}
                    if cid in state.get("parked", []):
                        state["parked"].remove(cid)
                    print(f"  [REFINE] Updated eval_prompt for {cid}")
                    print(f"  [REFINE] Reason: {reason}")
                    return True
    except Exception as e:
        print(f"  [REFINE] Failed to parse refinement output: {e}")

    print(f"  [REFINE] Could not refine {cid} — parking it")
    return False


def discover_criteria(skill_config: dict, state: dict) -> list[dict]:
    """Spawn agent to propose new criteria based on current skill state."""
    skill_name = skill_config["skill_name"]
    skill_path = skill_config["skill_path"]
    existing_criteria = skill_config["criteria"]
    scores = state.get("scores", {})

    existing_summary = []
    for cid, cdef in existing_criteria.items():
        s = get_score(scores.get(cid, 0))
        existing_summary.append(f"- {cid} ({cdef['name']}): score={s}/10, weight={cdef['weight']}")
    existing_text = "\n".join(existing_summary)

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

    discover_model = "opus" if runtime.model_profile in ("quality", "auto") else runtime.eval_model
    output = run_claude(
        discover_prompt,
        allowed_tools="Read,Grep,Glob",
        timeout=180,
        model=discover_model,
        max_turns=5,
        cwd=skill_path
    )

    proposals = []
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

    if added > 0 and state:
        enforce_active_cap(skill_config, state)

    with open(criteria_path) as f:
        config = json.load(f)
    config["criteria"] = skill_config["criteria"]
    with open(criteria_path, "w") as f:
        json.dump(config, f, indent=2)
