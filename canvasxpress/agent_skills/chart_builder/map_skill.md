---
title: "Map Chart Skill"
description: "Generate CanvasXpress map charts with choropleth coloring, zoom control, map projections, metadata coloring, size-based scaling, and animation workflows."
---

# Map Chart Skill

## Overview
Maps visualize geographic data with choropleth shading, marker overlays, and size encoding. CanvasXpress supports multiple map IDs (world, USA states, regions), projections (albers), zoom control, metadata-driven coloring, size-by variables, decoration overlays (pie charts), and workflow animation for temporal data.

## Data Formats

### World Country Data
```python
data = {
  'y': {
    'data': [[0, 0, 2, 2], [1, 1, 1, 3], [0, 3, 1, 4], ...],
    'smps': ['Gold', 'Silver', 'Bronze', 'Total'],
    'vars': ['ALB', 'ARG', 'ARM', 'AUS', 'AUT', ...],
  },
}
```

### USA State Data
```python
data = {
  'y': {
    'data': [[1665573, 692611, 941173, 5893, 25896], ...],
    'smps': ['Total', 'Democrat', 'Republican', 'Libertarian', 'Other'],
    'vars': ['AL', 'AK', 'AZ', 'AR', 'CA', ...],
  },
  'z': {
    'Winner': ['Republican', 'Republican', 'Republican', ...],
  },
}
```

### Geographic Point Data
```python
data = {
  'x': {
    'Latitude': [-17, -14, -22.3, ...],
    'Longitude': [118.5, 156, 162.2, ...],
    'Category': ['mild', 'moderate', 'severe', ...],
    'Year': [1940, 1940, 1940, ...],
  },
  'y': {
    'smps': ['R1', 'R2', ...],
  },
}
```

## Code Examples

### Example 1: World Choropleth (Olympic Medals)
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'y': {
    'data': [[0, 0, 2, 2], [1, 1, 1, 3], [0, 3, 1, 4], [18, 19, 16, 53], ...],
    'smps': ['Gold', 'Silver', 'Bronze', 'Total'],
    'vars': ['ALB', 'ARG', 'ARM', 'AUS', 'AUT', 'AZE', 'BEL', 'BGR', 'BHR', 'BRA', ...],
  },
}
config = {
  'graphType': 'Map',
  'colorBy': 'Total',
  'mapId': 'medals',
  'theme': 'tableau',
  'legendPosition': 'bottom',
  'topoJSON': 'https://www.canvasxpress.org/data/maps/WORLD.json',
  'title': 'Total Number of Olympic Medals in Paris - 2024',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: CO2 Emissions Map
```python
config = {
  'graphType': 'Map',
  'colorBy': 'CO2',
  'mapId': 'countries',
  'theme': 'solarized',
  'legendPosition': 'left',
  'topoJSON': 'https://www.canvasxpress.org/data/maps/WORLD.json',
  'title': 'CO2 Emissions During 2018',
}
```

### Example 3: USA Map with Albers Projection
```python
config = {
  'graphType': 'Map',
  'colorBy': 'Winner',
  'mapId': 'albersStates',
  'mapProjection': 'albers',
  'legendOrder': {'Winner': ['Republican', 'Democrat']},
  'theme': 'wallStreetJournal',
  'topoJSON': 'https://www.canvasxpress.org/data/maps/USA.json',
  'title': '2000 Presidential Elections',
}
```

### Example 4: USA Map with Pie Decorations
```python
config = {
  'graphType': 'Map',
  'colorBy': 'Winner',
  'sizeBy': 'Total',
  'mapId': 'albersStatesPie',
  'mapProjection': 'albers',
  'legendColumns': 4,
  'legendOrder': {'Winner': ['Republican', 'Democrat']},
  'theme': 'wallStreetJournal',
  'decorations': {
    'pie': [{
      'colors': ['blue', 'red', 'yellow', 'green'],
      'size': 2.5,
      'smps': ['Democrat', 'Republican', 'Libertarian', 'Other'],
    }],
  },
  'topoJSON': 'https://www.canvasxpress.org/data/maps/USA.json',
  'title': '2000 Presidential Elections',
}
```

### Example 5: Cyclones Map with Workflow Animation
```python
config = {
  'graphType': 'Map',
  'colorBy': 'variable',
  'colorScheme': 'Bootstrap',
  'markerBy': 'Category',
  'workflowBy': 'Year',
  'legendInside': True,
  'legendPosition': 'bottomLeft',
  'legendTextScaleFontFactor': 0.85,
  'mapConfig': {'zoom': 3},
  'mapId': 'australia',
  'topoJSON': 'https://www.canvasxpress.org/data/maps/AUS.json',
  'title': 'Cyclones in Australia 1940-2020',
}
```

## Agent Prompts

- "Create a CanvasXpress world choropleth map showing Olympic medals by country colored by total."
- "Generate a CO2 emissions map using solarized theme with left-positioned legend."
- "Build a USA map with albers projection coloring states by election winner."
- "Create a USA map with pie decorations showing vote distribution by party."
- "Generate a cyclone map with workflow animation by year and marker by category."
- "Build a map with zoom control (mapConfig: {zoom: 3}) and custom topoJSON URL."
- "Create a choropleth map with color by metadata column and Bootstrap color scheme."
- "Generate a map with size by variable showing total values and colored by category."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "map" | `graphType: 'Map'` | Sets the chart type to map |
| "choropleth" | `colorBy: 'ColumnName'` | Colors regions by data column |
| "world map" | `mapId: 'medals'` or `'countries'` | Uses world map |
| "USA states" | `mapId: 'albersStates'` | Uses USA states map |
| "albers projection" | `mapProjection: 'albers'` | Sets map projection |
| "zoom" | `mapConfig: {'zoom': N}` | Sets zoom level |
| "legend position" | `legendPosition: 'bottom'` | Sets legend location |
| "legend columns" | `legendColumns: N` | Sets legend column count |
| "legend order" | `legendOrder: {'Column': ['A', 'B']}` | Sets legend item order |
| "size by [column]" | `sizeBy: 'ColumnName'` | Sizes regions by data |
| "marker by [column]" | `markerBy: 'ColumnName'` | Colors markers by metadata |
| "workflow by [column]" | `workflowBy: 'ColumnName'` | Enables animation by metadata |
| "decorations" | `decorations: {'pie': [...]}` | Adds overlay decorations |
| "topoJSON URL" | `topoJSON: 'https://...'` | Sets custom map data URL |

## Key Configuration Parameters

- `graphType`: Always `'Map'` for map charts
- `colorBy`: Metadata column for choropleth coloring
- `sizeBy`: Column for sizing regions/markers
- `markerBy`: Column for marker coloring
- `workflowBy`: Column for animation workflow
- `mapId`: Map identifier (e.g., `'medals'`, `'countries'`, `'albersStates'`, `'australia'`)
- `mapProjection`: Projection type (e.g., `'albers'`)
- `mapConfig`: Object with map settings (e.g., `{'zoom': 3}`)
- `theme`: Theme name (e.g., `'tableau'`, `'solarized'`, `'wallStreetJournal'`)
- `legendPosition`: `'bottom'`, `'left'`, `'bottomLeft'`
- `legendInside`: Boolean to place legend inside map
- `legendColumns`: Number of columns in legend
- `legendOrder`: Object mapping columns to ordered values (e.g., `{'Winner': ['Republican', 'Democrat']}`)
- `legendTextScaleFontFactor`: Float for legend text size
- `colorScheme`: Color palette (e.g., `'Bootstrap'`)
- `decorations`: Object with overlay types (e.g., `'pie'` with colors, size, and sample names)
- `topoJSON`: URL to geographic data file
- `title`: Chart title
