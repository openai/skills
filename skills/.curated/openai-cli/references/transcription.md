# Transcription

Use transcription commands when audio should become shell-readable text or structured timing data.

## Plain Text

```bash
openai audio:transcriptions create \
  --model gpt-4o-transcribe \
  --file ./speech.wav \
  --raw-output \
  --transform text
```

## Response Formats

Choose the response format for the job:

| Need | Use |
| --- | --- |
| Plain transcript text in shell pipelines | `--response-format json --transform text --raw-output` |
| Subtitle files | `--model whisper-1 --response-format srt` or `--response-format vtt` |
| Segment or word timestamps | `--model whisper-1 --response-format verbose_json` |
| Speaker-labeled diarization | `--model gpt-4o-transcribe-diarize --response-format diarized_json` |

## Word Timing

For word-level timing:

```bash
openai audio:transcriptions create \
  --model whisper-1 \
  --file ./speech.wav \
  --response-format verbose_json \
  --timestamp-granularity word \
  --format json
```

```json
{
  "text": "The OpenAI CLI can call the API from ordinary shell scripts.",
  "words": [
    { "word": "The", "start": 0.0, "end": 0.42 },
    { "word": "OpenAI", "start": 0.42, "end": 1.22 }
  ]
}
```

## Speaker Turns

For speaker-labeled output:

```bash
openai audio:transcriptions create \
  --model gpt-4o-transcribe-diarize \
  --file ./speech.wav \
  --response-format diarized_json \
  --format json
```

```json
{
  "text": "The OpenAI CLI can call the API from ordinary shell scripts.",
  "segments": [
    {
      "type": "transcript.text.segment",
      "speaker": "A",
      "start": 0.05,
      "end": 5.25,
      "text": " The OpenAI CLI can call the API from ordinary shell scripts."
    }
  ]
}
```

`whisper-1` supports `json`, `text`, `srt`, `verbose_json`, and `vtt`. Use `diarized_json` whenever speaker attribution is the requirement; plain `json` with `gpt-4o-transcribe-diarize` returns text without `segments[].speaker`.

If local transcription upload fails with an `UploadFile` type error, update the CLI and retry.
