import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.render.base import CXRenderable


class SampleRenderable(CXRenderable):
    """
    A generic CXRenderable for testing the abstract base class.
    """

    def __init__(self, *cx: CanvasXpress):
        super().__init__(*cx)

    def render(self):
        """
        Calls the base render method, but otherwise does nothing.
        """
        CXRenderable.render(self)


@pytest.fixture()
def testable_renderable() -> CXRenderable:
    """
    Provides a generic CXRenderable useful for testin the base class.
    """
    chart: CanvasXpress = CanvasXpress(
        render_to="canvasId",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                }
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )
    return SampleRenderable(chart)


def test_CXRenderable_init():
    chart: CanvasXpress = CanvasXpress(
        render_to="canvasId",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                }
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )

    SampleRenderable(chart)


def test_CXRenderable_get_canvas(testable_renderable: CXRenderable):
    assert testable_renderable.canvas is not None


def test_CXRenderable_set_canvas(testable_renderable: CXRenderable):
    original_canvas = testable_renderable.canvas

    chart: CanvasXpress = CanvasXpress(
        render_to="canvasId2",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                }
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Area)),
    )

    testable_renderable.canvas = chart

    assert original_canvas != testable_renderable.canvas
    assert chart == testable_renderable.canvas


def test_CXRenderable_set_canvas_None(testable_renderable: CXRenderable):
    testable_renderable.canvas = None
    assert testable_renderable.canvas is None


def test_CXRenderable_set_canvas_junk(testable_renderable: CXRenderable):
    for candidate in [0, "0", dict()]:
        with pytest.raises(TypeError):
            testable_renderable.canvas = candidate


def test_CXRenderable_render(testable_renderable: CXRenderable):
    try:
        testable_renderable.render()

    except Exception as e:
        pytest.fail(f"Unexpected {e} when calling CXRenderable.render()")
