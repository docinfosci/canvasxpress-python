---
name: events
description: CanvasXpress event handling including the complete event catalog, event handler patterns using JavaScript context variables (o, e, t), Shiny integration, dynamic event listeners, and post-render function calls. Use when creating interactive charts with custom click/hover/select behaviors.
---

# Events & Interactivity

## Event Handler Signature

Every event handler receives three arguments via JavaScript context variables:

```python
# script uses: o (data object), e (DOM event), t (CanvasXpress instance)
# Keep in mind:
# - o contains chart-specific data (e.g., o.y.vars[0], o.y.smps[0])
# - e has native DOM properties (e.clientX, e.clientY, e.ctrlKey)
# - t is the full CanvasXpress API (t.showInfoSpan(), t.zoom(), etc.)
```

## Complete Event Catalog

| Event | Description |
|---|---|
| `click` | Data element clicked |
| `clicklegend` | Legend item clicked |
| `contextmenu` | Right-click (prevent default for custom menu) |
| `dblclick` | Double-click |
| `drag` | During drag operation |
| `enddragnode` | Network node drag finished |
| `enddraw` | Rendering complete |
| `motion` | Motion complete (motion charts only) |
| `mousemove` | Mouse moving over chart elements |
| `mouseout` | Mouse left chart elements |
| `mouseover` | Mouse entered a data element |
| `mouseup` | Mouse button released |
| `remote` | Chart updated by remote source |
| `select` | Data points selected |
| `wheel` | Mouse wheel over chart |

## Basic Event Examples

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

cx = CanvasXpress(data=data, config={"graphType": "Bar"}, events=events)
graph(cx)
```

## Event Handler Organization Pattern

For complex applications, group handlers into a dedicated structure:

```python
events = CXEvents(
    CXEvent(id="click", script="/* handler code */"),
    CXEvent(id="mousemove", script="/* handler code */"),
    CXEvent(id="mouseout", script="/* handler code */"),
    CXEvent(id="dblclick", script="/* handler code */"),
)
```

## Dynamic Event Listeners (Post-Render)

Add or remove events after the chart is created:

```python
# After getting the chart instance:
# cx_instance = graph(cx)

# Add events dynamically
# cx_instance.addEventListener('click', handler_function)
# cx_instance.removeEventListener('click', handler_function)
```

## Shiny Integration Events

Trigger backend reactions from chart interactions:

```python
CXEvent(
    id="click",
    script="Shiny.setInputValue('point_selected', o.y);"
)
```

Then react in the Shiny server:

```python
from shiny import App, ui, render, reactive

@reactive.effect
@reactive.event(input.point_selected)
def show_selection():
    print(input.point_selected())
```

## Complete Shiny with Interactive Events Template

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
        print(input.point_selected())

    @render.ui
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

## Post-Render Function Calls

Apply transformations after initial render:

```python
cx = CanvasXpress(
    data=data,
    config={"graphType": "Bar"},
    after_render=[
        ["createRegression", [True, "Hip"]],   # Add regression
        ["pivotX", ["Gender"]],                 # Pivot by metadata
        ["createDOE", []]                       # Create DOE dashboard
    ]
)
graph(cx)
```

## Programmatic Chart Control

Access chart instance methods from event handlers:

```python
CXEvent(
    id="click",
    script="""
        // t is the CanvasXpress instance
        t.zoom();              // Zoom to fit
        t.filterSamples();     // Open filter panel
        // t.destroy();        // Destroy chart
    """
)
```

## Complete Events Template

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
from canvasxpress.plot import graph

events = CXEvents(
    CXEvent(
        id="click",
        script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
    ),
    CXEvent(
        id="mousemove",
        script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
    ),
    CXEvent(
        id="select",
        script="console.log('Selection made:', o);"
    )
)

cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D", "title": "Interactive Chart"},
    events=events
)
graph(cx)
```
