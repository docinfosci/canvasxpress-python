---
title: "Venn Diagram Skill"
description: "Generate CanvasXpress Venn diagrams for 2, 3, or 4 sets with intersection counts and custom legend labels."
---

# Venn Diagram Skill

## Overview
Venn diagrams visualize set overlaps and unique elements. CanvasXpress supports 2, 3, or 4-set diagrams with intersection counts displayed in regions and customizable legend labels for each set.

## Data Formats

### Venn Data with Legend
```python
data = {
  'venn': {
    'data': {
      'A': 340,
      'AB': 639,
      'ABC': 552,
      'ABCD': 148,
      'ABD': 578,
      'AC': 456,
      'ACD': 298,
      'AD': 257,
      'B': 562,
      'BC': 915,
      'BCD': 613,
      'BD': 354,
      'C': 620,
      'CD': 143,
      'D': 592,
    },
    'legend': {
      'A': 'List 1',
      'B': 'List 2',
      'C': 'List 3',
      'D': 'List 4',
    },
  },
}
```

## Code Examples

### Example 1: Four-Set Venn Diagram
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'venn': {
    'data': {
      'A': 340,
      'AB': 639,
      'ABC': 552,
      'ABCD': 148,
      'ABD': 578,
      'AC': 456,
      'ACD': 298,
      'AD': 257,
      'B': 562,
      'BC': 915,
      'BCD': 613,
      'BD': 354,
      'C': 620,
      'CD': 143,
      'D': 592,
    },
    'legend': {
      'A': 'List 1',
      'B': 'List 2',
      'C': 'List 3',
      'D': 'List 4',
    },
  },
}
config = {
  'graphType': 'Venn',
  'vennGroups': 4,
  'showTransition': False,
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Three-Set Venn Diagram
```python
config = {
  'graphType': 'Venn',
  'vennGroups': 3,
  'showTransition': False,
}
```

### Example 3: Two-Set Venn Diagram
```python
config = {
  'graphType': 'Venn',
  'vennGroups': 2,
}
```

### Example 4: Four-Set Venn with Legend Labels
```python
config = {
  'graphType': 'Venn',
  'vennGroups': 4,
  'showTransition': False,
}
```

## Agent Prompts

- "Create a CanvasXpress 4-set Venn diagram showing overlaps between List 1 through List 4 with intersection counts."
- "Generate a 3-set Venn diagram with intersection data for A, B, C and their combinations."
- "Build a 2-set Venn diagram showing overlap between two lists with counts."
- "Create a Venn diagram with custom legend labels (e.g., 'List 1', 'Gene Set A', etc.)."
- "Generate a Venn diagram with no animation transitions for static display."
- "Build a Venn diagram highlighting large overlaps (e.g., BC with 915 elements) and small intersections (e.g., ABCD with 148)."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "venn diagram" | `graphType: 'Venn'` | Sets the chart type to Venn |
| "4-set" | `vennGroups: 4` | Creates 4-set Venn diagram |
| "3-set" | `vennGroups: 3` | Creates 3-set Venn diagram |
| "2-set" | `vennGroups: 2` | Creates 2-set Venn diagram |
| "no animation" | `showTransition: False` | Disables animation |
| "legend labels" | `venn.legend: {'A': 'List 1', ...}` | Customizes set names in legend |

## Key Configuration Parameters

- `graphType`: Always `'Venn'` for Venn diagrams
- `vennGroups`: Integer (2, 3, or 4) for number of sets
- `showTransition`: Boolean to enable/disable animation (default `True`)
- `venn.data`: Dictionary mapping intersection keys (`'A'`, `'AB'`, `'ABC'`, `'ABCD'`, etc.) to counts
- `venn.legend`: Dictionary mapping set keys (`'A'`, `'B'`, `'C'`, `'D'`) to display names
