---
title: "Bullet Chart Skill"
description: "Generate CanvasXpress bullet charts with range stacking, target markers, progress bars, custom themes, and data value labels."
---

# Bullet Chart Skill

## Overview
Bullet charts display performance metrics with background ranges, target markers, and actual values. CanvasXpress supports horizontal/vertical orientations, range stacking (Low/Average/High), target variables, progress styles, custom fonts, color schemes, and layout topology for KPI dashboards.

## Data Formats

### Wide Format with Target Variable
```python
data = {
  'y': {
    'data': [
      [230, 180, 185, 225, 80],  # Value, Low, Average, High, Target
      [100, 15, 35, 115, 95],
      [150, 50, 70, 170, 135],
      [250, 250, 250, 250, 250],
      [234, 120, 150, 230, 175],
    ],
    'smps': ['USA', 'Chile', 'Brazil', 'Canada', 'Mexico'],
    'vars': ['Value', 'Low', 'Average', 'High', 'Target'],
  },
}
```

### Long Format with Metadata
```python
data = {
  'y': {
    'vars': ['Samples'],
    'smps': ['RNAseq', 'WGS', 'ctDNA', 'WES', ...],
    'data': [[26, 16, 6, 1, 3, 2, 5]],
  },
  'x': {
    'Type': ['RNAseq', 'WGS', 'ctDNA', 'WES', ...],
  },
}
```

## Code Examples

### Example 1: Horizontal Bullet with Range Stack
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [230, 180, 185, 225, 80, 190],
      [100, 15, 35, 115, 95, 30],
      [150, 50, 70, 170, 135, 50],
      [250, 250, 250, 250, 250, 250],
      [234, 120, 150, 230, 175, 55],
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'vars': ['V1', 'V2', 'V3', 'V4', 'V5'],
  },
}
config = {
  'graphType': 'Bullet',
  'graphOrientation': 'horizontal',
  'rangeStack': ['V2', 'V3', 'V4'],
  'rangeColors': ['#777777', '#AAAAAA', '#DDDDDD'],
  'bulletTargetVarName': 'V5',
  'showDataValues': True,
  'dataValuesPosition': 'inside',
  'dataTextColor': '#000000',
  'showLegend': False,
  'xAxis': ['V1'],
  'title': 'Horizontal Bullet Chart',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Vertical Bullet with Segregated Panels
```python
config = {
  'graphType': 'Bullet',
  'graphOrientation': 'vertical',
  'colors': ['#3F3F3F'],
  'rangeStack': ['V2', 'V3', 'V4'],
  'rangeColors': ['#945D55', '#C4A285', '#EBE7DE'],
  'bulletTargetVarName': 'V5',
  'bulletTargetVarColor': '#3F3F3F',
  'segregateSamplesBy': ['sample'],
  'layoutTopology': '1X6',
  'layoutAdjust': True,
  'showDataValues': True,
  'smpTextRotate': '90',
  'stripShow': False,
  'xAxisTextScaleFontFactor': 0.6,
  'xAxis': ['V1'],
}
```

### Example 3: Bullet with Custom Font and Color Grouping
```python
config = {
  'graphType': 'Bullet',
  'graphOrientation': 'vertical',
  'backgroundType': 'solid',
  'colorBy': 'Color',
  'colors': ['rgb(250,165,44)', 'rgb(254,225,60)', 'rgb(253,243,169)'],
  'rangeColors': ['rgb(48,126,164)'],
  'rangeColorTransparency': 1,
  'bulletWidthRatio': 1,
  'plotBackgroundColor': 'rgb(48,114,148)',
  'objectBorderColor': 'rgba(255,255,255,0)',
  'smpTextColor': 'rgb(255,255,255)',
  'smpTextRotate': '30',
  'smpTextScaleFontFactor': 2,
  'fontName': 'Waltograph',
  'fontsExternal': [{'name': 'Waltograph', 'url': 'https://www.canvasxpress.org/assets/fonts/waltograph42.otf'}],
  'marginBottom': 0,
  'marginLeft': 50,
  'marginRight': 50,
  'marginTop': 50,
  'maxTextSize': 80,
  'xAxis': ['Topic'],
  'xAxisShow': False,
  'xAxis2Show': False,
  'xAxisGridMajorShow': False,
  'xAxisGridMinorShow': False,
  'title': 'Friendship, Love, Family',
  'titleAlign': 'center',
  'titleColor': 'rgb(254,225,60)',
  'titleScaleFontFactor': 2.5,
  'showLegend': False,
}
```

### Example 4: Horizontal Bullet with Progress Bar Style
```python
config = {
  'graphType': 'Bullet',
  'graphOrientation': 'horizontal',
  'bulletStyle': 'progress',
  'progressWidthRatio': 0.28,
  'colorBy': 'Type',
  'colors': ['rgb(200,150,225)', 'rgb(240,170,90)', 'rgb(150,160,175)', 'rgb(80,160,235)', 'rgb(150,160,180)', 'rgb(90,200,120)', 'rgb(240,120,105)'],
  'backgroundType': 'solid',
  'background': 'rgb(20,26,38)',
  'plotBackgroundColor': 'rgb(20,26,38)',
  'foreground': 'rgb(235,240,248)',
  'objectBorderColor': 'rgba(0,0,0,0)',
  'showDataValues': True,
  'dataTextFontStyle': 'bold',
  'smpTextColor': 'rgb(235,240,248)',
  'title': 'NGS Data Types',
  'titleAlign': 'left',
  'titleColor': 'rgb(150,160,180)',
  'titleScaleFontFactor': 1.4,
  'marginTop': 40,
  'xAxis': ['Samples'],
  'xAxisShow': False,
  'xAxis2Show': False,
  'xAxisGridMajorShow': False,
  'xAxisGridMinorShow': False,
  'yAxisGridMajorShow': False,
  'showLegend': False,
}
```

### Example 5: Bullet with Round Gradient and Open Circle Target
```python
config = {
  'graphType': 'Bullet',
  'graphOrientation': 'horizontal',
  'barType': 'bullet',
  'rangeStack': ['Bad', 'Acceptable', 'Good'],
  'rangeStackShow': True,
  'rangeColors': ['#FFFFFF', '#F2F2F2', '#D8D8D8'],
  'bulletTargetType': 'openCircle',
  'bulletTargetVarName': 'Target',
  'bulletTargetWidthRatio': 0.2,
  'bulletStyle': 'roundGradient',
  'bulletWidthRatio': 0.5,
  'colors': ['#9422F5'],
  'showDataValues': True,
  'dataValuesPosition': 'inside',
  'dataTextColor': '#FFFFFF',
  'dataTextScaleFontFactor': 0.8,
  'layoutAdjust': True,
  'layoutSpacing': 20,
  'layoutTopology': '3X1',
  'segregateSamplesBy': ['sample'],
  'showLegend': False,
  'showSampleNames': False,
  'stripBackgroundColor': '#FFFFFF',
  'stripTextAlign': 'left',
  'stripTextColor': '#000000',
  'xAxis': ['Value'],
  'xAxis2Show': True,
  'xAxisShow': False,
  'xAxisGridMajorShow': False,
  'xAxisGridMinorShow': False,
}
```

## Agent Prompts

- "Create a CanvasXpress horizontal bullet chart with range stack (Low/Average/High) and target marker."
- "Generate a vertical bullet chart with segregated panels in 1x6 layout."
- "Build a bullet chart with custom font (Waltograph) and color grouping by metadata."
- "Create a horizontal bullet chart with progress bar style and dark background."
- "Generate a bullet chart with round gradient style and open circle target marker."
- "Build a bullet chart with stacked ranges in white/light gray/dark gray and 3x1 topology."
- "Create a bullet chart with target variable color coding and white data text."
- "Generate a bullet chart with 90-degree rotated sample labels and adjusted layout."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "bullet chart" | `graphType: 'Bullet'` | Sets the chart type to bullet |
| "horizontal" | `graphOrientation: 'horizontal'` | Horizontal orientation |
| "vertical" | `graphOrientation: 'vertical'` | Vertical orientation |
| "range stack" | `rangeStack: ['Low', 'Average', 'High']` | Stacks background ranges |
| "range colors" | `rangeColors: ['#hex1', '#hex2', ...]` | Sets range background colors |
| "target variable" | `bulletTargetVarName: 'ColumnName'` | Specifies target marker column |
| "progress style" | `bulletStyle: 'progress'` | Uses progress bar rendering |
| "round gradient" | `bulletStyle: 'roundGradient'` | Uses gradient-rounded bullets |
| "open circle target" | `bulletTargetType: 'openCircle'` | Shows circle for target |
| "data values inside" | `dataValuesPosition: 'inside'` | Places values inside bars |
| "data text color" | `dataTextColor: '#FFFFFF'` | Sets value text color |
| "custom font" | `fontName: 'Waltograph'` + `fontsExternal: [...]` | Loads custom font |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors bullets by metadata |
| "dark background" | `background: 'rgb(20,26,38)'` + `plotBackgroundColor: 'rgb(20,26,38)'` | Sets dark background |
| "foreground white" | `foreground: 'rgb(235,240,248)'` | Sets foreground text/stroke |
| "layout topology" | `layoutTopology: '3X1'` | Sets panel layout |
| "segregate by" | `segregateSamplesBy: ['ColumnName']` | Splits chart into panels |
| "layout adjust" | `layoutAdjust: True` | Auto-adjusts layout |
| "rotate text" | `smpTextRotate: '90'` | Rotates sample labels |
| "margin top" | `marginTop: 40` | Sets top margin |
| "no legend" | `showLegend: False` | Hides legend |
| "title color" | `titleColor: 'rgb(150,160,180)'` | Sets title text color |
| "title align" | `titleAlign: 'center'` | Aligns title text |
| "title scale" | `titleScaleFontFactor: 1.4` | Scales title font size |
| "no axis" | `xAxisShow: False` + `xAxis2Show: False` + `xAxisGridMajorShow: False` | Hides axes |

## Key Configuration Parameters

- `graphType`: Always `'Bullet'` for bullet charts
- `graphOrientation`: `'horizontal'` or `'vertical'`
- `rangeStack`: Array of columns for stacked range backgrounds (e.g., `['Low', 'Average', 'High']`)
- `rangeColors`: Array of colors for range backgrounds
- `rangeColorTransparency`: Float (0-1) for range transparency
- `bulletTargetVarName`: Column name for target marker
- `bulletTargetVarColor`: Color for target marker
- `bulletTargetType`: `'openCircle'` for circle target display
- `bulletStyle`: `'progress'`, `'roundGradient'`, or omitted for default
- `bulletWidthRatio`: Float for bullet width (0-1)
- `bulletTargetWidthRatio`: Float for target width (0-1)
- `progressWidthRatio`: Float for progress bar width (0-1)
- `barType`: `'bullet'` for bullet bar type
- `colors`: Array of colors for bullets
- `colorBy`: Metadata column for coloring bullets
- `background`: Background color (e.g., `'rgb(20,26,38)'`)
- `backgroundType`: `'solid'` or `'panel'`
- `plotBackgroundColor`: Background color for plot area
- `foreground`: Foreground text/stroke color
- `objectBorderColor`: Border color for elements
- `showDataValues`: Boolean to display values
- `dataValuesPosition`: `'inside'` or `'outside'`
- `dataTextColor`: Color for data values
- `dataTextFontStyle`: `'bold'`, `'italic'`, or `'normal'`
- `dataTextScaleFontFactor`: Float for data label size
- `fontName`: Font name (e.g., `'Waltograph'`)
- `fontsExternal`: Array of external font objects with `name` and `url`
- `smpTextColor`: Color for sample text
- `smpTextRotate`: String angle (e.g., `'90'`) for sample labels
- `smpTextScaleFontFactor`: Float for sample text size
- `layoutTopology`: Panel layout (e.g., `'3X1'`, `'1X6'`)
- `segregateSamplesBy`: Array to split chart into panels
- `layoutAdjust`: Boolean to auto-adjust layout
- `layoutSpacing`: Integer for layout spacing in pixels
- `marginBottom`, `marginLeft`, `marginRight`, `marginTop`: Integer margins in pixels
- `maxTextSize`: Integer for maximum text size
- `showLegend`: Boolean to show/hide legend
- `showSampleNames`: Boolean to show/hide sample names
- `stripShow`: Boolean to show/hide strip
- `stripBackgroundColor`, `stripTextAlign`, `stripTextColor`: Strip styling
- `xAxis`: Array of axis labels
- `xAxisShow`: Boolean to show/hide primary x-axis
- `xAxis2Show`: Boolean to show/hide secondary x-axis
- `xAxisGridMajorShow`: Boolean to show/hide major gridlines
- `xAxisGridMinorShow`: Boolean to show/hide minor gridlines
- `xAxisTextScaleFontFactor`: Float for x-axis text size
- `yAxisGridMajorShow`: Boolean to show/hide y-axis major gridlines
- `title`: Chart title
- `titleAlign`: `'left'`, `'center'`, `'right'`
- `titleColor`: Title text color
- `titleScaleFontFactor`: Float for title size
