---
title: "Violin Chart Skill"
description: "Generate CanvasXpress violin plots using Boxplot chart type with violin overlays, multiple scaling methods, notched boxes, mean markers, and single whiskers."
---

# Violin Chart Skill

## Overview
Violin plots combine boxplots with kernel density estimation to show data distribution shape. CanvasXpress implements violins via Boxplot with `showViolinBoxplot: True`, supporting area/width/count scaling, notched boxes, mean markers, single whiskers, and violin trimming for enhanced distribution visualization.

## Data Formats

### Long Format with Grouping Factors
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

### Example 1: Vertical Violin with Area Scaling
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'x': {
    'dose': ['0.5']*30 + ['1']*30 + ['2']*30,
    'order': list(range(1, 11))*6,
    'supp': ['VC']*10 + ['VC']*10 + ['VC']*10 + ['OJ']*10 + ['OJ']*10 + ['OJ']*10,
  },
  'y': {
    'data': [[4.2, 11.5, 7.3, 5.8, 6.4, 10, 11.2, 11.2, 5.2, 7, 16.5, 16.5, 15.2, 17.3, 22.5, 17.3, 13.6, 14.5, 18.8, 15.5, 23.6, 18.5, 33.9, 25.5, 26.4, 32.5, 26.7, 21.5, 23.3, 29.5, 15.2, 21.5, 17.6, 9.7, 14.5, 10, 8.2, 9.4, 16.5, 9.7, 19.7, 23.3, 23.6, 26.4, 20, 25.2, 25.8, 21.2, 14.5, 27.3, 25.5, 26.4, 22.4, 24.5, 24.8, 30.9, 26.4, 27.3, 29.4, 23]],
    'smps': ['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9', 'Var10', 'Var11', 'Var12', 'Var13', 'Var14', 'Var15', 'Var16', 'Var17', 'Var18', 'Var19', 'Var20', 'Var21', 'Var22', 'Var23', 'Var24', 'Var25', 'Var26', 'Var27', 'Var28', 'Var29', 'Var30', 'Var31', 'Var32', 'Var33', 'Var34', 'Var35', 'Var36', 'Var37', 'Var38', 'Var39', 'Var40', 'Var41', 'Var42', 'Var43', 'Var44', 'Var45', 'Var46', 'Var47', 'Var48', 'Var49', 'Var50', 'Var51', 'Var52', 'Var53', 'Var54', 'Var55', 'Var56', 'Var57', 'Var58', 'Var59', 'Var60'],
    'vars': ['len'],
  },
}
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': False,
  'violinScale': 'area',
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxisGridMajorColor': 'white',
  'xAxisGridMinorShow': False,
  'xAxis2Show': False,
  'xAxisTitle': 'len',
  'showLegend': False,
  'title': 'The Effect of Vitamin C on Tooth Growth in Guinea Pigs',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Horizontal Violin with Count Scaling
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'horizontal',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': False,
  'violinScale': 'count',
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
```

### Example 3: Vertical Violin with Width Scaling
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': False,
  'violinScale': 'width',
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
```

### Example 4: Violin with Notched Box and Single Whiskers
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': False,
  'boxplotNotched': True,
  'boxplotWishkersType': 'single',
  'violinTrim': False,
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
```

### Example 5: Violin with Boxplot Overlay
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': True,
  'boxplotNotched': True,
  'boxplotWishkersType': 'single',
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
```

### Example 6: Violin with Mean Markers
```python
config = {
  'graphType': 'Boxplot',
  'graphOrientation': 'vertical',
  'groupingFactors': ['dose'],
  'showViolinBoxplot': True,
  'showBoxplotIfViolin': True,
  'boxplotMean': True,
  'boxplotMeanColor': 'rgb(255,215,0)',
  'boxplotMeanColorBorder': 'red',
  'boxplotNotched': True,
  'boxplotWishkersType': 'single',
  'axisAlgorithm': 'rPretty',
  'axisTitleFontStyle': 'bold',
  'smpTitle': 'dose',
  'smpTitleFontStyle': 'bold',
  'smpTextRotate': 90,
  'background': 'white',
  'backgroundType': 'panel',
  'panelBackgroundColor': '#E5E5E5',
  'guidesShow': True,
  'guidesColor': 'white',
  'guidesLineType': 'solid',
  'xAxis': ['len'],
  'xAxisTitle': 'len',
}
```

## Agent Prompts

- "Create a CanvasXpress violin plot with area scaling showing tooth growth distribution across vitamin C doses."
- "Generate a horizontal violin plot with count-based scaling grouped by dose."
- "Build a vertical violin plot with width scaling for density visualization."
- "Create a violin plot with notched boxes and single whiskers for 95% confidence intervals."
- "Generate a violin plot with boxplot overlay showing median and quartiles."
- "Build a violin plot with mean markers (gold fill, red border) and notched boxes."
- "Create a violin plot with no trimming and panel background styling."
- "Generate a violin plot with white gridlines and italic sample titles."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "violin plot" | `graphType: 'Boxplot'` + `showViolinBoxplot: True` | Enables violin visualization |
| "area scaling" | `violinScale: 'area'` | Scales violins by area |
| "count scaling" | `violinScale: 'count'` | Scales violins by count |
| "width scaling" | `violinScale: 'width'` | Scales violins by width |
| "no trimming" | `violinTrim: False` | Disables violin trimming |
| "notched box" | `boxplotNotched: True` | Adds notches for confidence intervals |
| "single whisker" | `boxplotWishkersType: 'single'` | Shows single-sided whiskers |
| "mean marker" | `boxplotMean: True` + `boxplotMeanColor: 'rgb(255,215,0)'` + `boxplotMeanColorBorder: 'red'` | Shows mean with styled marker |
| "box overlay" | `showBoxplotIfViolin: True` | Shows boxplot inside violin |
| "group by [column]" | `groupingFactors: ['ColumnName']` | Groups violins by metadata |
| "panel background" | `backgroundType: 'panel'` + `panelBackgroundColor: '#E5E5E5'` | Adds gray background |
| "white gridlines" | `xAxisGridMajorColor: 'white'` + `guidesShow: True` + `guidesColor: 'white'` | Sets white guides |
| "italic title" | `smpTitleFontStyle: 'italic'` | Makes sample title italic |
| "rotate labels" | `smpTextRotate: 90` | Rotates sample/axis labels |
| "no legend" | `showLegend: False` | Hides legend |
| "axis algorithm" | `axisAlgorithm: 'rPretty'` | Sets axis tick generation |

## Key Configuration Parameters

- `graphType`: Always `'Boxplot'` for violin plots
- `showViolinBoxplot`: Boolean to enable violin visualization
- `showBoxplotIfViolin`: Boolean to show boxplot inside violin
- `violinScale`: `'area'`, `'count'`, or `'width'` for violin scaling method
- `violinTrim`: Boolean to enable/disable violin trimming
- `boxplotNotched`: Boolean to add notches for confidence intervals
- `boxplotWishkersType`: `'single'` for single-sided whiskers
- `boxplotMean`: Boolean to show mean marker
- `boxplotMeanColor`: Fill color for mean marker (e.g., `'rgb(255,215,0)'`)
- `boxplotMeanColorBorder`: Border color for mean marker (e.g., `'red'`)
- `groupingFactors`: Array of metadata columns for grouping violins
- `background`: Chart background color (e.g., `'white'`)
- `backgroundType`: `'panel'` for panel background styling
- `panelBackgroundColor`: Background color for chart panel (e.g., `'#E5E5E5'`)
- `guidesShow`: Boolean to show guide lines
- `guidesColor`: Color for guide lines
- `guidesLineType`: `'solid'`, `'dashed'`, `'dotted'`
- `smpTitleFontStyle`: `'italic'`, `'bold'`, or `'normal'`
- `smpTextRotate`: Angle in degrees for sample label rotation
- `axisAlgorithm`: `'rPretty'` for axis tick generation
- `xAxisGridMajorColor`: Color for major gridlines
- `xAxisGridMinorShow`: Boolean to show/hide minor gridlines
- `xAxis2Show`: Boolean to show/hide secondary x-axis
- `showLegend`: Boolean to show/hide legend
