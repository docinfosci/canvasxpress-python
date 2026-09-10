# Streamlit Subskill for CanvasXpress

## Prerequisites

**Ensure canvasxpress is installed with the streamlit extra before creating Streamlit apps:**

```bash
pip install canvasxpress[streamlit]
```

If you use `uv`:
```bash
uv add canvasxpress[streamlit]
```

## Core CanvasXpress Streamlit Usage

### Imports

```python
import streamlit as st
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph, convert_to_reproducible_json, convert_to_image, show_in_browser
```

### Basic Graph Call

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["GeneA", "GeneB"], "smps": ["S1", "S2", "S3"], "data": [[10, 20, 30], [15, 25, 35]]}
    },
    config={"graphType": "Scatter2D", "title": "My Chart"}
)

graph(cx)
```

`graph(cx)` auto-detects the Streamlit environment and renders the CanvasXpress chart directly in the app.

### Chart with Dimensions

Streamlit charts can include dimensions via the CanvasXpress constructor:

```python
cx = CanvasXpress(
    data=data,
    config={"graphType": "Bar"},
    width=800,
    height=600
)
graph(cx)
```

### Chart with Unique Identifier

```python
# For apps with multiple charts or when using st.cache_data
cx = CanvasXpress(
    render_to="my_unique_chart_id",
    data=df,
    config={"graphType": "Heatmap"}
)
graph(cx)
```

## Essential Streamlit Concepts for CanvasXpress Apps

### 1. Minimal Streamlit App

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

st.set_page_config(page_title="CanvasXpress App", page_icon="📊", layout="wide")

st.title("My Data Visualization App")

# Create chart
cx = CanvasXpress(
    data={
        "y": {"vars": ["A", "B", "C"], "smps": ["S1", "S2"], "data": [[1, 2], [3, 4], [5, 6]]}
    },
    config={"graphType": "Bar", "title": "Example Chart"}
)

# Render chart in Streamlit
graph(cx)
```

**Key documentation:** [Streamlit Quick Tutorial](https://docs.streamlit.io/get-started/tutorials/create-an-app)

### 2. Streamlit API Reference

When building Streamlit apps with CanvasXpress, you'll commonly use:

- `st.title()`, `st.header()`, `st.subheader()` - Page layout
- `st.sidebar` - Navigation and controls
- `st.selectbox()`, `st.multiselect()` - Data filtering options
- `st.slider()`, `st.number_input()` - Numeric inputs
- `st.checkbox()`, `st.radio()` - Boolean options
- `st.dataframe()` - Display pandas DataFrames
- `st.download_button()` - Export functionality
- `st.columns()` - Layout control

**Key documentation:** [Streamlit API Reference](https://docs.streamlit.io/develop/api-reference)

### 3. Streamlit Architecture (Critical for CanvasXpress)

**Streamlit reruns the entire script on every interaction.** This is the most important concept to understand:

- Every user interaction (button click, slider move, dropdown change) triggers a full script rerun from top to bottom
- State must be preserved using `st.session_state`
- Charts should be recreated on each run with updated parameters
- Use `@st.cache_data` or `@st.cache_resource` to cache expensive operations (data loading, heavy computations)

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

# Cache expensive data loading
@st.cache_data
def load_data():
    import pandas as pd
    return pd.read_csv("large_dataset.csv")

# Cache expensive computations
@st.cache_data
def compute_annotations(df):
    # ... heavy processing ...
    return annotations

# Main app
df = load_data()
annot = compute_annotations(df)

cx = CanvasXpress(data=df, sample_annotation=annot, config={"graphType": "Heatmap"})
graph(cx)
```

**Key documentation:** [Streamlit Architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture)

### 4. Data Persistence with Session State

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

if "selected_graph_type" not in st.session_state:
    st.session_state.selected_graph_type = "Scatter2D"

graph_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Scatter2D", "Heatmap", "Bar", "Line"],
    index=["Scatter2D", "Heatmap", "Bar", "Line"].index(st.session_state.selected_graph_type)
)
st.session_state.selected_graph_type = graph_type

cx = CanvasXpress(
    data=data,
    config={"graphType": st.session_state.selected_graph_type}
)
graph(cx)
```

### 5. Building a Complete Streamlit App with CanvasXpress

```python
import streamlit as st
import pandas as pd
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("Analytics Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
chart_type = st.sidebar.selectbox("Chart Type", ["Scatter2D", "Heatmap", "Bar", "Line"])
show_legend = st.sidebar.checkbox("Show Legend", value=True)

# Data loading with caching
@st.cache_data
def load_data():
    return pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [2, 3, 1, 5, 4]
    }, index=["S1", "S2", "S3", "S4", "S5"])

df = load_data()

# Main column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Create and render chart
    config = {
        "graphType": chart_type,
        "title": f"{chart_type} View",
        "showLegend": show_legend
    }
    cx = CanvasXpress(data=df, config=config)
    graph(cx, width=700, height=500)

with col2:
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Export options
    if st.button("Export JSON"):
        json_data = convert_to_reproducible_json(cx)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="chart_config.json",
            mime="application/json"
        )
```

### 6. Using Streamlit with Interactive Charts

Streamlit charts are embedded in the app and support CanvasXpress events:

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents

st.title("Interactive Chart")

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
```

### 7. Multiple Charts in Streamlit

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

st.title("Multiple Charts")

cx1 = CanvasXpress(
    render_to="chart_1",
    data=data1,
    config={"graphType": "Scatter2D", "title": "Chart 1"}
)
graph(cx1)

st.divider()

cx2 = CanvasXpress(
    render_to="chart_2",
    data=data2,
    config={"graphType": "Heatmap", "title": "Chart 2"}
)
graph(cx2)
```

### 8. Stateful Filters with CanvasXpress

```python
import streamlit as st
import pandas as pd
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

st.title("Filtered Dashboard")

@st.cache_data
def load_full_data():
    return pd.DataFrame(...)  # Load full dataset

full_df = load_full_data()

# Filter controls
min_value = st.sidebar.slider("Min Value", 0, 100, 20)
category = st.sidebar.multiselect("Categories", ["A", "B", "C", "D"])

# Filter data
filtered_df = full_df[full_df["value"] >= min_value]
if category:
    filtered_df = filtered_df[filtered_df["category"].isin(category)]

# Render filtered chart
if not filtered_df.empty:
    cx = CanvasXpress(
        data=filtered_df,
        config={"graphType": "Scatter2D", "title": f"Filtered Data ({len(filtered_df)} rows)"}
    )
    graph(cx)
else:
    st.warning("No data matches the current filters.")
```

## Streamlit Database Integration

For apps that load and visualize data from databases:

```python
import streamlit as st
import pandas as pd
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

@st.cache_data
def query_db(query: str) -> pd.DataFrame:
    # Use your preferred database connector
    import sqlite3
    conn = sqlite3.connect("data.db")
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Database Dashboard")

query = st.text_area("SQL Query", "SELECT * FROM measurements WHERE value > 50")

if st.button("Run Query"):
    df = query_db(query)
    st.dataframe(df)
    
    cx = CanvasXpress(data=df, config={"graphType": "Scatter2D"})
    graph(cx)
```

**Key documentation:** [Streamlit Databases Tutorial](https://docs.streamlit.io/develop/tutorials/databases)

## Testing Streamlit Apps with CanvasXpress

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

def test_chart():
    cx = CanvasXpress(
        data={"y": {"vars": ["A"], "smps": ["S1"], "data": [[1]]}},
        config={"graphType": "Bar"}
    )
    # Verify the chart object is created correctly
    assert cx is not None
    assert cx.config["graphType"] == "Bar"
```

Run with Streamlit's test utilities:

```bash
streamlit test your_app.py
```

**Key documentation:** [Streamlit App Testing](https://docs.streamlit.io/develop/concepts/app-testing/get-started)

## Common Streamlit + CanvasXpress Patterns

### Pattern 1: Tabbed Interface

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

tab1, tab2, tab3 = st.tabs(["Scatter", "Heatmap", "Bar"])

with tab1:
    plot(CanvasXpress(data=data1, config={"graphType": "Scatter2D"}))

with tab2:
    plot(CanvasXpress(data=data2, config={"graphType": "Heatmap"}))

with tab3:
    plot(CanvasXpress(data=data3, config={"graphType": "Bar"}))
```

### Pattern 2: Expandable Sections

```python
with st.expander("Advanced Options", expanded=False):
    color_scheme = st.selectbox("Color Scheme", ["CanvasXpress", "Viridis", "Plasma"])
    marker_size = st.slider("Marker Size", 1, 20, 10)
    
    cx = CanvasXpress(
        data=data,
        config={
            "graphType": "Scatter2D",
            "colorScheme": color_scheme,
            "objectSize": marker_size
        }
    )
    graph(cx)
```

### Pattern 3: Dynamic Chart Updates

```python
import streamlit as st
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress

if "update_count" not in st.session_state:
    st.session_state.update_count = 0

st.session_state.update_count += 1

st.write(f"Chart update #{st.session_state.update_count}")

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Line",
        "title": f"Live Data - Update {st.session_state.update_count}"
    }
)
graph(cx)
```

## Complete Streamlit App Template

```python
"""
CanvasXpress Streamlit Application Template
"""
import streamlit as st
import pandas as pd
from canvasxpress.streamlit import plot
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json

# Page configuration
st.set_page_config(
    page_title="CanvasXpress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better chart presentation
st.markdown("""
<style>
.st-emotion-cache-1v0mbdj {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Data Explorer", "Settings"]
)

# Cache data loading
@st.cache_data(ttl=3600)
def load_data():
    """Load and preprocess data."""
    df = pd.read_csv("data.csv")
    return df

@st.cache_data(ttl=3600)
def load_annotations():
    """Load sample annotations."""
    annot = pd.read_csv("annotations.csv", index_col=0)
    return annot

# Main content
def render_dashboard():
    """Render the main dashboard."""
    st.title("Data Visualization Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Filter controls
        chart_type = st.selectbox(
            "Chart Type",
            ["Scatter2D", "Heatmap", "Bar", "Line", "Boxplot"]
        )
        
        # Load data
        df = load_data()
        annot = load_annotations()
        
        # Create chart
        cx = CanvasXpress(
            data=df,
            sample_annotation=annot,
            config={
                "graphType": chart_type,
                "title": f"{chart_type} Analysis",
                "showLegend": True,
                "showSmpOverlaysLegend": True
            }
        )
        
        # Render chart
        graph(cx, width=800, height=600)
    
    with col2:
        st.subheader("Data Summary")
        st.metric("Total Samples", len(df.columns))
        st.metric("Total Variables", len(df.index))
        st.dataframe(annot)

# Run the app
if page == "Dashboard":
    render_dashboard()
elif page == "Data Explorer":
    st.title("Data Explorer")
    df = load_data()
    st.dataframe(df)
elif page == "Settings":
    st.title("Settings")
    st.write("Configuration options go here.")
```

## Key Takeaways

1. **Always install canvasxpress with the streamlit extra** (`pip install canvasxpress[streamlit]`) before running Streamlit apps
2. **Use `graph(cx)`** for rendering - it auto-detects the Streamlit environment
3. **Streamlit reruns the entire script** on every interaction - use caching wisely
4. **Use `st.session_state`** to preserve state across reruns
5. **Cache expensive operations** with `@st.cache_data` or `@st.cache_resource`
6. **Each chart needs a unique `render_to` ID** if displaying multiple charts
7. **CanvasXpress events work** within Streamlit apps for interactivity
8. **Use Streamlit layout components** (`columns`, `tabs`, `expander`) to organize charts
9. **Export functionality** is easy with `convert_to_reproducible_json()` and `st.download_button()`
10. **Test your app** using `streamlit test` for reliable deployments
