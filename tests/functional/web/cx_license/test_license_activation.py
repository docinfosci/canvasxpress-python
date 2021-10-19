import pkg_resources
import pytest
from flask import Flask, render_template
from flask import url_for

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
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

    @app.route("/license")
    def get_canvasxpress_python_chart_with_license() -> str:
        """
        Renders a CanvasXpress example using Python that adapts a Javascript
        examples from the canvasxpress.org site.
        """
        chart: CanvasXpress = CanvasXpress(
            render_to="canvasId",
            data=CXDictData(data),
            config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
        )

        chart.license_url = "file://" + pkg_resources.resource_filename(
            __package__, "static/CanvasXpressLicense.js"
        )

        html_parts = chart.render_to_html_parts()
        return render_template(
            "license.html",
            canvasxpress_license=html_parts["cx_license"],
            canvas_element=html_parts["cx_canvas"],
            bar_graph=html_parts["cx_js"],
        )

    return app


@pytest.fixture
def app() -> Flask:
    flask_app_for_license = create_app()
    return flask_app_for_license


@pytest.mark.usefixtures("live_server")
def test_license_activation(app, tmp_path):
    """
    This test ensures that the license file can be incorporated into the output
    for CanvasXpress objects.  The license must be provided by whomever is
    running the test -- if the license is missing this test is skipped.
    """

    # Identify the location of the test page URL
    python_url: str = url_for(
        "get_canvasxpress_python_chart_with_license", _external=True
    )

    with ChromeManagedBrowser(python_url) as py_browser:
        py_browser.session.set_window_size(800, 800)
        assert py_browser.session.find_element_by_id("canvasId") is not None
        print(py_browser.session.page_source)
        assert "CanvasXpressLicense.js" in py_browser.session.page_source
