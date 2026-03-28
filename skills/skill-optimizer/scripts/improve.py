#!/usr/bin/env python3 -u
"""
Skill Improver — Autoresearch Loop for Claude Code Skills
Karpathy-pattern: improve -> evaluate -> keep/revert -> repeat

Usage:
    python3 improve.py --skill design-prompt --hours 1 --parallel 2
    python3 improve.py --skill proposal --hours 1 --parallel 2
    python3 improve.py --skill all --hours 2 --parallel 4
"""

from improver.cli import main

if __name__ == "__main__":
    main()
