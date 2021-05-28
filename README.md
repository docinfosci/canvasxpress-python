# CanvasXpress Python Library

<a href="https://www.canvasxpress.org">
<img src="https://raw.githubusercontent.com/docinfosci/canvasxpress-python/main/readme/images/hexagon.png" align="left" width="175"></a>

## About CanvasXpress for Python

***This package was recently released for general use.  We maintain thorough code coverage and use the package ourselves,
but it remains possible that edge use cases can be refined.  We appreciate your feedback and patience.***

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
| **Version Info** | [![Release](https://img.shields.io/pypi/v/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | 
| **Popularity** | ![PyPI - Downloads](https://img.shields.io/pypi/dm/canvasxpress) |
| **Compatibility** | [![Compatibility](https://img.shields.io/pypi/pyversions/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | 
| **Implementations** | [![Implementations](https://img.shields.io/pypi/implementation/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | 
| **Build Status** | [![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/main.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=main) | 
| **Test Status** | [![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=main)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=main) | 
| **Requirements Status** | [![Requirements Status](https://requires.io/github/docinfosci/canvasxpress-python/requirements.svg?branch=main)](https://requires.io/github/docinfosci/canvasxpress-python/requirements/?branch=main) | 
| **Documentation Status** | [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=latest)](https://canvasxpress-python.readthedocs.io/en/latest/) | 
| **Activity** | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/main)](https://github.com/docinfosci/canvasxpress-python) | 
<!-- End Badges -->

### Recent Enhancements

#### 2021 May 28: width, height, and canvas properties
The `CanvasXpress` object now accepts dedicated `width`, `height`, `canvas` 
properties.  

`width` and `height` replace the now-deprecated `element_width` and 
`element_height` properties, and these are expected to be the final 
names used for each.  Values for each are used in the `<canvas>` element
generated for use in HTML, and they affect the render container sizes when
used in conjunction with contexts such as Jupyter Notebooks.

`canvas` tracks `CXConfig` values that become attributes of the generated
`<canvas>` element.  In this manner attributes such as `class` or `style`
can be calculated and managed at the Python tier.

See the documentation and examples for detailed usage.

#### 2021 May 28: dict and tuple values now supported for CXConfigs
The `CanvasXpress` class uses `CXConfigs` to track configuration parameters 
for the chart and `<canvas>` element.  These now accept `dict` and `tuple`
values for more convenient initialization of the `CanvasXpress` object.

See the documentation and examples for detailed usage.

#### 2021 May 21: CXUrlData added
CanvasXpress accepts URL references to files or endpoints with properly 
formatted JSON data.  `CXUrlData` has been added to support URL passthrough 
to the CanvasXpress Javascript, along with some validation ability at the
Python tier.

#### 2021 May 18: CXDataProfile added
CanvasXpress has specific requirements for data organization within a JSON so 
that it can be properly rendered in a chart.  See the 
[CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data) for
additional information.

Data generated or provided at the Python tier might not satisfy those 
requirements, especially where matrix data is concerned.  CXDataProfile has
been added as a component to facilitate proper JSON formatting when providing
the data to the rendered CanvasXpress Javascript.  CXData has been enhanced to
make use of CXDataProfile.

The [CanvasXpress for Python documentation](https://canvasxpress-python.readthedocs.org)
 discusses profiles in detail, but in summary:

* Each CXData object is provided with a CXStandardProfile that understands how
  to pass through or add `y` `vars`, `smps`, and `data` attributes as proper.

* Default values for `vars` and `smps` are autogenerated if missing, provided 
  that sufficient information in the data is available.  This is especially
  handy for common matrix data sources typical in Python applications.
  
* Validation is supported for affirming that rows and columns in data align with
  provided `vars` and `smps` attributes, respectively.
  
As such, raw data can be passed on to CanvasXpress via key-pair structures so as
to keep mapping between Javascript and Python sources simple; however, custom
or default formatting is now supported at the Python tier to ease integration
and exploration where `y` attributes are not present in the source data.

***Additional** functionality will be added soon, such as to support `x` and `z`
CanvasXpress JSON data profiles.  Expect rapid enhancements in this area.*

#### 2021 May 17: Adjusted property names
To better align with CanvasXpress for Javascript, or otherwise avoid confusion, 
some property names were changed in the `CanvasXpress` class:

* `target_id` has been replaced with `render_to` to align with the JS 
  `renderTo` attribute.  Functionality is identical.  `target_id` will 
  remain as a deprecated property through May, after which it will be removed
  per team convenience.
  
* `configs` has been replaced with `config` to align with the JS 
  `config` attribute.  Functionality is identical.  `configs` will 
  remain as a deprecated property through May, after which it will be removed
  per team convenience.
  
* `chart_width` and `chart_height` are replaced with `element_width` and 
  `element_height`, respectively.  These properties dictate the container
  size at the Python tier in application, such as the render window provided
  for Jupyter Notebooks.  The actual CanvasXpress chart continues to use the
  `width` and `height` attributes per the JS documentation, and if these values
  result in a rendered chart larger than the element window then depending on
  the application context aspects such as scrollbars might appear to provide
  full access.  The distinction is maintained for applications with non-reactive
  user interfaces, such as what might be typical of QT apps.

### Roadmap

This package is actively maintained and developed.  Our focus for 2021 is:

#### Immediate Focus

- Enhanced examples and documentation for CXDataProfile components
- Support CanvasXpress JSON data object `x` and `z` attributes in profiles
- Support alternate CanvasXpress data objects for venn (etc.)
- An exhaustive Jupyter Notebook tutorial for all aspects of the package

#### General Focus

- Continued alignment with the CanvasXpress Javascript library
- Continued stability and security, if/as needed
- Expanded examples and tutorials
- Expanded platform integrations

## Getting Started

### Documentation

The [documentation site](https://canvasxpress-python.readthedocs.io/en/latest/) 
contains complete [examples](https://canvasxpress-python.readthedocs.io/en/latest/examples/) 
and [API documentation](https://canvasxpress-python.readthedocs.io/en/latest/api/).
There is also a wealth of additional information, including full Javascript API 
documentation, at [https://www.canvasxpress.org](https://www.canvasxpress.org).

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
    </head>
    <body>
    
        <!-- 1. DOM element where the visualization will be displayed -->
        {{canvas_element|safe}}
        
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

<img src="flask_bar_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created your first Python-driven CanvasXpress app!
