---
title: "Platform Reference"
description: "CanvasXpress rendering for different frameworks (Jupyter, Dash, Shiny, Streamlit, Flask) with event hooks and integration templates."
---

# Platform Reference

## Rendering

The `graph(cx)` function from `canvasxpress.plot` auto-detects the environment and renders appropriately:

```python
from canvasxpress.plot import graph
graph(cx)  # Works in Jupyter, Dash, Shiny, Streamlit, Flask, CLI, browser
```

### Environment-Specific Notes

- **Jupyter**: Inline rendering with auto-detection
- **Dash**: Works in `dcc.Graph(figure=graph(cx))`
- **Shiny**: Works in `@render.ui` functions
- **Streamlit**: Works directly in Streamlit apps
- **Flask/FastAPI**: Use `render_to="unique_id"` for chart identification
- **CLI**: Opens in browser automatically

### Unique Chart IDs

For environments requiring unique identifiers (Jupyter, Flask, FastAPI), use `render_to`:

```python
# Named chart (Jupyter, Flask, FastAPI)
CanvasXpress(render_to="my_chart_id", ...)

# Anonymous chart (Dash, React-based)
CanvasXpress(render_to="", ...)
```

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

## Complete Code Templates

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

### Template 3: Dash integration

```python
from dash import Dash, html, dcc
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("My CanvasXpress Dashboard"),
    dcc.Graph(
        id="chart",
        figure=graph(CanvasXpress(render_to="", ...))
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### Template 4: Shiny for Python

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.markdown("My CanvasXpress Chart")
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
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.output_text_verbatim("selected_point")
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.point_selected)
    def show_selection():
        print(input.point_selected())

    @render.ui
    def chart_view():
        return graph(CanvasXpress(
            render_to="example",
            data=xyz_data,
            config={"graphType": "Scatter2D", "title": "Interactive Chart"},
            events=[
                CXEvent(
                    id="click",
                    script="Shiny.setInputValue('point_selected', o.y);"
                )
            ]
        ))

app = App(app_ui, server)
```

### Template 6: Streamlit integration

```python
import streamlit as st
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

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
            ["V1", "S1"]
        ]
    }
)
graph(cx)
```
