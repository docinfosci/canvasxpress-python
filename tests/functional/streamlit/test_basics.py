import streamlit as st
st.set_page_config(layout="wide")

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.render.streamlit import plot

st.title("Test CanvasXpress rendering functions in different Streamlit layouts")
st.write("""
Test that the `canvasxpress.plot.graph` and `canvasxpress.render.streamlit.plot` functions 
both successfully render CX charts within different Streamlit layouts.
""")


common_config = {
    "graphOrientation": "vertical",
    "plotBox": True,
    "showLegend": False,
    "smpLabelRotate": 90,
    "smpTitle": "Samples",
    "theme": "CanvasXpress",
    "xAxis": ["V1"],
    "xAxisTitle": "Value",
    "graphType": "Bar"
}

chart1 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 35, 88]]
        }
    },
    config={**common_config, "title": "Chart 1"}
)

chart2 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 40, 30]]
        }
    },
    config={**common_config, "title": "Chart 2"}
)

chart3 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 5, 9]]
        }
    },
    config={**common_config, "title": "Chart 3"}
)

chart4 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 5, 9]]
        }
    },
    config={**common_config, "title": "Chart 4"}
)

chart5 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[40, 30, 10]]
        }
    },
    config={**common_config, "title": "Chart 5"}
)

chart6 = CanvasXpress(
    data={
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[-3, 5, -2]]
        }
    },
    config={**common_config, "title": "Chart 6"}
)

st.write("## Charts rendered individually")
graph(chart1)
plot(chart2)

st.write("## Charts rendered individually in Streamlit 2 columns layout")
st.write("### Using context manager for columns layout")
st.write("These should be side by side")
column1, column2 = st.columns(2)

with column1:
    graph(chart3)

with column2:
    plot(chart4)


st.write("## Charts rendered individually in Streamlit 2 columns layout")
st.write("### Using `.write()` on column elements")
st.write("These should be side by side")
col1, col2 = st.columns(2)

col1.write(
    graph(chart5)
)

col2.write(
    plot(chart6)
)