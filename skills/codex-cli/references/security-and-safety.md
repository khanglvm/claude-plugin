# Codex Security and Safety

Use this file when users ask about approvals, sandboxing, bypass modes, trust boundaries, or secure defaults.

## Security Model

Codex applies two control layers:

1. sandbox mode controls what actions are technically possible
2. approval policy controls when user approval is required

Explain both explicitly in answers.

## Official Sandbox Modes

- `read-only`
- `workspace-write`
- `danger-full-access`

Guidance:

- start with `read-only` for analysis-only tasks
- use `workspace-write` for normal local coding with constrained write scope
- reserve `danger-full-access` for high-trust, controlled environments

## Official Approval Policies

- `untrusted`
- `on-failure` (marked deprecated in schema description)
- `on-request`
- `never`
- structured reject policy object

Structured reject object:

```toml
approval_policy = { reject = { sandbox_approval = true, rules = false, mcp_elicitations = false } }
```

This allows fine-grained auto-rejection of selected prompt categories.

## Safe Defaults and Risk Notes

From official security guidance:

- safer defaults are intended for version-controlled directories
- non-version-controlled contexts may default to stricter behavior
- network access is restricted by default in typical workspace-write setups
- protected paths like `.git`, `.agents`, and `.codex` are treated carefully

Risk escalators:

- approval bypass + unrestricted sandbox significantly increases blast radius
- network access can increase prompt-injection and data exfiltration risk
- broad MCP tool exposure can increase unintended side effects

## Sandbox Workspace Controls

Relevant keys under `[sandbox_workspace_write]`:

- `network_access`
- `writable_roots`
- `exclude_slash_tmp`
- `exclude_tmpdir_env_var`

Safer workspace-write example:

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/path/to/repo"]
```

## Shell Environment Hardening

Use `[shell_environment_policy]` to reduce sensitive variable leakage.

Keys:

- `inherit` (`core`, `all`, `none`)
- `include_only`
- `exclude`
- `set`
- `ignore_default_excludes`

Hardened example:

```toml
[shell_environment_policy]
inherit = "core"
include_only = ["^PATH$", "^HOME$", "^LANG$"]
exclude = ["TOKEN", "SECRET", "KEY"]
```

## MCP Hardening

For `[mcp_servers.<name>]`:

- set `enabled_tools` to an allowlist where possible
- use `disabled_tools` to block risky tools explicitly
- prefer `bearer_token_env_var` over literal `bearer_token`
- set startup and tool timeouts
- use `required` only where operationally necessary

Example:

```toml
[mcp_servers.docs]
url = "https://example.com/mcp"
enabled_tools = ["search_docs", "read_doc"]
disabled_tools = ["write_file"]
bearer_token_env_var = "DOCS_MCP_TOKEN"
startup_timeout_ms = 10000
tool_timeout_sec = 30
```

## Provider Hardening

For `[model_providers.<id>]`:

- prefer `env_key`
- use `env_http_headers` for secret header values
- avoid hardcoding tokens in `http_headers`
- scope retries and timeouts appropriately

## Recommended Baselines

### Baseline A: Read-only audit

```toml
sandbox_mode = "read-only"
approval_policy = "never"
web_search = "disabled"
```

Use for CI or analysis tasks where modification is not needed.

### Baseline B: Interactive dev

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = false
```

Use for most local coding tasks.

### Baseline C: Controlled auto-run

```toml
sandbox_mode = "workspace-write"
approval_policy = "never"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/path/to/repo"]
```

Use only in tightly scoped automation with clear repo boundaries.

## Unsafe Patterns To Avoid Recommending

- `danger-full-access` + broad network + `approval_policy = "never"` without explicit risk acknowledgment
- committing `~/.codex/auth.json`
- setting broad shell env inheritance when secrets are present
- exposing unrestricted MCP servers in untrusted contexts

## Security Review Checklist

Before finalizing security advice:

- separate approval from sandbox in explanation
- recommend least privilege first
- include one explicit risk statement for elevated modes
- avoid embedding secrets in examples
- include rollback path if changing existing config

## Suggested Rollback Pattern

1. backup existing `~/.codex/config.toml`
2. apply minimal change
3. validate behavior
4. revert if approvals/sandbox behavior is not as expected
