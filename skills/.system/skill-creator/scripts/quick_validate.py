#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64
INTERFACE_STRING_FIELDS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}
DEPENDENCY_TOOL_STRING_FIELDS = {
    "type",
    "value",
    "description",
    "transport",
    "url",
}


def validate_openai_yaml(skill_path):
    openai_yaml = skill_path / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        return True, None

    try:
        data = yaml.safe_load(openai_yaml.read_text())
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in agents/openai.yaml: {e}"

    if data is None:
        return False, "agents/openai.yaml is empty"
    if not isinstance(data, dict):
        return False, "agents/openai.yaml must be a YAML dictionary"

    if "interface" in data:
        interface = data["interface"]
        if not isinstance(interface, dict):
            return False, "agents/openai.yaml field 'interface' must be a YAML dictionary"
        for key, value in interface.items():
            if key in INTERFACE_STRING_FIELDS and not isinstance(value, str):
                return (
                    False,
                    f"agents/openai.yaml field 'interface.{key}' must be a string, "
                    f"got {type(value).__name__}",
                )

    if "dependencies" in data:
        dependencies = data["dependencies"]
        if not isinstance(dependencies, dict):
            return False, "agents/openai.yaml field 'dependencies' must be a YAML dictionary"
        tools = dependencies.get("tools")
        if tools is not None:
            if not isinstance(tools, list):
                return False, "agents/openai.yaml field 'dependencies.tools' must be a YAML list"
            for index, tool in enumerate(tools, start=1):
                if not isinstance(tool, dict):
                    return (
                        False,
                        "agents/openai.yaml field 'dependencies.tools' entries must be YAML "
                        f"dictionaries (entry {index})",
                    )
                for key, value in tool.items():
                    if key in DEPENDENCY_TOOL_STRING_FIELDS and not isinstance(value, str):
                        return (
                            False,
                            f"agents/openai.yaml field 'dependencies.tools[{index}].{key}' "
                            f"must be a string, got {type(value).__name__}",
                        )

    return True, None


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
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

    openai_yaml_valid, openai_yaml_error = validate_openai_yaml(skill_path)
    if not openai_yaml_valid:
        return False, openai_yaml_error

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
