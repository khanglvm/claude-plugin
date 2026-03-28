# Intent Detection Logic

Detect user intent from natural language and route to appropriate workflow.

## Detection Algorithm

```
FUNCTION detectMode(input):
  # Priority 1: Explicit flags (override all)
  IF input contains "--fast": RETURN "fast"
  IF input contains "--parallel": RETURN "parallel"
  IF input contains "--auto": RETURN "auto"
  IF input contains "--no-test": RETURN "no-test"

  # Priority 2: Plan path detection
  IF input matches path pattern (./plans/*, plan.md, phase-*.md):
    RETURN "code"

  # Priority 3: Keyword detection (case-insensitive)
  keywords = lowercase(input)

  IF keywords contains ["fast", "quick", "rapidly", "asap"]:
    RETURN "fast"

  IF keywords contains ["trust me", "auto", "yolo", "just do it"]:
    RETURN "auto"

  IF keywords contains ["no test", "skip test", "without test"]:
    RETURN "no-test"

  # Priority 4: Complexity detection
  features = extractFeatures(input)
  IF count(features) >= 3 OR keywords contains "parallel":
    RETURN "parallel"

  # Default
  RETURN "interactive"
```

## Feature Extraction

```
"implement auth, payments, and notifications" → ["auth", "payments", "notifications"]
"add login + signup + password reset"        → ["login", "signup", "password reset"]
"create dashboard with charts and tables"    → single feature (dashboard)
```

**Parallel trigger:** 3+ distinct features = parallel mode

## Mode Behaviors

| Mode | Skip Research | Skip Test | Review Gates | Auto-Approve | Parallel Exec |
|------|---------------|-----------|--------------|--------------|---------------|
| interactive | N | N | **Yes (stops)** | N | N |
| auto | N | N | **No (skips)** | Y (score>=9.5) | Y (all phases) |
| fast | Y | N | Yes (stops) | N | N |
| parallel | Optional | N | Yes (stops) | N | Y |
| no-test | N | Y | Yes (stops) | N | N |
| code | Y | N | Yes (stops) | Per plan | Per plan |

## Conflict Resolution

Priority order:
1. Explicit flags (`--fast`, `--auto`, etc.)
2. Path detection (plan files)
3. Keywords in text
4. Feature count analysis
5. Default (interactive)
