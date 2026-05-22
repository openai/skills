# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. Tokenizer work is compatibility work; the skill must guide an agent through reproducible artifact changes and behavior checks.

## Retrieved Sources

- `huggingface/tokenizers`: Rust/Python/Node source and tests covering BPE, WordPiece, Unigram, normalizers, pre-tokenizers, post-processors, encoders, decoders, offsets, truncation, and save/load behavior.
- `huggingface/transformers`: `PreTrainedTokenizerFast` integration, trainer mapping for BPE/Unigram/WordLevel/WordPiece, `tokenizer.json` save behavior, special token handling, offsets, and retraining-from-existing-tokenizer behavior.
- Related mined environments: `tokenizers` 0.22.x and `transformers` constraints expecting `tokenizers>=0.22.0,<=0.23.0`.

## Workflows Reflected In The Skill

### Artifact Inventory

Transformers source treats fast tokenizer state as a `tokenizer.json` artifact while slow/tokenizer-specific formats may also require vocab, merges, SentencePiece model files, added-token maps, and special-token maps. The skill therefore requires agents to inventory every tokenizer artifact before editing.

### Behavior Comparison

Tokenizers tests exercise encode/decode, batch encode/decode, truncation, pair inputs, offsets, and special token behavior. The skill requires old/new behavior tables for representative strings, including:

- leading spaces and Unicode;
- special tokens;
- code-like text;
- chat-template formatted examples;
- offset mappings when alignment matters.

### Training And Conversion

Transformers maps model types to trainer classes for BPE, Unigram, WordLevel, and WordPiece. The skill requires algorithm selection, normalization choices, special-token reservation, and save/reload checks rather than one-off artifact edits.

### Model Compatibility

Tokenizer length and special-token IDs affect model embeddings and prompt formatting. The skill requires agents to state whether model embeddings need resizing and whether chat templates or generation stop tokens changed.

## Review Standard

Reject tokenizer changes without behavior evidence. A useful workflow must show installed versions, artifact inventory, representative old/new encodings, special token IDs, save/reload results, and model compatibility notes.
