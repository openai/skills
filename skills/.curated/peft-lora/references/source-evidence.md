# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. The skill should make a fresh agent able to run, debug, and review PEFT/LoRA workflows, not merely describe adapter concepts.

## Retrieved Sources

- `huggingface/peft`: examples and source around `LoraConfig`, `get_peft_model`, `PeftModel.from_pretrained`, EVA initialization, DoRA/offloading, non-transformer LoRA targets, and `merge_and_unload`.
- `artidoro/qlora`: QLoRA training script patterns using `bitsandbytes`, `prepare_model_for_kbit_training`, adapter-only checkpoint callbacks, target-module discovery, and adapter reload for generation.
- Mined package evidence: `peft` 0.18.0 source with compatibility branches around several `transformers` versions.

## Workflows Reflected In The Skill

### Target Module Discovery

PEFT examples show architecture-specific targets such as `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, and `down_proj`. They also show LoRA can apply outside transformer attention blocks. The skill therefore requires agents to inspect `model.named_modules()` and prove that configured targets exist before training.

### Quantized Training

QLoRA workflows combine 4-bit loading, `bitsandbytes`, compute dtype, device maps, and `prepare_model_for_kbit_training`. The skill covers quantization as a training contract, not an optimization afterthought:

- capture `bitsandbytes`, `transformers`, `peft`, `accelerate`, and `torch` versions;
- verify the model loads on the intended devices;
- run a tiny training smoke before a long job;
- keep adapter save/load separate from merged model export.

### Adapter Artifacts

The source workflows save adapter weights and reload them with `PeftModel.from_pretrained`. The skill therefore requires:

- base model id and revision;
- tokenizer and chat template notes;
- adapter config and checkpoint path;
- fresh-process reload;
- generation or prediction before and after merge when `merge_and_unload` is used.

### Nonstandard LoRA

Mined examples include non-transformer models and saved heads/modules. The skill must teach agents to identify when `modules_to_save`, classifier heads, embeddings, or output projections need to stay trainable.

## Review Standard

Reject PEFT/LoRA changes that only set a config. A useful workflow must prove trainable parameters, target-module match, dataset/tokenizer compatibility, adapter save/reload, and artifact ancestry. Version capture is required because PEFT, Transformers, bitsandbytes, and Accelerate interactions are version-sensitive.
