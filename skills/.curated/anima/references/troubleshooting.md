# Common Issues and Solutions

## Issue: Timeout on playground-create
**Cause:** Default MCP client timeout is too short (often 60s).
**Solution:** Always use a 10-minute timeout (600000ms) for `playground-create` and `playground-publish` calls. Playground generation builds a full application and typically takes 3-7 minutes.

## Issue: Node ID format error
**Cause:** Using `-` instead of `:` in node IDs when calling Figma-related tools.
**Solution:** Convert `42-15` from the Figma URL to `42:15` for the API call.

## Issue: Wrong styling options for type
**Cause:** Each type (p2c, l2c, f2c) supports different styling and UI library options.
**Solution:** Check the styling and UI library options tables in [mcp-tools.md](mcp-tools.md). For example, `css_modules` is only available for f2c, and `uiLibrary` is not supported for p2c.

## Issue: Can't access playground
**Cause:** Private playground or expired session.
**Solution:** Verify authentication is set up correctly. Private playgrounds require team membership or direct sharing.

## Issue: Download URL expired
**Cause:** Pre-signed download URL from `project-download_from_playground` is only valid for 10 minutes.
**Solution:** Call `project-download_from_playground` again to get a fresh link.

## Issue: Generated code doesn't match project style
**Cause:** Tool parameters didn't match the project's actual technology stack.
**Solution:** Always detect the project stack first (Path B, Step B2). Pass accurate `framework`, `styling`, `language`, and `uiLibrary` parameters.

## Issue: Visual mismatch after implementation
**Cause:** Generated code was adapted without referencing the design context or comparing against snapshots.
**Solution:** For `codegen-figma_to_code`, always download and review snapshots. Use the `guidelines` field for design context (spacing, layout, typography).

## Issue: MCP connection not verified before calling tools
**Cause:** Attempting `playground-create` or other tools without first confirming the Anima MCP server is connected and authenticated.
**Solution:** Try calling any Anima MCP tool first. If it errors, set up authentication (see [setup.md](setup.md)).
