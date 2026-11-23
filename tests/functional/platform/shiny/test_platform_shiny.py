"""
Captures the Shiny test apps in a headless browser and compares them with the
approved images. See tests/functional/platform/README.md.
"""

from pathlib import Path

import pytest

pytest.importorskip("shiny")

from tests.functional.platform.charts import CHART_IDS, COLUMN_IDS  # noqa: E402
from tests.functional.platform.server import (  # noqa: E402
    free_port,
    python_command,
    running_app,
)
from tests.functional.platform.visual import (  # noqa: E402
    assert_matches_canon,
    resize_window,
    wait_for_charts,
)

FRAMEWORK = "shiny"
APP_DIR = Path(__file__).parent


def _serve(app_file: str):
    port = free_port()
    command = python_command(
        "-m", "shiny", "run", "--host", "127.0.0.1", "--port", str(port), app_file
    )
    env = {"CANVASXPRESS_TARGET_CONTEXT": "shiny"}
    return running_app(command, APP_DIR, port, "/", env)


@pytest.fixture(scope="module")
def app_url():
    with _serve("app.py") as url:
        yield url


@pytest.fixture(scope="module")
def columns_url():
    with _serve("app_columns.py") as url:
        yield url


def test_initial(page, app_url):
    page.goto(app_url)
    wait_for_charts(page, CHART_IDS)
    assert_matches_canon(page, FRAMEWORK, "initial", CHART_IDS)


def test_resized(page, app_url):
    page.goto(app_url)
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
