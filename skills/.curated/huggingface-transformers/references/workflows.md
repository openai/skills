# Hugging Face Transformers Workflows

Use these workflows when the basic `SKILL.md` checklist is not enough. Prefer the repository's existing scripts and config format; these recipes define the checks and artifacts that should exist by the end.

## Contents

- [Model Loading and Inference](#model-loading-and-inference)
- [Trainer and Accelerate Debugging](#trainer-and-accelerate-debugging)
- [Offline, Private, and Reproducible Loads](#offline-private-and-reproducible-loads)
- [Quantization and Memory](#quantization-and-memory)
- [Conversion and Export](#conversion-and-export)
- [PR Review Artifact](#pr-review-artifact)

## Model Loading and Inference

1. Record model identity: model id or path, `revision`, local cache behavior, `trust_remote_code`, and task class.
2. Load config first with `AutoConfig.from_pretrained(...)` and inspect `model_type`, architectures, vocab size, max positions, and special IDs.
3. Load tokenizer/processor and check special tokens before loading weights.
4. Load model with explicit dtype/device choices.
5. Run a tiny input and print decoded output or output shape.

Minimal causal LM check:

```python
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

model_id = "sshleifer/tiny-gpt2"
revision = None
config = AutoConfig.from_pretrained(model_id, revision=revision)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
model = AutoModelForCausalLM.from_pretrained(model_id, revision=revision)
inputs = tokenizer("hello", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=8)
print(config.model_type, len(tokenizer), tokenizer.decode(outputs[0], skip_special_tokens=True))
```

If this works but the target model does not, compare config class, tokenizer files, `revision`, auth, and remote code requirements.

## Trainer and Accelerate Debugging

1. Print dataset column names and one raw example.
2. Print one tokenized example with labels and masks.
3. Run `max_steps=2`, batch size 1, and no distributed launcher first.
4. Save a tiny checkpoint and reload it in a fresh process.
5. Only then restore distributed launch, mixed precision, gradient accumulation, and full dataset.

Common label checks:

- Causal LM labels should mask prompt/user tokens when doing instruction tuning.
- Seq2Seq labels should use `-100` for ignored positions.
- Classification labels must be integer class IDs unless the loss expects floats.
- Token classification labels must align with offset mappings or word IDs.

## Offline, Private, and Reproducible Loads

Record these before changing code:

```text
HF_HOME:
TRANSFORMERS_CACHE:
HF_HUB_OFFLINE:
local_files_only:
model id/path:
revision:
tokenizer files present:
```

For private or production loads, prefer:

```python
AutoTokenizer.from_pretrained(model_id, revision=revision, local_files_only=True)
AutoModelForCausalLM.from_pretrained(model_id, revision=revision, local_files_only=True)
```

Use `local_files_only=False` only when network access is intentional.

## Quantization and Memory

Debug order:

1. Confirm unquantized CPU or small-device load works.
2. Confirm dtype and device map.
3. Add quantization config.
4. Run one forward/generate call.
5. Save and reload if the workflow expects persisted artifacts.

Record:

```text
torch:
cuda:
transformers:
quantization package:
dtype:
device_map:
max memory:
input length:
```

## Conversion and Export

Before conversion:

- Compare source and target config fields.
- Compare state dict key counts and missing/unexpected keys.
- Check tied embeddings and vocab size.
- Check dtype and sharding.

After conversion:

```python
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained("converted-output")
tokenizer = AutoTokenizer.from_pretrained("converted-output")
print(model.__class__.__name__, len(tokenizer))
```

For ONNX/TorchScript/export tasks, run one inference with the exported artifact, not only the source model.

## PR Review Artifact

Include this in final notes or PR body:

```text
Task:
Model id/path:
Revision:
Versions:
Smoke command:
Smoke result:
Changed files:
Known version assumptions:
Residual risks:
```
