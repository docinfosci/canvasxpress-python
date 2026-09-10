---
title: "Area Chart Skill"
description: "Generate CanvasXpress area charts with single/multiple series, stacked, or percentage layouts."
---

# Area Chart Skill

## Overview
Area charts display quantitative data as filled regions between a line and the x-axis. They excel at visualizing trends over time and comparing multiple data series. CanvasXpress supports single series, overlapping multi-series, stacked, and percentage-stacked area charts.

## Data Formats

### Wide Format (Series as Variables)
```python
data = {
  'y': {
    'data': [
      [10, 11, 13, 4, 18, 21],
      [5, 6, 10, 12, 15, 10],
      [2, 3, 6, 4, 8, 6],
    ],
    'smps': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'vars': ['Series A', 'Series B', 'Series C'],
  },
}
```

### Long/Skinny Format
```python
data = {
  'y': {
    'data': [
      [1, 10], [2, 11], [3, 13], [4, 4], [5, 18], [6, 21],
      [1, 5],  [2, 8],  [3, 10], [4, 12], [5, 15], [6, 10],
      [1, 2],  [2, 3],  [3, 6],  [4, 4],  [5, 8],  [6, 6],
    ],
    'smps': ['Month', 'Value'],
    'vars': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
  },
  'z': {
    'Series': ['Series A']*6 + ['Series B']*6 + ['Series C']*6,
  },
}
```

## Code Examples

### Example 1: Single Series Vertical Area Chart
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[10, 11, 13, 4, 18, 21]],
    'smps': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'vars': ['Value'],
  },
}
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'Prism',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'title': 'Area graph with one series',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Value'],
  'xAxisTitle': 'Revenue (in Millions)',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Smooth Line (Spline) Area Chart
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'Prism',
  'lineType': 'spline',
  'showLegend': False,
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'title': 'Area graph with one series - Spline',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Value'],
  'xAxisTitle': 'Revenue (in Millions)',
}
```

### Example 3: Overlapping Multi-Series Area Chart
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'Behance',
  'lineType': 'spline',
  'objectColorTransparency': 0.7,
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'subtitle': 'random data',
  'title': 'Area graph with three overlapping data series',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Series A', 'Series B', 'Series C'],
  'xAxisTitle': 'Revenue (in Millions)',
}
```

### Example 4: Stacked Area Chart
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'LastAirBenderWater',
  'areaType': 'stacked',
  'lineType': 'spline',
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'title': 'Area graph with three stacked data series',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Series A', 'Series B', 'Series C'],
  'xAxisTitle': 'Revenue (in Millions)',
}
```

### Example 5: Percentage Stacked Area Chart
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'Prism',
  'areaType': 'percent',
  'lineType': 'spline',
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'title': 'Area graph with three data series in percentage',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Series A', 'Series B', 'Series C'],
  'xAxisTitle': 'Percent of Revenue (in Millions)',
}
```

### Example 6: Filtered Data Area Chart
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'colorScheme': 'Behance',
  'lineType': 'spline',
  'objectColorTransparency': 0.7,
  'filterData': [
    ['guess', False, 'different', ['Series C']],
  ],
  'smpTextRotate': 90,
  'smpTitle': 'Month / First Quarters of 2024',
  'subtitle': 'Filtered data',
  'title': 'Area graph with three overlapping data series',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Series A', 'Series B', 'Series C'],
  'xAxisTitle': 'Revenue (in Millions)',
}
```

### Example 7: Long Format with Color Grouping
```python
config = {
  'graphType': 'Area',
  'colorBy': 'Series',
  'colorScheme': 'GameOfThronesStannis',
  'lineType': 'spline',
  'legendColumns': 3,
  'legendPosition': 'top',
  'subtitle': 'skiny-long format',
  'title': 'Area graph with three stacked data series',
  'titleScaleFontFactor': 1.2,
  'xAxis': ['Month'],
  'xAxisTitle': 'Revenue (in Millions)',
  'yAxis': ['Value'],
  'yAxisTitle': 'Months / First Quarters of 2024',
}
```

### Example 8: Steam Plot (Stacked, No Axes)
```python
config = {
  'graphType': 'Area',
  'graphOrientation': 'vertical',
  'areaType': 'stacked',
  'lineType': 'spline',
  'colorScheme': 'ColorSpectrum',
  'colorSpectrum': ['blue', 'cyan', 'yellow', 'red'],
  'objectColorTransparency': 0.3,
  'objectBorderColor': False,
  'showLegend': False,
  'showSampleNames': False,
  'xAxisShow': False,
  'xAxisGridMajorShow': False,
  'xAxisGridMinorShow': False,
  'title': 'Steam Plot',
}
```

## Agent Prompts

- "Create a CanvasXpress area chart showing monthly revenue over six months with values [10, 11, 13, 4, 18, 21]. Use a vertical orientation and Prism color scheme."
- "Generate a stacked area chart with three series (Series A, B, C) across months Jan-Jun. The data should be stacked vertically with a spline line type."
- "Build a percentage stacked area chart in CanvasXpress showing three data series. Use smooth lines and a Prism color palette."
- "Create an overlapping area chart with transparency for three series, highlighting one series with a different color using filterData."
- "Make a CanvasXpress area graph from long-format data where a 'Series' column groups the data by color using colorBy."
- "Generate a steam plot using CanvasXpress stacked area charts with no axes or legend, using a color spectrum from blue to red."
- "Visualize US population age distribution over time as a stacked area chart with age groups on the x-axis and population counts on the y-axis."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "area chart" | `graphType: 'Area'` | Sets the chart type to area |
| "stacked area" | `areaType: 'stacked'` | Stacks series vertically |
| "percentage area" / "percent" | `areaType: 'percent'` | Normalizes series to 100% |
| "smooth line" / "spline" | `lineType: 'spline'` | Uses quadratic bezier curves |
| "vertical" | `graphOrientation: 'vertical'` | Default, values on y-axis |
| "transparent" / "transparency" | `objectColorTransparency: 0.x` | Controls fill opacity (0-1) |
| "color by [column]" | `colorBy: '[column]'` | Groups data by metadata column |
| "filter [series]" | `filterData: [['guess', False, 'different', ['Series Name']]]` | Excludes specified series |
| "long format" / "skinny" | Separate `y` data structure with `z` metadata | Data rows as [index, value] pairs |
| "no axes" / "clean" | `xAxisShow: False`, `showLegend: False`, `showSampleNames: False` | Hides UI elements |
| "steam plot" | Stacked area + no axes + spectrum colors | Custom visual style |
| "legend columns" | `legendColumns: N` | Sets number of legend columns |
| "legend at top" | `legendPosition: 'top'` | Positions legend above chart |
| "rotate labels" | `smpTextRotate: 90` | Rotates sample/x-axis labels |

## Key Configuration Parameters

- `graphType`: Always `'Area'` for area charts
- `areaType`: `'stacked'`, `'percent'`, or omitted for overlapping
- `lineType`: `'spline'` for smooth curves, `'step'` for step lines, or omitted for straight lines
- `colorScheme`: `'Prism'`, `'Behance'`, `'LastAirBenderWater'`, `'GameOfThronesStannis'`, `'ColorSpectrum'`, `'GGPlot'`, `'Blues'`
- `objectColorTransparency`: Float between 0 and 1 for overlapping series visibility
- `filterData`: Array of filter rules for excluding specific series or samples
- `colorBy`: Metadata column name for coloring groups in long-format data
