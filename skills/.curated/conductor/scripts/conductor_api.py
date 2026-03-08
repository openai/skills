#!/usr/bin/env python3
"""Conductor REST API fallback — stdlib only, no third-party packages.

Use when the `conductor` CLI is not installed.
Requires CONDUCTOR_SERVER_URL env var. CONDUCTOR_AUTH_TOKEN is optional.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_config():
    base = os.environ.get("CONDUCTOR_SERVER_URL", "").rstrip("/")
    if not base:
        print("Error: CONDUCTOR_SERVER_URL is not set.", file=sys.stderr)
        sys.exit(1)
    token = os.environ.get("CONDUCTOR_AUTH_TOKEN", "")
    return base, token


def build_url(base, path, params=None):
    url = f"{base}{path}"
    if params:
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        if qs:
            url = f"{url}?{qs}"
    return url


def request_json(url, token, method="GET", body=None, expect_json=True):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["X-Authorization"] = token

    data = None
    if body is not None:
        data = json.dumps(body).encode() if not isinstance(body, bytes) else body

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    retries = 3
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                if not raw:
                    return None
                if expect_json:
                    return json.loads(raw)
                return raw
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            body_text = ""
            try:
                body_text = e.read().decode()
            except Exception:
                pass
            print(f"HTTP {e.code}: {e.reason}\n{body_text}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"Connection error: {e.reason}", file=sys.stderr)
            sys.exit(1)


def output(data):
    print(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# Workflow metadata handlers
# ---------------------------------------------------------------------------

def handle_list_workflows(args):
    base, token = get_config()
    url = build_url(base, "/metadata/workflow")
    result = request_json(url, token)
    output(result)


def handle_get_workflow(args):
    base, token = get_config()
    params = {}
    if args.version:
        params["version"] = args.version
    url = build_url(base, f"/metadata/workflow/{urllib.parse.quote(args.name)}", params)
    result = request_json(url, token)
    output(result)


def handle_create_workflow(args):
    base, token = get_config()
    with open(args.file) as f:
        body = json.load(f)
    url = build_url(base, "/metadata/workflow")
    result = request_json(url, token, method="POST", body=body)
    if result:
        output(result)
    else:
        print("Workflow created successfully.")


def handle_update_workflow(args):
    base, token = get_config()
    with open(args.file) as f:
        body = json.load(f)
    # Update expects an array
    if isinstance(body, dict):
        body = [body]
    url = build_url(base, "/metadata/workflow")
    result = request_json(url, token, method="PUT", body=body)
    if result:
        output(result)
    else:
        print("Workflow updated successfully.")


def handle_delete_workflow(args):
    base, token = get_config()
    url = build_url(base, f"/metadata/workflow/{urllib.parse.quote(args.name)}/{args.version}")
    request_json(url, token, method="DELETE", expect_json=False)
    print(f"Workflow {args.name} v{args.version} deleted.")


# ---------------------------------------------------------------------------
# Workflow execution handlers
# ---------------------------------------------------------------------------

def handle_start_workflow(args):
    base, token = get_config()
    body = {"name": args.name}
    if args.version:
        body["version"] = int(args.version)
    if args.correlation_id:
        body["correlationId"] = args.correlation_id
    if args.input:
        body["input"] = json.loads(args.input)
    elif args.input_file:
        with open(args.input_file) as f:
            body["input"] = json.load(f)

    url = build_url(base, "/workflow")
    result = request_json(url, token, method="POST", body=body, expect_json=False)
    # Start returns the workflow ID as plain text
    wf_id = result.strip().strip('"') if result else ""
    print(json.dumps({"workflowId": wf_id}, indent=2))


def handle_get_execution(args):
    base, token = get_config()
    params = {}
    if args.include_tasks:
        params["includeTasks"] = "true"
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}", params)
    result = request_json(url, token)
    output(result)


def handle_search_workflows(args):
    base, token = get_config()
    params = {"size": str(args.size or 10)}
    if args.status:
        params["query"] = f"status={args.status}"
    if args.query:
        params["query"] = args.query
    if args.sort:
        params["sort"] = args.sort
    url = build_url(base, "/workflow/search", params)
    result = request_json(url, token)
    output(result)


# ---------------------------------------------------------------------------
# Workflow management handlers
# ---------------------------------------------------------------------------

def handle_pause_workflow(args):
    base, token = get_config()
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}/pause")
    request_json(url, token, method="PUT", expect_json=False)
    print(f"Workflow {args.id} paused.")


def handle_resume_workflow(args):
    base, token = get_config()
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}/resume")
    request_json(url, token, method="PUT", expect_json=False)
    print(f"Workflow {args.id} resumed.")


def handle_terminate_workflow(args):
    base, token = get_config()
    params = {}
    if args.reason:
        params["reason"] = args.reason
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}", params)
    request_json(url, token, method="DELETE", expect_json=False)
    print(f"Workflow {args.id} terminated.")


def handle_restart_workflow(args):
    base, token = get_config()
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}/restart")
    request_json(url, token, method="POST", expect_json=False)
    print(f"Workflow {args.id} restarted.")


def handle_retry_workflow(args):
    base, token = get_config()
    url = build_url(base, f"/workflow/{urllib.parse.quote(args.id)}/retry")
    request_json(url, token, method="POST", expect_json=False)
    print(f"Workflow {args.id} retried.")


# ---------------------------------------------------------------------------
# Task handlers
# ---------------------------------------------------------------------------

def handle_signal_task(args):
    base, token = get_config()
    status = urllib.parse.quote(args.status)
    url = build_url(
        base,
        f"/tasks/{urllib.parse.quote(args.workflow_id)}/{urllib.parse.quote(args.task_ref)}/{status}",
    )
    body = {}
    if args.output:
        body = json.loads(args.output)
    result = request_json(url, token, method="POST", body=body, expect_json=False)
    print(f"Task {args.task_ref} signaled with status {args.status}.")
    if result:
        print(result)


def handle_signal_task_sync(args):
    base, token = get_config()
    status = urllib.parse.quote(args.status)
    url = build_url(
        base,
        f"/tasks/{urllib.parse.quote(args.workflow_id)}/{urllib.parse.quote(args.task_ref)}/{status}/sync",
    )
    body = {}
    if args.output:
        body = json.loads(args.output)
    result = request_json(url, token, method="POST", body=body)
    if result:
        output(result)
    else:
        print(f"Task {args.task_ref} signaled synchronously with status {args.status}.")


def handle_poll_task(args):
    base, token = get_config()
    params = {"count": str(args.count or 1)}
    url = build_url(base, f"/tasks/poll/batch/{urllib.parse.quote(args.task_type)}", params)
    result = request_json(url, token)
    output(result)


def handle_queue_size(args):
    base, token = get_config()
    params = {}
    if args.task_type:
        params["taskType"] = args.task_type
    url = build_url(base, "/tasks/queue/size", params)
    result = request_json(url, token)
    output(result)


# ---------------------------------------------------------------------------
# CLI definition
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Conductor REST API fallback (stdlib only)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- Workflow metadata --
    sub.add_parser("list-workflows", help="List all workflow definitions")

    p = sub.add_parser("get-workflow", help="Get a workflow definition")
    p.add_argument("--name", required=True)
    p.add_argument("--version", default=None)

    p = sub.add_parser("create-workflow", help="Create a workflow definition from JSON file")
    p.add_argument("--file", required=True)

    p = sub.add_parser("update-workflow", help="Update a workflow definition from JSON file")
    p.add_argument("--file", required=True)

    p = sub.add_parser("delete-workflow", help="Delete a workflow definition")
    p.add_argument("--name", required=True)
    p.add_argument("--version", required=True)

    # -- Workflow execution --
    p = sub.add_parser("start-workflow", help="Start a workflow execution")
    p.add_argument("--name", required=True)
    p.add_argument("--version", default=None)
    p.add_argument("--correlation-id", default=None)
    p.add_argument("--input", default=None, help="Inline JSON input")
    p.add_argument("--input-file", default=None, help="Path to JSON input file")

    p = sub.add_parser("get-execution", help="Get workflow execution status")
    p.add_argument("--id", required=True)
    p.add_argument("--include-tasks", action="store_true")

    p = sub.add_parser("search-workflows", help="Search workflow executions")
    p.add_argument("--status", default=None)
    p.add_argument("--query", default=None)
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--sort", default=None)

    # -- Workflow management --
    p = sub.add_parser("pause-workflow", help="Pause a running workflow")
    p.add_argument("--id", required=True)

    p = sub.add_parser("resume-workflow", help="Resume a paused workflow")
    p.add_argument("--id", required=True)

    p = sub.add_parser("terminate-workflow", help="Terminate a workflow")
    p.add_argument("--id", required=True)
    p.add_argument("--reason", default=None)

    p = sub.add_parser("restart-workflow", help="Restart a completed workflow")
    p.add_argument("--id", required=True)

    p = sub.add_parser("retry-workflow", help="Retry the last failed task")
    p.add_argument("--id", required=True)

    # -- Task operations --
    p = sub.add_parser("signal-task", help="Signal a task (async)")
    p.add_argument("--workflow-id", required=True)
    p.add_argument("--task-ref", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--output", default=None, help="JSON output to pass to the task")

    p = sub.add_parser("signal-task-sync", help="Signal a task (sync, returns workflow)")
    p.add_argument("--workflow-id", required=True)
    p.add_argument("--task-ref", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--output", default=None, help="JSON output to pass to the task")

    p = sub.add_parser("poll-task", help="Poll for tasks of a given type")
    p.add_argument("--task-type", required=True)
    p.add_argument("--count", type=int, default=1)

    p = sub.add_parser("queue-size", help="Get task queue size")
    p.add_argument("--task-type", default=None)

    args = parser.parse_args()

    handlers = {
        "list-workflows": handle_list_workflows,
        "get-workflow": handle_get_workflow,
        "create-workflow": handle_create_workflow,
        "update-workflow": handle_update_workflow,
        "delete-workflow": handle_delete_workflow,
        "start-workflow": handle_start_workflow,
        "get-execution": handle_get_execution,
        "search-workflows": handle_search_workflows,
        "pause-workflow": handle_pause_workflow,
        "resume-workflow": handle_resume_workflow,
        "terminate-workflow": handle_terminate_workflow,
        "restart-workflow": handle_restart_workflow,
        "retry-workflow": handle_retry_workflow,
        "signal-task": handle_signal_task,
        "signal-task-sync": handle_signal_task_sync,
        "poll-task": handle_poll_task,
        "queue-size": handle_queue_size,
    }

    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
