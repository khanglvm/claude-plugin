---
name: fix-codex-skill
description: Repair invalid global or project skill formats for Codex compatibility, especially skills installed via `npx skills add` or copied from Claude-only templates. Use when users ask to fix broken global skills, invalid SKILL.md frontmatter, missing `agents/openai.yaml`, non-triggering skills, metadata schema issues, or cross-tool skill compatibility across Codex/Claude/agents skill folders.
metadata:
  version: "1.0.0"
---

# Fix Codex Skill

Use this skill to diagnose and repair skill-format problems across user-scope and project-scope skill directories.

## What This Skill Fixes

- Invalid `SKILL.md` YAML frontmatter.
- Missing or invalid `name` / `description` fields.
- Non-Codex-compatible frontmatter keys.
- Missing `agents/openai.yaml` metadata for Codex UI/runtime.
- Description/type issues that break quick validation.

## Scope Discovery

Run the repair script against default roots (user + project):

```bash
scripts/repair_codex_skill_format.py
```

Default user-scope roots:

- `$CODEX_HOME/skills` (if set)
- `~/.codex/skills`
- `~/.claude/skills`
- `~/.agents/skills`

Default project-scope roots:

- `<cwd>/.codex/skills`
- `<cwd>/.claude/skills`
- `<git-root>/.codex/skills` (if different)
- `<git-root>/.claude/skills` (if different)

## Safer First Run

Preview changes first:

```bash
scripts/repair_codex_skill_format.py --dry-run
```

Then apply:

```bash
scripts/repair_codex_skill_format.py
```

## Useful Flags

- Add extra scan roots:

```bash
scripts/repair_codex_skill_format.py --root /path/to/skills --root /another/skills
```

- Scan only user-scope defaults:

```bash
scripts/repair_codex_skill_format.py --no-project
```

- Scan only project-scope defaults:

```bash
scripts/repair_codex_skill_format.py --no-user
```

- Verbose output:

```bash
scripts/repair_codex_skill_format.py --verbose
```

## Validation Step

After repair, validate critical skills:

```bash
python3 /Users/khang/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

For format rules and rationale, load:

- `references/codex-format-rules.md`
- `references/scope-discovery.md`
- `references/remediation-workflow.md`
