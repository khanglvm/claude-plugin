---
name: codex-cli
description: This skill should be used whenever the user mentions Codex CLI (including "codex", "openai codex cli", "codex cli", or "gpt coding tool") or asks anything about Codex CLI setup, installation, authentication, configuration, config setting file options, model/provider configuration, commands, non-interactive usage, approvals, sandboxing, MCP/tools, AGENTS.md/skills integration, security, or troubleshooting.
version: 1.0.0
---

# Codex CLI

Use this skill to work with the official OpenAI Codex CLI using current official docs and repository structure. Focus on the official behavior first. If blog posts or community examples disagree with OpenAI docs or the `openai/codex` repository, trust the official sources.

## Goal

Help another agent install, configure, operate, and troubleshoot Codex CLI with accurate guidance on:

- installation and platform support
- authentication and credential storage
- config file locations, precedence, profiles, and exact option names
- interactive and non-interactive usage
- approvals and sandbox controls
- AGENTS.md, skills, and agent-related settings
- MCP and connector integration
- security-sensitive settings and risky modes
- common debugging and recovery workflows

## Start Here

1. Confirm whether the task is about local Codex CLI, Codex cloud/web, the VS Code extension, or a custom provider setup.
2. Prefer official documentation and the `openai/codex` repository.
3. When config details matter, load `references/config-options.md`.
4. When auth or provider setup matters, load `references/auth-and-providers.md`.
5. When usage patterns matter, load `references/usage-and-operations.md`.
6. When approvals, sandboxing, or risky settings matter, load `references/security-and-safety.md`.

## Installation Workflow

Use the official install path first:

```bash
npm i -g @openai/codex
```

Also recognize official alternatives:

- Homebrew installation
- GitHub release binaries
- DotSlash file from GitHub releases
- building from source from `openai/codex`

Use the official system requirements as the baseline:

- macOS 12+
- Ubuntu 20.04+ or Debian 10+
- Windows 11 via WSL2
- Git 2.23+ recommended
- 4 GB RAM minimum, 8 GB recommended

For Windows, prefer WSL2 guidance rather than claiming full native parity.

## Authentication Workflow

Support the two official auth paths:

1. ChatGPT sign-in
2. API key sign-in

Important auth facts:

- CLI and IDE extensions support ChatGPT sign-in or API-key-based access.
- Codex cloud requires ChatGPT sign-in.
- Credentials may be stored in `~/.codex/auth.json` or in the system keyring, depending on config.
- Treat `~/.codex/auth.json` as sensitive.

When headless auth is needed, prefer device auth first. If the environment is remote or headless, mention the documented fallback patterns only if necessary.

## Config File Workflow

Always cover config setting file options when the user asks about setup or configuration.

Primary config locations:

- user config: `~/.codex/config.toml`
- project config: `.codex/config.toml`
- admin-enforced config: `requirements.toml`

Behavior notes:

- project-scoped config loads only when the project is trusted
- profile-level settings override top-level settings
- exact keys and nested tables matter; avoid paraphrasing key names in code samples

When the user wants exact settings, pull from `references/config-options.md` and preserve official key names.

## Core Command Workflow

Interactive mode:

```bash
codex
codex "initial prompt"
```

Non-interactive mode:

```bash
codex exec "task"
```

Use non-interactive mode for automation, CI-oriented tasks, and repeatable scripts. Recognize related workflows such as resume, apply, login, logout, and MCP management.

If the user wants exact commands and patterns, load `references/usage-and-operations.md`.

## Approvals and Sandbox Workflow

Explain the separation clearly:

- `approval_policy` controls when the user is asked
- `sandbox_mode` controls what the agent can technically do

Official approval values:

- `untrusted`
- `on-failure`
- `on-request`
- `never`
- structured rejection config under `approval_policy = { reject = ... }`

Official sandbox values:

- `read-only`
- `workspace-write`
- `danger-full-access`

Treat dangerous bypass modes as exceptional. Recommend safer defaults first. For unattended automation, suggest read-only or tightly scoped workspace-write setups before any broader access.

## Skills, Agents, and AGENTS.md

Codex supports skills and AGENTS.md guidance. When this is part of the task:

- explain AGENTS.md scope and precedence carefully
- explain that config also contains `agents` settings and `skills` settings
- separate repository instructions from global/user instructions
- avoid mixing Claude-specific plugin semantics into Codex unless the user explicitly wants cross-tool compatibility

## MCP and Tool Integration

Codex can connect to MCP servers through config. For MCP work:

1. Identify whether the server is stdio or URL-based.
2. Use exact `mcp_servers.<name>` fields.
3. Cover auth fields only when needed.
4. Narrow exposed tools with `enabled_tools` or `disabled_tools` when safety matters.
5. Mention timeouts and required flags for production-like usage.

Prefer minimal, auditable examples.

## Provider and Model Setup

Codex supports custom providers through `model_providers` and profile selection. When configuring providers:

- define `model_provider`
- define `model`
- use exact provider keys under `[model_providers.<id>]`
- prefer `env_key` over embedding secrets in config
- set `wire_api = "responses"` when following official provider examples

When the task involves Azure or another compatible endpoint, keep the example aligned with official OpenAI docs and exact config keys.

## Troubleshooting Workflow

Check the following in order:

1. installation works: `codex --version`
2. auth is valid: login state, keyring/file storage, expected env vars
3. config path is correct and file syntax is valid TOML
4. profile selection is what the user expects
5. sandbox and approval settings match the intended workflow
6. MCP server starts and exposes expected tools
7. provider endpoint, model name, and auth method are aligned
8. logs exist where expected

Useful logging facts:

- TUI logs go to `~/.codex/log/codex-tui.log`
- `codex exec` defaults to inline error logging rather than separate log monitoring
- `RUST_LOG` can raise verbosity for debugging
- `-c log_dir=...` can redirect the log directory for a run

## Security Rules

Follow these rules when advising:

- never recommend committing `~/.codex/auth.json`
- prefer env vars or keyring-backed auth over raw secrets in files
- explain that `danger-full-access` and approval bypass increase risk materially
- mention that enabling network access increases prompt-injection exposure
- note protected paths like `.git`, `.agents`, and `.codex` when discussing safe defaults
- prefer least privilege and explicit scope

## Deliverable Patterns

When helping a user, provide one of these outputs:

### Minimal answer

- direct command(s)
- exact config snippet
- one-paragraph explanation

### Setup answer

- install command
- auth steps
- config file snippet
- verification command
- one troubleshooting note

### Deep config answer

- precedence explanation
- exact key names
- profile example
- provider example
- security caveats

## Reference Files

Load these as needed:

- `references/config-options.md` - exact config keys, tables, enums, and file behavior
- `references/auth-and-providers.md` - auth flows, auth storage, provider definitions, env keys
- `references/usage-and-operations.md` - commands, interactive usage, exec, resume, MCP operations, logs
- `references/security-and-safety.md` - approvals, sandboxing, risky modes, safe defaults, hardening notes

## Validation Checklist

Before finalizing an answer:

- use official OpenAI terminology
- include config file options if config/setup was requested
- preserve exact TOML key names in examples
- separate approval policy from sandbox mode
- avoid unsupported Windows claims; prefer WSL2 wording
- avoid leaking secrets into examples unless using placeholder values
- state uncertainty if a feature appears experimental or feature-flagged
