---
name: arduino-cli-debug-monitor
description: Debug session setup and serial communication workflows for supported boards. Use when requests involve `arduino-cli debug`, `debug check`, or `monitor`, including interpreter modes, debug metadata, and monitor port configuration.
---

# Workflow
1. Check board and programmer debug support before session start.
2. Resolve and pass explicit debug artifacts or input directories.
3. Start debugger with the required interpreter mode.
4. Configure serial monitor settings before runtime observation.

# Command Coverage
- `arduino-cli debug`
- `arduino-cli debug check`
- `arduino-cli monitor`

# Defaults
- Use `debug --info` when metadata inspection is requested.
- Use `monitor --describe` before setting custom monitor configs.
- Add `--timestamp` in monitor mode for time-series debugging.

# ICL Examples (Captured 2026-02-14)
1. Inspect monitor capabilities on the connected Nano serial port.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data monitor --describe -p /dev/cu.usbserial-3120
```
Observed output listed settings for `baudrate`, `bits`, `parity`, `rts`, and `stop_bits`.
2. Stream live serial output from the sketch at 9600 baud.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data monitor -p /dev/cu.usbserial-3120 --config baudrate=9600
```
Observed sample line from live output:
```text
{"profile":"uno-dev","note":"icl example"}
```
3. Validate debugger support on AVR Nano target.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data debug check -b arduino:avr:nano:cpu=atmega328old /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/project/icl_suite_demo_v2
```
Observed output: `The given board/programmer configuration does NOT support debugging.`
