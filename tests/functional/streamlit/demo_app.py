import random

import streamlit as st

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
from canvasxpress.js.function import CXEvent

# A basic bar chart.  It's anonymous, so no render_to.  Data is added during the draw phase.
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
        "graphType": "Bar"
    },
    width=500,
    height=500,
    events=[
        CXEvent(
            id="click",
            script="""
            var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
            t.showInfoSpan(e, s);
            """
        ),
    ]
)

# Write the UI to the browser
# This code will be re-executed with each click of the button

# Name the theme
st.title('CanvasXpress in Streamlit!')

# Some columns to organize the button and chart
column1, column2 = st.columns(2)

# A column with our data generator button
column1.write(
    # This has no associated action, so by default it triggers a redraw of the UI.
    st.button("Generate New Data")
)

# Another column with the chart displayed
# With each redraw generate new random values
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
        ]
    }
}
column2.write(
    # This plots the CanvasXpress chart into the UI.
    graph(bar_chart)
)