import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXList, CXBool


def test_CXList_init():
    subject: CXList = CXList(
        label="1",
        value=[1]
    )
    assert subject.label == "1"
    assert subject.value == [1]

    subject: CXList = CXList(
        label="1",
        value=None
    )
    assert subject.label == "1"
    assert subject.value == []

    with pytest.raises(ValueError):
        subject: CXList = CXList(
            label=None,
            value=[2]
        )


def test_CXList_label():
    subject: CXList = CXList("1", [])
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXList = CXList("1", [])
        subject.label = "2"


def test_CXList_value():
    subject: CXList = CXList("1", [])
    subject.value = ["2"]
    assert subject.value == ["2"]

    subject: CXList = CXList("1", [1])
    subject.value = None
    assert subject.value == []

    subject: CXList = CXList("1", [])
    subject.value = [1]
    assert subject.value == [1]


def test_CXList_copy():
    subject: CXList = CXList("1", [1])
    assert subject == copy(subject)


def test_CXList_deepcopy():
    subject: CXList = CXList("1", [1])
    assert subject == deepcopy(subject)


def test_CXList_str():
    subject: CXList = CXList("1", [1])
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXList_repr():
    subject: CXList = CXList("1", [2])
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXList_equality():
    subject1: CXList = CXList("1", [])
    subject2: CXList = CXList("1", [])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXList = CXList("1", [2])
    subject2: CXList = CXList("1", [2])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXList = CXList("1", [2])
    subject2: CXList = CXList("1", [2, 2])
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXList = CXList("1", [])
    subject2: CXList = CXList("2", [])
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXList = CXList("1", [1])
    subject2: CXList = CXList("1", [2])
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXList = CXList("1", [1])
    subject2: CXList = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXList = CXList("1", [1])
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2