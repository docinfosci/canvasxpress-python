# Jupyter Notebook Subskill for CanvasXpress

## Prerequisites

**Ensure canvasxpress is installed with the jupyter extra before working in Jupyter:**

```bash
pip install canvasxpress[jupyter]
```

If you use `uv`:
```bash
uv add canvasxpress[jupyter]
```

## Notebook Creation

For creating Jupyter notebooks from scratch with CanvasXpress charts, use the **notebook_builder** skill which handles:
- Creating `.md` files with MyST markdown format
- Converting to `.ipynb` using jupytext
- Proper cell structure (imports, data, config, render)
- Black formatting and best practices

Load the notebook_builder skill when users request notebook creation. This subskill focuses on **using CanvasXpress within Jupyter notebooks**.

## Core CanvasXpress Jupyter Usage

### Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json, convert_to_image
```

### Basic Graph Call in Jupyter

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["GeneA", "GeneB"], "smps": ["S1", "S2", "S3"], "data": [[10, 20, 30], [15, 25, 35]]}
    },
    config={"graphType": "Scatter2D", "title": "My Chart"}
)

graph(cx)
```

`graph(cx)` auto-detects the Jupyter environment and renders the CanvasXpress chart inline.

### Explicit Jupyter Rendering

For more control or when auto-detection fails:

```python
from canvasxpress.plot import graph
from canvasxpress.canvas import CanvasXpress

cx = CanvasXpress(
    data=data,
    config={"graphType": "Heatmap"}
)

# Explicit Jupyter rendering
CXNoteBook(cx).render()
```

### Chart with Unique Identifier

```python
# For notebooks with multiple charts
cx = CanvasXpress(
    render_to="my_chart_id",
    data=df,
    config={"graphType": "Heatmap"}
)
graph(cx)
```

## Essential Jupyter Notebook Concepts for CanvasXpress

### 1. Notebook Setup

```python
# Cell 1: Imports and setup
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
import numpy as np

# Optional: Set default styling
import matplotlib.pyplot as plt
plt.style.use('default')
```

### 2. Minimal Jupyter Notebook Example

```python
# Cell 1: Imports
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
import numpy as np

# Cell 2: Generate or load data
np.random.seed(42)
df = pd.DataFrame(
    np.random.randn(100, 4),
    columns=['GeneA', 'GeneB', 'GeneC', 'GeneD'],
    index=[f'Sample{i}' for i in range(1, 101)]
)

# Cell 3: Create and render chart
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Heatmap",
        "title": "Gene Expression Heatmap",
        "showLegend": True,
        "colorScheme": "Viridis"
    }
)
graph(cx)
```

### 3. Interactive Widgets with CanvasXpress

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import ipywidgets as widgets
import pandas as pd

# Sample data
df = pd.DataFrame(
    np.random.randn(50, 5),
    columns=['A', 'B', 'C', 'D', 'E'],
    index=[f'S{i}' for i in range(50)]
)

# Create widgets
chart_type = widgets.Dropdown(
    options=['Scatter2D', 'Heatmap', 'Bar', 'Line'],
    value='Scatter2D',
    description='Chart:',
    disabled=False
)

color_scheme = widgets.Dropdown(
    options=['CanvasXpress', 'Viridis', 'Plasma', 'CoolWarm'],
    value='CanvasXpress',
    description='Color:',
    disabled=False
)

def update_chart(chart_type_value, color_scheme_value):
    cx = CanvasXpress(
        data=df,
        config={
            "graphType": chart_type_value,
            "title": f"{chart_type_value} - {color_scheme_value}",
            "colorScheme": color_scheme_value
        }
    )
    graph(cx)

widgets.interact(
    update_chart,
    chart_type_value=chart_type,
    color_scheme_value=color_scheme
)
```

### 4. Multiple Charts in a Notebook

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

df = pd.DataFrame(
    {'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1], 'C': [2, 3, 1, 5, 4]},
    index=['S1', 'S2', 'S3', 'S4', 'S5']
)

# First chart
cx1 = CanvasXpress(
    render_to="scatter_chart",
    data=df,
    config={"graphType": "Scatter2D", "title": "Scatter Plot"}
)
graph(cx1)

# Second chart
cx2 = CanvasXpress(
    render_to="heatmap_chart",
    data=df,
    config={"graphType": "Heatmap", "title": "Heatmap"}
)
graph(cx2)

# Third chart
cx3 = CanvasXpress(
    render_to="bar_chart",
    data=df,
    config={"graphType": "Bar", "title": "Bar Chart"}
)
graph(cx3)
```

### 5. Interactive Chart Events in Jupyter

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
import ipywidgets as widgets

output = widgets.Output()

@output.capture()
def render_chart():
    events = CXEvents(
        CXEvent(
            id="click",
            script="var s = 'Clicked: ' + o.y.vars[0] + ', ' + o.y.smps[0]; console.log(s);"
        )
    )
    
    cx = CanvasXpress(
        data=data,
        config={"graphType": "Scatter2D", "title": "Click on Points"},
        events=events
    )
    graph(cx)

render_chart()
display(output)
```

### 6. Loading Data in Jupyter

```python
# From CSV
df = pd.read_csv("data.csv", index_col=0)

# From Excel
df = pd.read_excel("data.xlsx", index_col=0)

# From SQLite database
import sqlite3
conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM measurements", conn)
conn.close()

# From URL
import requests
df = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))

# Render chart
cx = CanvasXpress(data=df, config={"graphType": "Heatmap"})
graph(cx)
```

### 7. Data Exploration Workflow in Jupyter

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

# Load data
df = pd.read_csv("expression_data.csv", index_col=0)

# Explore data
print(df.head())
print(df.describe())

# Quick visualization
cx = CanvasXpress(
    data=df,
    config={"graphType": "Heatmap", "title": "Quick Look"}
)
graph(cx)

# Filter data
df_filtered = df[(df.mean(axis=1) > 0)]

# Visualize filtered data
cx_filtered = CanvasXpress(
    data=df_filtered,
    config={"graphType": "Heatmap", "title": "Filtered Data"}
)
graph(cx_filtered)
```

### 8. Annotation Integration

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

# Load data
df = pd.read_csv("expression.csv", index_col=0)

# Load annotations
sample_annot = pd.read_csv("sample_annotations.csv", index_col=0)
variable_annot = pd.read_csv("variable_annotations.csv", index_col=0)

# Create chart with annotations
cx = CanvasXpress(
    data=df,
    sample_annotation=sample_annot,
    variable_annotation=variable_annot,
    config={
        "graphType": "Heatmap",
        "title": "Annotated Heatmap",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["Treatment", "Batch"],
        "showVarOverlaysLegend": True,
        "varOverlays": ["Pathway", "Category"]
    }
)
graph(cx)
```

## Complete Jupyter Notebook Template

```python
"""
CanvasXpress Jupyter Notebook Template
"""
# In[1]: Setup and Imports
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json
import pandas as pd
import numpy as np

# In[2]: Load Data
@lru_cache(maxsize=1)
def load_data():
    """Load and cache the dataset."""
    return pd.read_csv("data.csv", index_col=0)

df = load_data()

# In[3]: Data Summary
print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()[:10]}...")
print(df.describe())

# In[4]: First Visualization
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Heatmap",
        "title": "Initial Overview",
        "showLegend": True
    }
)
graph(cx)

# In[5]: Interactive Analysis
import ipywidgets as widgets

chart_selector = widgets.Dropdown(
    options=["Scatter2D", "Heatmap", "Bar", "Line", "Boxplot"],
    value="Scatter2D",
    description="Chart Type:"
)

display(chart_selector)

def on_chart_change(change):
    cx = CanvasXpress(
        data=df,
        config={
            "graphType": change["new"],
            "title": f"Analysis: {change['new']}"
        }
    )
    graph(cx)

chart_selector.observe(on_chart_change, names="value")

# In[6]: Export Options
json_output = convert_to_reproducible_json(cx)
print("JSON configuration ready for export")
```

## Key Takeaways

1. **Always install canvasxpress with the jupyter extra** (`pip install canvasxpress[jupyter]`) before working in Jupyter
2. **Use `graph(cx)`** for rendering - it auto-detects Jupyter environments
3. **Use `render_to` parameter** for unique chart identification when multiple charts exist
4. **Leverage Jupyter widgets** (`ipywidgets`) for interactive chart controls
5. **Cache expensive data loading** with `@lru_cache` or `@st.cache_data` equivalents
6. **Use explicit `CXNoteBook(cx).render()`** if auto-detection fails
7. **CanvasXpress events work** in Jupyter for interactive chart exploration
8. **Load data from various sources**: CSV, Excel, SQLite, URLs
9. **Integrate annotations** for rich metadata visualization
10. **Export configurations** with `convert_to_reproducible_json()` for reproducibility
