#!/usr/bin/env python3
"""Scan global/project skill folders and repair Codex compatibility issues."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
OPTIONAL_INTERFACE_KEYS = {"icon_small", "icon_large", "brand_color"}
ACRONYMS = {"API", "CI", "CLI", "JSON", "LLM", "MCP", "PDF", "PR", "UI", "URL", "SQL"}
BRANDS = {"openai": "OpenAI", "github": "GitHub", "fastapi": "FastAPI", "sqlite": "SQLite"}
SMALL_WORDS = {"and", "or", "to", "up", "with"}


@dataclass
class SkillResult:
    path: Path
    changed: bool = False
    frontmatter_changed: bool = False
    agents_yaml_changed: bool = False
    notes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def normalize_name(raw: str, fallback: str) -> str:
    value = raw if isinstance(raw, str) and raw.strip() else fallback
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    value = re.sub(r"-{2,}", "-", value)
    if not value:
        value = "skill"
    return value[:MAX_NAME_LEN].strip("-") or "skill"


def normalize_description(value: Any, skill_name: str) -> str:
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                parts.extend(f"{k}: {v}" for k, v in item.items())
            else:
                parts.append(str(item))
        value = " ".join(parts)
    elif isinstance(value, dict):
        value = " ".join(f"{k}: {v}" for k, v in value.items())
    elif value is None:
        value = ""
    elif not isinstance(value, str):
        value = str(value)

    desc = value.strip()
    if not desc:
        desc = (
            f"Skill for {skill_name} workflows. Use when users request tasks related to "
            f"{skill_name.replace('-', ' ')}."
        )

    desc = desc.replace("<", "(").replace(">", ")")
    if len(desc) > MAX_DESC_LEN:
        desc = desc[:MAX_DESC_LEN].rstrip()
    return desc


def format_display_name(skill_name: str) -> str:
    words = [w for w in skill_name.split("-") if w]
    formatted: list[str] = []
    for i, word in enumerate(words):
        lower = word.lower()
        upper = word.upper()
        if upper in ACRONYMS:
            formatted.append(upper)
        elif lower in BRANDS:
            formatted.append(BRANDS[lower])
        elif i > 0 and lower in SMALL_WORDS:
            formatted.append(lower)
        else:
            formatted.append(word.capitalize())
    return " ".join(formatted) if formatted else "Skill"


def generate_short_description(display_name: str) -> str:
    desc = f"Help with {display_name} tasks"
    if len(desc) < 25:
        desc = f"Help with {display_name} tasks and workflows"
    if len(desc) > 64:
        desc = f"Help with {display_name}"
    if len(desc) > 64:
        desc = f"{display_name} helper"
    if len(desc) > 64:
        trimmed = display_name[: 64 - len(" helper")].rstrip()
        desc = f"{trimmed} helper"
    if len(desc) < 25:
        desc = f"{desc} workflows"
    return desc[:64].rstrip()


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, text
    front = parts[0][4:]
    body = parts[1]
    return front, body


def parse_frontmatter(front: str | None) -> dict[str, Any]:
    if front is None:
        return {}
    try:
        data = yaml.safe_load(front)
        if isinstance(data, dict):
            return data
        return {}
    except yaml.YAMLError:
        # Fallback to empty dict if malformed; body is preserved.
        return {}


def build_frontmatter(data: dict[str, Any]) -> str:
    ordered: dict[str, Any] = {}
    for key in ["name", "description", "license", "allowed-tools", "metadata"]:
        if key in data:
            ordered[key] = data[key]
    yaml_block = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{yaml_block}\n---\n"


def normalize_frontmatter(original: dict[str, Any], skill_dir_name: str) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    meta = dict(original) if isinstance(original, dict) else {}

    compatibility = meta.pop("compatibility", None)
    if compatibility is not None:
        metadata = meta.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
        metadata.setdefault("compatibility", compatibility)
        meta["metadata"] = metadata
        notes.append("moved compatibility into metadata.compatibility")

    filtered = {k: v for k, v in meta.items() if k in ALLOWED_FRONTMATTER_KEYS}
    removed = sorted(set(meta.keys()) - ALLOWED_FRONTMATTER_KEYS)
    if removed:
        notes.append(f"removed unsupported keys: {', '.join(removed)}")

    raw_name = filtered.get("name", "")
    fixed_name = normalize_name(raw_name if isinstance(raw_name, str) else "", skill_dir_name)
    if raw_name != fixed_name:
        notes.append(f"normalized name: {raw_name!r} -> {fixed_name!r}")
    filtered["name"] = fixed_name

    raw_desc = filtered.get("description", "")
    fixed_desc = normalize_description(raw_desc, fixed_name)
    if raw_desc != fixed_desc:
        notes.append("normalized description")
    filtered["description"] = fixed_desc

    metadata = filtered.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        filtered["metadata"] = {"value": str(metadata)}
        notes.append("normalized metadata to object")

    return filtered, notes


def read_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def ensure_openai_yaml(existing_doc: dict[str, Any], skill_name: str) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    doc = dict(existing_doc) if isinstance(existing_doc, dict) else {}

    interface = doc.get("interface")
    if not isinstance(interface, dict):
        interface = {}

    display_name = interface.get("display_name")
    if not isinstance(display_name, str) or not display_name.strip():
        display_name = format_display_name(skill_name)
        notes.append("set interface.display_name")
    else:
        display_name = display_name.strip()

    short_description = interface.get("short_description")
    if not isinstance(short_description, str) or not (25 <= len(short_description.strip()) <= 64):
        short_description = generate_short_description(display_name)
        notes.append("set interface.short_description")
    else:
        short_description = short_description.strip()

    default_prompt = interface.get("default_prompt")
    required_token = f"${skill_name}"
    if not isinstance(default_prompt, str) or required_token not in default_prompt:
        default_prompt = f"Use {required_token} to diagnose and repair skill format issues."
        notes.append("set interface.default_prompt")

    new_interface: dict[str, Any] = {
        "display_name": display_name,
        "short_description": short_description,
        "default_prompt": default_prompt,
    }

    for k in OPTIONAL_INTERFACE_KEYS:
        if k in interface and isinstance(interface[k], str) and interface[k].strip():
            new_interface[k] = interface[k].strip()

    doc["interface"] = new_interface
    return doc, notes


def dump_yaml(obj: dict[str, Any]) -> str:
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)


def git_root(cwd: Path) -> Path | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception:
        return None
    root = out.stdout.strip()
    return Path(root) if root else None


def discover_roots(cwd: Path, include_user: bool, include_project: bool, extra_roots: list[str]) -> list[Path]:
    roots: list[Path] = []

    if include_user:
        codex_home = Path.home() / ".codex"
        if "CODEX_HOME" in os.environ:
            codex_home = Path(os.environ["CODEX_HOME"])
        roots.extend(
            [
                codex_home / "skills",
                Path.home() / ".codex" / "skills",
                Path.home() / ".claude" / "skills",
                Path.home() / ".agents" / "skills",
            ]
        )

    if include_project:
        roots.extend([cwd / ".codex" / "skills", cwd / ".claude" / "skills"])
        gr = git_root(cwd)
        if gr and gr != cwd:
            roots.extend([gr / ".codex" / "skills", gr / ".claude" / "skills"])

    for raw in extra_roots:
        roots.append(Path(raw).expanduser())

    unique: list[Path] = []
    seen: set[Path] = set()
    for r in roots:
        p = r.resolve()
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def iter_skills(root: Path) -> list[Path]:
    if (root / "SKILL.md").exists():
        return [root]
    if not root.exists() or not root.is_dir():
        return []
    results: list[Path] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / "SKILL.md").exists():
            results.append(child)
    return results


def process_skill(skill_dir: Path, dry_run: bool, verbose: bool) -> SkillResult:
    result = SkillResult(path=skill_dir)
    skill_md = skill_dir / "SKILL.md"

    try:
        original_text = safe_read(skill_md)
    except Exception as exc:
        result.errors.append(f"failed to read SKILL.md: {exc}")
        return result

    front_raw, body = split_frontmatter(original_text)
    current_frontmatter = parse_frontmatter(front_raw)
    normalized, notes = normalize_frontmatter(current_frontmatter, skill_dir.name)
    result.notes.extend(notes)

    frontmatter_changed = (front_raw is None) or (current_frontmatter != normalized)
    if frontmatter_changed:
        body_out = body.lstrip("\n")
        new_front = build_frontmatter(normalized)
        new_skill_text = f"{new_front}\n{body_out}" if body_out else f"{new_front}\n"
        result.changed = True
        result.frontmatter_changed = True
        if not dry_run:
            skill_md.write_text(new_skill_text, encoding="utf-8")

    agents_path = skill_dir / "agents" / "openai.yaml"
    existing_yaml_doc = read_yaml_file(agents_path)
    yaml_doc, yaml_notes = ensure_openai_yaml(existing_yaml_doc, normalized["name"])
    result.notes.extend(yaml_notes)
    if yaml_doc != existing_yaml_doc:
        new_yaml = dump_yaml(yaml_doc)
        result.changed = True
        result.agents_yaml_changed = True
        if not dry_run:
            agents_path.parent.mkdir(parents=True, exist_ok=True)
            agents_path.write_text(new_yaml, encoding="utf-8")

    if verbose and not result.notes and not result.errors:
        result.notes.append("no issues detected")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair Codex skill format issues across skill roots.")
    parser.add_argument("--root", action="append", default=[], help="Additional root to scan")
    parser.add_argument("--no-user", action="store_true", help="Skip default user-scope roots")
    parser.add_argument("--no-project", action="store_true", help="Skip default project-scope roots")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--verbose", action="store_true", help="Print details for every skill")
    args = parser.parse_args()

    cwd = Path.cwd()
    roots = discover_roots(
        cwd,
        include_user=not args.no_user,
        include_project=not args.no_project,
        extra_roots=args.root,
    )

    print(f"Scan mode: {'DRY-RUN' if args.dry_run else 'APPLY'}")
    print("Roots:")
    for r in roots:
        print(f"  - {r}")

    all_skills: list[Path] = []
    for root in roots:
        all_skills.extend(iter_skills(root))

    deduped: list[Path] = []
    seen: set[Path] = set()
    for s in all_skills:
        rs = s.resolve()
        if rs not in seen:
            seen.add(rs)
            deduped.append(rs)

    print(f"Detected skills: {len(deduped)}")

    changed = 0
    errors = 0
    for skill in deduped:
        res = process_skill(skill, dry_run=args.dry_run, verbose=args.verbose)
        state = "changed" if res.changed else "ok"
        if res.errors:
            state = "error"
            errors += 1
        if res.changed:
            changed += 1

        print(f"[{state}] {skill}")
        for note in res.notes:
            print(f"    - {note}")
        for err in res.errors:
            print(f"    ! {err}")

    print("Summary:")
    print(f"  skills_scanned={len(deduped)}")
    print(f"  skills_changed={changed}")
    print(f"  skills_with_errors={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
