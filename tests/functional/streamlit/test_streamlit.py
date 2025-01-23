import random

import streamlit as st

st.set_page_config(layout="wide")

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXList

st.title("CanvasXpress in Streamlit!")

st.write("## Basic Chart")

bar_chart = CanvasXpress(
    config={
        "graphOrientation": "vertical",
        "plotBox": True,
        "showLegend": False,
        "smpLabelRotate": 90,
        "smpTitle": "Samples",
        "theme": "CanvasXpress",
        "title": "Bar Graph Title",
        "xAxis": ["V1"],
        "xAxisTitle": "Value",
        "graphType": "Bar",
    },
    width=500,
    height=500,
)

column1, column2 = st.columns([1, 3])

with column1:
    # This has no associated action, so by default it triggers a redraw of the UI.
    st.button("Generate New Data")

bar_chart.data = {
    "y": {
        "vars": ["V1"],
        "smps": ["S1", "S2", "S3"],
        "data": [
            [
                random.randint(100, 10000),
                random.randint(100, 10000),
                random.randint(100, 10000),
            ]
        ],
    }
}

with column2:
    graph(bar_chart)

st.write("## Broadcasting")

chart1 = CanvasXpress(
    data={
        "y": {
            "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "smps": ["Height", "Weight"],
            "data": [
                [174, 65.6],
                [161, 51.6],
                [194, 80.7],
                [160, 49.2],
                [173, 55.2],
                [151, 48.7],
            ],
        }
    },
    config={
        "graphType": "Scatter2D",
        "xAxis": "Height",
        "yAxis": "Weight",
        "theme": "CanvasXpress",
        "title": "Chart 1",
    },
    width=300,
    height=300,
)

chart2 = CanvasXpress(
    data={
        "y": {
            "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "smps": ["Hip", "Waist"],
            "data": [
                [93.5, 71.5],
                [92, 66.5],
                [95, 83.2],
                [91, 61.2],
                [90.3, 66.5],
                [89.9, 61.6],
            ],
        }
    },
    config={
        "graphType": "Scatter2D",
        "xAxis": "Hip",
        "yAxis": "Waist",
        "theme": "CanvasXpress",
        "title": "Chart 2",
    },
    width=300,
    height=300,
)

chart3 = CanvasXpress(
    data={
        "y": {
            "vars": ["Age"],
            "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data": [[21, 22, 28, 19, 32, 35]],
        }
    },
    config={
        "graphType": "Bar",
        "graphOrientation": "vertical",
        "theme": "CanvasXpress",
        "title": "Chart 3",
    },
    width=300,
    height=300,
)

chart4 = CanvasXpress(
    data={
        "x": {
            "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"],
            "Exercise": ["Low", "Moderate", "Moderate", "Moderate", "Low", "Intense"],
        },
        "y": {
            "vars": ["Age"],
            "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data": [[21, 22, 28, 19, 32, 35]],
        },
    },
    config={"graphType": "Bar", "theme": "CanvasXpress", "title": "Chart 4"},
    after_render=CXConfigs(CXList("createTreemap", ["Exercise"])),
    width=300,
    height=300,
)

chart5 = CanvasXpress(
    data={
        "x": {"Gender": ["Male", "Female", "Male", "Female", "Female", "Female"]},
        "y": {
            "vars": ["Age"],
            "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data": [[21, 22, 28, 19, 32, 35]],
        },
    },
    config={"graphType": "Bar", "theme": "CanvasXpress", "title": "Chart 5"},
    after_render=CXConfigs(CXList("createPie", ["Gender"])),
    width=300,
    height=300,
)

chart6 = CanvasXpress(
    data={
        "z": {
            "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"],
            "Exercise": ["Low", "Moderate", "Moderate", "Moderate", "Low", "Intense"],
        },
        "y": {
            "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "smps": ["Age"],
            "data": [[21], [22], [28], [19], [32], [35]],
        },
    },
    config={
        "graphType": "Scatter2D",
        "showHistogram": "true",
        "histogramBins": 5,
        "theme": "CanvasXpress",
        "title": "Chart 6",
    },
    width=300,
    height=300,
)

col1, col2, col3 = st.columns(3)

with col1:
    graph(chart1)
    graph(chart4)

with col2:
    graph(chart2)
    graph(chart5)

with col3:
    graph(chart3)
    graph(chart6)


st.write("## Other Chart Types")

area_chart: CanvasXpress = CanvasXpress(
    data={
        "y": {
            "data": [[10, 11, 13, 4, 18, 21]],
            "vars": ["Value"],
            "smps": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        }
    },
    config={
        "colorScheme": "Prism",
        "graphOrientation": "vertical",
        "graphType": "Area",
        "smpTextRotate": 90,
        "smpTitle": "Month / First Quarters of 2024",
        "title": "Area graph with one series",
        "titleScaleFontFactor": 1.2,
        "xAxis": ["Value"],
        "xAxisTitle": "Revenue (in Millions)",
    },
)

box_chart: CanvasXpress = CanvasXpress(
    data={
        "y": {
            "vars": ["len"],
            "smps": [
                "V1",
                "V2",
                "V3",
                "V4",
                "V5",
                "V6",
                "V7",
                "V8",
                "V9",
                "V10",
                "V11",
                "V12",
            ],
            "data": [
                [4.2, 10, 16.5, 17.3, 23.6, 32.5, 15.2, 10, 19.7, 25.2, 25.5, 30.9]
            ],
        },
        "x": {
            "dose": [0.5, 0.5, 1, 1, 2, 2, 0.5, 0.5, 1, 1, 2, 2],
            "order": [1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6],
            "supp": [
                "VC",
                "VC",
                "VC",
                "VC",
                "VC",
                "VC",
                "OJ",
                "OJ",
                "OJ",
                "OJ",
                "OJ",
                "OJ",
            ],
        },
    },
    config={
        "graphOrientation": "vertical",
        "graphType": "Boxplot",
        "groupingFactors": ["dose"],
        "showLegend": False,
        "smpTextRotate": 90,
        "smpTitle": "dose",
        "smpTitleFontStyle": "bold",
        "summaryType": "iqr",
        "theme": "CanvasXpress",
        "title": "Box Plot",
        "xAxis": ["len"],
        "xAxisTitle": "len",
    },
)

heatmap_chart: CanvasXpress = CanvasXpress(
    data={
        "y": {
            "vars": ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"],
            "smps": ["S1", "S2", "S3", "S4", "S5"],
            "data": [
                [0.784, 3.879, -0.639, 1.013, 0.47],
                [0.256, 1.53, -1.466, 3.524, -0.542],
                [-0.099, 0.781, -0.379, 0.98, 0.463],
                [-0.876, -0.889, 3.857, -0.432, 4.61],
                [1.693, 0.309, 2.024, -1.429, 4.521],
                [0.957, 0.004, 2.497, -0.034, 3.85],
                [-1.862, 0.924, 5.869, -1.097, 3.055],
                [-0.015, 1.919, 5.379, 0.544, 4.422],
            ],
        }
    },
    config={
        "graphType": "Heatmap",
        "title": "Simple Heatmap",
        "xAxis": ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"],
        "colorSpectrum": ["rgb(0,0,128)", "rgb(255,255,255)", "rgb(205,38,38)"],
    },
)

network_chart: CanvasXpress = CanvasXpress(
    data={
        "nodes": [
            {"id": "Id0", "name": "Myriel", "group": "G01"},
            {"id": "Id1", "name": "Napoleon", "group": "G01"},
            {"id": "Id2", "name": "Mlle. Baptistine", "group": "G01"},
            {"id": "Id3", "name": "Mme. Magloire", "group": "G01"},
            {"id": "Id4", "name": "Countess de Lo", "group": "G01"},
            {"id": "Id5", "name": "Geborand", "group": "G01"},
            {"id": "Id6", "name": "Champtercier", "group": "G01"},
            {"id": "Id7", "name": "Cravatte", "group": "G01"},
            {"id": "Id8", "name": "Count", "group": "G01"},
            {"id": "Id9", "name": "Old Man", "group": "G01"},
            {"id": "Id10", "name": "Labarre", "group": "G02"},
            {"id": "Id11", "name": "Valjean", "group": "G02"},
            {"id": "Id12", "name": "Marguerite", "group": "G03"},
            {"id": "Id13", "name": "Mme. de R", "group": "G02"},
            {"id": "Id14", "name": "Isabeau", "group": "G02"},
            {"id": "Id15", "name": "Gervais", "group": "G02"},
            {"id": "Id16", "name": "Tholomyes", "group": "G03"},
            {"id": "Id17", "name": "Listolier", "group": "G03"},
            {"id": "Id18", "name": "Fameuil", "group": "G03"},
            {"id": "Id19", "name": "Blacheville", "group": "G03"},
            {"id": "Id20", "name": "Favourite", "group": "G03"},
        ],
        "edges": [
            {"id1": "Id1", "id2": "Id0", "value": 1},
            {"id1": "Id2", "id2": "Id0", "value": 8},
            {"id1": "Id3", "id2": "Id0", "value": 10},
            {"id1": "Id3", "id2": "Id2", "value": 6},
            {"id1": "Id4", "id2": "Id0", "value": 1},
            {"id1": "Id5", "id2": "Id0", "value": 1},
            {"id1": "Id6", "id2": "Id0", "value": 1},
            {"id1": "Id7", "id2": "Id0", "value": 1},
            {"id1": "Id8", "id2": "Id0", "value": 2},
            {"id1": "Id9", "id2": "Id0", "value": 1},
            {"id1": "Id11", "id2": "Id10", "value": 1},
            {"id1": "Id11", "id2": "Id3", "value": 3},
            {"id1": "Id11", "id2": "Id2", "value": 3},
            {"id1": "Id11", "id2": "Id0", "value": 5},
            {"id1": "Id12", "id2": "Id11", "value": 1},
            {"id1": "Id13", "id2": "Id11", "value": 1},
            {"id1": "Id14", "id2": "Id11", "value": 1},
            {"id1": "Id15", "id2": "Id11", "value": 1},
            {"id1": "Id17", "id2": "Id16", "value": 4},
            {"id1": "Id18", "id2": "Id16", "value": 4},
            {"id1": "Id18", "id2": "Id17", "value": 4},
            {"id1": "Id19", "id2": "Id16", "value": 4},
            {"id1": "Id19", "id2": "Id17", "value": 4},
            {"id1": "Id19", "id2": "Id18", "value": 4},
        ],
    },
    config={
        "colorNodeBy": "group",
        "graphType": "Network",
        "networkLayoutType": "forceDirected",
    },
)

col_1, col_2 = st.columns(2)

with col_1:
    st.write("### Area")
    graph(area_chart)

    st.write("### Box Plot")
    graph(box_chart)

with col_2:
    st.write("### Heatmap")
    graph(heatmap_chart)

    st.write("### Network")
    graph(network_chart)
