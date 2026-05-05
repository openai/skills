# Row Semantics

Use this file when defining the 9 animation rows before prompting image generation.

Global rule:

- each row must read at tiny UI size
- each row must be one loopable action
- if a row only works because of subtle face acting or tiny finger motion, redesign it

## Shared Design Heuristics

- Lead with silhouette and 2-3 strong state changes.
- Favor readable mechanics over nuanced acting.
- If a gesture is weak, convert it to a more binary motion rather than adding noise.
- For compact toy characters, “heavier” motion often reads better than athletic motion.

## Row 1: `idle`

What it is:

- a calm loop with one attitude change
- breathing, blink, eye slide, side-eye, head tilt, or similar small beats

What it is not:

- eight unrelated cute expressions
- a noisy acting showcase

Tiny-UI mechanic:

- one small facial or head-state change that loops cleanly

High-risk failure:

- extra legs in seated poses
- turning the row into generic “cute idle”

## Row 2: `running-right`

What it is:

- a cyclical rightward motion loop
- either true travel or a deliberate forced-motion concept

What it is not:

- a one-way dash or process shot
- a pose series that never closes back to frame 1

Tiny-UI mechanic:

- big body lean, clear leg separation, readable motion direction

High-risk failure:

- collapsing into generic run when the intended action was something else

## Row 3: `running-left`

What it is:

- the leftward counterpart of row 2

What it is not:

- a lazy mirror if the character concept requires different body logic

Tiny-UI mechanic:

- same as row 2, but still readable when the UI flips or alternates states

High-risk failure:

- scale or hair logic drifting away from the rightward row

## Row 4: `waving`

What it is:

- a communication row
- wave, beckon, salute, point, or other character-specific callout

What it is not:

- automatically a friendly hello
- subtle finger animation that disappears when the pet is small

Tiny-UI mechanic:

- use a gesture with strong hand-state contrast
- if needed, prefer `open hand -> closed hand` or `raise -> pull` over micro finger curls

High-risk failure:

- the gesture reads as nothing at small size
- the gesture says the wrong thing, for example “stop” instead of “come here”

## Row 5: `jumping`

What it is:

- a loop with anticipation, lift, apex, descent, impact, and recovery

What it is not:

- automatically an athletic or celebratory jump

Tiny-UI mechanic:

- make compression and impact readable
- for heavy characters, a low hop, forced shock, or flat flop may read better than a tall leap

High-risk failure:

- the row becomes too tall, floaty, or gymnast-like

## Row 6: `failed`

What it is:

- an unmistakable “this did not work” loop

What it is not:

- generic sadness
- random bug vibes without a readable failure mechanic

Tiny-UI mechanic:

- the failure must be obvious by silhouette or prop logic
- examples: mismatch, jam, tangle, stuck state, short deadpan recoil

High-risk failure:

- it becomes emotionally vague instead of instantly readable

## Row 7: `waiting`

What it is:

- impatient idle
- foot tap, weight shift, look-around, narrowed eyes, or similar annoyance loop

What it is not:

- just another neutral standing pose

Tiny-UI mechanic:

- one readable impatience mechanic

High-risk failure:

- standing scale stretches vertically
- the row loses its character and becomes generic idle

## Row 8: `running`

What it is:

- an active energetic loop distinct from rows 2 and 3
- can be sprint, repeated work, or repeated busy motion if that fits the character

What it is not:

- visually redundant with the directional rows

Tiny-UI mechanic:

- pick one active repeated action and make the rhythm obvious

High-risk failure:

- row meaning overlaps too strongly with travel rows

## Row 9: `review`

What it is:

- reading, inspecting, evaluating, or thinking

What it is not:

- a detailed prop showcase that only works when zoomed in

Tiny-UI mechanic:

- use very simple readable props
- keep book, glasses, device, or tool shapes chunky and clear

High-risk failure:

- prop clutter overwhelms the character
