---
title: "Radar Chart Skill"
description: "Generate CanvasXpress radar charts using Circular chart type with line, area, bar, dot, and stacked ring styles, half-circle layouts, rotation control, and metadata overlays."
---

# Radar Chart Skill

## Overview
Radar charts visualize multivariate data across multiple axes in a circular layout. CanvasXpress implements radar via Circular chart type with `circularType: 'radar'`, supporting line, area, bar, dot, and stacked ring graph types. Features include arc control (180° half-circle, 360° full), rotation, metadata overlays, and transition animations.

## Data Formats

### Radar with Factors and Magnitudes
```python
data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', ...],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', ...],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', ...],
  },
  'y': {
    'data': [[5, 10, 25, 40, 45, 50], [95, 80, 75, 70, 55, 40], ...],
    'desc': ['Magnitude1', 'Magnitude2'],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
  'z': {
    'Annt1': ['Desc : 1', 'Desc : 2', 'Desc : 3', 'Desc : 4'],
    'Annt2': ['Desc : A', 'Desc : B', 'Desc : A', 'Desc : B'],
  },
}
```

### Scatter Radar with Size/Color
```python
data = {
  'x': {
    'size': [93, 55, 57, ...],
    'color': ['red', 'red', 'blue', ...],
    'alpha': [0.44, 0.5, 0.41, ...],
  },
  'y': {
    'data': [[2, 1, 5, ...], [0.25, 1.07, 1.17, ...]],
    'smps': ['smp1', 'smp2', ...],
    'vars': ['radius', 'radians'],
  },
}
```

## Code Examples

### Example 1: Radar Line Chart
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', 'Lev : 1', 'Lev : 2', 'Lev : 3'],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', 'Lev : B', 'Lev : A', 'Lev : B'],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', 'Lev : Y', 'Lev : Z', 'Lev : Z'],
  },
  'y': {
    'data': [[5, 10, 25, 40, 45, 50], [95, 80, 75, 70, 55, 40], [25, 30, 45, 60, 65, 70], [55, 40, 35, 30, 15, 1]],
    'desc': ['Magnitude1', 'Magnitude2'],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
  'z': {
    'Annt1': ['Desc : 1', 'Desc : 2', 'Desc : 3', 'Desc : 4'],
    'Annt2': ['Desc : A', 'Desc : B', 'Desc : A', 'Desc : B'],
  },
}
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 360,
  'circularRotate': 0,
  'ringGraphType': ['line'],
  'colorScheme': 'Bootstrap',
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Radar - Line',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Radar Area Chart
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 360,
  'circularRotate': 0,
  'ringGraphType': ['area'],
  'colorScheme': 'Bootstrap',
  'legendPosition': 'top',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Radar - Area',
}
```

### Example 3: Radar Bar Chart
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 360,
  'circularRotate': 0,
  'ringGraphType': ['bar'],
  'colorScheme': 'Bootstrap',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Radar - Bar',
}
```

### Example 4: Half Radar
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 180,
  'circularRotate': 0,
  'ringGraphType': ['line'],
  'colorScheme': 'Bootstrap',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Half Radar',
}
```

### Example 5: Rotated Half Radar
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 180,
  'circularRotate': -90,
  'ringGraphType': ['line'],
  'colorScheme': 'Bootstrap',
  'legendPosition': 'top',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Rotated Half Radar',
}
```

### Example 6: Radar with Overlays
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularArc': 360,
  'circularRotate': 0,
  'ringGraphType': ['line'],
  'colorScheme': 'Bootstrap',
  'objectBorderColor': 'rgb(0,0,0)',
  'smpOverlays': ['Factor3', '-', 'Factor1', 'Factor2'],
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'title': 'Radar with Overlays',
}
```

### Example 7: Scatter Radar with Size/Color
```python
config = {
  'graphType': 'Circular',
  'circularType': 'radar',
  'circularTrackGraphType': ['scatter'],
  'colorBy': 'color',
  'sizeBy': 'size',
  'colorKey': {
    'color': {
      'red': '#FF0000',
      'blue': '#0000FF',
      'green': '#00FF00',
      'brown': '#A52A2A',
    },
  },
  'rAxis': 'radians',
  'yAxis': ['radius'],
  'setMinY': 0,
  'setMaxY': 5,
  'setMinR': 0,
  'setMaxR': 6.283185307179586,
  'showSampleNames': False,
  'showLegend': True,
  'rAxisShow': True,
  'rAxisPercentShow': False,
}
```

## Agent Prompts

- "Create a CanvasXpress radar chart with line rings showing performance across four variables."
- "Generate a radar area chart with Bootstrap color scheme and top legend."
- "Build a radar bar chart with four magnitudes across six factors."
- "Create a half-circle radar (180 degrees) with line style."
- "Generate a rotated half radar (180° arc, -90° rotation) with Bootstrap colors."
- "Build a radar chart with stacked ring style for cumulative data."
- "Create a radar chart with dot/scatter ring type."
- "Generate a radar with metadata overlays showing Factor3, Factor1, and Factor2."
- "Build a scatter radar with size by 'size' column and color by 'color' column."
- "Create a radar with custom color key mapping red, blue, green, and brown."
- "Generate a radar with radial axis from 0 to 2π (6.28) and radius 0-5."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "radar chart" | `graphType: 'Circular'`, `circularType: 'radar'` | Sets radar type |
| "line radar" | `ringGraphType: ['line']` | Line style rings |
| "area radar" | `ringGraphType: ['area']` | Filled area rings |
| "bar radar" | `ringGraphType: ['bar']` | Bar style rings |
| "dot radar" | `ringGraphType: ['dot']` | Dot/scatter rings |
| "stacked radar" | `ringGraphType: ['stacked']` | Stacked rings |
| "full circle" | `circularArc: 360` | Full 360° radar |
| "half circle" | `circularArc: 180` | Half 180° radar |
| "rotate" | `circularRotate: -90` | Rotates radar |
| "Bootstrap colors" | `colorScheme: 'Bootstrap'` | Bootstrap palette |
| "legend position" | `legendPosition: 'top'` | Sets legend location |
| "metadata overlay" | `smpOverlays: ['Factor3', '-', 'Factor1', 'Factor2']` | Adds overlays |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors by metadata |
| "size by [column]" | `sizeBy: 'ColumnName'` | Sizes by metadata |
| "color key" | `colorKey: {'ColumnName': {'val': '#hex'}}` | Custom color mapping |
| "radial axis" | `rAxis: 'ColumnName'` | Sets radial axis |
| "y-axis" | `yAxis: ['ColumnName']` | Sets y-axis |
| "radius range" | `setMinR: 0`, `setMaxR: 6.28` | Sets radial limits |
| "y range" | `setMinY: 0`, `setMaxY: 5` | Sets y-axis limits |
| "track type" | `circularTrackGraphType: ['scatter']` | Sets track style |

## Key Configuration Parameters

- `graphType`: Always `'Circular'` for radar charts
- `circularType`: `'radar'` for radar layout
- `circularArc`: `180` for half-circle, `360` for full circle
- `circularRotate`: Float/Int for rotation angle (e.g., `-90`)
- `ringGraphType`: Array of styles: `['line']`, `['area']`, `['bar']`, `['dot']`, `['stacked']`
- `circularTrackGraphType`: Array for track style (e.g., `['scatter']`)
- `colorScheme`: `'Bootstrap'` or custom palette
- `colorBy`: Column name for coloring
- `sizeBy`: Column name for sizing
- `colorKey`: Object mapping values to hex colors (e.g., `{'color': {'red': '#FF0000'}}`)
- `legendPosition`: `'top'`, `'bottom'`, etc.
- `legendKeyBackgroundBorderColor`: `'rgba(255,255,255,0)'` for invisible borders
- `legendKeyBackgroundColor`: `'rgba(255,255,255,0)'` for transparent background
- `objectBorderColor`: `'rgb(0,0,0)'` for black borders
- `smpOverlays`: Array of metadata columns for overlays (can include `'-'` as separator)
- `rAxis`: Column name for radial axis
- `yAxis`: Array of y-axis column names
- `setMinR`/`setMaxR`: Radial axis limits
- `setMinY`/`setMaxY`: Y-axis limits
- `rAxisShow`: Boolean to show radial axis
- `rAxisPercentShow`: Boolean to show percentage on radial axis
- `showSampleNames`: Boolean to display sample names
- `showLegend`: Boolean to show/hide legend
- `xAxis`: Array of x-axis column names
- `title`: Chart title
