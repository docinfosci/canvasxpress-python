"""
This tutorial is based on Plotly's Dash tutorial series, which begins at:
https://dash.plotly.com/installation

The intention of this tutorial is to demonstrate the CanvasXpress class as a replacement for Plotly's own charts
but retaining the same overall application functionality.

CXDashElement is the essential means by which a CanvasXpress Dash element is added to a user interface.  It accepts
prepared config and event JSON strings to format and enhance a CanvasXpress chart.  CXDashElement is part of the
cxdash package that is bundled with the canvasxpress[dash] and canvasxpress[all] installations.

CanvasXpress is a full-featured component for customizing charts: it eases working with data at the Python tier, and
it simplifies dynamic configuration.  Coupled with supporting components, such as CXDashElementFactory, it makes the
development of dynamic Dash, Flask, Django, Jupyter, and similar solutions easier.
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.=

from dash import Dash, html
from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.dash import CXElementFactory

g_app = Dash(__name__)

# No need to create_element many forms of data into CanvasXpress data objects; for example, use this CSV as-is.
_g_csv = """, Apples, Oranges, Bananas
SF      ,      4,       1,       2
Montreal,      2,       4,       5
"""

_g_cx_colors = {
    "background": "#111111",
    "text": "rgb(127,219,255)",
    "bars": ["rgb(99,110,250)", "rgb(239,85,59)"],
}

# Work with data as normal Python values.  cx_data could also have been a DataFrame, JSON, URL, etc.
_g_cx_chart = CanvasXpress(
    render_to="fruit_consumption",
    data=_g_csv,
    config={
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
    },
    width=650,
    height=450,
)

# Application
g_app.layout = html.Div(
    style={"backgroundColor": _g_cx_colors["background"]},
    children=[
        html.H1(
            children="Hello Dash",
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.H2(
            children=(
                "An Example of the Advanced CanvasXpress and CXDashElementFactory"
                " Classes for Plotting a CanvasXpress Chart"
            ),
            style={"textAlign": "center", "color": _g_cx_colors["text"]},
        ),
        html.Div(
            id="chart-container",
            children=[
                html.Div(
                    id="cx-container",
                    style={"textAlign": "center"},
                    children=CXElementFactory.render(_g_cx_chart),
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    g_app.run_server(debug=False)
