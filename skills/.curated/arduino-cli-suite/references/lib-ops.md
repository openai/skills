---
name: arduino-cli-lib-ops
description: Library lifecycle and dependency workflows for Arduino projects. Use when requests involve `arduino-cli lib` commands (`search`, `install`, `list`, `deps`, `examples`, `download`, `uninstall`, `update-index`, `upgrade`) or library compatibility management.
---

# Workflow
1. Update indexes before new searches in stale environments.
2. Select library version constraints explicitly when reproducibility matters.
3. Inspect dependency status before removals.
4. Verify installed set after each operation.

# Command Coverage
- `arduino-cli lib update-index`
- `arduino-cli lib search <query>`
- `arduino-cli lib install <name[@version]>`
- `arduino-cli lib list`
- `arduino-cli lib deps <name>`
- `arduino-cli lib examples <name>`
- `arduino-cli lib download <name[@version]>`
- `arduino-cli lib uninstall <name>`
- `arduino-cli lib upgrade [<name>]`

# Defaults
- Prefer `--json` when dependency output is consumed by tooling.
- Use exact versions for CI and reproducible firmware pipelines.

# ICL Examples (Captured 2026-02-14)
1. Search, install, and verify a pinned library version.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib search ArduinoJson
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib install ArduinoJson@6.21.4
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib list
```
Observed output listed `ArduinoJson` with `Installed 6.21.4` and `Available 7.4.2`.
2. Inspect dependency and examples, then download the library archive.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib deps ArduinoJson
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib examples ArduinoJson
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data lib download ArduinoJson@6.21.4
```
Observed output included dependency mismatch signal (`7.4.2 required but 6.21.4 installed`) and example sketch paths.
