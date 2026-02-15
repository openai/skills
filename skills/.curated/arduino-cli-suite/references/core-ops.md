---
name: arduino-cli-core-ops
description: Platform core lifecycle management for install, search, update, and upgrade flows. Use when requests involve `arduino-cli core` commands (`download`, `install`, `list`, `search`, `uninstall`, `update-index`, `upgrade`) or platform/toolchain provisioning.
---

# Workflow
1. Refresh indexes before install and upgrade operations.
2. Search and pin target platform references explicitly.
3. Confirm installed versions after each mutation.
4. Remove unused cores only after dependency checks.

# Command Coverage
- `arduino-cli core update-index`
- `arduino-cli core search <query>`
- `arduino-cli core list`
- `arduino-cli core download <core[@version]>`
- `arduino-cli core install <core[@version]>`
- `arduino-cli core uninstall <core[@version]>`
- `arduino-cli core upgrade [<core>]`

# Defaults
- Add `--additional-urls` when third-party package indexes are required.
- Prefer explicit version pinning for reproducible builds.

# ICL Examples (Captured 2026-02-14)
1. Refresh indexes, search, install, and verify an AVR core.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data core update-index
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data core search arduino:avr
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data core install arduino:avr
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data core list
```
Observed output included:
```text
arduino:avr 1.8.7 Arduino AVR Boards
Platform arduino:avr@1.8.7 installed
```
2. Download core artifacts without changing active installation state.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data core download arduino:avr@1.8.7
```
Observed output downloaded `arduino:avr@1.8.7` and required tools (`avr-gcc`, `avrdude`, `arduinoOTA`).
