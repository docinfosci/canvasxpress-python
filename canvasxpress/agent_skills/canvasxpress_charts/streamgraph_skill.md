---
title: "Streamgraph Skill"
description: "Generate CanvasXpress streamgraph-style scatter plots with Loess fits, stream bandwidth control, mirror/ridge rendering, and metadata-based color grouping."
---

# Streamgraph Skill

## Overview
Streamgraphs (implemented via Scatter2D with `scatterType: 'stream'`) visualize density distributions over continuous intervals. CanvasXpress supports stream bandwidth tuning, mirror/ridge modes, Loess trend fitting, metadata-based coloring, and point size scaling for rich temporal data exploration.

## Data Formats

### Long Format with Metadata
```python
data = {
  'y': {
    'data': [
      [1977, 2.98], [1977, 0.21], [1977, 0.52], [1977, 2.54],
      [1978, 1.92], [1978, 0.76], [1978, 1.04], [1978, 0.20],
      ...
    ],
    'smps': ['year', 'box_office'],
    'vars': ['1', '2', '3', ...],
  },
  'z': {
    'genre': ['Action', 'Adventure', 'Comedy', 'Drama', ...],
  },
}
```

## Code Examples

### Example 1: Stream Plot with Loess Fit and Color by Genre
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [1977, 2.98], [1977, 0.21], [1977, 0.52], [1977, 2.54],
      [1978, 1.92], [1978, 0.76], [1978, 1.04], [1978, 0.20],
      [1979, 1.15], [1979, 0.31], [1979, 0.56], [1979, 1.02],
      [1980, 1.80], [1980, 0.58], [1980, 1.20],
      [1981, 1.75], [1981, 0.13], [1981, 0.69], [1981, 0.35],
      [1982, 0.77], [1982, 0.96], [1982, 0.69],
      [1983, 1.34], [1983, 0.23], [1983, 0.52], [1983, 0.42],
    ],
    'smps': ['year', 'box_office'],
    'vars': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'],
  },
  'z': {
    'genre': ['Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Adventure', 'Comedy', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Comedy', 'Drama', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Comedy', 'Drama', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Comedy', 'Drama', 'Action', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Comedy', 'Drama', 'Action', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Comedy', 'Drama', 'Action', 'Animation', 'Comedy', 'Drama', 'Action', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Action', 'Adventure', 'Animation', 'Action', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Action', 'Adventure', 'Animation', 'Comedy', 'Action', 'Adventure', 'Animation', 'Action', 'Adventure', 'Animation', 'Drama', 'Action', 'Adventure', 'Action', 'Animation', 'Action', 'Adventure', 'Animation', 'Action', 'Animation', 'Action', 'Adventure', 'Animation', 'Action', 'Adventure', 'Animation'],
  },
}
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 0.75,
  'scatterStreamExtraSpan': 0.1,
  'scatterStreamNumber': 1000,
  'scatterStreamTrueRange': 'both',
  'colorBy': 'genre',
  'colors': ['rgb(255,180,0)', 'rgb(255,199,64)', 'rgb(194,0,8)', 'rgb(255,2,13)', 'rgb(19,175,239)'],
  'showLoessFit': 'genre',
  'showConfidenceIntervals': False,
  'dataPointSizeScaleFactor': 0,
  'backgroundType': 'panel',
  'panelBackgroundColor': 'rgb(222,222,222)',
  'xAxisGridMinorShow': False,
  'yAxisGridMinorShow': False,
  'xAxis': ['year'],
  'yAxis': ['box_office'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Stream Plot with Mirror Mode and Custom Colors
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 0.75,
  'scatterStreamNumber': 1000,
  'scatterStreamTrueRange': 'both',
  'colorBy': 'genre',
  'dataPointSizeScaleFactor': 0,
  'showLoessFit': 'genre',
  'xAxis': ['year'],
  'yAxis': ['box_office'],
}
```

### Example 3: Ridge Stream with High Density Sampling
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'ridge',
  'scatterStreamBandwidth': 0.5,
  'scatterStreamNumber': 2000,
  'scatterStreamExtraSpan': 0.2,
  'colorBy': 'category',
  'dataPointSizeScaleFactor': 0,
  'xAxis': ['time'],
  'yAxis': ['value'],
}
```

### Example 4: Stream Plot with Confidence Intervals
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 0.75,
  'scatterStreamNumber': 1000,
  'colorBy': 'group',
  'showLoessFit': 'group',
  'showConfidenceIntervals': True,
  'dataPointSizeScaleFactor': 0,
  'xAxis': ['time'],
  'yAxis': ['value'],
}
```

### Example 5: Stream Plot with Gradient Background
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 1.0,
  'scatterStreamNumber': 1500,
  'scatterStreamExtraSpan': 0.05,
  'colorBy': 'genre',
  'dataPointSizeScaleFactor': 0,
  'backgroundType': 'panel',
  'panelBackgroundColor': 'rgb(240,240,240)',
  'showLoessFit': 'genre',
  'xAxis': ['year'],
  'yAxis': ['revenue'],
}
```

### Example 6: Stream Plot with Wide Bandwidth
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 1.5,
  'scatterStreamNumber': 800,
  'colorBy': 'category',
  'dataPointSizeScaleFactor': 0,
  'xAxis': ['time'],
  'yAxis': ['measurement'],
}
```

### Example 7: Stream Plot with Narrow Bandwidth
```python
config = {
  'graphType': 'Scatter2D',
  'scatterType': 'stream',
  'scatterStreamType': 'mirror',
  'scatterStreamBandwidth': 0.3,
  'scatterStreamNumber': 1200,
  'colorBy': 'type',
  'dataPointSizeScaleFactor': 0,
  'xAxis': ['x'],
  'yAxis': ['y'],
}
```

## Agent Prompts

- "Create a CanvasXpress scatter stream plot showing box office revenue trends by genre with mirror stream type and Loess fit."
- "Generate a stream plot with color by category and ridge stream rendering mode."
- "Build a scatter stream with confidence intervals and Loess fit colored by group."
- "Create a stream plot with wide bandwidth (1.5) for smooth density visualization."
- "Generate a stream plot with narrow bandwidth (0.3) for detailed density peaks."
- "Build a scatter stream with panel background and gray styling."
- "Create a stream plot with 2000 sampling points for high-density rendering."
- "Generate a stream plot with extra span of 0.2 and bandwidth of 0.5."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "stream" / "streamgraph" | `graphType: 'Scatter2D'` + `scatterType: 'stream'` | Enables stream visualization |
| "mirror stream" | `scatterStreamType: 'mirror'` | Flows in both directions |
| "ridge stream" | `scatterStreamType: 'ridge'` | Unidirectional ridge mode |
| "bandwidth" | `scatterStreamBandwidth: 0.75` | Controls stream smoothness |
| "extra span" | `scatterStreamExtraSpan: 0.1` | Adds padding to stream range |
| "sampling number" | `scatterStreamNumber: 1000` | Sets density point count |
| "true range both" | `scatterStreamTrueRange: 'both'` | Includes all data in range |
| "loess fit" | `showLoessFit: 'ColumnName'` | Adds trend line by category |
| "confidence intervals" | `showConfidenceIntervals: True` | Shows confidence band |
| "color by [column]" | `colorBy: 'ColumnName'` | Colors streams by metadata |
| "no points" | `dataPointSizeScaleFactor: 0` | Hides individual dots |
| "panel background" | `backgroundType: 'panel'` + `panelBackgroundColor: 'rgb(222,222,222)'` | Adds gray background |
| "no gridlines" | `xAxisGridMinorShow: False` + `yAxisGridMinorShow: False` | Removes minor gridlines |

## Key Configuration Parameters

- `graphType`: Always `'Scatter2D'` for scatter-based streams
- `scatterType`: `'stream'` for streamgraph-style density visualization
- `scatterStreamType`: `'mirror'` for bidirectional flow, `'ridge'` for unidirectional
- `scatterStreamBandwidth`: Float controlling density smoothness (0.3 = narrow, 1.0 = wide)
- `scatterStreamNumber`: Integer for sampling density (800-2000 recommended)
- `scatterStreamExtraSpan`: Float for additional stream padding (0.0-0.2)
- `scatterStreamTrueRange`: `'both'` to include all data values
- `showLoessFit`: `'ColumnName'` to add Loess trend line by category
- `showConfidenceIntervals`: Boolean to show confidence band around Loess fit
- `colorBy`: Metadata column for stream coloring
- `colors`: Array of custom colors (e.g., `['rgb(255,180,0)', 'rgb(19,175,239)']`)
- `dataPointSizeScaleFactor`: Float to scale point size (use `0` to hide dots)
- `backgroundType`: `'panel'` for panel background styling
- `panelBackgroundColor`: Background color for chart panel
- `xAxisGridMinorShow`: Boolean to show/hide minor x-axis gridlines
- `yAxisGridMinorShow`: Boolean to show/hide minor y-axis gridlines
