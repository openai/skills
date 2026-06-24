#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function fail(message) {
  console.log(`失败：${message}`);
  process.exit(1);
}

function relative(filePath) {
  return path.relative(ROOT, filePath);
}

const skill = path.join(ROOT, "SKILL.md");
const reference = path.join(ROOT, "references", "alibaba-java-rules.md");
const metadata = path.join(ROOT, "agents", "openai.yaml");

for (const filePath of [skill, reference]) {
  if (!existsSync(filePath)) {
    fail(`缺少文件 ${relative(filePath)}`);
  }
}

const skillText = readFileSync(skill, "utf8");
if (!skillText.startsWith("---\n")) {
  fail("SKILL.md 缺少 YAML frontmatter");
}

const frontmatterMatch = skillText.match(/^---\n(?<body>[\s\S]*?)\n---/);
if (!frontmatterMatch || !frontmatterMatch.groups) {
  fail("SKILL.md frontmatter 格式不正确");
}

const frontmatter = frontmatterMatch.groups.body;
const nameMatch = frontmatter.match(/^name:\s*([a-z0-9-]+)\s*$/m);
if (!nameMatch) {
  fail("SKILL.md 缺少合法的 name");
}

const skillName = nameMatch[1];
if (skillName !== path.basename(ROOT)) {
  fail(`skill 名称必须和目录名一致：${skillName} != ${path.basename(ROOT)}`);
}

if (
  skillName.length > 64 ||
  skillName.startsWith("-") ||
  skillName.endsWith("-") ||
  skillName.includes("--")
) {
  fail("skill 名称不符合 Agent Skills 命名限制");
}

if (!/^description:\s*.+$/m.test(frontmatter)) {
  fail("SKILL.md 缺少 description");
}

const referenceText = readFileSync(reference, "utf8");
const requiredSections = ["编程规约", "异常和日志", "MySQL 规约", "工程规约", "安全规约"];
const missing = requiredSections.filter((section) => !referenceText.includes(section));
if (missing.length > 0) {
  fail(`规则摘要缺少章节：${missing.join("、")}`);
}

if (existsSync(metadata)) {
  const metadataText = readFileSync(metadata, "utf8");
  if (!metadataText.includes(`$${skillName}`)) {
    fail("agents/openai.yaml 的默认提示没有引用当前 skill 名称");
  }
}

console.log("通过：skill 结构和关键章节完整");
