# Structured Data Extraction

Use this when downstream scripts need stable JSON, reusable schemas, or one JSON object per line.

## Reusable Schema

Save schemas to disk when reused.

```bash
openai responses create \
  --model gpt-5.5 \
  --instructions "Extract the person and topic from the input." \
  --input "Ada Lovelace wrote notes about the Analytical Engine." \
  --text.format "$(cat ./schema.json)" \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text'
```

## Flatten Arrays Into JSONL

When one input may yield zero, one, or many records, return an `items` array and flatten it into JSONL for later shell steps.

```bash
: > records.jsonl

for file in notes/*.md; do
  extracted="$(
    openai responses create \
      --model gpt-5.5 \
      --raw-output \
      --transform 'output.#(type=="message").content.0.text' <<YAML
instructions: Extract compact evidence-backed records. Return JSON only.
input: |
  <note path="$file">
$(sed 's/^/  /' "$file")
  </note>
text:
  format:
    type: json_schema
    name: items
    strict: true
    schema:
      type: object
      additionalProperties: false
      properties:
        items:
          type: array
          items:
            type: object
            additionalProperties: false
            properties:
              title: { type: string }
              summary: { type: string }
              evidence: { type: string }
            required: [title, summary, evidence]
      required: [items]
YAML
  )"

  jq -r --arg source "$file" '.items[]? + {source: $source} | @json' <<<"$extracted" >> records.jsonl
done
```

This keeps the model response structured while producing one JSON object per line for `jq`, `cat`, `rg`, imports, or later batch jobs.
