#!/usr/bin/env python3
"""Quick validation script for skills."""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

MAX_SKILL_NAME_LENGTH = 64
EXIT_VALIDATION_FAILED = 1
EXIT_RUNTIME_ERROR = 2


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path).expanduser()

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"Could not read SKILL.md: {e}"

    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}

    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Validate one or more Codex skill directories.")
    parser.add_argument(
        "skill_directories",
        metavar="skill_directory",
        nargs="+",
        help="Path to a skill directory containing SKILL.md.",
    )
    parser.add_argument(
        "--report",
        metavar="path",
        help="Write the complete validation result as JSON.",
    )
    return parser.parse_args(argv)


def build_result(raw_skill_path):
    skill_path = Path(raw_skill_path).expanduser()
    valid, message = validate_skill(skill_path)
    return {
        "path": str(skill_path),
        "resolved_path": str(skill_path.resolve(strict=False)),
        "valid": valid,
        "message": message,
    }


def summarize(results):
    total = len(results)
    passed = sum(1 for result in results if result["valid"])
    failed = total - passed
    return {"total": total, "passed": passed, "failed": failed}


def print_summary(results):
    if len(results) == 1:
        print(results[0]["message"])
        return

    for result in results:
        status = "PASS" if result["valid"] else "FAIL"
        print(f"{status}\t{result['path']}\t{result['message']}")

    summary = summarize(results)
    print(
        "Summary: "
        f"{summary['passed']}/{summary['total']} skills valid; "
        f"{summary['failed']} failed."
    )


def write_report(report_path, results):
    path = Path(report_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"summary": summarize(results), "results": results}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv):
    if yaml is None:
        print(
            "Missing dependency: PyYAML. Run with: "
            f"uv run --isolated --with pyyaml python3 {sys.argv[0]} <skill_directory> [...]",
            file=sys.stderr,
        )
        return EXIT_RUNTIME_ERROR

    args = parse_args(argv)
    results = [build_result(skill_path) for skill_path in args.skill_directories]
    print_summary(results)

    if args.report:
        try:
            write_report(args.report, results)
        except OSError as e:
            print(f"Failed to write report: {e}", file=sys.stderr)
            return EXIT_RUNTIME_ERROR

    if any(not result["valid"] for result in results):
        return EXIT_VALIDATION_FAILED
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
