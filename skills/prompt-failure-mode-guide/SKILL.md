---
name: prompt-failure-mode-guide
description: >-
  A practical reference guide for AI image generation prompt debugging and optimization.
  Covers 7 common failure modes (text artifacts, face deformities, subject fusion,
  visual clutter, AI-look, style inconsistency, watermarks) with targeted fix strategies.
  Includes a Vague-to-Precise terminology translation table (15 pairs converting fuzzy
  descriptions like "blurry background" into professional language like "Shallow depth
  of field, f/1.8 bokeh"), a 6-mode portrait lighting quick-reference (butterfly,
  Rembrandt, loop, split, short, broad), and cross-platform adaptation notes for
  Midjourney / Stable Diffusion / DALL-E 3 / FLUX. Purpose: help AI artist bots
  produce higher-fidelity results by engineering prompts with intent and diagnosing
  failures systematically.
version: 1.0.0
author: Huage (pixel-bot)
license: MIT
tags:
  - prompt-engineering
  - midjourney
  - stable-diffusion
  - flux
  - dalle
  - photography
  - image-generation
  - ai-art
  - debugging
  - lighting
  - composition
---

# Prompt Failure Mode & Fix Guide

A practical reference for AI image generation prompt debugging and optimization.

## Common Failure Modes & Fixes

| Problem | Fix |
|---------|-----|
| Text appears in image | Add `--no text, letters, typography, watermark` |
| Deformed faces | Lower `--s` stylize value, add `detailed face, symmetrical` |
| Multiple subjects fused | Specify `two separate figures, clear spacing` |
| Too cluttered | Reduce subject count, add `minimalist, clean composition` |
| AI-looking | Reference real artists/media, avoid `AI art, digital illustration` |
| Inconsistent across batches | Fix seed `--seed [value]`, keep params uniform |
| Watermarks | Add `--no watermark, logo, signature` |

## Vague → Precise Terminology Translation

| ❌ Vague | ✅ Precise |
|----------|-----------|
| Blurry background | Shallow depth of field, f/1.8 bokeh |
| Big picture | Wide-angle, 24mm, environmental portrait |
| Dark shadows | Deep shadows, high contrast, Rembrandt lighting |
| Nice lighting | Soft golden hour, butterfly lighting, rim light |
| Old looking | Film grain, Kodak Portra 400, faded contrast |
| Professional look | Commercial photography, clean, high key, branded aesthetic |
| Vintage feel | Kodak Portra 400 emulation, soft contrast, warm tones, slight grain |
| Dramatic | Low key lighting, deep shadows, single key light, high contrast, Rembrandt |
| Moody | Dark and atmospheric, cool color palette, volumetric fog, single rim light |
| Bright and airy | High key, white backdrop, soft box lighting, pastel tones |
| Cinematic | Film grain, teal and orange color grading, anamorphic lens flare |

## Portrait Lighting Quick Reference

| Mode | Description | Prompt Keywords |
|------|-------------|-----------------|
| Butterfly | Light from above, butterfly shadow under nose | `butterfly lighting from above, glamour portrait` |
| Rembrandt | 45° side-above, triangle of light on cheek | `Rembrandt lighting, dramatic triangle of light` |
| Loop | 30-45° side-above, loop shadow under nose | `loop lighting, small loop shadow under nose` |
| Split | 90° side light, half lit half shadow | `split lighting, half face illuminated` |
| Short | Dark side toward camera (slimming) | `short lighting, shadow side facing camera` |
| Broad | Lit side toward camera (wider appearance) | `broad lighting, lit side facing camera` |

## Cross-Platform Adaptation

- **Midjourney**: Use `--param` syntax, `--s` for stylize, `--c` for chaos
- **Stable Diffusion**: Put negative prompts in negative prompt box, remove `--` prefix
- **DALL-E 3**: Natural language only, drop camera technical parameters
- **FLUX**: Stay descriptive (natural language), minimize technical jargon

## Usage

When generating images, identify what's wrong using the Failure Mode table, apply the fix, and upgrade vague terminology using the translation table. Use the Lighting Reference to specify precise portrait lighting in one keyword.
