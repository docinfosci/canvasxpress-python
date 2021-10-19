import pytest

from canvasxpress.config.type import CXGraphTypeOptions, CXGraphType


def test_CXGraphType_init():
    CXGraphType(CXGraphTypeOptions.Area)
    CXGraphType("Area")

    with pytest.raises(ValueError):
        CXGraphType(3)


def test_CXGraphType_custom_value():
    subject: CXGraphType = CXGraphType(CXGraphTypeOptions.Area)
    subject.set_custom_value("fred")


def test_CXGraphType_value():
    subject: CXGraphType = CXGraphType(CXGraphTypeOptions.Area)
    subject.value = CXGraphTypeOptions.Tree
    assert subject.value == CXGraphTypeOptions.Tree.value

    subject: CXGraphType = CXGraphType(CXGraphTypeOptions.Area)
    subject.value = "Tree"
    assert subject.value == CXGraphTypeOptions.Tree.value

    with pytest.raises(ValueError):
        CXGraphType(None)

    with pytest.raises(ValueError):
        subject: CXGraphType = CXGraphType(CXGraphTypeOptions.Area)
        subject.value = None

    with pytest.raises(ValueError):
        subject: CXGraphType = CXGraphType(CXGraphTypeOptions.Area)
        subject.value = 4
