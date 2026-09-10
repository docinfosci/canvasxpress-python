---
title: "Chart Types Reference"
description: "CanvasXpress chart type mappings, Plotly/Matplotlib conversions, and sub-skill catalog."
---

# Chart Types Reference

## Chart Type Catalog

### Core Chart Types

These are the base `graphType` values that CanvasXpress supports directly:

| Config Value | chartType | User-Requested Meta Charts |
|---|---|---|
| `"Bar"` | Bar | Waterfall, Lollipop, Bullet*, Stacked |
| `"Line"` | Line | Area, Streamgraph |
| `"Scatter2D"` | Scatter2D | Density, Histogram |
| `"Scatter3D"` | Scatter3D | (none) |
| `"Bubble"` | Bubble | (built-in) |
| `"Heatmap"` | Heatmap | Contour, Correlation |
| `"Boxplot"` | Boxplot | Violin |
| `"Pie"` | Pie | Donut |
| `"Circular"` | Circular | Chord, Sunburst, Radar |
| `"Network"` | Network | (none) |
| `"Tree"` | Tree | (none) |
| `"Sankey"` | Sankey | (none) |
| `"Dotplot"` | Dotplot | (none) |
| `"Map"` | Map | (none) |
| `"Gantt"` | Gantt | Timeline |
| `"SPLOM"` | SPLOM | (none) |
| `"Oncoprint"` | Oncoprint | (none) |
| `"Venn"` | Venn | (built-in) |
| `"Treemap"` | Treemap | (built-in) |
| `"Dumbbell"` | Dumbbell | (built-in) |
| `"Stacked"` | Stacked | (built-in) |

### Standalone Meta Chart Types

These have their own `graphType` values:

| Config Value | Type | Key Config |
|---|---|---|
| `"Bullet"` | Bullet (standalone) | `rangeStack`, `bulletTargetVarName`, `rangeColors` |
| `"Waterfall"` | Waterfall (standalone) | `waterfallType`, range colors |

\* Note: `bar_skill.md` also covers the Bullet style using `barType: 'lollipopBullet'`, but the dedicated `"Bullet"` graphType offers additional features like `rangeStack` and `bulletTargetVarName`.

## Sub-Skill Specializations

When a user requests a specific chart type, consult the corresponding sub-skill file for detailed examples, prompt-to-config mappings, and specialized patterns:

| Chart Type | Sub-Skill File | Key Features |
|---|---|---|
| Area chart | `area_skill.md` | Single/multi-series, stacked, percentage, filtered data, long format |
| Bar chart | `bar_skill.md` | Single/multi-series, horizontal, grouped, decorative lines, overlays, citation, workflow animation, plot-by-variable |
| Heatmap | `heatmap_skill.md` | Clustering, color spectra, cell markers, dendrograms, overlays |
| Line chart | `line_skill.md` | Vertical/horizontal, spline lines, error areas, pattern decorations, segregated panels |
| Box plot | `boxplot_skill.md` | Vertical/horizontal, notched, single whiskers, segregated, mean markers, custom median, jitter, colored/shaped boxes |
| Violin plot | `violin_skill.md` | Boxplot type with `showViolinBoxplot: True`, multiple scaling methods, notched boxes, mean markers |
| Scatter plot | `scatter_skill.md` | (See density_skill.md for histogram overlays) |
| Network | `network_skill.md` | Force-directed layout, node coloring by metadata, edge weights, Barnes-Hut simulation |
| Tree | `tree_skill.md` | Hierarchical data, collapsible nodes, circular/bracket layouts, metadata coloring |
| Sankey | `sankey_skill.md` | (See Stacked for flow visualization) |
| Radar | `radar_skill.md` | Line/area/bar/dot/stacked rings, half-circle (180°), rotation control, metadata overlays |
| Dot plot | `dotplot_skill.md` | Binned data, error bars, jitter, stacked layouts, overlays, metadata color/shape encoding |
| Bullet | `bullet_skill.md` | Range stacking, target markers, progress bars, custom themes, data value labels |
| Chord | `chord_skill.md` | Circular type with `circularType: 'chord'`, color highlighting, rotation, arc control |
| Contour | `contour_skill.md` | Heatmap/ScatterBubble2D with contour levels, filled contours, normal/advanced rendering |
| Correlation | `correlation_skill.md` | Sample/variable axes, circle correlation, anchor legends, matrix visualization |
| Density | `density_skill.md` | Scatter2D with histogram/density overlays, count-based statistics, distribution visualization |
| Dumbbell | `dumbbell_skill.md` | Comparing two values, sorting, highlighting, data labels, custom themes |
| Histogram | `histogram_skill.md` | Scatter2D with configurable bins (5/10/20), stacked/staggered layouts, filled paths, citations |
| Lollipop | `lollipop_skill.md` | Standard lollipop and bullet variants, size encoding, data value labels, range coloring |
| Map | `map_skill.md` | Choropleth coloring, zoom control, albers projection, metadata coloring, size encoding, pie decorations, workflow animation |
| Pie | `pie_skill.md` | Multiple layouts, segment labels, separation, precision control, solid/3D types, grid overlays |
| Stacked | `stacked_skill.md` | Vertical/horizontal, grouping, treemap layouts, segregation, gradient fills |
| Sunburst | `sunburst_skill.md` | Circular type with `circularType: 'sunburst'`, hierarchical data, rotation control, metadata coloring |
| Streamgraph | `streamgraph_skill.md` | Stream bandwidth control, mirror/ridge rendering, Loess fits, metadata coloring |
| Treemap | `treemap_skill.md` | Hierarchical rectangles, metadata coloring, annotation markers, ISO3/continent grouping |
| Venn | `venn_skill.md` | 2/3/4-set diagrams, intersection counts, custom legend labels |
| Waterfall | `waterfall_skill.md` | Traditional waterfall (positive/negative cumulative), bar-based clinical trials, tumor shrinkage, NEJM colors, metadata overlays |

**Workflow:** When the user requests a specific chart type, load the corresponding sub-skill to access specialized code examples, agent prompts, and prompt-to-config mappings tailored to that chart type.

## Plotly to CanvasXpress Conversion

### Plotly Trace Mapping

| Plotly Trace | CanvasXpress Config |
|---|---|
| `go.Bar()` | `"Bar"` |
| `go.Scatter(mode='markers')` | `"Scatter2D"` |
| `go.Scatter(mode='lines')` | `"Line"` |
| `go.Scatter(mode='area')` | `"Area"` |
| `go.Scatter3d()` | `"Scatter3D"` |
| `go.Box()` | `"Boxplot"` |
| `go.Violin()` | `"Violin"` |
| `go.Histogram()` | `"Histogram"` |
| `go.Pie()` | `"Pie"` |
| `go.Bubble()` | `"Bubble"` |
| `go.Heatmap()` | `"Heatmap"` |
| `go.Treemap()` | `"Treemap"` |
| `go.Sunburst()` | `"Sunburst"` |
| `go.Sankey()` | `"Sankey"` |
| `go.Parcoords()` | `"ParallelCoordinates"` |
| `go.Scattergeo()` | `"Map"` |

### Styling Mapping

| Plotly Style | CanvasXpress Config |
|---|---|
| `marker_color='red'` | `"objectColor": "rgb(255,0,0)"` |
| `opacity=0.5` | `"objectColorTransparency": 0.5` |
| `line_width=3` | `"lineThickness": 3` |
| `mode='markers'` | `"objectShape": "circle"` |
| `marker_size=10` | `"objectSize": 10` |
| `barmode='group'` | `"barGrouping": "group"` |
| `barmode='stack'` | `"barGrouping": "stack"` |
| `title_text='My Chart'` | `"title": "My Chart"` |
| `xaxis_title='X Axis'` | `"xAxisTitle": "X Axis"` |
| `yaxis_title='Y Axis'` | `"yAxisTitle": "Y Axis"` |
| `layout_colorway=['#1f77b4', ...]` | `"colors": ["rgb(31,119,180)", ...]` |

### Data Extraction Patterns

```python
# Single-trace bar chart
# go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30])
xyz = {
    "y": {"vars": ["Series1"], "smps": ["A", "B", "C"], "data": [[10, 20, 30]]}
}

# Multi-trace (each trace = one variable)
# fig.add_trace(go.Bar(x=['Jan', 'Feb'], y=[100, 200], name='Product A'))
# fig.add_trace(go.Bar(x=['Jan', 'Feb'], y=[150, 180], name='Product B'))
xyz = {
    "y": {"vars": ["Product A", "Product B"], "smps": ["Jan", "Feb"], "data": [[100, 200], [150, 180]]}
}

# Heatmap
# go.Heatmap(z=[[1, 2], [3, 4]], x=['A', 'B'], y=['X', 'Y'])
xyz = {
    "y": {"vars": ["X", "Y"], "smps": ["A", "B"], "data": [[1, 2], [3, 4]]}
}
```

## Matplotlib to CanvasXpress Conversion

### Matplotlib Plot Mapping

| Matplotlib | CanvasXpress Config |
|---|---|
| `plt.bar(x, y)` | `"Bar"` |
| `plt.barh(x, y)` | `"Bar"` + horizontal |
| `plt.plot(x, y)` | `"Line"` |
| `plt.plot(x, y, 'o')` | `"Scatter2D"` |
| `plt.scatter(x, y)` | `"Scatter2D"` |
| `plt.hist(data, bins=n)` | `"Histogram"` |
| `plt.boxplot(data)` | `"Boxplot"` |
| `plt.violinplot(data)` | `"Violin"` |
| `plt.pie(values, labels=...)` | `"Pie"` |
| `plt.imshow(data)` | `"Heatmap"` |
| `plt.pcolormesh(data)` | `"Heatmap"` |

### Complete Plotly Conversion Example

**Original Plotly code:**
```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30]))
fig.update_layout(title='My Chart', xaxis_title='Category', yaxis_title='Value')
```

**Converted to CanvasXpress:**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
    "y": {
        "vars": ["Series1"],
        "smps": ["A", "B", "C"],
        "data": [[10, 20, 30]]
    }
}

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Bar",
        "title": "My Chart",
        "xAxisTitle": "Category",
        "yAxisTitle": "Value"
    }
)
graph(cx)
```

### Complete Matplotlib Conversion Example

**Original Matplotlib code:**
```python
import matplotlib.pyplot as plt
plt.bar(['A', 'B', 'C'], [10, 20, 30])
plt.title('My Chart')
plt.xlabel('Category')
plt.ylabel('Value')
plt.show()
```

**Converted to CanvasXpress:**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
    "y": {
        "vars": ["Series1"],
        "smps": ["A", "B", "C"],
        "data": [[10, 20, 30]]
    }
}

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Bar",
        "title": "My Chart",
        "xAxisTitle": "Category",
        "yAxisTitle": "Value"
    }
)
graph(cx)
```

### Scatter Conversion Example

**Original Matplotlib code:**
```python
import matplotlib.pyplot as plt
plt.scatter([174, 161, 194], [65.6, 51.6, 80.7])
plt.xlabel('Height')
plt.ylabel('Weight')
```

**Converted to CanvasXpress:**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

xyz = {
    "y": {
        "vars": ["Weight"],
        "smps": ["S1", "S2", "S3"],
        "data": [[65.6], [51.6], [80.7]]
    },
    "x": {
        "Height": [174, 161, 194]
    }
}

cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "xAxisTitle": "Height",
        "yAxisTitle": "Weight"
    }
)
graph(cx)
```
