import json
from random import random

from cxdash import CXDashElement
import dash
from dash.dependencies import Input, Output
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            CXDashElement(
                width="300",
                height="400",
                id=f"example_cx",
                data=json.dumps(
                    {
                        "y": {
                            "vars": ["V1"],
                            "smps": ["S1", "S2", "S3", "S4"],
                            "data": [
                                [
                                    random() % 10,
                                    random() % 100,
                                    random() % 10,
                                    random() % 100,
                                ]
                            ],
                        }
                    }
                ),
                config=json.dumps(
                    {
                        "axisAlgorithm": "rPretty",
                        "colors": ["rgb(200,117,180)"],
                        "graphOrientation": "horizontal",
                        "plotBox": True,
                        "plotBoxColor": "#337AB7",
                        "showLegend": False,
                        "smpLabelRotate": 90,
                        "smpTitle": "Samples",
                        "theme": "CanvasXpress",
                        "title": f"Bar Graph Title",
                        "xAxis": ["V1"],
                        "xAxisTitle": "Value",
                    }
                ),
            ),
            id="main-container",
        ),
        html.Div([], id="new-chart-container"),
        html.Button("Change", id="change-btn", n_clicks=0),
    ]
)


@app.callback(
    Output("new-chart-container", "children"),
    Input("change-btn", "n_clicks"),
)
def change(n):
    if not n:
        raise dash.exceptions.PreventUpdate

    else:
        return CXDashElement(
            width="300",
            height="400",
            id=f"example_cx{n}",
            data=json.dumps(
                {
                    "y": {
                        "vars": ["V1"],
                        "smps": ["S1", "S2", "S3", "S4"],
                        "data": [
                            [
                                random() % 10,
                                random() % 100,
                                random() % 10,
                                random() % 100,
                            ]
                        ],
                    }
                }
            ),
            config=json.dumps(
                {
                    "axisAlgorithm": "rPretty",
                    "colors": ["rgb(69,117,180)"],
                    "graphOrientation": "horizontal" if n % 2 == 0 else "vertical",
                    "plotBox": True,
                    "plotBoxColor": "#337AB7",
                    "showLegend": False,
                    "smpLabelRotate": 90,
                    "smpTitle": "Samples",
                    "theme": "CanvasXpress",
                    "title": f"Bar Graph Title",
                    "xAxis": ["V1"],
                    "xAxisTitle": "Value",
                }
            ),
        )


if __name__ == "__main__":
    app.run_server(debug=True)
