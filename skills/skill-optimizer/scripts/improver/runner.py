"""Claude CLI subprocess wrapper."""

import subprocess
from pathlib import Path

from .config import CLAUDE_BIN, runtime


def run_claude(prompt: str, allowed_tools: str = "Read,Grep,Glob", timeout: int = 300,
               model: str = None, max_turns: int = None, cwd: str = None) -> str:
    """Run claude CLI in non-interactive mode."""
    if model is None:
        model = runtime.improve_model
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
