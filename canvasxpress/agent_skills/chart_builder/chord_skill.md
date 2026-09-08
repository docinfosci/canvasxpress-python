---
title: "Chord Diagram Skill"
description: "Generate CanvasXpress chord diagrams using Circular chart type showing relationships between categories with color highlighting, rotation, and arc control."
---

# Chord Diagram Skill

## Overview
Chord diagrams visualize relationships and flows between categories as ribbons connecting circular segments. CanvasXpress implements chord diagrams via the Circular chart type with `circularType: 'chord'`, supporting full/partial arcs, rotation, largest-value highlighting, and custom color schemes.

## Data Formats

### Square Matrix
```python
data = {
  'y': {
    'data': [
      [11975, 5871, 8916, 2868],
      [1951, 10048, 2060, 6171],
      [8010, 16145, 8090, 8045],
      [1013, 990, 940, 6907],
    ],
    'smps': ['A', 'B', 'C', 'D'],
    'vars': ['A', 'B', 'C', 'D'],
  },
}
```

## Code Examples

### Example 1: Simple Full Chord Diagram
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [11975, 5871, 8916, 2868],
      [1951, 10048, 2060, 6171],
      [8010, 16145, 8090, 8045],
      [1013, 990, 940, 6907],
    ],
    'smps': ['A', 'B', 'C', 'D'],
    'vars': ['A', 'B', 'C', 'D'],
  },
}
config = {
  'graphType': 'Circular',
  'circularType': 'chord',
  'circularArc': 360,
  'circularRotate': 0,
  'colors': ['#000000', '#FFDD89', '#957244', '#F26223'],
  'higlightGreyOut': True,
  'objectBorderColor': 'rgb(0,0,0)',
  'rAxisTickFormat': ['%sK', ' / 1000'],
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'title': 'Simple Chord Graph',
  'transitionStep': 50,
  'transitionTime': 1500,
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Rotated Chord with Largest Highlight
```python
config = {
  'graphType': 'Circular',
  'circularType': 'chord',
  'circularArc': 360,
  'circularRotate': 180,
  'chordColor': 'largest',
  'higlightGreyOut': True,
  'objectBorderColor': 'rgb(0,0,0)',
  'rAxisTickFormat': ['%sK', ' / 1000'],
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'title': 'Rotated Chord Graph',
  'transitionStep': 50,
  'transitionTime': 1500,
}
```

### Example 3: Half Chord Diagram (180 Arc)
```python
config = {
  'graphType': 'Circular',
  'circularType': 'chord',
  'circularArc': 180,
  'circularRotate': -90,
  'higlightGreyOut': True,
  'objectBorderColor': 'rgb(0,0,0)',
  'rAxisTickFormat': ['%sK', ' / 1000'],
  'showLegend': False,
  'showTransition': False,
  'title': 'Rotated Half Chord Graph',
  'transitionStep': 50,
  'transitionTime': 1500,
}
```

### Example 4: Round Robin Tournament Similarity
```python
config = {
  'graphType': 'Circular',
  'circularType': 'chord',
  'circularArc': 360,
  'circularRotate': 180,
  'chordColor': 'largest',
  'chordScaleShow': False,
  'higlightGreyOut': True,
  'objectBorderColor': 'rgb(0,0,0)',
  'showTransition': False,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'title': 'Four way Round Robin Tournament',
}
```

## Agent Prompts

- "Create a CanvasXpress full 360-degree chord diagram with 4 categories and custom colors."
- "Generate a rotated chord diagram (180 degrees) with largest-value highlighting."
- "Build a half-circle chord diagram (180 arc) with -90 degree rotation."
- "Create a chord diagram showing similarity matrix for a round-robin tournament."
- "Generate a chord diagram with grey-out highlighting and black borders."
- "Build a chord diagram with axis tick format showing thousands (%sK)."
- "Create a chord diagram with transition animation (1500ms duration)."
- "Generate a chord diagram with scale labels hidden."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "chord diagram" | `graphType: 'Circular'` + `circularType: 'chord'` | Sets chord visualization |
| "full circle" | `circularArc: 360` | Full 360-degree arc |
| "half circle" | `circularArc: 180` | Half 180-degree arc |
| "rotate" | `circularRotate: N` | Rotates diagram by N degrees |
| "largest highlight" | `chordColor: 'largest'` | Colors largest chords distinctly |
| "grey out" | `higlightGreyOut: True` | Grey-outs non-highlighted elements |
| "no scale" | `chordScaleShow: False` | Hides scale labels |
| "black border" | `objectBorderColor: 'rgb(0,0,0)'` | Sets chord border color |
| "axis format" | `rAxisTickFormat: ['%sK', ' / 1000']` | Formats axis labels |
| "custom colors" | `colors: ['#hex1', '#hex2', ...]` | Sets chord colors |
| "no legend bg" | `legendKeyBackgroundColor: 'rgba(255,255,255,0)'` | Transparent legend background |
| "transition" | `showTransition: True` + `transitionTime: 1500` + `transitionStep: 50` | Enables animation |

## Key Configuration Parameters

- `graphType`: Always `'Circular'` for chord diagrams
- `circularType`: `'chord'` for chord diagram layout
- `circularArc`: Integer for arc degrees (180 = half, 360 = full)
- `circularRotate`: Integer for rotation angle in degrees
- `chordColor`: `'largest'` to highlight maximum-value chords
- `chordScaleShow`: Boolean to show/hide scale labels
- `higlightGreyOut`: Boolean to enable grey-out effect
- `objectBorderColor`: Color for chord borders (e.g., `'rgb(0,0,0)'`)
- `colors`: Array of hex colors for categories
- `rAxisTickFormat`: Array of format strings (e.g., `['%sK', ' / 1000']`)
- `showTransition`: Boolean to enable/disable animation
- `transitionTime`: Integer for animation duration in ms
- `transitionStep`: Integer for animation step size
- `showLegend`: Boolean to show/hide legend
- `legendKeyBackgroundColor`: Background color for legend keys
- `legendKeyBackgroundBorderColor`: Border color for legend keys
