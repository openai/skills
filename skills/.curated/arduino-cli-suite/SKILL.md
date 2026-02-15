---
name: arduino-cli-suite
description: Unified orchestration for Arduino CLI tasks across discovery, setup, build, deployment, and diagnostics. Use when requests span multiple Arduino CLI domains or need an end-to-end workflow that coordinates board selection, core and library state, sketch operations, compile or upload, debug or monitor, configuration, maintenance, profiles, or daemon and gRPC integration.
---

# Workflow
1. Classify the request into one or more Arduino CLI domains.
2. Establish shared context first: board target, FQBN, port, sketch path, and output mode (`--json` vs text).
3. Route to the minimum set of domain modules needed for execution.
4. Execute in dependency order, then return verification commands and next checks.

# Domain Modules
- Foundation and global flags: `references/foundation.md`
- Board and port discovery: `references/board-ops.md`
- Core platform lifecycle: `references/core-ops.md`
- Library lifecycle: `references/lib-ops.md`
- Sketch creation and packaging: `references/sketch-ops.md`
- Build, upload, and bootloader: `references/build-upload.md`
- Debug and monitor sessions: `references/debug-monitor.md`
- Config initialization and edits: `references/config.md`
- Profile operations: `references/profile-ops.md`
- Environment maintenance and upgrades: `references/maintenance.md`
- Daemon and gRPC operation: `references/daemon-grpc.md`
- Ecosystem specifications and compliance: `references/ecosystem-specs.md`

# Routing Rules
- Prefer explicit `--fqbn` and `-p` when compiling, uploading, debugging, or monitoring.
- Run index refresh steps before install, search, upgrade, or outdated checks.
- Use profile-driven flows when a sketch project contains multiple targets.
- Use `--json` for automation output and text output for interactive diagnosis.
- Load only the domain modules needed for the current request.

# Common End-to-End Sequences
- Board bring-up: foundation -> board -> core -> lib -> compile -> upload -> monitor.
- Existing project recovery: config -> maintenance -> board -> compile -> upload -> debug.
- Multi-target project setup: sketch -> profile -> core -> lib -> compile (per profile).

# ICL Examples (Captured 2026-02-14)
1. End-to-end Nano workflow with explicit discovery, profile, build, and upload.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board attach -p /dev/cu.usbserial-3120 -b arduino:avr:nano:cpu=atmega328old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data profile create --profile nano-old --fqbn arduino:avr:nano:cpu=atmega328old --set-default /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data compile -b arduino:avr:nano:cpu=atmega328old --output-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/build_nano_old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data upload -p /dev/cu.usbserial-3120 -b arduino:avr:nano:cpu=atmega328old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed outcomes: successful attach, profile creation, compile memory report, and upload to `/dev/cu.usbserial-3120`.
2. Post-upload runtime observation.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data monitor -p /dev/cu.usbserial-3120 --config baudrate=9600
```
Observed live serial payload: `{"profile":"uno-dev","note":"icl example"}`.
