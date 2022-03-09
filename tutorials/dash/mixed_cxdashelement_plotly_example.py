import json
import uuid
from math import log, isnan

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

from cxdash import CXDashElement

_g_external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

_g_app = Dash(__name__, external_stylesheets=_g_external_stylesheets)

_g_country_indicators_df = pd.read_csv(
    "https://plotly.github.io/datasets/country_indicators.csv"
)


_g_app.layout = html.Div(
    [
        html.H1(
            "Mixed CanvasXpress and Plotly Graph Example",
            style={"width": "100%", "text-align": "center"},
        ),
        html.Hr(),
        html.Div(
            """
            This Dash application demonstrates a mixture of CanvasXpress and Plotly elements coordinating data
            exchange and UI refresh.  The CXDashElement class is used for preparing CanvasXpress charts, which is
            a straightforward mechanism to use but can require additional work on the developer's part to process 
            or format data, configurations, and events.  Also see the advanced CanvasXpress edition of this example.
            """
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(style={"display": "inline-block", "width": "5%"}),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    _g_country_indicators_df["Indicator Name"].unique(),
                                    "Life expectancy at birth, total (years)",
                                    id="crossfilter-yaxis-column",
                                    style={"display": "inline-block", "width": "85%"},
                                ),
                                dcc.RadioItems(
                                    ["Linear", "Log"],
                                    "Linear",
                                    id="crossfilter-yaxis-type",
                                    style={"display": "inline-block", "width": "15%"},
                                ),
                            ],
                            style={"display": "inline-block", "width": "100%"},
                        ),
                    ],
                    style={"display": "inline-block", "width": "40%"},
                ),
                html.Div(style={"display": "inline-block", "width": "10%"}),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    _g_country_indicators_df["Indicator Name"].unique(),
                                    "Fertility rate, total (births per woman)",
                                    id="crossfilter-xaxis-column",
                                    style={"display": "inline-block", "width": "85%"},
                                ),
                                dcc.RadioItems(
                                    ["Linear", "Log"],
                                    "Linear",
                                    id="crossfilter-xaxis-type",
                                    style={"display": "inline-block", "width": "15%"},
                                ),
                            ],
                            style={"display": "inline-block", "width": "100%"},
                        ),
                    ],
                    style={"display": "inline-block", "width": "40%"},
                ),
                html.Div(style={"display": "inline-block", "width": "5%"}),
            ],
        ),
        html.Div(
            [
                html.Div(style={"display": "inline-block", "width": "2%"}),
                html.Div(
                    dcc.Slider(
                        _g_country_indicators_df["Year"].min(),
                        _g_country_indicators_df["Year"].max(),
                        step=None,
                        id="crossfilter-year--slider",
                        value=_g_country_indicators_df["Year"].max(),
                        marks={
                            str(year): str(year)
                            for year in _g_country_indicators_df["Year"].unique()
                        },
                    ),
                    style={"display": "inline-block", "width": "93%"},
                ),
                html.Div(style={"display": "inline-block", "width": "2%"}),
            ],
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="crossfilter-indicator-scatter",
                            hoverData={"points": [{"customdata": "Japan"}]},
                        ),
                    ],
                    style={"display": "inline-block", "width": "50%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    id="y-time-series",
                                    style={"display": "inline-block", "width": "100%"},
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="x-time-series",
                                    style={"display": "inline-block", "width": "100%"},
                                ),
                            ],
                        ),
                    ],
                    style={"display": "inline-block", "width": "50%"},
                ),
            ],
        ),
        html.Hr(),
    ]
)


@_g_app.callback(
    Output("crossfilter-indicator-scatter", "figure"),
    Input("crossfilter-xaxis-column", "value"),
    Input("crossfilter-yaxis-column", "value"),
    Input("crossfilter-xaxis-type", "value"),
    Input("crossfilter-yaxis-type", "value"),
    Input("crossfilter-year--slider", "value"),
)
def update_graph(
    xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value
):
    dff = _g_country_indicators_df[_g_country_indicators_df["Year"] == year_value]

    fig = px.scatter(
        x=dff[dff["Indicator Name"] == xaxis_column_name]["Value"],
        y=dff[dff["Indicator Name"] == yaxis_column_name]["Value"],
        hover_name=dff[dff["Indicator Name"] == yaxis_column_name]["Country Name"],
    )

    fig.update_traces(
        customdata=dff[dff["Indicator Name"] == yaxis_column_name]["Country Name"]
    )

    fig.update_xaxes(
        title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
    )

    fig.update_yaxes(
        title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
    )

    fig.update_layout(margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest")

    return fig


def adjust_value(value, type):
    if isnan(value):
        return None
    elif type == "Linear":
        return value
    else:
        return log(value)


def format_data_point(data_point, axis_type):
    return [int(data_point[0]), adjust_value(float(round(data_point[1], 2)), axis_type)]


def create_time_series(id, dff, axis_type, title):

    data = {
        "y": {
            "data": [
                format_data_point(
                    dff[["Year", "Value"]].iloc[i].values.tolist(), axis_type
                )
                for i in range(dff["Value"].count())
            ],
            "smps": ["Date", "Value"],
        },
        "z": {"Series": ["Value" for i in range(dff["Value"].count())]},
    }

    config = {
        "graphOrientation": "vertical",
        "graphType": "Scatter2D",
        "lineBy": "Series",
        "smpLabelRotate": 90,
        "yAxisTitle": " ",
        "xAxisTitle": "Year",
        "xAxis2Show": False,
        "showLegend": False,
        "theme": "CanvasXpress",
        "title": pd.unique(dff["Indicator Name"].values)[0],
        "titleAlign": "left",
        "titleScaleFontFactor": 0.65,
        "subtitle": pd.unique(dff["Country Name"].values)[0],
        "subtitleAlign": "left",
        "subtitleScaleFontFactor": 0.5,
    }

    events = """
    {
        "mousemove": function(o, e, t) {
            t.showInfoSpan(e, '<b>' + o.y.data[0][0] + '</b>: ' + o.y.data[0][1]);
        },
        "mouseout": function(o, e, t) {},
    }
    """

    chart = CXDashElement(
        id=str(uuid.uuid4()),
        data=json.dumps(data),
        config=json.dumps(config),
        events=events,
        height="225",
    )

    return [
        chart,
    ]


@_g_app.callback(
    Output("x-time-series", "children"),
    Input("crossfilter-indicator-scatter", "hoverData"),
    Input("crossfilter-xaxis-column", "value"),
    Input("crossfilter-xaxis-type", "value"),
)
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData["points"][0]["customdata"]
    dff = _g_country_indicators_df[
        _g_country_indicators_df["Country Name"] == country_name
    ]
    dff = dff[dff["Indicator Name"] == xaxis_column_name]
    title = "{} {}".format(country_name, xaxis_column_name)
    return create_time_series("x", dff, axis_type, title)


@_g_app.callback(
    Output("y-time-series", "children"),
    Input("crossfilter-indicator-scatter", "hoverData"),
    Input("crossfilter-yaxis-column", "value"),
    Input("crossfilter-yaxis-type", "value"),
)
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = _g_country_indicators_df[
        _g_country_indicators_df["Country Name"] == hoverData["points"][0]["customdata"]
    ]
    dff = dff[dff["Indicator Name"] == yaxis_column_name]
    return create_time_series("y", dff, axis_type, yaxis_column_name)


if __name__ == "__main__":
    _g_app.run_server(debug=False)
