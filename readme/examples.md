# CanvasXpress for Python Examples

This section provides CanvasXpress for Python usage examples that cover typical
platforms and scenarios.  The emphasis is on the Python package rather than 
CanvasXpress APIs, and for the latter the CanvasXpress documentation is a 
strongly recommended read:

- [CanvasXpress](https://www.canvasxpress.org)
- [CanvasXpress Docs](https://www.canvasxpress.org/docs.html)
- [CanvasXpress Examples](https://www.canvasxpress.org/examples.html)

## Web Example

[flask](https://palletsprojects.com/p/flask/) is a popular lean Web development 
framework for Python based applications.  flask applications can serve Web 
pages, RESTful APIs, and similar backend service concepts.  This example shows
how to create a basic flask application that provides a basic Web page with a
CanvasXpress chart composed using Python in the backend.

The concepts in this example equally apply to other frameworks that can serve 
Web pages, such as Django and Tornado.

### Create a Basic flask App

A basic flask app provides a means by which:

1. A local, development server can be started
1. A function can respond to a URL

First install flask and CanvasXpress for Python:
```terminal
pip install -U flask canvasxpress
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
                {{bar_graph|safe}}
            })
        </script>
    
    </body>
</html>
```

The HTML file, which uses [Jinja syntax](https://palletsprojects.com/p/jinja/) achieves three things:

1. Provides a location for a `<div>` element that marks where the chart will be placed.
1. References the CanvasXpress CSS and JS files needed to illustrate and operate the charts.
1. Provides a location for the Javascript that will replace the chart `<div>` with a working element on page load.

Going back to our flask app, we can add a basic chart definition with some data to our example function:

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
        target_id="example_chart",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]]
                }
            }
        ),
        configs=CXConfigs(
            CXGraphType(CXGraphTypeOptions.Bar)
        )
    )

    # Get the HTML parts for use in our Web page:
    html_parts: dict = chart.render_to_html_parts()

    # Return a Web page based on canvasxpress_example.html and our HTML parts
    return render_template(
        "canvasxpress_example.html",
        canvas_element=html_parts["cx_canvas"],
        bar_graph=html_parts["cx_js"]
    )
```

Rerun the flask app on the command line and browse to the indicated IP and URL.
A page similar to the following will be displayed:

<img src="flask_bar_chart_basic.png" align="center" width="500"></a>

Congratulations!  You have created your first Python-driven CanvasXpress app!

## Jupyter Notebook


## Extras

[Jyputer Notebook](https://jupyter.org) is a programming journal, among other things, based 
in part on the powerful [IPython](https://ipython.org) framework.  CanvasXpress for Python
provides built-in support for IPython Web containers.  This example shows how to make the 
same chart in the flask example available in an IPython/Jupyter session.

Assuming familiarity with Jupyter Notebooks in general, create a new Notebook based on the
Python3 kernal.  If that kernal is note available the system administrator will be needed
to add one.

First, the canvasxpress package and supporting requirements need to be installed.  This can
be performed by the system administrator or, for Notebooks with proper user permissions, 
the packages can be installed via the Notebook.

The essential install command is:

```jupyterpython
import sys
!{sys.executable} -m pip install -U canvasxpress
```

`!{sys.executable}` invokes the installation python3 application.  `-U` informs
pip that the latest edition of the specified package should be used.

If other requirements are missing then the same command can be used to satisy the missing
packages.  At the time of writing the full installation is:

```jupyterpython
import sys
!{sys.executable} -m pip install -U pandas gitpython pytz canvasxpress
```

In flask a function returning the chart HTML parts merged into an HTML template needed to be
created.  Notebook charts are simpler in that the CanvasXpress for Python provided `CXNoteBook`
can be used to render the chart as part of the cell's output.

Taking the essential chart logic from the flask example, the import for `CXNoteBook` is added
and that component's `render()` function is used:

```jupyterpython
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.render.jupyter import CXNoteBook

# Define a CX bar chart with some basic data
chart: CanvasXpress = CanvasXpress(
    target_id="example_chart",
    data=CXDictData(
        {
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]]
            }
        }
    ),
    configs=CXConfigs(
        CXGraphType(CXGraphTypeOptions.Bar)
    )
)
    
demo_nb = CXNoteBook(chart)
demo_nb.render()
```

Executing that cell will result in output similar to:

