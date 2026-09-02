---
name: canvasxpress
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

## Data Handling Patterns

### Pattern 1: Existing DataFrame in context

```python
cx = CanvasXpress(
    data=df,
    sample_annotation=annot_df,
    variable_annotation=var_df,
    config={"graphType": "Heatmap"}
)
graph(cx)
```

### Pattern 2: XYZ dict from user

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["A", "B"], "smps": ["S1", "S2", "S3"], "data": [[1,2,3], [4,5,6]]},
        "x": {"Group": ["Control", "Control", "Treatment"]},
        "z": {"A": {"Pathway": "P1"}, "B": {"Pathway": "P2"}}
    },
    config={"graphType": "Scatter2D"}
)
graph(cx)
```

### Pattern 3: Fabricated sample data (when user has no data)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["GeneA", "GeneB", "GeneC"],
    index=[f"Smp{i}" for i in range(1, 51)]
)
```

### Pattern 4: URL/CSV loading

```python
import requests, io, pandas as pd
df = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))
```

### Pattern 5: Loading data and annotations from URLs

```python
import requests, io, pandas as pd

# Load main data
data_url = "https://www.canvasxpress.org/data/r/cX-generic-dat.txt"
data_df = pd.read_csv(
    io.StringIO(requests.get(data_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

# Load sample annotations
sample_annot_url = "https://www.canvasxpress.org/data/r/cX-generic-smp.txt"
sample_annot_df = pd.read_csv(
    io.StringIO(requests.get(sample_annot_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

# Load variable annotations
variable_annot_url = "https://www.canvasxpress.org/data/r/cX-generic-var.txt"
variable_annot_df = pd.read_csv(
    io.StringIO(requests.get(variable_annot_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

cx = CanvasXpress(
    data=data_df,
    sample_annotation=sample_annot_df,
    variable_annotation=variable_annot_df,
    config={"graphType": "Dotplot"}
)
graph(cx)
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

## Production-Ready Config Patterns

Every generated chart should include production-quality configuration:

```python
config = {
    "graphType": "Bar",
    "title": "Chart Title",
    "subtitle": "Optional subtitle",
    "xAxisTitle": "X Axis Label",
    "yAxisTitle": "Y Axis Label",
    "colorScheme": "CanvasXpress",
    "theme": "CanvasXpress",
    "showLegend": True,
    "showLegendBorder": True,
    "graphOrientation": "vertical",
    "background": "rgb(255,255,255)",
}
```

Common additions by chart type:

```python
# Scatter-specific
"objectShape": "circle",
"objectColor": "rgb(69,117,180)",
"regressionLine": True,

# Heatmap-specific
"heatMapping": "color",
"sortSmpByTree": True,
"sortVarByTree": True,

# Bar/Stacked-specific
"objectBorderColor": "rgb(0,0,0)",
"objectBorderThickness": 1,

# Network-specific
"nodeLabelSize": 10,
"ringGraphWeight": [25, 25, 25, 25],

# Sample overlays (for advanced metadata visualization)
"smpOverlayProperties": {
    "Factor1": {
        "type": "Default",
        "color": "rgb(10,176,219)",
        "spectrum": ["rgb(69,117,180)", "rgb(145,191,219)"],
        "scheme": "CanvasXpress",
        "showLegend": True
    }
},

# Line chart specific
"lineType": "spline",
"llmHeader": [["V1", "V2", "V3", "V4"]],
```

## Framework-Specific Rendering

| Framework | Code Pattern |
|---|---|
| Auto-detect (default) | `graph(cx)` |
| Jupyter/IPython | `graph(cx)` or `CXNoteBook(cx).render()` |
| Dash | `CXElementFactory().render(cx)` returns Dash component |
| Shiny for Python | `CXShinyWidget(cx)` returned from reactive function |
| Streamlit | `streamlit.plot(cx)` |
| Flask/Django | `html_parts = cx.render_to_html_parts()` + Jinja template |
| Browser/CLI | `show_in_browser(cx)` |
| Image export | `convert_to_image(cx, type="png")` |
| JSON export | `convert_to_reproducible_json(cx)` |

## Event Hook Patterns

Basic events use CanvasXpress JavaScript context variables:
- `o` - the data provided to the CanvasXpress chart
- `e` - the JavaScript object for the triggering event
- `t` - the full JavaScript CanvasXpress object (including configuration)

```python
events = CXEvents(
    CXEvent(
        id="click",
        script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
    ),
    CXEvent(
        id="mousemove",
        script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
    )
)
```

### Shiny Integration Events

For Shiny apps, use `Shiny.setInputValue()` to trigger backend reactions:

```python
CXEvent(
    id="click",
    script="Shiny.setInputValue('point_selected', o.y);"
)
```

Then react in the Shiny server:

```python
@reactive.effect
@reactive.event(input.point_selected)
def show_selection():
    print(input.point_selected())
```

## Complete Code Templates by Framework

### Template 1: Minimal with auto-rendering

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

cx = CanvasXpress(
    data={
        "y": {"vars": ["Gene1"], "smps": ["Smp1", "Smp2", "Smp3"], "data": [[10, 35, 88]]}
    },
    config={"graphType": "Bar", "title": "My Chart"}
)
graph(cx)
```

**Note:** The `render_to` parameter provides a unique identifier for the chart. For environments that require unique IDs (Jupyter, Flask), use a descriptive name. For React-based environments (Dash), use an empty string for anonymous charts with auto-generated IDs.

```python
# Named chart (Jupyter, Flask)
CanvasXpress(render_to="my_chart_id", ...)

# Anonymous chart (Dash, React-based)
CanvasXpress(render_to="", ...)
```

### Template 2: DataFrame with sample annotation

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

df = pd.DataFrame(...)
annot = pd.DataFrame(...)

cx = CanvasXpress(
    data=df,
    sample_annotation=annot,
    config={
        "graphType": "Heatmap",
        "title": "Heatmap with Annotations",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["Factor1"]
    }
)
graph(cx)
```

### Template 3: Full Dash integration

```python
from dash import Dash, html, dcc
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("My CanvasXpress Dashboard"),
    dcc.Graph(
        id="chart",
        figure=graph(CanvasXpress(...))
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### Template 4: Full Shiny for Python

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.shiny import output_canvasxpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.row(output_canvasxpress("chart_view"))
)

def server(input, output, session):
    @render.ui
    def chart_view():
        return graph(CanvasXpress(...))

app = App(app_ui, server)
```

### Template 7: Shiny with Interactive Events

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.render.shiny import output_canvasxpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.row(output_canvasxpress("chart_view")),
    ui.output_text_verbatim("selected_point")
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.point_selected)
    def show_selection():
        # React to chart point selection
        print(input.point_selected())

    @render.ui
    @reactive.event(house_data.cell_selection)
    def chart_view():
        chart = CanvasXpress(
            render_to="example",
            data=xyz_data,
            config={
                "graphType": "Scatter2D",
                "title": "Interactive Chart"
            },
            events=[
                CXEvent(
                    id="click",
                    script="Shiny.setInputValue('point_selected', o.y);"
                )
            ]
        )
        return graph(chart)

app = App(app_ui, server)
```

### Template 8: Pre-selected Data Points

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# XYZ data
xyz = {
    "y": {
        "vars": ["V1", "V2", "V3"],
        "smps": ["S1", "S2", "S3"],
        "data": [[10, 20, 30], [15, 25, 35], [20, 30, 40]]
    }
}

cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "title": "Chart with Pre-selected Point",
        "selectedDataPoints": [
            ["V1", "S1"]  # Pre-select variable V1, sample S1
        ]
    }
)
graph(cx)
```

### Template 5: Image export

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_image

cx = CanvasXpress(...)
png_bytes = convert_to_image(cx, type="png")
with open("chart.png", "wb") as f:
    f.write(png_bytes)
```

### Template 6: Browser popup (CLI usage)

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import show_in_browser

cx = CanvasXpress(...)
show_in_browser(cx)
```

## DataFrame-to-XYZ Conversion

### Core Conversion Function

```python
def dataframe_to_xyz(
    df: pd.DataFrame,
    sample_annotation: pd.DataFrame = None,
    variable_annotation: pd.DataFrame = None,
) -> dict:
    """
    Converts a DataFrame into a CanvasXpress XYZ dict.
    
    Parameters:
        df: Main data DataFrame (index=vars, columns=smps)
        sample_annotation: Optional annotation DataFrame (per-sample metadata -> x)
        variable_annotation: Optional annotation DataFrame (per-variable metadata -> z)
    
    Returns:
        dict with structure: {
            "y": {"data": [...], "vars": [...], "smps": [...]},
            "x": {...},  # optional
            "z": {...}   # optional
        }
    """
    xyz = {
        "y": {
            "data": df.values.tolist(),
            "vars": df.index.tolist(),
            "smps": df.columns.tolist()
        }
    }
    
    if sample_annotation is not None:
        xyz["x"] = _convert_annotation_to_x(sample_annotation, xyz["y"]["smps"])
    
    if variable_annotation is not None:
        xyz["z"] = _convert_annotation_to_z(variable_annotation, xyz["y"]["vars"])
    
    return xyz
```

### User Workflow: Inspect -> Modify -> Use

```python
# Step 1: Convert DataFrame to XYZ
xyz = dataframe_to_xyz(df, sample_annotation=annot_df)

# Step 2: Inspect the structure
print(f"Samples: {xyz['y']['smps']}")
print(f"Variables: {xyz['y']['vars']}")
print(f"X annotations: {list(xyz['x'].keys())}")

# Step 3: Enhance with additional metadata
xyz["x"]["NewFactor"] = ["Group1", "Group1", "Group2", "Group2"]
xyz["x"]["Condition"] = ["A", "B", "A", "B"]

# Step 4: Use in CanvasXpress
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Heatmap",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["NewFactor", "Condition"]
    }
)
graph(cx)
```

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

## Example Interactions

### Example 1: Create a simple bar chart

**User:** "Create a bar chart showing sales data"

**Agent:** Provides complete code:
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# Sales data
data = {
    "y": {
        "vars": ["Sales"],
        "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
        "data": [[120, 150, 180, 200, 250]]
    }
}

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Bar",
        "title": "Monthly Sales",
        "xAxisTitle": "Month",
        "yAxisTitle": "Sales ($)",
        "showLegend": False
    }
)
graph(cx)
```

### Example 2: Convert existing Plotly code

**User:** "Convert this Plotly code to CanvasXpress"
```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30]))
```

**Agent:** Provides converted code:
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
        "title": "My Chart"
    }
)
graph(cx)
```

### Example 3: DataFrame with annotations

**User:** "I have a pandas DataFrame with gene expression data. Create a heatmap with sample annotations."

**Agent:** Provides complete code:
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

# Sample expression data
df = pd.DataFrame(
    {'GeneA': [1.2, 3.4, 0.5], 'GeneB': [2.1, 1.8, 4.2], 'GeneC': [0.3, 2.7, 1.9]},
    index=['Sample1', 'Sample2', 'Sample3']
)

# Sample annotations
annot = pd.DataFrame({
    'Treatment': ['Control', 'Treatment', 'Control'],
    'Batch': ['A', 'A', 'B']
}, index=['Sample1', 'Sample2', 'Sample3'])

cx = CanvasXpress(
    data=df,
    sample_annotation=annot,
    config={
        "graphType": "Heatmap",
        "title": "Gene Expression Heatmap",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["Treatment", "Batch"]
    }
)
graph(cx)
```
