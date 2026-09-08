---
title: "Heatmap Skill"
description: "Generate CanvasXpress heatmaps with clustering, color spectra, cell markers, dendrograms, and sample/variable overlays."
---

# Heatmap Skill

## Overview
Heatmaps display matrix data as color-coded grids, ideal for visualizing patterns in large datasets. CanvasXpress supports hierarchical clustering, customizable color spectra, cell markers, dendrograms, and metadata overlays for enriched data exploration.

## Data Formats

### Wide Format with Metadata
```python
data = {
  'x': {
    'Dose': [0, 0, 5, 5, 10, 10, ...],
    'Site': ['Site1', 'Site2', 'Site1', 'Site2', ...],
    'Treatment': ['Control', 'TreatmentA', ...],
  },
  'y': {
    'data': [
      [0.784, 1.036, -0.641, ...],  # V1
      [0.222, 0.716, 0.993, ...],   # V2
      ...
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5'],
    'vars': ['V1', 'V2', 'V3', 'V4', 'V5'],
  },
  'z': {
    'Lab': ['A', 'A', 'B', 'B', ...],
    'Type': ['Pro', 'Tyr', 'Pho', ...],
  },
}
```

## Code Examples

### Example 1: Simple Heatmap
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [
      [0.784, 1.036, -0.641, 1.606, 2.208],
      [0.222, 0.716, 0.993, -0.913, 0.996],
      [0.486, 2.15, -0.069, -0.468, 0.402],
    ],
    'smps': ['S1', 'S2', 'S3', 'S4', 'S5'],
    'vars': ['V1', 'V2', 'V3', 'V4', 'V5'],
  },
}
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['navy', 'white', 'firebrick3'],
  'title': 'Simple Heatmap',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Clustered Heatmap with Cell Markers
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['navy', 'white', 'firebrick3'],
  'variablesClustered': True,
  'samplesClustered': True,
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'heatmapCellMarkers': [
    {
      'variable': 'V1',
      'sample': 'S3',
      'width': 2,
    },
    {
      'variable': 'V2',
      'sample': 'S5',
      'shape': 'circle',
      'color': 'purple',
      'width': 2,
    },
    {
      'variable': 'V4',
      'sample': 'S1',
      'shape': 'square',
      'size': 0.3,
      'width': 2,
    },
  ],
  'title': 'Clustered data',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 3: Heatmap with Custom Color Breaks
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['blue', 'white', 'red'],
  'colorSpectrumBreaks': [1, 2, 10],
  'variablesClustered': True,
  'samplesClustered': True,
  'showSmpDendrogram': False,
  'showVarDendrogram': False,
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'title': 'Custom color breaks',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 4: Cluster Heatmap Without Dendrograms
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['magenta', 'blue', 'black', 'red', 'gold'],
  'variablesClustered': True,
  'samplesClustered': True,
  'heatmapCellBox': False,
  'showSmpDendrogram': False,
  'showVarDendrogram': False,
  'title': 'Cluster Heatmap Without Trees',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 5: Multi-Color Symmetrical Heatmap
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['black', 'blue', 'magenta', 'red', 'gold'],
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'variablesClustered': True,
  'samplesClustered': True,
  'heatmapCellMarkers': [
    {
      'variable': 'V1',
      'sample': 'S3',
      'shape': 'diamond',
      'color': 'purple',
      'width': 2,
    },
  ],
  'title': 'Symmetrical Colors in Heatmap',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 6: Heatmap with Sample Annotations (Overlays)
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['navy', 'white', 'firebrick3'],
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'variablesClustered': True,
  'samplesClustered': True,
  'showSmpDendrogram': False,
  'showVarDendrogram': False,
  'smpOverlays': ['Lab', 'Type'],
  'showSmpOverlaysLegend': True,
  'title': 'Heatmap with Sample Annotations',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 7: Sorted Heatmap by Tree
```python
config = {
  'graphType': 'Heatmap',
  'colorSpectrum': ['navy', 'white', 'firebrick3'],
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'sortSmpByTree': True,
  'sortVarByTree': True,
  'showSmpDendrogram': True,
  'showVarDendrogram': True,
  'title': 'Sorted Heatmap by Tree',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

### Example 8: Heatmap with Color Mapping Type
```python
config = {
  'graphType': 'Heatmap',
  'heatMapping': 'color',
  'colorSpectrum': ['navy', 'white', 'firebrick3'],
  'heatmapCellBoxColor': 'rgb(255,255,255)',
  'heatmapCellMarkers': [
    {
      'variable': 'V1',
      'sample': 'S3',
      'shape': 'triangle',
      'color': 'red',
      'width': 2,
    },
  ],
  'variablesClustered': True,
  'samplesClustered': True,
  'title': 'Heatmap with Color Mapping',
  'xAxis': ['V1', 'V2', 'V3', 'V4', 'V5'],
}
```

## Agent Prompts

- "Create a CanvasXpress heatmap showing gene expression data across samples with navy-white-firebrick color spectrum."
- "Generate a clustered heatmap with hierarchical clustering on both rows and columns."
- "Build a heatmap with custom color breaks at specific values (1, 2, 10) using blue-white-red spectrum."
- "Create a clustered heatmap without dendrogram trees for a clean visualization."
- "Generate a heatmap with cell markers (circles, squares, diamonds) highlighting specific data points."
- "Build a heatmap with sample annotations as overlays showing Lab and Type metadata."
- "Create a symmetrical heatmap with five-color spectrum (black, blue, magenta, red, gold)."
- "Generate a heatmap sorted by hierarchical tree with dendrograms visible."
- "Make a heatmap with heatMapping set to 'color' for value-based coloring."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "heatmap" | `graphType: 'Heatmap'` | Sets the chart type to heatmap |
| "clustered" | `variablesClustered: True` + `samplesClustered: True` | Enables hierarchical clustering |
| "color spectrum" | `colorSpectrum: ['color1', 'color2', ...]` | Defines gradient colors |
| "color breaks" | `colorSpectrumBreaks: [val1, val2, ...]` | Sets custom value breakpoints |
| "cell markers" | `heatmapCellMarkers: [{variable, sample, shape, color, width}]` | Adds markers to specific cells |
| "no dendrogram" | `showSmpDendrogram: False` + `showVarDendrogram: False` | Hides tree structures |
| "show dendrogram" | `showSmpDendrogram: True` + `showVarDendrogram: True` | Displays tree structures |
| "sample overlay" | `smpOverlays: ['ColumnName']` | Adds metadata overlays to samples |
| "sort by tree" | `sortSmpByTree: True` + `sortVarByTree: True` | Sorts rows/columns by hierarchy |
| "heat mapping" | `heatMapping: 'color'` | Maps values to colors |
| "no cell border" | `heatmapCellBox: False` | Removes cell borders |
| "cell border color" | `heatmapCellBoxColor: 'rgb(255,255,255)'` | Sets cell border color |
| "legend for overlays" | `showSmpOverlaysLegend: True` | Shows overlay legend |
| "marker shape" | `heatmapCellMarkers: [{shape: 'circle'|'square'|'diamond'|'triangle'}]` | Sets marker geometry |

## Key Configuration Parameters

- `graphType`: Always `'Heatmap'` for heatmaps
- `colorSpectrum`: Array of colors for value gradient (e.g., `['navy', 'white', 'firebrick3']`)
- `colorSpectrumBreaks`: Array of numeric values for custom color breakpoints
- `variablesClustered`: Boolean to cluster variables (columns)
- `samplesClustered`: Boolean to cluster samples (rows)
- `showSmpDendrogram`: Boolean to show sample dendrogram
- `showVarDendrogram`: Boolean to show variable dendrogram
- `heatmapCellMarkers`: Array of marker objects with `{variable, sample, shape, color, width, size}`
- `heatmapCellBox`: Boolean to show/hide cell borders
- `heatmapCellBoxColor`: Color for cell borders (e.g., `'rgb(255,255,255)'`)
- `smpOverlays`: Array of metadata column names for sample overlays
- `showSmpOverlaysLegend`: Boolean to show overlay legend
- `sortSmpByTree`: Boolean to sort samples by hierarchical tree
- `sortVarByTree`: Boolean to sort variables by hierarchical tree
- `heatMapping`: `'color'` for value-based color mapping
- `showLegend`: Boolean to show/hide main legend
