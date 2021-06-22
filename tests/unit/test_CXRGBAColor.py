import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXRGBAColor, CXBool


def test_CXRGBAColor_init():
    subject: CXRGBAColor = CXRGBAColor(
        label="1",
        value={'r': 128, 'g': 128, 'b': 128, 'a': 0.5}
    )
    assert subject.label == "1"
    assert subject.value == {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}

    subject: CXRGBAColor = CXRGBAColor(
        label="1",
        value=None
    )
    assert subject.label == "1"
    assert subject.value == {'r': 0, 'g': 0, 'b': 0, 'a': 1}

    with pytest.raises(ValueError):
        CXRGBAColor(
            label=None,
            value={'r': 1, 'g': 1, 'b': 1, 'a': 1}
        )


def test_is_color_str():
    assert CXRGBAColor.is_color_str("rgba(0,0,0,1)")
    assert CXRGBAColor.is_color_str("rgba(0 ,0 ,0 , 1)")
    assert not CXRGBAColor.is_color_str("rgba(0 ,0 ,0 , 2)")
    assert not CXRGBAColor.is_color_str("rgba(0 ,0 ,0 , q)")
    assert not CXRGBAColor.is_color_str("rgba(-1,0,0,1)")
    assert not CXRGBAColor.is_color_str("rgba(256,0,0,1)")
    assert not CXRGBAColor.is_color_str("rgba(0,0,0)")
    assert not CXRGBAColor.is_color_str("fred(0,0,0,1)")
    assert not CXRGBAColor.is_color_str({'r': 0, 'g': 0, 'b': 0, 'a': 1})


def test_is_color_list():
    assert CXRGBAColor.is_color_list([0,0,0,1])
    assert CXRGBAColor.is_color_list([0 ,0 ,0 , 1])
    assert not CXRGBAColor.is_color_list([0, 0,])
    assert not CXRGBAColor.is_color_list([0, 0, 0, '1'])
    assert not CXRGBAColor.is_color_list([0, 0, 0, 2])
    assert not CXRGBAColor.is_color_list([0, 0, 0, 1, 7])
    assert not CXRGBAColor.is_color_list([-1,0,0,1])
    assert not CXRGBAColor.is_color_list([256,0,0,1])
    assert not CXRGBAColor.is_color_list("rgba(0,0,0)")
    assert not CXRGBAColor.is_color_list("fred(0,0,0,1)")
    assert not CXRGBAColor.is_color_list({'r': 0, 'g': 0, 'b': 0, 'a': 1})


def test_is_color_dict():
    assert CXRGBAColor.is_color_dict({'r': 0, 'g': 0, 'b': 0, 'a': 1})
    assert not CXRGBAColor.is_color_dict({'r': -1, 'g': 0, 'b': 0, 'a': 1})
    assert not CXRGBAColor.is_color_dict({'r': 1, 'g': 0, 'b': 0, 'a': -1})
    assert not CXRGBAColor.is_color_dict({'r': 0, 'g': 0, 'b': 0, 'q': 1})
    assert not CXRGBAColor.is_color_dict({'r': 0, 'g': 0, 'b': 0, 'a': 1, 'q': 1})
    assert not CXRGBAColor.is_color_dict({'r': '0', 'g': 0, 'b': 0, 'a': 1})
    assert not CXRGBAColor.is_color_dict([0,0,0,1])
    assert not CXRGBAColor.is_color_dict("rgba(0,0,0)")
    assert not CXRGBAColor.is_color_dict("fred(0,0,0,1)")


def test_CXRGBAColor_label():
    subject: CXRGBAColor = CXRGBAColor("1", None)
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXRGBAColor = CXRGBAColor("1", None)
        subject.label = "2"


def test_CXRGBAColor_value():
    subject: CXRGBAColor = CXRGBAColor("1", None)
    subject.value = {'r': 1, 'g': 1, 'b': 1, 'a': 1}
    assert subject.value == {'r': 1, 'g': 1, 'b': 1, 'a': 1}

    subject: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    subject.value = None
    assert subject.value == {'r': 0, 'g': 0, 'b': 0, 'a': 1}

    subject: CXRGBAColor = CXRGBAColor("1", None)
    subject.value = {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}
    assert subject.value == {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}

    subject: CXRGBAColor = CXRGBAColor("1", None)
    subject.value = CXRGBAColor("a", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    assert subject.value == {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}

    subject: CXRGBAColor = CXRGBAColor("1", None)
    subject.value = "rgba(128, 128, 128, 0.5)"
    assert subject.value == {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}

    subject: CXRGBAColor = CXRGBAColor("1", None)
    subject.value = [128, 128, 128, 0.5]
    assert subject.value == {'r': 128, 'g': 128, 'b': 128, 'a': 0.5}

    with pytest.raises(TypeError):
        subject: CXRGBAColor = CXRGBAColor('1', None)
        subject.value = 2

    with pytest.raises(ValueError):
        subject: CXRGBAColor = CXRGBAColor('1', None)
        subject.value = "rgba(1,1,1,q)"

    with pytest.raises(ValueError):
        subject: CXRGBAColor = CXRGBAColor('1', None)
        subject.value = [0, 0, 0, 1, 7]

    with pytest.raises(ValueError):
        subject: CXRGBAColor = CXRGBAColor('1', None)
        subject.value = {'q': 128, 'y': 128, 'b': '128', 'a': 0.5}


def test_CXRGBAColor_copy():
    subject: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    assert subject == copy(subject)


def test_CXRGBAColor_deepcopy():
    subject: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    assert subject == deepcopy(subject)


def test_CXRGBAColor_str():
    subject: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    assert str(subject) == json.dumps({subject.label: "rgba(128,128,128,0.5)"})


def test_CXRGBAColor_repr():
    subject: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


def test_CXRGBAColor_equality():
    subject1: CXRGBAColor = CXRGBAColor("1", None)
    subject2: CXRGBAColor = CXRGBAColor("1", None)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBAColor = CXRGBAColor("1", {'r': 1, 'g': 1, 'b': 1, 'a': 1})
    subject2: CXRGBAColor = CXRGBAColor("1", {'r': 1, 'g': 1, 'b': 1, 'a': 1})
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBAColor = CXRGBAColor("1", {'r': 1, 'g': 1, 'b': 1, 'a': 1})
    subject2: CXRGBAColor = CXRGBAColor("1", {'r': 255, 'g': 255, 'b': 255, 'a': 1})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBAColor = CXRGBAColor("1", None)
    subject2: CXRGBAColor = CXRGBAColor("2", None)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2
    assert subject2 > subject1

    subject1: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    subject2: CXRGBAColor = CXRGBAColor("1", {'r': 1, 'g': 1, 'b': 1, 'a': 1})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    subject2: CXRGBAColor = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXRGBAColor = CXRGBAColor("1", {'r': 128, 'g': 128, 'b': 128, 'a': 0.5})
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
