# LLM Router CLI & Config Reference

## Full CLI Commands

### Gateway Management
```bash
llr start                    # Start on 127.0.0.1:8376
llr stop                     # Stop running gateway
llr reload                   # Hot-reload config without restart
llr reclaim                  # Force-free port if blocked
llr update                   # Update to latest version
```

### Web UI
```bash
llr                          # Open Web UI (default port 9090)
llr web --port=9090          # Specify port
llr web --open=false         # Don't auto-open browser
```

### Provider Management
```bash
# Discover models from a provider endpoint
llr config --operation=discover-provider-models \
  --endpoints=https://api.example.com/v1 \
  --api-key=sk-...

# Test provider connectivity
llr config --operation=test-provider \
  --endpoints=https://api.example.com/v1 \
  --api-key=sk-... \
  --models=gpt-4o,gpt-4o-mini

# Add/update provider
llr config --operation=upsert-provider \
  --provider-id=openrouter \
  --name="OpenRouter" \
  --base-url=https://openrouter.ai/api/v1 \
  --api-key=sk-... \
  --models=gpt-4o-mini,gpt-4o
```

### Model Alias Management
```bash
# Create/update alias
llr config --operation=upsert-model-alias \
  --alias-id=chat.default \
  --strategy=auto \
  --targets=openrouter/gpt-4o-mini@3,anthropic/claude-3-5-haiku@2
```

### Rate Limits
```bash
llr config --operation=set-provider-rate-limits \
  --provider-id=openrouter \
  --bucket-name="Monthly cap" \
  --bucket-models=all \
  --bucket-requests=20000 \
  --bucket-window=month:1
```

### Coding Tool Integration
```bash
# Codex CLI routing
llr config --operation=set-codex-cli-routing \
  --enabled=true --default-model=chat.default

# Claude Code routing
llr config --operation=set-claude-code-routing \
  --enabled=true \
  --primary-model=chat.default \
  --default-haiku-model=chat.fast

# AMP client routing
llr config --operation=set-amp-client-routing \
  --enabled=true --amp-client-settings-scope=workspace
```

### Subscription Providers (OAuth)
```bash
# Add subscription provider
llr config --operation=upsert-provider \
  --provider-id=chatgpt \
  --name="ChatGPT Sub" \
  --type=subscription \
  --subscription-type=chatgpt-codex \
  --subscription-profile=default

# Login
llr subscription login --subscription-type=chatgpt-codex --profile=default
llr subscription login --subscription-type=claude-code --profile=default
llr subscription status
```

### Deployment
```bash
llr deploy                              # Deploy to Cloudflare Workers
llr deploy --dry-run=true               # Preview only
llr deploy --generate-master-key=true   # Generate key during deploy
llr worker-key --generate-master-key=true  # Rotate worker key
```

### Status & Diagnostics
```bash
llr config --operation=validate        # Validate config
llr config --operation=snapshot        # Full config + state dump
llr config --operation=tool-status     # Coding tool integration status
llr ai-help                            # Agent-oriented operating guide
```

## Config JSON Schema (v2)

```json
{
  "version": 2,
  "defaultModel": "chat.default",
  "providers": [
    {
      "id": "provider-id",
      "name": "Display Name",
      "type": "standard|subscription",
      "baseUrl": "https://api.provider.com/v1",
      "format": "openai|claude",
      "apiKey": "sk-...",
      "models": [
        { "id": "model-name" }
      ],
      "rateLimits": [
        {
          "id": "bucket-id",
          "name": "Bucket Name",
          "models": ["all"],
          "requests": 20000,
          "window": { "unit": "month", "size": 1 }
        }
      ]
    }
  ],
  "modelAliases": {
    "alias.name": {
      "strategy": "auto|ordered|round-robin|weighted-rr|quota-aware-weighted-rr",
      "targets": [
        { "ref": "provider-id/model-id", "weight": 1 }
      ],
      "fallbackTargets": [
        { "ref": "provider-id/model-id" }
      ]
    }
  },
  "masterKey": "optional-auth-key",
  "amp": {
    "preset": "builtin",
    "defaultRoute": "chat.default",
    "routes": { "smart": "chat.smart", "rush": "chat.fast" },
    "restrictManagementToLocalhost": true
  }
}
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `LLM_ROUTER_PORT` | 8376 | Local server port |
| `LLM_ROUTER_HOST` | 127.0.0.1 | Bind address |
| `LLM_ROUTER_MAX_REQUEST_BODY_BYTES` | 1MB (8MB for /responses) | Max request size |
| `LLM_ROUTER_UPSTREAM_TIMEOUT_MS` | 120000 | Provider call timeout |
| `LLM_ROUTER_CONFIG_JSON` | — | Worker config (inline JSON) |
| `CLOUDFLARE_API_TOKEN` | — | For deployment |

## Fallback & Retry Behavior

| Error | Action |
|-------|--------|
| 429 Rate Limited | Retry with backoff + Retry-After |
| 402 Billing | Circuit break (5min cooldown) |
| 401/403 Auth | Skip candidate |
| Context exceeded | Filter candidate |
| Timeout/Network | Retry with backoff |
| 5xx Server | Retry with backoff |

## API Endpoints Summary

| Endpoint | Format |
|----------|--------|
| `POST /v1/chat/completions` | OpenAI input |
| `POST /v1/messages` | Claude input |
| `POST /v1/responses` | Codex Responses API |
| `POST /` | Auto-detect |
| `GET /v1/models` | List models |
| `POST /amp/chat/completions` | AMP routing |
