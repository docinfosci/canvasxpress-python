---
title: "Dumbbell Chart Skill"
description: "Generate CanvasXpress dumbbell charts for comparing two values with connected dots, sorting, highlighting, data labels, and custom themes."
---

# Dumbbell Chart Skill

## Overview
Dumbbell charts (Cleveland dot plots) compare two values per entity using connected dots. CanvasXpress supports horizontal/vertical orientations, connected styles, sorting, sample highlighting, data value labels, point size scaling, and custom themes for clear comparative visualization.

## Data Formats

### Wide Format with Entities
```python
data = {
  'y': {
    'vars': ['Combined', 'Male', 'Female'],
    'smps': ['Monaco', 'Japan', 'Germany', 'Italy', ...],
    'data': [
      [53.1, 47.3, 47.1, 45.5, ...],  # Combined
      [51.7, 46.0, 46.0, 44.4, ...],  # Male
      [54.5, 48.7, 48.2, 46.5, ...],  # Female
    ],
  },
}
```

## Code Examples

### Example 1: Horizontal Dumbbell with Sorted Data
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'vars': ['Combined', 'Male', 'Female'],
    'smps': ['Monaco', 'Japan', 'Germany', 'Italy', 'Greece', 'Hong Kong', 'Austria', 'Spain', 'Netherlands', 'Finland', 'South Korea', 'France', 'Poland', 'United Kingdom', 'Russia', 'Norway', 'United States', 'New Zealand', 'China'],
    'data': [
      [53.1, 47.3, 47.1, 45.5, 44.5, 44.4, 44.0, 42.7, 42.6, 42.5, 41.8, 41.4, 40.7, 40.5, 39.6, 39.2, 38.1, 37.9, 37.4],
      [51.7, 46.0, 46.0, 44.4, 43.5, 43.5, 42.8, 41.5, 41.5, 40.9, 40.2, 39.6, 39.0, 39.3, 36.6, 38.4, 37.1, 36.5, 36.5],
      [54.5, 48.7, 48.2, 46.5, 45.6, 45.0, 45.1, 43.9, 43.6, 44.3, 43.4, 42.4, 41.7, 42.5, 40.0, 39.4, 38.8, 38.4, 38.4],
    ],
  },
}
config = {
  'graphType': 'Dumbbell',
  'graphOrientation': 'horizontal',
  'colors': ['grey', 'blue', 'pink'],
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'sortDir': 'ascending',
  'xAxis': ['Female', 'Male'],
  'xAxis2Show': True,
  'xAxisShow': False,
  'xAxisTitle2': 'Age',
  'title': 'Age Range by Gender',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Vertical Dumbbell with Highlighted Sample
```python
config = {
  'graphType': 'Dumbbell',
  'graphOrientation': 'vertical',
  'colors': ['grey', 'blue', 'pink'],
  'dataPointSizeScaleFactor': 3.5,
  'plotStyle': 'open',
  'showDataValues': True,
  'dataTextScaleFontFactor': 0.6,
  'highlightSmp': ['Russia'],
  'smpTextRotate': 30,
  'sortDir': 'ascending',
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'title': 'Age Range by Gender',
  'titleFontStyle': 'bold',
  'subtitle': 'The age difference between men and women is largest in Russia',
  'xAxis': ['Female', 'Male'],
  'xAxisTitle': 'Age',
}
```

### Example 3: Connected Horizontal Dumbbell with Theme
```python
config = {
  'graphType': 'Dumbbell',
  'graphOrientation': 'horizontal',
  'dumbbellType': 'connected',
  'dataPointSizeScaleFactor': 3,
  'plotStyle': 'open',
  'showDataValues': True,
  'dataTextScaleFontFactor': 0.5,
  'sortDir': 'ascending',
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'theme': 'wallStreetJournal',
  'title': 'Age Range by Gender',
  'titleFontStyle': 'bold',
  'xAxis': ['Female', 'Male'],
  'xAxisTitle': 'Age',
}
```

### Example 4: Vertical Dumbbell with Default Settings
```python
config = {
  'graphType': 'Dumbbell',
  'graphOrientation': 'vertical',
  'colors': ['grey', 'blue', 'pink'],
  'sortDir': 'ascending',
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'xAxis': ['Female', 'Male'],
  'xAxisTitle': 'Age',
  'title': 'Age Range by Gender',
}
```

### Example 5: Descending Sorted Dumbbell
```python
config = {
  'graphType': 'Dumbbell',
  'graphOrientation': 'horizontal',
  'dataPointSizeScaleFactor': 2.5,
  'plotStyle': 'open',
  'showDataValues': True,
  'dataTextScaleFontFactor': 0.5,
  'sortDir': 'descending',
  'legendColumns': 2,
  'legendPosition': 'bottom',
  'title': 'Age Range by Gender',
  'xAxis': ['Female', 'Male'],
  'xAxisTitle': 'Age',
}
```

## Agent Prompts

- "Create a CanvasXpress horizontal dumbbell chart comparing Female and Male age ranges across countries."
- "Generate a vertical dumbbell chart with open style and highlighted Russia sample."
- "Build a connected dumbbell chart with wallStreetJournal theme and bold title."
- "Create a dumbbell chart with ascending sort order and two-column bottom legend."
- "Generate a dumbbell chart with data values displayed and 0.6x text scaling."
- "Build a dumbbell chart with grey/blue/pink colors and subtitle text."
- "Create a dumbbell chart with 3.5x point size scaling and 30-degree rotated labels."
- "Generate a descending-sorted dumbbell chart with open dots and connected lines."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "dumbbell chart" | `graphType: 'Dumbbell'` | Sets the chart type to dumbbell |
| "horizontal" | `graphOrientation: 'horizontal'` | Horizontal orientation |
| "vertical" | `graphOrientation: 'vertical'` | Vertical orientation |
| "connected" | `dumbbellType: 'connected'` | Connects dots with lines |
| "open style" | `plotStyle: 'open'` | Uses hollow dots |
| "sort ascending" | `sortDir: 'ascending'` | Sorts data ascending |
| "sort descending" | `sortDir: 'descending'` | Sorts data descending |
| "highlight [entity]" | `highlightSmp: ['EntityName']` | Highlights specific sample |
| "data values" | `showDataValues: True` | Displays values on chart |
| "point size" | `dataPointSizeScaleFactor: N` | Scales dot size by N |
| "text scale" | `dataTextScaleFontFactor: N` | Scales data label size |
| "rotate labels" | `smpTextRotate: N` | Rotates labels by N degrees |
| "legend columns" | `legendColumns: N` | Sets legend column count |
| "legend position" | `legendPosition: 'bottom'` | Sets legend location |
| "theme" | `theme: 'wallStreetJournal'` | Applies theme |
| "title bold" | `titleFontStyle: 'bold'` | Makes title bold |
| "subtitle" | `subtitle: 'Text'` | Adds subtitle |
| "custom colors" | `colors: ['grey', 'blue', 'pink']` | Sets custom dot colors |
| "no x-axis" | `xAxisShow: False` + `xAxis2Show: True` | Hides primary x-axis |
| "x-axis title2" | `xAxisTitle2: 'Text'` | Sets secondary x-axis label |

## Key Configuration Parameters

- `graphType`: Always `'Dumbbell'` for dumbbell charts
- `graphOrientation`: `'horizontal'` or `'vertical'`
- `dumbbellType`: `'connected'` to connect dots with lines
- `plotStyle`: `'open'` for hollow dots, omitted for filled
- `colors`: Array of colors for variables (e.g., `['grey', 'blue', 'pink']`)
- `sortDir`: `'ascending'` or `'descending'` for data sorting
- `highlightSmp`: Array of sample names to highlight
- `showDataValues`: Boolean to display data values
- `dataPointSizeScaleFactor`: Float to scale dot size
- `dataTextScaleFontFactor`: Float to scale data label size
- `smpTextRotate`: Angle in degrees for sample label rotation
- `legendColumns`: Number of columns in legend
- `legendPosition`: `'bottom'`, `'top'`, `'left'`, `'right'`
- `theme`: Theme name (e.g., `'wallStreetJournal'`)
- `titleFontStyle`: `'bold'`, `'italic'`, or `'normal'`
- `subtitle`: Subtitle text
- `xAxis`: Array of axis labels (e.g., `['Female', 'Male']`)
- `xAxisTitle`: Label for primary x-axis
- `xAxisTitle2`: Label for secondary x-axis
- `xAxisShow`: Boolean to show/hide primary x-axis
- `xAxis2Show`: Boolean to show/hide secondary x-axis
