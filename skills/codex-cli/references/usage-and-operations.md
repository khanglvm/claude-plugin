# Codex Usage and Operations

Use this file when users ask how to run Codex in day-to-day workflows, automation, session recovery, MCP operation, or debugging.

## Installation and Verification

Canonical install command:

```bash
npm i -g @openai/codex
```

Verify installation:

```bash
codex --version
```

Other official install channels include Homebrew, GitHub release binaries, DotSlash release artifact, and building from source.

## Interactive Usage

Start TUI:

```bash
codex
```

Start TUI with initial prompt:

```bash
codex "explain this codebase"
```

## Non-Interactive Usage

Use `exec` mode for automation and scripts:

```bash
codex exec "implement tests for auth service"
```

Use `exec` when repeatability and machine-friendly execution matter.

## Session and Workflow Commands

Common command families to reference when relevant:

- `codex` (interactive)
- `codex exec` (non-interactive)
- `codex resume` (resume a previous session)
- `codex apply` (apply generated diff)
- `codex login` and `codex logout`
- `codex mcp ...` (MCP management)
- `codex app` (desktop app flow)

Keep examples minimal and task-specific.

## MCP Operations

When users want to use tools or external context, guide through MCP:

1. define server in config under `[mcp_servers.<name>]`
2. start Codex
3. validate that tools show up and are callable
4. narrow exposure with `enabled_tools` or `disabled_tools`

Example stdio config:

```toml
[mcp_servers.docs]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]
enabled = true
```

Example HTTP config:

```toml
[mcp_servers.remote]
url = "https://example.com/mcp"
bearer_token_env_var = "REMOTE_MCP_TOKEN"
required = true
enabled = true
```

## Apps and Connectors

From official docs:

- `/apps` lists available and installed apps in the Codex UI
- `$` in the composer inserts a ChatGPT connector

Only mention connector behavior if the user is in a context where those surfaces exist.

## Logs and Debugging

Important logging behavior from official install docs:

- TUI defaults to `RUST_LOG=codex_core=info,codex_tui=info,codex_rmcp_client=info`
- TUI logs are written to `~/.codex/log/codex-tui.log`
- `codex exec` defaults to `RUST_LOG=error` and logs inline

Useful commands:

```bash
tail -F ~/.codex/log/codex-tui.log
```

Override log directory for one run:

```bash
codex -c log_dir=./.codex-log
```

## Automation Patterns

### Pattern A: Scripted non-interactive task

```bash
codex exec "run lint, fix trivial issues, and summarize remaining failures"
```

### Pattern B: Profile-based run behavior

```toml
profile = "ci"

[profiles.ci]
approval_policy = "never"
sandbox_mode = "read-only"
```

Then run commands normally with that active profile.

### Pattern C: Repeatable provider config

Use one `model_provider` and switch profiles for safety level or verbosity rather than duplicating full provider blocks.

## AGENTS.md and Instruction Layers

Codex supports AGENTS.md guidance. Explain layering carefully:

- global/user AGENTS.md can hold personal defaults
- repository/root AGENTS.md can hold team defaults
- deeper folder AGENTS.md can hold subsystem-specific rules

If the `child_agents_md` feature is enabled, additional scope guidance can be emitted.

Do not conflate AGENTS.md with TOML config files.

## Troubleshooting by Symptom

### Symptom: command exists but behavior seems wrong

- check active profile
- inspect `approval_policy` and `sandbox_mode`
- verify project trust state for project config loading

### Symptom: model/provider errors

- check `model_provider` key matches a provider block
- verify `base_url` and `wire_api`
- verify env var named by `env_key`

### Symptom: no MCP tools visible

- check server block name and syntax
- check command/url reachability
- check `enabled`, `enabled_tools`, `disabled_tools`
- inspect logs for startup timeout or auth issues

### Symptom: auth loops

- check forced login method
- check credential store mode
- re-run `codex login`

## Output Templates

### Quick answer template

- exact command(s)
- exact config snippet
- one warning or caveat

### Setup template

1. install
2. login
3. minimal config
4. verify
5. fallback troubleshooting

### Ops template

- current state diagnosis
- shortest safe config change
- verification command
- rollback note

## Reminder

When the user asks for "all config and usage aspects," include:

- config file locations and precedence notes
- key config sections
- command usage for interactive and exec mode
- approval/sandbox controls
- auth and provider behavior
- MCP integration path
- logging and troubleshooting workflow
