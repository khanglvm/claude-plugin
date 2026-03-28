# Remediation Workflow

1. Run dry-run scan:

```bash
scripts/repair_codex_skill_format.py --dry-run
```

2. Review planned changes:

- Normalized `name`
- Repaired `description`
- Removed/mapped unsupported keys
- Created/updated `agents/openai.yaml`

3. Apply fixes:

```bash
scripts/repair_codex_skill_format.py
```

4. Validate key skills with `quick_validate.py`.

5. Re-run dry-run to confirm idempotence (should report no changes).
