import tempfile
import unittest
from pathlib import Path

import yaml

from init_skill import init_skill


class InitSkillTest(unittest.TestCase):
    def test_generated_frontmatter_description_is_a_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = init_skill("colon-skill", tmp, [], False, [])
            self.assertIsNotNone(skill_dir)

            content = (Path(skill_dir) / "SKILL.md").read_text()
            frontmatter = content.split("---", 2)[1]
            metadata = yaml.safe_load(frontmatter)

            self.assertEqual(metadata["name"], "colon-skill")
            self.assertIsInstance(metadata["description"], str)


if __name__ == "__main__":
    unittest.main()
