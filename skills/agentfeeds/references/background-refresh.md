# Background Refresh

Background refresh is required for normal Agent Feeds use. It keeps subscriptions warm between conversations so the agent can answer from local state instead of rerunning source-specific fetching, searching, querying, or processing on demand.

Check scheduler status:

```bash
python3 scripts/agentfeeds.py admin polling status --json
python3 scripts/agentfeeds.py streams health --json
```

Install or update background polling:

```bash
python3 scripts/agentfeeds.py admin polling install
```

Uninstall polling only when the user no longer wants ambient refresh:

```bash
python3 scripts/agentfeeds.py admin polling uninstall
```

On macOS, polling uses launchd. On Linux, FreeBSD, and WSL-style POSIX environments, polling uses a tagged crontab block. Native Windows polling is not currently supported. The runtime computes the shortest configured subscription interval and floors it at 5 minutes.

Agents should try to verify or install polling at session start. If the scheduler is unsupported or unavailable, report that Agent Feeds can still refresh explicitly but ambient refresh is degraded.

Use stream health to distinguish scheduler setup from per-stream fetch problems. `streams health --json` reports missing state, stale state, last success, last error, and consecutive failure count for each active subscription.

Explicit refresh remains useful for immediate freshness:

```bash
python3 scripts/agentfeeds.py refresh --stream <subscription-id>
python3 scripts/agentfeeds.py refresh --all
```
