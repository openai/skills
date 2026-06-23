#!/usr/bin/env bash
set -euo pipefail

ROSETTA=false
VERBOSE=false
SCHEME_FLAG=""
TEST_TYPE="all"
TEST_IDENTIFIER=""

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
        unit|ui|all|single)
            TEST_TYPE="$1"
            shift
            if [ "$TEST_TYPE" = "single" ] && [ $# -gt 0 ]; then
                TEST_IDENTIFIER="$1"
                shift
            fi
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 [--rosetta] [--verbose] [--scheme <name>] [unit|ui|all|single <target>]"
            exit 1
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

ALL_TARGETS=$(xcodebuild -list "$PROJECT_FLAG" "$PROJECT_FILE" 2>/dev/null | sed -n '/Targets:/,/^$/p' | tail -n +2 | sed 's/^[[:space:]]*//' | grep -v '^$')

UNIT_TARGETS=$(echo "$ALL_TARGETS" | grep -E "Tests$" | grep -v "UITests" || true)
UI_TARGETS=$(echo "$ALL_TARGETS" | grep -E "UITests$" || true)

extract_test_failure_details() {
    local test_name="$1"
    local full_output="$2"
    local xcresult_path="$3"
    local method_name=$(echo "$test_name" | sed 's/.*\.//' | sed 's/()$//')

    if [ "$VERBOSE" = true ]; then
        echo "[DEBUG] Extracting failure details for: $test_name" >&2
        echo "[DEBUG] Method name: $method_name" >&2
        echo "[DEBUG] xcresult path: $xcresult_path" >&2
    fi

    if [ -n "$xcresult_path" ] && [ -d "$xcresult_path" ] && command -v xcrun >/dev/null 2>&1; then
        if [ "$VERBOSE" = true ]; then
            echo "[DEBUG] Attempting xcresulttool extraction..." >&2
        fi

        local failure_details=$(xcrun xcresulttool get --format json --path "$xcresult_path" 2>/dev/null |
            jq -r --arg test_name "$test_name" '
            .. | objects |
            select(.testIdentifier? == $test_name or (.identifier? // .name? // .title?) | test($test_name)) |
            (.failureSummary? // .message? // .issueDocument?.message? // empty)' 2>/dev/null |
            grep -v "null" | head -5)

        if [ -n "$failure_details" ] && [ "$failure_details" != "null" ] && [ "$failure_details" != "" ]; then
            echo "$failure_details"
            return
        fi

        local issue_details=$(xcrun xcresulttool get --format json --path "$xcresult_path" 2>/dev/null |
            jq -r --arg test_name "$test_name" '
            .. | objects | select(.issues?) | .issues[] |
            select(.testCaseName? == $test_name or .message | contains($test_name)) |
            .message' 2>/dev/null | head -3)

        if [ -n "$issue_details" ] && [ "$issue_details" != "null" ] && [ "$issue_details" != "" ]; then
            echo "$issue_details"
            return
        fi
    fi

    if [ "$VERBOSE" = true ]; then
        echo "[DEBUG] Searching for error patterns in output..." >&2
    fi

    local swift_testing_errors=$(echo "$full_output" | grep -A 20 -B 5 "$method_name" |
        grep -E "(failed|error|assertion|expectation|Issue recorded|XCTAssert)" | head -5)

    if [ -n "$swift_testing_errors" ]; then
        echo "$swift_testing_errors"
        return
    fi

    local service_errors=$(echo "$full_output" |
        grep -E "\[$method_name\].*❌|\[$method_name\].*failed|❌.*$method_name|error.*$method_name" | head -3)

    if [ -n "$service_errors" ]; then
        echo "$service_errors"
        return
    fi

    local test_context=$(echo "$full_output" | grep -A 15 -B 5 "$test_name")
    local failure_indicators=$(echo "$test_context" | grep -E "(failed|error|assertion|❌|✗|Issue recorded)" | head -3)

    if [ -n "$failure_indicators" ]; then
        echo "$failure_indicators"
        return
    fi

    local nearby_errors=$(echo "$full_output" |
        grep -A 50 -B 10 "Test \"$method_name\"" |
        grep -E "(❌|failed|error|assertion)" | head -3)

    if [ -n "$nearby_errors" ]; then
        echo "$nearby_errors"
        return
    fi

    if [ "$VERBOSE" = true ]; then
        echo "Test failed - detailed context:"
        echo "$test_context" | head -10
        return
    fi

    echo "Test failed - run with --verbose for more details or individually: xcodebuild test -only-testing:\"$test_name\""
}

run_tests() {
    local target="$1"
    local name="$2"

    echo ""
    echo "🔍 Running $name ($target)..."

    mkdir -p .test_logs
    log_file=".test_logs/${target}_$(date +%Y%m%d_%H%M%S).log"

    echo "Running tests..."

    TEST_CMD=(xcodebuild test "$PROJECT_FLAG" "$PROJECT_FILE" -scheme "$SCHEME" -destination "$DESTINATION" -only-testing:"$target")

    if [ "$ROSETTA" = true ]; then
        TEST_CMD=(arch -x86_64 "${TEST_CMD[@]}")
    fi

    set +e
    output=$("${TEST_CMD[@]}" 2>&1 | tee "$log_file")
    local exit_code=$?
    set -e

    if [ "$VERBOSE" != true ]; then
        output=$(cat "$log_file")
    fi

    echo "Log saved to: $log_file"

    if echo "$output" | grep -q "BUILD FAILED\|fatal error:\|error:.*\.swift\|Build input file cannot be found\|Compilation failed"; then
        echo "💥 $name: Build failed"
        echo ""
        echo "🔥 Build Errors:"
        echo "$output" | grep -E "error:.*\.swift|fatal error:|Build input file cannot be found|.*\.swift:[0-9]+:[0-9]+: error:" | head -15 | sed 's/^/   /'
        echo ""
        echo "📋 Build Output (last 20 lines):"
        echo "$output" | tail -20 | sed 's/^/   /'
        return 1
    fi

    if echo "$output" | grep -q "Unable to find a destination\|does not contain a scheme"; then
        echo "💥 $name: Configuration error"
        echo ""
        echo "🔧 Configuration Issues:"
        echo "$output" | grep -E "Unable to find a destination|does not contain a scheme" | sed 's/^/   /'
        return 1
    fi

    if echo "$output" | grep -q "Test run with.*tests\? "; then
        swift_test_summary=$(echo "$output" | grep -E "Test run with [0-9]+ tests?" | tail -1)

        if [ -n "$swift_test_summary" ]; then
            if echo "$swift_test_summary" | grep -q "✔ Test run with.*passed"; then
                total=$(echo "$swift_test_summary" | grep -o '[0-9]\+ tests\?' | head -1 | grep -o '[0-9]\+' || echo "")
                if [ -n "$total" ]; then
                    passed="$total"
                    failed="0"
                else
                    passed="0"
                    failed="0"
                fi
            elif echo "$swift_test_summary" | grep -q "✘ Test run with.*failed"; then
                total=$(echo "$swift_test_summary" | grep -o '[0-9]\+ tests\?' | head -1 | grep -o '[0-9]\+' || echo "")
                issues=$(echo "$swift_test_summary" | grep -o 'with [0-9]\+ issues\?' | grep -o '[0-9]\+' || echo "")

                if [ -n "$total" ] && [ -n "$issues" ]; then
                    failed="$issues"
                    passed=$((total - issues))
                else
                    passed="0"
                    failed="0"
                fi
            else
                passed="0"
                failed="0"
            fi
        else
            passed="0"
            failed="0"
        fi

        filtered_output=$(echo "$output" | grep -E "(✔ Test.*passed|✗ Test.*failed|✘ Test.*failed|◇ Test.*started)")
    else
        filtered_output=$(echo "$output" | grep -iE "(Test Case|Test Suite.*failed|Test Suite.*passed)")
        passed=$(echo "$filtered_output" | grep -ic "Test Case.*passed" 2>/dev/null || echo "0")
        failed=$(echo "$filtered_output" | grep -ic "Test Case.*failed" 2>/dev/null || echo "0")
    fi

    passed=$(echo "$passed" | tr -d ' \t\n\r')
    failed=$(echo "$failed" | tr -d ' \t\n\r')

    if [ -z "$passed" ] || [ -z "$failed" ] || ! [[ "$passed" =~ ^[0-9]+$ ]] || ! [[ "$failed" =~ ^[0-9]+$ ]]; then
        echo "⚠️ $name: Failed to parse test results"
        echo ""
        echo "🔍 Debug Output (last 10 lines):"
        echo "$output" | tail -10 | sed 's/^/   /'
        return 1
    fi

    total=$((passed + failed))

    if [ "$failed" -eq 0 ] && [ "$total" -gt 0 ]; then
        echo "✅ $name: $total tests - $passed passed, $failed failed"
        return 0
    elif [ "$total" -eq 0 ]; then
        if [ "$exit_code" -eq 0 ] && echo "$output" | grep -q "\*\* TEST SUCCEEDED \*\*"; then
            echo "✅ $name: Tests passed (0 test cases counted — xcodebuild reported success)"
            return 0
        fi
        echo "⚠️ $name: No tests found or build failed"
        if [ "$exit_code" -ne 0 ]; then
            echo ""
            echo "🔍 Debug Information:"
            echo "$output" | grep -E "Testing failed|BUILD FAILED|No tests|error:|fatal error:" | head -10 | sed 's/^/   /'
            echo ""
            echo "🔍 Full Build Output (last 30 lines):"
            echo "$output" | tail -30 | sed 's/^/   /'
        fi
        return 1
    else
        echo "❌ $name: $total tests - $passed passed, $failed failed"
        echo ""

        if echo "$output" | grep -q "✗.*failed\|✘.*failed\|Failing tests:"; then
            echo "   Failed tests:"
            if echo "$filtered_output" | grep -q "✗.*failed\|✘.*failed"; then
                echo "$filtered_output" | grep -E "✗.*failed|✘.*failed" | sed 's/^/   - /'
            fi
            if echo "$output" | grep -q "Failing tests:"; then
                echo "$output" | sed -n '/Failing tests:/,/^$/p' | grep -E "^\s*[A-Za-z].*\(\)" | sed 's/^/   - /'
            fi
            echo ""
            echo "   Detailed Failures:"

            if echo "$output" | grep -q "Failing tests:"; then
                failed_tests=$(echo "$output" | sed -n '/Failing tests:/,/^$/p' | grep -E "^\s*[A-Za-z].*\(\)" | sed 's/^\s*//' | sed 's/()$//')
            else
                failed_tests=$(echo "$filtered_output" | grep -E "✗.*failed|✘.*failed" | sed 's/.*Test "//' | sed 's/" failed.*//')
            fi
        else
            echo "   Failed tests:"
            echo "$filtered_output" | grep "Test Case.*failed" | sed 's/.*Test Case /   - /' | sed 's/ failed.*//' | sed "s/'//g"
            echo ""
            echo "   Detailed Failures:"

            failed_tests=$(echo "$filtered_output" | grep "Test Case.*failed" | sed 's/.*Test Case //' | sed 's/ failed.*//' | sed "s/'//g")
        fi

        xcresult_path=$(echo "$output" | grep -o '/.*\.xcresult' | tail -1)

        while IFS= read -r test_name; do
            if [ -n "$test_name" ]; then
                echo "   📍 $test_name:"

                failure_details=$(extract_test_failure_details "$test_name" "$output" "$xcresult_path")

                if [ -n "$failure_details" ]; then
                    echo "$failure_details" | while IFS= read -r error_line; do
                        if [ -n "$error_line" ]; then
                            clean_line=$(echo "$error_line" | sed 's/^[0-9-]* [0-9:]* *[+-][0-9]* //' | sed 's/\[.*\] //' | sed 's/❌ //')

                            file_info=$(echo "$error_line" | grep -o '[^/]*\.swift:[0-9]*')

                            if [ -n "$file_info" ]; then
                                echo "      ❌ $clean_line ($file_info)"
                            else
                                echo "      ❌ $clean_line"
                            fi
                        fi
                    done
                else
                    echo "      ❌ Test failed - run with --verbose or check:"
                    echo "         xcodebuild test -only-testing:\"$test_name\" -enableCodeCoverage NO"
                fi
                echo ""
            fi
        done <<< "$failed_tests"

        return 1
    fi
}

overall_failures=0

if [ "$TEST_TYPE" = "single" ]; then
    if [ -z "$TEST_IDENTIFIER" ]; then
        echo "Error: single test type requires a test target name"
        echo "Usage: $0 single <target>"
        exit 1
    fi

    run_tests "$TEST_IDENTIFIER" "Single Test Target" || overall_failures=1
elif [ "$TEST_TYPE" = "unit" ]; then
    if [ -z "$UNIT_TARGETS" ]; then
        echo "⚠️ No unit test targets found"
        echo "   Available targets: $(echo "$ALL_TARGETS" | tr '\n' ' ')"
        exit 1
    fi

    while IFS= read -r target; do
        if [ -n "$target" ]; then
            run_tests "$target" "Unit Tests" || overall_failures=1
        fi
    done <<< "$UNIT_TARGETS"
elif [ "$TEST_TYPE" = "ui" ]; then
    if [ -z "$UI_TARGETS" ]; then
        echo "⚠️ No UI test targets found"
        echo "   Available targets: $(echo "$ALL_TARGETS" | tr '\n' ' ')"
        exit 1
    fi

    while IFS= read -r target; do
        if [ -n "$target" ]; then
            run_tests "$target" "UI Tests" || overall_failures=1
        fi
    done <<< "$UI_TARGETS"
else
    if [ -n "$UNIT_TARGETS" ]; then
        while IFS= read -r target; do
            if [ -n "$target" ]; then
                run_tests "$target" "Unit Tests" || overall_failures=1
            fi
        done <<< "$UNIT_TARGETS"
    fi

    if [ -n "$UI_TARGETS" ]; then
        while IFS= read -r target; do
            if [ -n "$target" ]; then
                run_tests "$target" "UI Tests" || overall_failures=1
            fi
        done <<< "$UI_TARGETS"
    fi

    if [ -z "$UNIT_TARGETS" ] && [ -z "$UI_TARGETS" ]; then
        echo "⚠️ No test targets found"
        echo "   Available targets: $(echo "$ALL_TARGETS" | tr '\n' ' ')"
        exit 1
    fi
fi

echo ""
echo "=================="
if [ $overall_failures -eq 0 ]; then
    echo "🎉 All tests passed!"
else
    echo "💥 Some tests failed!"
fi
echo "=================="

exit $overall_failures
