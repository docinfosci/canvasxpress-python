---
title: "Density Chart Skill"
description: "Generate CanvasXpress density plots using Scatter2D chart type with histograms, density overlays, and statistical aggregations."
---

# Density Chart Skill

## Overview
Density plots visualize data distribution with scatter points and histogram/density overlays. CanvasXpress implements density via Scatter2D with histogram support, showing count-based or statistical aggregations, density curves, and customizable axes for distribution analysis.

## Data Formats

### Single Variable with Metadata
```python
data = {
  'y': {
    'data': [[49], [56], [60], [43], [57], ...],
    'smps': ['weight'],
  },
  'z': {
    'sex': ['F', 'F', 'F', 'F', ...],
  },
}
```

## Code Examples

### Example 1: Scatter with Histogram and Density
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[49], [56], [60], [43], [57], [58], [52], [52], [52], [51], ...],
    'smps': ['weight'],
  },
  'z': {
    'sex': ['F']*100 + ['M']*100,
  },
}
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'hideHistogram': True,
  'histogramStat': 'count',
  'showHistogramDensity': True,
  'xAxis': ['weight'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Scatter with Density Overlay
```python
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'showHistogramDensity': True,
  'histogramStat': 'count',
  'xAxis': ['weight'],
}
```

## Agent Prompts

- "Create a CanvasXpress scatter plot with histogram showing weight distribution using count statistics."
- "Generate a density plot with histogram and density overlay on x-axis."
- "Build a scatter plot with count-based histogram showing data distribution."
- "Create a scatter plot with histogram density enabled for distribution visualization."
- "Generate a scatter plot with histogram statistics set to count."
- "Build a density plot with x-axis showing weight variable."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "density plot" | `graphType: 'Scatter2D'` | Sets scatter-based density |
| "histogram" | `showHistogram: True` | Shows histogram overlay |
| "hide histogram" | `hideHistogram: True` | Hides histogram (overlaps) |
| "histogram stat" | `histogramStat: 'count'` | Sets histogram statistics |
| "histogram density" | `showHistogramDensity: True` | Shows density curve |
| "x-axis column" | `xAxis: ['ColumnName']` | Sets x-axis column |

## Key Configuration Parameters

- `graphType`: Always `'Scatter2D'` for density plots
- `showHistogram`: Boolean to show histogram overlay
- `hideHistogram`: Boolean to hide histogram (overlaps scatter)
- `histogramStat`: `'count'` for count-based histogram
- `showHistogramDensity`: Boolean to show density curve
- `xAxis`: Array of x-axis column names
