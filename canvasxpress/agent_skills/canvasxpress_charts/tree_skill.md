---
title: "Tree Chart Skill"
description: "Generate CanvasXpress tree charts with hierarchical data, collapsible nodes, circular/bracket layouts, metadata coloring, and annotations."
---

# Tree Chart Skill

## Overview
Tree charts display hierarchical data with expandable/collapsible nodes. CanvasXpress supports linear, circular, and bracket layouts, metadata-based coloring, annotations, and multi-level hierarchies for exploring nested relationships.

## Data Formats

### Multi-Level Hierarchy with Annotations
```python
data = {
  'x': {
    'Level1': ['L1.1', 'L1.1', 'L1.1', 'L1.1', 'L1.2', ...],
    'Level2': ['L2.1', 'L2.1', 'L2.2', 'L2.2', 'L2.1', ...],
    'Level3': ['L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', ...],
    'Annot1': ['A', 'B', 'C', 'A', 'B', ...],
    'Annot2': [5, 10, 15, 20, 25, ...],
  },
  'y': {
    'data': [
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    ],
    'smps': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
    'vars': ['Order'],
  },
}
```

### Bracket Hierarchy
```python
data = {
  'x': {
    'Final': ['I']*16,
    'Semifinal': ['A']*8 + ['I']*8,
    '4th': ['A']*4 + ['G']*4 + ['I']*4 + ['N']*4,
    '8th': ['A']*2 + ['C']*2 + ['E']*2 + ['G']*2 + ['I']*2 + ['K']*2 + ['N']*2 + ['O']*2,
  },
  'y': {
    'data': [[37, 12, 23, 14, 25, 16, 27, 18, 39, 20, 31, 22, 31, 34, 25, 26]],
    'smps': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
    'vars': ['Goals'],
  },
}
```

## Code Examples

### Example 1: Collapsible Linear Tree with Three Levels
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Level1': ['L1.1', 'L1.1', 'L1.1', 'L1.1', 'L1.2', 'L1.2', 'L1.2', 'L1.2', 'L1.3', 'L1.3', 'L1.3', 'L1.3', 'L1.4', 'L1.4', 'L1.4', 'L1.4'],
    'Level2': ['L2.1', 'L2.1', 'L2.2', 'L2.2', 'L2.1', 'L2.1', 'L2.2', 'L2.2', 'L2.1', 'L2.1', 'L2.2', 'L2.2', 'L2.1', 'L2.1', 'L2.2', 'L2.2'],
    'Level3': ['L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2', 'L3.1', 'L3.2'],
  },
  'y': {
    'data': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]],
    'smps': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
    'vars': ['Order'],
  },
}
config = {
  'graphType': 'Tree',
  'hierarchy': ['Level1', 'Level2', 'Level3'],
  'treeLabelAlign': 'left',
  'showTransition': True,
  'title': 'Collapsible Tree',
  'xAxis': ['Order'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Two-Level Tree
```python
config = {
  'graphType': 'Tree',
  'hierarchy': ['Level1', 'Level2'],
  'showTransition': True,
  'title': 'Collapsible Tree',
  'xAxis': ['Order'],
}
```

### Example 3: Tree Colored by Metadata (Left Labels)
```python
config = {
  'graphType': 'Tree',
  'hierarchy': ['Level1', 'Level2', 'Level3'],
  'colorBy': 'Annot1',
  'treeLabelAlign': 'left',
  'showTransition': True,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'xAxis': ['Order'],
}
```

### Example 4: Tree Colored by Numeric Annotation (Right Labels)
```python
config = {
  'graphType': 'Tree',
  'hierarchy': ['Level1', 'Level2', 'Level3'],
  'colorBy': 'Annot2',
  'treeLabelAlign': 'right',
  'showTransition': True,
  'title': 'Collapsible Tree',
  'xAxis': ['Order'],
}
```

### Example 5: Circular Tree
```python
config = {
  'graphType': 'Tree',
  'hierarchy': ['Level1', 'Level2', 'Level3'],
  'colorBy': 'Annot2',
  'treeType': 'circular',
  'showTransition': True,
  'title': 'Collapsible Tree',
  'xAxis': ['Order'],
}
```

### Example 6: Inverted Bracket Tree
```python
config = {
  'graphType': 'Tree',
  'hierarchy': ['Final', 'Semifinal', '4th', '8th'],
  'treeType': 'bracket',
  'treeInverted': True,
  'treeNodeSizeScaleFactor': 4,
  'treeClickDisable': True,
  'treeBracketLabelAlign': 'left',
  'showTransition': False,
  'title': 'Bracket',
  'xAxis': ['Goals'],
}
```

## Agent Prompts

- "Create a CanvasXpress collapsible linear tree with three hierarchy levels (Level1, Level2, Level3) and left-aligned labels."
- "Generate a two-level tree chart showing Level1 and Level2 hierarchy with transitions enabled."
- "Build a tree colored by Annot1 metadata with left-aligned labels and transparent legend."
- "Create a tree chart colored by numeric Annot2 values with right-aligned labels."
- "Generate a circular tree layout with three levels and metadata coloring."
- "Build an inverted bracket tree showing tournament progression with 4 stages."
- "Create a bracket tree with disabled node clicking and scaled node sizes."
- "Generate a collapsible tree with smooth transitions for interactive exploration."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "tree chart" | `graphType: 'Tree'` | Sets the chart type to tree |
| "hierarchy" | `hierarchy: ['Level1', 'Level2', 'Level3']` | Defines hierarchical columns |
| "collapsible" | `showTransition: True` | Enables expand/collapse with animation |
| "linear tree" | `treeType: 'linear'` (default) | Standard linear tree layout |
| "circular tree" | `treeType: 'circular'` | Radial/circular tree layout |
| "bracket tree" | `treeType: 'bracket'` | Tournament bracket layout |
| "inverted" | `treeInverted: True` | Flips tree direction (bracket only) |
| "left labels" | `treeLabelAlign: 'left'` | Aligns labels to left |
| "right labels" | `treeLabelAlign: 'right'` | Aligns labels to right |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors nodes by metadata |
| "no legend bg" | `legendKeyBackgroundColor: 'rgba(255,255,255,0)'` | Transparent legend background |
| "no transitions" | `showTransition: False` | Disables animation |
| "node size scale" | `treeNodeSizeScaleFactor: N` | Scales node sizes |
| "disable clicking" | `treeClickDisable: True` | Prevents node interaction |
| "bracket label align" | `treeBracketLabelAlign: 'left'` | Aligns bracket labels |

## Key Configuration Parameters

- `graphType`: Always `'Tree'` for tree charts
- `hierarchy`: Array of column names defining hierarchy levels (e.g., `['Level1', 'Level2', 'Level3']`)
- `treeType`: `'linear'` (default), `'circular'`, or `'bracket'` for layout style
- `treeInverted`: Boolean to flip tree direction (bracket only)
- `treeLabelAlign`: `'left'` or `'right'` for label alignment
- `colorBy`: Metadata column for node coloring
- `showTransition`: Boolean to enable/disable collapse/expand animation
- `treeNodeSizeScaleFactor`: Float to scale node sizes
- `treeClickDisable`: Boolean to prevent node interaction
- `treeBracketLabelAlign`: `'left'` for bracket label alignment
- `legendKeyBackgroundColor`: Background color for legend (use `'rgba(255,255,255,0)'` for transparent)
- `legendKeyBackgroundBorderColor`: Border color for legend (use `'rgba(255,255,255,0)'` for transparent)
