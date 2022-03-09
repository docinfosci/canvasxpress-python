from math import log, isnan

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

from canvasxpress.canvas import CanvasXpress
from canvasxpress.data.matrix import CXDataframeData
from canvasxpress.js.function import CXEvent
from canvasxpress.render.dash import CXElementFactory

_g_external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
_g_app = Dash(__name__, external_stylesheets=_g_external_stylesheets)
_g_country_indicators_df = pd.read_csv(
    "https://plotly.github.io/datasets/country_indicators.csv"
)

_g_common_config = {
    "graphOrientation": "vertical",
    "graphType": "Scatter2D",
    "lineBy": "Series",
    "smpLabelRotate": 90,
    "yAxisTitle": " ",
    "xAxisTitle": "Year",
    "xAxis2Show": False,
    "showLegend": False,
    "theme": "CanvasXpress",
    "titleAlign": "left",
    "titleScaleFontFactor": 0.65,
    "subtitleAlign": "left",
    "subtitleScaleFontFactor": 0.5,
}

_g_common_events = [
    CXEvent(
        id="mousemove",
        script="t.showInfoSpan(e, '<b>' + o.y.data[0][0] + '</b>: ' + o.y.data[0][1]);",
    ),
    CXEvent(id="mouseout", script=""),
]

# Establish the essential X axis chart configuration.  Only data and data specific configurations will be
# adjusted during the app's use.
_g_x_time_series_chart = CanvasXpress(
    render_to=None,
    config=_g_common_config,
    events=_g_common_events,
    height=225,
)

# Establish the essential Y axis chart configuration.  Only data and data specific configurations will be
# adjusted during the app's use.
_g_y_time_series_chart = CanvasXpress(
    render_to=None,
    config=_g_common_config,
    events=_g_common_events,
    height=225,
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
            exchange and UI refresh.  The CanvasXpress class is used for preparing CanvasXpress charts, and the 
            CXDashElementFactory is used to provide properly configured Dash elements for display.
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


@_g_app.callback(
    Output("x-time-series", "children"),
    Input("crossfilter-indicator-scatter", "hoverData"),
    Input("crossfilter-xaxis-column", "value"),
    Input("crossfilter-xaxis-type", "value"),
)
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    global _g_x_time_series_chart

    country_name = hoverData["points"][0]["customdata"]
    dff = _g_country_indicators_df[
        _g_country_indicators_df["Country Name"] == country_name
        ]
    dff = dff[dff["Indicator Name"] == xaxis_column_name]

    dff.drop(columns=["Country Name", "Indicator Name"], inplace=True)

    dff.Value.apply(lambda x: None if isnan(x) else x)
    dff.Value.apply(lambda x: x if axis_type == "Linear" else log(x))

    data = CXDataframeData(dff)
    data.profile.smps = ["Year", "Value"]
    data.profile.z = {
        "z": {"Series": ["Value" for i in range(dff["Value"].count())]},
    }

    _g_x_time_series_chart.data = data
    _g_x_time_series_chart.config.set_param("title", xaxis_column_name)
    _g_x_time_series_chart.config.set_param("subtitle", country_name)

    return CXElementFactory.render(_g_x_time_series_chart)


@_g_app.callback(
    Output("y-time-series", "children"),
    Input("crossfilter-indicator-scatter", "hoverData"),
    Input("crossfilter-yaxis-column", "value"),
    Input("crossfilter-yaxis-type", "value"),
)
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    global _g_y_time_series_chart

    country_name = hoverData["points"][0]["customdata"]
    dff = _g_country_indicators_df[
        _g_country_indicators_df["Country Name"] == country_name
        ]
    dff = dff[dff["Indicator Name"] == yaxis_column_name]

    dff.drop(columns=["Country Name", "Indicator Name"], inplace=True)

    dff.Value.apply(lambda x: None if isnan(x) else x)
    dff.Value.apply(lambda x: x if axis_type == "Linear" else log(x))

    data = CXDataframeData(dff)
    data.profile.z = {
        "z": {"Series": ["Series" for i in range(dff["Value"].count())]},
    }

    _g_y_time_series_chart.data = data
    _g_y_time_series_chart.config.set_param("title", yaxis_column_name)
    _g_y_time_series_chart.config.set_param("subtitle", country_name)

    return CXElementFactory.render(_g_y_time_series_chart)


if __name__ == "__main__":
    _g_app.run_server(debug=False)
