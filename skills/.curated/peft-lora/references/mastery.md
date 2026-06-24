# PEFT and LoRA Mastery Notes

## Mental Model

PEFT trains small adapter weights around a frozen or mostly frozen base model. The adapter is only meaningful with the exact base model, tokenizer, and task formatting used to train it.

## Artifact Types

- **Adapter only**: small, depends on base model.
- **Merged model**: larger, can often be loaded without PEFT but may inherit base license/privacy constraints.
- **Quantized training setup**: memory-saving path, not always merge/export compatible.

## Target Module Strategy

Target modules must match real module names. Good choices usually affect attention and/or MLP projections. Bad choices produce zero useful learning or no trainable parameters.

## Training Quality Risks

- all labels masked
- wrong chat template
- tokenizer pad/eos mismatch
- target modules absent
- adapter inactive at inference
- base revision drift
- quantized merge unsupported

## Review Standard

A complete adapter change proves:

- base model/revision recorded
- tokenizer/chat template recorded
- trainable parameters are nonzero
- tiny training or adapter-load smoke succeeds
- adapter reloads in a fresh process
- merge status and upload safety are explicit
