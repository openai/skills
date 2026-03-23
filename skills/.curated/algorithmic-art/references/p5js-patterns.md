# p5.js And Seeded Generative Patterns

Load this reference when the output will be a browser-based sketch, especially with p5.js or plain canvas.

## Reproducibility First

Always set the seed explicitly and route both noise and random generation through it.

```js
let seed = 12345;

function setup() {
  createCanvas(1200, 1200);
  randomSeed(seed);
  noiseSeed(seed);
}
```

## Parameter Discipline

Expose only parameters that materially change the aesthetic, such as:

- particle count
- noise scale
- velocity or damping
- palette selection
- stroke weight
- recursion depth

Avoid giant control panels with dozens of weak sliders.

## Good Output Shapes

- One self-contained HTML file with inline JS and controls
- One `.js` file plus a minimal HTML wrapper
- A rendered PNG or GIF plus the source that generated it

## Common System Families

- flow fields
- particle trails
- recursive subdivision
- circle packing
- harmonic or trigonometric interference
- cellular growth
- noise-driven line systems

Choose one family and make it excellent before combining systems.

## Refinement Checklist

- Is the composition readable at a glance?
- Does the seed create meaningful variation without breaking the system?
- Are the parameters few but powerful?
- Is the palette intentional?
- Does the code look like one coherent idea rather than several demos stitched together?
