---
name: arduino-cli-board-ops
description: Board and port discovery workflows for selecting the right FQBN and attachment metadata. Use when requests involve `arduino-cli board` commands (`list`, `attach`, `details`, `listall`, `search`) or board identification and port mapping.
---

# Workflow
1. Start with hardware discovery (`board list`) and catalog ports.
2. Resolve or confirm FQBN using `board listall` or `board search`.
3. Use `board details` to inspect capabilities and options.
4. Use `board attach` to persist sketch-to-board association when needed.

# Command Coverage
- `arduino-cli board list`
- `arduino-cli board listall`
- `arduino-cli board search <query>`
- `arduino-cli board details -b <fqbn>`
- `arduino-cli board attach -p <port> -b <fqbn> <sketch>`

# Defaults
- Prefer explicit `-p` and `-b` flags in examples.
- Include protocol only when auto-detection fails.

# ICL Examples (Captured 2026-02-14)
1. Discover connected ports and candidate Nano board mappings.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board list
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board search nano
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board listall nano
```
Observed output included USB serial port `/dev/cu.usbserial-3120` and `Arduino Nano arduino:avr:nano`.
2. Inspect board options and attach sketch defaults for old bootloader.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board details -b arduino:avr:nano
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board attach -p /dev/cu.usbserial-3120 -b arduino:avr:nano:cpu=atmega328old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output showed `Processor` option `cpu=atmega328old` and set default port/FQBN for the sketch.
