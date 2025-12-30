#!/usr/bin/env python3
"""
Azure Log Observer - Fetch logs from Azure Web Apps

This script reads logs from Azure Web Apps using the Azure CLI.
It can stream logs in real-time or capture a snapshot of recent logs.

Usage:
    get_azure_logs.py --app-name <name> --resource-group <group> [--lines N] [--filter-errors] [--timeout N]
"""

import argparse
import re
import subprocess
import sys
import threading
import time
from typing import Optional


def check_azure_auth() -> bool:
    """Check if Azure CLI is authenticated."""
    try:
        result = subprocess.run(
            ["az", "account", "show"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_recent_logs(
    app_name: str,
    resource_group: str,
    lines: int = 50,
    filter_errors: bool = False,
    timeout: int = 30,
) -> str:
    """
    Get recent logs from an Azure Web App.

    Args:
        app_name: Name of the Azure Web App
        resource_group: Name of the Azure resource group
        lines: Number of lines to capture (approximate)
        filter_errors: If True, return only error lines
        timeout: Maximum seconds to run the log tail command

    Returns:
        String containing the captured log lines
    """
    if not check_azure_auth():
        raise RuntimeError(
            "Azure CLI is not authenticated. Please run 'az login' first."
        )

    # Build the Azure CLI command
    cmd = [
        "az",
        "webapp",
        "log",
        "tail",
        "--name",
        app_name,
        "--resource-group",
        resource_group,
    ]

    # Use a list to collect output from the subprocess
    output_lines: list[str] = []
    process: Optional[subprocess.Popen] = None
    error_message: Optional[str] = None

    def read_output(pipe):
        """Read output from subprocess pipe."""
        nonlocal output_lines, error_message
        try:
            for line in iter(pipe.readline, ""):
                if line:
                    output_lines.append(line.rstrip("\n\r"))
        except Exception as e:
            error_message = f"Error reading output: {e}"

    try:
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
        )

        # Start thread to read stdout
        stdout_thread = threading.Thread(
            target=read_output, args=(process.stdout,), daemon=True
        )
        stdout_thread.start()

        # Wait for timeout or until we have enough lines
        start_time = time.time()
        while time.time() - start_time < timeout:
            if len(output_lines) >= lines:
                break
            if process.poll() is not None:
                # Process ended
                break
            time.sleep(0.1)

        # Terminate the process if still running
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        # Wait for output thread to finish reading
        stdout_thread.join(timeout=2)

        # Check for errors
        if process.returncode and process.returncode != -15:  # -15 is SIGTERM
            stderr_output = process.stderr.read() if process.stderr else ""
            if stderr_output:
                raise RuntimeError(
                    f"Azure CLI command failed: {stderr_output.strip()}"
                )

        # Get the captured output
        log_text = "\n".join(output_lines)

        # Apply error filter if requested
        if filter_errors:
            error_pattern = re.compile(
                r"(Exception|Error|Critical)", re.IGNORECASE
            )
            filtered_lines = [
                line for line in log_text.split("\n") if error_pattern.search(line)
            ]
            log_text = "\n".join(filtered_lines)

        # Return the last N lines if we captured more
        if log_text:
            all_lines = log_text.split("\n")
            if len(all_lines) > lines:
                log_text = "\n".join(all_lines[-lines:])

        return log_text

    except FileNotFoundError:
        raise RuntimeError(
            "Azure CLI (az) not found. Please install it from https://aka.ms/InstallAzureCLI"
        )
    except Exception as e:
        if error_message:
            raise RuntimeError(error_message) from e
        raise RuntimeError(f"Failed to fetch logs: {e}") from e
    finally:
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=2)
            except Exception:
                pass


def main() -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Fetch logs from Azure Web App",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--app-name",
        required=True,
        help="Name of the Azure Web App",
    )
    parser.add_argument(
        "--resource-group",
        required=True,
        help="Name of the Azure resource group",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=50,
        help="Number of lines to capture (approximate)",
    )
    parser.add_argument(
        "--filter-errors",
        action="store_true",
        help="Return only lines containing 'Exception', 'Error', or 'Critical'",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Maximum seconds to run the log tail command",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )

    args = parser.parse_args()

    try:
        logs = get_recent_logs(
            app_name=args.app_name,
            resource_group=args.resource_group,
            lines=args.lines,
            filter_errors=args.filter_errors,
            timeout=args.timeout,
        )

        if args.json:
            import json

            print(
                json.dumps(
                    {
                        "app_name": args.app_name,
                        "resource_group": args.resource_group,
                        "lines_captured": len(logs.split("\n")),
                        "logs": logs,
                    },
                    indent=2,
                )
            )
        else:
            if logs:
                print(logs)
            else:
                print(
                    "No logs captured. The app may not be generating logs, or the timeout was too short.",
                    file=sys.stderr,
                )
                return 1

        return 0

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

