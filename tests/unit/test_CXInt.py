import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXString, CXBool, CXInt


def test_CXInt_init():
    subject: CXInt = CXInt(label="1", value=2)
    assert subject.label == "1"
    assert subject.value == 2

    subject: CXInt = CXInt(label="1", value=None)
    assert subject.label == "1"
    assert subject.value == 0

    with pytest.raises(ValueError):
        subject: CXInt = CXInt(label=None, value=2)


def test_CXInt_label():
    subject: CXInt = CXInt("1", 2)
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXInt = CXInt("1", 2)
        subject.label = "2"


def test_CXInt_value():
    subject: CXInt = CXInt("1", 1)
    subject.value = 2
    assert subject.value == 2

    subject: CXInt = CXInt("1", 1)
    subject.value = None
    assert subject.value == 0

    subject: CXInt = CXInt("1", 2)
    subject.value = 1
    assert subject.value == 1


def test_CXInt_copy():
    subject: CXInt = CXInt("1", 2)
    assert subject == copy(subject)


def test_CXInt_deepcopy():
    subject: CXInt = CXInt("1", 2)
    assert subject == deepcopy(subject)


def test_CXInt_str():
    subject: CXInt = CXInt("1", 2)
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXInt_repr():
    subject: CXInt = CXInt("1", 2)
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXInt_equality():
    subject1: CXInt = CXInt("1", 1)
    subject2: CXInt = CXInt("1", 1)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXInt = CXInt("1", 2)
    subject2: CXInt = CXInt("1", 2)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXInt = CXInt("1", 1)
    subject2: CXInt = CXInt("2", 1)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXInt = CXInt("1", 1)
    subject2: CXInt = CXInt("1", 2)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXInt = CXInt("1", 1)
    subject2: CXInt = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXInt = CXInt("1", 1)
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
