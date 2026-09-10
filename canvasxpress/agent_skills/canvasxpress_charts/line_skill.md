---
title: "Line Chart Skill"
description: "Generate CanvasXpress line charts with vertical/horizontal orientation, spline lines, error areas, pattern decorations, and segregated panels."
---

# Line Chart Skill

## Overview
Line charts display quantitative values across continuous intervals or time periods. CanvasXpress supports single/multiple series, spline smoothing, error areas, line patterns, data segregation by factors, and custom themes for trend visualization.

## Data Formats

### Wide Format (Series as Variables)
```python
data = {
  'y': {
    'data': [
      [30, 58, 87, 115, 120, 142, 145],
      [33, 69, 111, 156, 172, 203, 203],
      [30, 51, 75, 108, 115, 139, 140],
    ],
    'smps': [118, 484, 664, 1004, 1231, 1372, 1582],
    'vars': [1, 2, 3],
  },
}
```

### Long Format with Metadata
```python
data = {
  'y': {
    'data': [
      [118, 30], [484, 58], [664, 87], ...
    ],
    'smps': ['Days Old', 'Circumference (mm)'],
    'vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...],
  },
  'z': {
    'Tree': ['Tree-1']*7 + ['Tree-2']*7 + ...
  },
}
```

## Code Examples

### Example 1: Vertical Line Chart with GGPlot Theme
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [30, 58, 87, 115, 120, 142, 145],
      [33, 69, 111, 156, 172, 203, 203],
      [30, 51, 75, 108, 115, 139, 140],
      [32, 62, 112, 167, 179, 209, 214],
      [30, 49, 81, 125, 142, 174, 177],
    ],
    'smps': [118, 484, 664, 1004, 1231, 1372, 1582],
    'vars': [1, 2, 3, 4, 5],
  },
}
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'theme': 'GGPlot',
  'backgroundType': 'panel',
  'blockContrast': True,
  'evenColor': 'rgb(226,236,248)',
  'panelBackgroundColor': 'rgb(226,236,248)',
  'legendInside': True,
  'legendPosition': 'topLeft',
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'smpTextRotate': 90,
  'smpTitle': 'Days Old',
  'title': 'Growth of Orange Trees',
  'xAxis': [1, 2, 3, 4, 5],
  'xAxisTitle': 'Circumference (mm)',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Long Format with Line By Metadata
```python
config = {
  'graphType': 'Scatter2D',
  'graphOrientation': 'horizontal',
  'colorBy': 'Tree',
  'lineBy': 'Tree',
  'showLegend': False,
  'title': 'Growth of Orange Trees',
  'xAxis': ['Days Old'],
  'yAxis': ['Circumference (mm)'],
}
```

### Example 3: Segregated Line Chart with Pattern Decoration
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'segregateSamplesBy': ['Factor3'],
  'layoutTopology': '1X3',
  'lineDecoration': 'pattern',
  'legendPosition': 'right',
  'smpTextRotate': 90,
  'smpTitle': 'Collection of Samples',
  'smpTitleFontStyle': 'italic',
  'theme': 'blackAndWhite',
  'title': 'Random Data',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 4: Time Series with Area Error Type
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'lineErrorType': 'area',
  'lineType': 'spline',
  'xAxis': ['Var1', 'Var2'],
}
```

### Example 5: Line Chart with Confidence Intervals
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'lineErrorType': 'area',
  'lineType': 'spline',
  'colorBy': 'Condition',
  'showLegend': True,
  'title': 'Spatiotemporal Control of RhoGTPase Activation',
  'xAxis': ['Time'],
  'yAxis': ['YFP/CFP Ratio'],
}
```

### Example 6: Horizontal Line Chart
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'horizontal',
  'theme': 'CanvasXpress',
  'showLegend': True,
  'lineType': 'step',
  'title': 'Horizontal Line Chart',
  'xAxis': ['Var1', 'Var2'],
  'yAxis': ['Sample'],
}
```

### Example 7: Multi-Series Line Chart with Custom Colors
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'colorScheme': 'Prism',
  'lineType': 'spline',
  'showLegend': True,
  'legendPosition': 'bottom',
  'legendColumns': 3,
  'title': 'Multi-Series Line Chart',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'xAxisTitle': 'Variables',
  'yAxisTitle': 'Magnitude',
}
```

### Example 8: Line Chart with Block Contrast and Alternating Colors
```python
config = {
  'graphType': 'Line',
  'graphOrientation': 'vertical',
  'blockContrast': True,
  'evenColor': 'rgb(226,236,248)',
  'backgroundType': 'panel',
  'panelBackgroundColor': 'rgb(226,236,248)',
  'theme': 'GGPlot',
  'legendInside': True,
  'legendPosition': 'topLeft',
  'smpTextRotate': 90,
  'title': 'Growth Pattern with Block Contrast',
  'xAxis': [1, 2, 3, 4, 5],
}
```

## Agent Prompts

- "Create a CanvasXpress vertical line chart showing growth data across five variables with GGPlot theme."
- "Generate a horizontal line chart using long-format data with lines grouped by tree metadata."
- "Build segregated line charts split by Factor3 with pattern decorations and italic sample titles."
- "Create a time series line chart with spline smoothing and area-based error intervals."
- "Generate a line chart with confidence intervals showing YFP/CFP ratio over time across conditions."
- "Build a horizontal line chart with step lines for categorical data visualization."
- "Create a multi-series line chart with Prism color scheme and legend in 3 columns at bottom."
- "Generate a line chart with block contrast showing alternating background colors."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "line chart" | `graphType: 'Line'` | Sets the chart type to line |
| "vertical" | `graphOrientation: 'vertical'` | Default, lines go up |
| "horizontal" | `graphOrientation: 'horizontal'` | Lines go left-to-right |
| "spline" / "smooth" | `lineType: 'spline'` | Uses quadratic bezier curves |
| "step" / "steps" | `lineType: 'step'` | Uses step-line visualization |
| "error area" | `lineErrorType: 'area'` | Adds shaded error region |
| "pattern decoration" | `lineDecoration: 'pattern'` | Applies line patterns (dashed, dotted) |
| "legend inside" | `legendInside: True` | Places legend inside chart area |
| "legend position" | `legendPosition: 'topLeft'` | Sets legend location |
| "legend columns" | `legendColumns: N` | Sets number of legend columns |
| "separate by [column]" | `segregateSamplesBy: ['ColumnName']` + `layoutTopology: '1X3'` | Splits into panels |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors lines by metadata |
| "line by [column]" | `lineBy: 'ColumnName'` | Groups points into lines by metadata |
| "block contrast" | `blockContrast: True` | Alternates background colors |
| "even color" | `evenColor: 'rgb(226,236,248)'` | Sets alternating background color |
| "theme" | `theme: 'GGPlot'` | Applies theme (GGPlot, CanvasXpress, blackAndWhite) |
| "rotate labels" | `smpTextRotate: 90` | Rotates sample/axis labels |
| "italic title" | `smpTitleFontStyle: 'italic'` | Makes sample title italic |

## Key Configuration Parameters

- `graphType`: `'Line'` for line charts, `'Scatter2D'` with `lineBy` for long-format lines
- `graphOrientation`: `'vertical'` (default) or `'horizontal'`
- `lineType`: `'spline'` for smooth curves, `'step'` for step lines, or omitted for straight lines
- `lineErrorType`: `'area'` for shaded error/confidence regions
- `lineDecoration`: `'pattern'` for dashed/dotted line patterns
- `colorBy`: Metadata column for coloring lines
- `lineBy`: Metadata column for grouping points into lines (long format)
- `segregateSamplesBy`: Array to split chart into separate panels
- `layoutTopology`: Panel layout (e.g., `'1X3'` for 1 row, 3 columns)
- `legendInside`: Boolean to place legend inside chart area
- `legendPosition`: `'topLeft'`, `'topRight'`, `'bottomLeft'`, `'bottomRight'`, `'right'`
- `legendColumns`: Number of columns in legend
- `blockContrast`: Boolean to enable alternating background
- `evenColor`: Color for alternating background bands
- `backgroundType`: `'panel'` for panel background styling
- `panelBackgroundColor`: Background color for chart panel
- `theme`: `'GGPlot'`, `'CanvasXpress'`, `'blackAndWhite'`
- `smpTextRotate`: Angle in degrees for sample label rotation
- `smpTitleFontStyle`: `'italic'`, `'bold'`, or `'normal'`
- `colorScheme`: Color palette (e.g., `'Prism'`, `'Behance'`)
