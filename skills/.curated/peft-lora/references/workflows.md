# PEFT and LoRA Workflows

Use this reference to complete adapter work end to end.

## Base and Adapter Contract

Record:

```text
base model id/path:
base revision:
adapter path or output path:
tokenizer/chat template:
task type:
quantization:
peft/transformers/torch/accelerate/bitsandbytes:
```

Adapters are not standalone unless merged. Treat the base model revision as part of the artifact.

## Target Module Discovery

List candidate modules:

```python
for name, module in model.named_modules():
    if "Linear" in type(module).__name__:
        print(name)
```

Choose target modules that match the architecture. Common LLM choices include attention projections and MLP projections, but names differ by model family.

## Dataset and Tokenization

Before training:

- Print one raw example.
- Print one formatted prompt.
- Tokenize and print `input_ids`, `attention_mask`, and `labels`.
- Confirm prompt/user tokens are masked when doing supervised instruction tuning.
- Confirm pad/eos settings match inference.

## Tiny Training Run

Run the smallest real training command:

```bash
python train.py --max_steps 2 --per_device_train_batch_size 1
```

Adapt to TRL, Accelerate, Axolotl, Unsloth, or the repo launcher. The run must save an adapter and reload it.

## QLoRA Checks

Check:

- `bitsandbytes` import works.
- compute dtype is explicit.
- quantization type is intentional.
- device map is compatible with training.
- the model is prepared for k-bit training when required.

## Merge and Export

Fresh process:

```python
from peft import PeftModel
base = AutoModelForCausalLM.from_pretrained(base_model)
model = PeftModel.from_pretrained(base, adapter_path)
model.eval()
```

If merging:

```python
merged = model.merge_and_unload()
merged.save_pretrained("merged-output")
tokenizer.save_pretrained("merged-output")
```

Run one sample before and after merge and preserve the unmerged adapter unless the user explicitly wants only merged weights.

## Final Artifact

Final notes should include:

```text
base model and revision:
adapter config:
target modules:
trainable parameter count:
tiny run command:
reload command:
merge status:
upload/privacy constraints:
```
