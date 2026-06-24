package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
)

func fail(message string) {
	fmt.Printf("失败：%s\n", message)
	os.Exit(1)
}

func mustRead(path string) string {
	content, err := os.ReadFile(path)
	if err != nil {
		fail(fmt.Sprintf("无法读取文件 %s", path))
	}
	return string(content)
}

func main() {
	_, sourcePath, _, ok := runtime.Caller(0)
	if !ok {
		fail("无法定位校验脚本路径")
	}

	root := filepath.Clean(filepath.Join(filepath.Dir(sourcePath), ".."))
	skill := filepath.Join(root, "SKILL.md")
	reference := filepath.Join(root, "references", "alibaba-java-rules.md")
	metadata := filepath.Join(root, "agents", "openai.yaml")

	for _, filePath := range []string{skill, reference} {
		if _, err := os.Stat(filePath); err != nil {
			relativePath, _ := filepath.Rel(root, filePath)
			fail(fmt.Sprintf("缺少文件 %s", relativePath))
		}
	}

	skillText := mustRead(skill)
	if !strings.HasPrefix(skillText, "---\n") {
		fail("SKILL.md 缺少 YAML frontmatter")
	}

	frontmatterRegexp := regexp.MustCompile(`(?s)^---\n(.*?)\n---`)
	frontmatterMatch := frontmatterRegexp.FindStringSubmatch(skillText)
	if len(frontmatterMatch) < 2 {
		fail("SKILL.md frontmatter 格式不正确")
	}

	frontmatter := frontmatterMatch[1]
	nameRegexp := regexp.MustCompile(`(?m)^name:\s*([a-z0-9-]+)\s*$`)
	nameMatch := nameRegexp.FindStringSubmatch(frontmatter)
	if len(nameMatch) < 2 {
		fail("SKILL.md 缺少合法的 name")
	}

	skillName := nameMatch[1]
	if skillName != filepath.Base(root) {
		fail(fmt.Sprintf("skill 名称必须和目录名一致：%s != %s", skillName, filepath.Base(root)))
	}

	if len(skillName) > 64 ||
		strings.HasPrefix(skillName, "-") ||
		strings.HasSuffix(skillName, "-") ||
		strings.Contains(skillName, "--") {
		fail("skill 名称不符合 Agent Skills 命名限制")
	}

	descriptionRegexp := regexp.MustCompile(`(?m)^description:\s*.+$`)
	if !descriptionRegexp.MatchString(frontmatter) {
		fail("SKILL.md 缺少 description")
	}

	referenceText := mustRead(reference)
	requiredSections := []string{"编程规约", "异常和日志", "MySQL 规约", "工程规约", "安全规约"}
	missing := []string{}
	for _, section := range requiredSections {
		if !strings.Contains(referenceText, section) {
			missing = append(missing, section)
		}
	}
	if len(missing) > 0 {
		fail("规则摘要缺少章节：" + strings.Join(missing, "、"))
	}

	if _, err := os.Stat(metadata); err == nil {
		metadataText := mustRead(metadata)
		if !strings.Contains(metadataText, "$"+skillName) {
			fail("agents/openai.yaml 的默认提示没有引用当前 skill 名称")
		}
	}

	fmt.Println("通过：skill 结构和关键章节完整")
}
