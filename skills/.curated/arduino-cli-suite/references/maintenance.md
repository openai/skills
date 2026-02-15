---
name: arduino-cli-maintenance
description: Environment maintenance and upgrade hygiene for Arduino CLI installations. Use when requests involve `arduino-cli cache clean`, `update`, `upgrade`, or `outdated`, including index refresh and upgrade drift checks.
---

# Workflow
1. Refresh indexes before evaluating outdated components.
2. Review outdated status before broad upgrades.
3. Perform upgrades with explicit pre/post script behavior when needed.
4. Clean manager caches when recovering from corrupted or stale downloads.

# Command Coverage
- `arduino-cli cache clean`
- `arduino-cli update`
- `arduino-cli upgrade`
- `arduino-cli outdated`

# Defaults
- Use `update --show-outdated` for quick health checks.
- Prefer targeted remediation before full-environment resets.

# ICL Examples (Captured 2026-02-14)
1. Detect outdated components and verify after refresh.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data outdated
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data update --show-outdated
```
Observed output consistently reported:
```text
ArduinoJson 6.21.4 installed, 7.4.2 latest
```
2. Clean cache before a fresh download cycle.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data cache clean
```
Observed successful completion (`EXIT: 0`) in the supplemental run.
