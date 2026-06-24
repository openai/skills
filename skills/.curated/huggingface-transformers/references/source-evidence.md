# Transformers Source Evidence Map

This reference records high-signal workflows retrieved from the mined `transformers` repository export and source checkout. Use it to keep the skill grounded in real repository practices.

## Contents

- [Retrieved Sources](#retrieved-sources)
- [Workflows Found in Source](#workflows-found-in-source)
- [New Model Implementation](#new-model-implementation)
- [Test Selection](#test-selection)
- [Pipeline Usage](#pipeline-usage)
- [Trainer and Accelerate](#trainer-and-accelerate)
- [Tokenizer and Processor Tests](#tokenizer-and-processor-tests)
- [Quantization Tests](#quantization-tests)
- [Remaining Coverage Gaps](#remaining-coverage-gaps)
- [Evidence-Grounded Review Standard](#evidence-grounded-review-standard)

## Retrieved Sources

- Repository checkout: `huggingface/transformers`, source revision observed locally as `0a8ab33f7a`.
- Mined export: `repository_library/exports/transformers/structured/repo_skills_miner.skills.jsonl` and annotations.
- Version evidence: source `transformers` reports `5.0.0.dev0`; dependency table includes `tokenizers>=0.22.0,<=0.23.0`, `torch>=2.2`, `accelerate>=1.1.0`, `safetensors>=0.4.3`, and `sentencepiece>=0.1.91,!=0.1.92`.

## Workflows Found in Source

### New Model Implementation

`CONTRIBUTING.md` describes a full new-model path:

- provide model information before implementation
- use the modular architecture pattern with `modular_<model_name>.py`
- add integration tests with exact output matching
- add docs/model card material including pipeline and `AutoModel` usage
- run impacted model tests, not the entire suite

The skill should therefore cover more than model loading. It must guide agents through new model integration, modular implementation, exact-output integration tests, docs, and targeted test commands.

### Test Selection

`AGENTS.md` and `CONTRIBUTING.md` emphasize targeted tests:

```bash
pytest tests/models/[name]/test_modeling_[name].py
pytest tests/models/[name]/test_processing_[name].py
pytest tests/models/[name]/test_tokenization_[name].py
RUN_SLOW=1 python -m pytest tests/models/my_new_model/test_my_new_model.py
```

The skill should tell agents not to run the entire test suite by default.

### Pipeline Usage

`README.md` includes pipeline patterns for:

- text generation
- chat-style text generation with dtype and `device_map`
- automatic speech recognition
- image classification
- visual question answering

The skill should include pipeline return-shape validation and when to drop below `pipeline` to `AutoProcessor`/`AutoModel`.

### Trainer and Accelerate

Source/docs show both `Trainer` and no-trainer Accelerate workflows. The skill should cover:

- `Trainer` for standard supervised training
- `Seq2SeqTrainer` generation kwargs
- `Accelerate` when a custom training loop needs distributed/mixed precision support
- tiny runs before distributed launch

### Tokenizer and Processor Tests

Mined annotations surfaced tokenizer tests such as `CTRLTokenizationTest`, `PerceiverTokenizationTest`, and processor tests such as `VideoLlama3ProcessorTest`. These point to required skill coverage:

- tokenizer save/load behavior
- special token edge cases
- processor input preparation for multimodal models
- truncation and vision-token risks

### Quantization Tests

Mined annotations surfaced quantization integration tests such as `QuantoQuantizationSerializationCudaTest` and `VptqConfigTest`. The skill should cover:

- CPU vs CUDA quantization behavior
- serialization/reload checks
- quantization config compatibility
- memory/runtime risks

## Remaining Coverage Gaps

The skill is much stronger than the original, but it is not complete unless it adds or preserves guidance for:

- implementing a new Transformers model in the repo's modular style
- adding or modifying tokenizers/processors with targeted tests
- multimodal processors and exact-output integration tests
- quantization config and serialization validation
- model card/documentation update expectations
- targeted test command selection

## Evidence-Grounded Review Standard

A complete Transformers skill should let a fresh agent handle these task classes:

```text
load/debug existing model:
pipeline inference:
Trainer fine-tuning:
Accelerate/custom loop:
tokenizer/processor change:
new model integration:
quantization/serialization:
conversion/export:
docs/model card:
targeted tests:
```
