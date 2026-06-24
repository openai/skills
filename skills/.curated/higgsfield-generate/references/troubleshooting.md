# Troubleshooting

## MCP Auth

- `Unauthorized` or auth challenge → ask the user to connect/authenticate the Higgsfield MCP server.
- The server advertises OAuth/device auth through `.well-known/oauth-protected-resource`; let the MCP host handle the flow.
- If auth succeeds but user data is empty, ask the user to confirm they are using the intended Higgsfield account/workspace.

## Validation

- Missing `prompt` → ask for a concise prompt.
- Invalid enum or unsupported field → call `models_explore(action: "get", model_id: ...)` and retry with declared params.
- Media role rejected → inspect the model's `medias` schema and change the role.
- Local file path rejected → use `media_upload`, upload bytes, then `media_confirm`; pass the resulting media ID.

## Job Lifecycle

- Non-terminal job → call `job_status`; respect `poll_after_seconds` if present.
- `failed` → try a safer or clearer prompt; mention the failure briefly.
- `nsfw` / `ip_detected` → content policy; ask for a safer revision.
- Timeout or transient server/network error → retry once, then report the request id if present.

## Marketing Studio

- Product fetch failed → ask for a clearer product URL or uploaded product images.
- Hook/setting rejected → confirm the selected `mode` supports setup items.
- Ad reference plus hook/setting rejected → choose one path: `ad_reference_id` or explicit hook/setting.
