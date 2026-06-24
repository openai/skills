# Responses

Use Responses as a shell primitive: map prompts over files, emit stable JSON, and save artifacts. Prefer small scripts that leave reviewable outputs on disk.

When injecting local file contents into a prompt, wrap them in explicit tags such as `<note>...</note>` so prompt text and source data stay easy to distinguish.

## Default Shape

```bash
openai responses create \
  --model gpt-5.5 \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text' <<'YAML'
input: |
  Summarize this in one sentence.
YAML
```

Use `--raw-output --transform ...` for scalar shell output. Use `--format json` when you need `id`, `usage`, output item types, tool calls, sources, or errors.

Responses output may include non-message items such as reasoning items before the assistant message. When extracting assistant text, prefer `output.#(type=="message").content.0.text` over positional selectors like `output.0.content.0.text`.

## Batch Over Files

Emit derived files, JSONL, TSV, or a rename map.

```bash
mkdir -p summaries

for file in notes/*.md; do
  openai responses create \
    --model gpt-5.5 \
    --raw-output \
    --transform 'output.#(type=="message").content.0.text' <<YAML > "summaries/$(basename "$file" .md).summary.md"
input: |
  Summarize this note in five bullets. Preserve names, dates, and open loops.

  <note path="$file">
$(sed 's/^/  /' "$file")
  </note>
YAML
done
```

## Heredoc Templating

Use unquoted heredocs when shell variables should expand. Indent substituted file content inside YAML block scalars.

```bash
FILE_ID="$(
  openai files create \
    --file ./brief.pdf \
    --purpose user_data \
    --raw-output \
    --transform id
)"
QUESTION="Summarize this file in three bullets."

openai responses create \
  --model gpt-5.5 \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text' <<YAML
input:
  - role: user
    content:
      - type: input_text
        text: ${QUESTION}
      - type: input_file
        file_id: ${FILE_ID}
YAML
```

## Background And State

Background for longer work:

```bash
RESPONSE_ID="$(
  openai responses create \
    --model gpt-5.5 \
    --background \
    --input "Return a prioritized review of this launch checklist." \
    --raw-output \
    --transform id
)"

while [[ "$(openai responses retrieve --response-id "$RESPONSE_ID" --raw-output --transform status)" != "completed" ]]; do
  sleep 2
done

openai responses retrieve \
  --response-id "$RESPONSE_ID" \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text'
```
