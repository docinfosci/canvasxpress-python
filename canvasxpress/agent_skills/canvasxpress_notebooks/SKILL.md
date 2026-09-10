---
name: canvasxpress_notebooks
description: Create Jupyter notebooks (.ipynb) with CanvasXpress charts. Uses jupytext for MyST markdown to notebook conversion. Generates notebooks with proper cell structure for chart visualization.
category: data-visualization
tools:
  - python
  - jupyter
  - jupytext
---

## CRITICAL: Load canvasxpress_charts Skill First

**BEFORE writing any CanvasXpress code, you MUST load the `canvasxpress_charts` skill.**

This skill provides the authoritative reference for:
- Correct import statements for all CanvasXpress classes
- Chart type mappings and configuration patterns
- Event handling with `CXEvent` and `CXEvents`
- Framework-specific rendering (Jupyter, Dash, Shiny, etc.)

Without loading `canvasxpress_charts`, you risk generating incorrect code that uses wrong imports, invalid patterns, or non-existent classes.

**Required workflow:**
1. **Load `canvasxpress_charts` skill** - Access authoritative CanvasXpress patterns
2. **Determine chart type** - Load specific chart sub-skill if needed (bar_skill.md, heatmap_skill.md, etc.)
3. **Load `events_skill.md`** if user requests interactive events
4. **Generate code** using patterns from loaded skills
5. **Convert to notebook** using the workflow below

## Workflow

### 1. Plan the Notebook Structure

Determine the cells needed for the notebook:
1. **Title cell** - Markdown heading with chart/notebook name
2. **Description cell** - What the chart visualizes
3. **Import cell** - CanvasXpress imports
4. **Data cell** - DataFrame creation with data
5. **Config cell** - CanvasXpress object configuration
6. **Render cell** - Chart rendering with `graph(cx)`

### 2. Write MyST Markdown File

Create a `.md` file using MyST markdown format with appropriate cell markers:

```python
# Chart Title

## Description
Brief description of what this chart shows.

## Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
```

## Data

```python
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 25, 15, 30]
})
```

## Configuration

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        "title": "Chart Title",
        "xAxisTitle": "Category",
        "yAxisTitle": "Values"
    }
)
```

## Render

```python
graph(cx)
```
```

### 3. Convert to Notebook with Jupytext

```bash
jupytext --from myst --to notebook notebook.md
```

This generates `notebook.ipynb` with proper cell types:
- Markdown cells for titles and descriptions
- Code cells for Python code
- Proper kernel metadata

### 4. Verify the Notebook

Check the notebook has correct cells:
- Markdown cells for title, description, and user prompt
- Code cells for imports, data, config, and rendering
- Kernel metadata references the project's Python environment

## Notebook Structure Guidelines

### Markdown Cells
- Use `#` for notebook title
- Use `##` for section headers
- Include user prompts in a dedicated markdown cell
- Keep descriptions concise and informative

### Code Cells

**Imports Cell:**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
```

**Data Cell:**
- Create DataFrames with explicit column names
- Use Black formatting (trailing commas, proper indentation)
- Include data source comments when applicable

**Config Cell:**
```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        "title": "Chart Title",
        "xAxisTitle": "X Axis Label",
        "yAxisTitle": "Y Axis Label",
        "showLegend": True
    },
    width=800,
    height=600
)
```

**Render Cell:**
```python
graph(cx)
```

## Best Practices

1. **Load canvasxpress_charts first** - Always load the canvasxpress_charts skill before generating any code
2. **Black Formatting:** Use trailing commas, proper indentation, and wrapped lines for long lists
3. **Explicit Dimensions:** Always set `width` and `height` in CanvasXpress config
4. **Descriptive Titles:** Include meaningful chart titles and axis labels
5. **Legend Settings:** Set `showLegend=True` when there are multiple series/groups
6. **Cell Order:** Maintain logical flow: imports → data → config → render
7. **Markdown Context:** Provide sufficient context in markdown cells for users to understand the chart purpose

## Example Notebook Creation

### From Scratch
Create a complete notebook with a bar chart:

```python
# Sales Data Visualization

## Overview
This notebook visualizes monthly sales data using a CanvasXpress bar chart.

## Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd
```

## Data

```python
sales_df = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': [120, 150, 180, 200, 250]
})
```

## Configuration

```python
cx = CanvasXpress(
    data=sales_df,
    config={
        "graphType": "Bar",
        "title": "Monthly Sales",
        "xAxisTitle": "Month",
        "yAxisTitle": "Sales ($)",
        "showLegend": False
    },
    width=800,
    height=600
)
```

## Render

```python
graph(cx)
```
```

### From Existing DataFrame
When user has existing data:

```python
# Existing DataFrame Visualization

## Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
```

## Data (existing df variable)

# Use the existing pandas DataFrame 'df' already in context

## Configuration

```python
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Heatmap",
        "title": "Data Heatmap",
        "showSmpOverlaysLegend": True
    }
)
```

## Render

```python
graph(cx)
```
```

## Jupytext Workflow

### Installation
```bash
pip install jupytext
```

### Convert MyST to Notebook
```bash
jupytext --from myst --to notebook input.md
```

### Convert Notebook to MyST (for editing)
```bash
jupytext --to myst notebook.ipynb
```

### Pair Notebook with Markdown (auto-sync)
```bash
jupytext --set-formats ipynb,myst notebook.ipynb
```

## User Prompt Integration

Users can provide natural language prompts describing their visualization needs. Convert these prompts into appropriate CanvasXpress code:

1. **Understand the request:** What chart type? What data? What styling?
2. **Create DataFrame:** Structure data appropriately for CanvasXpress
3. **Configure chart:** Set graphType, title, axis labels, dimensions
4. **Render:** Call `graph(cx)` to display

Example prompt conversion:
- **User:** "Show me sales by month with a bar chart"
- **Agent:** Creates DataFrame with Month/Sales columns, configures Bar chart, adds axis labels

<small>Note that canvasxpress-python must be installed for this skill to work as it provides the necessary CanvasXpress functionality.</small>
