# CanvasXpress Python Library

<a href="https://www.canvasxpress.org">
<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/images/hexagon.png" align="left" width="175"></a>

## About CanvasXpress for Python

[***CanvasXpress***](https://www.canvasxpress.org) was developed as the core visualization component for bioinformatics and systems biology analysis
at Bristol-Myers Squibb. It supports a large number of [visualizations ](https://www.canvasxpress.org/examples.html) 
to display scientific and non-scientific data. ***CanvasXpress*** also includes a simple and unobtrusive
[user interface](https://www.canvasxpress.org/docs/interface.html) to explore complex data sets, a sophisticated and
unique mechanism to keep track of all user customization for
[Reproducible Research ](https://www.canvasxpress.org/docs/audit.html) purposes, as well as an 'out of the box'
broadcasting capability to synchronize selected data points across all ***CanvasXpress*** plots in a page. Data can
be easily sorted, grouped, transposed, transformed or clustered dynamically. The fully customizable mouse events
as well as the zooming, panning and drag-and-drop capabilities are features that make this library unique in its
class.

***CanvasXpress*** can be now be used within Python for native integration into
IPython and Web environments, such as:

- [Jupyter](https://jupyter.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Django](https://www.djangoproject.com/)

Complete examples using the ***CanvasXpress*** library including the mouse events,
zooming, and broadcasting capabilities are included in this package.  This 
***CanvasXpress*** Python package was created by Dr. Todd C. Brett, with support from 
[Aggregate Genius Inc.](https://www.aggregate-genius.com), in cooperation with the 
***CanvasXpress*** team.

The maintainer of the Python edition of this package is [Dr. Todd C. Brett](https://github.com/docinfosci).

### Project Status

| Topic | Status | 
|---|---|
| **Version and Platform** | [![Release](https://img.shields.io/pypi/v/canvasxpress.svg)](https://pypi.org/project/canvasxpress) [![Compatibility](https://img.shields.io/pypi/pyversions/canvasxpress.svg)](https://pypi.org/project/canvasxpress) [![Implementations](https://img.shields.io/pypi/implementation/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | 
| **Popularity** | [![PyPI - Downloads](https://img.shields.io/pypi/dm/canvasxpress)](https://pypi.org/project/canvasxpress) |
| **Status** | [![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/main.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=main) [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=latest)](https://canvasxpress-python.readthedocs.io/en/latest/) [![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=main)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=main) [![Requirements Status](https://requires.io/github/docinfosci/canvasxpress-python/requirements.svg?branch=main)](https://requires.io/github/docinfosci/canvasxpress-python/requirements/?branch=main) [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/main)](https://github.com/docinfosci/canvasxpress-python) |
<!-- End Badges -->

#### Notes
1. This project uses older versions of `mkdoc` and `pydoc-markdown` due to a 
conflict between these packages.  Once the conflict is resolved they will be
upgraded to current release editions.  This only affects doc builds.

### Recent Enhancements

#### 2021 June 21: Support for reproducable research JSON
CanvasXpress for Javascript can save JSON representations of a rendered chart.
`CanvasXpress` now offers `from_reproducible_json`, which accepts such a JSON
and creates a new `CanvasXpress` object with all properties updated with the 
relevant portions of the JSON.

#### 2021 June 21: CanvasXPress __repr__ now available for example code
The `CanvasXpress` `__repr__` method now produces example Python code for
all properties of the object.  The Python built-in`eval` method can read
the provided string to reconstruct the `CanvasXpress` object when the proper
imports for the CanvasXpress packages/modules are included in the file.

#### 2021 June 16: CXNoteBook accepts file paths for output
The `CXNoteBook` class now accepts a file path at which output rendered in 
Jupyter will also be captured for viewing in later sessions.  Until now a 
temporary file had be used, which remains the default behaviour.

#### 2021 June 16: CXConfigs now accepts lists of values
The `CXConfigs` class can now be initialized using lists of `CXConfig` objects
or their `list/tuple` equivalents (e.g., `["label", "value"]`).  The `add` 
method supports the same formats.  Similarly, wherever the `CanvasXpress` class
accepts a `CXConfigs` object during initialization or assigment a `list` of
`CXConfig` or equivalent objects can be provided.  This is in additon to the 
already supported `dict` collections of `CXConfig` value equivalents.

#### 2021 June 16: direct DataFrame support for CanvasXpress.data
The `CanvasXpress` class already supported `None`, `CXData`, and `dict` data
assignments.  Now raw `DataFrame` is supported on initialization or use of 
the `data` property.

#### 2021 June 16: pop-up browser support
One or more charts can now be displayed in a new Web page using the default 
browser for the host system, assuming it is graphical (e.g., MacOS X or 
Windows).  The **A Quick Script/Console Example** below illustrates the use.

#### 2021 May, June Prior Release Summary
* All JSON data formats now generally supported:
    1. URL:
        * Data path with standard URI formatting (e.g., http, sftp, etc.)
    1. Standard:
        * Matrix and key-pair data
        * `x`, `y`, and `z` attributes
        * Missing attributes calculated for easier data integration
    1. Venn:
        * Matrix and key-pair data 
        * `venn` and `legend` attributes
        * Missing attributes calculated for easier data integration
    1. Network 
        * key-pair data
        * `node` attributes and general `dict`/`list` structure
    1. Genome
        * key-pair data
        * `tracks` and `type` attributes and general `dict`/`list` structure
    1. RAW / Passthrough
        * Matrix and key-pair
        * Beyond conversion of data to JSON, effective pass-through of data
* Python `dict` data direct reference in `CanvasXpress.data` parameter with
  auto-coonversion to `CXDictData`.
* Introduction of `CXDataProfile` and profiled formatting of incomplete
  data per `graphType` configuration.
* Minor bug fixes and expansion of automated tests.
* Jupyter `CXNoteBook` can now render multiple charts in the same group so as
  to support broadcasting.
* `CanvasXpress` now supports the `after_render` property and initialization
  value to enable the `afterRender` attribute of CanvasXpress for Javascript
  objects (includes DOE dashboard support).

### Roadmap

This package is actively maintained and developed.  Our focus for 2021 is:

#### Immediate Focus

* Detailed documentation and working examples of all Python functionality

#### General Focus

* Embedded CanvasXpress for JS libraries (etc.) for offline work
* Integraton with dashboard frameworks for easier applet creation
* Continued alignment with the CanvasXpress Javascript library
* Continued stability and security, if/as needed

## Getting Started

### Documentation

The [documentation site](https://canvasxpress-python.readthedocs.io/en/latest/) 
contains complete [examples](https://canvasxpress-python.readthedocs.io/en/latest/examples/) 
and [API documentation](https://canvasxpress-python.readthedocs.io/en/latest/api/).
There is also a wealth of additional information, including full Javascript API 
documentation, at [https://www.canvasxpress.org](https://www.canvasxpress.org).

### A Quick Script/Console Example
Charts can be defined in scripts or a console session and then displayed using 
the default browser, assuming that a graphical browser with Javascript support 
is available on the host system.

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.render.popup import CXBrowserPopup

if __name__ == "__main__":
    # Define a CX bar chart with some basic data
    chart: CanvasXpress = CanvasXpress(
        render_to="example_chart",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]]
                }
            }
        ),
        config=CXConfigs(
            CXGraphType(CXGraphTypeOptions.Bar)
        )
    )
    
    # Display the chart in its own Web page
    browser = CXBrowserPopup(chart)
    browser.render()
```

Upon running the example the following chart will be displayed on systems such
as MacOS X, Windows, and Linux with graphical systems:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/flask_bar_chart_basic.png" align="center" width="600"></a>

### A Quick Flask Example

[Flask](https://palletsprojects.com/p/flask/) is a popular lean Web development 
framework for Python based applications.  Flask applications can serve Web 
pages, RESTful APIs, and similar backend service concepts.  This example shows
how to create a basic Flask application that provides a basic Web page with a
CanvasXpress chart composed using Python in the backend.

The concepts in this example equally apply to other frameworks that can serve 
Web pages, such as Django and Tornado.

### Create a Basic Flask App

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

### Add a Chart

CanvasXpress for Python can be used to define a chart with various attributes
and then generate the necessary HTML and Javascript for proper display in the
browser.

Add a `templates` directory to the same location as the `app.py` file, and 
inside add a file called `canvasxpress_example.html`.  Inside the file add:

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
                {{canvas_source|safe}}
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
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData

app = Flask(__name__)

@app.route('/')
def canvasxpress_example():
    # Define a CX bar chart with some basic data
    chart: CanvasXpress = CanvasXpress(
        render_to="example_chart",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]]
                }
            }
        ),
        config=CXConfigs(
            CXGraphType(CXGraphTypeOptions.Bar)
        )
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

Rerun the flask app on the command line and browse to the indicated IP and URL. A page similar to the following will be
displayed:

<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/examples/flask_bar_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created your first Python-driven CanvasXpress app!
