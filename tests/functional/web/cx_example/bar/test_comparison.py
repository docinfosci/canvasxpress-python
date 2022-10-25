import json
from pathlib import Path

import pkg_resources
import pytest
from flask import Flask, render_template
from flask import url_for
from selenium.webdriver.common.by import By

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions, CXString
from canvasxpress.data.keypair import CXDictData
from tests.util.visual.image import image_files_match
from tests.util.web.platform.browser.chrome import ChromeManagedBrowser


def create_app() -> Flask:
    app: Flask = Flask(
        "test_flask_server",
        template_folder=pkg_resources.resource_filename(__package__, "templates"),
    )

    app.config["TESTING"] = True
    app.config["LIVESERVER_PORT"] = 8888
    app.config["LIVESERVER_TIMEOUT"] = 10

    data: dict = {
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 35, 88]],
        }
    }

    @app.route("/js")
    def get_canvasxpress_js_chart() -> str:
        """
        Renders a CanvasXpress example using standard Javascript from the
        canvasxpress.org site.
        """
        chart: dict = {
            "renderTo": "canvasId",
            "data": data,
            "config": {"graphType": "Bar"},
        }

        return render_template(
            "bar.html",
            canvas_element="<canvas id='canvasId' width='500' height='500'"
            " responsive='true'>",
            bar_graph=f"var cXcanvasId = new CanvasXpress({json.dumps(chart)});",
        )

    @app.route("/python")
    def get_canvasxpress_python_chart() -> str:
        """
        Renders a CanvasXpress example using Python that adapts a Javascript
        examples from the canvasxpress.org site.
        """
        chart: CanvasXpress = CanvasXpress(
            render_to="canvasId",
            data=CXDictData(data),
            config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
        )

        html_parts = chart.render_to_html_parts()
        return render_template(
            "bar.html",
            canvas_element=html_parts["cx_canvas"],
            bar_graph=html_parts["cx_js"],
        )

    return app


@pytest.fixture
def app() -> Flask:
    app = create_app()
    return app


@pytest.mark.usefixtures("live_server")
def test_js_vs_python_bar_example(app, tmp_path):
    """
    Establish matching charts using a typical Javascript example from
    canvasxpress.org and compare the rendered chart to one created by the
    Python package.  The charts should be identical.
    """

    # Identify the location of URLs for each test
    js_url: str = url_for("get_canvasxpress_js_chart", _external=True)
    python_url: str = url_for("get_canvasxpress_python_chart", _external=True)

    js_chart_png = Path(tmp_path).joinpath("js_chart.png")
    py_chart_png = Path(tmp_path).joinpath("py_chart.png")

    # Render each chart and get the image
    with ChromeManagedBrowser(js_url) as js_browser:
        js_browser.session.set_window_size(800, 800)
        js_chart = js_browser.session.find_element(By.ID, "canvasId")
        js_chart.screenshot(str(js_chart_png))

        with ChromeManagedBrowser(python_url) as py_browser:
            py_browser.session.set_window_size(800, 800)
            py_chart = py_browser.session.find_element(By.ID, "canvasId")
            py_chart.screenshot(str(py_chart_png))

    # Compare images
    ssim = image_files_match(js_chart_png, py_chart_png)
    assert ssim >= 0.95
