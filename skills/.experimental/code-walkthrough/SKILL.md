---
name: code-walkthrough
description: Use when the user wants Codex to teach, replay, or explain an existing code feature from implementation source, especially requests like “讲解这个实现”, “一步步带我复现”, “从代码实现角度讲”, “带我理解完整链路”, “这个功能怎么跑起来”, “下一步”, or feedback that the explanation feels fragmented. Produces a source-grounded walkthrough that first builds a complete mental model, then follows the real runtime path with state/data continuity, API flow, rendering, interactions, edge cases, and design reasons. Do not use for code changes unless the user separately asks to implement or fix something.
---

# Code Walkthrough

## Teaching Contract

Explain code as a runnable story the user can reconstruct, not as a list of modules.

Always optimize for continuity:

- Start from the caller or user action.
- Keep a visible state ledger across steps.
- Explain what each function consumes, produces, and hands to the next function.
- Make file responsibilities clear, but do not let file boundaries replace runtime flow.
- Zoom into details only after the user has the full path in mind.

If the user says the explanation is fragmented, too abstract, or hard to reconstruct, switch to **Reconstruction Mode**: pause the step sequence, rebuild the complete mental model, show the state/data ledger, then continue.

## Mandatory First Response For Complex Features

Before step-by-step teaching, read the relevant files and produce an orientation pass. A complex feature is any feature that crosses a route/page boundary, API boundary, state/store/composable boundary, rendering boundary, timer/polling boundary, native/platform boundary, or more than three files.

The first response must include:

1. **Runtime script**: a compact end-to-end chain from user action to final UI/update.
2. **State ledger**: the important variables/entities, where they come from, and who uses them next.
3. **File responsibility map**: each important file's role in the runtime story.
4. **Deep-dive plan**: 3-6 runtime chains or phases to teach next.
5. **First deep-dive choice**: either start phase 1 immediately or ask the user which chain to expand when multiple chains are equally plausible.

Do not begin with isolated component summaries for complex features.

## Workflow

1. **Find the runtime boundary.**
   Use `rg` and file reads. Identify the user-facing trigger, route/open helper, page/container, state owner, API module, normalizer, renderer, interaction handlers, cleanup, and validation path.

2. **Build the whole map before details.**
   Draw the top-level chain as a real execution path, for example:

   ```text
   user click
     -> open helper
     -> platform route resolution
     -> page onLoad/onShow
     -> initial state
     -> query event
     -> request wrapper
     -> normalizer
     -> render model
     -> component render
     -> send/poll/popup update loop
   ```

3. **Create the state ledger.**
   List the key runtime values with this shape:

   ```ts
   {
     requestId: 'source -> first consumer -> later consumer',
     messages: 'canonical shape -> library shape -> rendered shape',
     timer: 'owner -> start -> stop -> cleanup'
   }
   ```

4. **Teach by runtime chain, not by file.**
   Each deep-dive section follows one real chain such as “open page”, “load history”, “send message”, “poll updates”, or “open auth popup”. A section may cross several files if that is how the code actually runs.

5. **Use local detail loops.**
   For every important function, explain:
   - who calls it
   - what inputs it receives
   - what it returns or mutates
   - why that boundary exists
   - what downstream code relies on

6. **Reconstruct concrete state.**
   Use small examples to show data shape before and after important boundaries. Include ordering, IDs, flags, loading states, disabled states, cache keys, timer state, and error state when relevant.

7. **Separate code facts from inference.**
   If the behavior is directly visible in source, state it as fact. If it depends on framework/library behavior, label it as inference and name the evidence.

8. **Preserve momentum.**
   End by naming the next runtime chain, not merely the next file.

## Output Shape

For complex features, prefer this sequence:

````markdown
**整体模型**

```text
runtime chain...
```

**状态账本**

```ts
{ ... }
```

**文件分工**

- [file](absolute/path:line): runtime role

**接下来按这几条链路讲**

1. 打开/入口链路
2. 初始数据链路
3. 渲染链路
4. 交互更新链路
5. 特殊状态/错误/清理链路

**第 1 条链路：标题**

...
````

For each deep-dive chain, use:

````markdown
**当前链路：N/M 标题**

上游留下：
这一步消费：
这一步产出：
下游使用：

真实执行顺序：

1. caller -> callee
2. callee -> data transformation
3. transformed state -> renderer/update

关键代码：

```ts
short snippet
```

状态变化：

```ts
before -> after
```

为什么这样设计：

核心结论：

下一条链路：
````

Keep each response digestible, but do not make a step so small that it loses the user's mental model. It is better to include one full runtime chain with several local details than to split every file into separate messages.

## Continuation Rules

When the user says “下一步”, “继续”, or similar:

- Continue the next planned runtime chain.
- Start with a short continuity anchor: what the previous chain produced and what the new chain consumes.
- Do not restart unless the user asks for a recap or a restart.
- If context is missing, reconstruct the most likely current map briefly and continue.
- If the previous answer was too fragmented, switch to Reconstruction Mode before advancing.

## Reconstruction Mode

Use when the user cannot reconstruct the implementation from the explanation, asks for “完整内容”, says “断层”, or asks to redesign the explanation.

Do this immediately:

1. Acknowledge the gap plainly.
2. Replace the step list with one complete runtime narrative.
3. Show the state ledger and data shape transitions.
4. Collapse minor helper files into the nearest runtime boundary.
5. Resume with fewer, larger chains.

Avoid defensive explanations. The fix is a better map, not more isolated detail.

## Code Reading Rules

- Start from the caller/user action, not an isolated helper.
- Prefer nearby implementation over abstract guesses.
- Use `rg` to find references before explaining exported functions.
- Follow delegation at least one layer deeper for important behavior.
- When explaining UI, include template structure, state, event handlers, child component responsibilities, and what the user sees.
- When explaining API, include request entry, request base, auth/signing, response handling, normalization, and cache if present.
- When explaining timers, polling, event listeners, or native resources, include owner lifecycle, duplicate prevention, start, stop, and cleanup.
- When a library boundary changes data shape, order, scrolling, rendering, or lifecycle, give it explicit attention and show the before/after shape.
- Cite clickable source references with line numbers for claims that matter.

## Detail Calibration

Include details that help the user rebuild the feature:

- exact variable names and where they are assigned
- why two similar fields both exist
- request/response shape and normalized shape
- list ordering before and after a library boundary
- disabled/loading/empty/error states
- owner and cleanup for timers/listeners/polling
- optimistic updates and later reconciliation
- platform-specific constraints and why dependencies are avoided

Compress details that do not affect the runtime story:

- obvious CSS declarations
- repetitive props that only pass through unchanged
- helper functions with no independent state or branching
- boilerplate imports

## Output Rules

- Use Chinese by default when the user is Chinese.
- Explain from source evidence; do not invent behavior not visible in code.
- Use short snippets only when they clarify a mechanism.
- Do not modify project files unless the user explicitly asks to implement or fix something.
- Do not run builds for explanation-only requests.
- For review-style requests, switch to code-review stance instead of walkthrough.

## Good Examples Of Step Boundaries

Good:

- “打开聊天室链路：列表点击 -> openPage -> 平台别名 -> native onLoad”
- “历史消息链路：z-paging query -> native API -> normalizer -> z-paging 顺序适配 -> 气泡渲染”
- “发送闭环：输入栏 emit -> 接口发送 -> 本地消息 -> z-paging 追加 -> 后续轮询去重”
- “授权消息链路：消息标记 -> 点击气泡 -> 拉详情 -> 弹窗状态 -> 提交同意/拒绝”

Avoid:

- “这个文件做什么”
- “这个组件做什么”
- “这个 API 做什么”

File-level explanation is allowed only after the runtime chain is clear.
