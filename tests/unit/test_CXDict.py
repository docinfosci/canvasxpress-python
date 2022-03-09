import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXDict, CXBool


def test_CXDict_init():
    subject: CXDict = CXDict(label="1", value={"a": 1})
    assert subject.label == "1"
    assert subject.value == {"a": 1}

    subject: CXDict = CXDict(label="1", value=None)
    assert subject.label == "1"
    assert subject.value == {}

    with pytest.raises(ValueError):
        subject: CXDict = CXDict(label=None, value={"b": 1})


def test_CXDict_label():
    subject: CXDict = CXDict("1", {})
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXDict = CXDict("1", {})
        subject.label = "2"


def test_CXDict_value():
    subject: CXDict = CXDict("1", {})
    subject.value = {"b": 1}
    assert subject.value == {"b": 1}

    subject: CXDict = CXDict("1", {"a": 1})
    subject.value = None
    assert subject.value == {}

    subject: CXDict = CXDict("1", {})
    subject.value = {"a": 1}
    assert subject.value == {"a": 1}

    subject: CXDict = CXDict("1", {})
    subject.value = CXDict("a", {"a": 1})
    assert subject.value == {"a": 1}

    subject: CXDict = CXDict("1", {})
    subject.value = json.dumps({"a": 1})
    assert subject.value == {"a": 1}


def test_CXDict_copy():
    subject: CXDict = CXDict("1", {"a": 1})
    assert subject == copy(subject)


def test_CXDict_deepcopy():
    subject: CXDict = CXDict("1", {"a": 1})
    assert subject == deepcopy(subject)


def test_CXDict_str():
    subject: CXDict = CXDict("1", {"a": 1})
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXDict_repr():
    subject: CXDict = CXDict("1", {"b": 1})
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXDict_equality():
    subject1: CXDict = CXDict("1", {})
    subject2: CXDict = CXDict("1", {})
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXDict = CXDict("1", {"b": 1})
    subject2: CXDict = CXDict("1", {"b": 1})
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXDict = CXDict("1", {"b": 1})
    subject2: CXDict = CXDict("1", {"b": 2})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXDict = CXDict("1", {"b": 1, "c": 2})
    subject2: CXDict = CXDict("1", {"b": 2})
    assert subject1 != subject2
    assert subject2 < subject1
    assert subject1 > subject2

    subject1: CXDict = CXDict("1", {})
    subject2: CXDict = CXDict("2", {})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2
    assert subject2 > subject1

    subject1: CXDict = CXDict("1", {"a": 1})
    subject2: CXDict = CXDict("1", {"b": 1})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXDict = CXDict("1", {"b": 1})
    subject2: CXDict = CXDict("1", {"a": 1})
    assert subject1 != subject2
    assert subject1 > subject2
    assert not subject1 < subject2

    subject1: CXDict = CXDict("1", {"a": 1})
    subject2: CXDict = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXDict = CXDict("1", {"a": 1})
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
