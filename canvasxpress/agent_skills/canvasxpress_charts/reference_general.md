---
title: "General Reference"
description: "CanvasXpress data handling, DataFrame-to-XYZ conversion, production config patterns, and common examples."
---

# General Reference

## Data Handling Patterns

### Pattern 1: Existing DataFrame in context

```python
cx = CanvasXpress(
    data=df,
    sample_annotation=annot_df,
    variable_annotation=var_df,
    config={"graphType": "Heatmap"}
)
graph(cx)
```

### Pattern 2: XYZ dict from user

```python
cx = CanvasXpress(
    data={
        "y": {"vars": ["A", "B"], "smps": ["S1", "S2", "S3"], "data": [[1,2,3], [4,5,6]]},
        "x": {"Group": ["Control", "Control", "Treatment"]},
        "z": {"A": {"Pathway": "P1"}, "B": {"Pathway": "P2"}}
    },
    config={"graphType": "Scatter2D"}
)
graph(cx)
```

### Pattern 3: Fabricated sample data (when user has no data)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["GeneA", "GeneB", "GeneC"],
    index=[f"Smp{i}" for i in range(1, 51)]
)
```

### Pattern 4: URL/CSV loading

```python
import requests, io, pandas as pd
df = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))
```

### Pattern 5: Loading data and annotations from URLs

```python
import requests, io, pandas as pd

# Load main data
data_url = "https://www.canvasxpress.org/data/r/cX-generic-dat.txt"
data_df = pd.read_csv(
    io.StringIO(requests.get(data_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

# Load sample annotations
sample_annot_url = "https://www.canvasxpress.org/data/r/cX-generic-smp.txt"
sample_annot_df = pd.read_csv(
    io.StringIO(requests.get(sample_annot_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

# Load variable annotations
variable_annot_url = "https://www.canvasxpress.org/data/r/cX-generic-var.txt"
variable_annot_df = pd.read_csv(
    io.StringIO(requests.get(variable_annot_url).content.decode('utf-8')),
    sep="\t",
    index_col=0
)

cx = CanvasXpress(
    data=data_df,
    sample_annotation=sample_annot_df,
    variable_annotation=variable_annot_df,
    config={"graphType": "Dotplot"}
)
graph(cx)
```

## Production-Ready Config Patterns

Every generated chart should include production-quality configuration:

```python
config = {
    "graphType": "Bar",
    "title": "Chart Title",
    "subtitle": "Optional subtitle",
    "xAxisTitle": "X Axis Label",
    "yAxisTitle": "Y Axis Label",
    "colorScheme": "CanvasXpress",
    "theme": "CanvasXpress",
    "showLegend": True,
    "showLegendBorder": True,
    "graphOrientation": "vertical",
    "background": "rgb(255,255,255)",
}
```

Common additions by chart type:

```python
# Scatter-specific
"objectShape": "circle",
"objectColor": "rgb(69,117,180)",
"regressionLine": True,

# Heatmap-specific
"heatMapping": "color",
"sortSmpByTree": True,
"sortVarByTree": True,

# Bar/Stacked-specific
"objectBorderColor": "rgb(0,0,0)",
"objectBorderThickness": 1,

# Network-specific
"nodeLabelSize": 10,
"ringGraphWeight": [25, 25, 25, 25],

# Sample overlays (for advanced metadata visualization)
"smpOverlayProperties": {
    "Factor1": {
        "type": "Default",
        "color": "rgb(10,176,219)",
        "spectrum": ["rgb(69,117,180)", "rgb(145,191,219)"],
        "scheme": "CanvasXpress",
        "showLegend": True
    }
},

# Line chart specific
"lineType": "spline",
"llmHeader": [["V1", "V2", "V3", "V4"]],
```

## DataFrame-to-XYZ Conversion

### Core Conversion Function

```python
def dataframe_to_xyz(
    df: pd.DataFrame,
    sample_annotation: pd.DataFrame = None,
    variable_annotation: pd.DataFrame = None,
) -> dict:
    """
    Converts a DataFrame into a CanvasXpress XYZ dict.
    
    Parameters:
        df: Main data DataFrame (index=vars, columns=smps)
        sample_annotation: Optional annotation DataFrame (per-sample metadata -> x)
        variable_annotation: Optional annotation DataFrame (per-variable metadata -> z)
    
    Returns:
        dict with structure: {
            "y": {"data": [...], "vars": [...], "smps": [...]},
            "x": {...},  # optional
            "z": {...}   # optional
        }
    """
    xyz = {
        "y": {
            "data": df.values.tolist(),
            "vars": df.index.tolist(),
            "smps": df.columns.tolist()
        }
    }
    
    if sample_annotation is not None:
        xyz["x"] = _convert_annotation_to_x(sample_annotation, xyz["y"]["smps"])
    
    if variable_annotation is not None:
        xyz["z"] = _convert_annotation_to_z(variable_annotation, xyz["y"]["vars"])
    
    return xyz
```

### User Workflow: Inspect -> Modify -> Use

```python
# Step 1: Convert DataFrame to XYZ
xyz = dataframe_to_xyz(df, sample_annotation=annot_df)

# Step 2: Inspect the structure
print(f"Samples: {xyz['y']['smps']}")
print(f"Variables: {xyz['y']['vars']}")
print(f"X annotations: {list(xyz['x'].keys())}")

# Step 3: Enhance with additional metadata
xyz["x"]["NewFactor"] = ["Group1", "Group1", "Group2", "Group2"]
xyz["x"]["Condition"] = ["A", "B", "A", "B"]

# Step 4: Use in CanvasXpress
cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Heatmap",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["NewFactor", "Condition"]
    }
)
graph(cx)
```

## Advanced Data Wrangling

CanvasXpress supports in-browser data manipulation via configuration parameters and after-render function calls.

### Grouping Data

Group data points by a metadata factor (e.g., show all males together in a boxplot):

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Boxplot",
        "groupingFactors": ["Gender"]  # Group by this metadata field
    }
)
graph(cx)
```

### Faceting (Segregation)

Split the chart into sub-plots by a metadata factor:

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        "segregateSamplesBy": ["Excercise"]  # Creates sub-plots for Low/Moderate/Intense
    }
)
graph(cx)
```

### Sorting Data

Sort samples or variables by a specific field:

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        # sortData: [['var'|'cat', 'smp'|'var', 'fieldName']]
        "sortData": [["var", "smp", "Age"]]   # Sort samples by Age
        # "sortData": [["cat", "smp", "Height"]]  # Sort by category Height
    }
)
graph(cx)
```

### Clustering Data

Hierarchical clustering with dendrograms:

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Heatmap",
        "samplesClustered": True,    # Cluster samples (columns)
        "variablesClustered": True,  # Cluster variables (rows)
        "sortSmpByTree": True,       # Order samples by cluster tree
        "sortVarByTree": True        # Order variables by cluster tree
    }
)
graph(cx)
```

### Transposing Data

Swap rows and columns:

```python
# Via configuration
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        "transposeData": True
    }
)
graph(cx)

# Or after rendering
# cx.transpose()
```

### Transforming Data

Apply transformations like log-scale:

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Heatmap",
        # Data transforms happen automatically in the browser
        # Use log scale via yAxisScale / xAxisScale if needed
        "yAxisScale": "log"
    }
)
graph(cx)
```

### Pivoting Data

Pivot metadata fields into axes via after-render function:

```python
cx = CanvasXpress(
    data=df,
    config={"graphType": "Bar"},
    # afterRender parameter applies functions after initial draw
    after_render=[
        ["pivotX", ["Gender"]]  # Pivot by Gender metadata
    ]
)
graph(cx)
```

### Correlation / Regression

Add regression lines after rendering:

```python
cx = CanvasXpress(
    data=df,
    config={"graphType": "Scatter2D"},
    after_render=[
        ["createRegression", [True, "Hip"]]  # Enable regression, correlate with Hip
    ]
)
graph(cx)
```

## Specialized Data Formats

### Venn Diagram Data

Two formats supported:

```python
# Format 1: 2D array (simple, fewer sets)
venn_data = [
    ["Id", "Value"],
    ["A", 340], ["B", 562], ["C", 620],
    ["AB", 639], ["AC", 456], ["BC", 915],
    ["ABC", 552]
]

cx = CanvasXpress(
    data={"y": venn_data},
    config={"graphType": "Venn"}
)

# Format 2: JSON object with legend (custom set names)
venn_data = {
    "venn": {
        "data": {
            "A": 340, "B": 562, "C": 620,
            "AB": 639, "AC": 456, "BC": 915,
            "ABC": 552
        },
        "legend": {
            "A": "List1", "B": "List2", "C": "List3"
        }
    }
}

cx = CanvasXpress(
    data=venn_data,
    config={"graphType": "Venn"}
)
```

### Network Data

```python
network_data = {
    "nodes": [
        {"id": "Node1", "color": "red"},
        {"id": "Node2", "color": "green"},
        {"id": "Node3", "color": "blue"}
    ],
    "edges": [
        {"id1": "Node1", "id2": "Node2", "color": "yellow"},
        {"id1": "Node2", "id2": "Node3", "color": "orange"}
    ]
}

cx = CanvasXpress(
    data=network_data,
    config={"graphType": "Network"}
)
```

### Simple 2D Array Format

Quick prototyping with minimal metadata:

```python
simple_data = [
    ["Variable", "Sample1", "Sample2", "Sample3"],
    ["Gene1", 10, 20, 30],
    ["Gene2", 35, 25, 15]
]

cx = CanvasXpress(
    data={"y": simple_data},
    config={"graphType": "Heatmap"}
)
```

### Long-Form Data for Scatter Plots

CanvasXpress prefers "short and wide" format for categorical comparisons (Bar, Boxplot) but "long and skinny" format when comparing two numerical columns (Scatter):

```python
# Long-form: each row = one observation with both X and Y coordinates
df_long = pd.DataFrame({
    "Height": [174, 161, 194, 160, 173, 151],
    "Weight": [65.6, 51.6, 80.7, 49.2, 55.2, 48.7],
    "Name": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"]
})

# Convert to XYZ for Scatter2D
xyz = {
    "y": {
        "vars": ["Weight"],  # One variable for Y
        "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
        "data": [[65.6], [51.6], [80.7], [49.2], [55.2], [48.7]]
    },
    "x": {
        "Height": [174, 161, 194, 160, 173, 151]  # X from annotation
    }
}

cx = CanvasXpress(
    data=xyz,
    config={
        "graphType": "Scatter2D",
        "xAxisTitle": "Height",
        "yAxisTitle": "Weight"
    }
)
graph(cx)
```

## Known Limitations

1. **3D charts:** Plotly 3D and Matplotlib 3D require careful data reshaping; CanvasXpress Scatter3D is supported but complex geometries may not map perfectly
2. **Custom shapes:** Plotly `go.Scatter` with custom fill areas may not have exact CanvasXpress equivalents
3. **Dual axes:** Plotly's dual y-axis has limited CanvasXpress equivalent
4. **Faceted/colored plots:** Plotly `facet_row`/`facet_col` requires manual handling in CanvasXpress
5. **Time series with complex formatting:** Date formatting requires CanvasXpress `xAxisTickFormat`
6. **Word clouds:** Matplotlib has no native word cloud; requires external library
7. **Geographic maps:** CanvasXpress Map requires GeoJSON input, not direct lat/lon scatter

## Example Interactions

### Example 1: Create a simple bar chart

**User:** "Create a bar chart showing sales data"

**Agent:** Provides complete code:
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

# Sales data
data = {
    "y": {
        "vars": ["Sales"],
        "smps": ["Jan", "Feb", "Mar", "Apr", "May"],
        "data": [[120, 150, 180, 200, 250]]
    }
}

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Bar",
        "title": "Monthly Sales",
        "xAxisTitle": "Month",
        "yAxisTitle": "Sales ($)",
        "showLegend": False
    }
)
graph(cx)
```

### Example 2: Convert existing Plotly code

**User:** "Convert this Plotly code to CanvasXpress"
```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30]))
```

**Agent:** Provides converted code:
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
    "y": {
        "vars": ["Series1"],
        "smps": ["A", "B", "C"],
        "data": [[10, 20, 30]]
    }
}

cx = CanvasXpress(
    data=data,
    config={
        "graphType": "Bar",
        "title": "My Chart"
    }
)
graph(cx)
```

### Example 3: DataFrame with annotations

**User:** "I have a pandas DataFrame with gene expression data. Create a heatmap with sample annotations."

**Agent:** Provides complete code:
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

# Sample expression data
df = pd.DataFrame(
    {'GeneA': [1.2, 3.4, 0.5], 'GeneB': [2.1, 1.8, 4.2], 'GeneC': [0.3, 2.7, 1.9]},
    index=['Sample1', 'Sample2', 'Sample3']
)

# Sample annotations
annot = pd.DataFrame({
    'Treatment': ['Control', 'Treatment', 'Control'],
    'Batch': ['A', 'A', 'B']
}, index=['Sample1', 'Sample2', 'Sample3'])

cx = CanvasXpress(
    data=df,
    sample_annotation=annot,
    config={
        "graphType": "Heatmap",
        "title": "Gene Expression Heatmap",
        "showSmpOverlaysLegend": True,
        "smpOverlays": ["Treatment", "Batch"]
    }
)
graph(cx)
```
