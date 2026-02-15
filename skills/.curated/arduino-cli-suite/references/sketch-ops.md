---
name: arduino-cli-sketch-ops
description: Sketch project creation and packaging workflows with Arduino sketch structure expectations. Use when requests involve `arduino-cli sketch` commands (`new`, `archive`) or standardizing sketch folder layout and deliverable archives.
---

# Workflow
1. Create sketches with canonical naming and folder structure.
2. Keep source and metadata files in spec-compliant locations.
3. Package sketch deliverables with archive output when sharing.

# Command Coverage
- `arduino-cli sketch new <name>`
- `arduino-cli sketch archive <path>`

# Defaults
- Use `sketch new` over manual folder creation.
- Validate output archive contents before distribution.

# ICL Examples (Captured 2026-02-14)
1. Create a new sketch directory for integration testing.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data sketch new /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output:
```text
Sketch created in: /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
2. Archive an existing sketch for distribution.
```bash
arduino-cli --config-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/arduino_data sketch archive /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo
```
Observed exit status was successful (`EXIT: 0`) in the captured run.
