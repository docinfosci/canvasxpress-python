"""
Tests for the IPython display hook of `CanvasXpress`: `_repr_mimebundle_`
renders a chart when it is the result of a notebook cell. The representations
are built by the shared HTML/JS/CSS layer in `canvasxpress.render.context`,
so these tests assert that the hook stays on that layer.
"""

import re

from canvasxpress.canvas import CanvasXpress

_MIME_TYPES = {"text/plain", "text/html", "application/javascript"}


def sample_chart() -> CanvasXpress:
    return CanvasXpress(
        render_to="bar1",
        data={
            "y": {
                "vars": ["Revenue"],
                "smps": ["Q1", "Q2", "Q3", "Q4"],
                "data": [[10, 14, 9, 17]],
            }
        },
        config={"graphType": "Bar", "title": "Quarterly Revenue"},
    )


def test_repr_mimebundle_offers_each_representation():
    bundle = sample_chart()._repr_mimebundle_()

    assert set(bundle.keys()) == _MIME_TYPES


def test_repr_mimebundle_text_plain_matches_repr():
    chart = sample_chart()

    assert chart._repr_mimebundle_()["text/plain"] == repr(chart)


def test_repr_mimebundle_html_is_built_from_the_shared_layer():
    html = sample_chart()._repr_mimebundle_()["text/html"]

    # The shared layout from CXHtmlDocument, not a bespoke wrapper.
    assert 'class="canvasxpress-layout"' in html
    assert '<canvas id="bar1"' in html
    # The shared on-demand loader, with the library URLs of the active
    # CanvasXpress configuration.
    assert "window.canvasxpress.loadLibrary" in html
    assert CanvasXpress.js_library_url() in html
    assert CanvasXpress.css_library_url() in html
    # One properly terminated script element.
    assert html.count("</script>") == 1


def test_repr_mimebundle_javascript_is_the_shared_loader():
    js = sample_chart()._repr_mimebundle_()["application/javascript"]

    assert "window.canvasxpress.loadLibrary" in js
    assert "new CanvasXpress(" in js


def test_repr_mimebundle_html_escapes_chart_script():
    # A </script> sequence in the chart data must not terminate the script
    # element of the output; escape_script() writes it as <\/script instead.
    chart = CanvasXpress(
        render_to="bar2",
        data={
            "y": {
                "vars": ["Revenue"],
                "smps": ["Q1", "</script>"],
                "data": [[10, 14]],
            }
        },
        config={"graphType": "Bar"},
    )

    html = chart._repr_mimebundle_()["text/html"]

    assert "<\\/script" in html
    assert html.count("</script>") == 1


def test_repr_mimebundle_anonymous_chart_has_one_id():
    # An anonymous chart mints a new ID on each access, so the canvas element
    # and the chart's renderTo must agree within the output.
    chart = CanvasXpress(
        data={
            "y": {
                "vars": ["Revenue"],
                "smps": ["Q1", "Q2"],
                "data": [[10, 14]],
            }
        },
        config={"graphType": "Bar"},
    )

    assert chart.anonymous

    html = chart._repr_mimebundle_()["text/html"]

    canvas_id = re.search(r'<canvas id="([^"]+)"', html).group(1)
    render_to = re.search(r'"renderTo": "([^"]+)"', html).group(1)

    assert canvas_id == render_to


def test_repr_mimebundle_loads_the_license():
    chart = sample_chart()
    chart.license_url = "https://example.com/CanvasXpressLicense.js"

    bundle = chart._repr_mimebundle_()

    assert "https://example.com/CanvasXpressLicense.js" in bundle["text/html"]
    assert (
        "https://example.com/CanvasXpressLicense.js" in bundle["application/javascript"]
    )


def test_repr_mimebundle_honors_include():
    bundle = sample_chart()._repr_mimebundle_(include=["text/plain"])

    assert set(bundle.keys()) == {"text/plain"}


def test_repr_mimebundle_honors_exclude():
    bundle = sample_chart()._repr_mimebundle_(exclude=["text/html"])

    assert set(bundle.keys()) == {"text/plain", "application/javascript"}


def test_repr_mimebundle_include_and_exclude_together():
    bundle = sample_chart()._repr_mimebundle_(
        include=["text/plain", "text/html"], exclude=["text/html"]
    )

    assert set(bundle.keys()) == {"text/plain"}


def test_repr_mimebundle_does_not_disturb_the_chart():
    chart = sample_chart()
    before = repr(chart)

    chart._repr_mimebundle_()

    assert repr(chart) == before
