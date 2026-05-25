# sculpt-ui

Guide the creation of distinctive, production-grade frontend interfaces with high design quality.
Run this workflow step before building any frontend component, page, or application to establish
a design brief, micro design system, and implementation strategy that avoids generic AI output.

## Rules

1. **Read-only on spec system** - Never modify state.json, session specs, or task checklists
2. **Design brief first** - Always complete Phase 1 before writing code
3. **ASCII only** - All generated files use characters 0-127, no emoji or smart quotes
4. **Performance budget** - Target locked 60fps; test with 6x CPU throttling in DevTools
5. **Accessibility baseline** - WCAG AA contrast minimum, semantic HTML, focus states, reduced-motion support

## Steps

### 1. Design Intelligence (ALWAYS do this first)

Before writing a single line of code, build a **Design Brief** by thinking through these layers:

#### The Human Layer
- **Who is here?** Not "users" -- real people. A stressed founder checking metrics at midnight? A curious teenager exploring for the first time? A professional making a high-stakes decision? Their emotional state shapes everything.
- **What should they FEEL?** Define 2-3 emotional targets. Examples: "calm authority + subtle delight," "raw energy + controlled chaos," "intimate warmth + precision." This emotional palette drives every decision downstream.
- **What is the micro-narrative?** Every great interface has an arc: Arrival -> Orientation -> Engagement -> Action -> Resolution. Map the key moments. Think of the interface as a physical space the user navigates through -- architectural, intentional, almost editorial in its pacing -- not a flat page they scan.

#### The Aesthetic Identity
Do not pick from a list -- CONSTRUCT a unique identity by combining:
- **A primary reference domain** (outside of web design): architecture, fashion editorial, vinyl record sleeves, scientific instruments, Japanese packaging, brutalist concrete, Art Nouveau ironwork, aerospace interfaces, museum exhibitions, vintage pharmacy labels, racing liveries, botanical illustrations...
- **An era or movement**: Bauhaus, Memphis Group, Swiss International, Psychedelic 60s, Y2K, Acid Graphics, De Stijl, Constructivism, Streamline Moderne, Ukiyo-e...
- **A material metaphor**: Does this interface feel like brushed steel? Handmade paper? Wet ink? Polished marble? Stretched canvas? Frosted glass? Worn leather?

The intersection of these three inputs creates something that cannot be generic. A "Swiss International + aerospace instruments + brushed aluminum" interface is fundamentally different from "Memphis Group + Japanese packaging + wet ink."

#### The Signature Moment
Every interface needs ONE thing someone will screenshot or share. Define it explicitly:
- A mesmerizing loading sequence?
- A hover interaction that reveals hidden depth?
- A scroll-triggered transformation that recontextualizes the page?
- A typography treatment so beautiful it stops someone mid-scroll?
- A data visualization that makes complexity feel elegant?

This is your hero. Everything else supports it.

### 2. Design System Foundation

Build a micro design system BEFORE implementing components. This invisible architecture makes bold choices feel intentional rather than chaotic.

#### Type Scale and Typography as Visual Object
Define a modular type scale (e.g., 1.25 ratio, 1.414 ratio, or custom). Choose:
- **Display font**: The personality carrier. Must be distinctive -- pull from Google Fonts deeper catalog, variable fonts, or characterful choices. NEVER default to overused favorites. Consider: Fraunces, Instrument Serif, Playfair Display, Space Mono, Anybody, Bricolage Grotesque, Syne, Crimson Pro, Outfit, Cormorant, Darker Grotesque, Climate Crisis, Unbounded... but also do not converge on these -- explore and vary every time.
- **Body font**: Highly legible but with character. The quiet partner.
- **Monospace** (if needed): For data, code, or utilitarian accents.

**CRITICAL MINDSET SHIFT**: Typography is not just content delivery -- it is a visual and spatial element. Oversized text IS the layout. Words can be compositional anchors, kinetic objects, texture, negative space. Consider: text that acts as background at massive scale, headlines that ARE the hero instead of sitting next to one, letter-spacing and weight as scroll-driven variables, text as mask for imagery or color. The best interfaces make you notice the words as visual form before you read them as language.

#### Color Architecture
- **Dominant surface** (60%): The canvas. Sets the mood.
- **Secondary surfaces** (25%): Depth, cards, sections. Relate to dominant.
- **Accent** (10%): The punctuation. Sharp, intentional, memorable.
- **Signal colors** (5%): Functional -- success, warning, error. Still on-brand.
- Define as CSS custom properties with semantic names, not just color values.
- Consider: Does the palette feel WARM or COOL? NATURAL or SYNTHETIC? LOUD or QUIET?

**Accent restraint rule**: Limit accent color to ONE visible element at a time within any viewport. Accent gains its power from scarcity -- if everything is highlighted, nothing is. Multiple simultaneous accents create visual noise; a single accent creates a focal point.

#### Spacing and Rhythm
Use a consistent spacing scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px) as CSS variables. Generous whitespace is not emptiness -- it is breathing room that makes content sing. Cramped interfaces feel cheap; spacious ones feel confident.

#### Elevation and Depth
Define how depth works in your system: shadows, layers, blur, transparency, borders. Commit to a model -- flat with sharp borders? Deep with soft shadows? Layered with frosted glass? Flat with color-shift depth?

### 3. Implementation Craft

#### Layout as Composition
Think like a graphic designer or architect, not a Bootstrap user:
- **Break the grid intentionally**: Overlap elements. Use asymmetric columns. Let images bleed. Create diagonal flow with transforms.
- **Negative space is a design element**: The emptiest areas of your layout should feel as intentional as the fullest.
- **Visual hierarchy through scale contrast**: Make important things BIG. Make supporting things small. Avoid the mediocre middle where everything is roughly the same size.
- **Consider the viewport as a canvas**: The fold, the edges, the scroll depth -- all are compositional tools.
- **Asymmetry as intentional placement**: Elements should not be centered by default. Every element should feel PLACED with purpose -- pushed to a margin, offset from center, anchored to an edge. Symmetry is a choice, not a fallback. The asymmetry should create energy and direct the eye.
- **Vary spatial rhythm dramatically**: Not every section should be the same height or density. Some sections should breathe with massive whitespace; others should be dense and information-rich. The variation itself creates pacing and narrative.

#### Section Transitions as Choreography
Sections should NOT end with hard cuts. Transitions between content areas happen through:
- **Color shifts**: Background color evolving over scroll distance, not switching abruptly
- **Element migration**: Objects from one section traveling into the next, creating continuity
- **Overlap zones**: Content from adjacent sections sharing viewport space briefly during scroll
- **Atmospheric changes**: Texture, grain, or depth shifting gradually to signal a new context

This is what separates editorial-quality interfaces from template-assembled pages.

#### Motion as Storytelling
Motion should have PURPOSE, PHYSICS, and DISCIPLINE:

**Entrance choreography**: Stagger reveals with `animation-delay` to create a narrative sequence. The eye should be guided, not overwhelmed. One well-orchestrated page entrance > 50 scattered animations.

**Interaction feedback**: Hover states, click responses, focus rings -- these should feel PHYSICAL. Elements should have weight, resistance, elasticity.

**Scroll-driven narrative**: Use `scroll-timeline`, `IntersectionObserver`, or scroll-triggered classes to create moments of transformation as the user moves through content. Scroll is a storytelling medium -- treat it as the user's way of pacing through a physical space.

**Animation Discipline Rules** (these prevent motion from becoming noise):
- **Maximum 3 elements animating simultaneously** in the same viewport region. More than this overwhelms the eye and tanks performance.
- **Minimum 0.6s duration** for any scroll-triggered reveal. Anything faster reads as a glitch, not an animation.
- **Never use linear easing.** Always use power, expo, or custom cubic-bezier curves. Linear motion looks mechanical and cheap.
- **Easing philosophy**: Ease-out for entrances (arriving with energy, settling into place). Ease-in for exits (gathering energy, departing). Ease-in-out for state transitions. Custom cubic-beziers for personality.
- **Entrance vectors matter**: Elements should NOT always enter from directly below their final position. Use diagonals, rotations, scale changes, and lateral movement. Predictable entrance directions are a hallmark of template animation.
- **Decorative elements must respond to scroll or interaction.** Static decorative elements feel dead. If a geometric shape or line exists on the page, it should move, scale, rotate, or change opacity in response to something.

Prefer CSS-only animation for HTML artifacts. Use Motion/Framer Motion for React when available. Use GSAP with ScrollTrigger for scroll-driven animation when the complexity warrants it.

#### Advanced Techniques to Employ
Push beyond basics. These create the "how did they do that" moments:
- `clip-path` for non-rectangular reveals and morphing shapes
- `mix-blend-mode` and `background-blend-mode` for depth and texture
- CSS `mask-image` for gradient fades and pattern masks
- `backdrop-filter` for frosted glass and environmental blur
- SVG filters (`feTurbulence`, `feDisplacementMap`) for organic textures
- `@property` for animatable custom properties (gradient animations, color transitions)
- `container queries` for truly responsive component-level art direction
- `scroll-snap` for controlled scroll experiences
- Custom `cursor` styles that match the aesthetic
- `text-shadow` and layered `box-shadow` for dimensional type and surfaces
- CSS `conic-gradient` and `radial-gradient` for complex backgrounds
- `@font-face` with `font-display: swap` and variable font axes
- CSS Grid with `subgrid` for precise nested alignment
- View Transitions API for page-level morphing (when supported)
- SplitText-style character/word-level animation for typographic sequences

#### Texture and Atmosphere
Flat, solid-color backgrounds are a missed opportunity. Create atmosphere:
- **Gradient meshes**: Multiple radial gradients layered for organic color fields
- **Noise/grain**: Subtle SVG noise overlays add analog warmth (use SVG `feTurbulence`)
- **Geometric patterns**: Repeating SVGs, CSS patterns, or generated backgrounds
- **Photographic elements**: Blurred, color-shifted, or masked imagery as atmospheric layers
- **Light effects**: Subtle glows, ambient reflections, or spotlight effects that respond to interaction

### 4. Quality Standards

#### Performance-Conscious Animation
Beautiful AND fast -- these are not in tension when done right:
- Prefer CSS over JS for visual effects wherever possible
- Apply `will-change: transform` ONLY to elements currently animating -- add it before animation begins, remove it via `onComplete` callback. Permanent `will-change` on many elements consumes GPU memory for no benefit.
- Use CSS containment (`contain: layout style paint`) on pinned or independently-scrolling sections to isolate rendering work
- Batch identical animations (e.g., `ScrollTrigger.batch()` for card grids, logo strips)
- Lazy-initialize animation controllers for content below the fold -- do not set up scroll listeners for elements the user may never reach
- Target locked 60fps -- test with 6x CPU throttling in DevTools. If frames drop, reduce concurrent animations first, then simplify easing curves
- Lazy-load heavy elements below the fold
- Font loading optimization
- Use modern image formats, appropriate sizes, `loading="lazy"`

#### Accessibility as Creative Constraint
Accessibility is not a checkbox -- it is a design discipline that produces BETTER work:
- Color contrast ratios (WCAG AA minimum) force you to choose bolder, more intentional palettes
- Focus states become another surface for creative expression -- make them beautiful, not just visible
- Semantic HTML creates clean, maintainable structure
- Reduced motion preferences (`prefers-reduced-motion`) should have their own elegant experience, not just "turn everything off" -- consider subtle opacity transitions or position shifts that respect the preference while maintaining design quality
- Screen reader text and ARIA labels are invisible craft -- do them well

#### Responsive as Adaptive Design
Do not just shrink things. Redesign for each context:
- Mobile should feel native to mobile -- thumb-friendly targets, swipe affordances, simplified hierarchy
- Tablet gets its own composition -- not just "between phone and desktop"
- Large screens are an opportunity for cinematic layouts, not just wider containers
- Horizontal scroll sections should become vertical stacks on mobile with modified (not just disabled) animations
- Touch targets: minimum 44x44px, with generous spacing between interactive elements

### 5. Anti-Pattern Awareness

Avoid these not because they are on a list, but because they signal LACK OF THOUGHT:
- Same font appearing across multiple generations (if you notice yourself reaching for the same font, STOP and explore)
- Card grids with identical border-radius and padding (cards are not the only container)
- Purple/blue gradients as a default "modern" look
- Centered-everything layouts with symmetric padding (asymmetry creates energy; centering should be a deliberate choice, not a default)
- Icon libraries used without modification (customize, recolor, resize beyond defaults)
- Drop shadows as the only depth mechanism
- Hero sections that are just big text + button + gradient background
- Animations with linear easing (always use power/expo curves)
- Animations that complete instantly -- if it is worth animating, it is worth giving time to breathe
- More than 3 elements animating simultaneously in the same viewport area
- Elements always entering from directly below (use diagonals, rotations, scale)
- Uniform section heights -- vary dramatically to create pacing
- Hard cuts between sections instead of choreographed transitions
- White/light gray backgrounds with blue accents (the unofficial colorway of AI demos)
- Decorative elements that do not move or respond to anything -- dead ornaments
- Sans-serif body text smaller than 18px on desktop
- Stock photography or placeholder image boxes when CSS/SVG visuals would be more distinctive

The test: If you removed the content and just looked at the structure and styling, could you tell this was designed for THIS specific context? If not, push further.

## Output

After running this workflow step, you will have:
- A Design Brief documenting emotional targets, aesthetic identity, and signature moment
- A micro design system (type scale, color architecture, spacing, depth model)
- An implementation strategy with layout composition, motion choreography, and advanced techniques
- Code that targets 60fps, WCAG AA accessibility, and responsive adaptive design

The standard: Every interface should make someone pause and think, "this feels like it was designed by a human who cares deeply." Every pixel, every transition, every font choice should feel intentional.
