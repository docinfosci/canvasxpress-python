---
title: "Treemap Chart Skill"
description: "Generate CanvasXpress treemaps using Treemap and Stacked chart types with hierarchical data, metadata coloring, marker decorations, and region/ISO3 grouping."
---

# Treemap Chart Skill

## Overview
Treemaps visualize hierarchical data with nested rectangles sized and colored by metrics. CanvasXpress supports both dedicated Treemap chart type and Stacked chart type with `treemapBy` option. Features include metadata coloring (e.g., GNI), annotation markers with text labels, continent/ISO3 grouping, and interactive hover displays.

## Data Formats

### Hierarchical Country Data
```python
data = {
  'x': {
    'GNI': [106140, 103630, 92200, ...],
    'ISO3': ['BMU', 'NOR', 'QAT', ...],
    'continent': ['North America', 'Europe', 'Asia', ...],
  },
  'y': {
    'data': [[67837, 4676305, 833285, ...]],
    'smps': ['Bermuda', 'Norway', 'Qatar', ...],
    'vars': ['population'],
  },
}
```

### Simple Variable Hierarchical Data
```python
data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', ...],
    'Factor2': ['Lev : A', 'Lev : B', ...],
  },
  'y': {
    'data': [[5, 10, 25, ...], [95, 80, 75, ...], ...],
    'desc': ['Magnitude1', 'Magnitude2'],
    'smps': ['S1', 'S2', ...],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
  'z': {
    'Annt1': ['Desc : 1', 'Desc : 2', ...],
  },
}
```

## Code Examples

### Example 1: Population by Country with GNI Coloring
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'GNI': [106140, 103630, 92200, 88120, ...],
    'ISO3': ['BMU', 'NOR', 'QAT', 'CHE', ...],
    'continent': ['North America', 'Europe', 'Asia', ...],
  },
  'y': {
    'data': [[67837, 4676305, 833285, 7604467, ...]],
    'smps': ['Bermuda', 'Norway', 'Qatar', 'Switzerland', ...],
    'vars': ['population'],
  },
}
config = {
  'graphType': 'Treemap',
  'colorBy': 'GNI',
  'objectBorderColor': 'rgb(0,0,0)',
  'decorations': {
    'marker': [
      {
        'align': 'center',
        'baseline': 'middle',
        'color': 'red',
        'sample': 'Norway',
        'text': 'Norway is the country\nwith the largest GNI\naccording to 2014 census',
        'variable': 'population',
        'x': 0.65,
        'y': 0.7,
      },
      {
        'align': 'center',
        'baseline': 'middle',
        'color': 'red',
        'sample': 'China',
        'text': 'China is the country with\nthe largest population\naccording to 2014 census',
        'variable': 'population',
        'x': 0.15,
        'y': 0.1,
      },
    ],
  },
  'showDecorations': False,
  'showTransition': False,
  'xAxis': ['population'],
  'title': 'Population colored by Gross National Income 2014',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Interactive Treemap with Magnitudes
```python
config = {
  'graphType': 'Treemap',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 3: Stacked Vertical Treemap
```python
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'vertical',
  'colorBy': 'GNI',
  'treemapBy': ['ISO3'],
  'objectBorderColor': 'rgb(0,0,0)',
  'legendInside': True,
  'legendPosition': 'right',
  'smpTextRotate': 45,
  'axisAlgorithm': 'rPretty',
  'xAxis': ['population'],
  'xAxisGridMinorShow': False,
  'title': 'Country Population colored by Gross National Income',
  'subtitle': '2014 Census',
}
```

## Agent Prompts

- "Create a CanvasXpress treemap showing population by country colored by GNI."
- "Generate a treemap with marker decorations highlighting Norway and China."
- "Build a hierarchical treemap with factors Lev, A, B, X, Y, Z and magnitudes."
- "Create a stacked vertical treemap grouped by ISO3 with right legend."
- "Generate a treemap with GNI color coding and black borders."
- "Build a treemap with annotation markers at specific x/y positions."
- "Create a treemap with sample text rotated 45 degrees."
- "Generate a treemap with hidden decorations (showDecorations: False)."
- "Build a hierarchical data treemap with magnitude series across variables."
- "Create a treemap with subtitle '2014 Census' and population data."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "treemap" | `graphType: 'Treemap'` | Sets treemap chart type |
| "stacked treemap" | `graphType: 'Stacked'`, `treemapBy: [...]` | Uses stacked as treemap |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors by metadata |
| "group by [column]" | `treemapBy: ['ColumnName']` | Groups by metadata |
| "marker decoration" | `decorations: {'marker': [...]}` | Adds text markers |
| "highlight country" | `decorations: {'marker': [{'sample': 'Country', ...}]}` | Highlights specific sample |
| "black borders" | `objectBorderColor: 'rgb(0,0,0)'` | Sets black borders |
| "legend inside" | `legendInside: True` | Places legend inside |
| "legend position" | `legendPosition: 'right'` | Sets legend location |
| "rotate text" | `smpTextRotate: 45` | Rotates sample text |
| "vertical" | `graphOrientation: 'vertical'` | Sets vertical orientation |
| "show decorations" | `showDecorations: False` | Hides decorations |
| "transition" | `showTransition: False` | Disables animation |
| "axis algorithm" | `axisAlgorithm: 'rPretty'` | Sets axis formatting |
| "subtitle" | `subtitle: 'Text'` | Adds subtitle |
| "x-axis" | `xAxis: ['ColumnName']` | Sets x-axis column |
| "hide minor grid" | `xAxisGridMinorShow: False` | Hides minor grid lines |

## Key Configuration Parameters

- `graphType`: `'Treemap'` for treemap, `'Stacked'` with `treemapBy` for stacked treemap
- `graphOrientation`: `'vertical'` for vertical stacked layout
- `colorBy`: Metadata column for coloring (e.g., `'GNI'`)
- `treemapBy`: Array of columns for grouping (e.g., `['ISO3']`)
- `objectBorderColor`: `'rgb(0,0,0)'` for black borders
- `decorations`: Object with `marker` array for annotations
  - `align`: `'center'` for text alignment
  - `baseline`: `'middle'` for vertical alignment
  - `color`: `'red'` for marker color
  - `sample`: Sample name to highlight
  - `text`: Multiline annotation text (use `\n` for breaks)
  - `variable`: Variable name for reference
  - `x`: Float position (0-1)
  - `y`: Float position (0-1)
- `showDecorations`: Boolean to show/hide decorations
- `showTransition`: Boolean to enable/disable animation
- `legendInside`: Boolean to place legend inside chart
- `legendPosition`: `'right'`, `'left'`, `'top'`, `'bottom'`
- `smpTextRotate`: Rotation angle for sample text (e.g., `45`)
- `axisAlgorithm`: `'rPretty'` for axis formatting
- `xAxis`: Array of x-axis column names
- `xAxisGridMinorShow`: Boolean to show/hide minor grid lines
- `title`: Chart title
- `subtitle`: Chart subtitle
