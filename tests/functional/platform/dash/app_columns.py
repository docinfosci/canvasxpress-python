"""
The Dash columns app captured by test_platform_dash.py: two charts side by side
in a flex row of equal columns, each filling the width of its column.

Run with the port in the PORT environment variable.
"""

import os

from dash import Dash, html

from canvasxpress.plot import graph
from tests.functional.platform.charts import left_chart, right_chart

app = Dash(__name__, title="CanvasXpress platform test")

# Equal columns: each grows from a zero basis, and may shrink below the width of
# its chart, so the charts follow the columns rather than set them.
_COLUMN = {"flex": "1 1 0", "minWidth": 0}

app.layout = html.Div(
    [
        html.H2("CanvasXpress in Dash columns"),
        html.Div(
            [
                html.Div(graph(left_chart(), fill_to_width=True), style=_COLUMN),
                html.Div(graph(right_chart(), fill_to_width=True), style=_COLUMN),
            ],
            style={"display": "flex", "gap": "16px"},
        ),
    ],
    style={"fontFamily": "sans-serif", "padding": "16px"},
)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["PORT"]), debug=False)
