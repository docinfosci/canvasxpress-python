---
name: styling
description: CanvasXpress styling and theming including theme selection, color palettes, object styling (shapes, sizes, borders, transparency), font settings, layout, dimensions, and orientation. Use when customizing chart appearance, applying color schemes, or adjusting layout.
---

# Styling & Theming

## Theme Selection

```python
config = {
    "theme": "CanvasXpress",    # Built-in theme
    "colorScheme": "CanvasXpress",  # Color palette scheme
    "background": "rgb(255,255,255)",  # Chart background
}
```

## Color Configuration

```python
config = {
    # Custom color palette
    "colors": ["rgb(31,119,180)", "rgb(255,127,14)", "rgb(44,160,44)"],
    
    # Object styling
    "objectColor": "rgb(69,117,180)",
    "objectColorTransparency": 0.3,  # 0 = opaque, 1 = transparent
    "objectBorderColor": "rgb(0,0,0)",
    "objectBorderThickness": 1,
    
    # Line styling
    "lineThickness": 3,
    "lineType": "spline",  # or "straight"
    
    # Shape styling
    "objectShape": "circle",  # circle, square, triangle, etc.
    "objectSize": 10,
    
    # Highlight/selection color
    "highlightColor": "rgb(30,120,220)",
}
```

## Layout & Dimensions

```python
cx = CanvasXpress(
    data=data,
    config={"graphType": "Bar"},
    width=800,
    height=600,
)
```

## Font & Label Styling

```python
config = {
    "title": "Chart Title",
    "subtitle": "Optional subtitle",
    "xAxisTitle": "X Axis Label",
    "yAxisTitle": "Y Axis Label",
    "legendScaleFontFactor": 1,     # Scale factor for legend text
    # Font sizes inherit from theme; adjust via CSS for custom fonts
}
```

## Orientation

```python
config = {
    "graphOrientation": "vertical",  # or "horizontal"
}
```

## Chart-Type-Specific Styling

### Scatter2D

```python
config = {
    "objectShape": "circle",
    "objectColor": "rgb(69,117,180)",
    "dataPointSizeScaleFactor": 2,
    "objectColorTransparency": 0.3,
}
```

### Heatmap

```python
config = {
    "heatMapping": "color",
    "colorZToData": True,          # Color based on data range
    "objectBorderColor": "rgb(255,255,255)",
    "objectBorderThickness": 1,
}
```

### Bar / Stacked

```python
config = {
    "objectBorderColor": "rgb(0,0,0)",
    "objectBorderThickness": 1,
    "barGrouping": "group",        # or "stack"
    "graphOrientation": "vertical",
}
```

### Network

```python
config = {
    "nodeLabelSize": 10,
    "ringGraphWeight": [25, 25, 25, 25],
}
```

### Pie / Treemap

```python
config = {
    "showLegend": False,           # Often unnecessary for pie
    "treemapBorderWidth": 0,
}
```

### Line

```python
config = {
    "lineType": "spline",
    "lineThickness": 3,
    "llmHeader": [["V1", "V2", "V3", "V4"]],
}
```

### Histogram Overlay

```python
config = {
    "showHistogram": True,
    "histogramBins": 5,
}
```

### Sample Overlays

For advanced metadata visualization on heatmaps:

```python
config = {
    "smpOverlayProperties": {
        "Factor1": {
            "type": "Default",
            "color": "rgb(10,176,219)",
            "spectrum": ["rgb(69,117,180)", "rgb(145,191,219)"],
            "scheme": "CanvasXpress",
            "showLegend": True
        }
    },
    "showSmpOverlaysLegend": True,
}
```

## Complete Styling Template

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Scatter2D",
        "title": "Styled Chart",
        "subtitle": "Optional context",
        "xAxisTitle": "X Axis Label",
        "yAxisTitle": "Y Axis Label",
        "theme": "CanvasXpress",
        "colorScheme": "CanvasXpress",
        "background": "rgb(255,255,255)",
        "showLegend": True,
        "showLegendBorder": True,
        "legendScaleFontFactor": 1,
        "graphOrientation": "vertical",
        "objectShape": "circle",
        "objectColor": "rgb(69,117,180)",
        "objectColorTransparency": 0.3,
        "objectBorderColor": "rgb(0,0,0)",
        "objectBorderThickness": 1,
    },
    width=800,
    height=600,
)
graph(cx)
```
