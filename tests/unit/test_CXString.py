import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXString, CXBool


def test_CXString_init():
    subject: CXString = CXString(
        label="1",
        value="2"
    )
    assert subject.label == "1"
    assert subject.value == "2"

    subject: CXString = CXString(
        label="1",
        value=None
    )
    assert subject.label == "1"
    assert subject.value == ""

    with pytest.raises(ValueError):
        subject: CXString = CXString(
            label=None,
            value="2"
        )


def test_CXString_label():
    subject: CXString = CXString("1", "")
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXString = CXString("1", "")
        subject.label = "2"


def test_CXString_value():
    subject: CXString = CXString("1", "")
    subject.value = "2"
    assert subject.value == "2"

    subject: CXString = CXString("1", "")
    subject.value = None
    assert subject.value == ""

    subject: CXString = CXString("1", "")
    subject.value = 1
    assert subject.value == "1"


def test_CXString_copy():
    subject: CXString = CXString("1", "2")
    assert subject == copy(subject)


def test_CXString_deepcopy():
    subject: CXString = CXString("1", "2")
    assert subject == deepcopy(subject)


def test_CXString_str():
    subject: CXString = CXString("1", "2")
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXString_repr():
    subject: CXString = CXString("1", "2")
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXString_equality():
    subject1: CXString = CXString("1", "")
    subject2: CXString = CXString("1", "")
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXString = CXString("1", "2")
    subject2: CXString = CXString("1", "2")
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXString = CXString("1", "")
    subject2: CXString = CXString("2", "")
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXString = CXString("1", "1")
    subject2: CXString = CXString("1", "2")
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXString = CXString("1", "1")
    subject2: CXString = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXString = CXString("1", "1")
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2