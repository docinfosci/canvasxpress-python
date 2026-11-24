import logging
import warnings

import pytest

from canvasxpress.config.type import (
    CX_GRAPHTYPE_DEPRECATION_MESSAGE,
    CXGraphType,
    CXGraphTypeOptions,
)
from canvasxpress.util.cx_logger import LOGGER_NAME, get_logger

# The exact message the @deprecated decorator must carry and the
# canvasxpress-python logger must write at WARNING level.
EXPECTED_MESSAGE: str = (
    "Support will end January 2027.  Use a CanvasXpress JavaScript library "
    "recognized str value for the chart type instead."
)


def _deprecation_warning_messages(caught: list) -> list:
    """Collects the text of the DeprecationWarnings among `caught`."""
    return [
        str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)
    ]


def _graph_type_logs(caplog) -> list:
    """Collects the canvasxpress-python WARNING records in `caplog`."""
    return [
        record
        for record in caplog.records
        if record.name == "canvasxpress-python" and record.levelno == logging.WARNING
    ]


def test_deprecation_message_constant():
    assert CX_GRAPHTYPE_DEPRECATION_MESSAGE == EXPECTED_MESSAGE


def test_logger_identified_as_canvasxpress_python():
    logger = get_logger()
    assert logger.name == LOGGER_NAME
    assert logger.name == "canvasxpress-python"
    # No handlers of its own: records propagate to the client's master
    # (root) logger and are written to the client's configured targets.
    assert logger.handlers == []
    assert logger.propagate is True


def test_logger_records_reach_the_client_master_logger(caplog):
    # caplog captures on the root (master) logger, so a record reaching it
    # demonstrates propagation of the canvasxpress-python logger.
    with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
        CXGraphType("Bar")

    graph_type_logs = _graph_type_logs(caplog)
    assert len(graph_type_logs) > 0
    assert all(record.msg == EXPECTED_MESSAGE for record in graph_type_logs)


def test_CXGraphType_init_emits_deprecation_warning_and_log(caplog):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
            subject = CXGraphType(CXGraphTypeOptions.Bar)

    assert subject.value == "Bar"

    # @deprecated provides the DeprecationWarning carrying the reason.
    assert any(
        EXPECTED_MESSAGE in message for message in _deprecation_warning_messages(caught)
    )

    # The canvasxpress-python logger writes the same message at WARNING.
    graph_type_logs = _graph_type_logs(caplog)
    assert len(graph_type_logs) > 0
    assert all(record.msg == EXPECTED_MESSAGE for record in graph_type_logs)


def test_CXGraphType_value_setter_emits_deprecation_warning_and_log(caplog):
    subject = CXGraphType(CXGraphTypeOptions.Bar)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
            subject.value = CXGraphTypeOptions.Area

    assert subject.value == "Area"

    assert any(
        EXPECTED_MESSAGE in message for message in _deprecation_warning_messages(caught)
    )
    assert len(_graph_type_logs(caplog)) > 0


def test_CXGraphType_set_custom_value_emits_deprecation_warning_and_log(caplog):
    subject = CXGraphType(CXGraphTypeOptions.Bar)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
            subject.set_custom_value("fred")

    assert subject.value == "fred"

    assert any(
        EXPECTED_MESSAGE in message for message in _deprecation_warning_messages(caught)
    )
    assert len(_graph_type_logs(caplog)) > 0


def test_CXGraphType_render_emits_deprecation_warning_and_log(caplog):
    subject = CXGraphType(CXGraphTypeOptions.Bar)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
            rendered = subject.render()

    assert rendered == {"graphType": "Bar"}

    assert any(
        EXPECTED_MESSAGE in message for message in _deprecation_warning_messages(caught)
    )
    assert len(_graph_type_logs(caplog)) > 0


def test_CXGraphTypeOptions_still_resolves_values():
    # The supporting logic remains functional; only its deprecation is
    # signalled.
    assert CXGraphTypeOptions("Bar") is CXGraphTypeOptions.Bar
    assert CXGraphTypeOptions.Bar.value == "Bar"

    with pytest.raises(ValueError):
        CXGraphTypeOptions(42)


def test_CXString_graph_type_config_is_not_deprecated(caplog):
    # The migration path: a plain str graphType value via CXString carries no
    # deprecation warning or log.
    from canvasxpress.config.type import CXString

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with caplog.at_level(logging.WARNING, logger="canvasxpress-python"):
            subject = CXString("graphType", "Bar")
            rendered = subject.render()

    assert rendered == {"graphType": "Bar"}
    assert _deprecation_warning_messages(caught) == []
    assert _graph_type_logs(caplog) == []
