"""
The Shiny for Python columns app captured by test_platform_shiny.py: two charts
side by side in `ui.layout_columns`, each filling the width of its column.
"""

from shiny import App, render, ui

from canvasxpress.plot import graph
from canvasxpress.render.shiny import output_canvasxpress
from tests.functional.platform.charts import left_chart, right_chart

app_ui = ui.page_fluid(
    ui.h2("CanvasXpress in Shiny columns"),
    ui.layout_columns(
        output_canvasxpress("left"),
        output_canvasxpress("right"),
        col_widths=(6, 6),
    ),
    title="CanvasXpress platform test",
)


def server(input, output, session):
    @render.ui
    def left():
        return graph(left_chart(), fill_to_width=True)

    @render.ui
    def right():
        return graph(right_chart(), fill_to_width=True)


app = App(app_ui, server)
