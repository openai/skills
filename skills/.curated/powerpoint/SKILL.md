---
name: powerpoint
description: Use when the task involves reading, creating, or editing `.pptx` presentations where layout and formatting matter; prefer `python-pptx` for programmatic access and LibreOffice for visual review.
---

# PowerPoint Skill

## When to use
- Create new presentations with slides, text, images, tables, and charts.
- Read or review existing PPTX content where layout matters.
- Modify presentations while preserving formatting.
- Extract text or content from slides for analysis.

## Workflow
1. Confirm the file type and goals (create, edit, analyze, extract).
2. Use `python-pptx` for all programmatic access.
3. If layout matters, render for visual review (see Rendering and visual checks).
4. After each meaningful change, re-render and inspect the slides.
5. Save outputs and clean up intermediate files.

## Temp and output conventions
- Use `tmp/pptx/` for intermediate files; delete when done.
- Write final artifacts under `output/pptx/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install python-pptx
```
If `uv` is unavailable:
```
python3 -m pip install python-pptx
```
System tools (for rendering):
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## Rendering and visual checks
If LibreOffice and Poppler are available, render slides for visual review:
```
soffice --headless --convert-to pdf --outdir $OUTDIR $INPUT_PPTX
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

If rendering tools are unavailable, ask the user to review the output locally.

## Slide layouts
| Index | Layout Name | Use Case |
|-------|-------------|----------|
| 0 | Title Slide | Opening/section slides |
| 1 | Title and Content | Bullet points |
| 5 | Title Only | Custom content |
| 6 | Blank | Full custom layout |

## Primary tooling

### Create presentation
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Title"
slide.placeholders[1].text = "Subtitle"
prs.save('output.pptx')
```

### Add bullet slide
```python
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Slide Title"
tf = slide.placeholders[1].text_frame
tf.text = "First bullet"
p = tf.add_paragraph()
p.text = "Second bullet"
p.level = 1
```

### Add image
```python
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.shapes.add_picture("image.png", Inches(1), Inches(1), height=Inches(3))
```

### Add table
```python
table = slide.shapes.add_table(rows, cols, left, top, width, height).table
table.cell(0, 0).text = "Header"
```

### Add shape
```python
from pptx.enum.shapes import MSO_SHAPE
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
shape.text = "Shape text"
```

### Add chart
See [references/charts.md](references/charts.md) for chart creation (bar, line, pie charts).

### Extract text
```python
prs = Presentation("input.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                print(para.text)
```

## Quality expectations
- Maintain consistent formatting: typography, spacing, and slide hierarchy.
- Avoid rendering issues: clipped text, overlapping elements, or broken layouts.
- Charts, tables, and images must be properly aligned and labeled.
- Use ASCII hyphens only. Avoid U+2011 and other Unicode dashes.

## Final checks
- Render and inspect slides before delivery when possible.
- Confirm layout, spacing, and content are correct.
- Remove temp files after final approval.
