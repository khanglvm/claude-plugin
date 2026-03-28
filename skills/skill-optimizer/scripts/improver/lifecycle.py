"""Criteria lifecycle — cooldown, parking, graduation, overlap detection, cap enforcement."""

from .config import (
    COOLDOWN_CYCLES, GRADUATE_THRESHOLD, MAX_CONSECUTIVE_FAILS,
    PARK_THRESHOLD, COLD_TIER_INTERVAL, WARM_TIER_INTERVAL,
    runtime,
)
from .state import get_confidence, get_score


def pick_weakest_criterion(scores: dict, criteria: dict, state: dict) -> str | None:
    """Pick the criterion with lowest score, respecting cooldown and parked status."""
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
    """Graduate criteria scoring 9-10 for GRADUATE_THRESHOLD consecutive cycles."""
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

    for cid in list(graduated):
        score = get_score(scores.get(cid, 0))
        if score < 7:
            graduated.remove(cid)
            high_streak[cid] = 0
            print(f"  [UNGRADUATED] {cid} regressed to {score} — back in active rotation")


def get_eval_tier(cid: str, score: int, state: dict) -> str:
    """Classify criterion into eval tier for frequency-based scheduling."""
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
    """Detect overlap between candidate criterion and existing criteria."""
    cand_files = set(candidate.get("target_files", []))
    cand_name = candidate.get("name", "").lower()
    stop_words = {"and", "the", "of", "in", "for", "with", "a", "an", "is", "to"}

    for cid, cdef in existing.items():
        existing_files = set(cdef.get("target_files", []))
        if not cand_files or not existing_files:
            continue
        file_overlap = len(cand_files & existing_files) / max(len(cand_files), 1)
        if file_overlap > 0.5:
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
    """Enforce max active criteria cap. Force-graduates highest-scoring if over cap."""
    criteria = skill_config["criteria"]
    graduated = state.get("graduated", [])
    parked = state.get("parked", [])
    active = [cid for cid in criteria if cid not in graduated and cid not in parked]

    if len(active) <= runtime.max_active_criteria:
        return

    overflow = len(active) - runtime.max_active_criteria
    scores = state.get("scores", {})
    candidates = sorted(active,
                        key=lambda c: (-get_score(scores.get(c, 0)), criteria[c]["weight"]))

    for cid in candidates[:overflow]:
        score = get_score(scores.get(cid, 0))
        if score >= 7:
            graduated.append(cid)
            print(f"  [CAP] Force-graduated {cid} (score={score}, weight={criteria[cid]['weight']}) "
                  f"— active cap {runtime.max_active_criteria} exceeded")
        else:
            break
