---
title: "Sunburst Chart Skill"
description: "Generate CanvasXpress sunburst charts using Circular chart type with hierarchical data, rotation control, metadata coloring, and multi-level breakdowns."
---

# Sunburst Chart Skill

## Overview
Sunburst charts display hierarchical data as concentric rings with segments sized by value. CanvasXpress implements sunbursts via Circular with `circularType: 'sunburst'`, supporting metadata-based coloring, rotation control, arc configuration, hierarchy levels, and custom color schemes for multi-level breakdowns.

## Data Formats

### Hierarchy with Metadata
```python
data = {
  'x': {
    'Quarter': ['1st', '1st', '1st', '1st', '1st', '1st', '2nd', '2nd', '2nd', ...],
    'Month': ['Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Mar', 'Apr', 'May', 'Jun', ...],
    'Week': [None, 'Week 1', 'Week 2', 'Week 3', 'Week 4', None, None, None, None, ...],
    'Color': ['red', 'blue', 'green', 'grey', 'red', 'blue', 'green', 'grey', ...],
  },
  'y': {
    'data': [[3.5, 1.2, 0.8, 0.6, 0.5, 1.7, 1.1, 0.8, 0.3, ...]],
    'smps': ['Sales1', 'Sales2', ...],
    'vars': ['Sales'],
  },
}
```

## Code Examples

### Example 1: Full Sunburst Colored by Quarter
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Quarter': ['1st', '1st', '1st', '1st', '1st', '1st', '2nd', '2nd', '2nd', '3rd', '3rd', '3rd', '4th', '4th', '4th'],
    'Month': ['Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Week': [None, 'Week 1', 'Week 2', 'Week 3', 'Week 4', None, None, None, None, None, None, None, None, None, None],
    'Color': ['red', 'blue', 'green', 'grey', 'red', 'blue', 'green', 'grey', 'red', 'blue', 'green', 'grey', 'red', 'blue', 'green'],
  },
  'y': {
    'data': [[3.5, 1.2, 0.8, 0.6, 0.5, 1.7, 1.1, 0.8, 0.3, 0.7, 0.6, 0.1, 0.5, 0.4, 0.3]],
    'smps': ['Sales1', 'Sales2', 'Sales3', 'Sales4', 'Sales5', 'Sales6', 'Sales7', 'Sales8', 'Sales9', 'Sales10', 'Sales11', 'Sales12', 'Sales13', 'Sales14', 'Sales15'],
    'vars': ['Sales'],
  },
}
config = {
  'graphType': 'Circular',
  'circularType': 'sunburst',
  'circularArc': 360,
  'circularRotate': 0,
  'colorBy': 'Quarter',
  'colorScheme': 'Bootstrap',
  'hierarchy': ['Quarter', 'Month', 'Week'],
  'objectBorderColor': 'rgb(0,0,0)',
  'showTransition': False,
  'title': 'Simple Sunburst',
  'xAxis': ['Sales'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Sunburst Colored by Month
```python
config = {
  'graphType': 'Circular',
  'circularType': 'sunburst',
  'circularArc': 360,
  'circularRotate': 0,
  'colorBy': 'Month',
  'colorScheme': 'RdYlBu',
  'hierarchy': ['Quarter', 'Month', 'Week'],
  'objectBorderColor': 'rgb(0,0,0)',
  'showTransition': False,
  'title': 'Simple Sunburst Colored by Category',
  'xAxis': ['Sales'],
}
```

### Example 3: Rotated Sunburst (-90 degrees)
```python
config = {
  'graphType': 'Circular',
  'circularType': 'sunburst',
  'circularArc': 360,
  'circularRotate': -90,
  'colorScheme': 'Bootstrap',
  'hierarchy': ['Quarter', 'Month', 'Week'],
  'objectBorderColor': 'rgb(0,0,0)',
  'showTransition': False,
  'title': 'Rotated Sunburst',
  'xAxis': ['Sales'],
}
```

### Example 4: Half Sunburst (180 degrees)
```python
config = {
  'graphType': 'Circular',
  'circularType': 'sunburst',
  'circularArc': 180,
  'circularRotate': -90,
  'colorScheme': 'Bootstrap',
  'hierarchy': ['Quarter', 'Month', 'Week'],
  'objectBorderColor': 'rgb(0,0,0)',
  'showTransition': False,
  'title': 'Rotated Half Sunburst',
  'xAxis': ['Sales'],
}
```

## Agent Prompts

- "Create a CanvasXpress full 360-degree sunburst chart showing sales by quarter with Bootstrap colors."
- "Generate a sunburst colored by month using RdYlBu color scheme with quarter-month-week hierarchy."
- "Build a rotated sunburst (-90 degrees) with 360-degree arc and black borders."
- "Create a half-circle (180-degree) sunburst rotated to face upwards."
- "Generate a sunburst with hierarchy: Quarter > Month > Week showing sales values."
- "Build a sunburst chart with color by metadata column (Quarter or Month)."
- "Create a sunburst with no transitions and black object borders."
- "Generate a rotated half sunburst with Bootstrap color scheme and sales data."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "sunburst" | `graphType: 'Circular'` + `circularType: 'sunburst'` | Sets sunburst visualization |
| "full circle" | `circularArc: 360` | Full 360-degree arc |
| "half circle" | `circularArc: 180` | Half 180-degree arc |
| "rotate" | `circularRotate: N` | Rotates by N degrees (e.g., `-90`) |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors segments by metadata |
| "color scheme" | `colorScheme: 'Bootstrap'` or `'RdYlBu'` | Sets color palette |
| "hierarchy" | `hierarchy: ['Quarter', 'Month', 'Week']` | Defines hierarchy levels |
| "black border" | `objectBorderColor: 'rgb(0,0,0)'` | Sets black borders |
| "no transition" | `showTransition: False` | Disables animation |
| "x-axis column" | `xAxis: ['ColumnName']` | Sets axis column |

## Key Configuration Parameters

- `graphType`: Always `'Circular'` for sunburst charts
- `circularType`: `'sunburst'` for sunburst layout
- `circularArc`: Integer for arc degrees (180 = half, 360 = full)
- `circularRotate`: Integer for rotation angle in degrees
- `colorBy`: Metadata column for segment coloring
- `colorScheme`: Color palette (e.g., `'Bootstrap'`, `'RdYlBu'`)
- `hierarchy`: Array of column names defining hierarchy levels
- `objectBorderColor`: Border color for segments (e.g., `'rgb(0,0,0)'`)
- `showTransition`: Boolean to enable/disable animation
- `xAxis`: Array of axis column names
