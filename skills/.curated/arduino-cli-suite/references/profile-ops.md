---
name: arduino-cli-profile-ops
description: Build profile management in sketch project files, including profile-scoped library sets. Use when requests involve `arduino-cli profile` commands (`create`, `set-default`, `lib add`, `lib remove`) or multi-target build profile workflows.
---

# Workflow
1. Define or update named profiles with explicit board and options.
2. Set a default profile only after validating primary workflows.
3. Manage per-profile libraries with add and remove operations.
4. Re-run compile using the target profile to confirm correctness.

# Command Coverage
- `arduino-cli profile create`
- `arduino-cli profile set-default <name>`
- `arduino-cli profile lib add <library> --profile <name>`
- `arduino-cli profile lib remove <library> --profile <name>`

# Defaults
- Keep profile names stable and environment-agnostic.
- Prefer profile-driven commands for multi-board projects.

# ICL Examples (Captured 2026-02-14)
1. Create a Nano old-bootloader profile and make it default.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data profile create --profile nano-old --fqbn arduino:avr:nano:cpu=atmega328old --set-default /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output:
```text
Project file created in: .../icl_suite_demo_v2/sketch.yaml
```
2. Add and remove profile-scoped libraries.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data profile lib add ArduinoJson@6.21.4 --profile uno-dev --sketch-path /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data profile lib remove ArduinoJson@6.21.4 --profile uno-dev --sketch-path /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed outputs confirmed add/remove actions against the selected profile.
