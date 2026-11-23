"""
The minimal Dash app captured by test_platform_dash.py: one chart at its
configured size, and one that fills the width of the page.

Run with the port in the PORT environment variable.
"""

import os

from dash import Dash, html

from canvasxpress.plot import graph
from tests.functional.platform.charts import fill_chart, fixed_chart

app = Dash(__name__, title="CanvasXpress platform test")

app.layout = html.Div(
    [
        html.H2("CanvasXpress in Dash"),
        graph(fixed_chart()),
        graph(fill_chart(), fill_to_width=True),
    ],
    style={"fontFamily": "sans-serif", "padding": "16px"},
)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["PORT"]), debug=False)
