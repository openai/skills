# Compatibility Notes

This document consolidates the naming-compatibility rules for `easy-memory`
related-resource metadata.

## Purpose

`easy-memory` originally stored only local filesystem paths.
Later revisions expanded the same metadata channel so it can also store:
- project-relative local filesystem paths for resources inside the current
  working directory
- absolute local filesystem paths for resources outside the current working
  directory
- URLs
- document addresses

For backward compatibility, the historical field names and CLI option names were
kept stable even though their meaning is now broader.

## Historical Names And Current Meaning

- `PATHS`
  - Historical on-disk log field name
  - Current meaning: array of related resource objects
- `path_id`
  - Historical object field name
  - Current meaning: unique related resource ID
- `path_ids`
  - Historical agent-response field name from the older structured-response contract
  - Current meaning when encountered: list of related resource IDs
- `--related-path`
  - Historical CLI option name
  - Current meaning: project-local path, external absolute path, or
    URL/document address
- `--path-update`
  - Historical CLI option name
  - Current meaning: replace one related resource by ID
- `--path-clear`
  - Historical CLI option name
  - Current meaning: clear one related resource by ID while preserving the ID

## Stable Compatibility Rules

- Existing logs that use `PATHS` remain valid.
- Existing payloads that use `path_id` and older structured responses that use
  `path_ids` remain valid.
- Existing automation or tooling that calls `--related-path`, `--path-update`, or
  `--path-clear` does not need renaming.
- New implementations should interpret these historical names using the broader
  related-resource meaning.
- Older local-path entries that stored absolute paths remain valid and should be
  interpreted as `path_format:"absolute"` when no explicit `path_format` is
  present.

## Resource Interpretation

Each related resource object should be interpreted using `resource_type`:
- `local_path`
  - `path_format:"project_relative"` means `path` is relative to the current
    working directory and `directory` is the corresponding relative container
  - `path_format:"absolute"` means `path` is an absolute local filesystem path
    and `directory` is the absolute parent directory, or the directory itself
    if the stored target is already a directory
  - `system_hint` may be present for `path_format:"absolute"` entries to record
    a brief host hint for cross-machine work
- `url`
  - `path` is the URL or document address
  - `directory` is the derived parent or container URL

If older metadata does not include `resource_type`, the runtime should infer it.
If older local-path metadata does not include `path_format`, the runtime should
infer `absolute` for absolute-looking local paths and `project_relative` for
relative-looking local paths.

## Reading Strategy

When reading `easy-memory` metadata:
- do not assume `path` means a local filesystem path
- treat `path_id` as a stable related resource identifier
- use `resource_type` to decide whether the target is local or remote

## Source Of Truth

This note explains naming compatibility only.
The canonical structural contracts remain:
- `SKILL.md`
- `references/openai-compatible-api.md`
- `references/response-schema.md`
- `references/script-output-schema.md`
