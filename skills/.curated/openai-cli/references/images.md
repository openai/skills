# Image Generation

Use the Image API when the task is to generate or edit a local bitmap asset. Use Responses when images are part of a larger tool workflow.

## Generate an Image

```bash
openai images generate \
  --model gpt-image-2 \
  --prompt "A product render of a translucent green cube on a neutral background." \
  --format yaml \
  --transform 'data.0.b64_json' | base64 --decode > hero.png
```

No native image `--output` yet: extract `data.0.b64_json` and decode.

`gpt-image-2` notes:
- Do not use `--background transparent`; transparent backgrounds are not currently supported.
- Omit `--input-fidelity`; image inputs are always processed at high fidelity.
- `--size` accepts many custom resolutions, not only the older `1024x1024`, `1536x1024`, and `1024x1536` set. Keep both edges multiples of `16px`, max edge `3840px`, aspect ratio no wider than `3:1`, and total pixels between `655,360` and `8,294,400`.
- `--quality` still accepts `low`, `medium`, `high`, or `auto`.
- Prefer `--output-format jpeg` for lower-latency drafts when transparency is not needed.

## Edit an Image

```bash
openai images edit \
  --model gpt-image-2 \
  --image ./hero.png \
  --prompt "Turn the cube bright green." \
  --format yaml \
  --transform 'data.0.b64_json' | base64 --decode > hero-edited.png
```

If local image edit upload fails with an `UploadFile` type error, update the CLI and retry.
