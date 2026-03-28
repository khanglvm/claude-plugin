# Codex Config Options

Use this file when the task needs exact config setting file coverage. Keep key names exact. Prefer these names over paraphrased blog terminology.

## Config File Locations

Primary official config locations:

- User config: `~/.codex/config.toml`
- Project config: `.codex/config.toml`
- Admin-enforced config: `requirements.toml`

Important behavior:

- Project-scoped config only loads when the project is trusted.
- Profile-level settings override top-level settings.
- MCP server definitions can be placed in `~/.codex/config.toml`.
- The generated schema lives at `codex-rs/core/config.schema.json` in the official repository.

## Core Top-Level Keys

Current schema-derived top-level keys include:

- `agents`
- `allow_login_shell`
- `analytics`
- `approval_policy`
- `apps`
- `audio`
- `background_terminal_max_timeout`
- `chatgpt_base_url`
- `check_for_update_on_startup`
- `cli_auth_credentials_store`
- `commit_attribution`
- `compact_prompt`
- `developer_instructions`
- `disable_paste_burst`
- `experimental_compact_prompt_file`
- `experimental_realtime_ws_backend_prompt`
- `experimental_realtime_ws_base_url`
- `experimental_use_freeform_apply_patch`
- `experimental_use_unified_exec_tool`
- `features`
- `feedback`
- `file_opener`
- `forced_chatgpt_workspace_id`
- `forced_login_method`
- `ghost_snapshot`
- `hide_agent_reasoning`
- `history`
- `instructions`
- `js_repl_node_module_dirs`
- `js_repl_node_path`
- `log_dir`
- `mcp_oauth_callback_port`
- `mcp_oauth_callback_url`
- `mcp_oauth_credentials_store`
- `mcp_servers`
- `memories`
- `model`
- `model_auto_compact_token_limit`
- `model_catalog_json`
- `model_context_window`
- `model_instructions_file`
- `model_provider`
- `model_providers`
- `model_reasoning_effort`
- `model_reasoning_summary`
- `model_supports_reasoning_summaries`
- `model_verbosity`
- `notice`
- `notify`
- `oss_provider`
- `otel`
- `permissions`
- `personality`
- `plan_mode_reasoning_effort`
- `profile`
- `profiles`
- `project_doc_fallback_filenames`
- `project_doc_max_bytes`
- `project_root_markers`
- `projects`
- `review_model`
- `sandbox_mode`
- `sandbox_workspace_write`
- `shell_environment_policy`
- `show_raw_agent_reasoning`
- `skills`
- `sqlite_home`
- `suppress_unstable_features_warning`
- `tool_output_token_limit`
- `tools`
- `tui`
- `web_search`
- `windows`
- `windows_wsl_setup_acknowledged`
- `zsh_path`

Do not dump all of these into user examples unless they are relevant.

## High-Value Settings To Know

### Model selection

```toml
model = "gpt-5-codex"
model_provider = "openai"
model_reasoning_effort = "medium"
model_reasoning_summary = "auto"
model_verbosity = "medium"
review_model = "gpt-5-codex"
plan_mode_reasoning_effort = "medium"
```

Enums:

- `model_reasoning_effort`: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`
- `model_reasoning_summary`: `auto`, `concise`, `detailed`, `none`
- `model_verbosity`: `low`, `medium`, `high`

### Approval and sandbox

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
writable_roots = []
exclude_slash_tmp = false
exclude_tmpdir_env_var = false
```

Approval values:

- `untrusted`
- `on-failure`
- `on-request`
- `never`
- or a structured reject object

Structured reject example:

```toml
approval_policy = { reject = { sandbox_approval = true, rules = false, mcp_elicitations = false } }
```

Sandbox values:

- `read-only`
- `workspace-write`
- `danger-full-access`

### Profiles

Use profiles for clean switching between setups.

```toml
profile = "safe"

[profiles.safe]
model = "gpt-5-codex"
approval_policy = "untrusted"
sandbox_mode = "read-only"

[profiles.auto]
model = "gpt-5-codex"
approval_policy = "never"
sandbox_mode = "workspace-write"
```

Profile properties can override many top-level keys, including:

- `approval_policy`
- `features`
- `model`
- `model_catalog_json`
- `model_instructions_file`
- `model_provider`
- `model_reasoning_effort`
- `model_reasoning_summary`
- `model_verbosity`
- `oss_provider`
- `personality`
- `plan_mode_reasoning_effort`
- `sandbox_mode`
- `web_search`
- `windows`
- `zsh_path`

### Custom providers

Official provider object keys under `[model_providers.<id>]`:

- `name`
- `base_url`
- `env_http_headers`
- `env_key`
- `env_key_instructions`
- `experimental_bearer_token`
- `http_headers`
- `query_params`
- `request_max_retries`
- `requires_openai_auth`
- `stream_idle_timeout_ms`
- `stream_max_retries`
- `supports_websockets`
- `wire_api`

Minimal example:

```toml
model_provider = "azure"
model = "gpt-5-codex"
model_reasoning_effort = "medium"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_RESOURCE.openai.azure.com/openai/v1"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"
```

Guidance:

- Prefer `env_key` over storing secrets in config.
- `wire_api = "responses"` is the official wire API enum shown in the schema.
- `requires_openai_auth = true` means Codex can drive an OpenAI login flow and store credentials in auth storage.

### MCP servers

Official MCP server keys under `[mcp_servers.<id>]`:

- `args`
- `bearer_token`
- `bearer_token_env_var`
- `command`
- `cwd`
- `disabled_tools`
- `enabled`
- `enabled_tools`
- `env`
- `env_http_headers`
- `env_vars`
- `http_headers`
- `oauth_resource`
- `required`
- `scopes`
- `startup_timeout_ms`
- `startup_timeout_sec`
- `tool_timeout_sec`
- `url`

Stdio example:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]
enabled = true
```

HTTP example:

```toml
[mcp_servers.remote]
url = "https://example.com/mcp"
bearer_token_env_var = "REMOTE_MCP_TOKEN"
enabled_tools = ["search", "read_doc"]
startup_timeout_ms = 10000
tool_timeout_sec = 60
```

### Shell environment policy

Official keys under `[shell_environment_policy]`:

- `exclude`
- `experimental_use_profile`
- `ignore_default_excludes`
- `include_only`
- `inherit`
- `set`

`inherit` values:

- `core`
- `all`
- `none`

Example:

```toml
[shell_environment_policy]
inherit = "core"
include_only = ["^PATH$", "^HOME$", "^PYTHON.*$"]
exclude = ["TOKEN", "SECRET", "KEY"]

[shell_environment_policy.set]
CI = "1"
```

### Agents

Official keys under `[agents]`:

- `job_max_runtime_seconds`
- `max_depth`
- `max_threads`

Additional nested role entries may also appear under `agents.<name>` with:

- `config_file`
- `description`

### Skills

Official `skills` config structure includes:

```toml
[[skills.config]]
path = "/absolute/path/to/skill/SKILL.md"
enabled = true
```

### Tools and web search

Tool toggles:

```toml
[tools]
view_image = true
web_search = true
```

Web search mode values:

- `disabled`
- `cached`
- `live`

Example:

```toml
web_search = "cached"
```

### Windows-specific settings

Official keys:

```toml
[windows]
sandbox = "unelevated"
```

Enum values:

- `elevated`
- `unelevated`

### Permissions network settings

Network permissions live under `[permissions.network]` with keys such as:

- `admin_url`
- `allow_local_binding`
- `allow_unix_sockets`
- `allow_upstream_proxy`
- `allowed_domains`
- `dangerously_allow_all_unix_sockets`
- `dangerously_allow_non_loopback_admin`
- `dangerously_allow_non_loopback_proxy`
- `denied_domains`
- `enable_socks5`
- `enable_socks5_udp`
- `enabled`
- `mode`
- `proxy_url`
- `socks_url`

Use these only when the task is explicitly about network policy.

### Notifications, logs, and state

Useful keys:

```toml
notify = ["terminal-notifier", "-title", "Codex", "done"]
log_dir = "~/.codex/log"
sqlite_home = "~/.codex/state"
```

Important behavior notes from official docs:

- TUI logs default to `~/.codex/log/codex-tui.log`.
- SQLite state lives under `sqlite_home` or `CODEX_SQLITE_HOME`.
- If `sqlite_home` and `CODEX_SQLITE_HOME` are unset, workspace-write sessions default to a temp directory; other modes default to `CODEX_HOME`.
- Notices are stored under `[notice]`.

### Feature flags

The schema exposes many feature flags under `[features]`, including:

- `apply_patch_freeform`
- `apps`
- `apps_mcp_gateway`
- `child_agents_md`
- `codex_git_commit`
- `collab`
- `collaboration_modes`
- `connectors`
- `default_mode_request_user_input`
- `elevated_windows_sandbox`
- `enable_experimental_windows_sandbox`
- `enable_request_compression`
- `experimental_use_freeform_apply_patch`
- `experimental_use_unified_exec_tool`
- `experimental_windows_sandbox`
- `include_apply_patch_tool`
- `js_repl`
- `js_repl_tools_only`
- `memories`
- `memory_tool`
- `multi_agent`
- `personality`
- `powershell_utf8`
- `prevent_idle_sleep`
- `realtime_conversation`
- `remote_models`
- `request_permissions`
- `request_rule`
- `responses_websockets`
- `responses_websockets_v2`
- `runtime_metrics`
- `search_tool`
- `shell_snapshot`
- `shell_tool`
- `shell_zsh_fork`
- `skill_env_var_dependency_prompt`
- `skill_mcp_dependency_install`
- `sqlite`
- `steer`
- `undo`
- `unified_exec`
- `use_linux_sandbox_bwrap`
- `voice_transcription`
- `web_search`
- `web_search_cached`
- `web_search_request`

Treat these as evolving and feature-flagged. Only recommend them when the user explicitly needs that area.

## Precedence Guidance

When explaining precedence, use this wording:

- User config lives at `~/.codex/config.toml`.
- Project config lives at `.codex/config.toml`.
- Project config loads only for trusted projects.
- Profile-level settings override top-level settings.
- Admin-enforced `requirements.toml` may constrain behavior.

## Safe Example Config

```toml
model = "gpt-5-codex"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "disabled"

[sandbox_workspace_write]
network_access = false

[tools]
view_image = true
web_search = false
```

## When Answering Users

- Keep examples minimal.
- Include only the keys relevant to the question.
- Preserve exact TOML key names.
- Mark feature flags and experimental keys clearly.
- Prefer env vars or keyring-backed auth over literal secrets.
