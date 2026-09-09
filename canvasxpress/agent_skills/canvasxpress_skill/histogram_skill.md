---
title: "Histogram Chart Skill"
description: "Generate CanvasXpress histograms using Scatter2D chart type with histogram overlays, configurable bins, stacked/staggered layouts, filled paths, and citation support."
---

# Histogram Chart Skill

## Overview
Histograms visualize data distribution with scatter plots and configurable histogram overlays. CanvasXpress implements histograms via Scatter2D with bin control (e.g., 5, 10, 20 bins), stacked or staggered layout types, filled histogram paths, density overlays, and metadata-driven annotations.

## Data Formats

### Single Variable with Organ Metadata
```python
data = {
  'y': {
    'data': [[124], [42], [25], [45], ...],
    'desc': ['days'],
    'smps': ['Survival'],
    'vars': ['s1', 's2', 's3', ...],
  },
  'z': {
    'Organ': ['Stomach', 'Stomach', 'Bronchus', ...],
  },
}
```

### Two Variable Comparison
```python
data = {
  'y': {
    'data': [[6.47, 4.03], [6.13, 3.76], ...],
    'smps': ['Alcohol', 'Tobacco'],
    'vars': ['North', 'Yorkshire', 'Northeast', ...],
  },
}
```

## Code Examples

### Example 1: Survival Data with 10 Bins
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[124], [42], [25], [45], [412], [51], [1112], ...],
    'desc': ['days'],
    'smps': ['Survival'],
    'vars': ['s1', 's2', 's3', ...],
  },
  'z': {
    'Organ': ['Stomach', 'Stomach', 'Bronchus', 'Colon', 'Ovary', 'Breast'],
  },
}
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'histogramBins': 10,
  'citation': 'Cameron, E. and Pauling, L. (1978). Proceedings of the National Academy of Science USA, 75.',
  'xAxis': ['Survival'],
  'xAxisTitle': 'Survival (days)',
  'yAxisTitle': 'Number of Subjects',
  'axisTitleFontStyle': 'italic',
  'title': 'Patients with advanced cancers of the stomach,\\nbronchus, colon, ovary or breast treated with ascorbate.',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: 20 Bins
```python
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'histogramBins': 20,
  'citation': 'Cameron, E. and Pauling, L. (1978). Proceedings of the National Academy of Science USA, 75.',
  'xAxis': ['Survival'],
  'xAxisTitle': 'Survival (days)',
  'yAxisTitle': 'Number of Subjects',
  'title': 'Patients with advanced cancers...',
}
```

### Example 3: Filled Histogram with Hidden Base
```python
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'hideHistogram': True,
  'showFilledHistogramPath': True,
  'showHistogramPath': True,
  'histogramBins': 20,
  'xAxis': ['Survival'],
  'xAxisTitle': 'Survival (days)',
  'yAxisTitle': 'Number of Subjects',
}
```

### Example 4: Tobacco vs Alcohol with Staggered Histograms
```python
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'histogramBins': 5,
  'histogramType': 'staggered',
  'citation': 'Moore, David S., and George P. McCabe (1989). Introduction to the Practice of Statistics, p. 179.',
  'xAxis': ['Tobacco', 'Alcohol'],
  'xAxisTitle': 'Pounds Spent',
  'yAxisTitle': 'Frequency',
  'title': 'Average weekly household spending, in British pounds, on tobacco products\\nand alcoholic beverages for each of the 11 regions of Great Britain.',
}
```

### Example 5: Stacked Histograms
```python
config = {
  'graphType': 'Scatter2D',
  'showHistogram': True,
  'histogramBins': 5,
  'histogramType': 'stacked',
  'citation': 'Moore, David S., and George P. McCabe (1989). Introduction to the Practice of Statistics, p. 179.',
  'xAxis': ['Tobacco', 'Alcohol'],
  'xAxisTitle': 'Pounds Spent',
  'yAxisTitle': 'Frequency',
  'title': 'Average weekly household spending...',
}
```

## Agent Prompts

- "Create a CanvasXpress scatter plot with histogram showing survival days data with 10 bins."
- "Generate a histogram with 20 bins for cancer patient survival data."
- "Build a histogram with filled path and hidden base for smooth distribution visualization."
- "Create a staggered histogram comparing tobacco and alcohol spending across regions."
- "Generate a stacked histogram for two variables with 5 bins."
- "Build a histogram with italic axis titles and citation in cancer survival data."
- "Create a scatter plot with histogram overlay showing frequency distribution."
- "Generate a histogram with filled path enabled for continuous distribution display."
- "Build a histogram with staggered layout for comparative data."
- "Create a histogram with citation referencing Cameron and Pauling (1978)."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "histogram" | `showHistogram: True` | Shows histogram overlay |
| "10 bins" | `histogramBins: 10` | Sets bin count |
| "20 bins" | `histogramBins: 20` | Sets bin count |
| "5 bins" | `histogramBins: 5` | Sets bin count |
| "staggered" | `histogramType: 'staggered'` | Staggered layout |
| "stacked" | `histogramType: 'stacked'` | Stacked layout |
| "filled path" | `showFilledHistogramPath: True` | Fills histogram area |
| "histogram path" | `showHistogramPath: True` | Shows histogram border |
| "hide histogram" | `hideHistogram: True` | Hides base histogram |
| "citation" | `citation: 'Author (Year). Title.'` | Adds citation |
| "italic title" | `axisTitleFontStyle: 'italic'` | Italicizes axis titles |
| "x-axis" | `xAxis: ['ColumnName']` | Sets x-axis column |
| "x-axis title" | `xAxisTitle: 'Label'` | Sets x-axis label |
| "y-axis title" | `yAxisTitle: 'Label'` | Sets y-axis label |

## Key Configuration Parameters

- `graphType`: Always `'Scatter2D'` for histograms
- `showHistogram`: Boolean to show histogram overlay
- `hideHistogram`: Boolean to hide base histogram
- `histogramBins`: Integer for number of bins (e.g., 5, 10, 20)
- `histogramType`: `'staggered'` or `'stacked'` for layout
- `showFilledHistogramPath`: Boolean to fill histogram area
- `showHistogramPath`: Boolean to show histogram border
- `citation`: String for study reference
- `axisTitleFontStyle`: `'italic'` for italicized titles
- `xAxis`: Array of x-axis column names
- `xAxisTitle`: X-axis label
- `yAxisTitle`: Y-axis label
- `title`: Chart title (use `\\n` for line breaks)
