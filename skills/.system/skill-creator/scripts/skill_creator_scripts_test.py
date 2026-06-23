#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
import sys

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_openai_yaml  # type: ignore
import quick_validate  # type: ignore


class SkillCreatorScriptsTest(unittest.TestCase):
    def make_skill_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        skill_dir = Path(temp_dir.name)
        skill_dir.joinpath("SKILL.md").write_text(
            "---\n"
            "name: openai-docs\n"
            "description: Reference official OpenAI docs for implementation guidance.\n"
            "---\n"
        )
        return skill_dir

    def test_write_openai_yaml_preserves_existing_sections(self):
        skill_dir = self.make_skill_dir()
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir()
        openai_yaml = agents_dir / "openai.yaml"
        openai_yaml.write_text(
            "interface:\n"
            '  display_name: "Old Name"\n'
            '  short_description: "Old description that is safely long enough"\n'
            '  icon_small: "./assets/openai-small.svg"\n'
            '  default_prompt: "Use $openai-docs to answer product questions."\n'
            "dependencies:\n"
            "  tools:\n"
            '    - type: "mcp"\n'
            '      value: "openaiDeveloperDocs"\n'
            '      description: "OpenAI Developer Docs MCP server"\n'
            '      transport: "streamable_http"\n'
            '      url: "https://developers.openai.com/mcp"\n'
        )

        result = generate_openai_yaml.write_openai_yaml(skill_dir, "openai-docs", [])

        self.assertEqual(result, openai_yaml)
        data = yaml.safe_load(openai_yaml.read_text())
        self.assertEqual(data["interface"]["display_name"], "OpenAI Docs")
        self.assertEqual(
            data["interface"]["short_description"],
            "Help with OpenAI Docs tasks",
        )
        self.assertEqual(data["interface"]["icon_small"], "./assets/openai-small.svg")
        self.assertEqual(
            data["interface"]["default_prompt"],
            "Use $openai-docs to answer product questions.",
        )
        self.assertEqual(
            data["dependencies"]["tools"][0]["value"],
            "openaiDeveloperDocs",
        )

    def test_write_openai_yaml_rejects_invalid_existing_yaml(self):
        skill_dir = self.make_skill_dir()
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir()
        openai_yaml = agents_dir / "openai.yaml"
        openai_yaml.write_text("interface: [\n")

        result = generate_openai_yaml.write_openai_yaml(skill_dir, "openai-docs", [])

        self.assertIsNone(result)
        self.assertEqual(openai_yaml.read_text(), "interface: [\n")

    def test_validate_skill_accepts_valid_openai_yaml(self):
        skill_dir = self.make_skill_dir()
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir()
        agents_dir.joinpath("openai.yaml").write_text(
            "interface:\n"
            '  display_name: "OpenAI Docs"\n'
            '  short_description: "Reference official OpenAI docs for implementations"\n'
            "dependencies:\n"
            "  tools:\n"
            '    - type: "mcp"\n'
            '      value: "openaiDeveloperDocs"\n'
        )

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid)
        self.assertEqual(message, "Skill is valid!")

    def test_validate_skill_rejects_invalid_openai_yaml(self):
        skill_dir = self.make_skill_dir()
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir()
        agents_dir.joinpath("openai.yaml").write_text("interface: [\n")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("agents/openai.yaml", message)


if __name__ == "__main__":
    unittest.main()
