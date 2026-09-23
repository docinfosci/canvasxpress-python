import json

from canvasxpress.canvas import CanvasXpress, _CX_MIME_TYPE


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

    assert set(bundle.keys()) == {"text/plain", "text/html", _CX_MIME_TYPE}


def test_repr_mimebundle_text_plain_matches_repr():
    chart = sample_chart()

    assert chart._repr_mimebundle_()["text/plain"] == repr(chart)


def test_repr_mimebundle_specification_is_json_serializable():
    specification = sample_chart()._repr_mimebundle_()[_CX_MIME_TYPE]

    # The specification travels as JSON, so every value must survive a round
    # trip. Javascript event handlers are deliberately not included.
    assert json.loads(json.dumps(specification)) == specification


def test_repr_mimebundle_specification_carries_the_chart():
    specification = sample_chart()._repr_mimebundle_()[_CX_MIME_TYPE]

    assert specification["config"]["graphType"] == "Bar"
    assert specification["config"]["title"] == "Quarterly Revenue"
    assert specification["data"]["y"]["vars"] == ["Revenue"]
    assert specification["data"]["y"]["data"] == [[10, 14, 9, 17]]


def test_repr_mimebundle_html_is_self_contained():
    html = sample_chart()._repr_mimebundle_()["text/html"]

    assert "<canvas" in html
    assert "new CanvasXpress(" in html
    assert CanvasXpress.js_library_url() in html
    assert CanvasXpress.css_library_url() in html
    # Frontends that do not execute script in HTML output should see a message
    # rather than an empty canvas.
    assert "bar1-cx-fallback" in html


def test_repr_mimebundle_honors_include():
    bundle = sample_chart()._repr_mimebundle_(include=["text/plain"])

    assert set(bundle.keys()) == {"text/plain"}


def test_repr_mimebundle_honors_exclude():
    bundle = sample_chart()._repr_mimebundle_(exclude=["text/html"])

    assert set(bundle.keys()) == {"text/plain", _CX_MIME_TYPE}


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
