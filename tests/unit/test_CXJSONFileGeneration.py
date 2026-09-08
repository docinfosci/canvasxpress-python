import json

import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.render.json import CXJSON

# Example from https://www.canvasxpress.org/examples/bar-1.html
cx_example = CanvasXpress(
    render_to="bar1",
    data={
        "y": {
            "data": [[4, 5, 4, 4, 7]],
            "smps": ["Cat 1", "Cat 2", "Cat 3", "Cat 4", "Cat 5"],
            "vars": ["Var 1"],
        }
    },
    config={
        "graphOrientation": "vertical",
        "graphType": "Bar",
        "showLegend": False,
        "smpTextRotate": 90,
        "smpTitle": "Categories",
        "title": "Bar graph with a single series",
        "xAxis": ["Var 1"],
        "xAxisTitle": "Var 1",
    },
)


def test_CXJSONFileGeneration_init_valid_input():
    """
    Test that a CXJSON object can be initialized with a valid CanvasXpress chart.
    """
    render: CXJSON = CXJSON(cx_example)
    assert render.canvas == cx_example


def test_CXJSONFileGeneration_init_invalid_input():
    """
    Test that initializing CXJSON with non-chart values raises a TypeError.
    """
    for sample in [1, "1", [12, 13], 4.5]:
        with pytest.raises(TypeError):
            CXJSON(sample)


def test_CXJSONFileGeneration_init_none():
    """
    Test that initializing CXJSON with None results in no tracked canvas.
    """
    render: CXJSON = CXJSON(None)
    assert render.canvas is None


def test_CXJSONFileGeneration_set_canvas_invalid():
    """
    Test that assigning non-chart values to the canvas property raises a TypeError.
    """
    render: CXJSON = CXJSON()
    for sample in [1, "1", [12, 13], 4.5]:
        with pytest.raises(TypeError):
            render.canvas = sample


def test_CXJSONFileGeneration_data_rendered_successfully():
    """
    Test that the data section of the generated JSON matches the chart data.
    """
    output = json.loads(CXJSON.render_to_json(cx_example))
    assert output["data"] == cx_example.data.data


def test_CXJSONFileGeneration_config_rendered_successfully():
    """
    Test that the config section of the generated JSON matches the chart config.
    """
    output = json.loads(CXJSON.render_to_json(cx_example))
    assert output["config"] == cx_example.config.render_to_dict()


def test_CXJSONFileGeneration_render_to_json_valid_json():
    """
    Test that render_to_json returns a string parseable as a JSON dict.
    """
    result = CXJSON.render_to_json(cx_example)

    assert isinstance(result, str)
    parsed = json.loads(result)
    assert isinstance(parsed, dict)


def test_CXJSONFileGeneration_render_to_json_top_level_keys():
    """
    Test that the generated JSON contains all expected top-level keys.
    """
    parsed = json.loads(CXJSON.render_to_json(cx_example))

    expected_keys = [
        "version",
        "renderTo",
        "data",
        "config",
        "events",
        "info",
        "afterRender",
        "noValidate",
        "factory",
        "system",
    ]
    for key in expected_keys:
        assert key in parsed, f"missing top-level key: {key}"


def test_CXJSONFileGeneration_render_to_json_chart_sections():
    """
    Test that the renderTo, data, config, events, and afterRender sections are correct.
    """
    parsed = json.loads(CXJSON.render_to_json(cx_example))

    assert parsed["renderTo"] == "bar1"
    assert parsed["version"] is not None
    assert parsed["data"]["y"]["vars"] == ["Var 1"]
    assert parsed["config"]["graphType"] == "Bar"
    assert parsed["events"] == {}
    assert parsed["afterRender"] == []


def test_CXJSONFileGeneration_render_to_json_factory_sections():
    """
    Test that the factory section contains the expected environment details.
    """
    parsed = json.loads(CXJSON.render_to_json(cx_example))

    factory = parsed["factory"]
    assert "version" in factory
    assert factory["version"] is not None
    assert "buildDate" in factory
    assert "client" in factory
    assert factory["siteSrc"] is True
    assert "href" in factory
    assert "services" in factory


def test_CXJSONFileGeneration_render_to_json_system_sections():
    """
    Test that the system section contains the expected environment details.
    """
    parsed = json.loads(CXJSON.render_to_json(cx_example))

    system = parsed["system"]
    assert "browser" in system
    assert "browserVersion" in system
    assert "os" in system
    assert "isShiny" in system
    assert "isJupyter" in system


def test_CXJSONFileGeneration_after_render_extra_preserved():
    """
    Test that trailing afterRender values are preserved in the generated JSON.
    """
    chart = CanvasXpress(
        render_to="bar1",
        data=cx_example.data,
        config=cx_example.config,
        after_render=CXConfigs(["setDimensions", [525, 596], "context", "flag", 0]),
    )
    parsed = json.loads(CXJSON.render_to_json(chart))

    assert parsed["afterRender"] == [
        ["setDimensions", [525, 596], "context", "flag", 0]
    ]


def test_CXJSONFileGeneration_multiple_after_render_entries():
    """
    Test that multiple afterRender entries are preserved in order.
    """
    chart = CanvasXpress(
        render_to="bar1",
        data=cx_example.data,
        config=cx_example.config,
        after_render=CXConfigs(
            ["setDimensions", [525, 596]],
            ["setPixelsPerPoint", [7]],
        ),
    )
    parsed = json.loads(CXJSON.render_to_json(chart))

    assert parsed["afterRender"] == [
        ["setDimensions", [525, 596]],
        ["setPixelsPerPoint", [7]],
    ]


def test_CXJSONFileGeneration_render_to_json_none_chart_raises():
    """
    Test that rendering a None chart raises a ValueError.
    """
    with pytest.raises(ValueError):
        CXJSON.render_to_json(None)


def test_CXJSONFileGeneration_render_to_json_reproducible():
    """
    Test that rendering the same chart twice produces identical JSON.
    """
    first_chart_temp = CXJSON.render_to_json(cx_example)
    second_chart_temp = CXJSON.render_to_json(cx_example)
    assert first_chart_temp == second_chart_temp


def test_CXJSONFileGeneration_file_roundtrip(tmp_path):
    """
    Test that generated JSON can be written to and read back from a file.
    """
    generated = CXJSON.render_to_json(cx_example)

    target = tmp_path / "chart_reproducible.json"
    target.write_text(generated)

    assert target.read_text() == generated
    loaded_data = json.loads(target.read_text())
    assert loaded_data["renderTo"] == "bar1"


def test_CXJSONFileGeneration_render_none_canvas_returns_empty_list():
    """
    Test that rendering with no tracked canvas returns an empty list.
    """
    render_chart = CXJSON(None)
    assert render_chart.render() == []


def test_CXJSONFileGeneration_render_single_chart_returns_one_json():
    """
    Test that rendering a single chart returns a list of one JSON string.
    """
    render_chart = CXJSON(cx_example)
    results = render_chart.render()

    assert isinstance(results, list)
    assert len(results) == 1
    parsed = json.loads(results[0])
    assert parsed["renderTo"] == "bar1"


def test_CXJSONFileGeneration_render_list_of_charts_returns_all():
    """
    Test that rendering multiple charts returns JSON for each in order.
    """
    chart1 = CanvasXpress(
        render_to="bar1",
        data=cx_example.data,
        config=cx_example.config,
    )
    chart2 = CanvasXpress(
        render_to="bar2",
        data=cx_example.data,
        config=cx_example.config,
    )

    render_chart = CXJSON([chart1, chart2])
    results = render_chart.render()

    assert len(results) == 2
    render_output = [json.loads(r)["renderTo"] for r in results]
    assert render_output == ["bar1", "bar2"]
