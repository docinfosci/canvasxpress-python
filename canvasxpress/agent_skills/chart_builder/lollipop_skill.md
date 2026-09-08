---
title: "Lollipop Chart Skill"
description: "Generate CanvasXpress lollipop charts using Bar chart type with standard lollipop style and lollipop bullet variants, size encoding, and data value display."
---

# Lollipop Chart Skill

## Overview
Lollipop charts are elegant alternatives to bar charts, showing data points connected to a baseline. CanvasXpress implements lollipops via Bar chart type with `barType: 'lollipop'` for standard lollipops and `barType: 'lollipopBullet'` for bullet-style with open endpoints. Features include size encoding, data value labels, range coloring, and margin customization.

## Data Formats

### Standard Lollipop
```python
data = {
  'y': {
    'data': [[10, 15, 20, 30, 40, 70, 80, 90]],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'],
    'vars': ['V1'],
  },
  'x': {
    'val': [3, 3, 3, 3, 5, 3, 3, 1],
  },
}
```

### Bullet Lollipop with Metadata
```python
data = {
  'x': {
    'Color': ['A', 'B', 'C', 'D', 'E', 'F'],
  },
  'y': {
    'data': [[-40, -85, -60, 50, 75, 100]],
    'smps': ['Engineering', 'Biology', 'Computer', 'Psycology', 'Education', 'Health'],
    'vars': ['Var1'],
  },
}
```

## Code Examples

### Example 1: Standard Lollipop
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[10, 15, 20, 30, 40, 70, 80, 90]],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'],
    'vars': ['V1'],
  },
  'x': {
    'val': [3, 3, 3, 3, 5, 3, 3, 1],
  },
}
config = {
  'graphType': 'Bar',
  'barType': 'lollipop',
  'colorScheme': 'CanvasXpress',
  'dataPointSizeScaleFactor': 6,
  'widthFactor': 0.2,
  'sizeBy': 'val',
  'xAxis': ['V1'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Lollipop Bullet
```python
config = {
  'graphType': 'Bar',
  'barType': 'lollipopBullet',
  'barLollipopOpen': True,
  'colorBy': 'Color',
  'colorScheme': 'GGPlot',
  'dataPointSizeScaleFactor': 7,
  'rangeColors': ['rgb(200,200,200)'],
  'showDataValues': True,
  'showLegend': False,
  'xAxis': ['Var1'],
  'title': 'Occupations',
  'marginBottom': 50,
  'marginLeft': 50,
  'marginRight': 50,
  'marginTop': 50,
  'maxTextSize': 80,
  'setMinX': -150,
  'setMaxX': 150,
  'xAxisShow': False,
  'xAxis2Show': False,
  'xAxisGridMajorShow': False,
  'xAxisGridMinorShow': False,
}
```

## Agent Prompts

- "Create a CanvasXpress lollipop chart showing V1 values across samples S1-S8 with CanvasXpress color scheme."
- "Generate a lollipop chart with data point size scale factor of 6 and width factor of 0.2."
- "Build a lollipop bullet chart with open endpoints and GGPlot color scheme."
- "Create a performance lollipop with categories A-F showing negative and positive values."
- "Generate a lollipop chart with size encoding by metadata column."
- "Build a lollipop bullet with gray range background and data value labels."
- "Create a lollipop chart with custom margins (50px all sides) and maximum text size 80."
- "Generate a lollipop chart with x-axis range from -150 to 150."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "lollipop chart" | `graphType: 'Bar'`, `barType: 'lollipop'` | Sets lollipop style |
| "lollipop bullet" | `barType: 'lollipopBullet'` | Sets bullet lollipop |
| "open endpoint" | `barLollipopOpen: True` | Opens bullet endpoints |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors bars by metadata |
| "color scheme" | `colorScheme: 'CanvasXpress'` or `'GGPlot'` | Sets color palette |
| "data point size" | `dataPointSizeScaleFactor: N` | Scales data points |
| "width factor" | `widthFactor: 0.2` | Sets bar/lollipop width |
| "size by [column]" | `sizeBy: 'ColumnName'` | Encodes size by metadata |
| "show data values" | `showDataValues: True` | Displays value labels |
| "range color" | `rangeColors: ['rgb(200,200,200)']` | Sets background range color |
| "margin" | `marginBottom/MarginLeft/MarginRight/MarginTop` | Sets chart margins |
| "max text size" | `maxTextSize: 80` | Sets maximum text size |
| "axis range" | `setMinX: -150`, `setMaxX: 150` | Sets x-axis limits |
| "hide axis" | `xAxisShow: False` | Hides x-axis |
| "hide legend" | `showLegend: False` | Hides legend |

## Key Configuration Parameters

- `graphType`: Always `'Bar'` for lollipop charts
- `barType`: `'lollipop'` for standard, `'lollipopBullet'` for bullet style
- `barLollipopOpen`: Boolean to open bullet endpoints
- `colorBy`: Metadata column for coloring bars
- `colorScheme`: `'CanvasXpress'`, `'GGPlot'`, or custom palette
- `dataPointSizeScaleFactor`: Float to scale data point size
- `widthFactor`: Float to control bar/lollipop width
- `sizeBy`: Column for size encoding
- `showDataValues`: Boolean to display value labels
- `showLegend`: Boolean to show/hide legend
- `rangeColors`: Array of colors for range/background
- `marginBottom/marginLeft/marginRight/marginTop`: Integers for chart margins
- `maxTextSize`: Integer for maximum text size
- `setMinX`: Float for minimum x-axis value
- `setMaxX`: Float for maximum x-axis value
- `xAxis`: Array of x-axis column names
- `xAxisShow`: Boolean to show/hide x-axis
- `xAxis2Show`: Boolean to show/hide secondary axis
- `xAxisGridMajorShow`: Boolean to show major grid lines
- `xAxisGridMinorShow`: Boolean to show minor grid lines
- `title`: Chart title
