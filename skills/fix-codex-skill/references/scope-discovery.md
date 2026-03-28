# Scope Discovery

## Goal

Find all likely global and project skill folders that may be loaded by coding tools, then normalize them to Codex-compatible shape.

## Default Scan Targets

User/global scope:

- `$CODEX_HOME/skills` (when present)
- `~/.codex/skills`
- `~/.claude/skills`
- `~/.agents/skills`

Project scope:

- `<cwd>/.codex/skills`
- `<cwd>/.claude/skills`
- `<git-root>/.codex/skills`
- `<git-root>/.claude/skills`

## Skill Folder Detection

A directory is treated as a skill if it contains `SKILL.md`.

The script skips hidden directories (names starting with `.`) when iterating children under a root.
