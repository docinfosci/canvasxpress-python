---
name: broadcast
description: Coordinate multiple CanvasXpress charts via automatic broadcasting, filter propagation, legend coordination, DOE dashboards, and page-level saved states. Use when building multi-chart dashboards where clicking or filtering in one chart updates others.
---

# Broadcasting & Cross-Chart Coordination

CanvasXpress provides automatic broadcast mechanisms for linking multiple visualizations without extra code.

## Basic Broadcasting (Automatic)

By default, clicking a data point in one chart highlights corresponding points in ALL charts on the page. No configuration needed:

```python
# Chart 1: Scatter
cx1 = CanvasXpress(
    data=data1,
    config={"graphType": "Scatter2D", "title": "Height vs Weight"}
)

# Chart 2: Bar
cx2 = CanvasXpress(
    data=data2,
    config={"graphType": "Bar", "title": "Age by Gender"}
)

# Chart 3: Heatmap
cx3 = CanvasXpress(
    data=data3,
    config={"graphType": "Heatmap", "title": "Measurements"}
)

graph(cx1)
graph(cx2)
graph(cx3)
# Clicking a point in any chart highlights corresponding data in all others
```

## Broadcast Groups

Limit broadcasting to a specific subset of charts:

```python
cx1 = CanvasXpress(
    data=data1,
    config={
        "graphType": "Scatter2D",
        "broadcastGroup": "sales-overview"  # Only coordinates with same group ID
    }
)

cx2 = CanvasXpress(
    data=data2,
    config={
        "graphType": "Bar",
        "broadcastGroup": "sales-overview"  # Same group = coordinated
    }
)

cx3 = CanvasXpress(
    data=data3,
    config={
        "graphType": "Heatmap",
        "broadcastGroup": "separate-group"  # Different group = independent
    }
)
```

## Filter Broadcasting

Filtering in one chart propagates to all charts in the same broadcast group. On by default; opt out with:

```python
cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Scatter2D",
        "broadcastFilter": False  # Opt out of filter broadcasting
    }
)
```

## Legend Broadcasting

Hide/show data via legend clicks, coordinated across charts:

```python
cx1 = CanvasXpress(
    data=data,
    config={
        "graphType": "Scatter2D",
        "colorBy": "cyl",           # Color by cylinder count
        "broadcastGroup": "legends",  # Group for legend coordination
        "legendScaleFontFactor": 3
    }
)
# Clicking legend items hides/shows data across all charts in "legends" group
# Press Ctrl+Esc to reset all
```

## Page-Level Saved States

Save and restore coordinated chart states across all graphs:

```python
# In JavaScript (called from event handlers or browser console):
# CanvasXpress.savePageState("My View");
# CanvasXpress.applyPageState("My View");
# CanvasXpress.deletePageState("My View");
# CanvasXpress.getPageStates();  # -> ["My View", ...]

# Optional: scope to one broadcastGroup
# CanvasXpress.savePageState("My View", "sales-overview");
```

## DOE (Design of Experiments) Dashboard

A single chart that acts as a dashboard, filtering data for other charts:

```python
# All metadata in x, one numerical variable in y
doe_data = {
    "x": {
        "Height": [174, 161, 194, 160, 173, 151],
        "Weight": [65.6, 51.6, 80.7, 49.2, 55.2, 48.7],
        "Hip": [93.5, 92, 95, 91, 90.3, 89.9],
        "Waist": [71.5, 66.5, 83.2, 61.2, 66.5, 61.6],
        "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"],
        "Excercise": ["Low", "Moderate", "Moderate", "Moderate", "Low", "Intense"]
    },
    "y": {
        "vars": ["Age"],
        "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
        "data": [[21, 22, 28, 19, 32, 35]]
    }
}

cx = CanvasXpress(
    data=doe_data,
    config={"graphType": "Bar", "histogramBins": 5},
    after_render=[["createDOE", []]]  # Creates interactive DOE dashboard
)
graph(cx)
# Clicking pie charts or histograms filters data across all coordinated charts
```

## Complete Dashboard Template

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# Multiple charts that coordinate via automatic broadcasting
# Clicking a point in any chart highlights corresponding data in all others

scatter = CanvasXpress(
    data=scatter_data,
    config={
        "graphType": "Scatter2D",
        "title": "Height vs Weight"
    }
)

bar = CanvasXpress(
    data=bar_data,
    config={
        "graphType": "Bar",
        "title": "Age Distribution"
    }
)

heatmap = CanvasXpress(
    data=heatmap_data,
    config={
        "graphType": "Heatmap",
        "title": "Measurements Overview"
    }
)

graph(scatter)
graph(bar)
graph(heatmap)
```
