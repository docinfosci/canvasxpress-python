---
title: "Bar Chart Skill"
description: "Generate CanvasXpress bar charts with vertical/horizontal orientation, grouped data, annotations, and decorative elements."
---

# Bar Chart Skill

## Overview
Bar charts display categorical data with rectangular bars proportional to the values they represent. CanvasXpress supports single/multiple series, horizontal/vertical orientation, data value labels, sample overlays, color grouping, and decorative reference lines.

## Data Formats

### Wide Format (Series as Variables)
```python
data = {
  'y': {
    'data': [
      [4, 5, 4, 4, 7],
      [3, 6, 5, 5, 6],
    ],
    'smps': ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5'],
    'vars': ['Var 1', 'Var 2'],
  },
}
```

### Long Format with Metadata
```python
data = {
  'x': {
    'Species': ['setosa']*50 + ['versicolor']*50 + ['virginica']*50,
  },
  'y': {
    'data': [
      [5.1, 4.9, 4.7, ...],  # Sepal.Length
      [3.5, 3.0, 3.2, ...],  # Sepal.Width
      [1.4, 1.4, 1.3, ...],  # Petal.Length
      [0.2, 0.2, 0.3, ...],  # Petal.Width
    ],
    'smps': ['s1', 's2', ..., 's150'],
    'vars': ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'],
  },
}
```

## Code Examples

### Example 1: Single Series Vertical Bar Chart
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[4, 5, 4, 4, 7]],
    'smps': ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5'],
    'vars': ['Var 1'],
  },
}
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'Categories',
  'title': 'Bar graph with a single series',
  'xAxis': ['Var 1'],
  'xAxisTitle': 'Var 1',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Horizontal Bar Chart with Data Values Inside Bars
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'horizontal',
  'showDataValues': True,
  'dataValuesPosition': 'inside',
  'dataTextColor': '#FFFFFF',
  'smpTextRotate': 90,
  'smpTitle': 'Categories',
  'title': 'Bar graph showing data values',
  'xAxis': ['Var 1', 'Var 2'],
  'xAxisTitle': 'Value',
}
```

### Example 3: Multi-Series Vertical Bar Chart
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'smpTextRotate': 90,
  'smpTitle': 'Categories',
  'legendColumns': 3,
  'legendPosition': 'bottom',
  'title': 'Bar graph with multiple series',
  'xAxis': ['Var 1', 'Var 2', 'Var 3'],
  'xAxisTitle': 'Value',
}
```

### Example 4: Grouped Bar Chart by Metadata (Species)
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'groupingFactors': ['Species'],
  'showDataValues': True,
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'smpTextRotate': 90,
  'smpTitle': 'Species',
  'title': 'Iris flower data set',
  'xAxis': ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'],
}
```

### Example 5: Bar Chart with Decorative Reference Line
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'colorBy': 'Drug Sensitivity',
  'smpTextRotate': 90,
  'smpTitle': 'Cell Lines',
  'title': 'Sensitivity of cell lines to different drugs',
  'xAxis': ['V1'],
  'decorations': {
    'line': [
      {
        'align': 'left',
        'color': 'rgb(255,0,0)',
        'label': 'Cutoff',
        'value': 50,
        'width': 2,
      },
    ],
  },
}
```

### Example 6: Bar Chart with Sample Overlays and IC50 Coloring
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'colorBy': 'IC50',
  'smpOverlays': ['Drug Sensitivity'],
  'smpTextRotate': 90,
  'smpTitle': 'Cell Lines',
  'title': 'Sensitivity of cell lines to different drugs',
  'xAxis': ['V1'],
  'decorations': {
    'line': [
      {
        'align': 'left',
        'color': 'rgb(255,0,0)',
        'label': 'Cutoff',
        'value': 50,
        'width': 2,
      },
    ],
  },
}
```

### Example 7: Horizontal Bar Chart with Citation
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'horizontal',
  'showDataValues': True,
  'dataValuesPosition': 'inside',
  'dataTextColor': '#FFFFFF',
  'dataTextScaleFontFactor': 0.8,
  'showLegend': False,
  'maxSmpStringLen': 50,
  'citation': '<b>Data source</b> : IHME, Global Burden of Disease (2024)',
  'citationScaleFontFactor': 0.7,
  'subtitle': 'Estimated number of deaths from different types of cancer per 100,000 people.',
  'subtitleScaleFontFactor': 0.6,
  'title': 'Cancer crude death rate by type, World, 2021',
  'xAxis': ['Number of Deaths per 100000 people'],
  'xAxisShow': False,
  'xAxisGridMajorShow': False,
}
```

### Example 8: Workflow Bar Chart (Temporal Animation)
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'horizontal',
  'workflowBy': 'Year',
  'showDataValues': True,
  'showLegend': False,
  'maxSmpStringLen': 50,
  'dataTextScaleFontFactor': 0.7,
  'citation': '<b>Data source</b> : WHO Mortality Database (2024)',
  'citationScaleFontFactor': 0.7,
  'subtitle': 'The reported annual death rate from malignant cancers...',
  'subtitleScaleFontFactor': 0.6,
  'title': 'Cancer death rate by age group, United States',
  'xAxisShow': False,
  'xAxisGridMajorShow': False,
}
```

### Example 9: Plot by Variable (Wide Format Layout)
```python
config = {
  'graphType': 'Bar',
  'graphOrientation': 'vertical',
  'plotByVariable': True,
  'smpTextRotate': 90,
  'smpLabelInterval': 2,
  'smpTitle': 'Samples',
  'title': 'Data Organized by variables',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
}
```

## Agent Prompts

- "Create a CanvasXpress vertical bar chart showing Var 1 values for categories Cat 1 through Cat 5."
- "Generate a horizontal bar chart comparing two variables (Var 1 and Var 2) across five categories with data values displayed inside the bars."
- "Build a multi-series bar chart with three variables across five categories, legend with 3 columns at the bottom."
- "Create an Iris flower bar chart grouped by species showing sepal and petal measurements."
- "Generate a bar chart with a decorative cutoff reference line at value 50, coloring bars by drug sensitivity."
- "Make a horizontal bar chart showing cancer death rates by type with citation and data values inside bars."
- "Create a temporal bar chart with workflow animation by year showing cancer death rates across age groups."
- "Build a bar chart that plots by variable instead of sample, organizing data across V1-V4."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "bar chart" | `graphType: 'Bar'` | Sets the chart type to bar |
| "vertical" | `graphOrientation: 'vertical'` | Default, bars go up |
| "horizontal" | `graphOrientation: 'horizontal'` | Bars go left-to-right |
| "show values" / "data labels" | `showDataValues: True` | Displays numerical values |
| "inside bars" | `dataValuesPosition: 'inside'` | Positions labels inside bars |
| "white text" | `dataTextColor: '#FFFFFF'` | Sets text color for data values |
| "group by [column]" | `groupingFactors: ['ColumnName']` | Groups bars by metadata column |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors bars by metadata values |
| "reference line" / "cutoff" | `decorations.line: [{value, label, color, align}]` | Adds decorative lines |
| "sample overlay" | `smpOverlays: ['ColumnName']` | Adds metadata overlay to samples |
| "legend columns" | `legendColumns: N` | Sets number of legend columns |
| "legend at bottom" | `legendPosition: 'bottom'` | Positions legend below chart |
| "rotate labels" | `smpTextRotate: 90` | Rotates category/sample labels |
| "max label length" | `maxSmpStringLen: 50` | Limits sample string length |
| "plot by variable" | `plotByVariable: True` | Flips layout to plot by variables |
| "animation" / "temporal" | `workflowBy: 'ColumnName'` | Enables temporal workflow animation |
| "hide x-axis" | `xAxisShow: False` | Hides x-axis line and labels |
| "citation" | `citation: 'Source info'` | Adds data source attribution |
| "subtitle" | `subtitle: 'Text'` | Adds chart subtitle |

## Key Configuration Parameters

- `graphType`: Always `'Bar'` for bar charts
- `graphOrientation`: `'vertical'` (default) or `'horizontal'`
- `showDataValues`: Boolean to show/hide numerical labels on bars
- `dataValuesPosition`: `'inside'` or `'outside'` for label positioning
- `dataTextColor`: Hex color for data value text (e.g., `'#FFFFFF'`)
- `groupingFactors`: Array of metadata column names for grouping bars
- `colorBy`: Metadata column name for coloring bars
- `smpOverlays`: Array of metadata columns for sample overlays
- `decorations`: Object containing reference lines, labels, and styling
- `workflowBy`: Metadata column name for temporal animation workflow
- `plotByVariable`: Boolean to flip chart layout from sample-based to variable-based
- `smpTextRotate`: Angle in degrees to rotate sample/axis labels
- `maxSmpStringLen`: Maximum length for sample labels before truncation
