# Hugging Face Transformers Mastery Notes

This reference gives an agent the conceptual map needed to work effectively with `transformers` without assuming the user already knows the library.

## Contents

- [Mental Model](#mental-model)
- [Choosing APIs](#choosing-apis)
- [Artifact Anatomy](#artifact-anatomy)
- [Tokenizer and Model Compatibility](#tokenizer-and-model-compatibility)
- [Generation Behavior](#generation-behavior)
- [Trainer Stack](#trainer-stack)
- [Accelerate and Distributed Runs](#accelerate-and-distributed-runs)
- [Quantization](#quantization)
- [Common Breaking Boundaries](#common-breaking-boundaries)
- [Review Checklist](#review-checklist)

## Mental Model

Transformers projects are built from a small set of artifact contracts:

- **Config**: architecture and model hyperparameters. Usually loaded with `AutoConfig`.
- **Tokenizer or processor**: converts user data into model tensors. Text uses `AutoTokenizer`; multimodal uses `AutoProcessor` or task-specific processors.
- **Model class**: task-specific `AutoModel*` wrapper or model-specific class.
- **Generation config**: decoding behavior for generation models.
- **Weights**: PyTorch, safetensors, TensorFlow, Flax, or sharded checkpoints.
- **Training/eval script**: `Trainer`, `Seq2SeqTrainer`, `Accelerate`, or custom loop.

Most failures come from a mismatch between these artifacts, not from the model code itself.

## Choosing APIs

Use `Auto*` classes by default:

| Task | Preferred class |
|---|---|
| causal language modeling | `AutoModelForCausalLM` |
| seq2seq generation | `AutoModelForSeq2SeqLM` |
| classification | `AutoModelForSequenceClassification` |
| token classification | `AutoModelForTokenClassification` |
| embeddings/features | `AutoModel` or library-specific embedding wrapper |
| multimodal | `AutoProcessor` plus model-specific `AutoModel*` |

Use model-specific classes only when the repo already does, or when the model requires methods not exposed by the auto class.

## Artifact Anatomy

Expected files often include:

```text
config.json
generation_config.json
tokenizer.json
tokenizer_config.json
special_tokens_map.json
vocab/merges or sentencepiece model
model.safetensors or pytorch_model.bin
model.safetensors.index.json for sharded checkpoints
preprocessor_config.json for vision/audio/multimodal models
```

If a saved model cannot reload, inspect missing files before changing code.

## Tokenizer and Model Compatibility

Always compare:

```python
len(tokenizer)
model.get_input_embeddings().weight.shape[0]
tokenizer.pad_token_id
tokenizer.eos_token_id
tokenizer.bos_token_id
getattr(tokenizer, "chat_template", None)
```

If tokens are added, resize embeddings and save the model/tokenizer pair together. If the chat template changes, generated behavior can change even when token IDs do not.

## Generation Behavior

Generation output depends on:

- prompt formatting
- chat template
- tokenizer special tokens
- `max_new_tokens` vs `max_length`
- sampling parameters
- stopping criteria
- KV cache behavior
- dtype and device

When output quality is the issue, print the exact rendered prompt before changing model settings.

## Trainer Stack

`Trainer` handles boilerplate but hides important contracts:

- dataset column names
- data collator behavior
- label masking
- distributed launcher
- mixed precision
- save/eval/logging cadence

Before changing trainer code, run a tiny dataset through preprocessing and inspect one batch. A successful `Trainer` run with bad labels is still a broken result.

## Accelerate and Distributed Runs

Distributed failures can come from launch configuration rather than code. Record:

```text
accelerate config:
process count:
mixed precision:
gradient accumulation:
device map:
FSDP/DeepSpeed config:
```

Debug single-process first unless the bug is explicitly distributed-only.

## Quantization

Quantized loading affects:

- supported devices
- merge/export support
- dtype assumptions
- adapter training compatibility
- save format

Do not assume a quantized model can be merged, exported, or uploaded in the same way as full precision weights.

## Common Breaking Boundaries

- `transformers` and `tokenizers` version ranges.
- `trust_remote_code` model classes changing behavior.
- Hub `revision` moving when not pinned.
- private model auth missing in CI or production.
- old tokenizer artifacts with newer model configs.
- `pad_token_id` absent for batching.
- sequence length exceeding model limit.

## Review Checklist

Use this checklist before finalizing a Transformers change:

```text
versions captured:
model id/path and revision pinned:
config loaded:
tokenizer/processor loaded:
special tokens checked:
tiny input run:
realistic input run:
artifact save/reload checked, if applicable:
offline/private behavior documented:
trust_remote_code documented:
```
