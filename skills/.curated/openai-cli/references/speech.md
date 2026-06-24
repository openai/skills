# Speech

Use speech commands when the output should be a local audio file. Keep model, voice, and output path explicit.

```bash
openai audio:speech create \
  --model gpt-4o-mini-tts \
  --voice marin \
  --input "The OpenAI CLI can call the API from ordinary shell scripts." \
  --output speech.mp3
```

How to play the audio depends on the local tools available on the machine.

Tone control:

```bash
openai audio:speech create \
  --model gpt-4o-mini-tts \
  --voice marin \
  --instructions "Speak clearly and neutrally, like a concise product demo narrator." \
  --input "The build passed. The release note is ready for review." \
  --output release-note.mp3
```

Use `instructions` for delivery and `input` for the words to say. Name audible qualities directly: pace, warmth, energy, formality, emphasis, audience, or whether the line should sound like narration, a notification, or a demo readout.

## Responses To Speech

```bash
summary="$(
  openai responses create \
    --model gpt-5.5 \
    --raw-output \
    --transform 'output.#(type=="message").content.0.text' <<'YAML'
input: |
  Summarize this release note in 90 seconds or less.
YAML
)"

openai audio:speech create \
  --model gpt-4o-mini-tts \
  --voice marin \
  --input "$summary" \
  --output release-note-summary.mp3
```
