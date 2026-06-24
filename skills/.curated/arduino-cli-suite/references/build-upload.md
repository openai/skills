---
name: arduino-cli-build-upload
description: End-to-end build and deployment flows for firmware binaries and programmers. Use when requests involve `arduino-cli compile`, `upload`, or `burn-bootloader`, including build properties, artifacts, verification, and port/programmer selection.
---

# Workflow
1. Compile with explicit `--fqbn` and deterministic build flags.
2. Store or export binaries to predictable output locations.
3. Upload with explicit port or programmer settings.
4. Use verify and verbose flags only when needed for diagnosis.

# Command Coverage
- `arduino-cli compile`
- `arduino-cli upload`
- `arduino-cli burn-bootloader`

# Defaults
- Pass `--profile` for profile-managed projects.
- Prefer `--output-dir` or `--build-path` in automated pipelines.
- Use `--upload` on compile only when a combined flow is intended.

# ICL Examples (Captured 2026-02-14)
1. Compile for Nano old bootloader with explicit FQBN and output directory.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data compile -b arduino:avr:nano:cpu=atmega328old --output-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/build_nano_old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output:
```text
Sketch uses 5332 bytes (17%) of program storage space.
Global variables use 402 bytes (19%) of dynamic memory.
```
2. Upload compiled firmware to an explicitly selected port.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data upload -p /dev/cu.usbserial-3120 -b arduino:avr:nano:cpu=atmega328old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output confirmed target port: `New upload port: /dev/cu.usbserial-3120 (serial)`.
