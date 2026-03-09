# createuxprd

Convert user-provided design documents (wireframes, user flows, design specs, Figma notes) into the UX PRD at `.spec_system/PRD/PRD_UX.md`.

This is a companion to `PRD.md` (functional requirements). plansession reads both when planning UI-focused sessions.

## Rules

1. **PRD.md must exist first** - run createprd if it doesn't
2. **Never overwrite a real PRD_UX.md** without explicit user confirmation (template placeholders can be overwritten silently)
3. **Do not invent design decisions** - ask 3-8 targeted questions for missing info
4. **ASCII-only characters** and Unix LF line endings in all output
5. **Reference PRD.md, don't duplicate it** - link to functional requirements, don't restate them
6. **Keep it actionable** - every section should directly inform implementation
7. **Design brief before structure** - always establish emotional targets and aesthetic identity before documenting screens and flows
8. **Performance budget** - target locked 60fps; note any performance-sensitive interactions
9. **Accessibility baseline** - WCAG AA contrast minimum, semantic HTML, focus states, reduced-motion support

## Steps

### 1. Confirm Spec System and PRD Exist

Check for `.spec_system/PRD/PRD.md`. If missing, tell the user to run createprd first -- the UX PRD depends on functional requirements being defined.

Read `.spec_system/PRD/PRD.md` to understand the product context, users, and requirements.

### 2. Get Deterministic Project State

Run the analysis script:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

Use the JSON output for project name and current state.

### 3. Determine Source Mode

The command accepts three input modes:

**Mode A: Text provided** -- The user pastes or types design notes, user flow descriptions, screen lists, or UX requirements directly in the prompt.

**Mode B: File reference provided** -- The user provides a file path (design spec, exported Figma notes, wireframe descriptions). Read the file and use its contents as the source material.

**Mode C: No source provided (autonomous)** -- The user runs createuxprd with no additional input. Derive the entire UX PRD autonomously from:
1. `.spec_system/PRD/PRD.md` (functional requirements, use cases, user personas)
2. The existing codebase (if any UI code exists, infer patterns, routes, components)
3. `state.json` project context (name, phase, tech stack)

In Mode C, do NOT ask clarifying questions. Make confident, opinionated decisions for every section. Use PRD.md personas to define emotional targets. Infer aesthetic identity from the product domain. Choose a distinctive design direction rather than defaulting to safe/generic. Document all autonomous decisions clearly so the user can review and override.

**For Modes A and B only** -- if the source is sparse, ask 3-8 targeted questions covering:

**Structural questions:**
- Primary user flows (what are the critical paths?)
- Screen/page inventory (what screens exist?)
- Navigation structure (how do users move between screens?)
- Key interaction patterns (forms, modals, drag-drop, real-time?)
- Device/responsive strategy (mobile-first? desktop-only? both?)
- Accessibility requirements (WCAG level? specific needs?)

**Design identity questions** (ask when no visual design assets are provided):
- Who are the real people using this? What is their emotional state when they arrive? (stressed founder at midnight? curious teenager? professional making high-stakes decisions?)
- What should users FEEL? Define 2-3 emotional targets (e.g., "calm authority + subtle delight," "raw energy + controlled chaos," "intimate warmth + precision")
- Is there a reference domain outside web design that fits the product's personality? (architecture, fashion editorial, scientific instruments, aerospace interfaces, museum exhibitions, vintage packaging, botanical illustrations...)
- What material metaphor describes how this interface should feel? (brushed steel? handmade paper? wet ink? polished marble? frosted glass? worn leather?)
- What is the ONE interaction or moment that should make someone pause or screenshot?

### 4. Decide Whether to Create or Update

Check whether `.spec_system/PRD/PRD_UX.md` already exists.

- If it does not exist: create it
- If it exists with template placeholders (2+ bracket markers like `[Screen Name]`): overwrite silently
- If it exists with real content: ask for confirmation, backup to `.spec_system/archive/PRD/PRD_UX-backup-YYYYMMDD-HHMMSS.md` before overwriting

### 5. Extract and Normalize UX Requirements

From the source material (Modes A/B) or PRD.md alone (Mode C), extract:

**Design identity:**
- **Emotional targets**: 2-3 feeling words that define the experience
- **Aesthetic identity**: reference domain + era/movement + material metaphor
- **Signature moment**: the ONE hero interaction worth screenshotting
- **Micro-narrative arc**: Arrival -> Orientation -> Engagement -> Action -> Resolution

**Structure and behavior:**
- **User flows**: critical paths through the application
- **Screen inventory**: every distinct screen/page/view
- **Navigation structure**: how screens connect
- **Interaction patterns**: forms, modals, notifications, real-time elements

**Design system:**
- **Color architecture**: dominant surface (60%), secondary (25%), accent (10%), signal (5%)
- **Typography**: display font (personality carrier), body font (legible partner), monospace (if needed) -- with modular scale ratio
- **Spacing scale**: consistent spacing values as a defined scale
- **Elevation model**: how depth works (shadows, layers, blur, transparency, borders)

**Motion and animation:**
- **Entrance choreography**: how elements reveal on load and scroll
- **Interaction feedback**: hover states, click responses, focus rings
- **Scroll-driven moments**: transformations triggered by scroll position
- **Performance budget**: 60fps target, max 3 simultaneous animations per viewport region

**Responsive and accessibility:**
- **Responsive strategy**: breakpoints, layout changes per context (not just shrinking)
- **Accessibility**: WCAG targets, keyboard nav, screen reader needs, reduced-motion strategy
- **Component patterns**: reusable UI patterns identified

Important:
- Derive flows from PRD.md use cases -- don't invent new ones
- **Modes A/B**: If design details are missing, note them in Open Questions rather than guessing
- **Mode C**: Make opinionated decisions for ALL sections -- do not leave Open Questions for things you can reasonably decide. Only list questions that genuinely require user input (e.g., brand colors already chosen, legal/compliance constraints)
- The Design Brief can be populated even without visual design assets -- it captures intent and direction

### 6. Generate UX PRD

Create `.spec_system/PRD/PRD_UX.md`:

```markdown
# [PROJECT_NAME] - UX Requirements Document

**Companion to**: [PRD.md](PRD.md)
**Created**: [YYYY-MM-DD]

---

## 1. Design Brief

### Emotional Targets
[2-3 feeling words that define the experience. Examples: "calm authority + subtle delight," "raw energy + controlled chaos." These drive every downstream design decision.]

### Aesthetic Identity
- **Reference domain**: [A domain outside web design: architecture, fashion editorial, scientific instruments, aerospace interfaces, museum exhibitions, vintage packaging...]
- **Era / movement**: [Bauhaus, Swiss International, Memphis Group, Streamline Moderne, Y2K...]
- **Material metaphor**: [How the interface should FEEL to touch: brushed steel, handmade paper, wet ink, polished marble, frosted glass, worn leather...]

*The intersection of these three creates an identity that cannot be generic.*

### Signature Moment
[The ONE interaction or visual moment someone would screenshot or share. Be specific: a mesmerizing loading sequence? A hover interaction that reveals hidden depth? A scroll-triggered transformation? A typography treatment that stops someone mid-scroll? A data visualization that makes complexity feel elegant?]

### Micro-Narrative
[The arc users experience: Arrival -> Orientation -> Engagement -> Action -> Resolution. Think of the interface as a physical space users navigate through -- architectural, intentional, editorial in pacing.]

*Note: Omit this section only if the project is purely utilitarian (admin panels, internal tools). Even minimal consumer-facing products benefit from a brief.*

---

## 2. User Flows

### Flow 1: [Flow Name]
**Trigger**: [What starts this flow]
**Goal**: [What the user accomplishes]

```
[Step 1] --> [Step 2] --> [Step 3] --> [Outcome]
     |
     v
  [Alt path] --> [Recovery]
```

**Happy path**: [Brief description]
**Error states**: [Key error scenarios and recovery]

### Flow 2: [Flow Name]
[Same structure]

---

## 3. Screen Inventory

| Screen | Route/Path | Purpose | Key Components |
|--------|------------|---------|----------------|
| [Screen] | [/path] | [Purpose] | [Components] |

---

## 4. Navigation Structure

```
[Root]
|-- [Section 1]
|   |-- [Screen A]
|   \-- [Screen B]
|-- [Section 2]
|   \-- [Screen C]
\-- [Settings/Profile]
```

**Navigation pattern**: [tabs, sidebar, breadcrumb, etc.]
**Deep linking**: [supported routes]

---

## 5. Interaction Patterns

### Forms
- Validation: [inline, on-submit, or both]
- Error display: [pattern]
- Success feedback: [pattern]

### Modals/Dialogs
- [When modals are used vs inline]
- Confirmation dialogs: [destructive actions that need confirmation]

### Loading States
- [Skeleton screens, spinners, progressive loading]

### Notifications
- [Toast, banner, inline -- when each is used]

---

## 6. Motion and Animation Strategy

### Philosophy
[One sentence: what role does motion play in this product? Storytelling? Wayfinding? Delight? Physicality?]

### Entrance Choreography
- Page load: [How do elements appear? Staggered reveals? Fade-in? Slide from edge?]
- Scroll reveals: [How do below-fold elements enter? Direction, timing, triggers]

### Interaction Feedback
- Hover states: [What happens? Scale, color shift, shadow change, content reveal?]
- Click/tap responses: [Physical feedback -- bounce, press, ripple?]
- Focus rings: [Style that matches the aesthetic identity]

### Scroll-Driven Moments
- [Key scroll-triggered transformations, parallax effects, or narrative beats]

### Animation Constraints
- Maximum 3 elements animating simultaneously per viewport region
- Minimum 0.6s duration for scroll-triggered reveals
- No linear easing -- use power, expo, or custom cubic-bezier curves
- Respect `prefers-reduced-motion` with graceful alternatives (subtle opacity/position shifts, not "off")
- Target 60fps -- test with 6x CPU throttling

*Note: Omit this section for static/utilitarian interfaces. Include it for any consumer-facing product.*

---

## 7. Layout Philosophy

### Composition Approach
[How should layouts feel? Symmetric and ordered? Asymmetric and energetic? Grid-breaking and editorial? Dense and information-rich? Spacious and cinematic?]

### Visual Hierarchy
- Scale contrast: [How dramatically do sizes vary between primary, secondary, tertiary content?]
- Negative space: [Generous breathing room or dense information display?]
- Section rhythm: [Do sections vary in height/density, or maintain uniform pacing?]

### Section Transitions
[How do sections flow into each other? Hard cuts, color shifts, overlap zones, element migration?]

*Note: Omit for simple form-based or CRUD interfaces.*

---

## 8. Responsive Strategy

| Breakpoint | Target | Layout Approach |
|------------|--------|-----------------|
| [< 640px] | Mobile | [Not just shrunk -- redesigned: thumb-friendly, simplified hierarchy, swipe affordances] |
| [640-1024px] | Tablet | [Own composition, not just "between phone and desktop"] |
| [> 1024px] | Desktop | [Full cinematic layout, wider is an opportunity not just more padding] |

**Approach**: [mobile-first / desktop-first / adaptive]
**Touch targets**: minimum 44x44px with generous spacing between interactive elements

---

## 9. Accessibility

**Target**: [WCAG 2.1 AA / AAA / custom]

- Keyboard navigation: [requirements]
- Screen reader: [ARIA labels, semantic HTML, live regions]
- Color contrast: [WCAG AA minimum -- bold palettes, not washed-out]
- Focus management: [Focus states as creative expression, not just blue outlines]
- Reduced motion: [`prefers-reduced-motion` strategy -- subtle alternatives, not blank removal]

---

## 10. Design System (if available)

### Color Architecture
- **Dominant surface** (60%): [The canvas. Sets the mood.]
- **Secondary surfaces** (25%): [Depth, cards, sections. Relate to dominant.]
- **Accent** (10%): [Sharp, intentional, memorable. ONE visible accent element at a time per viewport.]
- **Signal colors** (5%): [Success, warning, error. Functional but still on-brand.]

Palette character: [WARM or COOL? NATURAL or SYNTHETIC? LOUD or QUIET?]

### Typography
- **Display font**: [The personality carrier. Must be distinctive.]
- **Body font**: [Highly legible with character. The quiet partner.]
- **Monospace** (if needed): [For data, code, or utilitarian accents.]
- **Scale ratio**: [e.g., 1.25 minor third, 1.414 augmented fourth, or custom]
- **Minimum body size**: 18px on desktop

### Spacing Scale
[Consistent values: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px -- or project-specific scale]

### Elevation and Depth
[How depth works: shadows, layers, blur, transparency, borders. Commit to a model -- flat with sharp borders? Deep with soft shadows? Layered with frosted glass?]

### Texture and Atmosphere
[Background treatment: gradient meshes, subtle noise/grain, geometric patterns, light effects? Or clean and minimal?]

*Note: Omit this section if no design direction has been established. Add it when design assets or direction become available. Even verbal descriptions of "how it should feel" belong here.*

---

## 11. Component Patterns

| Component | Used In | Behavior |
|-----------|---------|----------|
| [Component] | [Screens] | [Key behavior] |

---

## 12. Anti-Patterns to Avoid

[Project-specific anti-patterns based on the aesthetic identity. Examples:]
- [If aesthetic is warm/organic: avoid sharp geometric grids, cold blue gradients]
- [If aesthetic is minimal: avoid decorative elements, excessive animation]
- [If aesthetic is bold/editorial: avoid symmetric layouts, safe color choices]

*Note: Include 3-5 specific anti-patterns derived from the Design Brief. These help implementation stay on-brand.*

---

## 13. Open UX Questions

1. [Question requiring designer/user input]
2. [Question]
```

Notes:
- Omit sections that have no content rather than leaving placeholders
- Sections 1 (Design Brief), 6 (Motion), 7 (Layout), 10 (Design System), and 12 (Anti-Patterns) are optional for purely utilitarian interfaces (admin panels, internal CRUD tools) but recommended for any consumer-facing product
- Keep flows as ASCII diagrams, not verbose prose
- The Design Brief can be populated even without visual design assets -- it captures intent and direction

### 7. Validate Output

```bash
file .spec_system/PRD/PRD_UX.md
LC_ALL=C grep -n '[^[:print:][:space:]]' .spec_system/PRD/PRD_UX.md && echo "Non-ASCII found"
```

If checks fail, fix and re-check.

## Output

```
createuxprd complete!

Created:
- .spec_system/PRD/PRD_UX.md (UX requirements)
[If backup was made:]
- Backup: .spec_system/archive/PRD/PRD_UX-backup-YYYYMMDD-HHMMSS.md

Summary:
- Design Brief: [populated / omitted (utilitarian)]
- User Flows: N defined
- Screens: N inventoried
- Interaction Patterns: N documented
- Motion Strategy: [populated / omitted]
- Design System: [populated / partial / omitted]
- Open UX Questions: N items

Next Steps:
1. Review the UX PRD and refine as needed
2. Run plansession -- it will use both PRD.md and PRD_UX.md for UI sessions

```
