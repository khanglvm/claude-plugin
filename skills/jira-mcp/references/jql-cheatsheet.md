# JQL Cheatsheet (Jira Server 7.x)

## Operators

| Operator | Use | Example |
|----------|-----|---------|
| `=` | Exact match | `project = "PROJ"` |
| `!=` | Not equal | `status != Done` |
| `~` | Contains (text) | `summary ~ "crash"` |
| `!~` | Does not contain | `description !~ "test"` |
| `IN` | Any of | `status IN ("Open", "In Progress")` |
| `NOT IN` | None of | `priority NOT IN (Low, Lowest)` |
| `IS EMPTY` | No value | `assignee IS EMPTY` |
| `IS NOT EMPTY` | Has value | `resolution IS NOT EMPTY` |
| `>` `<` `>=` `<=` | Comparison | `created >= -7d` |
| `WAS` | Historical value | `status WAS "Open"` |
| `CHANGED` | Field was modified | `status CHANGED` |

## Key Fields

| Field | Description | Note |
|-------|-------------|------|
| `project` | Project key | `project = XESM` |
| `status` | Exact workflow status name | Instance-specific (e.g. "Open", "In Review") |
| `statusCategory` | Broad category | Only: `"To Do"` / `"In Progress"` / `"Done"` |
| `issuetype` / `type` | Issue type | `Bug`, `Task`, `Story`, `Epic`, `Sub-task` |
| `assignee` | Assigned user | `assignee = currentUser()` |
| `reporter` | Created by | `reporter = "john.doe"` |
| `priority` | Priority | `High`, `Highest`, `Medium`, `Low`, `Lowest` |
| `resolution` | How resolved | `resolution = Fixed` |
| `created` | Creation date | `created >= 2026-01-01` |
| `updated` | Last update | `updated >= -1w` |
| `duedate` | Due date | `duedate < now()` |
| `labels` | Labels | `labels = "production"` |
| `component` | Project component | `component = "Backend"` |
| `fixVersion` | Target version | `fixVersion = "1.0.0"` |

## Functions

| Function | Description |
|----------|-------------|
| `currentUser()` | Logged-in user |
| `now()` | Current datetime |
| `startOfDay()` | Start of today |
| `startOfWeek()` | Start of this week |
| `startOfMonth()` | Start of this month |
| `endOfDay()` | End of today |
| `membersOf("group")` | Users in a group |

## Relative Dates

```
-1d   = 1 day ago       +1d  = 1 day from now
-7d   = 7 days ago      +1w  = 1 week from now
-1w   = 1 week ago
-30d  = 30 days ago
-1M   = 1 month ago
```

## Critical Distinction: status vs statusCategory

```
# WRONG - "To Do" is NOT an issue type
type = "To Do"  →  ERROR: value does not exist for field 'type'

# CORRECT - use statusCategory for broad status grouping
statusCategory = "To Do"          # all items not started
statusCategory = "In Progress"    # all active work
statusCategory = "Done"           # all completed

# CORRECT - use status for exact workflow state
status = "Open"
status IN ("Open", "Reopened", "Backlog")
```

## Status Category API Keys

| Category Name | API Key |
|---------------|---------|
| To Do | `new` |
| In Progress | `indeterminate` |
| Done | `done` |

## Proven Query Patterns

```jql
-- My open issues
assignee = currentUser() AND resolution IS EMPTY ORDER BY priority DESC

-- Todo in project
project = PROJ AND statusCategory = "To Do" ORDER BY priority DESC

-- Unassigned bugs
type = Bug AND assignee IS EMPTY AND resolution IS EMPTY ORDER BY created DESC

-- Updated this week
project = PROJ AND updated >= startOfWeek() ORDER BY updated DESC

-- High priority due soon
priority IN (High, Highest) AND duedate <= +7d AND resolution IS EMPTY

-- Recently created bugs
type = Bug AND created >= -7d ORDER BY created DESC

-- Team's open work
assignee IN membersOf("development-team") AND resolution IS EMPTY

-- Completed this week
assignee = currentUser() AND statusCategory = "Done" AND updated >= startOfWeek() ORDER BY updated DESC

-- Overdue
duedate < now() AND resolution IS EMPTY ORDER BY duedate ASC
```
