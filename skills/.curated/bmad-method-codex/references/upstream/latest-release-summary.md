# BMAD-METHOD latest release

- tag: v6.0.0
- name: v6.0.0 - V6 Stable Release! The End of Beta!
- published: 2026-02-17T05:41:04Z
- url: https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.0.0

## Release notes

## [6.0.0]

V6 Stable Release! The End of Beta!

### 🎁 Features

* Add PRD workflow steps 2b (vision/differentiators) and 2c (executive summary) for more complete product requirements documentation
* Add new `bmad uninstall` command with interactive and non-interactive modes for selective component removal
* Add dedicated GitHub Copilot installer that generates enriched `.agent.md`, `.prompt.md` files and project configuration
* Add TEA browser automation prerequisite prompts to guide Playwright CLI/MCP setup after configuration

### 🐛 Bug Fixes

* Fix version comparison to use semantic versioning, preventing incorrect downgrade recommendations to older beta versions
* Fix `--custom-content` flag to properly populate sources and selected files in module config
* Fix module configuration UX messaging to show accurate completion status and improve feedback timing
* Fix changelog URL in installer start message for proper GitHub resolution
* Remove incorrect `mode: primary` from OpenCode agent template and restore `name` field across all templates
* Auto-discover PRD files in validate-prd workflow to reduce manual path input
* Fix installer non-interactive mode hanging and improve IDE configuration handling during updates
* Fix workflow-level config.yaml copying for custom content modules

### ♻️ Refactoring

* Remove alias variables from Phase 4 workflows, use canonical `{implementation_artifacts}` and `{planning_artifacts}`
* Add missing `project_context` references to workflows for consistency

### 📚 Documentation

* Add post-install notes documentation for modules
* Improve project-context documentation and fix folder structure
* Add BMad Builder link to index for extenders
