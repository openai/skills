---
name: arduino-cli-ecosystem-specs
description: Authoring and compliance guidance for the Arduino CLI ecosystem specifications. Use when requests involve package index, platform, library format, pluggable discovery, or pluggable monitor specifications, including ecosystem-compatible hardware package design.
---

# Workflow
1. Identify which specification controls the requested artifact.
2. Validate field names and constraints against the relevant spec.
3. Keep examples minimal and aligned with current CLI behavior.
4. Call out compatibility implications across cores, tools, and monitors.

# Specification Coverage
- Package index JSON specification
- Platform specification
- Library specification
- Pluggable discovery specification
- Pluggable monitor specification

# Defaults
- Prefer spec-compliant examples over ad-hoc conventions.
- Keep references to required fields explicit and testable.

# ICL Examples (Captured 2026-02-14)
1. Validate FQBN and platform-id naming patterns across board catalog output.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board search nano
```
Observed mapping included `Arduino Nano -> arduino:avr:nano` with platform ID `arduino:avr`.
2. Inspect board option schema for processor variants.
```bash
arduino-cli --config-dir /tmp/arduino_cli_suite_icl_data board details -b arduino:avr:nano
```
Observed spec-like option key/value pairs including `Processor (cpu)` and `cpu=atmega328old`.
