---
name: arduino-cli-daemon-grpc
description: Arduino CLI daemon and gRPC integration workflows for external tools and automation services. Use when requests involve `arduino-cli daemon`, gRPC transport behavior, debug tracing of RPC calls, or mapping CLI operations to RPC usage.
---

# Workflow
1. Start daemon with explicit port and message size constraints.
2. Enable debug tracing selectively to diagnose RPC behavior.
3. Restrict debug filters to relevant RPC method names.
4. Validate client connectivity before running long workflows.

# Command Coverage
- `arduino-cli daemon`

# Defaults
- Keep daemon on default port unless orchestration requires a custom port.
- Use `--debug-file` for persistent RPC tracing during integration tests.
- Keep daemon execution separate from direct CLI invocation in scripts.

# ICL Examples (Captured 2026-02-14)
1. Start daemon mode on an explicit port with logs enabled.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data daemon --port 50052 --log-level debug --log
```
Observed startup logs included:
```text
time="2026-02-14T18:47:46-06:00" level=info msg="arduino-cli version 1.4.1"
time="2026-02-14T18:47:46-06:00" level=info msg="Using config file: /tmp/arduino_cli_suite_icl_data/arduino-cli.yaml"
time="2026-02-14T18:47:46-06:00" level=info msg="Executing `arduino-cli daemon`"
```
2. Capture non-interactive daemon startup for transcript logging.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data daemon --port 50052
```
Observed as a valid launch path for daemon/gRPC workflows in capture logs.
