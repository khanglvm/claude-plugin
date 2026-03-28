# Codex Authentication and Providers

Use this file when the user asks about login, API keys, headless auth, or custom model providers.

## Official Authentication Modes

Codex supports two primary sign-in methods:

1. ChatGPT sign-in
2. API key sign-in

Important scope note:

- Codex cloud requires ChatGPT sign-in.
- CLI and IDE extensions support both ChatGPT sign-in and API key sign-in.

## Auth Storage

Credentials can be stored in one of these places:

- `~/.codex/auth.json`
- system keyring / credential store

Treat `~/.codex/auth.json` like a password file:

- do not commit it
- do not paste real contents into chat
- rotate secrets if exposed

## Relevant Config Keys

Useful auth-related config keys:

```toml
forced_login_method = "chatgpt"
forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"
cli_auth_credentials_store = "keyring"
```

Documented values and meanings:

- `forced_login_method`: force a login path such as `chatgpt` or `api`
- `forced_chatgpt_workspace_id`: pin a workspace where relevant
- `cli_auth_credentials_store`: choose how credentials are cached

Credential store enum values from the schema:

- `file`
- `keyring`
- `auto`
- `ephemeral`

Prefer `keyring` or `auto` for long-lived local setups when supported.

## Headless Authentication

When the user needs headless or remote auth, prefer the official device flow first:

```bash
codex login --device-auth
```

Documented fallback patterns:

- copy `~/.codex/auth.json` to the headless system if policy permits
- use SSH port forwarding for the browser callback path when necessary

Use the fallbacks only when device auth is not practical.

## API-Key-Centric Setups

For provider-backed auth without OpenAI login storage, prefer environment variables.

Example pattern:

```toml
model_provider = "azure"
model = "gpt-5-codex"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_RESOURCE.openai.azure.com/openai/v1"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"
```

Then set the environment variable outside the config file.

Guidance:

- prefer `env_key`
- avoid literal API keys in config
- avoid `experimental_bearer_token` unless programmatic constraints force it

## Custom Provider Fields

Official keys under `[model_providers.<id>]`:

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

## OpenAI-Auth-Capable Custom Providers

Some custom providers can request OpenAI authentication instead of direct env-key auth:

```toml
[model_providers.some_provider]
name = "Some Provider"
base_url = "https://provider.example/v1"
requires_openai_auth = true
```

Meaning:

- if `requires_openai_auth = true`, Codex can present login UI on first run
- the resulting preference and token/key are stored in auth storage
- if `requires_openai_auth = false`, the login screen is skipped and auth should come from `env_key` if required

## Header-Based Auth Options

When a provider needs extra headers, the official fields are:

- `http_headers` for literal header values
- `env_http_headers` for header values sourced from environment variables

Prefer `env_http_headers` for secrets.

Example:

```toml
[model_providers.proxy]
name = "Proxy"
base_url = "https://proxy.example/v1"
env_http_headers = { "X-API-Key" = "PROXY_API_KEY" }
wire_api = "responses"
```

## Good Guidance Patterns

### Good

- recommend `env_key`
- recommend keyring-backed storage where available
- use placeholder env var names in examples
- mention `auth.json` sensitivity

### Avoid

- embedding real API keys in config samples
- suggesting users commit `auth.json`
- implying cloud works with API key login when the official docs say ChatGPT sign-in is required

## Quick Troubleshooting

If authentication fails, check in this order:

1. installed version works: `codex --version`
2. login method matches the intended setup
3. credentials store is readable and not corrupted
4. env var named by `env_key` actually exists in the shell session
5. provider `base_url` ends with the expected API root
6. `wire_api` is set correctly
7. workspace or account restrictions are not forcing a different login path

## Safe Example Answer Template

```toml
forced_login_method = "api"
model_provider = "azure"
model = "gpt-5-codex"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_RESOURCE.openai.azure.com/openai/v1"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"
```

Then instruct the user to export `AZURE_OPENAI_API_KEY` in the shell rather than writing the secret into TOML.
