---
name: canvasxpress_skill
description: Generate production-ready CanvasXpress Python charts. Supports creating charts from scratch with DataFrame or XYZ data, converting DataFrames to XYZ for metadata enhancement, translating Plotly or Matplotlib code to CanvasXpress equivalents, rendering to any framework (Jupyter, Dash, Shiny, Streamlit, Flask, browser), and exporting to images or JSON. Use when creating data visualizations, charts, or converting from Plotly/Matplotlib.
---

## Core API Reference

Primary imports the agent should always include:

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, show_in_browser, convert_to_image, convert_to_reproducible_json
from canvasxpress.config.type import CXGraphType, CXString, CXInt, CXFloat, CXBool, CXList, CXDict, CXRGBAColor, CXRGBColor
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
```

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

## Reference Files

Consult these reference files for detailed guidance on specific topics:

| Reference File | When to Load |
|---|---|
| `reference_conversion.md` | Converting from Plotly/Matplotlib, looking up CXGraphTypeOptions, mapping chart types |
| `reference_general.md` | DataFrame handling, XYZ conversion, production config patterns, data loading from URLs, advanced data wrangling, specialized formats (Venn, Network) |

## Cross-Chart & Interactive Sub-Skills

For advanced interactive features and multi-chart coordination, load these sub-skills:

| Capability | Sub-Skill | Key Topics |
|---|---|---|
| Broadcasting | `broadcast_skill.md` | Automatic broadcast, broadcast groups, filter broadcast, legend broadcast, page-level saved states, DOE dashboard |
| Highlighting | `highlighting_skill.md` | Declarative highlighting, ghost/focus modes, predicate-based highlighting, interactive selection, emphasis colors |
| Styling | `styling_skill.md` | Themes, color palettes, object styling, fonts, layout, dimensions, orientation, chart-type-specific styles |
| Events | `events_skill.md` | Event catalog (15 events), handler patterns, Shiny integration, dynamic listeners, post-render calls |

**Workflow:** When a user requests features covered by these sub-skills (multi-chart dashboards, highlighting storytelling, custom styling, or interactive events), load the corresponding sub-skill for detailed guidance.

## Framework Sub-Skills

For detailed framework-specific guidance, see the subskill files:

| Framework | Subskill File | Key Topics |
|---|---|---|
| Streamlit | `streamlit_skill.md` | Prerequisites, `graph(cx)`, caching, session state, architecture, API, databases, testing |
| Jupyter | `jupyter_skill.md` | Widgets, caching, annotations, events, multiple charts, `notebook_builder` skill integration |
| Dash | `dash_skill.md` | Callbacks, layouts, events, export, dcc components, auto-generated IDs |
| Shiny | `shiny_skill.md` | Reactive effects, sidebar, events, export, `@render.ui` decorator |
| Flask/FastAPI | `flask_skill.md` | Templates, HTMLResponse, API endpoints, `render_to_html_parts()`, unique chart IDs |

**Workflow:** When a user requests a specific framework, load the corresponding framework subskill for detailed guidance on prerequisites, rendering patterns, and best practices.

## Agent Interaction Pattern

### Decision Flow

1. **Identify chart type and data source**
2. **Load relevant reference/sub-skill:**
   - Chart type-specific? → Load corresponding chart sub-skill (bar_skill.md, heatmap_skill.md, etc.)
   - Plotly/Matplotlib conversion? → `reference_conversion.md`
   - DataFrame/data prep? → `reference_general.md`
   - Multi-chart coordination? → `broadcast_skill.md`
   - Highlighting/storytelling? → `highlighting_skill.md`
   - Custom styling? → `styling_skill.md`
   - Interactive events? → `events_skill.md`
3. **Ask clarifying questions:**
   - "What data source should I use? (existing DataFrame, XYZ dict, or sample data?)"
   - "Would you like me to convert your DataFrame to XYZ for manual metadata enhancement?"
   - "What rendering context? (Jupyter, Dash, Shiny, Streamlit, Flask, or browser)"
   - "Any specific styling preferences? (colors, theme, dimensions)"
   - "Do you need multi-chart coordination? (broadcasting, DOE dashboard)"
   - "Do you need highlighting/storytelling features? (declarative highlight, selection)"
4. **If XYZ conversion requested:**
   - Show the generated XYZ dict from `reference_general.md`
   - Explain the x/y/z structure
   - Let user choose between XYZ dict or direct DataFrame
5. **Generate complete, copy-paste-ready Python code**
6. **Include framework-specific rendering instructions**

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
