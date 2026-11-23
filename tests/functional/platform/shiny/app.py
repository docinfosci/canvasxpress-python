"""
The minimal Shiny for Python app captured by test_platform_shiny.py: one chart
at its configured size, and one that fills the width of the page.
"""

from shiny import App, render, ui

from canvasxpress.plot import graph
from canvasxpress.render.shiny import output_canvasxpress
from tests.functional.platform.charts import fill_chart, fixed_chart

app_ui = ui.page_fluid(
    ui.h2("CanvasXpress in Shiny"),
    output_canvasxpress("fixed"),
    output_canvasxpress("fill"),
    title="CanvasXpress platform test",
)


def server(input, output, session):
    @render.ui
    def fixed():
        return graph(fixed_chart())

    @render.ui
    def fill():
        return graph(fill_chart(), fill_to_width=True)


app = App(app_ui, server)
