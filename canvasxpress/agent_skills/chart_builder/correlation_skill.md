---
title: "Correlation Chart Skill"
description: "Generate CanvasXpress correlation plots and correlation heatmaps with circle correlation, sample/variable axes, anchor legends, and matrix visualization."
---

# Correlation Chart Skill

## Overview
Correlation charts visualize relationships between variables or samples using scatter-based correlation plots or correlation matrices. CanvasXpress supports sample/variable axes, circle correlation type, anchor legends, and can display correlation data as heatmaps for matrix visualization.

## Data Formats

### Wide Format with Metadata
```python
data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', ...],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', ...],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', ...],
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
```

## Code Examples

### Example 1: Correlation Plot with Samples on Axis
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
  'graphType': 'Correlation',
  'correlationAxis': 'samples',
  'title': 'Correlation Plot',
  'yAxisTitle': 'Correlation Title',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Circle Correlation Method
```python
config = {
  'graphType': 'Correlation',
  'correlationAxis': 'samples',
  'correlationType': 'circle',
  'title': 'Correlation Plot',
  'yAxisTitle': 'Correlation Title',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 3: Variables on Axis with Anchor Legend
```python
config = {
  'graphType': 'Correlation',
  'correlationAxis': 'variables',
  'correlationAnchorLegend': True,
  'correlationAnchorLegendAlignWidth': 20,
  'title': 'Correlation Plot',
  'yAxisTitle': 'Correlation Title',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 4: Correlation Heatmap (Car Attributes)
```python
config = {
  'graphType': 'Heatmap',
  'title': 'Heatmap - Correlation',
  'xAxis': ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'],
}
```

## Agent Prompts

- "Create a CanvasXpress correlation plot with samples on the correlation axis showing relationships between V1-V4."
- "Generate a correlation plot using circle correlation method with samples on the axis."
- "Build a correlation plot with variables on the axis and anchor legend with 20px alignment width."
- "Create a correlation heatmap showing relationships between car attributes (mpg, cyl, disp, hp, etc.)."
- "Generate a correlation plot with custom y-axis title and four variables."
- "Build a correlation visualization with anchor legend enabled and variable axis alignment."
- "Create a correlation heatmap with navy-white-firebrick color spectrum for correlation coefficients."
- "Generate a circle-type correlation plot with labeled axes."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "correlation plot" | `graphType: 'Correlation'` | Sets the chart type to correlation |
| "correlation heatmap" | `graphType: 'Heatmap'` | Displays correlation as heatmap |
| "samples on axis" | `correlationAxis: 'samples'` | Uses samples for correlation |
| "variables on axis" | `correlationAxis: 'variables'` | Uses variables for correlation |
| "circle correlation" | `correlationType: 'circle'` | Uses circle visualization method |
| "anchor legend" | `correlationAnchorLegend: True` | Shows anchor legend |
| "anchor width" | `correlationAnchorLegendAlignWidth: 20` | Sets anchor legend width in px |
| "y-axis title" | `yAxisTitle: 'Text'` | Sets y-axis label |

## Key Configuration Parameters

- `graphType`: `'Correlation'` for correlation plots, `'Heatmap'` for correlation matrices
- `correlationAxis`: `'samples'` or `'variables'` for correlation axis
- `correlationType`: `'circle'` for circle-based correlation visualization
- `correlationAnchorLegend`: Boolean to show/hide anchor legend
- `correlationAnchorLegendAlignWidth`: Integer for anchor legend alignment width in pixels
- `yAxisTitle`: Label for y-axis
- `title`: Chart title
- `xAxis`: Array of variable names for x-axis labels
