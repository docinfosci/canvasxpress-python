---
title: "Platform Reference"
description: "CanvasXpress rendering for different frameworks (Jupyter, Dash, Shiny, Streamlit, Flask) with event hooks and integration templates."
---

# Platform Reference

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

### Template 5: Shiny with Interactive Events

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

### Template 6: Streamlit integration

```python
import streamlit as st
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# Create chart
cx = CanvasXpress(
    data={
        "y": {
            "vars": ["Sales"],
            "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
            "data": [[120, 150, 180, 200, 250]]
        }
    },
    config={
        "graphType": "Bar",
        "title": "Monthly Sales",
        "xAxisTitle": "Month",
        "yAxisTitle": "Sales ($)"
    }
)

# Render in Streamlit
graph(cx)
```

### Template 7: Image export

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_image

cx = CanvasXpress(...)
png_bytes = convert_to_image(cx, type="png")
with open("chart.png", "wb") as f:
    f.write(png_bytes)
```

### Template 8: Browser popup (CLI usage)

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import show_in_browser

cx = CanvasXpress(...)
show_in_browser(cx)
```

### Template 9: Pre-selected Data Points

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
