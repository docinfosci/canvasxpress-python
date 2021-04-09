import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXBool, CXFloat


def test_CXFloat_init():
    subject: CXFloat = CXFloat(
        label="1",
        value=2
    )
    assert subject.label == "1"
    assert subject.value == 2

    subject: CXFloat = CXFloat(
        label="1",
        value=None
    )
    assert subject.label == "1"
    assert subject.value == 0

    with pytest.raises(ValueError):
        subject: CXFloat = CXFloat(
            label=None,
            value=2
        )


def test_CXFloat_label():
    subject: CXFloat = CXFloat("1", 2)
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXFloat = CXFloat("1", 2)
        subject.label = "2"


def test_CXFloat_value():
    subject: CXFloat = CXFloat("1", 1)
    subject.value = 2
    assert subject.value == 2

    subject: CXFloat = CXFloat("1", 1)
    subject.value = None
    assert subject.value == 0

    subject: CXFloat = CXFloat("1", 2)
    subject.value = 1
    assert subject.value == 1


def test_CXFloat_copy():
    subject: CXFloat = CXFloat("1", 2)
    assert subject == copy(subject)


def test_CXFloat_deepcopy():
    subject: CXFloat = CXFloat("1", 2)
    assert subject == deepcopy(subject)


def test_CXFloat_str():
    subject: CXFloat = CXFloat("1", 2)
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXFloat_repr():
    subject: CXFloat = CXFloat("1", 2)
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXFloat_equality():
    subject1: CXFloat = CXFloat("1", 1)
    subject2: CXFloat = CXFloat("1", 1)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXFloat = CXFloat("1", 2)
    subject2: CXFloat = CXFloat("1", 2)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXFloat = CXFloat("1", 1)
    subject2: CXFloat = CXFloat("2", 1)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXFloat = CXFloat("1", 1)
    subject2: CXFloat = CXFloat("1", 2)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXFloat = CXFloat("1", 1)
    subject2: CXFloat = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXFloat = CXFloat("1", 1)
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
