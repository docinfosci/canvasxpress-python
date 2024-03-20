# CanvasXpress for Python

<a href="https://www.canvasxpress.org">
<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/images/hexagon.png" align="left" width="175" style="vertical-align:middle;margin:10px 10px"> 
</a>
<br>

[***CanvasXpress***](https://www.canvasxpress.org) was developed as the core visualization component for bioinformatics
and systems biology analysis at Bristol-Myers Squibb. It supports a large number
of [visualizations ](https://www.canvasxpress.org/examples.html)
to display scientific and non-scientific data. ***CanvasXpress*** also includes a simple and unobtrusive
[user interface](https://www.canvasxpress.org/docs/interface.html) to explore complex data sets, a sophisticated and
unique mechanism to keep track of all user customization for
[Reproducible Research ](https://www.canvasxpress.org/docs/audit.html) purposes, as well as an 'out of the box'
broadcasting capability to synchronize selected data points across all ***CanvasXpress*** plots in a page. Data can be
easily sorted, grouped, transposed, transformed or clustered dynamically. The fully customizable mouse events as well as
the zooming, panning and drag-and-drop capabilities are features that make this library unique in its class.

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/images/sample_graphs.png" align="center" width="726"></a>

***CanvasXpress*** can be used for native Python integration for the following environments:

- [Shiny for Python](https://shiny.posit.co/py/)
- [Streamlit](https://streamlit.io/)
- [Plotly Dash](https://dash.plotly.com/)
- [Jupyter](https://jupyter.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Django](https://www.djangoproject.com/)

The RStudio IDE Viewer is also used when running code chunks in Jupyter, Quarto, and RMD Python code chunks.

This ***CanvasXpress*** Python package is maintained by [Dr. Todd C. Brett](https://github.com/docinfosci), with support 
from [Aggregate Genius Inc.](https://www.aggregate-genius.com), in cooperation with Dr. Isaac Neuhaus and the 
***CanvasXpress*** team.

## Project Status

[![Release](https://img.shields.io/pypi/v/canvasxpress.svg)](https://pypi.org/project/canvasxpress)
[![Compatibility](https://img.shields.io/pypi/pyversions/canvasxpress.svg)](https://pypi.org/project/canvasxpress)
[![Implementations](https://img.shields.io/pypi/implementation/canvasxpress.svg)](https://pypi.org/project/canvasxpress)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/canvasxpress)](https://pypi.org/project/canvasxpress)
[![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/main.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=main)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=main)
[![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/develop)](https://github.com/docinfosci/canvasxpress-python)

## Documentation, Installation, and Usage

### Documentation

Documentation is maintained at [CanvasXpress.org](https://www.canvasxpress.org) and LinkedIn:

- [Introduction to CanvasXpress for Python](https://www.linkedin.com/pulse/introducing-canvasxpress-python-todd-brett-hew0f/?trackingId=G8kTE2QyRH%2BrcVSzxJc8Hg%3D%3D)

### Installation

CanvasXpress for Python can be installed using _pip_:

The essential CanvasXpress package, for use with the CLI or flask and similar environments, can be installed using:

```terminal
pip install canvasxpress
```

or

```terminal
pip install "canvasxpress[core]"
```

In addition to _core_, the following additional targets can be used:

- _jupyter_ - installs additional packages to support rendering in Jupyter, Quarto, and IPython documents
- _dash_ - installs additional packages to support rendering in Plotly Dash applications
- _streamlit_ - installs additional packages to support rendering in Snowflake Streamlit applications
- _shiny_ - installs additional packages to support rendering in Posit Shiny for Python applications
- _rstudio_ - installs additional packages to support rendering in the Posit RStudio IDE Viewer, plus includes the same packages for jupyter and shiny
- _all_ - installs all additional packages to support rendering in any supported document or application

### Drawing Charts

The `CanvasXpress` object defines what a chart should contain and how it should be formatted, but rendering the chart
is performed by the functions `graph()` and `show_in_browser()`.  

To use `graph()` import it from `canvasxpress.plot` and then call it by passing a `CanvasXpress` object. For example, a
Quarto, RMD, or Jupyter Notebook code chunk could be:

```python
from random import random

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

graph(
    CanvasXpress(
        data={
            "y": {
                "data": [
                    [random() % 100 for i in range(20)]
                ],
                "vars": ["A"],
            }
        },
        config={
            "background": "rgb(255,255,255)",
            "colorScheme": "CanvasXpress",
            "graphOrientation": "vertical",
            "graphType": "Area",
            "objectBorderColor": False,
            "plotBox": False,
            "plotBoxColor": "rgb(204,204,204)",
            "showLegend": False,
            "showLegendBorder": True,
            "smpLabelRotate": 90,
            "smpTitle": "time",
            "xAxis": ["A"],
            "xAxisTickRightShow": False,
            "yAxisTickTopShow": False
        },
        width=609,
        height=609
    )
)
```

Some application frameworks, such as _Shiny for Python_ and _Plotly Dash_, expect an object to be rendered to the 
framework as part of the reactive flow.  In these contexts, the `graph()` function creates an appropriate object
and returns it.  That value can be assigned to a variable to be returned at a later point in the code, or be 
immediately returned.  See the Shiny for Python and Dash examples for specific usage.

`show_in_browser()` is similar to `graph()` except that it opens a browser window on the local system and displays the 
chart.  It's used to facilitate learning and debugging.

`graph()` does a good job of determining the runtime context to choose how the chart should be rendered, but in the 
case installed packages or runtime configurations confuse the function an environment variable can be set to override
how `graph()` performs the rendering.  Set `CANVASXPRESS_TARGET_CONTEXT` to be one of these values as appropriate for
this situation (and don't forget to pip install the necessary package support):

- rstudio
- shiny
- jupyter
- dash
- streamlit
- browser

For example:

```python
from os import environ
environ["CANVASXPRESS_TARGET_CONTEXT"] = "jupyter"
```

or via a shell (_bash_ example provided):

```shell
export CANVASXPRESS_TARGET_CONTEXT="jupyter"
```

### Default and Pinned CanvasXpress JavaScript Editions

CanvasXpress for Python generates JavaScript that assumes use of the latest available edition of CanvasXpress for
JavaScript, but it can be set to use a specific edition.

Review this site for available versions:
https://cdnjs.com/libraries/canvasXpress

The desired version is expressed as a `str`.  Prior to generating a CanvasXpress chart use the following code to set 
the edition that shall be used:

```python
from canvasxpress.canvas import CanvasXpress
CanvasXpress.set_cdn_edition("48.3")  # Or whatever available version is desired.
```

To use the default edition once again during the runtime session set the value to `None`.

This is the best way to assure a specific chart behavior for production application releases; however, once set any
new JavaScript edition features or fixes will not be available until the code is removed or a different version is set.

### Customizing Charts

Generally speaking, a `CanvasXpress` object accepts the following parameters:

#### render_to

`render_to` is a `str` value that identifies the chart when rendered into HTML.  JavaScript functions can use this ID
to access the chart and perform CanvasXpress operations within the browser.  Omitting `render_to` or setting it to 
`None` will make the `CanvasXpress` object assume an anonymous mode in which a new GUID will be generated each time 
`graph()` is called.  If the chart will not be maniluated using JavaScript in the browser it is fine for charts to be anonymous.

__NOTE:__ React environments regularly destroy and rebuild objects as the page is updated.  In these environments it is
possible for the timing of object destruction and JavaScript execution to cause a crash.  The best defense is to either 
use anonymous mode, or if an ID must be known then a unique identifier should be set each time `graph()` is called.  In
this manner an ID for a chart in the middle of being recreated is never referenced.  For example:

```python
chart = CanvasXpress(...)
chart.render_to = str(guid4()).replace("-", "_")
return graph(chart)
```

Plotly's Dash framework uses React, and Dash applications should consider using only anonymous charts or assigning
unique values as the ID similar to the above code.  Shiny for Python does not seem to suffer from this challenge.

#### data

`data` sets the chart's data and metadata.  This is an involved topic, and the [introductory article](https://www.linkedin.com/pulse/introducing-canvasxpress-python-todd-brett-hew0f/?trackingId=G8kTE2QyRH%2BrcVSzxJc8Hg%3D%3D)
is an excellent read to understand how data should be shaped.  In general, data will be a `dict`, Web URL, or `str`.

Data dict example:

```python
data_for_use_in_chart = {
    "y": {
        "data": [
            [random() % 100 for i in range(20)]
        ],
        "vars": ["A"],
    }
}
```

Data URL example:

```python
data_for_use_in_chart = "https://corgis-edu.github.io/corgis/datasets/csv/state_demographics/state_demographics.csv"
```

Data text (CSV) example:

```python
data_for_use_in_chart = """
"State","Population.Population Percent Change","Population.2014 Population"
"Connecticut","-10.2","3605944"
"Delaware","8.4","989948"
"""
```

#### config

`config` describes the chart's formatting.  It is a `dict` in which properties are specified and assigned values. All
of the values must be compliant with Python's `json.dumps()` function.  For example:

```python
config={
    "background": "rgb(255,255,255)",
    "colorScheme": "CanvasXpress",
    "graphOrientation": "vertical",
    "graphType": "Area",
    "objectBorderColor": False,
    "plotBox": False,
    "plotBoxColor": "rgb(204,204,204)",
    "showLegend": False,
    "showLegendBorder": True,
    "smpLabelRotate": 90,
    "smpTitle": "time",
    "xAxis": ["A"],
    "xAxisTickRightShow": False,
    "yAxisTickTopShow": False
},
```

#### width and height

`width` and `height` specify the chart's dimensions as pixels.  If ommitted the CanvasXpress edition active for the 
browser will assign default values, such as 500px by 500px.

#### Javascript Events

CanvasXpress provides support for Javascript events via hook functions that are called when events occur, such as mouse 
movement or clicks. These events are supported via the canvasxpress.js sub-package. `CXEvent` objects hold the 
Javascript instructions for Web events.  An example event for graph clicks with popup information is:

```python
from canvasxpress.js.function import CXEvent

CXEvent(
    id="click",
    script="""
    var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
    t.showInfoSpan(e, s);
    """
)
```

The general JavaScript template of a CanvasXpress Javascript hook function is:

```javascript
function (o, e, t) {
    // script logic goes here
};
```

`CXEvent` objects can be provided as a single object or as a list.  Here's an example of an event the provides 
additional information about chart data upon a user click:

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.js.function import CXEvent

graph(
    CanvasXpress(
        render_to="example_chart",
        data={
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]]
            }
        },
        config={
            "graphOrientation": "vertical",
            "graphType": "Bar",
            "showLegend": False,
            "smpLabelRotate": 90,
            "smpTitle": "Samples",
            "theme": "CanvasXpress",
            "title": "Bar Graph Title",
            "xAxisTitle": "Value"
        },
        events=[
            CXEvent(
                id="click",
                script="""
                var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
                t.showInfoSpan(e, s);
                """
            ),
        ]
    )
)
```

## Application, NoteBook, and Console Examples

### Rendering Charts in the RStudio IDE Viewer Pane 

The RStudio IDE's Viewer panel is now supported for rendering interactive charts in the Viewer!  When the `graph()`
function is called it detects that RStudio is running and renders the chart in the Viewer instead of a document, 
such as for Quarto code chunks.  However, if the document is a Quarto or RMD file and the appropriate HTML (etc.)
generation is performed then the CanvasXpress charts will be embedded in the generated output file as normal.

### A Basic Python Script / Console Example

Charts can be defined in scripts or a console session and then displayed using the default browser, assuming that a
graphical browser with Javascript support is available on the host system.  To do so use the `show_in_browser()`
function instead of graph()`.

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import show_in_browser

if __name__ == "__main__":
    # Define a CX bar chart with some basic data
    chart: CanvasXpress = CanvasXpress(
        data={
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]]
            }
        },
        config={
            "graphType": "Bar"
        }
    )

    # Display the chart in its own Web page
    show_in_browser(chart)
```

Upon running the example the following chart will be displayed on systems such as MacOS X, Windows, and Linux with
graphical systems:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/flask_bar_chart_basic.png" align="center" width="600"></a>

### A Shiny for Python Example

[Shiny for Python](https://shiny.posit.co/py/) is a new dashboard framework inspired by the highly successful Shiny for
R framework produced by Posit (formerly RStudio). This example shows how to create a basic Shiny for Python application
using a CanvasXpress Shiny element.

A basic Shiny for Python app provides a means by which:

1. A local development server can be started
1. A function can respond to input or draw an initial UI

First install Shiny for Python and CanvasXpress for Python:

```terminal
pip install shiny
pip install canvasxpress[shiny]
```

Then create a demo file, such as `app.py`, and insert:

```python
from random import random

from shiny import App, ui, render, reactive

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app_ui = ui.page_fluid(
    ui.row(
        ui.input_slider(
            "points_desired",
            "Points",
            min=0,
            max=100,
            value=0,
        ),
    ),
    ui.row(
        ui.output_ui("chart_view"),
    )
)


def server(input, output, session):
    @render.ui
    @reactive.event(input.points_desired)
    def chart_view():
        return graph(
            CanvasXpress(
                data={
                    "y": {
                        "data": [
                            [random() % 100 for i in range(input.points_desired())]
                        ],
                        "vars": ["A"],
                    }
                },
                config={
                    "background": "rgb(255,255,255)",
                    "colorScheme": "CanvasXpress",
                    "graphOrientation": "vertical",
                    "graphType": "Area",
                    "objectBorderColor": False,
                    "plotBox": False,
                    "plotBoxColor": "rgb(204,204,204)",
                    "showLegend": False,
                    "showLegendBorder": True,
                    "smpLabelRotate": 90,
                    "smpTitle": "time",
                    "xAxis": ["A"],
                    "xAxisTickRightShow": False,
                    "yAxisTickTopShow": False
                },
                width=500,
                height=500
            )
        )


app = App(app_ui, server)
```

#### Run the App and View the Page

On the command line, execute:

```terminal
shiny run --reload --launch-browser app.py
```

And output similar to the following will be provided:

```terminal
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Browsing to `http://localhost:8000/` will result in a page with a CanvasXpress chart, which is being hosted by the Shiny
for Python framework:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/shiny_chart_example.png" align="center" width="600"></a>

Congratulations!  You have created a Shiny for Python CanvasXpress app!

### A Streamlit Example

[Streamlit](https://streamlit.io) is a popular dashboard framework that is simplified compared to Dash and Shiny, but
just as powerful in terms of reactivity and extensions. This example shows how to create a basic Streamlit application
using a CanvasXpress Streamlit element.

A basic Streamlit app provides a means by which:

1. A local development server can be started
1. A function can respond to a URL

First install Streamlit and CanvasXpress for Python:

```terminal
pip install streamlit
pip install canvasxpress[streamlit]
```

Then create a demo file, such as `app.py`, and insert:

```python
import random

import streamlit as st

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# A basic bar chart.  It's anonymous, so no render_to.  Data is added during the draw phase.
chord_chart = CanvasXpress(
    config={
        "graphOrientation": "vertical",
        "plotBox": True,
        "showLegend": False,
        "smpLabelRotate": 90,
        "smpTitle": "Samples",
        "theme": "CanvasXpress",
        "title": "Bar Graph Title",
        "xAxis": ["V1"],
        "xAxisTitle": "Value",
        "graphType": "Bar"
    },
    width=500,
    height=500
)

# Write the UI to the browser
# This code will be re-executed with each click of the button

# Name the theme
st.title('CanvasXpress in Streamlit!')

# Some columns to organize the button and chart
column1, column2 = st.columns(2)

# A column with our data generator button
column1.write(
    # This has no associated action, so by default it triggers a redraw of the UI.
    st.button("Generate New Data")
)

# Another column with the chart displayed
# With each redraw generate new random values
chord_chart.data = {
    "y": {
        "vars": ["V1"],
        "smps": ["S1", "S2", "S3"],
        "data": [
            [
                random.randint(100, 10000),
                random.randint(100, 10000),
                random.randint(100, 10000),
            ]
        ]
    }
}
column2.write(
    # This plots the CanvasXpress chart into the UI.
    graph(chord_chart)
)
```

#### Run the App and View the Page

On the command line, execute:

```terminal
streamlit run app.py
```

And output similar to the following will be provided:

```terminal
Running on http://localhost:8501/ (Press CTRL+C to quit)
```

Browsing to `http://localhost:8501/` will result in a page with a CanvasXpress chart, which is being hosted by the
Streamlit framework:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/streamlit_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created a Streamlit CanvasXpress app!

### A Dash Example

[Plotly Dash](https://dash.plotly.com/) is a popular dashboard framework similar to Shiny for Python or R. Dash
applications are Web pages with widgets and elements facilitating the interactive presentation of information. This
example shows how to create a basic Dash application using a CanvasXpress Dash element.

#### Create a Basic Dash App

A basic Dash app provides a means by which:

1. A local development server can be started
1. A function can respond to a URL

First install Dash and CanvasXpress for Python:

```terminal
pip install dash
pip install canvasxpress[dash]
```

Then create a demo file, such as `app.py`, and insert:

```python
from random import random

from dash import Dash, html

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

g_app = Dash(__name__)

colors = {
    "background": "#111111",
    "text": "rgb(127,219,255)",
}

# Application
g_app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Hello Dash",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.H2(
            children=(
                "An Example of the Advanced CanvasXpress and CXDashElementFactory"
                " Classes for Plotting a CanvasXpress Chart"
            ),
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            id="chart-container",
            children=[
                html.Div(
                    id="cx-container",
                    style={"textAlign": "center"},
                    children=graph(
                        CanvasXpress(
                            data={
                                "y": {
                                    "data": [
                                        [random() % 100 for i in range(5)]
                                    ],
                                    "vars": ["A"],
                                }
                            },
                            config={
                                "background": "rgb(255,255,255)",
                                "colorScheme": "CanvasXpress",
                                "graphOrientation": "vertical",
                                "graphType": "Area",
                                "objectBorderColor": False,
                                "plotBox": False,
                                "plotBoxColor": "rgb(204,204,204)",
                                "showLegend": False,
                                "showLegendBorder": True,
                                "smpLabelRotate": 90,
                                "smpTitle": "time",
                                "xAxis": ["A"],
                                "xAxisTickRightShow": False,
                                "yAxisTickTopShow": False
                            },
                            width=500,
                            height=500
                        )
                    ),
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    g_app.run_server(debug=True)
```

#### Run the App and View the Page

On the command line, execute:

```terminal
python3 app.py
```

And output similar to the following will be provided:

```terminal
Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```

Browsing to `http://127.0.0.1:8050/` will result in a page with a CanvasXpress chart, which is being hosted by the Dash
framework:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/dash_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created a Plotly Dash CanvasXpress app!

### A Flask Example

[Flask](https://palletsprojects.com/p/flask/) is a popular lean Web development framework for Python based applications.
Flask applications can serve Web pages, RESTful APIs, and similar backend service concepts. This example shows how to
create a basic Flask application that provides a basic Web page with a CanvasXpress chart composed using Python in the
backend.

The concepts in this example equally apply to other frameworks that can serve Web pages, such as Django and Tornado.

#### Create a Basic Flask App

A basic Flask app provides a means by which:

1. A local development server can be started
1. A function can respond to a URL

First install Flask and CanvasXpress for Python:

```terminal
pip install -U Flask canvasxpress
```

Then create a demo file, such as `app.py`, and insert:

```python
# save this as app.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def canvasxpress_example():
    return "Hello!"
```

On the command line, execute:

```terminal
flask run
```

And output similar to the following will be provided:

```terminal
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Browsing to `http://127.0.0.1:5000/` will result in a page with the text
*Hello!*.

#### Add a Chart

CanvasXpress for Python can be used to define a chart with various attributes and then generate the necessary HTML and
Javascript for proper display in the browser.

Add a `templates` directory to the same location as the `app.py` file, and inside add a file
called `canvasxpress_example.html`. Inside the file add:

```html

<html>
<head>
    <meta charset="UTF-8">
    <title>Flask CanvasXpress Example</title>

    <!-- 2. Include the CanvasXpress library -->
    <link
            href='https://www.canvasxpress.org/dist/canvasXpress.css'
            rel='stylesheet'
            type='text/css'
    />
    <script
            src='https://www.canvasxpress.org/dist/canvasXpress.min.js'
            type='text/javascript'>
    </script>

    <!-- 3. Include script to initialize object -->
    <script type="text/javascript">
        onReady(function () {
            {
                {
                    canvas_source | safe
                }
            }
        })
    </script>

</head>
<body>

<!-- 1. DOM element where the visualization will be displayed -->
{{canvas_element|safe}}

</body>
</html>
```

The HTML file, which uses [Jinja syntax](https://palletsprojects.com/p/jinja/) achieves three things:

1. Provides a location for a `<div>` element that marks where the chart will be placed.
1. References the CanvasXpress CSS and JS files needed to illustrate and operate the charts.
1. Provides a location for the Javascript that will replace the chart `<div>` with a working element on page load.

Going back to our Flask app, we can add a basic chart definition with some data to our example function:

```python
from flask import Flask, render_template
from canvasxpress.canvas import CanvasXpress

app = Flask(__name__)


@app.route('/')
def canvasxpress_example():
    # Define a CX bar chart with some basic data
    chart: CanvasXpress = CanvasXpress(
        data={
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]]
            }
        },
        config={
            "graphType": "Bar"
        }
    )

    # Get the HTML parts for use in our Web page:
    html_parts: dict = chart.render_to_html_parts()

    # Return a Web page based on canvasxpress_example.html and our HTML parts
    return render_template(
        "canvasxpress_example.html",
        canvas_element=html_parts["cx_canvas"],
        canvas_source=html_parts["cx_js"]
    )
```

#### Run the App and View the Page

Rerun the flask app on the command line and browse to the indicated IP and URL. A page similar to the following will be
displayed:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/flask_bar_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created a Flask CanvasXpress app!
