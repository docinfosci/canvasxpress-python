"""
Captures of a browser window, compared against approved ("canon") captures.

Each test case captures the whole browser window at a known size, together with
the position and size of each chart on the page, and checks both against the
canon for that case:

- Layout: each chart's box must be within a few pixels of canon. This is what
  shows that a chart is present, at its configured size, and that a filling
  chart follows its container, and it does not depend on how a platform draws
  text.
- Image: the parts of the window that are drawn on ("ink"), on a coarse grid,
  must overlap canon's. This catches a chart that is blank or drawn wrongly,
  while tolerating the different fonts of Windows, macOS and Linux, which move
  text by a few pixels.

Neither check notices a sparse chart, such as a scatter plot, losing a few
points: that the data is drawn right is established when a person reviews the
capture before approving it.

Structural similarity (SSIM) over the whole window was tried first and is not
used: the white background dominates it, so a blank page still scores about
0.95 against canon.

A case with no canon yet is skipped, and its capture is kept for review. Once a
person has checked the capture, `approve.py` makes it canon.
"""

import json
from pathlib import Path
from typing import Dict, List, Sequence

import numpy
import pytest

# scikit-image is imported where it is used, so that importing this module, as
# the fixtures do, works where it is not installed and the tests skip instead.

PLATFORM_DIR = Path(__file__).parent

CAPTURE_DIR = PLATFORM_DIR / "captures"
"""Where each run's captures are written. Not committed."""

CANON_SUFFIXES = (".png", ".json")
"""The files of a capture or canon: the window image, and the chart layout."""

VIEWPORT = {"width": 1920, "height": 1080}
"""The browser window size of every capture: 1080p, a 16:9 ratio."""

RESIZED_VIEWPORT = {"width": 1280, "height": 720}
"""The window size after a resize, keeping the 16:9 ratio."""

CELL_PX = 32
"""The size of a grid cell when comparing where the window is drawn on."""

INK_MIN = 0.02
"""How dark a cell must be on average, from 0 (white) to 1 (black), to count as
drawn on. Low enough that a cell crossed by an axis line or a few letters counts,
high enough that the faint grid lines of a chart do not."""

OVERLAP_MIN = 0.85
"""The least overlap of drawn-on cells with canon that passes: the cells drawn
on in both, divided by the cells drawn on in either, where 1.0 is the same.
Windows and Linux captures of the same case overlap by 0.92 or more; a blank
page overlaps by 0, and a page with a chart missing or another framework's
layout by 0.8 or less."""

LAYOUT_TOLERANCE_PX = 4
"""How far each edge of a chart's box may be from canon. Windows and Linux place
every chart at the same pixel; the allowance is for text above a chart, such as
a heading, that another platform's fonts make a little taller or shorter."""

SETTLE_MS = 3000
"""How long to let charts finish drawing once they exist. This covers the fill
script's retries, the last of which runs 2 seconds after a chart is created."""

RESIZE_SETTLE_MS = 1500
"""How long to let charts redraw after the window is resized."""

CHART_TIMEOUT_MS = 90000
"""How long to wait for the charts to be created, including loading the
CanvasXpress library from its CDN."""

Layout = Dict[str, Dict[str, float]]
"""Each chart's box on the page, by chart ID: x, y, width and height in pixels."""


def canon_path(framework: str, case: str, suffix: str = ".png") -> Path:
    """
    Returns:
        The path of a canon file for a case, committed with its tests: the image
        (".png") or the chart layout (".json").
    """
    return PLATFORM_DIR / framework / "expected" / f"{case}{suffix}"


def capture_path(framework: str, case: str, suffix: str = ".png") -> Path:
    """
    Returns:
        The path of a file of the latest capture of a case: the image (".png")
        or the chart layout (".json").
    """
    return CAPTURE_DIR / framework / f"{case}{suffix}"


def diff_path(framework: str, case: str) -> Path:
    """
    Returns:
        The path of the difference image written when a case does not match.
    """
    return CAPTURE_DIR / framework / f"{case}.diff.png"


def wait_for_charts(page, chart_ids, settle_ms: int = SETTLE_MS) -> None:
    """
    Waits until CanvasXpress has created every chart, then lets them settle.

    Args:
        page: The Playwright page.
        chart_ids: The element IDs of the charts expected on the page.
        settle_ms: How long to wait once the charts exist.
    """
    page.wait_for_function(
        "ids => window.CanvasXpress"
        " && ids.every(id => window.CanvasXpress.getObject(id))",
        arg=list(chart_ids),
        timeout=CHART_TIMEOUT_MS,
    )
    page.wait_for_timeout(settle_ms)


def resize_window(page, viewport=RESIZED_VIEWPORT) -> None:
    """
    Resizes the browser window and lets the charts redraw.
    """
    page.set_viewport_size(viewport)
    page.wait_for_timeout(RESIZE_SETTLE_MS)


def chart_layout(page, chart_ids: Sequence[str]) -> Layout:
    """
    Returns:
        The box of each chart's canvas on the page, rounded to whole pixels, or
        None for a chart whose canvas is missing.
    """
    return page.evaluate(
        """ids => Object.fromEntries(ids.map(id => {
            const canvas = document.getElementById(id);
            if (!canvas) return [id, null];
            const box = canvas.getBoundingClientRect();
            return [id, {
                x: Math.round(box.x), y: Math.round(box.y),
                width: Math.round(box.width), height: Math.round(box.height),
            }];
        }))""",
        list(chart_ids),
    )


def compare_layouts(canon: Layout, capture: Layout) -> List[str]:
    """
    Returns:
        A description of each chart whose box differs from canon by more than
        LAYOUT_TOLERANCE_PX on any edge, or that is missing from either.
    """
    problems = []
    for chart_id in sorted(set(canon) | set(capture)):
        expected, actual = canon.get(chart_id), capture.get(chart_id)
        if not expected or not actual:
            problems.append(f"{chart_id}: canon {expected}, captured {actual}")
            continue

        edges = {
            "left": (expected["x"], actual["x"]),
            "top": (expected["y"], actual["y"]),
            "right": (
                expected["x"] + expected["width"],
                actual["x"] + actual["width"],
            ),
            "bottom": (
                expected["y"] + expected["height"],
                actual["y"] + actual["height"],
            ),
        }
        moved = [
            f"{edge} {was:.0f}->{now:.0f}"
            for edge, (was, now) in edges.items()
            if abs(now - was) > LAYOUT_TOLERANCE_PX
        ]
        if moved:
            problems.append(f"{chart_id}: {', '.join(moved)}")

    return problems


def _read_rgb(path: Path) -> numpy.ndarray:
    from skimage import img_as_float
    from skimage.io import imread

    image = imread(str(path))
    if image.ndim == 2:
        image = numpy.stack([image] * 3, axis=-1)
    return img_as_float(image[..., :3])


def _inked_cells(image: numpy.ndarray) -> numpy.ndarray:
    from skimage.transform import downscale_local_mean

    luminance = image @ numpy.array([0.299, 0.587, 0.114])
    return downscale_local_mean(1.0 - luminance, (CELL_PX, CELL_PX)) > INK_MIN


def compare_images(canon: Path, capture: Path, diff: Path) -> List[str]:
    """
    Compares where a capture is drawn on with its canon image.

    Args:
        canon: The canon image.
        capture: The new capture.
        diff: Where to write an image of the differences when the images do not
            match: the capture, with cells drawn on only in canon tinted red and
            cells drawn on only in the capture tinted blue.

    Returns:
        A description of the mismatch, or nothing when the capture matches.
    """
    from skimage import img_as_ubyte
    from skimage.io import imsave

    expected = _read_rgb(canon)
    actual = _read_rgb(capture)

    if expected.shape != actual.shape:
        return [
            f"capture is {actual.shape[1]}x{actual.shape[0]} but canon is"
            f" {expected.shape[1]}x{expected.shape[0]}"
        ]

    expected_ink, actual_ink = _inked_cells(expected), _inked_cells(actual)
    either = numpy.count_nonzero(expected_ink | actual_ink)
    overlap = numpy.count_nonzero(expected_ink & actual_ink) / max(either, 1)
    if overlap >= OVERLAP_MIN:
        return []

    def full_size(cells: numpy.ndarray) -> numpy.ndarray:
        pixels = numpy.kron(cells, numpy.ones((CELL_PX, CELL_PX), dtype=bool))
        return pixels[: actual.shape[0], : actual.shape[1]]

    marked = actual.copy()
    marked[full_size(expected_ink & ~actual_ink)] *= [1.0, 0.55, 0.55]
    marked[full_size(actual_ink & ~expected_ink)] *= [0.55, 0.55, 1.0]
    diff.parent.mkdir(parents=True, exist_ok=True)
    imsave(str(diff), img_as_ubyte(marked), check_contrast=False)

    return [f"drawn-on overlap {overlap:.3f} is below {OVERLAP_MIN}; see {diff}"]


def assert_matches_canon(
    page, framework: str, case: str, chart_ids: Sequence[str]
) -> None:
    """
    Captures the browser window and the chart layout, and checks them against
    the case's canon.

    Skips when there is no canon yet, keeping the capture for review, or when
    scikit-image is not installed.

    Args:
        page: The Playwright page, already showing the rendered charts.
        framework: The render target, which names the folder of its tests.
        case: The name of the case within the framework.
        chart_ids: The element IDs of the charts on the page.
    """
    pytest.importorskip("skimage")

    capture = capture_path(framework, case)
    capture.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(
        path=str(capture), full_page=False, animations="disabled", caret="hide"
    )
    layout = chart_layout(page, chart_ids)
    capture_path(framework, case, ".json").write_text(
        json.dumps(layout, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    canon = canon_path(framework, case)
    canon_layout = canon_path(framework, case, ".json")
    if not canon.exists() or not canon_layout.exists():
        pytest.skip(
            f"No canon for {framework}/{case}. Review {capture}, then approve it"
            f" with: python -m tests.functional.platform.approve"
            f" {framework}/{case}"
        )

    problems = compare_layouts(
        json.loads(canon_layout.read_text(encoding="utf-8")), layout
    )
    problems += compare_images(canon, capture, diff_path(framework, case))
    assert not problems, f"{framework}/{case} does not match canon:\n" + "\n".join(
        problems
    )
