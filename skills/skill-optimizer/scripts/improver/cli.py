"""CLI entry point — argparse and main()."""

import argparse
import signal
import sys

from .config import (
    DISCOVER_INTERVAL, GRADUATE_THRESHOLD, MODEL_PROFILES,
    runtime,
)
from .agents import domain_research
from .calibration import check_calibration, create_calibration_from_current
from .loop import run_loop
from .state import load_criteria, load_state, request_stop, save_state, DATA_DIR


def _setup_signal_handlers(skill_name: str):
    """Register SIGINT/SIGTERM handlers for graceful shutdown."""
    def handler(signum, frame):
        sig_name = signal.Signals(signum).name
        print(f"\n  [SIGNAL] Received {sig_name}. Requesting graceful stop...")
        request_stop(skill_name)
        # If signaled twice, force exit
        signal.signal(signum, lambda s, f: sys.exit(1))
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


def main():
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
                        help="Run domain research before starting the loop")
    parser.add_argument("--calibrate", choices=["create", "check"],
                        help="Create gold standard from current scores (create) or check eval drift (check)")
    parser.add_argument("--max-active", type=int, default=runtime.max_active_criteria,
                        help=f"Max active criteria cap (default: {runtime.max_active_criteria})")
    parser.add_argument("--graduate", nargs="*", metavar="CID",
                        help="Manually graduate criteria (or list graduated if no IDs)")
    args = parser.parse_args()

    # Handle --stop
    if args.stop:
        request_stop(args.skill)
        return

    # Handle --unpark
    if args.unpark is not None:
        state = load_state(args.skill)
        if not args.unpark:
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

    # Handle --graduate
    if args.graduate is not None:
        state = load_state(args.skill)
        graduated = state.setdefault("graduated", [])
        if not args.graduate:
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
            return

    # Apply model profile, then individual overrides
    if args.max_active != runtime.max_active_criteria:
        runtime.max_active_criteria = args.max_active
    runtime.model_profile = args.profile
    if args.profile != "auto" and args.profile in MODEL_PROFILES:
        profile = MODEL_PROFILES[args.profile]
        runtime.eval_model = profile["eval"]
        runtime.eval_model_2 = profile["eval_2"]
        runtime.improve_model = profile["improve"]
    if args.eval_model:
        runtime.eval_model = args.eval_model
    if args.eval_model_2:
        runtime.eval_model_2 = args.eval_model_2
    if args.improve_model:
        runtime.improve_model = args.improve_model

    # Handle --calibrate
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
        else:
            print(f"  [DOMAIN RESEARCH] No results (web search may have failed)")

    _setup_signal_handlers(args.skill)
    run_loop(args.skill, args.hours, args.parallel, args.cycle_minutes,
             args.skill_path, args.auto_refine, args.max_loops, args.discover_interval)
