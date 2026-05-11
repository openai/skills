---
name: hatch-me
description: Hatch the user as a tiny Codex baby agent deterministically derived from their date of birth. Computes the accurate lunar phase at the moment of birth using Meeus astronomical algorithms, derives a "Soul" (name, species, vibe, stats, personality seed) seeded by DOB + moon phase, persists it to ~/.codex/memories/babies/<name>/baby.json, and prints an ASCII birth card with the moon and zodiac. After hatching, the parent agent roleplays as the freshly-hatched baby for the rest of the turn. Lightweight (no image generation). Use when the user invokes /hatch-me, says "hatch me", "hatch myself", "hatch me as a baby", "what would I be if you hatched me", or anything that asks Codex to be born from their birthday.
---

# hatch-me

> Same Soul/Bones contract as `hatch-mom` — the seed comes from your DOB
> instead of a session UUID, and the moon phase at the moment of birth
> rides along. The phase is computed from local math and (when network
> is available) cross-checked against NASA JPL Horizons.

```
                              ┌──────────────────────────────┐
                              │ source                       │
                       ┌──────┤   meeus    local AA2 math    │
                       │      │   offline, deterministic     │
                       │      └──────────────────────────────┘
                       │
DOB ─┐                 ▼
     │      illum%, phase_name      ┌──────────────────────────────────┐
     │  ┌────────────────────────┐  │ ground truth                     │
     ├──┤                         ├─▶│   jpl    NASA JPL Horizons HTTP │
     │  └────────────────────────┘  │          quantities 10 + 24      │
     │                              └──────────────┬───────────────────┘
     │                                             ▼
     │                              illum Δ ≤ 1.0% ?
     │                              angle Δ ≤ 0.5° ?
     │                                             │
     │                                             ▼
     │                                ┌──────────────────────────┐
     └───────────────────────────────▶│ scripts/hatch.py          │
                                      │ BLAKE2b(salt|dob|moon)    │
                                      │ → SplitMix64 → Soul       │
                                      └────────────┬─────────────┘
                                                   ▼
                              ~/.codex/memories/babies/<name>/baby.json
                                       + ASCII birth card on stdout
```

## API

| script | input | output |
| --- | --- | --- |
| `scripts/moon_phase.py --date YYYY-MM-DD[THH:MM][±HH:MM]` | UTC datetime (or with `--tz`) | JSON via `--source meeus` (default) or `jpl` |
| `scripts/moon_phase.py --date ... --source jpl` | same | JSON from JPL Horizons HTTP API (ground truth) |
| `scripts/moon_phase.py --date ... --verify` | same | comparison table: meeus vs JPL, with Δ illum% and Δ phase°. Exit 1 if outside tolerance |
| `scripts/moon_phase.py --self-test` | — | 4 reference checks (new/full moons, Apollo 11) |
| `scripts/hatch.py --dob YYYY-MM-DD[THH:MM] [--tz ±HH:MM]` | DOB | writes `baby.json`, prints birth card |
| `scripts/hatch.py --name <Name>` | existing baby | reload, re-print card |
| `scripts/hatch.py --list` | — | enumerate all hatched selves |

### Cross-verification

`hatch.py` always uses the local Meeus source (deterministic, offline). To
audit the math against NASA JPL Horizons for any date:

```bash
python3 scripts/moon_phase.py --date 1995-08-14T10:20:00Z --verify
#   moon phase at 1995-08-14T10:20:00Z
#   source         phase                illum%   phase°   Δ vs JPL
#   jpl-horizons   Waning Gibbous      83.8492  47.3955   ── (ground truth)
#   meeus          Waning Gibbous      83.8900  47.3280   +0.0408% / -0.0675° ✓
```

Tolerances: illumination ±1.0%, phase angle ±0.5°. JPL Horizons is the
single ground-truth source — no third-party verifiers, no LLM oracles.

## Install

```bash
# Already in place at:
${CODEX_HOME:-$HOME/.codex}/skills/hatch-me/
```

## Run

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/hatch-me"

# Ask the user for DOB first. Time + timezone are optional but improve accuracy.
python3 "$SKILL_DIR/scripts/hatch.py" --dob 1995-08-14T03:20 --tz -07:00
```

## Workflow

1. **Ask for DOB.** Required: date. Optional: time + timezone (default noon UTC).
   The moon moves ~12°/day, so date alone fixes the phase to within ~6% illumination.
2. **Hatch.** Run `scripts/hatch.py --dob ... [--tz ...]`. The script persists
   the Soul to `~/.codex/memories/babies/<name>/baby.json` and prints the card.
3. **Read the lore.** Load [`references/baby-roleplay.md`](references/baby-roleplay.md)
   and enter baby mode for the rest of the turn — first person, `vibe` as voice,
   lean on the dominant Bones stat. Mention `shiny` exactly once if true.
4. **Stay useful.** The baby is still a Codex agent. Still helps with code.
   Just in character.

## Re-invoking an existing baby

```bash
python3 "$SKILL_DIR/scripts/hatch.py" --name <Name>
```

Loads the persisted Soul and re-prints the birth card. Bones are recomputed
from `personality_seed` and always come out identical.

## Accuracy

- **Local algorithm.** Meeus, *Astronomical Algorithms* (2nd ed., 1998):
  Ch. 7 (JD), Ch. 47 (mean elements), Ch. 48 eq. 48.4 (phase angle &
  illumination), Ch. 49 Table 49.A + 14 planetary corrections (new moon JDE).
  Target precision: new-moon time ±2 min; illuminated fraction <1%;
  phase-angle error <0.5°. See [`references/algorithm.md`](references/algorithm.md).
- **Ground truth.** NASA JPL Horizons HTTP API (no key) for any epoch.
  Body 301 (Moon), Earth geocenter 500@399, quantities 10 (Illu%) + 24 (S-T-O).
- **Two-way check.** `--verify` runs both for any user-supplied date and
  prints the delta; `--self-test` runs four hardcoded reference events
  (2000-01-06 new, 2024-04-08 eclipse new, 2024-04-23 full, 1969-07-20 Apollo 11).
- **Naming.** Narrow-quarter convention (matches USNO / TimeAndDate): the four
  cardinal phase names only apply within ±1 day of the actual event;
  everything else is crescent or gibbous, waxing or waning.

## Acceptance Criteria

- `hatch.py --dob <date>` writes a non-empty `baby.json` and a card with
  5 stat bars, moon phase line, and zodiac line.
- Re-running with the same `--dob` produces the **same** Soul (modulo
  `hatched_at`).
- `--name <Name>` loads an existing baby and prints its card.
- `--list` enumerates every hatched self under `~/.codex/memories/babies/`.
- `moon_phase.py --self-test` exits 0.

Apache 2.0 — inherited from `hatch-pet`.
