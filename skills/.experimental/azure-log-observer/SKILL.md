---
name: azure-log-observer
description: Read logs in real-time from Azure Web Apps to diagnose errors without leaving the development environment. Use when a user asks "why did the site crash?", "show me errors from app X on Azure", or needs to debug Azure Web App issues by viewing application logs.
metadata:
  short-description: Read Azure Web App logs for debugging
---

# Azure Log Observer

## Overview

This skill enables reading logs from Azure Web Apps in real-time to diagnose errors and debug issues. It uses the Azure CLI (`az`) to stream application logs directly to the development environment.

## Prerequisites

- Azure CLI (`az`) installed and authenticated on the host system
- Run `az login` to authenticate before using this skill
- The Azure Web App name and resource group name

## Quick Start

To get recent logs from an Azure Web App:

```bash
python "<path-to-skill>/scripts/get_azure_logs.py" --app-name "<app-name>" --resource-group "<resource-group>"
```

## Function Interface

The main function is `get_recent_logs(app_name: str, resource_group: str, lines: int = 50, filter_errors: bool = False, timeout: int = 30)`.

**Parameters:**
- `app_name`: Name of the Azure Web App
- `resource_group`: Name of the Azure resource group
- `lines`: Number of lines to capture (default: 50)
- `filter_errors`: If True, returns only lines containing "Exception", "Error", or "Critical" (default: False)
- `timeout`: Maximum seconds to run the log tail command (default: 30)

**Returns:** String containing the captured log lines

## Usage Examples

### Get last 50 lines of logs
```bash
python "<path-to-skill>/scripts/get_azure_logs.py" --app-name "my-webapp" --resource-group "my-resource-group"
```

### Get last 100 lines
```bash
python "<path-to-skill>/scripts/get_azure_logs.py" --app-name "my-webapp" --resource-group "my-resource-group" --lines 100
```

### Filter for errors only
```bash
python "<path-to-skill>/scripts/get_azure_logs.py" --app-name "my-webapp" --resource-group "my-resource-group" --filter-errors
```

### Custom timeout
```bash
python "<path-to-skill>/scripts/get_azure_logs.py" --app-name "my-webapp" --resource-group "my-resource-group" --timeout 60
```

## Workflow

1. **Verify Azure CLI authentication**
   - Run `az account show` to check if logged in
   - If not authenticated, prompt user to run `az login`

2. **Stream logs**
   - Execute `az webapp log tail --name <app-name> --resource-group <resource-group>`
   - Capture output for the specified duration or until the desired number of lines is reached
   - The `log tail` command streams continuously, so the script captures output for a limited time

3. **Filter (optional)**
   - If `filter_errors=True`, filter lines containing "Exception", "Error", or "Critical" (case-insensitive)

4. **Return results**
   - Return the captured log text to the agent for analysis

## Error Handling

- If Azure CLI is not authenticated, the script will fail with a clear error message
- If the Web App or resource group doesn't exist, Azure CLI will return an error
- If the log stream is empty or times out, the script returns what was captured

## Bundled Resources

### scripts/get_azure_logs.py

Executable script that connects to Azure Web App logs via Azure CLI and returns log output. Handles authentication checks, log streaming, filtering, and timeout management.

