from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXString, CXBool


def test_CXBool_init():
    subject: CXBool = CXBool(
        label="1",
        value=True
    )
    assert subject.label == "1"
    assert subject.value == True

    subject: CXBool = CXBool(
        label="1",
        value=None
    )
    assert subject.label == "1"
    assert subject.value == False

    with pytest.raises(ValueError):
        CXBool(
            label=None,
            value=True
        )


def test_CXBool_label():
    subject: CXBool = CXBool("1", True)
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXBool = CXBool("1", True)
        subject.label = "2"


def test_CXBool_value():
    subject: CXBool = CXBool("1", False)
    subject.value = True
    assert subject.value == True

    subject: CXBool = CXBool("1", True)
    subject.value = None
    assert subject.value == False

    subject: CXBool = CXBool("1", True)
    subject.value = False
    assert subject.value == False


def test_CXBool_copy():
    subject: CXBool = CXBool("1", True)
    assert subject == copy(subject)


def test_CXBool_deepcopy():
    subject: CXBool = CXBool("1", True)
    assert subject == deepcopy(subject)


def test_CXBool_str():
    subject: CXBool = CXBool("1", True)
    assert str(subject) == str(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXBool_repr():
    subject: CXBool = CXBool("1", True)
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXBool_equality():
    subject1: CXBool = CXBool("1", True)
    subject2: CXBool = CXBool("1", True)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXBool = CXBool("1", False)
    subject2: CXBool = CXBool("1", False)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXBool = CXBool("1", True)
    subject2: CXBool = CXBool("2", True)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXBool = CXBool("1", False)
    subject2: CXBool = CXBool("1", True)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXBool = CXBool("1", True)
    subject2: CXString = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXBool = CXBool("1", True)
    subject2: CXString = CXString("1", "1")
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
