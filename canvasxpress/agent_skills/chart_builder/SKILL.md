---
name: chart_builder
description: Generate production-ready CanvasXpress Python charts. Supports creating charts from scratch with DataFrame or XYZ data, converting DataFrames to XYZ for metadata enhancement, translating Plotly or Matplotlib code to CanvasXpress equivalents, rendering to any framework (Jupyter, Dash, Shiny, Streamlit, Flask, browser), and exporting to images or JSON. Use when creating data visualizations, charts, or converting from Plotly/Matplotlib.
---

## Core API Reference

Primary imports the agent should always include:

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, show_in_browser, convert_to_image, convert_to_reproducible_json
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions, CXString, CXInt, CXFloat, CXBool, CXList, CXDict, CXRGBAColor, CXRGBColor
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
```

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

## Reference Files

Consult these reference files for detailed guidance on specific topics:

| Reference File | When to Load |
|---|---|
| `reference_chart_types.md` | Converting from Plotly/Matplotlib, looking up CXGraphTypeOptions, mapping chart types |
| `reference_platform.md` | Building Dash, Shiny, Streamlit, Flask, or Jupyter apps; adding event hooks; exporting charts |
| `reference_general.md` | DataFrame handling, XYZ conversion, production config patterns, data loading from URLs |

## Agent Interaction Pattern

### Decision Flow

1. **Identify chart type and data source**
2. **Ask clarifying questions:**
   - "What data source should I use? (existing DataFrame, XYZ dict, or sample data?)"
   - "Would you like me to convert your DataFrame to XYZ for manual metadata enhancement?"
   - "What rendering context? (Jupyter, Dash, Shiny, Streamlit, Flask, or browser)"
   - "Any specific styling preferences? (colors, theme, dimensions)"
3. **If XYZ conversion requested:**
   - Show the generated XYZ dict
   - Explain the x/y/z structure
   - Let user choose between XYZ dict or direct DataFrame
4. **Generate complete, copy-paste-ready Python code**
5. **Include framework-specific rendering instructions**

### Style Guidelines

- Use keyword arguments for config when possible (more readable)
- Set dimensions explicitly: `CanvasXpress(..., width=800, height=600)`
- Always include a descriptive title
- Use appropriate color schemes for the data type
- Set `showLegend=True` when there are multiple series/groups

## Known Limitations

1. **3D charts:** Plotly 3D and Matplotlib 3D require careful data reshaping; CanvasXpress Scatter3D is supported but complex geometries may not map perfectly
2. **Custom shapes:** Plotly `go.Scatter` with custom fill areas may not have exact CanvasXpress equivalents
3. **Dual axes:** Plotly's dual y-axis has limited CanvasXpress equivalent
4. **Faceted/colored plots:** Plotly `facet_row`/`facet_col` requires manual handling in CanvasXpress
5. **Time series with complex formatting:** Date formatting requires CanvasXpress `xAxisTickFormat`
6. **Word clouds:** Matplotlib has no native word cloud; requires external library
7. **Geographic maps:** CanvasXpress Map requires GeoJSON input, not direct lat/lon scatter
