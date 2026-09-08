---
title: "Waterfall Chart Skill"
description: "Generate CanvasXpress waterfall plots showing cumulative changes, tumor shrinkage, QoL score changes, and clinical trial data with traditional waterfall bar charts."
---

# Waterfall Chart Skill

## Overview
Waterfall charts visualize cumulative changes, clinical trial responses, and score variations. CanvasXpress supports both traditional waterfall (chart type `'Waterfall'`) for positive/negative cumulative values and bar-based waterfalls (chart type `'Bar'`) for tumor shrinkage and QoL score distributions, with metadata segregation, overlays, and NEJM color schemes.

## Data Formats

### Traditional Waterfall (Positive/Negative Values)
```python
data = {
  'y': {
    'data': [[83, -44, 55, -60, 40, 0]],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1'],
  },
}
```

### QoL Score Changes (Bar-based Waterfall)
```python
data = {
  'x': {
    'Treatment': ['Trt-1', 'Trt-2', ...],
  },
  'y': {
    'data': [[109.09, 89.65, 57.14, ..., -19.24, -29.89]],
    'smps': ['Sub-253', 'Sub-337', ...],
    'vars': ['QoL-Score'],
  },
}
```

### Tumor Shrinkage with Metadata
```python
data = {
  'x': {
    'Status': ['PD', 'SD', 'PR', ...],
    'Tissue': ['Pancreas', 'Colrectal', ...],
  },
  'y': {
    'data': [[115, 75, 39, -8, -11, -31]],
    'smps': ['1001', '1002', ...],
    'vars': ['Shrinkage'],
  },
}
```

## Code Examples

### Example 1: Traditional Waterfall
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[83, -44, 55, -60, 40, 0]],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1'],
  },
}
config = {
  'graphType': 'Waterfall',
  'graphOrientation': 'vertical',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'Samples',
  'title': 'Traditional Waterfall',
  'xAxis': ['V1'],
  'xAxisTitle': 'Value',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Multi-variable Waterfall
```python
config = {
  'graphType': 'Waterfall',
  'graphOrientation': 'vertical',
  'smpTextRotate': 90,
  'smpTitle': 'Samples',
  'xAxis': ['V1', 'V2'],
  'xAxisTitle': 'Value',
}
```

### Example 3: QoL Score Waterfall (Bar)
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'showLegend': False,
  'showSampleNames': False,
  'xAxis': ['QoL-Score'],
  'xAxisTitle': 'Change from baseline (%) in QoL score',
  'title': 'Waterfall plot changes in QoL scores',
}
```

### Example 4: Segregated QoL Waterfall
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'segregateSamplesBy': ['Treatment'],
  'showLegend': False,
  'showSampleNames': False,
  'stripBackgroundBorderColor': 'rgb(0,0,0)',
  'stripTextColor': 'rgb(0,0,0)',
  'xAxis': ['QoL-Score'],
  'xAxisTitle': 'Change from baseline (%) in QoL score',
  'title': 'Waterfall plot changes in QoL scores',
}
```

### Example 5: Tumor Shrinkage with Metadata
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'colorBy': 'Tissue',
  'colorScheme': 'NEJM',
  'legendInside': True,
  'legendPosition': 'topRight',
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'showSampleNames': False,
  'smpOverlays': ['Status'],
  'smpOverlayProperties': {
    'Status': {
      'position': 'bottom',
      'scheme': 'White',
    },
  },
  'xAxis': ['Shrinkage'],
  'xAxisTitle': 'Best tumor shrinkage (%)',
  'xAxis2Show': False,
  'title': 'Clinical Trial',
}
```

## Agent Prompts

- "Create a CanvasXpress traditional waterfall chart showing positive and negative cumulative values for samples S1-S6."
- "Generate a vertical waterfall chart with two variables (V1 and V2) across six samples."
- "Build a QoL score waterfall using a bar chart with negative and positive percentage changes."
- "Create a tumor shrinkage waterfall with NEJM color scheme, tissue coloring, and status overlays."
- "Generate a segregated waterfall by treatment group with black borders."
- "Build a waterfall chart with sample names rotated 90 degrees."
- "Create a clinical trial waterfall with legend inside and status overlays at the bottom."
- "Generate a bar-based waterfall showing change from baseline percentages."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "waterfall chart" | `graphType: 'Waterfall'` | Sets waterfall chart type |
| "bar waterfall" | `graphType: 'Bar'` | Uses bar for waterfall |
| "positive/negative" | Data with +/− values | Data values drive color |
| "cumulative changes" | `graphType: 'Waterfall'` | Traditional waterfall |
| "tumor shrinkage" | `graphType: 'Bar'`, `colorScheme: 'NEJM'` | Clinical trial style |
| "sample names rotate" | `smpTextRotate: 90` | Rotates sample labels |
| "segregated by [column]" | `segregateSamplesBy: ['ColumnName']` | Segregates bars by metadata |
| "status overlay" | `smpOverlays: ['Status']` | Adds bottom overlay |
| "legend inside" | `legendInside: True` | Places legend in chart |
| "legend position" | `legendPosition: 'topRight'` | Sets legend location |
| "NEJM color scheme" | `colorScheme: 'NEJM'` | Clinical trial colors |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors bars by metadata |
| "change from baseline" | `xAxisTitle: 'Change from baseline (%)'` | X-axis label |
| "show sample names" | `showSampleNames: True` | Displays sample labels |

## Key Configuration Parameters

- `graphType`: `'Waterfall'` for traditional, `'Bar'` for clinical bar waterfalls
- `graphOrientation`: `'vertical'` for vertical bars
- `colorBy`: Metadata column for coloring bars
- `colorScheme`: `'NEJM'` for clinical trial colors
- `segregateSamplesBy`: Array of metadata columns to segregate bars
- `smpOverlays`: Array of metadata columns for bottom overlays
- `smpOverlayProperties`: Object with overlay styling (e.g., `{'Status': {'position': 'bottom', 'scheme': 'White'}}`)
- `smpTextRotate`: Rotation angle for sample names (e.g., `90`)
- `smpTitle`: Title for sample axis
- `legendInside`: Boolean to place legend inside chart
- `legendPosition`: `'topRight'`, `'bottom'`, etc.
- `legendKeyBackgroundBorderColor`: `'rgba(255,255,255,0)'` for invisible borders
- `legendKeyBackgroundColor`: `'rgba(255,255,255,0)'` for transparent background
- `showLegend`: Boolean to show/hide legend
- `showSampleNames`: Boolean to display sample names
- `stripBackgroundBorderColor`: `'rgb(0,0,0)'` for black borders
- `stripTextColor`: `'rgb(0,0,0)'` for black text
- `xAxis`: Array of x-axis column names
- `xAxisTitle`: X-axis label
- `xAxis2Show`: Boolean to show/hide secondary axis
- `title`: Chart title
