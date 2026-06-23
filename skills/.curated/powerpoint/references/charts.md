# Charts in PowerPoint

Create charts programmatically using python-pptx.

## Basic Chart Creation

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Chart Example"

# Define chart data
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Series 1', (19.2, 21.4, 16.7, 28.3))
chart_data.add_series('Series 2', (22.5, 28.1, 25.9, 31.2))

# Add chart to slide
x, y, cx, cy = Inches(1), Inches(2), Inches(8), Inches(4.5)
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
).chart

prs.save('chart.pptx')
```

## Chart Types

| Type | Constant |
|------|----------|
| Clustered Column | `XL_CHART_TYPE.COLUMN_CLUSTERED` |
| Stacked Column | `XL_CHART_TYPE.COLUMN_STACKED` |
| Clustered Bar | `XL_CHART_TYPE.BAR_CLUSTERED` |
| Line | `XL_CHART_TYPE.LINE` |
| Line with Markers | `XL_CHART_TYPE.LINE_MARKERS` |
| Pie | `XL_CHART_TYPE.PIE` |
| Area | `XL_CHART_TYPE.AREA` |

## Pie Chart

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = CategoryChartData()
chart_data.categories = ['Apple', 'Banana', 'Cherry', 'Date']
chart_data.add_series('Market Share', (0.35, 0.25, 0.22, 0.18))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data
).chart
```

## Line Chart

```python
chart_data = CategoryChartData()
chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
chart_data.add_series('Revenue', (4.5, 5.2, 4.8, 6.1, 7.3))
chart_data.add_series('Expenses', (3.2, 3.5, 3.8, 4.1, 4.0))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.LINE_MARKERS, x, y, cx, cy, chart_data
).chart
```

## Chart Customization

```python
# Access chart after creation
chart = slide.shapes.add_chart(...).chart

# Chart title
chart.has_title = True
chart.chart_title.text_frame.text = "Sales Report"

# Legend
chart.has_legend = True
from pptx.enum.chart import XL_LEGEND_POSITION
chart.legend.position = XL_LEGEND_POSITION.BOTTOM

# Access series for formatting
series = chart.series[0]
series.smooth = True  # For line charts
```

## XY Scatter Chart

```python
from pptx.chart.data import XyChartData

chart_data = XyChartData()
series = chart_data.add_series('Data Points')
series.add_data_point(1.2, 2.5)
series.add_data_point(2.3, 4.1)
series.add_data_point(3.5, 3.8)

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.XY_SCATTER, x, y, cx, cy, chart_data
).chart
```
