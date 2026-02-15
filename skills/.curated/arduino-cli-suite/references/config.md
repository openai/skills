---
name: arduino-cli-config
description: Arduino CLI configuration initialization and mutation, including key inspection and precedence-safe edits. Use when requests involve `arduino-cli config` commands (`init`, `dump`, `get`, `set`, `add`, `remove`, `delete`) or debugging config-driven behavior.
---

# Workflow
1. Dump current configuration before mutating values.
2. Edit the narrowest possible key path.
3. Re-dump the affected key to confirm the write.
4. Explain precedence impacts from flags and environment variables.

# Command Coverage
- `arduino-cli config init`
- `arduino-cli config dump`
- `arduino-cli config get <key>`
- `arduino-cli config set <key> <value>`
- `arduino-cli config add <key> <value>`
- `arduino-cli config remove <key> <value>`
- `arduino-cli config delete <key>`

# Safety Rules
- Back up config files before broad deletes.
- Use `config get` after each targeted update.

# ICL Examples (Captured 2026-02-14)
1. Initialize and inspect config in an isolated workspace.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data config init --overwrite
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data config dump
```
Observed output included:
```text
Config file written to: /tmp/arduino_cli_suite_icl_data/arduino-cli.yaml
board_manager:
    additional_urls: []
```
2. Add and remove an additional board-manager URL safely.
```bash
arduino-cli --config-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/arduino_data config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
arduino-cli --config-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/arduino_data config get board_manager.additional_urls
arduino-cli --config-dir /Volumes/trent/Documents/Arduino/Arduino_CLI_Codex_Skills/tmp/icl_capture/arduino_data config remove board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
Observed `config get` first returned the URL, then returned `[]` after removal.
