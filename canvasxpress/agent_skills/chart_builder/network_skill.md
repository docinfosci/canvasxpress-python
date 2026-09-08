---
title: "Network Chart Skill"
description: "Generate CanvasXpress network graphs with force-directed layouts, node coloring by metadata, edge weights, and Barnes-Hut simulation for large graphs."
---

# Network Chart Skill

## Overview
Network charts visualize relationships and connections between entities. CanvasXpress supports force-directed layouts with Barnes-Hut simulation for large graphs, node metadata coloring, edge weights, group-based coloring, and smooth animations for network exploration.

## Data Formats

### Nodes and Edges with Groups
```python
data = {
  'nodes': [
    {'id': 'Id0', 'name': 'Valjean', 'group': 1},
    {'id': 'Id1', 'name': 'Myriel', 'group': 2},
    {'id': 'Id2', 'name': 'Madeleine', 'group': 1},
    ...
  ],
  'edges': [
    {'id1': 'Id1', 'id2': 'Id0', 'value': 1},
    {'id1': 'Id2', 'id2': 'Id0', 'value': 8},
    {'id1': 'Id3', 'id2': 'Id0', 'value': 10},
    ...
  ],
}
```

## Code Examples

### Example 1: Les Misérable Network
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph

data = {
  'nodes': [
    {'id': 'Id0', 'name': 'Valjean', 'group': 1},
    {'id': 'Id1', 'name': 'Myriel', 'group': 2},
    {'id': 'Id2', 'name': 'Madeleine', 'group': 1},
    {'id': 'Id3', 'name': 'Marguerite', 'group': 3},
    ...
  ],
  'edges': [
    {'id1': 'Id1', 'id2': 'Id0', 'value': 1},
    {'id1': 'Id2', 'id2': 'Id0', 'value': 8},
    {'id1': 'Id3', 'id2': 'Id0', 'value': 10},
    {'id1': 'Id3', 'id2': 'Id2', 'value': 6},
    ...
  ],
}
config = {
  'graphType': 'Network',
  'networkLayoutType': 'forceDirected',
  'colorNodeBy': 'group',
  'colorSpectrum': ['purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red'],
  'showAnimation': True,
  'title': 'Les Miserable',
}
cx = CanvasXpress(data=data, config=config)
graph(cx)
```

### Example 2: Network with Barnes-Hut Simulation
```python
config = {
  'graphType': 'Network',
  'networkLayoutType': 'forceDirected',
  'colorNodeBy': 'group',
  'colorSpectrum': ['purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red'],
  'showAnimation': True,
  'useBarnesHutSimulation': True,
  'title': 'Les Miserable',
}
```

## Agent Prompts

- "Create a CanvasXpress network graph showing character relationships with force-directed layout."
- "Generate a network visualization with nodes colored by group using a 7-color spectrum."
- "Build a network chart with edge weights representing interaction frequency."
- "Create a Les Misérable network graph with group-based coloring and Barnes-Hut simulation."
- "Generate a network chart with animation enabled for smooth layout transitions."
- "Build a network graph with nodes having id, name, and group properties."
- "Create a network with edges connecting nodes by id1/id2 and value weights."
- "Generate a network chart using force-directed layout with custom color spectrum."

## Prompt-to-Config Mapping

| User Request Element | Config Parameter | Description |
|---------------------|------------------|-------------|
| "network graph" | `graphType: 'Network'` | Sets the chart type |
| "force-directed" | `networkLayoutType: 'forceDirected'` | Sets force layout |
| "color by [column]" | `colorNodeBy: 'ColumnName'` | Colors nodes by metadata |
| "color spectrum" | `colorSpectrum: ['purple', ...]` | Sets node colors |
| "animation" | `showAnimation: True` | Enables smooth animation |
| "Barnes-Hut" | `useBarnesHutSimulation: True` | Optimizes large graphs |
| "edge weight" | `edges: [{..., 'value': N}]` | Edge value controls thickness |
| "node groups" | `nodes: [{..., 'group': N}]` | Node metadata for coloring |
| "character relationships" | `graphType: 'Network'` | Network type |
| "interaction frequency" | `edges: [{..., 'value': N}]` | Weight data |

## Key Configuration Parameters

- `graphType`: Always `'Network'` for network charts
- `networkLayoutType`: `'forceDirected'` for force-based layout
- `colorNodeBy`: Metadata column name for node coloring
- `colorSpectrum`: Array of colors for node groups
- `showAnimation`: Boolean to enable layout animation
- `useBarnesHutSimulation`: Boolean to optimize large graphs
- `nodes`: Array of node objects with `id`, `name`, and metadata
- `edges`: Array of edge objects with `id1`, `id2`, and `value`
