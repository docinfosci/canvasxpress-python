---
title: "Pie Chart Skill"
description: "Generate CanvasXpress pie charts with multiple layouts, segment labels, separation, precision control, solid/3D types, and grid overlays."
---

# Pie Chart Skill

## Overview
Pie charts display proportional data as circular segments. CanvasXpress supports multi-chart layouts, inside/outside labels, segment separation (exploded slices), precision control, solid styles, and grid overlays for clean multi-sample comparisons.

## Data Formats

### Wide Format with Metadata Factors
```python
data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', ...],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', ...],
  },
  'y': {
    'data': [
      [5, 10, 25, 40, 45, 50],
      [95, 80, 75, 70, 55, 40],
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
}
```

## Code Examples

### Example 1: 2x3 Grid of Pie Charts with Inside Labels
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', 'Lev : 1', 'Lev : 2', 'Lev : 3'],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', 'Lev : B', 'Lev : A', 'Lev : B'],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', 'Lev : Y', 'Lev : Z', 'Lev : Z'],
    'Factor4': [5, 10, 15, 20, 25, 30],
    'Factor5': [8, 16, 24, 32, 40, 48],
    'Factor6': [10, 20, 30, 40, 50, 60],
  },
  'y': {
    'data': [
      [5, 10, 25, 40, 45, 50],
      [95, 80, 75, 70, 55, 40],
      [25, 30, 45, 60, 65, 70],
      [55, 40, 35, 30, 15, 1],
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
}
config = {
  'graphType': 'Pie',
  'layout': '2X3',
  'pieSegmentLabels': 'inside',
  'pieSegmentPrecision': 0,
  'pieSegmentSeparation': 1,
  'showPieGrid': True,
  'showPieSampleLabel': True,
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'xAxis': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Single Pie Chart with Outside Labels and Exploded Slices
```python
config = {
  'graphType': 'Pie',
  'pieSegmentLabels': 'outside',
  'pieSegmentPrecision': 1,
  'pieSegmentSeparation': 2,
  'pieType': 'solid',
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'xAxis': ['S1'],
}
```

### Example 3: Pie Chart Grouped by Metadata Factor
```python
config = {
  'graphType': 'Pie',
  'pieBy': 'Factor1',
  'pieSegmentLabels': 'inside',
  'pieSegmentPrecision': 0,
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
}
```

### Example 4: Single Pie Chart with Default Settings
```python
config = {
  'graphType': 'Pie',
  'pieSegmentLabels': 'inside',
  'pieSegmentPrecision': 2,
  'showPieGrid': True,
  'showPieSampleLabel': True,
  'xAxis': ['Sample1'],
}
```

### Example 5: 1x2 Grid Layout
```python
config = {
  'graphType': 'Pie',
  'layout': '1X2',
  'pieSegmentLabels': 'outside',
  'pieSegmentPrecision': 0,
  'pieSegmentSeparation': 0,
  'showPieGrid': False,
  'showPieSampleLabel': True,
  'xAxis': ['S1', 'S2'],
}
```

### Example 6: 3x3 Grid Layout
```python
config = {
  'graphType': 'Pie',
  'layout': '3X3',
  'pieSegmentLabels': 'inside',
  'pieSegmentPrecision': 1,
  'pieSegmentSeparation': 3,
  'showPieGrid': True,
  'showPieSampleLabel': True,
  'xAxis': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9'],
}
```

### Example 7: Solid Pie Chart with Segments by Column
```python
config = {
  'graphType': 'Pie',
  'pieType': 'solid',
  'pieSegmentLabels': 'inside',
  'pieSegmentPrecision': 0,
  'pieBy': 'Category',
  'showTransition': False,
  'showPieGrid': True,
}
```

## Agent Prompts

- "Create a CanvasXpress 2x3 grid of pie charts showing six samples with inside labels and segment separation."
- "Generate a single pie chart with outside labels and exploded slices (separation of 2)."
- "Build a pie chart grouped by Factor1 with inside labels and zero precision."
- "Create a pie chart with solid style, outside labels, and one decimal precision."
- "Generate a 1x2 grid of pie charts with no segment separation and sample labels."
- "Build a 3x3 grid of pie charts with 3-unit separation and grid overlay."
- "Create a pie chart with transparent legend background and inside labels."
- "Generate a pie chart with no transitions for a static appearance."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "pie chart" | `graphType: 'Pie'` | Sets the chart type to pie |
| "grid layout" | `layout: '2X3'` | Sets multi-chart layout (e.g., `'1X2'`, `'2X3'`, `'3X3'`) |
| "inside labels" | `pieSegmentLabels: 'inside'` | Places percentage labels inside segments |
| "outside labels" | `pieSegmentLabels: 'outside'` | Places percentage labels outside segments |
| "segment separation" | `pieSegmentSeparation: N` | Explodes segments by N units (0 = none) |
| "precision" | `pieSegmentPrecision: N` | Sets decimal places (0, 1, 2) |
| "pie type" | `pieType: 'solid'` | Uses solid fill (default is open) |
| "pie by [column]" | `pieBy: 'ColumnName'` | Groups segments by metadata column |
| "show grid" | `showPieGrid: True` | Adds grid overlay to pies |
| "show sample label" | `showPieSampleLabel: True` | Displays sample names |
| "no transition" | `showTransition: False` | Disables animation |
| "transparent legend" | `legendKeyBackgroundColor: 'rgba(255,255,255,0)'` + `legendKeyBackgroundBorderColor: 'rgba(255,255,255,0)'` | Removes legend background |

## Key Configuration Parameters

- `graphType`: Always `'Pie'` for pie charts
- `layout`: Multi-chart layout (e.g., `'1X2'`, `'2X3'`, `'3X3'`, `'3X1'`)
- `pieSegmentLabels`: `'inside'` or `'outside'` for label placement
- `pieSegmentPrecision`: Integer for decimal places (0, 1, 2)
- `pieSegmentSeparation`: Integer for slice explosion (0 = no separation)
- `pieType`: `'solid'` for filled pies, omitted for default style
- `pieBy`: Metadata column to group pie segments by
- `showPieGrid`: Boolean to show/hide pie grid overlay
- `showPieSampleLabel`: Boolean to show/hide sample names on pies
- `showTransition`: Boolean to enable/disable animation (default `True`)
- `legendKeyBackgroundColor`: Background color for legend keys (use `'rgba(255,255,255,0)'` for transparent)
- `legendKeyBackgroundBorderColor`: Border color for legend keys (use `'rgba(255,255,255,0)'` for transparent)
