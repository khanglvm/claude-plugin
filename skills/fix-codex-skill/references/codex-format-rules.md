# Codex Skill Format Rules

## Minimum Required

Every skill should include:

- `SKILL.md` with YAML frontmatter.
- Frontmatter `name` (hyphen-case, <= 64 chars).
- Frontmatter `description` (string, <= 1024 chars).

## Codex-Compatible Frontmatter Keys

Recommended safe key set:

- `name`
- `description`
- `license` (optional)
- `allowed-tools` (optional)
- `metadata` (optional)

When converting from Claude-centric skills, move extra compatibility metadata into `metadata` if needed.

## Agents Metadata (Codex)

`agents/openai.yaml` should exist for better Codex UI/runtime behavior.

At minimum, include under `interface`:

- `display_name`
- `short_description` (25-64 chars)
- `default_prompt`

## Common Breakages

- `description` accidentally written as YAML list, e.g. `description: [TODO: ...]`.
- Non-hyphen skill names.
- Missing frontmatter delimiters.
- Missing `agents/openai.yaml` after external installation.
