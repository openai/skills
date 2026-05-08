# Soul Character Troubleshooting

## Auth Or Plan

- Auth failure → ask the user to connect/authenticate the Higgsfield MCP server.
- Plan/upgrade error → explain that Soul training requires a paid plan.

## Photo Quality

Training may fail when photos are blurry, too dark, heavily filtered, duplicated, or show different people.

Ask for:

- 5–20 photos of the same person.
- Clear face visibility.
- Varied angles and lighting.
- Minimal sunglasses, masks, heavy filters, or extreme crops.

## Uploads

Local files must go through `media_upload` and `media_confirm`. Pass confirmed media IDs to `show_characters`, not local paths.

## Long Training

Use `show_characters` with `action: "status"` or `action: "list"` to check progress. If training stays pending for a long time, report the returned request id if present.
