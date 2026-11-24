"""
Executes minimal notebooks headlessly, exports them to HTML, and captures those
pages in a headless browser for comparison with the approved images. The export
keeps the notebook's HTML and JavaScript outputs, so the charts are drawn by the
same code a live notebook runs. See tests/functional/platform/README.md.
"""

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")
nbconvert = pytest.importorskip("nbconvert")

from tests.functional.platform.charts import CHART_IDS, COLUMN_IDS  # noqa: E402
from tests.functional.platform.server import REPO_ROOT  # noqa: E402
from tests.functional.platform.visual import (  # noqa: E402
    assert_matches_canon,
    resize_window,
    wait_for_charts,
)

FRAMEWORK = "jupyter"

_SETUP_CELL = 'import os\nos.environ["CANVASXPRESS_TARGET_CONTEXT"] = "jupyter"'

NOTEBOOK_CELLS = [
    _SETUP_CELL,
    "from canvasxpress.plot import graph\n"
    "from tests.functional.platform.charts import fill_chart, fixed_chart",
    "graph(fixed_chart())",
    "graph(fill_chart(), fill_to_width=True)",
]

COLUMNS_NOTEBOOK_CELLS = [
    _SETUP_CELL,
    "from IPython.display import display\n"
    "from canvasxpress.render.jupyter import CXNoteBook\n"
    "from tests.functional.platform.charts import left_chart, right_chart",
    "display(*CXNoteBook(left_chart(), right_chart())"
    ".render(columns=2, fill_to_width=True))",
]

KERNEL_TIMEOUT_S = 180


def _notebook_page(cells, directory) -> str:
    """
    Executes a notebook of code cells and saves it as an HTML page.

    Returns:
        The page's file URL.
    """
    notebook = nbformat.v4.new_notebook()
    notebook.cells = [nbformat.v4.new_code_cell(source) for source in cells]

    # The kernel runs from the repository root so that it can import the charts.
    client = nbclient.NotebookClient(
        notebook,
        timeout=KERNEL_TIMEOUT_S,
        kernel_name="python3",
        resources={"metadata": {"path": str(REPO_ROOT)}},
    )
    client.execute()

    exporter = nbconvert.HTMLExporter(
        exclude_input=True,
        exclude_input_prompt=True,
        exclude_output_prompt=True,
    )
    html, _ = exporter.from_notebook_node(notebook)

    page_path = directory / "notebook.html"
    page_path.write_text(html, encoding="utf-8")
    return page_path.as_uri()


@pytest.fixture(scope="module")
def notebook_url(tmp_path_factory):
    return _notebook_page(NOTEBOOK_CELLS, tmp_path_factory.mktemp("jupyter"))


@pytest.fixture(scope="module")
def columns_url(tmp_path_factory):
    return _notebook_page(
        COLUMNS_NOTEBOOK_CELLS, tmp_path_factory.mktemp("jupyter_columns")
    )


def test_initial(page, notebook_url):
    page.goto(notebook_url)
    wait_for_charts(page, CHART_IDS)
    assert_matches_canon(page, FRAMEWORK, "initial", CHART_IDS)


def test_resized(page, notebook_url):
    page.goto(notebook_url)
    wait_for_charts(page, CHART_IDS)
    resize_window(page)
    assert_matches_canon(page, FRAMEWORK, "resized", CHART_IDS)


def test_columns_initial(page, columns_url):
    page.goto(columns_url)
    wait_for_charts(page, COLUMN_IDS)
    assert_matches_canon(page, FRAMEWORK, "columns_initial", COLUMN_IDS)


def test_columns_resized(page, columns_url):
    page.goto(columns_url)
    wait_for_charts(page, COLUMN_IDS)
    resize_window(page)
    assert_matches_canon(page, FRAMEWORK, "columns_resized", COLUMN_IDS)
