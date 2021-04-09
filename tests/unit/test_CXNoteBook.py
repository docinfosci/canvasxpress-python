import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions
from canvasxpress.data.keypair import CXDictData
from canvasxpress.render.jupyter import CXNoteBook


def test_CXNoteBook_render():
    chart: CanvasXpress = CanvasXpress(
        target_id="canvasId",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]]
                }
            }
        ),
        configs=CXConfigs(
            CXGraphType(CXGraphTypeOptions.Bar)
        )
    )

    notebook: CXNoteBook = CXNoteBook(chart)

    try:
        notebook.render()

    except Exception as e:
        pytest.fail(f"Unexpected {e} when calling CXNoteBook.render()")
