---
name: codex-plugin-discovery
description: Use when a user asks what Codex plugins are available or can be used, wants plugin recommendations for a task, asks to find/search/discover installable plugins, asks about the plugin marketplace, or asks whether a plugin can help with a task.
---

# Codex Plugin Discovery

Discover candidate Codex plugins from the official `openai/plugins` GitHub repository.

## Core Rule

Use only metadata indexed from:

```text
https://github.com/openai/plugins
```

This boundary is intentional, even under deadline or coverage pressure. Do not read Codex `.tmp` marketplace caches, installed plugin caches, or active-session tool caches. Those sources are out of scope for this first version.

Do not auto-install plugins. Recommend candidates and explain the evidence only. Do not claim this covers the full Codex App Plugin Directory.

## Workflow

1. If the user asks what plugins are currently enabled/installed in this session, answer from the current session's available plugin list first. Keep it concise.
2. If the user asks broadly what plugins are available, can be used, or exist in the marketplace, do not list every indexed plugin. State that this skill can search `openai/plugins`, explain the coverage limit, and ask for the task or category they care about.
3. If the user asks for discoverable, installable, marketplace, or task-relevant plugins, use this skill's index.
4. If `index/plugins-index.json` is missing or stale, run `python3 scripts/build_index.py`.
5. Search with a concrete query, such as `python3 scripts/search_index.py "summarize support tickets"`.
6. Present up to five candidates from the index.
7. Explain matched fields and why each plugin may help.
8. State that results only cover plugins present in `openai/plugins`.

`stale` means the stored upstream commit SHA differs from `git ls-remote https://github.com/openai/plugins HEAD`.

## Index Boundary

Index only direct plugin manifests:

```text
plugins/*/.codex-plugin/plugin.json
```

Do not recursively include nested manifests such as `plugins/plugin-eval/fixtures/...`; valid fixture JSON is still test data, not a recommendable plugin.

## Output Shape

For broad availability questions such as "what plugins can I use?", do not dump the full index. Answer with:

- The current-session plugin list if the user asked about enabled plugins
- A short note that discoverable candidates can be searched from `openai/plugins`
- A request for the task, domain, or category to search
- At most five examples or categories if examples would help

For each recommendation, include:

- Plugin name and display name
- Category
- Why it matches
- Matched fields
- Repository or plugin path
- Confidence note

If no candidate is strong, say no strong match was found in `openai/plugins` and suggest manually inspecting that repository or broadening the query.

## Do Not

| Temptation | Required Response |
| --- | --- |
| "Use local caches for broader coverage" | Do not. This skill is `openai/plugins` only. |
| "Include fixture manifests for completeness" | Do not. Index only direct plugin manifests. |
| "Auto-install high-confidence matches" | Do not. Recommend and explain only. |
| "Claim this covers the Plugin Directory" | Do not. Say it only covers `openai/plugins`. |
