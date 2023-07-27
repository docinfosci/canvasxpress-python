# CanvasXpress Python Library

<a href="https://www.canvasxpress.org">
<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/images/hexagon.png" align="left" width="175" style="vertical-align:middle;margin:10px 10px"> 
</a>

## About CanvasXpress for Python

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

***CanvasXpress*** can be now be used within Python for native integration into IPython and Web environments, such as:

- [Streamlit](https://streamlit.io/)
- [Plotly Dash](https://dash.plotly.com/)
- [Jupyter](https://jupyter.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Django](https://www.djangoproject.com/)

Complete examples using the ***CanvasXpress*** library including the mouse events, zooming, and broadcasting
capabilities are included in this package. This
***CanvasXpress*** Python package was created by Dr. Todd C. Brett, with support from
[Aggregate Genius Inc.](https://www.aggregate-genius.com), in cooperation with the
***CanvasXpress*** team.

The maintainer of the Python edition of this package is [Dr. Todd C. Brett](https://github.com/docinfosci).

### Project Status

| Topic | Status | 
|---|---|
| **Release** |[![Release](https://img.shields.io/pypi/v/canvasxpress.svg)](https://pypi.org/project/canvasxpress) |
| **Python** | [![Compatibility](https://img.shields.io/pypi/pyversions/canvasxpress.svg)](https://pypi.org/project/canvasxpress) |
| **Edition** | [![Implementations](https://img.shields.io/pypi/implementation/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | 
| **Popularity** | [![PyPI - Downloads](https://img.shields.io/pypi/dm/canvasxpress)](https://pypi.org/project/canvasxpress) |
| **Build** | [![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/main.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=main) |
| **Coverage** | [![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=main)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=main) | 
| **Code** | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/main)](https://github.com/docinfosci/canvasxpress-python) |

<!-- End Badges -->

### Enhancements

_Streamlit Dashboards are now supported!_ 🥳 🎉

Streamlit is a popular dashboard framework that is generally simpler to use than Plotly Dash or Shiny for Python, but
just as powerful in terms of extensions and reactivity.

_Jupyter Notebook exports are now supported!_

Rendering in Notebooks has been available since Day 1, but now exporting saved notebooks to PDF, HTML, and other formats
is supported!  The HTML export includes _live_ CanvasXpress charts, which makes this an excellent option for
distributing rendered materials on the Web or with colleagues unfamiliar with notebook functionality.

_Pinned CanvasXpress versions are now supported!_

To facilitate productin and reproducible research environments, the edition of CanvasXpress to be used can now be set.
For example, version `34.9`. By default the latest available edition of CanvasXpress will be used.

A complete list of enhancements by release date is available at the
[CanvasXpress for Python Status Page](https://canvasxpress-python.readthedocs.io/en/latest/status/).

### Known Issues

None

### Roadmap

This package is actively maintained and developed. Our focus for 2023 is:

#### Immediate Focus

* Updated and detailed documentation and working examples of all Python functionality
* Shiny for Python support

#### General Focus

* Integraton with dashboard frameworks for easier applet creation
* Continued alignment with the CanvasXpress Javascript library
* Continued stability and security, if/as needed

## Getting Started

### Documentation

The [documentation site](https://canvasxpress-python.readthedocs.io/en/latest/)
contains complete [examples](https://canvasxpress-python.readthedocs.io/en/latest/examples/)
and [API documentation](https://canvasxpress-python.readthedocs.io/en/latest/api/). There is also a wealth of additional
information, including full Javascript API documentation,
at [https://www.canvasxpress.org](https://www.canvasxpress.org).

**Note**: We will begin replacing readthedocs with Quarto based examples this year.

**
New:** [Jupyter Notebook based examples](https://github.com/docinfosci/canvasxpress-python/tree/main/tutorials/notebook/cx_site_chart_examples)
for hundreds of chart configurations!

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

Jupyter components can be additionally installed with the core package via:

```terminal
pip install "canvasxpress[jupyter]"
```

Dash components can be additionally installed as:

```terminal
pip install "canvasxpress[dash]"
```

And Streamlit components can be additionally installed as:

```terminal
pip install "canvasxpress[streamlit]"
```

To get everything in one installation use:

```terminal
pip install "canvasxpress[all]"
```

### A Quick Script/Console Example

Charts can be defined in scripts or a console session and then displayed using the default browser, assuming that a
graphical browser with Javascript support is available on the host system.

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.popup import CXBrowserPopup

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
    browser = CXBrowserPopup(chart)
    browser.render()
```

Upon running the example the following chart will be displayed on systems such as MacOS X, Windows, and Linux with
graphical systems:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/flask_bar_chart_basic.png" align="center" width="600"></a>

### A Quick Streamlit Example

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
from canvasxpress.render import streamlit as cx_st

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
    cx_st.plot(chord_chart)
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

### A Quick Dash Example

[Plotly Dash](https://dash.plotly.com/) is a popular dashboard framework similar to R/shiny for Python. Dash
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
from dash import Dash, html
from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.dash import CXElementFactory

g_app = Dash(__name__)

# No need to create_element many forms of data into CanvasXpress data objects; for example, use this CSV as-is.
_g_csv = """, Apples, Oranges, Bananas
SF      ,      4,       1,       2
Montreal,      2,       4,       5
"""

_g_cx_colors = {
    "background": "#111111",
    "text": "rgb(127,219,255)",
    "bars": ["rgb(99,110,250)", "rgb(239,85,59)"],
}

# Work with data as normal Python values.  cx_data could also have been a DataFrame, JSON, URL, etc.
_g_cx_chart = CanvasXpress(
    render_to="fruit_consumption",
    data=_g_csv,
    config={
        "colors": _g_cx_colors["bars"],
        "graphOrientation": "vertical",
        "smpLabelRotate": 90,
        "plotBox": True,
        "plotBoxColor": "White",
        "background": _g_cx_colors["background"],
        "theme": "Plotly",
        "xAxis": ["Fruit", "City"],
        "xAxisTitle": "Amount",
        "xAxis2Show": False,
        "xAxisMinorTicks": False,
        "axisTitleColor": _g_cx_colors["text"],
        "axisTickColor": _g_cx_colors["text"],
        "legendColor": _g_cx_colors["text"],
        "smpTitle": "Fruit",
        "smpTitleFontColor": _g_cx_colors["text"],
        "smpLabelFontColor": _g_cx_colors["text"],
    },
    width=650,
    height=450,
)

# Application
g_app.layout = html.Div(
    style={"backgroundColor": _g_cx_colors["background"]},
    children=[
        html.H1(
            children="Hello Dash",
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.H2(
            children=(
                "An Example of the Advanced CanvasXpress and CXDashElementFactory"
                " Classes for Plotting a CanvasXpress Chart"
            ),
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.Div(
            id="chart-container",
            children=[
                html.Div(
                    id="cx-container",
                    style={"textAlign": "center"},
                    children=CXElementFactory.render(_g_cx_chart),
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

### A Quick Flask Example

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
