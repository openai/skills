# Tokenizers Workflows

Use this reference when tokenizer changes need to be safe across training and inference.

## Contents

- [Artifact Inventory](#artifact-inventory)
- [Baseline Comparison](#baseline-comparison)
- [Training a Tokenizer](#training-a-tokenizer)
- [Chat Template Checks](#chat-template-checks)
- [Offset Mapping Checks](#offset-mapping-checks)
- [Model Resize](#model-resize)
- [Final Artifact](#final-artifact)

## Artifact Inventory

Record:

```text
tokenizer.json:
vocab/merges/model files:
special_tokens_map.json:
tokenizer_config.json:
chat_template:
model config:
model embedding rows:
```

## Baseline Comparison

Before editing, save encodings for:

- leading-space examples
- code snippets
- chat prompts
- multilingual text
- special tokens
- long input near max length

Output format:

```text
sample:
old ids:
new ids:
old decoded:
new decoded:
token count delta:
```

## Training a Tokenizer

1. Choose BPE, byte-level BPE, WordPiece, or Unigram based on the model family.
2. Decide normalization and pre-tokenization.
3. Reserve special tokens before training.
4. Train on representative data with deduplication.
5. Save all artifacts together.
6. Reload in a fresh process.

Do not replace a production tokenizer without comparing downstream prompt formatting and model embedding size.

## Chat Template Checks

Render one conversation:

```python
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
print(text)
print(ids)
```

Confirm the output matches the format used during training.

## Offset Mapping Checks

For extraction, NER, highlighting, or eval alignment:

```python
encoded = tokenizer("Alice lives in Paris", return_offsets_mapping=True)
print(encoded.tokens())
print(encoded["offset_mapping"])
```

If offsets are wrong, inspect normalization and pre-tokenization.

## Model Resize

If tokens are added:

```python
num_added = tokenizer.add_tokens(["<NEW_TOKEN>"])
if num_added:
    model.resize_token_embeddings(len(tokenizer))
    model.save_pretrained("resized-model")
    tokenizer.save_pretrained("resized-model")
```

Reload the pair in a fresh process and assert tokenizer length equals embedding rows.

## Final Artifact

Final notes should include:

```text
tokenizer source:
old/new vocab size:
special token IDs:
chat template status:
representative old/new encodings:
model embedding compatibility:
save/reload path:
```
