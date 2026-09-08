# Flask/FastAPI Subskill for CanvasXpress

## Prerequisites

**Ensure canvasxpress is installed. For Flask/FastAPI, the base package is sufficient:**

```bash
pip install canvasxpress
```

For additional utilities, install the all extra:
```bash
pip install canvasxpress[all]
```

If you use `uv`:
```bash
uv add canvasxpress
# or for all extras:
uv add canvasxpress[all]
```

## Core CanvasXpress Flask/FastAPI Usage

### Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json, convert_to_image
```

### Basic Graph Call in Flask/FastAPI

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["GeneA", "GeneB"], "smps": ["S1", "S2", "S3"], "data": [[10, 20, 30], [15, 25, 35]]}
    },
    config={"graphType": "Scatter2D", "title": "My Chart"}
)

# For Flask/FastAPI, always use unique render_to identifiers
cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D"},
    render_to="unique_chart_id"
)
```

### Rendering CanvasXpress in Flask

```python
from flask import Flask, render_template
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = Flask(__name__)

@app.route("/")
def index():
    cx = CanvasXpress(
        render_to="chart_1",
        data=data,
        config={"graphType": "Heatmap", "title": "Flask Dashboard"}
    )
    chart_html = cx.render_to_html_parts()
    return render_template("index.html", chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
```

### Rendering CanvasXpress in FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    cx = CanvasXpress(
        render_to="chart_1",
        data=data,
        config={"graphType": "Scatter2D", "title": "FastAPI Dashboard"}
    )
    chart_html = cx.render_to_html_parts()
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>CanvasXpress FastAPI</title></head>
    <body>
        <h1>My Dashboard</h1>
        {chart_html}
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Essential Flask/FastAPI Concepts for CanvasXpress

### 1. Minimal Flask App with CanvasXpress

```python
from flask import Flask, render_template
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    cx = CanvasXpress(
        render_to="sales_chart",
        data={
            "y": {
                "vars": ["Sales"],
                "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
                "data": [[120, 150, 180, 200, 250]]
            }
        },
        config={"graphType": "Bar", "title": "Monthly Sales"}
    )
    return render_template("index.html", chart=cx.render_to_html_parts())

if __name__ == "__main__":
    app.run(debug=True)
```

### 2. Flask App with Chart Templates

```python
from flask import Flask, render_template
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():
    charts = [
        CanvasXpress(render_to="chart1", data=df1, config={"graphType": "Scatter2D", "title": "Chart 1"}),
        CanvasXpress(render_to="chart2", data=df2, config={"graphType": "Heatmap", "title": "Chart 2"}),
        CanvasXpress(render_to="chart3", data=df3, config={"graphType": "Bar", "title": "Chart 3"})
    ]
    return render_template("dashboard.html", charts=[c.render_to_html_parts() for c in charts])

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. Flask App with Dynamic Charts

```python
from flask import Flask, render_template, request
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    chart_type = request.args.get("type", "Scatter2D")
    cx = CanvasXpress(
        render_to="dynamic_chart",
        data=df,
        config={"graphType": chart_type, "title": f"Dynamic: {chart_type}"}
    )
    return render_template("index.html", chart=cx.render_to_html_parts())

if __name__ == "__main__":
    app.run(debug=True)
```

### 4. Flask App with API Endpoints

```python
from flask import Flask, jsonify, render_template
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():
    cx = CanvasXpress(
        render_to="chart",
        data=df,
        config={"graphType": "Scatter2D"}
    )
    return render_template("index.html", chart=cx.render_to_html_parts())

@app.route("/api/chart_config")
def get_chart_config():
    cx = CanvasXpress(
        data=df,
        config={"graphType": "Scatter2D"}
    )
    return jsonify(convert_to_reproducible_json(cx))

@app.route("/api/data")
def get_data():
    return jsonify({
        "vars": df.index.tolist(),
        "smps": df.columns.tolist(),
        "data": df.values.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
```

### 5. FastAPI App with Dynamic Charts

```python
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard(chart_type: str = Query("Scatter2D")):
    cx = CanvasXpress(
        render_to="chart",
        data=df,
        config={"graphType": chart_type, "title": f"Analysis: {chart_type}"}
    )
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>CanvasXpress FastAPI</title></head>
    <body>
        <h1>Dynamic Dashboard</h1>
        <form method="get">
            <select name="chart_type">
                <option value="Scatter2D" {"selected" if chart_type == "Scatter2D" else ""}>Scatter2D</option>
                <option value="Heatmap" {"selected" if chart_type == "Heatmap" else ""}>Heatmap</option>
                <option value="Bar" {"selected" if chart_type == "Bar" else ""}>Bar</option>
            </select>
            <button type="submit">Update</button>
        </form>
        {cx.render_to_html_parts()}
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6. Flask App with File Upload and Charts

```python
from flask import Flask, render_template, request
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded"
    
    file = request.files["file"]
    if file.filename == "":
        return "No file selected"
    
    # Read CSV
    df = pd.read_csv(io.BytesIO(file.read()), index_col=0)
    
    # Generate chart
    cx = CanvasXpress(
        render_to="uploaded_chart",
        data=df,
        config={"graphType": "Heatmap", "title": f"Uploaded: {file.filename}"}
    )
    
    return render_template("index.html", chart=cx.render_to_html_parts())

if __name__ == "__main__":
    app.run(debug=True)
```

### 7. FastAPI App with REST API and Chart Export

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json, convert_to_image
import pandas as pd

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    cx = CanvasXpress(
        render_to="chart",
        data=df,
        config={"graphType": "Scatter2D", "title": "Dashboard"}
    )
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>CanvasXpress API</title></head>
    <body>
        <h1>CanvasXpress FastAPI Dashboard</h1>
        {cx.render_to_html_parts()}
    </body>
    </html>
    """

@app.get("/api/config")
def get_config():
    cx = CanvasXpress(data=df, config={"graphType": "Scatter2D"})
    return JSONResponse(convert_to_reproducible_json(cx))

@app.get("/api/chart")
def get_chart(config_type: str = "Scatter2D"):
    cx = CanvasXpress(
        render_to=f"chart_{config_type}",
        data=df,
        config={"graphType": config_type}
    )
    return HTMLResponse(content=cx.render_to_html_parts())

@app.get("/api/export/png")
def export_png():
    cx = CanvasXpress(data=df, config={"graphType": "Scatter2D"})
    png_bytes = convert_to_image(cx, type="png")
    return JSONResponse(content={"status": "success", "message": "PNG exported"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 8. Complete Flask Application Template

```python
"""
CanvasXpress Flask Application Template
"""
from flask import Flask, render_template, request, jsonify
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
import pandas as pd

app = Flask(__name__)

# Load data once at startup
@app.before_request
def load_data():
    import pandas as pd
    g.data = pd.read_csv("data.csv", index_col=0)

@app.route("/")
def index():
    df = g.data
    chart_type = request.args.get("type", "Heatmap")
    
    cx = CanvasXpress(
        render_to="main_chart",
        data=df,
        config={
            "graphType": chart_type,
            "title": f"Analysis: {chart_type}",
            "showLegend": True
        }
    )
    
    return render_template("index.html", chart=cx.render_to_html_parts())

@app.route("/api/data")
def api_data():
    df = g.data
    return jsonify({
        "vars": df.index.tolist(),
        "smps": df.columns.tolist(),
        "data": df.values.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
```

## Key Takeaways

1. **Always install canvasxpress** (`pip install canvasxpress`) for Flask/FastAPI web apps, or use `canvasxpress[all]` for full functionality
2. **Use `graph(cx)`** for rendering CanvasXpress charts in Flask/FastAPI
3. **Always use unique `render_to` identifiers** for charts in web frameworks
4. **Use `cx.render_to_html_parts()`** to get HTML string for embedding in templates
5. **Use Jinja2 templates** in Flask for clean HTML rendering
6. **Use FastAPI's `HTMLResponse`** for returning HTML directly
7. **Create API endpoints** for chart configurations and data
8. **Handle user input** via query parameters or form submissions
9. **Export functionality** with `convert_to_reproducible_json()` and `convert_to_image()`
10. **Load data efficiently** - cache data loading at startup to avoid repeated I/O
