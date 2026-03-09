# dockbuild

Run `sudo docker compose up -d --build` with full output piped to both stderr and
stdout, then report every issue, warning, error, or notice from the build process.

Note: Docker commands MAY require `sudo` if you are not in the `docker` group.

## Rules

1. **Report everything** - Surface ALL issues, warnings, errors, deprecation notices, update notices, and informational messages regardless of severity -- even cosmetic, expected, or harmless ones
2. **Full output capture** - Pipe build output through `tee /dev/stderr` so nothing is lost
3. **Read-only on spec system** - Never modify state.json, session specs, or task checklists
4. **Sudo required** - Prefix docker commands with `sudo`

## Steps

### 1. Run Docker Compose build

Execute:
```bash
sudo docker compose up -d --build 2>&1 | tee /dev/stderr
```

Capture the complete output.

### 2. Verify container status

Run `sudo docker compose ps` to confirm all containers are running.

### 3. Report results

Present:
- The full build output
- Final container status (name, state, ports)
- Every warning, error, deprecation notice, update notice, or informational message found in the output -- no matter the severity level

## Output

The user sees the full build output followed by a summary of container status and a
categorized list of every issue found (errors, warnings, deprecations, notices, etc.).
