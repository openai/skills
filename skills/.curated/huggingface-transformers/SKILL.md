---
name: huggingface-transformers
description: Build, debug, fine-tune, evaluate, or ship models with Hugging Face Transformers. Use when working with AutoModel/AutoTokenizer, pipelines, generation configs, model cards, Trainer or Accelerate integration, model conversion, quantization, multimodal processors, or Transformers examples.
---

# Hugging Face Transformers

Use this skill for projects built on `transformers`. Prefer official APIs and the repo's existing model-loading conventions over one-off loading code.

## Validated Version Evidence

This guidance was checked against a mined `transformers` source checkout at `transformers` 5.0.0.dev0, plus locked downstream environments using `transformers` 4.57.6 and 5.0.0. The source checkout declares `tokenizers>=0.22.0,<=0.23.0`, `torch>=2.2`, `accelerate>=1.1.0`, `safetensors>=0.4.3`, and `sentencepiece>=0.1.91,!=0.1.92`.

Before changing version-sensitive model loading, capture the active stack:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["transformers", "tokenizers", "torch", "accelerate", "huggingface-hub", "safetensors", "sentencepiece"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to leave the user with one of these concrete outcomes:

- A model/tokenizer load path that works in the target environment.
- A minimal inference, training, evaluation, conversion, or export smoke test.
- A diagnosis that names the exact failing compatibility boundary: model id, revision, config, tokenizer, dtype, device, dependency version, or artifact layout.
- A small code change that follows the repo's existing Transformers pattern and includes a repeatable verification command.

Do not stop at general advice. Produce or run the smallest command that proves the model path works.

## Standalone Quick Start

When the repo does not already provide a smoke command, create one in the task context or run it inline with a tiny public model unless the user has supplied a private model:

```bash
python - <<'PY'
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "sshleifer/tiny-gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
inputs = tokenizer("Transformers smoke test:", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=8)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
PY
```

For classification-style models, use `AutoModelForSequenceClassification` and assert logits shape. For seq2seq, use `AutoModelForSeq2SeqLM`. For multimodal projects, use `AutoProcessor` and the model-specific `AutoModel*` class already used by the repo.

## Workflow

1. Identify the task: inference, training, evaluation, conversion, serving, or debugging.
2. Inspect installed versions and local dependencies before changing code:

```bash
python - <<'PY'
import transformers, torch
print("transformers", transformers.__version__)
print("torch", torch.__version__)
PY
```

3. Locate the model family, tokenizer/processor, and config path. Check whether the project uses `Auto*` classes, model-specific classes, or custom code.
4. Make the smallest change that preserves existing checkpoints, config names, and tensor shapes.
5. Validate with a tiny input, then a realistic input.

When model loading is the risk area, record the exact model id/path, `revision`, cache location, and whether loading is allowed to hit the network. For reproducible or private deployments, prefer pinned revisions and explicit `local_files_only` behavior over implicit Hub defaults.

## Decision Rules

- If the failure happens before weights load, inspect dependency versions, auth, cache, `revision`, `trust_remote_code`, and config class first.
- If the model loads but output is wrong, inspect tokenizer special tokens, chat template, padding/truncation, generation config, and preprocessing.
- If training runs but quality is broken, inspect dataset columns, label construction, masking, collator behavior, and whether the saved tokenizer/config match training.
- If export or conversion fails, compare config fields, state dict keys, tensor shapes, tied embeddings, dtype, and target runtime support.
- If memory is the blocker, reduce batch/sequence length first; then inspect dtype, `device_map`, quantization, activation checkpointing, KV cache, and retained tensors.

## Inference

- Use `AutoTokenizer`, `AutoProcessor`, `AutoConfig`, and `AutoModel*` unless model-specific APIs are already used.
- Set `trust_remote_code` only when necessary and make the risk visible.
- Keep generation parameters in a config object or named dictionary, not scattered across call sites.
- For GPU memory issues, check dtype, device map, quantization, batch size, sequence length, and KV cache behavior.
- For pipelines, verify task names and return shapes; pipeline abstractions can hide tokenizer/model mismatch.
- For offline or cached execution, inspect `HF_HOME`, `TRANSFORMERS_CACHE`, `HF_HUB_OFFLINE`, and any project-specific cache settings before changing code.

Minimal load contract for PR notes or debugging output:

```text
model_id/path:
revision:
transformers/tokenizers/torch:
trust_remote_code:
dtype/device/device_map:
input shape:
output shape or generated text:
```

## Training and Fine-Tuning

- Prefer existing `Trainer`, `Seq2SeqTrainer`, `Accelerate`, or custom loop conventions in the repo.
- Validate dataset columns before wiring a trainer.
- Confirm tokenizer padding/truncation and label masking for causal language modeling or seq2seq tasks.
- For distributed training, inspect launch commands and environment variables before changing code.
- Save tokenizer, processor, config, generation config, and model weights together.

Before a long training run, force a tiny run that completes end to end:

```bash
python train.py --max_steps 2 --per_device_train_batch_size 1
```

Adapt the command to the repo's launcher. If no launcher exists, add a minimal smoke path that tokenizes two examples, runs one forward/backward pass, saves to a temp directory, and reloads the artifact.

## Conversion and Compatibility

- When converting weights, compare config fields, state dict keys, tensor shapes, and tied embeddings.
- Pin model revision or source checkpoint when reproducibility matters.
- Add a smoke test that loads the converted artifact and runs one forward pass.
- Preserve model card metadata when publishing or repackaging.

## References

Open `references/workflows.md` when the task needs detailed recipes for model loading, inference, Trainer/Accelerate debugging, conversion/export, caching/offline behavior, quantization, or PR review artifacts.

Open `references/mastery.md` when the task requires broader Transformers reasoning: API selection, artifact anatomy, generation behavior, model/tokenizer compatibility, training stack choices, and version-sensitive pitfalls.

Open `references/source-evidence.md` when reviewing whether the skill covers the workflows observed in the mined `transformers` repository evidence.

## Debugging Checklist

- Tokenizer/model vocab size mismatch.
- Model download works locally but fails in CI or production because auth, cache, `revision`, or offline settings differ.
- Missing `pad_token`, wrong chat template, or wrong special token IDs.
- Incorrect dtype or device placement.
- Sequence length exceeding model or rotary embedding limits.
- Labels not shifted or masked correctly.
- Config changes not saved with the model artifact.

## Done Criteria

- The model/tokenizer load path is explicit and reproducible.
- A tiny inference or training smoke test runs.
- Any version, revision, dtype, quantization, or trust boundary assumption is documented in code or the PR notes.
- The final answer names the exact command run and the observed output shape, generated text, or failure boundary.
