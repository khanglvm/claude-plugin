# Claude Code Plugin System: Comprehensive Technical Research

**Date**: March 27, 2026
**Status**: Complete
**Scope**: Plugin auto-update mechanisms, marketplace structure, selective installation, distribution models

---

## Executive Summary

Claude Code's plugin system has two distinct distribution models:
1. **Marketplace-based**: Centralized catalogs with individual plugin selection
2. **Skills-based**: Direct installation via `npx` with per-skill selectivity

The auto-update mechanism is **version-driven** (not commit-based), stored at `~/.claude/plugins/cache/`, and triggered by version bumps in `plugin.json` or `marketplace.json`. A single repository **can serve as a marketplace** hosting multiple installable plugins/skills with selective per-item installation.

---

## 1. Plugin Auto-Update Mechanism

### Version-Driven Caching

**How it works:**
- Plugins are **pinned to a specific version**, not git commits
- When installed, Claude Code copies the plugin to `~/.claude/plugins/cache/`
- All reads come from cache—changes to source repo have no effect until version bumps
- Cache structure: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`

### Update Triggering

**Requirement:** Version must be incremented in either:
- `plugin.json` (inside `.claude-plugin/plugin.json`)
- `marketplace.json` (in the `plugins[*].version` field for that plugin)

**Process:**
```bash
# User runs:
/plugin update plugin-name@marketplace-name

# Claude Code:
1. Fetches latest marketplace.json from source
2. Compares marketplace version vs cached plugin version
3. If version changed → pulls new version into ~/.claude/plugins/cache
4. If version unchanged → skips (treats as identical)
```

### Known Issue: Cache Not Invalidated

**Critical gap:** When running `/plugin update`, the marketplace git repo is updated but the local cache is NOT cleared/updated. Updated plugin files don't reach users until cache is manually deleted:
```bash
rm -rf ~/.claude/plugins/cache/
```

This is a documented bug; workaround is manual cache clearing.

### Auto-Update Configuration

Claude Code supports marketplace-level auto-update settings:

```bash
# Enable/disable auto-update for a marketplace
/plugin marketplace update marketplace-name
# UI: Marketplaces tab → select marketplace → toggle auto-update
```

**Default behavior:**
- Official Anthropic marketplaces: **auto-update enabled**
- Third-party/local dev marketplaces: **auto-update disabled**

Environment variables to control global auto-update:
```bash
export DISABLE_AUTOUPDATER=true          # Disable all auto-updates
export FORCE_AUTOUPDATE_PLUGINS=true     # Force plugin updates even if Claude Code updates disabled
```

---

## 2. Plugin Marketplace Structure

### marketplace.json Format & Location

**File location:** `.claude-plugin/marketplace.json` at repo root

**Required fields:**
```json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "What it does"
    }
  ]
}
```

**Optional metadata:**
```json
{
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"  // Base dir for relative paths
  }
}
```

### Plugin Source Types (5 options)

| Source Type | Config | Notes |
|---|---|---|
| **Relative path** | `"./plugins/my-plugin"` | Local in same repo; resolves relative to marketplace root |
| **GitHub** | `{"source": "github", "repo": "owner/repo", "ref": "v1.0", "sha": "abc..."}` | Can pin to branch/tag or exact commit SHA |
| **Git URL** | `{"source": "url", "url": "https://gitlab.com/...", "ref": "main", "sha": "..."}` | Any git host (GitLab, self-hosted, etc.) |
| **Git subdirectory** | `{"source": "git-subdir", "url": "...", "path": "tools/plugin"}` | Sparse clone for monorepos; supports `ref` + `sha` |
| **npm** | `{"source": "npm", "package": "@org/plugin", "version": "^2.0.0", "registry": "..."}` | Public or private npm registry |

**Key distinction:** Marketplace source (where to fetch `marketplace.json`) vs plugin source (where each plugin lives):
- Marketplace source: `ref` only (branch/tag)
- Plugin source: `ref` + `sha` (both branch/tag AND exact commit)

### Multi-Plugin Single Repo

**Yes, one repo can be a marketplace with multiple installable plugins:**

```json
{
  "name": "company-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "version": "1.0.0"
    },
    {
      "name": "deployment-tools",
      "source": "./plugins/deploy",
      "version": "2.1.0"
    },
    {
      "name": "github-integration",
      "source": {
        "source": "github",
        "repo": "company/separate-github-plugin"
      }
    }
  ]
}
```

**Directory structure:**
```
company-tools/
├── .claude-plugin/
│   └── marketplace.json       ← Main catalog
├── plugins/
│   ├── formatter/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   └── ...
│   └── deploy/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       └── ...
```

### Strict Mode

Controls whether `plugin.json` or `marketplace.json` is authoritative for component definitions:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "strict": true,    // plugin.json defines components (default)
      "strict": false    // marketplace.json defines components (full control)
    }
  ]
}
```

---

## 3. Selective Skill Installation

### Within a Marketplace Plugin

When users add a marketplace and browse the Discover tab, they **can select individual plugins**:

```bash
# User adds marketplace
/plugin marketplace add owner/repo

# User then selects which plugins to install
/plugin install formatter@company-tools          # Just formatter
/plugin install deploy@company-tools             # Just deploy
/plugin install formatter@company-tools deploy@company-tools  # Both
```

**Answer:** Installing a marketplace installs NO plugins automatically. Users **must explicitly** choose each plugin from the Discover tab or CLI.

### Within a Plugin's Skills

Once a plugin is installed, **Claude can individually invoke** skills it contains via `/skill-name`, and can be configured to not invoke them:

**At skill level** (`.claude/skills/my-skill/SKILL.md`):
```yaml
---
name: my-skill
disable-model-invocation: true    # Only user can invoke, not Claude
user-invocable: false             # Only Claude can invoke, not user
---
```

**At permission level** (`.claude/settings.json` or `/permissions`):
```json
{
  "deniedTools": ["Skill"],           // Block all skill invocation
  "allowedTools": ["Skill(deploy)"]   // Allow only /deploy
}
```

**Can disable individual skills post-installation:**
- Move from `~/.claude/skills/` to `~/.claude/skills-disabled/`
- Use community `skill-manager` plugin: `/plugin install skill-manager` → `/skill-manager enable|disable <name>`

**Current limitation:** No built-in CLI to toggle individual skills; requires filesystem manipulation or third-party plugin.

---

## 4. npx skills add vs claude plugin add

### Two Separate Ecosystems

| Aspect | npx skills add | /plugin marketplace add |
|---|---|---|
| **What it is** | Direct skill installation from GitHub repo | Marketplace-based plugin discovery |
| **Installation** | `npx skills add owner/repo` | `/plugin marketplace add owner/repo` then `/plugin install` |
| **What gets installed** | Individual skills (SKILL.md files) | Plugins (can contain skills + agents + hooks + MCP servers) |
| **Scope** | User-level, personal skills | User/project/local scopes |
| **Activation** | Invoked as `/skill-name` | Invoked as `/plugin-name:skill-name` |
| **Configuration** | Simple git URL | Full marketplace.json + versions |
| **Selective install** | Can install specific skills from repo path | Can install individual plugins from marketplace |

### npx skills add Examples

```bash
# Install entire skills repo
npx skills add alirezarezvani/claude-skills

# Install specific skill from nested path (anthropic style)
npx skills add anthropics/skills -- skill document-skills

# Install specific skill from community repo
npx skills add alirezarezvani/claude-skills/marketing-skill/content-creator
```

### /plugin marketplace add Examples

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Install specific plugin from that marketplace
/plugin install formatter@owner-repo
```

### Key Difference

- **Skills** = Direct, simpler, older distribution model (single .SKILL.md files + supporting files)
- **Plugins** = Formal plugin system with marketplace catalogs, versioning, components (skills + agents + hooks + MCP servers)

**Recommendation:** Use plugins for team/community distribution (version control, selectivity, formal packaging). Use skills for personal quick installs from GitHub.

---

## 5. Plugin Distribution Models

### Per-Skill Plugins vs. Multi-Skill Marketplaces

**Option A: One Plugin Per Skill** (granular control)
```
repo-my-formatter-plugin/
├── .claude-plugin/plugin.json
├── skills/formatter/SKILL.md
└── README.md

repo-my-deploy-plugin/
├── .claude-plugin/plugin.json
├── skills/deploy/SKILL.md
└── README.md
```

Users must add each repo separately:
```bash
/plugin marketplace add owner/formatter-plugin
/plugin marketplace add owner/deploy-plugin
/plugin install formatter@owner-formatter-plugin
/plugin install deploy@owner-deploy-plugin
```

**Option B: Multi-Skill Single Marketplace** (curated)
```
repo-company-tools/
├── .claude-plugin/marketplace.json
├── plugins/formatter/
│   ├── .claude-plugin/plugin.json
│   └── skills/formatter/SKILL.md
├── plugins/deploy/
│   ├── .claude-plugin/plugin.json
│   └── skills/deploy/SKILL.md
└── README.md
```

Users add once, choose individually:
```bash
/plugin marketplace add owner/company-tools
/plugin install formatter@company-tools
/plugin install deploy@company-tools
```

### Release Channel Support

Create separate marketplaces for "stable" vs "latest":

```json
// marketplace-stable.json
{
  "name": "stable-tools",
  "plugins": [{
    "name": "code-formatter",
    "source": {
      "source": "github",
      "repo": "acme-corp/code-formatter",
      "ref": "stable"
    }
  }]
}
```

```json
// marketplace-latest.json
{
  "name": "latest-tools",
  "plugins": [{
    "name": "code-formatter",
    "source": {
      "source": "github",
      "repo": "acme-corp/code-formatter",
      "ref": "latest"
    }
  }]
}
```

Assign via managed settings to different user groups (early-access vs stable).

---

## 6. Marketplace Integration Patterns

### Team Auto-Installation

Add to project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "formatter@company-tools": true,
    "deploy@company-tools": true
  }
}
```

When team members clone + trust the folder, Claude Code prompts them to install these marketplaces + plugins.

### Private Marketplace Authentication

For private repos, set environment variables before running Claude Code:
```bash
export GITHUB_TOKEN=ghp_xxx
export GITLAB_TOKEN=glp_xxx
export BITBUCKET_TOKEN=xxx

claude
```

### Container/CI Pre-Population

Set `CLAUDE_CODE_PLUGIN_SEED_DIR` to pre-populate plugins at build time:
```bash
export CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/plugins

# Directory structure:
/opt/plugins/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

Plugins from seed are read-only; auto-updates disabled.

---

## 7. Cache & File Resolution

### ~/.claude/plugins/ Directory Structure

```
~/.claude/plugins/
├── known_marketplaces.json         # Registered marketplaces
├── marketplaces/
│   └── my-marketplace/
│       └── .claude-plugin/marketplace.json
├── cache/
│   └── my-marketplace/
│       ├── formatter/
│       │   └── 1.0.0/              # Version subdirectory
│       │       ├── .claude-plugin/plugin.json
│       │       ├── skills/
│       │       └── ...
│       └── deploy/
│           └── 2.1.0/
└── data/                           # Persistent plugin data
    ├── formatter-my-marketplace/   # Survives updates
    └── deploy-my-marketplace/
```

### Plugin Copying Behavior

When installed from marketplace, plugins are **copied (not symlinked)** to `~/.claude/plugins/cache/`. This means:

**Files outside plugin directory are NOT copied:**
```
# Won't work after installation:
"../shared-utils/helper.js"        ❌ Parent directory not copied

# Workaround: use symlinks within plugin:
ln -s /path/to/shared-utils ./shared-utils
```

Symlinks **are followed** and content is copied.

### Persistent Data Directory

For files that survive plugin updates, use `${CLAUDE_PLUGIN_DATA}`:
- Resolves to: `~/.claude/plugins/data/{id}/` where `{id}` = plugin name with `-` substitutions
- Survives version changes
- Deleted when plugin uninstalled from all scopes

**Pattern:** Install dependencies once, reuse across updates
```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && npm install)"
      }
    ]
  }
}
```

---

## 8. Plugin Validation & Testing

### Validation Command

```bash
# Check manifest syntax + schema
claude plugin validate .

# Or within Claude Code:
/plugin validate .
```

Reports errors in:
- `plugin.json` JSON syntax
- YAML frontmatter (skills, agents, commands)
- `hooks/hooks.json` structure

### Test Locally

```bash
# Add local marketplace for testing
/plugin marketplace add ./path/to/marketplace

# Install test plugin
/plugin install test-plugin@marketplace-name

# Reload if changes made
/reload-plugins
```

---

## 9. Release Channels & Version Resolution

### Version Specification

Set version in **one place only** (not both):

```json
// In plugin.json (preferred for external plugins)
{
  "name": "my-plugin",
  "version": "2.1.0"
}

// In marketplace.json (preferred for relative-path plugins)
{
  "plugins": [{
    "name": "my-plugin",
    "source": "./my-plugin",
    "version": "2.1.0"
  }]
}
```

**Critical:** If set in both, `plugin.json` **silently wins**, marketplace version is ignored.

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0       → Initial stable release
2.0.0       → Breaking changes
2.1.0       → New features (backward-compatible)
2.1.1       → Bug fix
2.0.0-beta.1 → Pre-release for testing
```

**Without version bump, users don't see updates** (cache comparison is exact match).

---

## 10. Managed Settings & Restrictions

### Strict Marketplace Allowlist

Organizations can restrict which marketplaces users can add via `managed-settings.json`:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    }
  ]
}
```

Options:
- Undefined (default): no restrictions
- Empty array `[]`: complete lockdown
- List: only these marketplaces allowed

---

## 11. Practical Examples

### Example 1: Single-Purpose Marketplace (recommended for teams)

**Repository structure:**
```
company-tools/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── code-review/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/quality-review/SKILL.md
│   ├── deployment/
│   │   ├── .claude-plugin/plugin.json
│   │   └── commands/deploy.md
│   └── git-tools/
│       ├── .claude-plugin/plugin.json
│       └── agents/commit-writer.md
└── README.md
```

**marketplace.json:**
```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "plugins": [
    {
      "name": "code-review",
      "source": "./plugins/code-review",
      "version": "1.2.0",
      "description": "Code review automation and quality checks"
    },
    {
      "name": "deployment",
      "source": "./plugins/deployment",
      "version": "2.0.0",
      "description": "Deployment automation tools"
    },
    {
      "name": "git-tools",
      "source": "./plugins/git-tools",
      "version": "1.0.0",
      "description": "Git workflow utilities"
    }
  ]
}
```

**User workflow:**
```bash
/plugin marketplace add your-org/company-tools
/plugin install code-review@company-tools
/plugin install deployment@company-tools
# git-tools not installed unless explicitly chosen
```

### Example 2: Cross-Repo Marketplace

```json
{
  "name": "multi-vendor-tools",
  "plugins": [
    {
      "name": "formatter",
      "source": {
        "source": "github",
        "repo": "prettier/prettier-claude-plugin"
      },
      "version": "1.5.0"
    },
    {
      "name": "local-formatter",
      "source": "./plugins/custom-formatter",
      "version": "1.0.0"
    },
    {
      "name": "database-tools",
      "source": {
        "source": "git-subdir",
        "url": "https://github.com/company/monorepo",
        "path": "tools/claude-db-plugin",
        "ref": "main"
      },
      "version": "2.1.0"
    }
  ]
}
```

---

## 12. Known Issues & Workarounds

| Issue | Root Cause | Workaround |
|---|---|---|
| **Plugin cache not cleared on update** | Bug in cache invalidation | `rm -rf ~/.claude/plugins/cache/` before re-installing |
| **CLAUDE_PLUGIN_ROOT points to stale version** | Cache not invalidated after `/plugin update` | Manual cache clear |
| **Version ignored from marketplace.json** | `plugin.json` version takes precedence silently | Set version in only one place |
| **Large git repos timeout** | Default 120s timeout | `export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000` |
| **Relative paths fail in URL-based marketplaces** | URL marketplace only downloads .json, not files | Use Git-based marketplace or external sources (GitHub, npm) |
| **Path not found after installation** | Plugins copied, parent dirs not included | Use symlinks within plugin, restructure directories |

---

## 13. Decision Matrix: Distribution Strategy

Choose based on your use case:

| Scenario | Model | Setup |
|---|---|---|
| **Team wants curated set of tools** | Multi-skill single marketplace | 1 repo with marketplace.json + plugin subdirs |
| **Distribute one skill widely** | Single-plugin marketplace | 1 repo per plugin + marketplace.json |
| **Rapid iteration, personal use** | npx skills add | Direct GitHub repo with skills/ |
| **Org enforcement + versioning** | Managed settings + marketplace | Central marketplace.json + managed-settings.json per group |
| **Open-source community** | Multi-skill marketplace + registry | Host marketplace.json on GitHub, register with Anthropic |

---

## Unresolved Questions

1. **Cost attribution:** How are plugin installation costs tracked across distributed/managed deployments?
2. **Streaming updates:** Can marketplace.json be streamed/paginated for large catalogs (1000+ plugins)?
3. **DAG dependency resolution:** Can plugins declare dependencies on other plugins with version constraints? How are conflicts resolved?
4. **Rollback mechanism:** After auto-update, can users roll back to a previous version?
5. **Split depth:** Can plugins in git-subdir sources be nested 5+ levels deep, or are there practical limits?
6. **Local-only plugin discovery:** When using `CLAUDE_CODE_PLUGIN_SEED_DIR`, can plugins reference MCP servers outside the seed?
7. **Cache retention policy:** How long are unused cached versions retained? Manual cleanup only?
8. **Multi-scope plugin conflicts:** If plugin X is installed in both user and project scopes with different versions, which wins?
9. **Marketplace schema versioning:** What happens if marketplace.json is in an older schema version?
10. **Private npm registry auth:** Does npm registry token come from .npmrc or must it be injected via env var?

---

## Sources

- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)
- [Plugin update detection and upgrade workflow — GitHub Issue #31462](https://github.com/anthropics/claude-code/issues/31462)
- [Plugin cache issues — GitHub Issues #15642, #29074, #17361, #14061](https://github.com/anthropics/claude-code/issues)

