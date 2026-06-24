# 黄历 Skill（Luck Skill）

[English](README.md) | [简体中文](README_zh.md)

它像东方的智多星，也像西方的幸运女神：用传统黄历帮你看时机、选方向、避小坑，给每天多一点好彩头。

给 AI 编程助手用的中国传统黄历技能。一键获取每日行运卡、穿衣颜色指南、宜忌建议——全部翻译成现代、实用的行动参考。

如果这个 skill 对你有用的话，麻烦点个 star，这对我来说真的很重要！🌟

## 功能

- **今日行运卡** — 一卡看全天：日势、幸运方向、穿衣颜色、宜忌
- **场景判断** — 问某个具体行动是否适合：发版、签约、面试、出行、打游戏等
- **穿衣颜色** — 基于五行推算今天穿什么颜色更好
- **彭祖百忌** — 古老禁忌翻译成现代避坑提醒
- **时辰吉凶** — 查看各时辰段的吉凶
- **多语言** — 用什么语言问就用什么语言答。中文问得中文，英文问得英文。
- **玩梗调味** — 任何回答都可以撒点有趣的话；离谱问题会先做现实判断，再给实用替代方案

## 安装

### 快速安装

直接对你的 AI 助手说：

> 请帮我安装这个 skill：https://github.com/clllb/luck-skill

### 手动安装

**Claude Code**

```bash
git clone https://github.com/clllb/luck-skill.git ~/.claude/skills/luck-skill
```

**OpenAI Codex**

```bash
git clone https://github.com/clllb/luck-skill.git ~/.codex/skills/luck-skill
```

**OpenCode**

```bash
mkdir -p ~/.config/opencode/skill
git clone https://github.com/clllb/luck-skill.git ~/.config/opencode/skill/luck-skill
```

安装后用 `/luck-skill` 调用，或者直接用中文说「今天黄历」「明天适合签约吗」即可。

## 使用示例

直接跟 AI 助手自然对话即可：

| 你说 | 你得到 |
|------|--------|
| `今天黄历` | 完整今日行运卡 |
| `明天适合发版吗` | 发版适宜度评估 + 建议 |
| `今天穿什么颜色` | 穿衣颜色推荐 |
| `今晚适合打游戏吗` | 游戏时段建议 |
| `明天我能不能上太空` | 好玩的现实判断 + 实用目标 |
| `今天签约怎么样` | 签约指引 |
| `今天面试穿什么` | 面试穿搭 + 方位建议 |

技能会拉取真实黄历数据，给出有依据的现代建议——绝不做确定性算命。

## 数据来源

黄历数据由 [Toolbox](https://github.com/clllb/toolbox) 生成并托管。

## 免责声明

本技能提供的黄历内容仅供**文化和娱乐参考**，不预测结果，不替代专业判断。医疗、法律、金融、雇佣、重大合同等决策，请以专业人士意见为准。

## 许可证

MIT
