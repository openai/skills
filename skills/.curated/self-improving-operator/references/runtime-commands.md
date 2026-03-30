# Runtime Commands

Use `scripts/operator_runtime.py` to make the operator loop deterministic.

- `python3 scripts/operator_runtime.py bootstrap --repo /path/to/repo --goal "Ship onboarding reliably"`
- `python3 scripts/operator_runtime.py scan --repo /path/to/repo`
- `python3 scripts/operator_runtime.py next --repo /path/to/repo`
- `python3 scripts/operator_runtime.py ingest-plan --repo /path/to/repo --plan-file /path/to/plan.md`
- `python3 scripts/operator_runtime.py checkpoint --repo /path/to/repo --item-id <id> --summary "..." --verification-status passed --verification-summary "..." --publish-checkpoint`
- `python3 scripts/operator_runtime.py status --repo /path/to/repo`

## Notes

- `scan` refreshes backlog candidates from repo and GitHub signals.
- `next` selects and records the current highest-priority pending item.
- `checkpoint` writes a durable checkpoint and updates `next_action`.
- `ingest-plan` converts a broad plan into multiple executable backlog items.
