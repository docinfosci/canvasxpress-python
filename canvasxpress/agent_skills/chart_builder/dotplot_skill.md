---
title: "Dotplot Skill"
description: "Generate CanvasXpress dotplots with binned data, error bars, jitter, stacked layouts, overlays, and metadata color/shape encoding."
---

# Dotplot Skill

## Overview
Dotplots display quantitative values as dots, ideal for comparing distributions across categories. CanvasXpress supports binned data, error bars (standard deviation), jitter for overlapping points, stacked dotplots, sample overlays (e.g., bars), and metadata-driven color/shape encoding.

## Data Formats

### Wide Format with Metadata Factors
```python
data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', ...],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', ...],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', ...],
  },
  'y': {
    'data': [
      [5, 10, 25, 40, 45, 50],
      [95, 80, 75, 70, 55, 40],
      ...
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
}
```

### Long Format for Grouped Data
```python
data = {
  'x': {
    'dose': ['0.5']*30 + ['1']*30 + ['2']*30,
    'supp': ['VC']*10 + ['VC']*10 + ['VC']*10 + ['OJ']*10 + ...
  },
  'y': {
    'data': [[4.2, 11.5, 7.3, ...]],
    'smps': ['Var1', 'Var2', ...],
    'vars': ['len'],
  },
}
```

## Code Examples

### Example 1: Dotplot with Sample Overlays (Bars)
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'Factor1': ['Lev : 1', 'Lev : 2', 'Lev : 3', 'Lev : 1', 'Lev : 2', 'Lev : 3'],
    'Factor2': ['Lev : A', 'Lev : B', 'Lev : A', 'Lev : B', 'Lev : A', 'Lev : B'],
    'Factor3': ['Lev : X', 'Lev : X', 'Lev : Y', 'Lev : Y', 'Lev : Z', 'Lev : Z'],
    'Factor4': [5, 10, 15, 20, 25, 30],
    'Factor5': [8, 16, 24, 32, 40, 48],
    'Factor6': [10, 20, 30, 40, 50, 60],
  },
  'y': {
    'data': [
      [5, 10, 25, 40, 45, 50],
      [95, 80, 75, 70, 55, 40],
      [25, 30, 45, 60, 65, 70],
      [55, 40, 35, 30, 15, 1],
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4'],
  },
}
config = {
  'graphType': 'Dotplot',
  'graphOrientation': 'vertical',
  'lineType': 'spline',
  'smpOverlays': ['Factor1', 'Factor2', 'Factor3', 'Factor4', 'Factor5', 'Factor6'],
  'smpOverlayProperties': {
    'Factor4': {
      'type': 'Bar',
      'color': 'blue',
      'thickness': 50,
      'showLegend': True,
    },
    'Factor5': {
      'type': 'Bar',
      'color': 'grey',
      'thickness': 50,
      'showLegend': True,
    },
    'Factor6': {
      'type': 'Bar',
      'color': 'red',
      'thickness': 50,
      'showLegend': True,
    },
  },
  'showSmpOverlaysLegend': True,
  'smpTextRotate': 45,
  'smpTitle': 'Collection of Samples',
  'smpTitleFontStyle': 'italic',
  'title': 'Dotplot Graph',
  'subtitle': 'Random Data',
  'xAxis': ['V1', 'V2', 'V3', 'V4'],
  'xAxisTickFormat': '%.0f Mil.',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Iris Dataset with Jitter
```python
config = {
  'graphType': 'Dotplot',
  'graphOrientation': 'vertical',
  'jitter': True,
  'axisTextFontStyle': 'bold',
  'axisTitleFontStyle': 'italic',
  'smpTextFontStyle': 'italic',
  'smpTextRotate': 90,
  'smpTitle': 'Species',
  'fontStyle': 'italic',
  'citation': 'R. A. Fisher (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics 7 (2) => 179-188.',
  'citationFontStyle': 'italic',
  'marginBottom': 30,
  'xAxis2Show': False,
  'title': 'Iris flower data set',
  'xAxis': ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'],
}
```

### Example 3: Automobile Data with Citation and Legend
```python
config = {
  'graphType': 'Dotplot',
  'jitter': True,
  'showErrorBars': False,
  'legendColumns': 2,
  'legendInside': True,
  'legendPosition': 'bottomRight',
  'citation': 'Henderson, H. V. and Velleman, P. F. (1981), Building Regression Models Interactively. Biometrics, 37, 391-411.',
  'citationFontStyle': 'italic',
  'title': 'Measurements on 38 1978-79 model automobiles.\nThe gas mileage in miles per gallon as measured by Consumers Union on a test track.',
  'xAxis': ['MPG', 'Weight', 'Drive_Ratio', 'Horsepower', 'Displacement', 'Cylinders'],
}
```

### Example 4: Stacked Dotplot with Sorted Data
```python
config = {
  'graphType': 'Dotplot',
  'dotplotType': 'stacked',
  'plotStyle': 'open',
  'showDataValues': True,
  'axisAlgorithm': 'wilkinson',
  'sortDir': 'descending',
  'dataPointSizeScaleFactor': 3,
  'dataTextScaleFontFactor': 0.6,
  'xAxis2Title': 'Annual Salary',
  'xAxisTitle': 'Annual Salary',
  'xAxisTickFormat': '$%sK',
  'xAxisGridMinorShow': False,
  'smpTitle': 'School',
  'title': 'Gender Earnings Disparity',
  'xAxis': ['Women', 'Men'],
}
```

### Example 5: Binned Dotplot with Standard Deviation Error Bars
```python
config = {
  'graphType': 'Dotplot',
  'graphOrientation': 'vertical',
  'binned': True,
  'groupingFactors': ['dose'],
  'errorBarsColor': 'red',
  'errorBarsType': 'standardDeviation',
  'jitter': False,
  'showLegend': False,
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
  'xAxisTitle': 'len',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
}
```

### Example 6: Dotplot with Color and Shape by Metadata
```python
config = {
  'graphType': 'Dotplot',
  'graphOrientation': 'vertical',
  'colorBy': 'dose',
  'colorScheme': 'GGPlot',
  'shapeBy': 'supp',
  'binned': True,
  'groupingFactors': ['dose'],
  'errorBarsColor': 'red',
  'errorBarsType': 'standardDeviation',
  'jitter': False,
  'showLegend': True,
  'legendKeyBackgroundBorderColor': 'rgba(255,255,255,0)',
  'legendKeyBackgroundColor': 'rgba(255,255,255,0)',
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'stringSampleFactors': ['dose'],
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'xAxis': ['len'],
  'xAxis2Show': False,
  'xAxisGridMinorShow': False,
  'xAxisTitle': 'len',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
}
```

### Example 7: Dotplot with Panel Background and White Gridlines
```python
config = {
  'graphType': 'Dotplot',
  'graphOrientation': 'vertical',
  'colorBy': 'dose',
  'colorScheme': 'Blues',
  'binned': True,
  'groupingFactors': ['dose'],
  'jitter': False,
  'showLegend': True,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'objectBorderColor': 'rgba(0,0,0)',
  'showErrorBars': False,
  'xAxisGridMajorColor': 'white',
  'xAxisGridMinorShow': False,
  'xAxis2Show': False,
  'smpTextRotate': 90,
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'stringSampleFactors': ['dose'],
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'xAxisTitle': 'len',
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
  'xAxis': ['len'],
}
```

## Agent Prompts

- "Create a CanvasXpress dotplot with sample overlays showing bar annotations for multiple factors."
- "Generate a dotplot with jitter applied to separate overlapping points for the Iris dataset."
- "Build a dotplot with citation text and a two-column legend positioned at bottom right."
- "Create a stacked dotplot showing gender earnings disparity with data values displayed and descending sort."
- "Generate a binned dotplot with standard deviation error bars grouped by dose."
- "Build a dotplot with dots colored by dose and shaped by supplement type."
- "Create a dotplot with panel background styling and white gridlines."
- "Generate a dotplot with horizontal orientation and string sample factors."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "dotplot" | `graphType: 'Dotplot'` | Sets the chart type to dotplot |
| "binned" | `binned: True` | Bins data for aggregated dot display |
| "grouped by [column]" | `groupingFactors: ['ColumnName']` | Groups dots by metadata column |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors dots by metadata |
| "shape by [column]" | `shapeBy: 'ColumnName'` | Shapes dots by metadata |
| "jitter" | `jitter: True` | Adds random displacement to avoid overlap |
| "error bars" | `errorBarsColor: 'red'` + `errorBarsType: 'standardDeviation'` | Adds error bars |
| "stacked" | `dotplotType: 'stacked'` | Stacks dots vertically |
| "open style" | `plotStyle: 'open'` | Uses hollow dot markers |
| "show values" | `showDataValues: True` | Displays data values near dots |
| "sample overlay" | `smpOverlays: ['ColumnName']` | Adds overlays to samples |
| "overlay bar" | `smpOverlayProperties: [{type: 'Bar', color, thickness}]` | Creates bar overlays |
| "rotate labels" | `smpTextRotate: 45|90` | Rotates sample/axis labels |
| "sort descending" | `sortDir: 'descending'` | Sorts data descending |
| "citation" | `citation: 'Text'` | Adds citation text to chart |
| "axis algorithm" | `axisAlgorithm: 'rPretty'` or `'wilkinson'` | Sets axis tick algorithm |
| "string factors" | `stringSampleFactors: ['ColumnName']` | Treats column as string categorical |
| "no error bars" | `showErrorBars: False` | Hides error bars |
| "panel background" | `backgroundType: 'panel'` + `panelBackgroundColor: '#E5E5E5'` | Adds panel background |
| "white gridlines" | `xAxisGridMajorColor: 'white'` + `guidesShow: True` + `guidesColor: 'white'` | Sets gridline color |

## Key Configuration Parameters

- `graphType`: Always `'Dotplot'` for dotplots
- `binned`: Boolean to bin and aggregate data into binned dot display
- `groupingFactors`: Array of metadata column names for grouping dots
- `colorBy`: Metadata column for dot color encoding
- `colorScheme`: Color palette (e.g., `'GGPlot'`, `'Blues'`, `'Prism'`)
- `shapeBy`: Metadata column for dot shape encoding
- `jitter`: Boolean to add random displacement and reduce overlap
- `dotplotType`: `'stacked'` for stacked dot display
- `plotStyle`: `'open'` for hollow dots, omitted for filled dots
- `showDataValues`: Boolean to display numeric values near dots
- `errorBarsColor`: Color for error bars (e.g., `'red'`)
- `errorBarsType`: `'standardDeviation'` for standard deviation error bars
- `showErrorBars`: Boolean to show/hide error bars
- `smpOverlays`: Array of metadata column names for sample overlays
- `smpOverlayProperties`: Object defining overlay types (`'Bar'`) with color, thickness, and legend settings
- `showSmpOverlaysLegend`: Boolean to show overlay legend
- `sortDir`: `'descending'` or `'ascending'` for data sorting
- `dotplotType`: `'stacked'` for vertical stacking of dots
- `dataPointSizeScaleFactor`: Float to scale dot size (e.g., `3`)
- `dataTextScaleFontFactor`: Float to scale text size (e.g., `0.6`)
- `axisAlgorithm`: `'rPretty'` or `'wilkinson'` for axis tick generation
- `smpTextRotate`: Angle in degrees for sample label rotation
- `smpTitleFontStyle`: `'italic'`, `'bold'`, or `'normal'`
- `stringSampleFactors`: Array of metadata columns to treat as strings
- `citation`: String for chart citation
- `citationFontStyle`: `'italic'` or `'normal'` for citation text style
- `backgroundType`: `'panel'` for panel background styling
- `panelBackgroundColor`: Background color for chart panel (e.g., `'rgb(226,236,248)'`, `'#E5E5E5'`)
- `guidesShow`: Boolean to show guide lines
- `guidesColor`: Color for guide lines
- `guidesLineType`: `'solid'`, `'dashed'`, `'dotted'`
- `xAxisGridMajorColor`: Color for major gridlines
- `xAxisGridMinorShow`: Boolean to show/hide minor gridlines
- `legendColumns`: Number of columns in legend
- `legendInside`: Boolean to place legend inside chart area
- `legendPosition`: `'topLeft'`, `'topRight'`, `'bottomLeft'`, `'bottomRight'`, `'right'`
