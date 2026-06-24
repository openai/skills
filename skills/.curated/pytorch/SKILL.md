---
name: pytorch
description: Build, debug, train, evaluate, or optimize PyTorch models. Use when working with torch tensors, nn.Module code, Dataset/DataLoader pipelines, autograd, CUDA/MPS devices, distributed training, mixed precision, checkpointing, model export, or performance and memory issues in PyTorch projects.
---

# PyTorch

Use this skill for PyTorch code paths. First understand the tensor shapes, device placement, and training/evaluation mode boundaries; most PyTorch bugs are contract bugs around those three areas.

## Validated Version Evidence

This guidance was checked against a mined PyTorch source checkout at commit `e2dc2224743`, with `requires-python = ">=3.10"` and `sympy>=1.13.3`, plus downstream locked environments using `torch` 2.9.1. PyTorch behavior is highly version-, device-, and backend-sensitive, so capture the active runtime before debugging:

```bash
python - <<'PY'
import torch
print("torch", torch.__version__)
print("cuda available", torch.cuda.is_available())
print("cuda runtime", getattr(torch.version, "cuda", None))
print("mps available", getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
PY
```

## What This Skill Delivers

Use this skill to make a PyTorch path correct and reproducible. A complete run produces:

- A version/device report for `torch`, CUDA/MPS, and the active accelerator.
- A tiny batch or inference smoke test that exercises the repo's real model/data path.
- A diagnosis of the failing contract: shape, dtype, device, mode, gradient, memory, checkpoint, or export.
- A minimal code/config change plus the command that verifies it.

## Standalone Quick Start

If the repo has no obvious test, create a temporary smoke path around the existing `model`, `loader`, and `criterion`. For pure inference modules, run one forward pass and print output shape:

```python
model.eval()
with torch.inference_mode():
    output = model(example.to(device))
print(tuple(output.shape) if hasattr(output, "shape") else type(output))
```

For training code, use the finite-loss/gradient check below before changing architecture.

## Workflow

1. Inspect the local stack and available accelerators:

```bash
python - <<'PY'
import torch
print("torch", torch.__version__)
print("cuda", torch.cuda.is_available())
print("mps", getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
PY
```

2. Locate model construction, data loading, loss computation, optimizer/scheduler setup, and checkpoint save/load code.
3. Trace one tiny batch end to end before changing architecture or training logic.
4. Prefer focused tests or smoke scripts that assert shapes, dtypes, devices, and finite losses.

Use a minimal batch smoke check when the project has a loader, model, and criterion available:

```python
model.train()
batch = next(iter(loader))
inputs, labels = batch
outputs = model(inputs.to(device))
loss = criterion(outputs, labels.to(device))
assert torch.isfinite(loss), loss
loss.backward()
assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
```

Adapt the unpacking to the repo's batch structure; the point is to verify the real data contract, not to create a separate synthetic path.

## Model Code

- Keep `nn.Module` state in registered modules, parameters, or buffers.
- Avoid creating new trainable tensors inside `forward` unless that is intentional and tested.
- Make input and output shape contracts explicit near complex modules.
- Use `model.train()` and `model.eval()` deliberately around dropout, batch norm, and evaluation.
- Keep random seeds and deterministic settings in test or experiment entrypoints, not hidden in library code.

## Data and Training

- Validate dataset item structure before debugging the model.
- Check collate behavior for variable-length inputs, padding, masks, and label dtypes.
- Ensure loss functions receive the expected logits/probabilities and target dtype.
- Call `optimizer.zero_grad()` in the intended place and verify gradients are finite.
- For mixed precision, use the repo's existing AMP pattern; do not mix multiple scaler strategies.

## Device, Memory, and Performance

- Move tensors and modules to the same device at clear boundaries.
- For CUDA OOM, reduce batch/sequence size first, then inspect activation checkpointing, dtype, gradient accumulation, and retained graph references.
- Use `torch.no_grad()` or `torch.inference_mode()` for inference-only paths.
- Profile only after correctness is established.

Memory triage order:

1. Reproduce with batch size 1.
2. Print tensor shapes and dtypes at the failing boundary.
3. Check accidental graph retention (`losses.append(loss)` instead of `loss.item()`).
4. Only then add checkpointing, lower precision, accumulation, or model surgery.

## Checkpointing and Export

- Save enough state to resume: model, optimizer, scheduler, scaler, epoch/step, config, and RNG state when needed.
- Load checkpoints with explicit device mapping.
- For TorchScript, ONNX, or `torch.export`, add a small exported-model smoke test.

## References

Open `references/workflows.md` for detailed recipes covering model/data contract debugging, training loops, memory triage, distributed runs, checkpointing, export, and PR review artifacts.

Open `references/mastery.md` for PyTorch mental models, module/state rules, autograd pitfalls, data pipeline design, backend differences, and review standards.

Open `references/source-evidence.md` when reviewing whether the skill covers workflows observed in the PyTorch repository evidence.

## Done Criteria

- A tiny batch or minimal inference path runs locally.
- Shape, dtype, and device assumptions are verified or documented.
- Training changes include a loss/gradient sanity check where practical.
- The final notes state the exact device/backend and the command used to prove the path.
