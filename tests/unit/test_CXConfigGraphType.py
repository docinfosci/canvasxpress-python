from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions


def test_basic_setter():
    config = CXGraphType(CXGraphTypeOptions.Area)
    config.value = CXGraphTypeOptions.Bar
    assert config.value == CXGraphTypeOptions.Bar.value


def test_immediate_graph_type_usage_via_bar():
    assert CXGraphTypeOptions.Bar.value == "Bar"


def test_graph_type_attribute_access():
    assert CXGraphTypeOptions.Area in CXGraphTypeOptions
