---
name: alibaba-java-coding-guidelines-skill
description: Use when 需要按 Alibaba Java Coding Guidelines（阿里巴巴 Java 编码规范）审查、生成或重构 Java、Spring、MyBatis、Maven、MySQL、SQL、日志、异常、安全或数据库相关代码。
---

# 阿里巴巴 Java 开发规约

## 概览

使用本 skill 时，把《阿里巴巴 Java 开发手册》当作 Java 代码生成、重构和审查的默认质量基线。优先处理强制规则，再处理推荐规则；如果项目本地约定和规约冲突，说明冲突点并以用户或项目约定为准。

详细规则摘要见 `references/alibaba-java-rules.md`。需要精确出处或完整条文时，打开官方页面：`https://alibaba.github.io/Alibaba-Java-Coding-Guidelines/`。

## 兼容性

这是通用 Agent Skill，不绑定单个应用或运行器。Claude Code、Codex 以及其他支持 Agent Skills 目录规范的工具都应只依赖 `SKILL.md` 和按需读取的 `references/` 内容。

`agents/openai.yaml` 只是 OpenAI/Codex UI 元数据，属于可选增强；不应作为 Claude Code 或其他 agent 使用本 skill 的前提。

校验入口提供 Python、Node.js、Go 三种等价实现：`scripts/validate_skill.py`、`scripts/validate_skill.mjs`、`scripts/validate_skill.go`。使用者可以按本地运行时任选其一；需要验证三者一致时运行 `tests/test_validators.sh`。

## 使用场景

- 审查 Java、Spring、MyBatis、Maven、SQL、DDL、日志、异常处理或安全相关改动。
- 生成新类、接口、DTO、VO、DO、枚举、异常类、测试类、Mapper、Service、DAO 或 SQL。
- 重构命名、常量、集合、并发、控制流、日志、异常和数据库访问代码。
- 给出代码评审意见、整改清单、规范符合性报告或自动修复建议。

## 工作流程

1. 先识别任务类型：代码生成、代码审查、重构、SQL/DDL 审查、依赖治理、安全检查。
2. 读取当前项目的已有风格、包结构、测试框架和持久层写法，避免只按通用规约硬套。
3. 按严重级别处理：
   - 强制：发现违反时必须指出或修复。
   - 推荐：默认遵循；如果不采用，说明权衡。
   - 参考：作为设计建议，不阻塞交付。
4. 针对相关模块读取 `references/alibaba-java-rules.md` 中对应小节。
5. 输出结果时按影响排序：正确性和安全性、稳定性和性能、可维护性、风格一致性。

## 代码生成规则

- 命名必须清晰准确：类名用 UpperCamelCase，方法、参数、成员变量和局部变量用 lowerCamelCase，常量用大写加下划线。
- 代码注释使用中文；公开 API、复杂业务规则、异常含义和空值语义要写清楚。
- 不使用魔法值；固定范围值优先使用枚举。
- 日志使用 SLF4J 门面，不直接绑定具体日志实现；低级别日志使用占位符或级别判断。
- 资源关闭优先使用 try-with-resources；不要在 finally 中 return 或抛出新异常。
- MyBatis 参数默认使用 `#{}`，禁止把用户输入拼进 SQL。
- Web、Open API、SQL、HTML 输出和用户输入必须做权限、参数校验、转义或脱敏。

## 代码审查输出

审查时优先给出可执行意见。每条意见包含：

- 级别：强制、推荐或参考。
- 位置：文件和行号，能定位就定位。
- 问题：违反了哪类规约。
- 风险：可能造成的错误、安全、性能或维护成本。
- 建议：给出可落地的改法。

如果没有发现问题，说明已检查的范围，并点出仍未覆盖的风险，例如没有运行测试、没有看到数据库索引信息、没有线上日志配置等。

## 常见误区

- 不要只检查格式；命名、空值、异常边界、日志上下文、事务、SQL 注入和权限校验同样重要。
- 不要把推荐规则包装成强制缺陷；推荐项要讲清收益和代价。
- 不要为了规约牺牲项目一致性；本地架构分层、包名和框架约束要先看再改。
- 不要依赖某个 agent 产品的专属工具、路径或配置；只把它们作为可选增强。
- 不要大段复述官方文档；只加载和任务相关的规则摘要。
