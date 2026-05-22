# PyTorch Workflows

Use these workflows when the task needs implementation detail beyond the entry checklist.

## Contents

- [Model and Data Contract](#model-and-data-contract)
- [Shape, Dtype, Device Debugging](#shape-dtype-device-debugging)
- [Training Loop](#training-loop)
- [Memory Triage](#memory-triage)
- [Checkpoint Contract](#checkpoint-contract)
- [Export Contract](#export-contract)
- [Final Artifact](#final-artifact)

## Model and Data Contract

Trace one batch through the real loader and model:

```python
batch = next(iter(loader))
print(type(batch), batch)
model = model.to(device)
model.train()
inputs, labels = batch
outputs = model(inputs.to(device))
loss = criterion(outputs, labels.to(device))
print("outputs", getattr(outputs, "shape", type(outputs)), "loss", loss.item())
```

If the batch is a dict, preserve names and move tensors key by key. Do not invent a synthetic path unless the bug is isolated to a layer.

## Shape, Dtype, Device Debugging

Add temporary prints at boundaries:

```python
def describe(name, x):
    print(name, tuple(x.shape), x.dtype, x.device)
```

Check:

- Inputs and labels are on the same device as the model.
- Loss receives logits vs probabilities as expected.
- Classification targets are `torch.long`; regression targets are floating point.
- Masks are boolean or numeric as expected by the module.

## Training Loop

Correctness order:

1. Zero gradients.
2. Forward pass.
3. Finite loss assertion.
4. Backward pass.
5. Finite gradient assertion.
6. Optimizer step.
7. Scheduler step only in the repo's intended place.

Minimal guard:

```python
assert torch.isfinite(loss), loss
loss.backward()
for name, p in model.named_parameters():
    if p.grad is not None:
        assert torch.isfinite(p.grad).all(), name
```

## Memory Triage

1. Reproduce at batch size 1.
2. Reduce sequence/image size.
3. Disable graph retention in logging.
4. Add `torch.inference_mode()` for inference.
5. Try AMP or lower dtype.
6. Add gradient accumulation/checkpointing.
7. Profile only after the path is correct.

## Checkpoint Contract

Save:

```python
{
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "scheduler": scheduler.state_dict() if scheduler else None,
    "scaler": scaler.state_dict() if scaler else None,
    "step": step,
    "config": config,
}
```

Reload in a fresh process with explicit `map_location`.

## Export Contract

For ONNX, TorchScript, or `torch.export`, run a real inference through the exported artifact and compare shape and a small numeric tolerance against eager output.

## Final Artifact

Final notes should include:

```text
torch/backend versions:
device:
batch shape:
loss/gradient result:
checkpoint/export path:
command run:
residual risks:
```
