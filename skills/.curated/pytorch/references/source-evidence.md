# PyTorch Source Evidence Map

This reference records high-signal workflows retrieved from the PyTorch source checkout and repository-library export. Use it to keep the skill grounded in real repository practices.

## Retrieved Sources

- Repository checkout: `pytorch/pytorch`, source revision observed locally as `e2dc2224743`.
- Version evidence: `requires-python = ">=3.10"` and `sympy>=1.13.3`; downstream mined environments included `torch` 2.9.1.
- Source documents consulted: `README.md`, `CONTRIBUTING.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, and `test/HowToWriteTestsUsingFileCheck.md`.

## Workflows Found in Source

### Targeted Testing

PyTorch contributor docs warn against running broad test suites by default. High-signal patterns:

```bash
python test/test_torch.py TestTorch.test_specific_case
python test/test_jit.py TestJit.test_Sequential
pytest test/test_nn.py -k Loss -v
```

The skill should tell agents to create a standalone reproduction first, then run targeted tests.

### Test Structure

Source guidance uses:

```python
from torch.testing._internal.common_utils import run_tests, TestCase
```

It also recommends:

- `assertEqual` for tensor equality
- `@parametrize` for multiple inputs
- `instantiate_device_type_tests` for device-generic numeric tests

The skill should include this for PyTorch repo changes, not only user-model debugging.

### Architecture Map

Repository docs identify major areas:

- `aten/`: tensor library foundation without autograd
- `torch/csrc/autograd/`: reverse-mode automatic differentiation
- `torch/csrc/distributed/`: distributed training
- `tools/autograd/derivatives.yaml`: gradient definitions
- `test/`: Python frontend tests
- `test/cpp`: C++ tests

The skill should help agents route changes to the correct subsystem.

### Config and Compile Workflows

`CLAUDE.md` recommends `torch._dynamo.config.patch` for temporary config changes in tests. This indicates the skill should include `torch.compile`/Dynamo config patching as a first-class workflow for modern PyTorch debugging.

### FileCheck

`test/HowToWriteTestsUsingFileCheck.md` shows PyTorch uses FileCheck for graph/compiler optimization tests. The skill should cover this when tasks involve JIT, generated graphs, or compiler passes.

## Remaining Coverage Gaps

The current skill covers end-user PyTorch model debugging better than it covers PyTorch-repository contribution workflows. It is not complete unless it adds guidance for:

- targeted PyTorch repo tests
- `TestCase`, `run_tests`, `assertEqual`, `parametrize`, and device-generic tests
- subsystem routing across ATen, autograd, distributed, compiler, Python frontend, and C++ tests
- `torch.compile`/Dynamo config patching
- FileCheck for graph/compiler tests
- C++ extension or C++ test boundaries when relevant

## Evidence-Grounded Review Standard

A complete PyTorch skill should let a fresh agent handle:

```text
end-user model/data debugging:
training loop correctness:
checkpoint/export:
memory/performance:
distributed/mixed precision:
PyTorch repo bug fix:
device-generic tests:
compiler/FileCheck tests:
targeted test selection:
```
