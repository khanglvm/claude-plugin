"""Claude CLI subprocess wrapper with retry and backoff."""

import subprocess
import time
from pathlib import Path

from .config import CLAUDE_BIN, runtime

MAX_RETRIES = 2
BACKOFF_BASE = 5  # seconds


def run_claude(prompt: str, allowed_tools: str = "Read,Grep,Glob", timeout: int = 300,
               model: str = None, max_turns: int = None, cwd: str = None,
               max_retries: int = MAX_RETRIES) -> str:
    """Run claude CLI in non-interactive mode with retry on transient failures."""
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

    last_output = ""
    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd
            )
            if result.returncode != 0 and result.stderr:
                stderr_snippet = result.stderr[:200]
                print(f"    [WARN] claude stderr: {stderr_snippet}")
                # Retry on transient errors (rate limit, overloaded, network)
                if attempt < max_retries and any(k in result.stderr.lower()
                        for k in ("rate limit", "overloaded", "529", "503", "connection")):
                    wait = BACKOFF_BASE * (attempt + 1)
                    print(f"    [RETRY] Transient error, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    continue
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            last_output = "[TIMEOUT]"
            if attempt < max_retries:
                wait = BACKOFF_BASE * (attempt + 1)
                print(f"    [RETRY] Timeout after {timeout}s, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
                continue
        except Exception as e:
            last_output = f"[ERROR: {e}]"
            if attempt < max_retries:
                wait = BACKOFF_BASE * (attempt + 1)
                print(f"    [RETRY] Error: {e}, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
                continue

    return last_output
