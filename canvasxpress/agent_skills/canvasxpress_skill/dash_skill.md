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

## Core CanvasXpress Dash Usage

### Imports

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
```

### Basic Graph Call in Dash

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["GeneA", "GeneB"], "smps": ["S1", "S2", "S3"], "data": [[10, 20, 30], [15, 25, 35]]}
    },
    config={"graphType": "Scatter2D", "title": "My Chart"}
)

# For Dash, use empty render_to for auto-generated IDs
cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D"},
    render_to=""
)
```

### Rendering CanvasXpress in Dash

```python
from dash import Dash, html, dcc
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Dash(__name__)

cx = CanvasXpress(
    data=data,
    config={"graphType": "Heatmap"},
    render_to=""
)

app.layout = html.Div([
    html.H1("My CanvasXpress Dashboard"),
    dcc.Graph(
        id="chart",
        figure=graph(cx)
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

## Essential Dash Concepts for CanvasXpress

### 1. Minimal Dash App with CanvasXpress

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Dash(__name__)

# Create chart
cx = CanvasXpress(
    data={
        "y": {
            "vars": ["Sales"],
            "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
            "data": [[120, 150, 180, 200, 250]]
        }
    },
    config={"graphType": "Bar", "title": "Monthly Sales"},
    render_to=""
)

app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(
        id="sales_chart",
        figure=graph(cx),
        style={'width': '80%', 'margin': 'auto'}
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 2. Dash App with Callbacks and Dynamic Charts

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
import numpy as np

app = Dash(__name__)

# Generate data
df = pd.DataFrame(
    np.random.randn(100, 5),
    columns=['A', 'B', 'C', 'D', 'E'],
    index=[f'S{i}' for i in range(100)]
)

# State management
app.layout = html.Div([
    html.H1("Interactive Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Chart Type:"),
        dcc.Dropdown(
            id="chart_type",
            options=['Scatter2D', 'Heatmap', 'Bar', 'Line', 'Boxplot'],
            value='Scatter2D',
            style={'width': '300px'}
        )
    ], style={'padding': '20px', 'textAlign': 'center'}),
    
    html.Div(id="chart_container")
])

@callback(
    Output("chart_container", "children"),
    Input("chart_type", "value")
)
def update_chart(chart_type):
    cx = CanvasXpress(
        data=df,
        config={
            "graphType": chart_type,
            "title": f"Analysis: {chart_type}",
            "showLegend": True
        },
        render_to=""
    )
    return dcc.Graph(figure=graph(cx))

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 3. Dash App with Multiple Charts

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Dash(__name__)

# Generate sample data
df1 = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])
df2 = pd.DataFrame(np.random.randn(50, 3), columns=['X', 'Y', 'Z'])

app.layout = html.Div([
    html.H1("Multi-Chart Dashboard"),
    
    html.Div([
        dcc.Graph(
            id="chart1",
            figure=graph(CanvasXpress(
                data=df1,
                config={"graphType": "Scatter2D", "title": "Dataset 1"},
                render_to=""
            )),
            style={'width': '48%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id="chart2",
            figure=graph(CanvasXpress(
                data=df2,
                config={"graphType": "Heatmap", "title": "Dataset 2"},
                render_to=""
            )),
            style={'width': '48%', 'display': 'inline-block'}
        )
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 4. Dash App with Layout Components

```python
from dash import Dash, html, dcc
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame(np.random.randn(30, 4), columns=['A', 'B', 'C', 'D'])

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Analytics Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
        dcc.Dropdown(
            id="filter",
            options=['All', 'Group A', 'Group B'],
            value='All'
        )
    ], style={'padding': '20px', 'backgroundColor': '#f0f0f0'}),
    
    # Main content in columns
    html.Div([
        html.Div([
            dcc.Graph(
                id="main_chart",
                figure=graph(CanvasXpress(
                    data=df,
                    config={"graphType": "Scatter2D", "title": "Main Analysis"},
                    render_to=""
                ))
            )
        ], style={'width': '65%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.H3("Summary"),
            html.P("Total Records: 30"),
            html.P("Variables: 4")
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'})
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 5. Dash App with Tabbed Interface

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Dash(__name__)

df1 = pd.DataFrame(np.random.randn(30, 3), columns=['A', 'B', 'C'])
df2 = pd.DataFrame(np.random.randn(30, 3), columns=['X', 'Y', 'Z'])

app.layout = html.Div([
    html.H1("Tabbed Dashboard"),
    
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label="Dataset 1", value="tab1"),
        dcc.Tab(label="Dataset 2", value="tab2"),
    ]),
    
    dcc.TabChildren(id="tab_content")
])

@callback(
    Output("tab_content", "children"),
    Input("tabs", "value")
)
def render_tab(tab_value):
    if tab_value == "tab1":
        return dcc.Graph(
            figure=graph(CanvasXpress(
                data=df1,
                config={"graphType": "Heatmap", "title": "Dataset 1"},
                render_to=""
            ))
        )
    else:
        return dcc.Graph(
            figure=graph(CanvasXpress(
                data=df2,
                config={"graphType": "Bar", "title": "Dataset 2"},
                render_to=""
            ))
        )

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 6. Dash App with Event Handling

```python
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])

app.layout = html.Div([
    html.H1("Interactive Chart with Callbacks"),
    dcc.Graph(
        id="chart",
        figure=graph(CanvasXpress(
            data=df,
            config={"graphType": "Scatter2D", "title": "Click Points"},
            render_to="",
            events=CXEvents(
                CXEvent(
                    id="click",
                    script="DashClient.call('plot_click', {var: o.y.vars[0], smp: o.y.smps[0]});"
                )
            )
        ))
    ),
    html.Div(id="selection_info")
])

@callback(
    Output("selection_info", "children"),
    Input({"type": "plot_click", "index": dash.ALL}, "data")
)
def update_info(click_data):
    if not any(click_data):
        return "Click on a data point to see details"
    return f"Selected: {click_data}"

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 7. Dash App with Data Export

```python
from dash import Dash, html, dcc, callback, Input, Output
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])

app.layout = html.Div([
    html.H1("Export Dashboard"),
    
    dcc.Graph(
        id="chart",
        figure=graph(CanvasXpress(
            data=df,
            config={"graphType": "Scatter2D", "title": "Your Chart"},
            render_to=""
        ))
    ),
    
    html.Button("Export JSON", id="export_btn", n_clicks=0),
    dcc.Download(id="download-json")
])

@callback(
    Output("download-json", "data"),
    Input("export_btn", "n_clicks"),
    prevent_initial_call=True
)
def export_json(n_clicks):
    cx = CanvasXpress(
        data=df,
        config={"graphType": "Scatter2D", "title": "Exported Chart"}
    )
    return convert_to_reproducible_json(cx)

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 8. Complete Dash Application Template

```python
"""
CanvasXpress Dash Application Template
"""
from dash import Dash, html, dcc, Input, Output, callback
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Dash(__name__)

# Initialize data
@callback(
    Output("chart-placeholder", "children"),
    Input("dropdown", "value"),
    prevent_initial_call=False
)
def update_chart(chart_type):
    cx = CanvasXpress(
        data=df,
        config={
            "graphType": chart_type,
            "title": f"{chart_type} Analysis",
            "showLegend": True
        },
        render_to=""
    )
    return dcc.Graph(figure=graph(cx))

# App layout
app.layout = html.Div([
    html.Header([
        html.H1("CanvasXpress Dash Dashboard", className="title"),
        html.P("Interactive Data Visualization", className="subtitle")
    ]),
    
    html.Div([
        dcc.Dropdown(
            id="dropdown",
            options=["Scatter2D", "Heatmap", "Bar", "Line"],
            value="Scatter2D"
        )
    ], className="controls"),
    
    html.Div(id="chart-placeholder", className="chart-container")
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

## Key Takeaways

1. **Always install canvasxpress with the dash extra** (`pip install canvasxpress[dash]`) before building Dash apps
2. **Use `graph(cx)`** for rendering CanvasXpress charts in Dash
3. **Use `render_to=""`** (empty string) for auto-generated IDs in Dash
4. **Wrap charts in `dcc.Graph(figure=graph(cx))`** for proper rendering
5. **Use Dash callbacks** for interactive chart updates based on user input
6. **Leverage Dash layout components** (`dcc.Tabs`, `dcc.Dropdown`, `dcc.Slider`) for controls
7. **CanvasXpress events can trigger Dash callbacks** using `DashClient.call()`
8. **Export functionality** with `convert_to_reproducible_json()` and `dcc.Download`
9. **Use HTML styling** for professional-looking dashboards
10. **Multiple charts** can coexist using `dcc.Graph` with different IDs
