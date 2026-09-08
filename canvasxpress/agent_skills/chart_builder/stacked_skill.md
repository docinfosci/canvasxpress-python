---
title: "Stacked Chart Skill"
description: "Generate CanvasXpress stacked charts with vertical/horizontal orientation, grouping by factors, treemap layouts, segregation, gradient fills, and data values display."
---

# Stacked Chart Skill

## Overview
Stacked charts display quantitative compositions across categories using stacked bars or areas. CanvasXpress supports vertical/horizontal layouts, multi-factor grouping, treemap nesting, sample segregation by metadata, gradient fills, and data value labels for rich compositional analysis.

## Data Formats

### Wide Format with Metadata Factors
```python
data = {
  'x': {
    'Factor1': ['F1-A', 'F1-A', 'F1-A', ...],
    'Factor2': ['F2-a', 'F2-a', 'F2-a', ...],
    'Factor3': ['F3-i', 'F3-i', 'F3-j', ...],
    'Factor4': ['F4-a', 'F4-a', 'F4-a', ...],
    'Factor5': ['F5-a', 'F5-b', 'F5-c', ...],
    'Factor6': [1, 2, 3, 4, 5, 6, ...],
  },
  'y': {
    'data': [
      [2, 4, 6, 8, 3, 5, 7, 9, ...],
      [4, 6, 8, 10, 3, 5, 7, 9, ...],
      [3, 5, 7, 9, 4, 6, 8, 10, ...],
    ],
    'smps': ['Smp1', 'Smp2', ...],
    'vars': ['Var1', 'Var2', 'Var3'],
  },
}
```

### Long Format with Segregation
```python
data = {
  'x': {
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', 'Lev : Y', 'Lev : Z', 'Lev : Z'],
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

### Example 1: Treemap Stacked Chart with Grouping and Nested Factors
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Factor1': ['F1-A', 'F1-A', 'F1-A', 'F1-A', 'F1-A', 'F1-A', 'F1-A', 'F1-A', 'F1-B', 'F1-B', 'F1-B', 'F1-B', 'F1-B', 'F1-B', 'F1-B', 'F1-B', 'F1-C', 'F1-C', 'F1-C', 'F1-C', 'F1-C', 'F1-C', 'F1-C', 'F1-C'],
    'Factor2': ['F2-a', 'F2-a', 'F2-a', 'F2-a', 'F2-b', 'F2-b', 'F2-b', 'F2-b', 'F2-c', 'F2-c', 'F2-c', 'F2-c', 'F2-d', 'F2-d', 'F2-d', 'F2-d', 'F2-e', 'F2-e', 'F2-e', 'F2-e', 'F2-f', 'F2-f', 'F2-f', 'F2-f'],
    'Factor3': ['F3-i', 'F3-i', 'F3-j', 'F3-j', 'F3-k', 'F3-k', 'F3-l', 'F3-l', 'F3-m', 'F3-m', 'F3-n', 'F3-n', 'F3-o', 'F3-o', 'F3-p', 'F3-p', 'F3-q', 'F3-q', 'F3-r', 'F3-r', 'F3-s', 'F3-s', 'F3-t', 'F3-t'],
    'Factor6': [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
  },
  'y': {
    'data': [
      [2, 4, 6, 8, 3, 5, 7, 9, 2, 4, 6, 8, 3, 5, 7, 9, 3, 5, 7, 9, 4, 6, 8, 10],
      [4, 6, 8, 10, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 2, 4, 6, 8, 3, 5, 7, 9],
      [3, 5, 7, 9, 4, 6, 8, 10, 3, 5, 7, 9, 2, 4, 6, 8, 4, 6, 8, 10, 3, 5, 7, 9],
    ],
    'smps': ['Smp1', 'Smp2', 'Smp3', 'Smp4', 'Smp5', 'Smp6', 'Smp7', 'Smp8', 'Smp9', 'Smp10', 'Smp11', 'Smp12', 'Smp13', 'Smp14', 'Smp15', 'Smp16', 'Smp17', 'Smp18', 'Smp19', 'Smp20', 'Smp21', 'Smp22', 'Smp23', 'Smp24'],
    'vars': ['Var1', 'Var2', 'Var3'],
  },
}
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'vertical',
  'colorScheme': 'Blues',
  'foreground': 'rgb(0,0,0)',
  'objectBorderColor': 'rgb(0,0,0)',
  'groupingFactors': ['Factor1'],
  'treemapBy': ['Factor2', 'Factor3'],
  'sampleSpaceFactor': 1,
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'title': 'Random Data',
  'xAxis': ['Var1', 'Var2', 'Var3'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Horizontal Stacked Bar with Data Values
```python
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'horizontal',
  'showDataValues': True,
  'sampleSpaceFactor': 1,
  'smpTextScaleFontFactor': 0.8,
  'smpTitle': 'Collection of Samples',
  'smpTitleFontStyle': 'italic',
  'legendBackgroundColor': False,
  'title': 'Random Data',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 3: Vertical Stacked with Gradient Fill
```python
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'vertical',
  'gradient': True,
  'smpTextScaleFontFactor': 0.8,
  'smpTitle': 'Collection of Samples',
  'smpTitleFontStyle': 'italic',
  'legendBackgroundColor': False,
  'title': 'Random Data',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 4: Horizontal Stacked with Segregation by Factor
```python
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'horizontal',
  'segregateSamplesBy': ['Factor3'],
  'showDataValues': True,
  'smpTextScaleFontFactor': 0.8,
  'smpTitle': 'Collection of Samples',
  'smpTitleFontStyle': 'italic',
  'legendBackgroundColor': False,
  'title': 'Random Data',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

### Example 5: Diverging Stacked Bar Chart
```python
config = {
  'graphType': 'Stacked',
  'graphOrientation': 'horizontal',
  'colorScheme': 'CanvasXpress',
  'axisAlgorithm': 'wilkinson',
  'showDataValues': True,
  'legendColumns': 3,
  'legendPosition': 'bottom',
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'xAxisTickFormat': '%s%%',
  'marginRight': 20,
  'title': 'Diverging Stacked Graph',
  'xAxis': ['Pants on Fire', 'False', 'Mostly False', 'Half True', 'Mostly True', 'True'],
}
```

## Agent Prompts

- "Create a CanvasXpress treemap stacked chart with grouping by Factor1 and nested by Factor2 and Factor3."
- "Generate a horizontal stacked bar chart with data values displayed and italic sample titles."
- "Build a vertical stacked chart with gradient fills for smooth color transitions."
- "Create a horizontal stacked chart segregated by Factor3 into separate panels."
- "Generate a diverging stacked bar chart with percentage formatting and 3-column bottom legend."
- "Build a stacked chart with black borders and foreground on white background."
- "Create a stacked chart with Blues color scheme and grouping factors."
- "Generate a horizontal stacked chart with transparent legend background."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "stacked chart" | `graphType: 'Stacked'` | Sets the chart type to stacked |
| "vertical" | `graphOrientation: 'vertical'` | Default, bars go up |
| "horizontal" | `graphOrientation: 'horizontal'` | Bars go left-to-right |
| "group by [column]" | `groupingFactors: ['ColumnName']` | Groups stacked bars by metadata |
| "treemap by" | `treemapBy: ['Column1', 'Column2']` | Creates nested treemap layout |
| "gradient" | `gradient: True` | Uses gradient color fills |
| "segregate by [column]" | `segregateSamplesBy: ['ColumnName']` | Splits chart by metadata |
| "show data values" | `showDataValues: True` | Displays values on bars |
| "diverging" | Data with negative/positive values + `axisAlgorithm: 'wilkinson'` | Creates diverging bars |
| "percentage format" | `xAxisTickFormat: '%s%%'` | Formats axis as percentages |
| "legend columns" | `legendColumns: N` | Sets legend column count |
| "legend position" | `legendPosition: 'bottom'` | Sets legend location |
| "black border" | `objectBorderColor: 'rgb(0,0,0)'` | Sets black borders |
| "foreground color" | `foreground: 'rgb(0,0,0)'` | Sets foreground text/stroke color |
| "sample space" | `sampleSpaceFactor: 1` | Controls sample spacing |
| "sample text scale" | `smpTextScaleFontFactor: 0.8` | Scales sample text size |
| "italic title" | `smpTitleFontStyle: 'italic'` | Makes sample title italic |
| "no legend bg" | `legendBackgroundColor: False` or `legendKeyBackgroundColor: 'rgba(255,255,255,0)'` | Transparent legend |
| "no transition" | `showTransition: False` | Disables animation |
| "margin right" | `marginRight: 20` | Adds right margin space |

## Key Configuration Parameters

- `graphType`: Always `'Stacked'` for stacked charts
- `graphOrientation`: `'vertical'` (default) or `'horizontal'`
- `colorScheme`: Color palette (e.g., `'Blues'`, `'CanvasXpress'`)
- `gradient`: Boolean to enable gradient color fills
- `groupingFactors`: Array of metadata columns for grouping bars
- `treemapBy`: Array of metadata columns for nested treemap layout
- `segregateSamplesBy`: Array to split chart into separate panels
- `showDataValues`: Boolean to display values on stacked bars
- `axisAlgorithm`: `'wilkinson'` for diverging bar axis algorithm
- `sampleSpaceFactor`: Float for sample spacing control
- `smpTextScaleFontFactor`: Float for sample text scaling
- `smpTitleFontStyle`: `'italic'`, `'bold'`, or `'normal'`
- `foreground`: Text/stroke color (e.g., `'rgb(0,0,0)'`)
- `objectBorderColor`: Border color for stacked elements
- `legendBackgroundColor`: Boolean `False` or color for legend background
- `legendKeyBackgroundColor`: Background for legend keys
- `legendKeyBackgroundBorderColor`: Border for legend keys
- `legendColumns`: Number of columns in legend
- `legendPosition`: `'bottom'`, `'top'`, `'left'`, `'right'`
- `showTransition`: Boolean to enable/disable animation
- `xAxisTickFormat`: Format string (e.g., `'%s%%'` for percentages)
- `marginRight`: Integer for right margin padding
