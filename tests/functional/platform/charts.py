"""
The charts drawn by every platform test app, so that each framework renders the
same content. Data is fixed: a capture must not change between runs.

Each framework's main app stacks a chart at its configured size, the control
that shows filling does not leak onto charts that did not ask for it, above one
that fills the width. Its columns app puts two charts side by side in the
framework's own columns, each filling the width of its column.
"""

from canvasxpress.canvas import CanvasXpress

CHART_WIDTH = 500
CHART_HEIGHT = 350


def bar_chart(render_to: str, title: str) -> CanvasXpress:
    """
    Args:
        render_to: The chart's element ID.
        title: The chart title, which names what the capture should show.

    Returns:
        A bar chart of fixed data at the standard test size.
    """
    return CanvasXpress(
        render_to=render_to,
        data={
            "y": {
                "vars": ["Value"],
                "smps": ["Alpha", "Beta", "Gamma", "Delta"],
                "data": [[12, 30, 21, 8]],
            }
        },
        config={
            "graphType": "Bar",
            "graphOrientation": "vertical",
            "theme": "CanvasXpress",
            "title": title,
            "showLegend": False,
        },
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
    )


def scatter_chart(render_to: str, title: str) -> CanvasXpress:
    """
    Args:
        render_to: The chart's element ID.
        title: The chart title, which names what the capture should show.

    Returns:
        A scatter chart of fixed data at the standard test size.
    """
    return CanvasXpress(
        render_to=render_to,
        data={
            "y": {
                "vars": ["Keith", "Nina", "Freddy", "Tracey", "Isabelle", "Penny"],
                "smps": ["Height", "Weight"],
                "data": [
                    [174, 65.6],
                    [161, 51.6],
                    [194, 80.7],
                    [160, 49.2],
                    [173, 55.2],
                    [151, 48.7],
                ],
            }
        },
        config={
            "graphType": "Scatter2D",
            "xAxis": ["Height"],
            "yAxis": ["Weight"],
            "theme": "CanvasXpress",
            "title": title,
        },
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
    )


FIXED_ID = "cx_fixed"
"""A chart drawn at its configured size."""

FILL_ID = "cx_fill"
"""A chart drawn with fill_to_width, which follows the width of its container."""

CHART_IDS = [FIXED_ID, FILL_ID]


def fixed_chart() -> CanvasXpress:
    return bar_chart(FIXED_ID, "Fixed 500 x 350")


def fill_chart() -> CanvasXpress:
    return scatter_chart(FILL_ID, "Fills the container width")


LEFT_ID = "cx_left"
"""The left of two charts side by side, filling the width of its column."""

RIGHT_ID = "cx_right"
"""The right of two charts side by side, filling the width of its column."""

COLUMN_IDS = [LEFT_ID, RIGHT_ID]


def left_chart() -> CanvasXpress:
    return bar_chart(LEFT_ID, "Fills the left column")


def right_chart() -> CanvasXpress:
    return scatter_chart(RIGHT_ID, "Fills the right column")
