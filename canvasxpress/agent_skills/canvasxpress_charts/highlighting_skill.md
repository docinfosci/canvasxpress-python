---
name: highlighting
description: CanvasXpress highlighting and selection patterns including declarative highlighting, ghost/focus modes, predicate-based highlighting, interactive selection, emphasis colors, and storytelling techniques. Use when creating charts that emphasize specific data points, guide reader attention, or enable interactive selection.
---

# Highlighting & Selection Patterns

## Declarative Highlighting

Emphasize specific variables or samples on load:

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightVar": ["Freddy", "Isabelle"],  # Emphasize these variables
        "highlightSmp": ["Keith"],                # Or emphasize samples
    }
)
graph(cx)
```

## Highlight Modes

Three render styles control how highlighted/non-highlighted elements appear:

### Highlight Mode

Recolors the chosen marks:

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightVar": ["Freddy", "Isabelle"],
        "highlightMode": "highlight",   # Recolors chosen marks
    }
)
graph(cx)
```

### Ghost Mode

Fades non-chosen marks:

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightVar": ["Freddy", "Isabelle"],
        "highlightMode": "ghost",       # Fades non-chosen marks
        "highlightGreyOut": 0.5,         # Strength of fade (0-1)
    }
)
graph(cx)
```

### Focus Mode

Greys non-chosen marks, keeps chosen in full color (like ggplot2's gghighlight):

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightVar": ["Freddy", "Isabelle"],
        "highlightMode": "focus",       # Greys non-chosen, keeps chosen in color
        "highlightGreyOut": 0.5,         # Strength of de-emphasis
    }
)
graph(cx)
```

## Highlight by Predicate

Dynamically highlight based on data values — no need to name specific elements:

```python
# Focus individuals taller than 170 cm (max of their measurements > 170)
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightBy": {
            "target": "variable",  # or "sample"
            "stat": "max",         # mean, max, min, sum, median
            "operator": ">",       # >, <, >=, <=, ==, !=
            "value": 170
        }
        # Automatically switches to focus mode
    }
)
graph(cx)
```

## Interactive Selection

Let users click/lasso to select, with configurable response modes:

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "selectionMode": "focus",    # highlight, ghost, focus, name, filter
        "selectedDataPoints": ["Freddy"],  # Pre-selected on load
    }
)
graph(cx)

# Switch selection mode live (JavaScript):
# cXSel.setConfig({ selectionMode: mode });
# cXSel.draw();
```

## Emphasis Colors

Global and per-target emphasis colors:

```python
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "highlightColor": "rgb(30,120,220)",  # Global emphasis color
        # Legacy per-target overrides (deprecated, inherit from highlightColor):
        # "varHighlightColor": "rgb(30,120,220)"
        # "smpHighlightColor": "rgb(30,120,220)"
        # "nodeHighlightColor": "rgb(30,120,220)"
        # "selectionColor": "rgb(30,120,220)"
    }
)
graph(cx)
```

## Complete Highlighting Storytelling Template

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "title": "Key Outliers",
        "highlightVar": ["Freddy", "Isabelle"],
        "highlightMode": "focus",     # Greys out non-highlighted
        "highlightColor": "rgb(30,120,220)",
        "xAxisTitle": "Height",
        "yAxisTitle": "Weight"
    }
)
graph(cx)
```
