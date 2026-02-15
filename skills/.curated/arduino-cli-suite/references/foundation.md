---
name: arduino-cli-foundation
description: Baseline Arduino CLI command usage, output shaping, and shell integration. Use when requests involve general `arduino-cli` guidance, command discovery, shared global flags (`--json`, logging, config paths, additional URLs), or the commands `help`, `version`, and `completion`.
---

# Workflow
1. Detect whether the request needs human output or automation-safe output.
2. Apply global flags consistently: `--json`, `--config-file`, `--config-dir`, `--additional-urls`, and log flags.
3. Prefer short, copyable command examples with explicit flags.
4. Return verification commands after any change-oriented action.

# Command Coverage
- `arduino-cli help`
- `arduino-cli version`
- `arduino-cli completion bash|zsh|fish|powershell`

# Output Rules
- Use `--json` for pipelines and scripts.
- Use text output for interactive diagnosis.
- Increase to `--log-level debug` only when troubleshooting.

# ICL Examples (Captured 2026-02-14)
1. Command discovery and version check.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data version
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data help
```
Observed output included `Version: 1.4.1` and the top-level command set (`board`, `compile`, `upload`, `monitor`, `profile`, `sketch`).
2. Shell completion generation for automation shells.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data completion bash | sed -n '1,8p'
```
Observed output began with `# bash completion V2 for arduino-cli`.
