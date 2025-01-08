import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXGraphWeight


def test_CXGraphWeight_init():
    subject: CXGraphWeight = CXGraphWeight(label="1", value=[1])
    assert subject.label == "1"
    assert subject.value == [1]

    subject: CXGraphWeight = CXGraphWeight(label="1", value=None)
    assert subject.label == "1"
    assert subject.value == []

    subject: CXGraphWeight = CXGraphWeight(label="1", value=[0.4])
    assert subject.label == "1"
    assert subject.value == []

    with pytest.raises(ValueError):
        subject: CXGraphWeight = CXGraphWeight(label=None, value=[2])


def test_CXGraphWeight_label():
    subject: CXGraphWeight = CXGraphWeight("1", [])
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXGraphWeight = CXGraphWeight("1", [])
        subject.label = "2"


def test_CXGraphWeight_value():
    subject: CXGraphWeight = CXGraphWeight("1", [])
    subject.value = ["2"]
    assert subject.value == []

    subject: CXGraphWeight = CXGraphWeight("1", [1])
    subject.value = None
    assert subject.value == []

    subject: CXGraphWeight = CXGraphWeight("1", [])
    subject.value = [1, 2]
    assert subject.value == []

    subject: CXGraphWeight = CXGraphWeight("1", [])
    subject.value = [10, 20, 70]
    assert subject.value == [0.10, 0.20, 0.70]

    subject: CXGraphWeight = CXGraphWeight("1", [10, 20, 70])
    assert subject.value == [0.10, 0.20, 0.70]

    subject: CXGraphWeight = CXGraphWeight("1", [0.10, 0.20, 0.70])
    assert subject.value == [0.10, 0.20, 0.70]

    subject: CXGraphWeight = CXGraphWeight("1", [])
    subject.value = [0.10, 0.20, 0.70]
    assert subject.value == [0.10, 0.20, 0.70]


def test_CXGraphWeight_copy():
    subject: CXGraphWeight = CXGraphWeight("1", [1])
    assert subject == copy(subject)


def test_CXGraphWeight_is_valid():
    assert not CXGraphWeight.is_graph_weight_list(None, None)
    assert not CXGraphWeight.is_graph_weight_list(None, [1])
    assert CXGraphWeight.is_graph_weight_list("ringGraphWeight", [1])
    assert not CXGraphWeight.is_graph_weight_list("ringGraphWeight", [0.1])
    assert CXGraphWeight.is_graph_weight_list("ringGraphWeight", [0.1, 0.2, 0.7])
    assert CXGraphWeight.is_graph_weight_list("ringGraphWeight", [10, 20, 70])


def test_CXGraphWeight_deepcopy():
    subject: CXGraphWeight = CXGraphWeight("1", [1])
    assert subject == deepcopy(subject)


def test_CXGraphWeight_str():
    subject: CXGraphWeight = CXGraphWeight("1", [1])
    assert str(subject) == json.dumps(
        {
            "label": subject.label,
            "value": subject.value,
        }
    )


def test_CXGraphWeight_repr():
    subject: CXGraphWeight = CXGraphWeight("1", [2])
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXGraphWeight_equality():
    subject1: CXGraphWeight = CXGraphWeight("1", [])
    subject2: CXGraphWeight = CXGraphWeight("1", [])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXGraphWeight = CXGraphWeight("1", [2])
    subject2: CXGraphWeight = CXGraphWeight("1", [2])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXGraphWeight = CXGraphWeight("1", [20, 30, 50])
    subject2: CXGraphWeight = CXGraphWeight("2", [50, 30, 20])
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXGraphWeight = CXGraphWeight("1", [20, 30, 50])
    subject2: CXGraphWeight = CXGraphWeight("2", [20, 30, 50])
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXGraphWeight = CXGraphWeight("1", [20, 30, 50])
    subject2: CXGraphWeight = CXGraphWeight("1", [20, 30, 50])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXGraphWeight = CXGraphWeight("1", [20, 30, 50])
    subject2: CXGraphWeight = CXGraphWeight("1", [0.20, 0.30, 0.50])
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2
