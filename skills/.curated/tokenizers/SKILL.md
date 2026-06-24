---
name: tokenizers
description: Build, train, inspect, debug, or migrate text tokenizers for LLM and NLP projects. Use when working with Hugging Face Tokenizers, BPE, byte-level BPE, WordPiece, Unigram, SentencePiece, special tokens, chat templates, tokenizer JSON files, vocabulary/merge files, offset mappings, or tokenizer/model compatibility bugs.
---

# Tokenizers

Use this skill for tokenizer work. Tokenizer changes are compatibility changes: preserve reproducibility and test old/new encodings before replacing artifacts.

## Validated Version Evidence

This guidance was checked against a mined Hugging Face `tokenizers` source checkout at `tokenizers` 0.22.2-dev.0, with Python bindings requiring Python >=3.9. Related mined environments locked `tokenizers` 0.22.1 and 0.22.2, and the mined `transformers` source expected `tokenizers>=0.22.0,<=0.23.0`.

Before modifying tokenizer artifacts, capture the active versions:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["tokenizers", "transformers", "sentencepiece", "huggingface-hub"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to make tokenizer behavior explicit and reproducible. A complete run produces:

- The tokenizer artifact paths and package versions.
- Old/new encodings for representative prompts.
- Special token IDs, chat template, vocab size, padding/truncation settings, and max length.
- A save/reload check in a fresh process.
- A compatibility statement for the target model embedding size or resize step.

## Standalone Quick Start

When there is no existing tokenizer test, run this baseline before editing artifacts:

```bash
python - <<'PY'
from transformers import AutoTokenizer

path = "."
t = AutoTokenizer.from_pretrained(path)
samples = ["hello world", " hello", "<|endoftext|>", "def foo(x): return x + 1"]
print("vocab", len(t))
print("special", t.special_tokens_map)
print("chat_template", bool(getattr(t, "chat_template", None)))
for s in samples:
    ids = t.encode(s)
    print(repr(s), ids, t.decode(ids))
PY
```

If `AutoTokenizer.from_pretrained(".")` does not apply, replace `path` with the tokenizer directory or model id used by the repo.

## Workflow

1. Identify tokenizer type and artifacts: `tokenizer.json`, vocab, merges, SentencePiece model, special token maps, chat template, and model config.
2. Encode a few representative strings before changing anything:

```bash
python - <<'PY'
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained(".")
for s in ["hello world", " hello", "<|endoftext|>"]:
    print(repr(s), t.encode(s), t.decode(t.encode(s)))
PY
```

3. Check vocabulary size, special token IDs, padding side, truncation, and max length.
4. Make changes in one place and save all dependent tokenizer files together.
5. Compare old and new token IDs for representative prompts.

After saving artifacts, reload them in a fresh process instead of relying on the in-memory tokenizer:

```bash
python - <<'PY'
from transformers import AutoTokenizer
saved_tokenizer = "<saved-tokenizer-dir-or-model-id>"
t = AutoTokenizer.from_pretrained(saved_tokenizer)
print(len(t), t.special_tokens_map)
print(t.encode("The saved tokenizer reloads."))
PY
```

## Training and Conversion

- Choose the algorithm for the data and model family: BPE, byte-level BPE, WordPiece, or Unigram.
- Normalize text deliberately; case folding, Unicode normalization, and whitespace handling affect every downstream result.
- Include domain-specific tokens only when they occur often enough to justify vocabulary slots.
- Reserve special tokens before training or add them consistently after training.
- When converting formats, verify both encoding IDs and decoded text.

## References

Open `references/workflows.md` for detailed tokenizer training, conversion, compatibility, chat-template, offset-mapping, and model-resize workflows.

Open `references/mastery.md` for tokenizer mental models, algorithm choices, artifact contracts, prompt-format risks, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

## Compatibility Checks

- Tokenizer vocab size must match model embedding size unless the model is resized and saved.
- Chat templates must produce exactly the prompt format expected by the trained model.
- `pad_token_id`, `eos_token_id`, `bos_token_id`, and `unk_token_id` should be explicit.
- Offset mappings matter for extraction, highlighting, NER, and evaluation.
- Byte-level tokenizers may preserve leading spaces in ways that affect tests.
- Fast and slow tokenizer implementations should agree for representative inputs when both are supported.

Model compatibility check:

```python
embedding_rows = model.get_input_embeddings().weight.shape[0]
assert len(tokenizer) == embedding_rows, (len(tokenizer), embedding_rows)
```

If the tokenizer is intentionally expanded, resize embeddings and save the model/config together with the tokenizer.

## Debugging

- If generation never stops, inspect EOS token IDs and stop sequences.
- If fine-tuning labels are wrong, inspect masked label positions after tokenization.
- If prompts get much longer, compare token counts and whitespace normalization.
- If model loading warns about size mismatch, compare tokenizer vocab and embedding shape.
- If multilingual text breaks, inspect normalization, pre-tokenization, unknown tokens, and byte fallback.

## Done Criteria

- Old/new encodings are compared for representative text.
- Special tokens and chat templates are verified.
- The tokenizer artifact can be loaded in a fresh process with the target model or training script.
- The final notes include whether model embeddings were unchanged, resized, or not checked.
