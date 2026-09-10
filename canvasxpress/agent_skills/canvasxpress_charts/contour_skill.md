---
title: "Contour Chart Skill"
description: "Generate CanvasXpress contour plots using Heatmap or ScatterBubble2D chart types with contour levels, filled contours, and normal/advanced rendering modes."
---

# Contour Chart Skill

## Overview
Contour plots visualize 3D data surfaces as 2D plots with contour lines or filled regions. CanvasXpress supports contour on Heatmap (matrix data) and ScatterBubble2D (scattered data), with contour levels, filled regions, and normal/advanced types for density visualization.

## Data Formats

### Matrix Data for Heatmap Contours
```python
data = {
  'y': {
    'data': [
      [100, 101, 102, 103, ...],  # V1-V50
      [100, 101, 102, 103, ...],
      ...
    ],
    'smps': ['Smp1', 'Smp2', ...],
    'vars': ['V1', 'V2', ...],
  },
}
```

### Scattered Data for ScatterBubble2D
```python
data = {
  'y': {
    'data': [
      [0, 0, 10], [1, 0, 5.625], [2, 0, 2.5], ...
    ],
    'smps': ['s1', 's2', 's3'],
    'vars': ['v1', 'v2', 'v3', ...],
  },
}
```

## Code Examples

### Example 1: Heatmap with Contour Levels (Volcano Topography)
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [100, 101, 102, 103, 104, 105, 105, 106, 107, 108, ...],
      [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, ...],
      [101, 102, 103, 104, 105, 105, 106, 107, 108, 109, ...],
      ...
    ],
    'smps': ['Smp1', 'Smp2', ...],
    'vars': ['V1', 'V2', ...],
  },
}
config = {
  'graphType': 'Heatmap',
  'heatmapCellBox': False,
  'showContourLevel': True,
  'showSampleNames': False,
  'showVariableNames': False,
  'subtitle': 'datasets - volcano',
  'title': "Topographic Information on Auckland's Maunga Whau Volcano",
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Heatmap with Normal Contour Type
```python
config = {
  'graphType': 'Heatmap',
  'contourType': 'normal',
  'heatmapCellBox': False,
  'showSampleNames': False,
  'showVariableNames': False,
  'title': 'Basic Contour Plot',
  'xAxis': ['v1', 'v2', 'v3', 'v4', 'v5'],
}
```

### Example 3: ScatterBubble2D with Filled Contours
```python
config = {
  'graphType': 'ScatterBubble2D',
  'contourFilled': True,
  'showContourLevel': True,
  'title': 'Basic Contour Plot',
  'xAxis': ['s1'],
  'yAxis': ['s2'],
  'zAxis': ['s3'],
}
```

### Example 4: ScatterBubble2D with Normal Contour
```python
config = {
  'graphType': 'ScatterBubble2D',
  'contourFilled': True,
  'contourType': 'normal',
  'title': 'Custom Contour Plot',
  'xAxis': ['s1'],
  'yAxis': ['s2'],
  'zAxis': ['s3'],
}
```

### Example 5: Heatmap with Spline Lines (No Contour)
```python
config = {
  'graphType': 'Heatmap',
  'contourType': 'normal',
  'heatmapCellBox': False,
  'lineType': 'spline',
  'showContourLevel': False,
  'showSampleNames': False,
  'showVariableNames': False,
  'xAxis': ['v1', 'v2', 'v3', 'v4', 'v5'],
}
```

## Agent Prompts

- "Create a CanvasXpress heatmap contour plot showing volcano topography with contour levels enabled."
- "Generate a basic contour plot using Heatmap with normal contour type and no cell borders."
- "Build a ScatterBubble2D with filled contours and contour level labels for scattered 3D data."
- "Create a custom contour plot with ScatterBubble2D showing s1, s2, s3 relationships."
- "Generate a heatmap with spline lines connecting data points without contour levels."
- "Build a contour plot with no sample or variable names shown for clean visualization."
- "Create a heatmap contour with false cell box for seamless color transitions."
- "Generate a filled contour plot with normal contour type on scattered bubble data."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "contour plot" (heatmap) | `graphType: 'Heatmap'` + `showContourLevel: True` | Shows contours on matrix |
| "contour plot" (scatter) | `graphType: 'ScatterBubble2D'` + `contourFilled: True` | Shows contours on scatter |
| "filled contour" | `contourFilled: True` | Fills contour regions |
| "normal contour" | `contourType: 'normal'` | Uses normal rendering mode |
| "show contour level" | `showContourLevel: True` | Displays contour level labels |
| "no cell box" | `heatmapCellBox: False` | Removes cell borders |
| "no sample names" | `showSampleNames: False` | Hides sample labels |
| "no variable names" | `showVariableNames: False` | Hides variable labels |
| "spline lines" | `lineType: 'spline'` | Uses spline connections |
| "x-axis" | `xAxis: ['ColumnName']` | Sets x-axis column |
| "y-axis" | `yAxis: ['ColumnName']` | Sets y-axis column |
| "z-axis" | `zAxis: ['ColumnName']` | Sets z-axis column (scatter only) |

## Key Configuration Parameters

- `graphType`: `'Heatmap'` for matrix contours, `'ScatterBubble2D'` for scattered contours
- `contourType`: `'normal'` for contour rendering mode
- `contourFilled`: Boolean to fill contour regions
- `showContourLevel`: Boolean to show contour level labels
- `heatmapCellBox`: Boolean to show/hide cell borders (heatmap only)
- `showSampleNames`: Boolean to show/hide sample labels
- `showVariableNames`: Boolean to show/hide variable labels
- `lineType`: `'spline'` for spline connections (heatmap only)
- `xAxis`: Array of x-axis column names
- `yAxis`: Array of y-axis column names
- `zAxis`: Array of z-axis column names (scatter only)
- `title`: Chart title
- `subtitle`: Chart subtitle
