# Frontend Polish Call Examples

Use these examples as starting points. Replace framework, page type, constraints, and source material as needed.

## How to use these examples

- If you have code, paste the code directly after the prompt.
- If you have screenshots, attach them and say what must stay unchanged.
- If you have a repo, include the stack and the target files or page route.
- If you want a review first, ask for diagnosis before implementation.
- If you want direct edits, say `edit the code directly`.

## Output format variants

Use these when you want the model to adapt its response shape instead of always answering the same way.

### Let the model offer choices

```text
Use $frontend-polish for this task. If the best delivery format is not obvious, briefly offer me a choice between:
1. direct edit
2. audit then edit
3. design options
Then continue in the format I choose.
```

### Force direct implementation

```text
Use $frontend-polish. Do not spend time comparing options. Edit the code directly, then give me:
1. Direction
2. What changed
3. Validation
```

### Audit first

```text
Use $frontend-polish. Do not edit immediately. First give me:
1. the main AI-generated UI smells
2. the top fixes by impact
3. the recommended visual direction
If I approve, then implement.
```

### Show design directions first

```text
Use $frontend-polish. Before editing, show me 3 possible design directions for this page:
1. restrained and premium
2. denser and more product-like
3. bolder and more expressive
For each one, explain the tradeoff in 1-2 sentences.
```

### Prompt-only mode

```text
Use $frontend-polish to turn this request into a reusable prompt for Codex and Claude. Do not edit code yet. Give me:
1. a short prompt
2. a detailed prompt
3. the key constraints I should keep
```

## Codex examples

These are optimized for a Codex-style workflow where the model can inspect and edit code directly.

### Landing page

```text
Use $frontend-polish to refine this landing page. Keep the copy and section order intact, but reduce the generic SaaS feel and make the page feel more deliberate and high-end. Focus on hierarchy, spacing rhythm, hero composition, CTA emphasis, and mobile behavior. Edit the code directly.
```

### Auth page

```text
Use $frontend-polish to improve this sign-in page. Keep the form fields and logic unchanged. Make it feel calmer, more trustworthy, and less templated. Focus on spacing, typography, error states, focus states, submit button priority, and mobile layout. Edit the code directly.
```

### Dashboard

```text
Use $frontend-polish to refine this dashboard without turning it into a marketing page. Keep the information density reasonable. Focus on grouping, table rhythm, filter clarity, panel hierarchy, status color discipline, and responsive behavior. Edit the code directly.
```

### Detail page

```text
Use $frontend-polish to improve this product detail page. Keep the product data and purchase flow unchanged. Focus on media hierarchy, price and CTA emphasis, option selection states, supporting information rhythm, and mobile purchase usability. Edit the code directly.
```

### Component polish

```text
Use $frontend-polish to polish this component only. Do not redesign the whole page. Focus on spacing rhythm, visual hierarchy, hover and focus states, disabled and loading states, and implementation cleanliness. Edit the code directly.
```

### Review first, then edit

```text
Use $frontend-polish to audit this page first. Identify the main AI-generated UI smells, explain the highest-impact fixes, then implement the changes directly. Keep business logic intact.
```

## Claude or general-model examples

These are better when the model cannot edit files directly and you want a stronger task framing.

### General page prompt

```text
You must follow the attached Frontend Polish instructions and playbook.

Task: refine this frontend so it feels hand-crafted, high-end, and production-ready instead of AI-generated.
Stack: React + Tailwind CSS.
Constraints: keep business logic, content structure, and routes unchanged.
Focus: hierarchy, spacing rhythm, typography, state quality, responsive behavior, and reduction of repetitive visual patterns.
Output: complete updated code, a one-sentence visual direction, and a short list of the highest-impact refinements.
```

### Screenshot-based prompt

```text
You must follow the attached Frontend Polish instructions and playbook.

Based on the attached screenshot, redesign this page so it feels less templated and more intentionally designed. Do not chase flashy effects. Keep the page purpose the same. Provide:
1. a one-sentence visual direction
2. a concrete UI change list ordered by impact
3. complete React + Tailwind code for the revised page
4. notes on mobile behavior and interaction states
```

### Existing component prompt

```text
You must follow the attached Frontend Polish instructions and playbook.

Polish this component without changing its API. Keep it compatible with the existing codebase. Focus on reducing generic visual repetition, improving hierarchy, and making hover, focus, disabled, and loading states feel intentional. Return the full updated component code.
```

## Input patterns that help a lot

When calling the skill, add these if possible:

- `stack`: React, Vue, Next.js, Nuxt, plain HTML, Tailwind, SCSS
- `scope`: full page, one route, one component, one module
- `must keep`: business logic, copy, route structure, API shape, design system
- `priority`: hierarchy, responsiveness, trust, density, conversion, motion, clarity
- `avoid`: gradients everywhere, glassmorphism, card soup, oversized hero blocks, over-animation

Example:

```text
Use $frontend-polish to refine this page.
Stack: Next.js + Tailwind.
Scope: only `app/dashboard/page.tsx` and related local components.
Must keep: existing data flow and filters.
Priority: grouping, table readability, filter clarity, mobile layout.
Avoid: marketing-style gradients and oversized cards.
Edit the code directly.
```

## Short prompts for repeated daily use

```text
Use $frontend-polish to make this page feel less AI-generated and more product-grade. Keep the logic intact and edit the code directly.
```

```text
Use $frontend-polish. Audit first, then fix the highest-impact UI problems directly in code.
```

## 10 common Chinese wake-up prompts

Use these when working in Codex and you want a stable way to invoke the skill quickly.

### 1. Generic page polish

```text
调用 $frontend-polish，优化这个页面，保留业务逻辑，直接改代码。
```

### 2. Backend or dashboard polish

```text
调用 $frontend-polish，优化这个后台页面。保留数据结构和交互逻辑，重点提升信息分组、层级、表格节奏和响应式表现，直接改代码。
```

### 3. Landing page polish

```text
调用 $frontend-polish，优化这个官网首页。保留文案和模块顺序，重点去掉 AI 模板味，提升版式节奏、按钮质感和移动端表现，直接改代码。
```

### 4. Login or auth page polish

```text
调用 $frontend-polish，优化这个登录页。不要改表单逻辑和字段，重点处理信任感、输入框状态、错误提示、主按钮层级和窄屏布局。
```

### 5. Component-only polish

```text
调用 $frontend-polish，只优化这个组件，不要顺带重做整个页面。重点处理间距、层级、交互状态、禁用态、加载态和代码结构。
```

### 6. Audit first, then edit

```text
调用 $frontend-polish，先审查这个页面有哪些 AI 味、廉价感和体验问题，按影响大小排序，再直接修改代码。
```

### 7. Offer response modes first

```text
调用 $frontend-polish，如果这次任务更适合先讨论，请先给我 3 种工作方式可选：
1. 直接修改
2. 先审查再修改
3. 先给设计方向
然后按我选的继续。
```

### 8. Design directions before implementation

```text
调用 $frontend-polish，先不要改代码。先给我 3 个设计方向：
1. 克制高级
2. 更偏产品感
3. 更有视觉张力
每个方向用 1-2 句话说明取舍，然后我再选。
```

### 9. Prompt-only mode

```text
调用 $frontend-polish，不要直接改代码，先把这个需求整理成适合 Codex 和 Claude 复用的 prompt，给我短版和长版各一份。
```

### 10. Strict constraints mode

```text
调用 $frontend-polish，优化这个页面。
技术栈：React + Tailwind
范围：只改当前页面和相关局部组件
必须保留：业务逻辑、接口、路由、文案
重点：层级、节奏、状态、移动端
避免：玻璃态、满屏渐变、卡片堆砌、过度动画
直接改代码。
```
