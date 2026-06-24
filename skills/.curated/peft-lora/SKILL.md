---
name: peft-lora
description: Fine-tune, debug, merge, evaluate, or export parameter-efficient adapters for LLMs and diffusion models with PEFT, LoRA, QLoRA, TRL, Axolotl, Unsloth, or Accelerate. Use when working with adapter configs, target modules, quantized training, adapter composition, checkpoint merging, or low-memory fine-tuning.
---

# PEFT and LoRA

Use this skill for parameter-efficient fine-tuning. Preserve the base model contract first: tokenizer, chat template, quantization config, target modules, and adapter checkpoint layout must line up.

## Validated Version Evidence

This guidance was checked against a mined `peft` source checkout at `peft` 0.18.0. That source contains version-sensitive branches for `transformers` around 4.33.0, 4.53.1, 4.54.0.dev0, and 4.56.0, and depends on `accelerate`, `torch`, `safetensors`, `bitsandbytes`, `transformers`, `datasets`, and related training packages.

Before changing adapter code or configs, capture the active stack:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["peft", "transformers", "torch", "accelerate", "bitsandbytes", "datasets", "safetensors"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to make adapter training, loading, merging, or export reproducible. A complete run produces:

- A base-model/adaptor compatibility record: base model id, revision, tokenizer/chat template, adapter type, and package versions.
- A trainable-parameter count proving the intended modules are unfrozen.
- A tiny train or inference smoke test.
- A fresh-process reload of the saved adapter or merged artifact.
- Notes on whether the final artifact is an adapter, merged model, quantized model, or private-base-dependent artifact.

## Standalone Quick Start

When the repo lacks a smoke test, verify adapter attachment with the smallest model or the user's target model:

```python
from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

base_model = "sshleifer/tiny-gpt2"
model = AutoModelForCausalLM.from_pretrained(base_model)
config = LoraConfig(r=8, lora_alpha=16, target_modules=["c_attn"], lora_dropout=0.05)
model = get_peft_model(model, config)
model.print_trainable_parameters()
```

The `c_attn` target is for the tiny GPT-2 smoke model. For the user's target model, list module names and choose real linear layers from that architecture:

```python
for name, module in model.named_modules():
    if "Linear" in type(module).__name__:
        print(name)
```

## Workflow

1. Identify the base model, adapter method, training framework, quantization mode, and expected output artifact.
2. Inspect current package versions and GPU memory before changing configs.
3. Validate the dataset formatting and tokenizer behavior on a few examples.
4. Run a tiny train/eval smoke before launching a long job.
5. Test loading the saved adapter separately from training.

Check trainable parameters before any real run:

```python
if hasattr(model, "print_trainable_parameters"):
    model.print_trainable_parameters()
else:
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"trainable params: {trainable:,} / {total:,} ({trainable / total:.4%})")
assert any(p.requires_grad for p in model.parameters())
```

## Configuration Checks

- Confirm `base_model_name_or_path` and adapter checkpoint ancestry.
- Match `target_modules` to actual module names in the model.
- Set LoRA rank, alpha, dropout, bias, and task type intentionally.
- For QLoRA, verify bitsandbytes availability, compute dtype, quantization type, and device map.
- For chat models, preserve the chat template and special tokens used during training.
- For sequence classification or embedding tasks, confirm the head/pooling layer is trainable if needed.

## Training Guidance

- Prefer the repo's existing launcher: raw PEFT, TRL, Axolotl, Unsloth, or Accelerate.
- Use small max steps and a tiny dataset slice for the first verification run.
- Watch for loss becoming `nan`, no trainable parameters, frozen target modules, or empty labels.
- Log effective batch size: per-device batch size, gradient accumulation, process count, and sequence length.
- Save adapter config, tokenizer files, training config, and evaluation notes together.

## Merge and Export

- Load the base model and adapter in a fresh process before merge/export.
- Run one generation or prediction before and after merge.
- Keep both unmerged adapter and merged artifact when practical.
- Document whether the merged model is safe to upload, quantized, or tied to a private base checkpoint.

Fresh-process reload contract:

```text
base model:
base revision:
adapter path:
peft/transformers/torch:
trainable parameter count:
sample prompt/input:
pre-merge output:
post-merge output, if merged:
```

## References

Open `references/workflows.md` for detailed adapter target-module discovery, QLoRA setup, dataset formatting, tiny training runs, merge/export checks, and artifact review.

Open `references/mastery.md` for PEFT/LoRA mental models, adapter artifact contracts, quantization interactions, target module strategy, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

## Common Failure Modes

- `target_modules` do not match after a model architecture or library version change.
- Tokenizer pad/eos settings differ between train and inference.
- Quantized weights are accidentally merged or saved in an unsupported format.
- Adapter loads but has no effect because it is inactive or attached to the wrong base model.
- Adapter checkpoint cannot be reproduced because base model revision, tokenizer files, or chat template were not pinned with it.
- Training appears to run but all labels are masked.

## Done Criteria

- Trainable parameter count is checked.
- A tiny training run completes or the inference-only adapter load path is tested.
- The final adapter or merged model can be loaded in a fresh process.
- The final notes state exactly which artifact should be kept, uploaded, or treated as private-base-dependent.
