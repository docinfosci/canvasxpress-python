from random import random
from string import ascii_lowercase

import pkg_resources
import pytest
from flask import Flask, render_template
from flask import url_for
from pandas import DataFrame
from selenium.webdriver.common.by import By

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.matrix import CXDataframeData
from tests.util.web.platform.browser.chrome import ChromeManagedBrowser


def create_app() -> Flask:
    app: Flask = Flask(
        "test_flask_server",
        template_folder=pkg_resources.resource_filename(__package__, "templates"),
    )

    app.config["TESTING"] = True
    app.config["LIVESERVER_PORT"] = 8888
    app.config["LIVESERVER_TIMEOUT"] = 10

    header = ["Index", "Col1", "Col2", "Col3"]
    LETTERS = {index: letter for index, letter in enumerate(ascii_lowercase, start=1)}
    rows = [[LETTERS[i + 1], random(), random(), random()] for i in range(10)]
    data: DataFrame = DataFrame(columns=header, data=rows)
    data.set_index(keys="Index", inplace=True)

    @app.route("/chart")
    def get_chart() -> str:
        """
        Renders a CanvasXpress example using Python that adapts a Javascript
        examples from the canvasxpress.org site.
        """
        configs = CXConfigs(CXGraphType(CXGraphTypeOptions.Line))
        configs.set_param("graphOrientation", "vertical")

        chart: CanvasXpress = CanvasXpress(
            render_to="cx_chart", data=CXDataframeData(data), config=configs
        )

        html_parts = chart.render_to_html_parts()
        return render_template(
            "chart.html",
            canvas_element=html_parts["cx_canvas"],
            cx_function=html_parts["cx_js"],
        )

    return app


@pytest.fixture
def app() -> Flask:
    flask_app_for_chart = create_app()
    return flask_app_for_chart


@pytest.mark.usefixtures("live_server")
def test_chart_render(app, tmp_path):
    python_url: str = url_for("get_chart", _external=True)

    with ChromeManagedBrowser(python_url) as py_browser:
        py_browser.session.set_window_size(800, 800)
        assert py_browser.session.find_element(By.ID, "cx_chart") is not None
