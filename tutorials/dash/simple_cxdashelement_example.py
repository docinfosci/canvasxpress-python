"""
This tutorial is based on Plotly's Dash tutorial series, which begins at:
https://dash.plotly.com/installation

The intention of this tutorial is to demonstrate the basic CXDashElement class as a replacement for Plotly's own charts
but retaining the same overall application functionality.

CXDashElement is the essential means by which a CanvasXpress Dash element is added to a user interface.  It accepts
prepared config and event JSON strings to format and enhance a CanvasXpress chart.  CXDashElement is part of the
cxdash package that is bundled with the canvasxpress[dash] and canvasxpress[all] installations.
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
from dash import Dash, html
import cxdash

g_app = Dash(__name__)

# CanvasXpress chart configuration
_g_cx_data = {
    "y": {
        "smps": ["Apples", "Oranges", "Bananas"],
        "vars": ["SF", "Montreal"],
        "data": [
            [4, 1, 2],
            [2, 4, 5],
        ],
    },
}

_g_cx_colors = {
    "background": "#111111",
    "text": "rgb(127,219,255)",
    "bars": ["rgb(99,110,250)", "rgb(239,85,59)"],
}

_g_cx_config: dict = {
    "colors": _g_cx_colors["bars"],
    "graphOrientation": "vertical",
    "smpLabelRotate": 90,
    "plotBox": True,
    "plotBoxColor": "White",
    "background": _g_cx_colors["background"],
    "theme": "Plotly",
    "xAxis": ["Fruit", "City"],
    "xAxisTitle": "Amount",
    "xAxis2Show": False,
    "xAxisMinorTicks": False,
    "axisTitleColor": _g_cx_colors["text"],
    "axisTickColor": _g_cx_colors["text"],
    "legendColor": _g_cx_colors["text"],
    "smpTitle": "Fruit",
    "smpTitleFontColor": _g_cx_colors["text"],
    "smpLabelFontColor": _g_cx_colors["text"],
}

# Application
g_app.layout = html.Div(
    style={"backgroundColor": _g_cx_colors["background"]},
    children=[
        html.H1(
            children="Hello Dash",
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.H2(
            children="An Example of the Basic CXDashElement Class for Plotting a CanvasXpress Chart",
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.Div(
            id="chart-container",
            children=[
                html.Div(
                    id="cx-container",
                    style={"textAlign": "center"},
                    children=[
                        cxdash.CXDashElement(
                            id="example-cx",
                            data=json.dumps(_g_cx_data),
                            config=json.dumps(_g_cx_config),
                            width="600",
                            height="400",
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    g_app.run_server(debug=False)
