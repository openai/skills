# PyTorch Mastery Notes

## Mental Model

PyTorch programs are contracts between tensors, modules, autograd, devices, and optimizer state. Most bugs are mismatches in shape, dtype, device, mode, or graph lifetime.

## Module State

Trainable state belongs in `nn.Parameter` or child modules. Non-trainable persistent tensors belong in buffers. Temporary tensors created in `forward` should not silently become trainable state.

## Autograd Pitfalls

- Calling `.item()` detaches a scalar.
- Appending losses without detaching can retain graphs.
- In-place ops can break gradients.
- `no_grad()` and `inference_mode()` are for inference paths.
- `model.eval()` changes dropout and batch norm behavior but does not disable gradients.

## Data Pipeline

Debug dataset and collate before debugging the model:

- one raw sample
- one collated batch
- tensor shapes/dtypes
- masks and padding
- label semantics

## Backend Differences

CUDA, CPU, and MPS can differ in dtype support, determinism, memory behavior, and kernel availability. Always report the backend used for validation.

## Review Standard

A complete PyTorch change proves:

- one real batch or inference path runs
- shape/dtype/device assumptions are visible
- loss and gradients are finite for training changes
- checkpoint/export reload works when touched
- memory changes are justified by measurement
