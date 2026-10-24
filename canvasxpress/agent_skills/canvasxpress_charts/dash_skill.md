# Dash Framework Subskill for CanvasXpress

## Prerequisites

**Ensure canvasxpress is installed with the dash extra before creating Dash apps:**

```bash
pip install canvasxpress[dash]
```

If you use `uv`:
```bash
uv add canvasxpress[dash]
```

No other package, JavaScript build, or `npm` step is required.

## Core CanvasXpress Dash Usage

### Imports

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
```

### How Charts Render in Dash

- `graph(cx)` returns a Dash component (`CXDashElement`). Place it directly in a layout, or return it from a
  callback, like any other Dash component.
- **Do not wrap it in `dcc.Graph`.** `dcc.Graph(figure=...)` is for Plotly figures and cannot display a
  CanvasXpress chart.
- The component's JavaScript ships inside the canvasxpress package and Dash serves it automatically. The
  CanvasXpress library itself loads from `CanvasXpress.js_library_url()` (the CanvasXpress CDN by default).
- The chart's `render_to` becomes its Dash component `id`. Dash requires IDs to be unique, so omit `render_to`
  (each chart gets a generated ID) or give every chart a distinct one.
- Charts render in the page's DOM, so charts with the same data broadcast to each other (see `broadcast_skill.md`).
- Set `width` and `height` on the `CanvasXpress` object, not on `graph()`.
- Use `app.run(...)`; `app.run_server` was removed in Dash 3.

The component can also be created explicitly, without `graph()`'s context detection:

```python
from canvasxpress.render.dash import CXElementFactory

chart_component = CXElementFactory.render(cx)
```

## Essential Dash Concepts for CanvasXpress

### 1. Minimal Dash App with CanvasXpress

```python
from dash import Dash, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)

cx = CanvasXpress(
    data={
        "y": {
            "vars": ["Sales"],
            "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
            "data": [[120, 150, 180, 200, 250]],
        }
    },
    config={"graphType": "Bar", "title": "Monthly Sales"},
    width=600,
    height=400,
)

app.layout = html.Div(
    [
        html.H1("Sales dashboard", style={"textAlign": "center"}),
        # graph(cx) returns a Dash component; place it directly in the layout
        html.Div(graph(cx), style={"display": "flex", "justifyContent": "center"}),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
```

**Key documentation:** [Dash Layout](https://dash.plotly.com/layout)

### 2. Dash App with Callbacks and Dynamic Charts

```python
import numpy as np
import pandas as pd
from dash import Dash, Input, Output, callback, dcc, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)

df = pd.DataFrame(
    np.random.randn(20, 5),
    columns=["A", "B", "C", "D", "E"],
    index=[f"S{i}" for i in range(20)],
)

app.layout = html.Div(
    [
        html.H1("Interactive dashboard"),
        dcc.Dropdown(
            id="chart_type",
            options=["Scatter2D", "Heatmap", "Bar", "Line", "Boxplot"],
            value="Scatter2D",
            style={"width": "300px"},
        ),
        html.Div(id="chart_container"),
    ]
)


@callback(Output("chart_container", "children"), Input("chart_type", "value"))
def update_chart(chart_type):
    cx = CanvasXpress(
        data=df,
        config={"graphType": chart_type, "title": f"Analysis: {chart_type}"},
        width=700,
        height=500,
    )
    # Return the component itself; Dash replaces the previous chart
    return graph(cx)


if __name__ == "__main__":
    app.run(debug=True)
```

**Key documentation:** [Dash Basic Callbacks](https://dash.plotly.com/basic-callbacks)

### 3. Dash App with Multiple, Coordinated Charts

```python
from dash import Dash, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)

people = ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"]

# Charts share the page's DOM, so charts with the same data broadcast to each
# other (see broadcast_skill.md).
scatter = CanvasXpress(
    render_to="body_chart",
    data={
        "y": {
            "vars": people,
            "smps": ["Height", "Weight"],
            "data": [
                [174, 65.6],
                [161, 51.6],
                [194, 80.7],
                [160, 49.2],
                [173, 55.2],
                [151, 48.7],
            ],
        }
    },
    config={"graphType": "Scatter2D", "xAxis": ["Height"], "yAxis": ["Weight"]},
    width=400,
    height=400,
)

bar = CanvasXpress(
    render_to="age_chart",
    data={"y": {"vars": ["Age"], "smps": people, "data": [[21, 22, 28, 19, 32, 35]]}},
    config={"graphType": "Bar", "title": "Age"},
    width=400,
    height=400,
)

app.layout = html.Div(
    [
        html.H1("Multi-chart dashboard"),
        html.Div([graph(scatter), graph(bar)], style={"display": "flex", "gap": "24px"}),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
```

### 4. Dash App with a Tabbed Interface

```python
import numpy as np
import pandas as pd
from dash import Dash, Input, Output, callback, dcc, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)

df1 = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])
df2 = pd.DataFrame(np.random.randn(10, 3), columns=["X", "Y", "Z"])

app.layout = html.Div(
    [
        html.H1("Tabbed dashboard"),
        dcc.Tabs(
            id="tabs",
            value="tab1",
            children=[
                dcc.Tab(label="Dataset 1", value="tab1"),
                dcc.Tab(label="Dataset 2", value="tab2"),
            ],
        ),
        html.Div(id="tab_content"),
    ]
)


@callback(Output("tab_content", "children"), Input("tabs", "value"))
def render_tab(tab_value):
    if tab_value == "tab1":
        cx = CanvasXpress(data=df1, config={"graphType": "Heatmap", "title": "Dataset 1"})
    else:
        cx = CanvasXpress(data=df2, config={"graphType": "Bar", "title": "Dataset 2"})
    return graph(cx)


if __name__ == "__main__":
    app.run(debug=True)
```

### 5. Dash App with Chart Events

CanvasXpress events run in the browser. They are not Dash callbacks and do not send data back to Python.

```python
from dash import Dash, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.plot import graph

app = Dash(__name__)

# Event scripts run in the browser with the CanvasXpress context variables
# o (the clicked object), e (the DOM event) and t (the chart).
events = CXEvents(
    CXEvent(
        id="click",
        script="t.showInfoSpan(e, 'Clicked ' + o.y.vars[0] + ', ' + o.y.smps[0]);",
    )
)

cx = CanvasXpress(
    data={
        "y": {
            "vars": ["V1", "V2"],
            "smps": ["S1", "S2", "S3"],
            "data": [[10, 20, 30], [15, 25, 35]],
        }
    },
    config={"graphType": "Bar", "title": "Click a bar"},
    events=events,
    width=600,
    height=400,
)

app.layout = html.Div([html.H1("Chart events"), graph(cx)])

if __name__ == "__main__":
    app.run(debug=True)
```

See the `canvasxpress_events` skill for event patterns. Event scripts run in the app page, so never build them
from user input.

### 6. Dash App with Data Export

```python
import json

from dash import Dash, Input, Output, callback, dcc, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json, graph

app = Dash(__name__)


def make_chart():
    return CanvasXpress(
        render_to="export_chart",
        data={"y": {"vars": ["V1"], "smps": ["S1", "S2", "S3"], "data": [[3, 1, 2]]}},
        config={"graphType": "Bar", "title": "Your chart"},
    )


app.layout = html.Div(
    [
        html.H1("Export dashboard"),
        graph(make_chart()),
        html.Button("Export JSON", id="export_btn", n_clicks=0),
        dcc.Download(id="download_json"),
    ]
)


@callback(
    Output("download_json", "data"),
    Input("export_btn", "n_clicks"),
    prevent_initial_call=True,
)
def export_json(n_clicks):
    reproducible = convert_to_reproducible_json(make_chart())
    content = reproducible if isinstance(reproducible, str) else json.dumps(reproducible)
    return dict(content=content, filename="chart.json")


if __name__ == "__main__":
    app.run(debug=True)
```

**Key documentation:** [dcc.Download](https://dash.plotly.com/dash-core-components/download)

## Key Takeaways

1. **Always install canvasxpress with the dash extra** (`pip install canvasxpress[dash]`); no other package or build is needed
2. **Use `graph(cx)`** to create the chart component, and place it directly in the layout or return it from a callback
3. **Never wrap charts in `dcc.Graph`**, which only displays Plotly figures
4. **Give each chart a unique `render_to`**, or omit it for a generated ID; it becomes the Dash component `id`
5. **Set `width` and `height` on `CanvasXpress`**, not on `graph()`
6. **Use Dash callbacks** to rebuild charts from user input; return `graph(cx)` as the output
7. **Charts with the same data broadcast** to each other because they share the page's DOM
8. **CanvasXpress events run in the browser**; they do not trigger Dash callbacks
9. **Export** with `convert_to_reproducible_json()` and `dcc.Download(dict(content=..., filename=...))`
10. **Run apps with `app.run()`**; `app.run_server` no longer exists
