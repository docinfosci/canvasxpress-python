import streamlit as st
st.set_page_config(layout="wide")

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXList
from canvasxpress.plot import graph
from canvasxpress.render.streamlit import plot

st.title("Test multi-chart layouts and broadcasting")

chart1 = CanvasXpress(
    data={
        "y": {
            "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "smps": ["Height", "Weight"],
            "data": [
              [ 174, 65.6 ],
              [ 161, 51.6 ],
              [ 194, 80.7 ],
              [ 160, 49.2 ],
              [ 173, 55.2 ],
              [ 151, 48.7 ]
            ]
        }
    },
    config={
        "graphType": "Scatter2D",
        "xAxis": "Height",
        "yAxis": "Weight",
        "theme": "CanvasXpress",
        "title": "Chart 1"
    },
    width=300,
    height=300
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
                [89.9, 61.6]
            ]
        }
    },
    config={
        "graphType": "Scatter2D",
        "xAxis": "Hip",
        "yAxis": "Waist",
        "theme": "CanvasXpress",
        "title": "Chart 2"
    },
    width=300,
    height=300
)

chart3 = CanvasXpress(
    data={
        "y": {
            "vars" : ["Age"],
            "smps" : ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data" : [
              [ 21, 22, 28, 19, 32, 35 ]
            ]
        }
    },
    config={
        "graphType": "Bar",
        "graphOrientation": "vertical",
        "theme": "CanvasXpress",
        "title": "Chart 3"
    },
    width=300,
    height=300
)

chart4 = CanvasXpress(
    data={
        "x": {
            "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"],
            "Exercise": ["Low", "Moderate", "Moderate", "Moderate", "Low", "Intense"]
        },
        "y": {
            "vars": ["Age"],
            "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data": [
                [21, 22, 28, 19, 32, 35]
            ]
        }
    },
    config={
        "graphType": "Bar",
        "theme": "CanvasXpress",
        "title": "Chart 4"
    },
    after_render=CXConfigs(CXList("createTreemap", ["Exercise"])),
    width=300,
    height=300
)

chart5 = CanvasXpress(
    data={
        "x": {
            "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"]
        },
        "y": {
            "vars": ["Age"],
            "smps": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "data": [
                [21, 22, 28, 19, 32, 35]
            ]
        }
    },
    config={
        "graphType": "Bar",
        "theme": "CanvasXpress",
        "title": "Chart 5"
    },
    after_render=CXConfigs(CXList("createPie", ["Gender"])),
    width=300,
    height=300
)

chart6 = CanvasXpress(
    data={
        "z": {
            "Gender": ["Male", "Female", "Male", "Female", "Female", "Female"],
            "Excercise": ["Low", "Moderate", "Moderate", "Moderate", "Low", "Intense"]
        },
        "y": {
            "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
            "smps": ["Age"],
            "data": [
                [21],
                [22],
                [28],
                [19],
                [32],
                [35]
            ]
        }
    },
    config={
        "graphType": "Scatter2D",
        "showHistogram": "true",
        "histogramBins": 5,
        "theme": "CanvasXpress",
        "title": "Chart 6"
    },
    after_render=CXConfigs(CXList("createPie", ["Gender"])),
    width=300,
    height=300
)

plot([chart1, chart2, chart3, chart4, chart5, chart6], columns=3)
