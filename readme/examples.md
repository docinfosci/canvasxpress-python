# CanvasXpress for Python Examples

This section provides CanvasXpress for Python usage examples that cover typical platforms and scenarios. The emphasis is
on the Python package rather than CanvasXpress APIs, and for the latter the CanvasXpress documentation is a strongly
recommended read:

- [CanvasXpress](https://www.canvasxpress.org)
- [CanvasXpress Docs](https://www.canvasxpress.org/docs.html)
- [CanvasXpress Examples](https://www.canvasxpress.org/examples.html)

## Web Example

[flask](https://palletsprojects.com/p/flask/) is a popular lean Web development framework for Python based applications.
flask applications can serve Web pages, RESTful APIs, and similar backend service concepts. This example shows how to
create a basic flask application that provides a basic Web page with a CanvasXpress chart composed using Python in the
backend.

The concepts in this example equally apply to other frameworks that can serve Web pages, such as Django and Tornado.

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

CanvasXpress for Python can be used to define a chart with various attributes and then generate the necessary HTML and
Javascript for proper display in the browser.

Add a `templates` directory to the same location as the `app.py` file, and inside add a file
called `canvasxpress_example.html`. Inside the file add:

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
        {
            {
                bar_graph | safe
            }
        }
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

Rerun the flask app on the command line and browse to the indicated IP and URL. A page similar to the following will be
displayed:

<img src="flask_bar_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created your first Python-driven CanvasXpress app!

## Jupyter Notebook

[Jyputer Notebook](https://jupyter.org) is a programming journal, among other things, based in part on the
powerful [IPython](https://ipython.org) framework. CanvasXpress for Python provides built-in support for IPython Web
containers. This example shows how to make the same chart in the flask example available in an IPython/Jupyter session.

Assuming familiarity with Jupyter Notebooks in general, create a new Notebook based on the Python3 kernal. If that
kernal is note available the system administrator will be needed to add one.

### Install *canvasxpress* and Supporting Packages

First, the canvasxpress package and supporting requirements need to be installed. This can be performed by the system
administrator or, for Notebooks with proper user permissions, the packages can be installed via the Notebook.

The essential install command is:

```jupyterpython
import sys
!{sys.executable} -m pip install -U canvasxpress
```

`!{sys.executable}` invokes the installation python3 application.  `-U` informs pip that the latest edition of the
specified package should be used.

If other requirements are missing then the same command can be used to satisy the missing packages. At the time of
writing the full installation is:

```jupyterpython
import sys
!{sys.executable} -m pip install -U pandas gitpython pytz canvasxpress
```

### Create a Chart

In flask a function returning the chart HTML parts merged into an HTML template needed to be created. Notebook charts
are simpler in that the CanvasXpress for Python provided `CXNoteBook`
can be used to render the chart as part of the cell's output.

Taking the essential chart logic from the flask example, the import for `CXNoteBook` is added and that
component's `render()` function is used:

```python
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

<img src="jupyter_bar_chart_basic.png" align="center" width="600"></a>

Congratulations!  You have created your first IPython-driven CanvasXpress chart!

### Using Chart Options to Create an Interesting Illustration

The CanvasXpress site maintains many useful examples, of which one is a Scatter 3D chart that makes use of the iris data
set.  [Read about it here](https://www.canvasxpress.org/examples/scatter3d-1.html).

The following example converts the Javascript into the Python equivalent to produce the exact same chart as produced by
the example. You can learn more about the options used in this example, in addition to others, in
our [API Documentation](../api/).

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.render.jupyter import CXNoteBook

iris_ds = CXDictData(
    {
        "z": {
            "Species": ["setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "setosa", "setosa", "setosa", "setosa", "setosa",
                        "setosa", "setosa", "setosa", "setosa", "setosa", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "versicolor", "versicolor", 
                        "versicolor", "versicolor", "virginica", "virginica",
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica",
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica", 
                        "virginica", "virginica", "virginica", "virginica"]
        },
        "y": {
            "vars": ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", 
                     "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17", 
                     "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25", 
                     "s26", "s27", "s28", "s29", "s30", "s31", "s32", "s33", 
                     "s34", "s35", "s36", "s37", "s38", "s39", "s40", "s41", 
                     "s42", "s43", "s44", "s45", "s46", "s47", "s48", "s49", 
                     "s50", "s51", "s52", "s53", "s54", "s55", "s56", "s57",
                     "s58", "s59", "s60", "s61", "s62", "s63", "s64", "s65", 
                     "s66", "s67", "s68", "s69", "s70", "s71", "s72", "s73", 
                     "s74", "s75", "s76", "s77", "s78", "s79", "s80", "s81", 
                     "s82", "s83", "s84", "s85", "s86", "s87", "s88", "s89", 
                     "s90", "s91", "s92", "s93", "s94", "s95", "s96", "s97", 
                     "s98", "s99", "s100", "s101", "s102", "s103", "s104", 
                     "s105", "s106", "s107", "s108", "s109", "s110", "s111",
                     "s112", "s113", "s114", "s115", "s116", "s117", "s118", 
                     "s119", "s120", "s121", "s122", "s123", "s124", "s125", 
                     "s126", "s127", "s128", "s129", "s130", "s131", "s132", 
                     "s133", "s134", "s135", "s136", "s137", "s138", "s139", 
                     "s140", "s141", "s142", "s143", "s144", "s145", "s146", 
                     "s147", "s148", "s149", "s150"],
            "smps": ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"],
            "data": [
                [5.1, 3.5, 1.4, 0.2],
                [4.9, 3, 1.4, 0.2],
                [4.7, 3.2, 1.3, 0.2],
                [4.6, 3.1, 1.5, 0.2],
                [5, 3.6, 1.4, 0.2],
                [5.4, 3.9, 1.7, 0.4],
                [4.6, 3.4, 1.4, 0.3],
                [5, 3.4, 1.5, 0.2],
                [4.4, 2.9, 1.4, 0.2],
                [4.9, 3.1, 1.5, 0.1],
                [5.4, 3.7, 1.5, 0.2],
                [4.8, 3.4, 1.6, 0.2],
                [4.8, 3, 1.4, 0.1],
                [4.3, 3, 1.1, 0.1],
                [5.8, 4, 1.2, 0.2],
                [5.7, 4.4, 1.5, 0.4],
                [5.4, 3.9, 1.3, 0.4],
                [5.1, 3.5, 1.4, 0.3],
                [5.7, 3.8, 1.7, 0.3],
                [5.1, 3.8, 1.5, 0.3],
                [5.4, 3.4, 1.7, 0.2],
                [5.1, 3.7, 1.5, 0.4],
                [4.6, 3.6, 1, 0.2],
                [5.1, 3.3, 1.7, 0.5],
                [4.8, 3.4, 1.9, 0.2],
                [5, 3, 1.6, 0.2],
                [5, 3.4, 1.6, 0.4],
                [5.2, 3.5, 1.5, 0.2],
                [5.2, 3.4, 1.4, 0.2],
                [4.7, 3.2, 1.6, 0.2],
                [4.8, 3.1, 1.6, 0.2],
                [5.4, 3.4, 1.5, 0.4],
                [5.2, 4.1, 1.5, 0.1],
                [5.5, 4.2, 1.4, 0.2],
                [4.9, 3.1, 1.5, 0.2],
                [5, 3.2, 1.2, 0.2],
                [5.5, 3.5, 1.3, 0.2],
                [4.9, 3.6, 1.4, 0.1],
                [4.4, 3, 1.3, 0.2],
                [5.1, 3.4, 1.5, 0.2],
                [5, 3.5, 1.3, 0.3],
                [4.5, 2.3, 1.3, 0.3],
                [4.4, 3.2, 1.3, 0.2],
                [5, 3.5, 1.6, 0.6],
                [5.1, 3.8, 1.9, 0.4],
                [4.8, 3, 1.4, 0.3],
                [5.1, 3.8, 1.6, 0.2],
                [4.6, 3.2, 1.4, 0.2],
                [5.3, 3.7, 1.5, 0.2],
                [5, 3.3, 1.4, 0.2],
                [7, 3.2, 4.7, 1.4],
                [6.4, 3.2, 4.5, 1.5],
                [6.9, 3.1, 4.9, 1.5],
                [5.5, 2.3, 4, 1.3],
                [6.5, 2.8, 4.6, 1.5],
                [5.7, 2.8, 4.5, 1.3],
                [6.3, 3.3, 4.7, 1.6],
                [4.9, 2.4, 3.3, 1],
                [6.6, 2.9, 4.6, 1.3],
                [5.2, 2.7, 3.9, 1.4],
                [5, 2, 3.5, 1],
                [5.9, 3, 4.2, 1.5],
                [6, 2.2, 4, 1],
                [6.1, 2.9, 4.7, 1.4],
                [5.6, 2.9, 3.6, 1.3],
                [6.7, 3.1, 4.4, 1.4],
                [5.6, 3, 4.5, 1.5],
                [5.8, 2.7, 4.1, 1],
                [6.2, 2.2, 4.5, 1.5],
                [5.6, 2.5, 3.9, 1.1],
                [5.9, 3.2, 4.8, 1.8],
                [6.1, 2.8, 4, 1.3],
                [6.3, 2.5, 4.9, 1.5],
                [6.1, 2.8, 4.7, 1.2],
                [6.4, 2.9, 4.3, 1.3],
                [6.6, 3, 4.4, 1.4],
                [6.8, 2.8, 4.8, 1.4],
                [6.7, 3, 5, 1.7],
                [6, 2.9, 4.5, 1.5],
                [5.7, 2.6, 3.5, 1],
                [5.5, 2.4, 3.8, 1.1],
                [5.5, 2.4, 3.7, 1],
                [5.8, 2.7, 3.9, 1.2],
                [6, 2.7, 5.1, 1.6],
                [5.4, 3, 4.5, 1.5],
                [6, 3.4, 4.5, 1.6],
                [6.7, 3.1, 4.7, 1.5],
                [6.3, 2.3, 4.4, 1.3],
                [5.6, 3, 4.1, 1.3],
                [5.5, 2.5, 4, 1.3],
                [5.5, 2.6, 4.4, 1.2],
                [6.1, 3, 4.6, 1.4],
                [5.8, 2.6, 4, 1.2],
                [5, 2.3, 3.3, 1],
                [5.6, 2.7, 4.2, 1.3],
                [5.7, 3, 4.2, 1.2],
                [5.7, 2.9, 4.2, 1.3],
                [6.2, 2.9, 4.3, 1.3],
                [5.1, 2.5, 3, 1.1],
                [5.7, 2.8, 4.1, 1.3],
                [6.3, 3.3, 6, 2.5],
                [5.8, 2.7, 5.1, 1.9],
                [7.1, 3, 5.9, 2.1],
                [6.3, 2.9, 5.6, 1.8],
                [6.5, 3, 5.8, 2.2],
                [7.6, 3, 6.6, 2.1],
                [4.9, 2.5, 4.5, 1.7],
                [7.3, 2.9, 6.3, 1.8],
                [6.7, 2.5, 5.8, 1.8],
                [7.2, 3.6, 6.1, 2.5],
                [6.5, 3.2, 5.1, 2],
                [6.4, 2.7, 5.3, 1.9],
                [6.8, 3, 5.5, 2.1],
                [5.7, 2.5, 5, 2],
                [5.8, 2.8, 5.1, 2.4],
                [6.4, 3.2, 5.3, 2.3],
                [6.5, 3, 5.5, 1.8],
                [7.7, 3.8, 6.7, 2.2],
                [7.7, 2.6, 6.9, 2.3],
                [6, 2.2, 5, 1.5],
                [6.9, 3.2, 5.7, 2.3],
                [5.6, 2.8, 4.9, 2],
                [7.7, 2.8, 6.7, 2],
                [6.3, 2.7, 4.9, 1.8],
                [6.7, 3.3, 5.7, 2.1],
                [7.2, 3.2, 6, 1.8],
                [6.2, 2.8, 4.8, 1.8],
                [6.1, 3, 4.9, 1.8],
                [6.4, 2.8, 5.6, 2.1],
                [7.2, 3, 5.8, 1.6],
                [7.4, 2.8, 6.1, 1.9],
                [7.9, 3.8, 6.4, 2],
                [6.4, 2.8, 5.6, 2.2],
                [6.3, 2.8, 5.1, 1.5],
                [6.1, 2.6, 5.6, 1.4],
                [7.7, 3, 6.1, 2.3],
                [6.3, 3.4, 5.6, 2.4],
                [6.4, 3.1, 5.5, 1.8],
                [6, 3, 4.8, 1.8],
                [6.9, 3.1, 5.4, 2.1],
                [6.7, 3.1, 5.6, 2.4],
                [6.9, 3.1, 5.1, 2.3],
                [5.8, 2.7, 5.1, 1.9],
                [6.8, 3.2, 5.9, 2.3],
                [6.7, 3.3, 5.7, 2.5],
                [6.7, 3, 5.2, 2.3],
                [6.3, 2.5, 5, 1.9],
                [6.5, 3, 5.2, 2],
                [6.2, 3.4, 5.4, 2.3],
                [5.9, 3, 5.1, 1.8]
            ]
        }
    }
)

chart_options = CXConfigs()
chart_options
    .add(CXGraphType(CXGraphTypeOptions.Scatter3D))
    .set_param('axisTickScaleFontFactor', 0.5)
    .set_param('axisTitleScaleFontFactor', 0.5)
    .set_param('colorBy', 'Species')
    .set_param('theme', 'CanvasXpress')
    .set_param('title', 'Iris Data Set')
    .set_param('xAxis', ['Sepal.Length'])
    .set_param('yAxis', ['Sepal.Width'])
    .set_param('zAxis', ['Petal.Length'])

chart = CanvasXpress(
    target_id="iris_scatter3d_example",
    data=iris_ds,
    configs=chart_options
)

iris_scatter3d_nb = CXNoteBook(chart)
iris_scatter3d_nb.render()
```

## Javascript Events

CanvasXpress provides support for [Javascript events](https://www.canvasxpress.org/docs.html#events)
via hook functions that are called when events occur, such as mouse movement or clicks.

CanvasXpress for Python provides support via the `canvasxpress.js` package.  `CXEvents` provides collection
functionality for sets of `CXEvent` objects, which hold the Javascript instructions for various events.

An example event for graph clicks with popup information is:

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

The general template of a CanvasXpress Javascript hook function is:

```javascript
function (o, e, t) {
    // script logic goes here
};
```

The CXEvent object maps the `id` parameter to the hook event and the `script` parameter to the function body. The
CXEvents object manages collections of CXEvent objects and renders them correctly for use with CanvasXpress in the
browser. Using the Jupyter example, we can add the above event as follows:

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
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
    ),
    events=CXEvents(
        CXEvent(
            id="click",
            script="""
            var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
            t.showInfoSpan(e, s);
            """
        )
    )
)

demo_nb = CXNoteBook(chart)
demo_nb.render()
```

Now a click on the chart displays some information per our function:

<img src="jupyter_bar_chart_click_event.png" align="center" width="600"></a>

## Adding Multiple Configuration Options at Once

CanvasXpress charts can make use of numerous configuration options as part of chart formatting.  `CXConfigs` provides
support for parameter chaining to ease large sets of options.

Option lists using specific data types can be used during `CXConfigs` initialization:

```python
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXString, CXBool

configs: CXConfigs = CXConfigs(
    CXString("legendPosition", "bottomRight"),
    CXString("axisAlgorithm", "rPretty"),
    CXBool("legendBox", True)
)
```

Chaining can be performed using specific data types:

```python
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXString, CXBool

configs: CXConfigs = CXConfigs()

# ...

configs
    .add(CXString("legendPosition", "bottomRight"))
    .add(CXString("axisAlgorithm", "rPretty"))
    .add(CXBool("legendBox", True))
```

Chaining can also be performed using inferred data types:

```python
from canvasxpress.config.collection import CXConfigs

configs: CXConfigs = CXConfigs()

# ...

configs
    .set_param("legendPosition", "bottomRight")
    .set_param("axisAlgorithm", "rPretty")
    .set_param("legendBox", True)
```

## Using Cloud Data

CanvasXpress for Python does not directly support non-local data, such as that obtained from a URL; however, it does
support the [pandas](https://pandas.pydata.org)
package. pandas supports loading data from URLs and databases.

```python
import pandas as pd
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.matrix import CXDataframeData

chart: CanvasXpress = CanvasXpress(
    target_id="example_chart",
    data=CXDataframeData(
        pd.read_csv("https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv")
    ),
    configs=CXConfigs(
        CXGraphType(CXGraphTypeOptions.Bar)
    )
)

# ...
```
