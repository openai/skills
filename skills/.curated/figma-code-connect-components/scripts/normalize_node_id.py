#!/usr/bin/env python3
"""Normalize a Figma node-id between URL and tool formats."""

from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: normalize_node_id.py <node-id>", file=sys.stderr)
        return 2
    node = sys.argv[1].strip()
    if not node:
        print("Empty node-id", file=sys.stderr)
        return 1
    if ":" in node:
        print(node.replace(":", "-"))
    else:
        print(node.replace("-", ":"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
