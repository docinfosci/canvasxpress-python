---
title: "Chart Types Reference"
description: "CanvasXpress chart type mappings, Plotly/Matplotlib conversions, and sub-skill catalog."
---

# Chart Types Reference

## Chart Type Catalog

| User Request | CXGraphTypeOptions |
|---|---|
| Bar chart | `CXGraphTypeOptions.Bar` |
| Line chart | `CXGraphTypeOptions.Line` |
| Area chart | `CXGraphTypeOptions.Area` |
| Scatter plot | `CXGraphTypeOptions.Scatter2D` |
| 3D Scatter | `CXGraphTypeOptions.Scatter3D` |
| Heatmap | `CXGraphTypeOptions.Heatmap` |
| Box plot | `CXGraphTypeOptions.Boxplot` |
| Violin plot | `CXGraphTypeOptions.Violin` |
| Histogram | `CXGraphTypeOptions.Histogram` |
| Pie chart | `CXGraphTypeOptions.Pie` |
| Donut chart | `CXGraphTypeOptions.Donnut` |
| Bubble chart | `CXGraphTypeOptions.Bubble` |
| Network | `CXGraphTypeOptions.Network` |
| Tree | `CXGraphTypeOptions.Tree` |
| Sankey | `CXGraphTypeOptions.Sankey` |
| Dot plot | `CXGraphTypeOptions.Dotplot` |
| Stacked bar | `CXGraphTypeOptions.Stacked` |
| Timeline/Gantt | `CXGraphTypeOptions.Gantt` |
| Radar/Spoke | `CXGraphTypeOptions.Radar` |
| Venn diagram | `CXGraphTypeOptions.Venn` |
| SPLOM | `CXGraphTypeOptions.SPLOM` |
| TCGA oncoprint | `CXGraphTypeOptions.Oncoprint` |
| Treemap | `CXGraphTypeOptions.Treemap` |
| Sunburst | `CXGraphTypeOptions.Sunburst` |
| Chord | `CXGraphTypeOptions.Circular` (with `circularType: 'chord'`) |
| Contour | `CXGraphTypeOptions.Heatmap` or `CXGraphTypeOptions.ScatterBubble2D` |
| Correlation | `CXGraphTypeOptions.Heatmap` or `CXGraphTypeOptions.Scatter2D` |
| Map | `CXGraphTypeOptions.Map` |
| Waterfall | `CXGraphTypeOptions.Bar` or `CXGraphTypeOptions.Waterfall` |
| Lollipop | `CXGraphTypeOptions.Bar` (with `barType: 'lollipop'`) |
| Bullet | `CXGraphTypeOptions.Bar` (with `barType: 'lollipopBullet'`) |
| Density | `CXGraphTypeOptions.Scatter2D` (with histogram overlays) |

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

### Trace-to-Chart Type Mapping

| Plotly Trace | CanvasXpress Type |
|---|---|
| `go.Bar()` | `CXGraphTypeOptions.Bar` |
| `go.Scatter(mode='markers')` | `CXGraphTypeOptions.Scatter2D` |
| `go.Scatter(mode='lines')` | `CXGraphTypeOptions.Line` |
| `go.Scatter(mode='area')` | `CXGraphTypeOptions.Area` |
| `go.Scatter3d()` | `CXGraphTypeOptions.Scatter3D` |
| `go.Box()` | `CXGraphTypeOptions.Boxplot` |
| `go.Violin()` | `CXGraphTypeOptions.Violin` |
| `go.Histogram()` | `CXGraphTypeOptions.Histogram` |
| `go.Pie()` | `CXGraphTypeOptions.Pie` |
| `go.Bubble()` | `CXGraphTypeOptions.Bubble` |
| `go.Heatmap()` | `CXGraphTypeOptions.Heatmap` |
| `go.Treemap()` | `CXGraphTypeOptions.Treemap` |
| `go.Sunburst()` | `CXGraphTypeOptions.Sunburst` |
| `go.Sankey()` | `CXGraphTypeOptions.Sankey` |
| `go.Parcoords()` | `CXGraphTypeOptions.ParallelCoordinates` |
| `go.Scattergeo()` | `CXGraphTypeOptions.Map` |

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

### Plot-to-Chart Type Mapping

| Matplotlib | CanvasXpress |
|---|---|
| `plt.bar(x, y)` | `CXGraphTypeOptions.Bar` |
| `plt.barh(x, y)` | `CXGraphTypeOptions.Bar` + horizontal |
| `plt.plot(x, y)` | `CXGraphTypeOptions.Line` |
| `plt.plot(x, y, 'o')` | `CXGraphTypeOptions.Scatter2D` |
| `plt.scatter(x, y)` | `CXGraphTypeOptions.Scatter2D` |
| `plt.hist(data, bins=n)` | `CXGraphTypeOptions.Histogram` |
| `plt.boxplot(data)` | `CXGraphTypeOptions.Boxplot` |
| `plt.violinplot(data)` | `CXGraphTypeOptions.Violin` |
| `plt.pie(values, labels=...)` | `CXGraphTypeOptions.Pie` |
| `plt.imshow(data)` | `CXGraphTypeOptions.Heatmap` |
| `plt.pcolormesh(data)` | `CXGraphTypeOptions.Heatmap` |
