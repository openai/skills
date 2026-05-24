#!/usr/bin/env python3
"""校验本仓库是否保持通用 Agent Skill 的基本结构。"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"失败：{message}")
    sys.exit(1)


def main() -> None:
    skill = ROOT / "SKILL.md"
    reference = ROOT / "references" / "alibaba-java-rules.md"
    metadata = ROOT / "agents" / "openai.yaml"

    for path in (skill, reference):
        if not path.exists():
            fail(f"缺少文件 {path.relative_to(ROOT)}")

    skill_text = skill.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        fail("SKILL.md 缺少 YAML frontmatter")

    frontmatter_match = re.match(r"^---\n(?P<body>.*?)\n---", skill_text, re.DOTALL)
    if not frontmatter_match:
        fail("SKILL.md frontmatter 格式不正确")

    frontmatter = frontmatter_match.group("body")
    name_match = re.search(r"^name:\s*(?P<name>[a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
    if not name_match:
        fail("SKILL.md 缺少合法的 name")

    skill_name = name_match.group("name")
    if skill_name != ROOT.name:
        fail(f"skill 名称必须和目录名一致：{skill_name} != {ROOT.name}")
    if len(skill_name) > 64 or skill_name.startswith("-") or skill_name.endswith("-") or "--" in skill_name:
        fail("skill 名称不符合 Agent Skills 命名限制")

    if not re.search(r"^description:\s*.+$", frontmatter, re.MULTILINE):
        fail("SKILL.md 缺少 description")

    reference_text = reference.read_text(encoding="utf-8")
    required_sections = ["编程规约", "异常和日志", "MySQL 规约", "工程规约", "安全规约"]
    missing = [section for section in required_sections if section not in reference_text]
    if missing:
        fail("规则摘要缺少章节：" + "、".join(missing))

    if metadata.exists():
        metadata_text = metadata.read_text(encoding="utf-8")
        if "$" + skill_name not in metadata_text:
            fail("agents/openai.yaml 的默认提示没有引用当前 skill 名称")

    print("通过：skill 结构和关键章节完整")


if __name__ == "__main__":
    main()
