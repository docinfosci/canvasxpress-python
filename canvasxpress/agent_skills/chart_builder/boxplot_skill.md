---
title: "Boxplot Skill"
description: "Generate CanvasXpress boxplots with notched boxes, mean markers, outlier detection, jittered data points, and sample overlays."
---

# Boxplot Skill

## Overview
Boxplots display the distribution of data through quartiles, medians, and outliers. CanvasXpress supports notched boxes, mean markers, customizable whiskers, outlier detection ratios, jittered data points, and sample overlays for enhanced statistical visualization.

## Data Formats

### Long Format with Metadata
```python
data = {
  'x': {
    'dose': ['0.5']*30 + ['1']*30 + ['2']*30,
    'order': list(range(1, 11))*3,
    'supp': ['VC']*30 + ['OJ']*30,
  },
  'y': {
    'data': [
      [4.2, 11.5, 7.3, ..., 29.5],  # Tooth length measurements
    ],
    'smps': ['Var1', 'Var2', ..., 'Var60'],
    'vars': ['len'],
  },
}
```

## Code Examples

### Example 1: Basic Vertical Boxplot
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'dose': ['0.5']*30 + ['1']*30 + ['2']*30,
    'order': list(range(1, 11))*3,
    'supp': ['VC']*30 + ['OJ']*30,
  },
  'y': {
    'data': [[4.2, 11.5, 7.3, 5.8, 6.4, 10, 11.2, 11.2, 5.2, 7,
              16.5, 16.5, 15.2, 17.3, 22.5, 17.3, 13.6, 14.5, 18.8, 15.5,
              23.6, 18.5, 33.9, 25.5, 26.4, 32.5, 26.7, 21.5, 23.3, 29.5,
              15.2, 21.5, 17.6, 9.7, 14.5, 10, 8.2, 9.4, 16.5, 9.7,
              19.7, 23.3, 23.6, 26.4, 20, 25.2, 25.8, 21.2, 14.5, 27.3,
              25.5, 26.4, 22.4, 24.5, 24.8, 30.9, 26.4, 27.3, 29.4, 23]],
    'smps': [f'Var{i}' for i in range(1, 61)],
    'vars': ['len'],
  },
}
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Horizontal Boxplot with Transparency
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'horizontal',
  'groupingFactors': ['dose'],
  'objectColorTransparency': 0.5,
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 3: Notched Boxplot with Single Whiskers
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'boxplotNotched': True,
  'boxplotWhiskersType': 'single',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxisGridMinorShow': False,
}
```

### Example 4: Segregated Boxplots with Outlier Control
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'boxplotNotched': True,
  'boxplotWhiskersType': 'single',
  'boxplotOutliersRatio': 3,
  'segregateSamplesBy': ['dose'],
  'layoutTopology': '1X3',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 5: Boxplot with Mean Markers
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'boxplotMean': True,
  'boxplotMeanColor': 'rgb(255,215,0)',
  'boxplotMeanColorBorder': 'red',
  'boxplotNotched': True,
  'boxplotWhiskersType': 'single',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 6: Custom Median Styling
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'boxplotMedianColor': 'red',
  'boxplotMedianWidth': 5,
  'boxplotNotched': True,
  'boxplotWhiskersType': 'single',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 7: Fivenum Hinge Function
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'boxplotHingeFunction': 'fivenum',
  'boxplotNotched': True,
  'boxplotWhiskersType': 'single',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 8: Boxplot with Original Data Points (Jitter)
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showBoxplotOriginalData': True,
  'jitter': True,
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
}
```

### Example 9: Colored Boxplot with Shapes and Legend
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'colorBy': 'dose',
  'colorScheme': 'GGPlot',
  'shapeBy': 'supp',
  'showBoxplotOriginalData': True,
  'jitter': True,
  'showLegend': True,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'axisTitleFontStyle': 'bold',
  'axisAlgorithm': 'rPretty',
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'stringSampleFactors': ['dose'],
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
  'xAxis2Show': False,
  'xAxisGridMajorColor': 'white',
  'xAxisGridMinorShow': False,
}
```

## Agent Prompts

- "Create a CanvasXpress vertical boxplot showing tooth length distribution across three vitamin C doses (0.5, 1, 2)."
- "Generate a horizontal boxplot with semi-transparent boxes showing dose effects on tooth growth."
- "Build a notched boxplot with single whiskers to show statistical significance between dose groups."
- "Create segregated boxplots (one per dose) with outlier detection ratio of 3."
- "Generate a boxplot with gold mean markers (rgb(255,215,0)) with red borders."
- "Make a boxplot with custom red median line (width 5) and notched boxes."
- "Create a boxplot showing original data points with jitter overlay."
- "Build a colored boxplot using GGPlot scheme with shapes by supplement type and a legend."
- "Generate a boxplot using the fivenum hinge function for five-number summary."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "boxplot" | `graphType: 'Boxplot'` | Sets the chart type to boxplot |
| "vertical" | `graphOrientation: 'vertical'` | Default, boxes displayed vertically |
| "horizontal" | `graphOrientation: 'horizontal'` | Boxes displayed horizontally |
| "group by [column]" | `groupingFactors: ['ColumnName']` | Groups boxplots by metadata column |
| "notched" / "notch" | `boxplotNotched: True` | Adds notches to boxes for significance indication |
| "single whiskers" | `boxplotWhiskersType: 'single'` | Uses single whisker style |
| "mean marker" | `boxplotMean: True` | Displays mean value in box |
| "mean color" | `boxplotMeanColor: 'rgb(...)'` | Sets fill color for mean marker |
| "mean border" | `boxplotMeanColorBorder: 'red'` | Sets border color for mean marker |
| "median color" | `boxplotMedianColor: 'red'` | Sets median line color |
| "median width" | `boxplotMedianWidth: 5` | Sets median line thickness |
| "outliers" / "outlier ratio" | `boxplotOutliersRatio: 3` | Controls outlier detection threshold (multiplier) |
| "separate boxes" / "segregated" | `segregateSamplesBy: ['ColumnName']` + `layoutTopology: '1X3'` | Creates separate panels per group |
| "show data points" | `showBoxplotOriginalData: True` | Displays individual data points |
| "jitter" | `jitter: True` | Adds random horizontal/vertical displacement to points |
| "fivenum" | `boxplotHingeFunction: 'fivenum'` | Uses five-number summary (min, q1, median, q3, max) |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors boxes by metadata values |
| "shape by [column]" | `shapeBy: 'ColumnName'` | Changes box shapes by metadata values |
| "color scheme" | `colorScheme: 'GGPlot'` | Sets color palette |
| "transparency" | `objectColorTransparency: 0.5` | Controls box fill opacity (0-1) |
| "hide legend" | `showLegend: False` | Hides legend |
| "rotate labels" | `smpTextRotate: 90` | Rotates group labels |
| "bold title" | `smpTitleFontStyle: 'bold'` | Makes sample title bold |
| "axis algorithm" | `axisAlgorithm: 'rPretty'` | Uses pretty axis scaling |

## Key Configuration Parameters

- `graphType`: Always `'Boxplot'` for boxplots
- `graphOrientation`: `'vertical'` (default) or `'horizontal'`
- `groupingFactors`: Array of metadata column names for grouping boxplots
- `boxplotNotched`: Boolean to enable notches for statistical significance
- `boxplotWhiskersType`: `'single'` for single whisker style
- `boxplotMean`: Boolean to display mean markers
- `boxplotMeanColor`: Fill color for mean marker (e.g., `'rgb(255,215,0)'`)
- `boxplotMeanColorBorder`: Border color for mean marker
- `boxplotMedianColor`: Color for median line
- `boxplotMedianWidth`: Thickness of median line
- `boxplotOutliersRatio`: Multiplier for outlier detection (default typically 1.5)
- `boxplotHingeFunction`: `'fivenum'` for five-number summary calculation
- `segregateSamplesBy`: Array to split into separate panels
- `layoutTopology`: Panel layout (e.g., `'1X3'` for 1 row, 3 columns)
- `showBoxplotOriginalData`: Boolean to show individual data points
- `jitter`: Boolean to add random displacement to data points
- `colorBy`: Metadata column for coloring boxes
- `shapeBy`: Metadata column for changing box shapes
- `objectColorTransparency`: Float 0-1 for box transparency
- `smpTextRotate`: Angle in degrees for sample label rotation
- `axisAlgorithm`: Axis scaling algorithm (`'rPretty'` recommended)
