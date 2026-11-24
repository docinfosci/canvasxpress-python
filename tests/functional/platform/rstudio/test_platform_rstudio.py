"""
Captures the standalone page that the RStudio renderer (CXHtml) saves with
output_file, as the RStudio viewer would show it, and compares it with the
approved images. The RStudio viewer itself cannot run headless.

The page has both charts side by side, filling the window's width and height,
so the resize case checks both dimensions. See tests/functional/platform/README.md.
"""

import pytest

pytest.importorskip("IPython")

from canvasxpress.render.rstudio import CXHtml  # noqa: E402
from tests.functional.platform.charts import (  # noqa: E402
    FILL_ID,
    FIXED_ID,
    bar_chart,
    scatter_chart,
)
from tests.functional.platform.visual import (  # noqa: E402
    assert_matches_canon,
    resize_window,
    wait_for_charts,
)

FRAMEWORK = "rstudio"
CHART_IDS = [FIXED_ID, FILL_ID]


@pytest.fixture(scope="module")
def page_url(tmp_path_factory):
    page_path = tmp_path_factory.mktemp("rstudio") / "charts.html"
    charts = CXHtml(
        bar_chart(FIXED_ID, "Fills width and height (left)"),
        scatter_chart(FILL_ID, "Fills width and height (right)"),
    )
    charts.render(
        columns=2,
        fill_to_width=True,
        fill_to_height=True,
        output_file=str(page_path),
    )
    return page_path.as_uri()


def test_initial(page, page_url):
    page.goto(page_url)
    wait_for_charts(page, CHART_IDS)
    assert_matches_canon(page, FRAMEWORK, "initial", CHART_IDS)


def test_resized(page, page_url):
    page.goto(page_url)
    wait_for_charts(page, CHART_IDS)
    resize_window(page)
    assert_matches_canon(page, FRAMEWORK, "resized", CHART_IDS)
