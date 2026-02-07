---
name: powerpoint
description: Create, read, and edit PowerPoint (.pptx) presentations using python-pptx. Use when Codex needs to work with PowerPoint files for: (1) Creating new presentations, (2) Adding slides with text, bullet points, images, shapes, or tables, (3) Modifying existing presentations, (4) Extracting text or content from slides, (5) Adding charts or diagrams, (6) Working with slide layouts and placeholders, or any other PowerPoint tasks.
metadata:
  short-description: Create and edit PowerPoint presentations
---

# PowerPoint Skill

Create, read, and update PowerPoint (.pptx) files using the `python-pptx` library.

## Installation

```bash
pip install python-pptx
```

## Quick Start

### Create a New Presentation

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
```

### Standard Slide Layouts

| Index | Layout Name | Use Case |
|-------|-------------|----------|
| 0 | Title Slide | Opening/section slides |
| 1 | Title and Content | Bullet points |
| 5 | Title Only | Custom content |
| 6 | Blank | Full custom layout |

## Common Operations

### Title Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Presentation Title"
slide.placeholders[1].text = "Subtitle text"
prs.save('output.pptx')
```

### Bullet Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Slide Title"
tf = slide.placeholders[1].text_frame
tf.text = "First bullet"
p = tf.add_paragraph()
p.text = "Second bullet"
p.level = 1  # Indent level (0-8)
```

### Add Text Box

```python
from pptx.util import Inches, Pt

slide = prs.slides.add_slide(prs.slide_layouts[6])
left = top = Inches(1)
width = Inches(4)
height = Inches(1)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame
tf.text = "Text content"
tf.paragraphs[0].font.size = Pt(24)
tf.paragraphs[0].font.bold = True
```

### Add Image

```python
from pptx.util import Inches

slide = prs.slides.add_slide(prs.slide_layouts[6])
left = Inches(1)
top = Inches(2)
# Width auto-calculated to maintain aspect ratio
pic = slide.shapes.add_picture("image.png", left, top, height=Inches(3))
```

### Add Table

```python
from pptx.util import Inches

slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Data Table"

rows, cols = 3, 4
left, top = Inches(1), Inches(2)
width, height = Inches(8), Inches(2)
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Set column widths
for col in table.columns:
    col.width = Inches(2)

# Add data
table.cell(0, 0).text = "Header 1"
table.cell(1, 0).text = "Row 1 Data"
```

### Add Shape

```python
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches

slide = prs.slides.add_slide(prs.slide_layouts[6])
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(1), Inches(1),  # left, top
    Inches(3), Inches(1.5)  # width, height
)
shape.text = "Shape text"
```

Common shapes: `RECTANGLE`, `ROUNDED_RECTANGLE`, `OVAL`, `CHEVRON`, `ARROW_RIGHT`, `PENTAGON`, `HEXAGON`

### Extract Text from Presentation

```python
from pptx import Presentation

prs = Presentation("input.pptx")
text_content = []
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                text_content.append(para.text)
print("\n".join(text_content))
```

## Text Formatting

```python
from pptx.dml.color import RgbColor
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN

# Font properties
para = tf.paragraphs[0]
para.font.name = "Arial"
para.font.size = Pt(18)
para.font.bold = True
para.font.italic = True
para.font.color.rgb = RgbColor(0x00, 0x00, 0xFF)  # Blue

# Paragraph alignment
para.alignment = PP_ALIGN.CENTER  # LEFT, CENTER, RIGHT, JUSTIFY
```

## Working with Existing Files

```python
# Open existing presentation
prs = Presentation("existing.pptx")

# Modify slides
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            # Modify text
            pass

# Save with new name
prs.save("modified.pptx")
```

## Charts

See [references/charts.md](references/charts.md) for chart creation (bar, line, pie charts).

## Key Classes Reference

| Class | Description |
|-------|-------------|
| `Presentation` | Top-level object, represents .pptx file |
| `Slide` | Individual slide |
| `Shape` | Any shape on a slide |
| `TextFrame` | Text container in a shape |
| `Paragraph` | Text paragraph |
| `Run` | Text run with consistent formatting |
| `Table` | Table shape |
| `Picture` | Image shape |

## Utility Classes

```python
from pptx.util import Inches, Pt, Cm, Emu

# Measurements
left = Inches(1)      # 1 inch
size = Pt(24)         # 24 points (font size)
width = Cm(5)         # 5 centimeters
height = Emu(914400)  # EMUs (English Metric Units)
```

## Script Reference

For common operations, use the bundled scripts:

- `scripts/create_presentation.py` - Create presentation from data
- `scripts/extract_text.py` - Extract all text from a presentation
- `scripts/add_slide.py` - Add a slide to existing presentation
