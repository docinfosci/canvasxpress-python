# Shiny for Python Subskill for CanvasXpress

## Prerequisites

**Ensure canvasxpress is installed with the shiny extra before creating Shiny apps:**

```bash
pip install canvasxpress[shiny]
```

If you use `uv`:
```bash
uv add canvasxpress[shiny]
```

## Core CanvasXpress Shiny Usage

### Imports

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
```

### Basic Graph Call in Shiny

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["GeneA", "GeneB"], "smps": ["S1", "S2", "S3"], "data": [[10, 20, 30], [15, 25, 35]]}
    },
    config={"graphType": "Scatter2D", "title": "My Chart"}
)

# For Shiny, use a unique render_to identifier
cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D"},
    render_to="chart_id"
)
```

### Rendering CanvasXpress in Shiny

```python
from shiny import App, ui, render
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.row(
        ui.output_ui("chart_view")
    )
)

def server(input, output, session):
    @render.ui
    def chart_view():
        return graph(CanvasXpress(
            render_to="chart_id",
            data=data,
            config={"graphType": "Heatmap"}
        ))

app = App(app_ui, server)
```

## Essential Shiny Concepts for CanvasXpress

### 1. Minimal Shiny App with CanvasXpress

```python
from shiny import App, ui, render
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.h1("My CanvasXpress Chart"),
    ui.row(
        ui.output_ui("chart")
    )
)

def server(input, output, session):
    @render.ui
    def chart():
        cx = CanvasXpress(
            render_to="chart",
            data={
                "y": {
                    "vars": ["Sales"],
                    "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
                    "data": [[120, 150, 180, 200, 250]]
                }
            },
            config={"graphType": "Bar", "title": "Monthly Sales"}
        )
        return graph(cx)

app = App(app_ui, server)
```

### 2. Shiny App with Sidebar Controls

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app_ui = ui.page_fluid(
    ui.sidebar(
        ui.input_select("chart_type", "Chart Type", 
                       choices=["Scatter2D", "Heatmap", "Bar", "Line"]),
        ui.input_checkbox("show_legend", "Show Legend", True),
        width="300px"
    ),
    ui.output_ui("chart")
)

def server(input, output, session):
    @render.ui
    @reactive.effect
    @reactive.event(input.chart_type)
    def chart():
        config = {
            "graphType": input.chart_type(),
            "title": f"Analysis: {input.chart_type()}",
            "showLegend": input.show_legend()
        }
        cx = CanvasXpress(
            render_to="chart",
            data=df,
            config=config
        )
        return graph(cx)

app = App(app_ui, server)
```

### 3. Shiny App with Reactive Chart Updates

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
import numpy as np

app_ui = ui.page_fluid(
    ui.h1("Reactive Dashboard"),
    ui.sidebar(
        ui.input_slider("n_points", "Number of Points", 10, 100, 50),
        ui.input_select("graph_type", "Graph Type", 
                       ["Scatter2D", "Heatmap", "Boxplot"]),
        ui.input_color("color", "Color", "#4285f4")
    ),
    ui.output_ui("chart")
)

def server(input, output, session):
    @render.ui
    @reactive.effect
    @reactive.event(input.n_points, input.graph_type)
    def chart():
        # Generate reactive data
        data = pd.DataFrame(
            np.random.randn(input.n_points(), 3),
            columns=['A', 'B', 'C']
        )
        
        config = {
            "graphType": input.graph_type(),
            "title": f"Reactive Chart ({input.n_points()} points)",
            "objectColor": input.color()
        }
        
        cx = CanvasXpress(
            render_to="chart",
            data=data,
            config=config
        )
        return graph(cx)

app = App(app_ui, server)
```

### 4. Shiny App with Tabbed Interface

```python
from shiny import App, ui, render
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app_ui = ui.page_fluid(
    ui.h1("Tabbed Dashboard"),
    ui.navset_tab(
        ui.nav_panel("Scatter", ui.output_ui("scatter_chart")),
        ui.nav_panel("Heatmap", ui.output_ui("heatmap_chart")),
        ui.nav_panel("Bar", ui.output_ui("bar_chart"))
    )
)

def server(input, output, session):
    @render.ui
    def scatter_chart():
        return graph(CanvasXpress(
            render_to="scatter",
            data=df1,
            config={"graphType": "Scatter2D", "title": "Scatter Plot"}
        ))
    
    @render.ui
    def heatmap_chart():
        return graph(CanvasXpress(
            render_to="heatmap",
            data=df2,
            config={"graphType": "Heatmap", "title": "Heatmap"}
        ))
    
    @render.ui
    def bar_chart():
        return graph(CanvasXpress(
            render_to="bar",
            data=df3,
            config={"graphType": "Bar", "title": "Bar Chart"}
        ))

app = App(app_ui, server)
```

### 5. Shiny App with Interactive Events

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
import pandas as pd

app_ui = ui.page_fluid(
    ui.h1("Interactive Chart"),
    ui.output_ui("chart"),
    ui.output_text_verbatim("selection")
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.point_selected)
    def show_selection():
        selection = input.point_selected()
        print(f"Selected: {selection}")
    
    @render.ui
    def chart():
        events = CXEvents(
            CXEvent(
                id="click",
                script="Shiny.setInputValue('point_selected', o.y);"
            )
        )
        
        cx = CanvasXpress(
            render_to="chart",
            data=df,
            config={"graphType": "Scatter2D", "title": "Click Points"},
            events=events
        )
        return graph(cx)
    
    @render.text
    def selection():
        sel = input.point_selected()
        if sel:
            return f"Selected: var={sel.get('vars')}, smp={sel.get('smps')}"
        return "Click on a data point to see details"

app = App(app_ui, server)
```

### 6. Shiny App with Pre-selected Data Points

```python
from shiny import App, ui, render
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app_ui = ui.page_fluid(
    ui.h1("Chart with Pre-selected Points"),
    ui.output_ui("chart")
)

def server(input, output, session):
    @render.ui
    def chart():
        xyz = {
            "y": {
                "vars": ["V1", "V2", "V3"],
                "smps": ["S1", "S2", "S3"],
                "data": [[10, 20, 30], [15, 25, 35], [20, 30, 40]]
            }
        }
        
        cx = CanvasXpress(
            render_to="chart",
            data=xyz,
            config={
                "graphType": "Scatter2D",
                "title": "Pre-selected Points",
                "selectedDataPoints": [["V1", "S1"]]
            }
        )
        return graph(cx)

app = App(app_ui, server)
```

### 7. Shiny App with Data Export

```python
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
import pandas as pd

app_ui = ui.page_fluid(
    ui.h1("Export Dashboard"),
    ui.output_ui("chart"),
    ui.download_button("download_json", "Download JSON")
)

def server(input, output, session):
    @render.ui
    def chart():
        cx = CanvasXpress(
            render_to="chart",
            data=df,
            config={"graphType": "Scatter2D", "title": "Your Chart"}
        )
        return graph(cx)
    
    @reactive.calc
    def json_data():
        cx = CanvasXpress(
            data=df,
            config={"graphType": "Scatter2D"}
        )
        return convert_to_reproducible_json(cx)
    
    @ui.render
    @reactive.event(input.download_json)
    def download_json():
        return ui.download_file(json_data())

app = App(app_ui, server)
```

### 8. Complete Shiny Application Template

```python
"""
CanvasXpress Shiny Application Template
"""
from shiny import App, ui, render, reactive
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

# App UI
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Dashboard",
            ui.h1("Analytics Dashboard"),
            ui.sidebar(
                ui.input_select("chart_type", "Chart Type",
                              ["Scatter2D", "Heatmap", "Bar", "Line"]),
                ui.input_checkbox("annotations", "Show Annotations", False)
            ),
            ui.output_ui("main_chart")
        ),
        ui.nav_panel("Data",
            ui.h1("Data Explorer"),
            ui.output_data_frame("data_table")
        )
    )
)

# Server function
def server(input, output, session):
    @render.ui
    @reactive.effect
    @reactive.event(input.chart_type)
    def main_chart():
        config = {
            "graphType": input.chart_type(),
            "title": f"{input.chart_type()} Analysis",
            "showLegend": True
        }
        
        if input.annotations():
            config["showSmpOverlaysLegend"] = True
            config["smpOverlays"] = ["Treatment", "Batch"]
        
        cx = CanvasXpress(
            render_to="main_chart",
            data=df,
            sample_annotation=annot,
            config=config
        )
        return graph(cx)
    
    @render.data_frame
    def data_table():
        return df

# Create app
app = App(app_ui, server)
```

## Key Takeaways

1. **Always install canvasxpress with the shiny extra** (`pip install canvasxpress[shiny]`) before building Shiny apps
2. **Use `graph(cx)`** for rendering CanvasXpress charts in Shiny
3. **Use unique `render_to` identifiers** for each chart in Shiny
4. **Use `@render.ui` decorator** to render CanvasXpress charts in Shiny
5. **Use `@reactive.effect` and `@reactive.event`** for reactive updates
6. **Use Shiny sidebar** (`ui.sidebar`) for controls and filters
7. **CanvasXpress events trigger Shiny inputs** using `Shiny.setInputValue()`
8. **React to chart interactions** using `@reactive.event(input.event_name)`
9. **Export with `convert_to_reproducible_json()`** and `ui.download_button()`
10. **Leverage Shiny's nav panels** for multi-page applications
