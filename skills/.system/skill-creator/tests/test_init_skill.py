#!/usr/bin/env python3

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import init_skill
import quick_validate


class InitSkillTemplateTests(unittest.TestCase):
    def test_generated_skill_template_passes_validator(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with contextlib.redirect_stdout(io.StringIO()):
                skill_dir = init_skill.init_skill(
                    "example-skill",
                    tmpdir,
                    [],
                    False,
                    [],
                )

            self.assertIsNotNone(skill_dir)

            valid, message = quick_validate.validate_skill(skill_dir)
            self.assertTrue(valid, message)


if __name__ == "__main__":
    unittest.main()
