#!/usr/bin/env bash
set -euo pipefail

ROSETTA=false
VERBOSE=false
SCHEME_FLAG=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --rosetta)
            ROSETTA=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --scheme)
            SCHEME_FLAG="$2"
            shift 2
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

WORKSPACE=$(find . -maxdepth 1 -name "*.xcworkspace" ! -name "Pods.xcworkspace" | head -n 1)
PROJECT=$(find . -maxdepth 1 -name "*.xcodeproj" ! -name "Pods.xcodeproj" | head -n 1)

if [ -n "$WORKSPACE" ]; then
    PROJECT_FILE="$WORKSPACE"
    PROJECT_FLAG="-workspace"
    PROJECT_NAME=$(basename "$WORKSPACE" .xcworkspace)
elif [ -n "$PROJECT" ]; then
    PROJECT_FILE="$PROJECT"
    PROJECT_FLAG="-project"
    PROJECT_NAME=$(basename "$PROJECT" .xcodeproj)
else
    echo "Error: No .xcworkspace or .xcodeproj found in current directory"
    exit 1
fi

if [ -n "$SCHEME_FLAG" ]; then
    SCHEME="$SCHEME_FLAG"
elif [ -n "${SCHEME:-}" ]; then
    : # Use SCHEME from .env
else
    ALL_SCHEMES=$(xcodebuild -list "$PROJECT_FLAG" "$PROJECT_FILE" 2>/dev/null | sed -n '/Schemes:/,/^$/p' | tail -n +2 | sed 's/^[[:space:]]*//' | grep -v '^$')

    MATCHING_SCHEME=$(echo "$ALL_SCHEMES" | grep -i "^${PROJECT_NAME}$" || true)

    if [ -n "$MATCHING_SCHEME" ]; then
        SCHEME="$MATCHING_SCHEME"
    else
        FIRST_SCHEME=$(echo "$ALL_SCHEMES" | grep -v -i "pods" | head -n 1)
        if [ -n "$FIRST_SCHEME" ]; then
            SCHEME="$FIRST_SCHEME"
        else
            echo "Error: No scheme found. Please specify with --scheme or add SCHEME to .env"
            exit 1
        fi
    fi
fi

if [ -n "${DEVICE_ID:-}" ]; then
    DESTINATION="platform=iOS Simulator,id=$DEVICE_ID"
else
    SIMULATOR_JSON=$(xcrun simctl list devices available -j)
    DEVICE_ID=$(echo "$SIMULATOR_JSON" | python3 -c "
import sys, json
devices = json.load(sys.stdin)['devices']
for runtime, device_list in devices.items():
    if 'iOS' in runtime:
        for device in device_list:
            if 'iPhone' in device['name'] and device.get('isAvailable', False):
                print(device['udid'])
                sys.exit(0)
sys.exit(1)
" || true)

    if [ -z "$DEVICE_ID" ]; then
        echo "Error: No simulator found. Please add DEVICE_ID to .env file"
        echo "Run: xcrun simctl list devices available"
        exit 1
    fi

    DESTINATION="platform=iOS Simulator,id=$DEVICE_ID"
fi

if [ "$ROSETTA" = true ]; then
    DESTINATION="${DESTINATION},arch=x86_64"
fi

mkdir -p .build_logs
LOG_FILE=".build_logs/build_$(date +%Y%m%d_%H%M%S).log"

echo "Building $PROJECT_NAME (scheme: $SCHEME)..."
if [ "$ROSETTA" = true ]; then
    echo "Using Rosetta mode (x86_64)"
fi

if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
    BUILD_CMD=(xcodebuild "$PROJECT_FLAG" "$PROJECT_FILE" -scheme "$SCHEME" -destination "$DESTINATION" build "${EXTRA_ARGS[@]}")
else
    BUILD_CMD=(xcodebuild "$PROJECT_FLAG" "$PROJECT_FILE" -scheme "$SCHEME" -destination "$DESTINATION" build)
fi

if [ "$ROSETTA" = true ]; then
    BUILD_CMD=(arch -x86_64 "${BUILD_CMD[@]}")
fi

if [ "$VERBOSE" = true ]; then
    "${BUILD_CMD[@]}" 2>&1 | tee "$LOG_FILE"
    BUILD_STATUS=${PIPESTATUS[0]}
else
    "${BUILD_CMD[@]}" > "$LOG_FILE" 2>&1
    BUILD_STATUS=$?
fi

if [ $BUILD_STATUS -eq 0 ]; then
    echo "✓ Build succeeded"
    echo "Log: $LOG_FILE"
    exit 0
else
    echo "✗ Build failed"
    echo "Log: $LOG_FILE"
    echo ""
    echo "Errors:"
    grep -E "error:" "$LOG_FILE" || echo "No specific errors found in log"
    exit 1
fi
