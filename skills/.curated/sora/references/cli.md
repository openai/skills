# CLI reference (`scripts/sora.py`)

This file contains the command catalog for the bundled Sora CLI. Keep `SKILL.md` overview-first; put verbose CLI details here.

## What this CLI does
- `create`: create a new video job
- `create-and-poll`: create a job, poll until complete, optionally download
- `create-character`: upload a reusable non-human character reference clip
- `edit`: edit an existing generated video by ID
- `extend`: continue a completed video
- `poll`: wait for an existing job to finish
- `status`: retrieve job status/details
- `download`: download video/thumbnail/spritesheet
- `list`: list recent jobs
- `delete`: delete a job
- `remix`: legacy remix endpoint
- `create-batch`: create multiple video jobs locally from JSONL input

Real API calls require network access and `OPENAI_API_KEY`. `--dry-run` does not.

## Important distinction
- `create-batch` is a local concurrent fan-out helper.
- It is not the official Batch API.
- For the official Batch API, prepare a JSONL file for `POST /v1/videos`, upload it with `purpose=batch`, then create a batch via the Files and Batches APIs.

## Quick start
Set a stable path to the skill CLI (default `CODEX_HOME` is `~/.codex`):

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export SORA_CLI="$CODEX_HOME/skills/sora/scripts/sora.py"
```

If you're in this repo, set the path directly:

```bash
export SORA_CLI="$(git rev-parse --show-toplevel)/<path-to-skill>/scripts/sora.py"
```

If uv cache fails with permission errors:

```bash
export UV_CACHE_DIR="/tmp/uv-cache"
```

Dry-run without calling the API:

```bash
python "$SORA_CLI" create --prompt "Test" --dry-run
```

## Defaults
- Model: `sora-2`
- Size: `1280x720`
- Seconds: `4`
- Variant: `video`
- Poll interval: `10` seconds

Allowed seconds: `4`, `8`, `12`, `16`, `20`

Allowed sizes:
- `sora-2`: `1280x720`, `720x1280`
- `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`, `1920x1080`, `1080x1920`

## Create
Create a job:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2 \
  --prompt "Wide tracking shot of a teal coupe on a desert highway" \
  --size 1280x720 \
  --seconds 8
```

Create with a file-based first-frame reference:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2-pro \
  --prompt "She turns around and smiles, then slowly walks out of frame." \
  --size 1280x720 \
  --seconds 8 \
  --input-reference sample_720p.jpeg
```

Create with a stored/remote JSON reference object:

```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Slow reveal of a mossy mascot in a lantern-lit market" \
  --input-reference-file-id file_abc123
```

Create with characters:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2 \
  --prompt "Mossy, a moss-covered teapot mascot, rushes through a lantern-lit market at dusk." \
  --character-id char_123 \
  --seconds 8
```

If the prompt is already structured, disable augmentation:

```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt-file prompt.txt \
  --no-augment \
  --seconds 16
```

## Create and poll

```bash
uv run --with openai python "$SORA_CLI" create-and-poll \
  --model sora-2-pro \
  --prompt "Close-up of a steaming coffee cup on a wooden table" \
  --size 1920x1080 \
  --seconds 16 \
  --download \
  --variant video \
  --out coffee.mp4
```

## Create a character

```bash
uv run --with openai python "$SORA_CLI" create-character \
  --name Mossy \
  --video-file character.mp4
```

Use short non-human MP4 source clips and mention the character name verbatim in later prompts.

## Edit
Edit an existing generated video by ID:

```bash
uv run --with openai python "$SORA_CLI" edit \
  --id video_abc123 \
  --prompt "Same shot and camera move; shift the palette to teal, sand, and rust."
```

## Extend

```bash
uv run --with openai python "$SORA_CLI" extend \
  --id video_abc123 \
  --seconds 8 \
  --prompt "Continue the scene as the camera rises above the rooftops and reveals sunrise."
```

## Poll / status / download

```bash
uv run --with openai python "$SORA_CLI" poll --id video_abc123 --download --out out.mp4
uv run --with openai python "$SORA_CLI" status --id video_abc123
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant thumbnail --out thumb.webp
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant spritesheet --out sheet.jpg
```

## List / delete

```bash
uv run --with openai python "$SORA_CLI" list --limit 20 --after video_123 --order asc
uv run --with openai python "$SORA_CLI" delete --id video_abc123
```

## Legacy remix

```bash
uv run --with openai python "$SORA_CLI" remix \
  --id video_abc123 \
  --prompt "Same shot and framing; change only the palette to teal and sand."
```

Use `edit` for new workflows. `remix` is retained only for legacy compatibility.

## JSON output (`--json-out`)
- `create`, `status`, `list`, `delete`, `poll`, `remix`, `edit`, `extend`, and `create-character` write the response to a file.
- `create-and-poll` writes `{ "create": ..., "final": ... }`.
- In `--dry-run`, `--json-out` writes the request preview.
- If the path has no extension, `.json` is added automatically.

## Local batch JSONL schema (`create-batch`)
Each line is a JSON object (or a raw prompt string). Required key: `prompt`.

Common top-level keys:
- `model`, `size`, `seconds`
- `characters`: list like `[{"id":"char_123"}]` or `["char_123"]`
- `character_ids`: alternate list form such as `["char_123"]`
- `input_reference`: either a file path string or a JSON object with `file_id` or `image_url`
- `input_reference_path` / `input_reference_file`: file path aliases
- `input_reference_file_id`
- `input_reference_url`
- `out`: optional output filename for the job JSON

Prompt augmentation keys:
- `use_case`, `scene`, `subject`, `action`, `camera`, `style`, `lighting`, `palette`, `audio`, `dialogue`, `text`, `timing`, `constraints`, `negative`

Example:

```bash
mkdir -p tmp/sora
cat > tmp/sora/prompts.jsonl << 'EOB'
{"prompt":"A neon-lit rainy alley, slow dolly-in","seconds":"8"}
{"prompt":"Mossy, a moss-covered teapot mascot, jogs through a lantern-lit alley","seconds":"16","character_ids":["char_123"]}
{"prompt":"A warm sunrise over a misty lake, gentle pan","input_reference":{"file_id":"file_abc123"}}
EOB

uv run --with openai python "$SORA_CLI" create-batch \
  --input tmp/sora/prompts.jsonl \
  --out-dir out \
  --concurrency 3
```

Notes:
- `create-batch` writes one JSON response per job under `--out-dir`.
- Output names default to `NNN-<prompt-slug>.json`.
- Higher concurrency can hit rate limits.
- Treat the JSONL file as temporary and clean it up after use.

## Guardrails
- Use `python "$SORA_CLI" ...` or `uv run --with openai python "$SORA_CLI" ...`.
- For live API calls, prefer `uv run --with openai ...`.
- Do not create one-off runners unless the user explicitly asks.
- `edit` replaces `remix` for new integrations.

## See also
- API parameter quick reference: `references/video-api.md`
- Prompt structure and iteration: `references/prompting.md`
- Sample prompts: `references/sample-prompts.md`
- Troubleshooting: `references/troubleshooting.md`
