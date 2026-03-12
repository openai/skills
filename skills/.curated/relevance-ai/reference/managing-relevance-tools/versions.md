# Version Management

How to recover tools from accidental changes using version history.

## Overview

Every time you publish a tool, a version snapshot is saved. If you accidentally wipe a tool's config, you can restore from a previous version.

## Available MCP Tools

| Tool                             | Description                                                |
| -------------------------------- | ---------------------------------------------------------- |
| `relevance_list_tool_versions`   | List version history for a tool                            |
| `relevance_get_tool_version`     | Get a specific version's full config                       |
| `relevance_restore_tool_version` | Restore a tool to a previous version (creates a new draft) |
| `relevance_publish_tool`         | Publish the restored draft                                 |

## Emergency Recovery Workflow

### 1. List Versions

```
relevance_list_tool_versions({
  toolId: "my-tool-id"
})
```

Returns version snapshots with `version_id`, `created_at`, and `config` (including `transformations`).

### 2. Find Working Version

Look at the `config` field in each version to find one with your transformations intact.

To inspect a specific version in detail:

```
relevance_get_tool_version({
  versionId: "version-uuid"
})
```

### 3. Restore Version

```
relevance_restore_tool_version({
  versionId: "working-version-uuid"
})
```

This creates a new draft from the specified version.

### 4. Publish Restored Draft

```
relevance_publish_tool({
  toolId: "my-tool-id"
})
```

## Preventing Accidental Wipes

### The MCP Auto-Merge

`relevance_upsert_tool` auto-merges with the existing tool config — top-level fields you omit are preserved.

**However**, `transformations` is replaced as a whole object. If you provide it, ALL steps must be included. To update one step in a 7-step tool, get the tool first with `relevance_get_tool`, modify that step in `transformations.steps`, then upsert with the complete `transformations`.

### Always Get Before Partial Updates

```
# WRONG — wipes transformations!
relevance_upsert_tool({ studio_id: "my-tool", emoji: "new-emoji" })

# CORRECT — get first, then upsert with all fields
# 1. relevance_get_tool({ studioId: "my-tool" })
# 2. relevance_upsert_tool({ ...full_config, emoji: "new-emoji" })
```

## Version Retention

- Versions are kept for recent publishes
- Old versions may be pruned over time

## API Reference (for `relevance_api_request` fallback)

| Operation       | Method | Endpoint                                             |
| --------------- | ------ | ---------------------------------------------------- |
| List versions   | POST   | `/tools/versions/list` with `{ tool_id, page_size }` |
| Get version     | GET    | `/tools/versions/{version_id}/get`                   |
| Restore version | POST   | `/tools/versions/restore` with `{ version_id }`      |
| Publish         | POST   | `/tools/versions/publish` with `{ tool_id }`         |
