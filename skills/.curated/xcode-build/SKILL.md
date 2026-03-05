---
name: "xcode-build"
description: "Build and test iOS Xcode projects. Use when the user asks to build, compile, run tests, or verify an iOS project with xcodebuild. Supports xcworkspace/xcodeproj auto-detection, Rosetta mode (x86_64 simulator), Swift Testing and XCTest frameworks, unit and UI test filtering, and detailed failure reporting."
---

# iOS Build and Test

## Prerequisites

- Require macOS with Xcode installed. Check `xcode-select -p`. If missing, ask the user to install Xcode.
- Require `xcrun simctl` for simulator detection. Verify with `xcrun simctl list devices available`.

## Scripts

- **build.sh**: `<path-to-skill>/scripts/build.sh` -- Build an iOS project for simulator.
- **run_tests.sh**: `<path-to-skill>/scripts/run_tests.sh` -- Run unit, UI, or all tests.

## Building

```bash
# Auto-detect project and build
<path-to-skill>/scripts/build.sh

# Build with Rosetta mode (x86_64 simulator)
<path-to-skill>/scripts/build.sh --rosetta

# Build with verbose output
<path-to-skill>/scripts/build.sh --verbose

# Build specific scheme
<path-to-skill>/scripts/build.sh --scheme MyApp

# Pass extra xcodebuild flags
<path-to-skill>/scripts/build.sh -configuration Release CODE_SIGNING_ALLOWED=NO
```

## Testing

```bash
# Run all tests
<path-to-skill>/scripts/run_tests.sh

# Run only unit tests
<path-to-skill>/scripts/run_tests.sh unit

# Run only UI tests
<path-to-skill>/scripts/run_tests.sh ui

# Run specific test target
<path-to-skill>/scripts/run_tests.sh single MyAppTests

# Run with Rosetta mode
<path-to-skill>/scripts/run_tests.sh --rosetta

# Run with verbose output
<path-to-skill>/scripts/run_tests.sh --verbose unit

# Run specific scheme
<path-to-skill>/scripts/run_tests.sh --scheme MyApp unit
```

## Flags Reference

### Common Flags (both scripts)

| Flag | Description |
|---|---|
| `--rosetta` | Run on x86_64 simulator (adds `arch -x86_64` prefix) |
| `--verbose` or `-v` | Show full xcodebuild output (not just errors) |
| `--scheme <name>` | Override auto-detected scheme |

### Test Types (positional argument for run_tests.sh)

| Type | Description |
|---|---|
| `all` (default) | Run all test targets |
| `unit` | Targets ending in `Tests` (excluding `UITests`) |
| `ui` | Targets ending in `UITests` |
| `single <target>` | Run a specific test target by name |

## Auto-Detection

### Project Detection (priority order)

1. `*.xcworkspace` (excluding Pods.xcworkspace)
2. `*.xcodeproj` (excluding Pods.xcodeproj)

### Scheme Detection (priority order)

1. `--scheme` flag
2. `SCHEME` from `.env` file in the current directory
3. Scheme matching the project/workspace name
4. First non-Pods scheme from `xcodebuild -list`

### Simulator Detection (priority order)

1. `DEVICE_ID` from `.env` file
2. First available iPhone simulator from `xcrun simctl list devices available -j`

## .env Configuration

Both scripts source an optional `.env` file from the current directory:

```bash
DEVICE_ID=4019771F-38B3-4DA7-B4D7-B458E99A5394
SCHEME=MyApp
```

Find available device IDs with `xcrun simctl list devices available`.

## Log Files

- **Build logs**: `.build_logs/build_YYYYMMDD_HHMMSS.log`
- **Test logs**: `.test_logs/<target>_YYYYMMDD_HHMMSS.log`

On failure, the scripts print extracted errors. Read the full log file for complete diagnostics.

## Workflow

1. Navigate to the project root (where `.xcodeproj` or `.xcworkspace` is located).
2. Run the appropriate script with flags as needed.
3. If the build or test fails, read the log file to diagnose errors.
4. If the user needs Rosetta mode (for older dependencies or x86_64-only frameworks), add `--rosetta`.

## Troubleshooting

- **"No scheme found"**: Specify with `--scheme YourSchemeName` or add `SCHEME=...` to `.env`.
- **"No simulator found"**: Add `DEVICE_ID=...` to `.env`. Find IDs with `xcrun simctl list devices available`.
- **Build fails on Apple Silicon**: Use `--rosetta` for dependencies that require x86_64.
- **Multiple projects found**: Specify the scheme explicitly with `--scheme`.
