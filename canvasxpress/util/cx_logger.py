"""
Python logging support for CanvasXpress for Python.

The package logs through a single logger identified as ``canvasxpress-python``.
It carries no handlers of its own, so its records propagate to the client
application's master (root) logger and are written to whatever targets the
client has configured for it.
"""

import logging

LOGGER_NAME: str = "canvasxpress-python"
"""The name identifying the CanvasXpress for Python logger."""


def get_logger() -> "logging.Logger":
    """Provides the logger for CanvasXpress for Python.

    The logger is identified as ``canvasxpress-python`` and does not assign
    any handlers of its own. Its records propagate to the client
    application's master (root) logger, where they are written to the targets
    the client has configured.

    Returns:
        `logging.Logger`: The shared package logger.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.propagate = True
    return logger
