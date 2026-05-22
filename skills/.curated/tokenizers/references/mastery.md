# Tokenizers Mastery Notes

## Mental Model

A tokenizer is part of the model contract. Changing tokenization changes sequence length, special-token behavior, labels, offsets, and embedding compatibility.

## Algorithm Choices

- BPE: common for GPT-style models.
- Byte-level BPE: robust to arbitrary bytes and whitespace-sensitive text.
- WordPiece: common for BERT-style models.
- Unigram/SentencePiece: common for multilingual and seq2seq families.

Choose based on the model family and training data, not convenience.

## Artifact Contract

Tokenizer artifacts should be saved and versioned together:

```text
tokenizer.json
tokenizer_config.json
special_tokens_map.json
vocab/merges or sentencepiece model
model config when embedding size changes
```

## High-Risk Changes

- adding/removing special tokens
- changing chat templates
- changing normalization
- changing padding side
- changing max length/truncation
- replacing tokenizer without resizing embeddings

## Review Standard

A complete tokenizer change proves:

- old/new encodings are compared
- special tokens are explicit
- chat template is rendered
- save/reload works
- model embedding compatibility is checked
- offset mappings are checked when relevant
