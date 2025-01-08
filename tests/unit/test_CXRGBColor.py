import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.type import CXRGBColor, CXBool


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_init():
    subject: CXRGBColor = CXRGBColor(label="1", value={"r": 128, "g": 128, "b": 128})
    assert subject.label == "1"
    assert subject.value == {"r": 128, "g": 128, "b": 128}

    subject: CXRGBColor = CXRGBColor(label="1", value=None)
    assert subject.label == "1"
    assert subject.value == {"r": 0, "g": 0, "b": 0}

    with pytest.raises(ValueError):
        CXRGBColor(label=None, value={"r": 1, "g": 1, "b": 1})


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_is_color_str():
    assert CXRGBColor.is_color_str("rgb(0,0,0)")
    assert CXRGBColor.is_color_str("rgb(0 ,0 ,0)")
    assert not CXRGBColor.is_color_str("rgb(0 ,0 ,256)")
    assert not CXRGBColor.is_color_str("rgb(0 ,-1 ,0)")
    assert not CXRGBColor.is_color_str("rgb(0 ,0 ,0 , 2)")
    assert not CXRGBColor.is_color_str("rgb(0 ,0 ,0 , q)")
    assert not CXRGBColor.is_color_str("rgb(-1,0,0,1)")
    assert not CXRGBColor.is_color_str("rgb(256,0,0,1)")
    assert not CXRGBColor.is_color_str("rgba(0,0,0)")
    assert not CXRGBColor.is_color_str("fred(0,0,0,1)")
    assert not CXRGBColor.is_color_str({"r": 0, "g": 0, "b": 0})


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_is_color_list():
    assert CXRGBColor.is_color_list([0, 0, 0])
    assert not CXRGBColor.is_color_list([0, 0, 256])
    assert not CXRGBColor.is_color_list([0, -1, 0])
    assert not CXRGBColor.is_color_list(
        [
            0,
            0,
        ]
    )
    assert not CXRGBColor.is_color_list([0, 0, 0, "1"])
    assert not CXRGBColor.is_color_list([0, 0, 0, 2])
    assert not CXRGBColor.is_color_list([0, 0, 0, 1, 7])
    assert not CXRGBColor.is_color_list([-1, 0, 0, 1])
    assert not CXRGBColor.is_color_list([256, 0, 0, 1])
    assert not CXRGBColor.is_color_list("rgb(0,0,0)")
    assert not CXRGBColor.is_color_list("fred(0,0,0,1)")
    assert not CXRGBColor.is_color_list({"r": 0, "g": 0, "b": 0})


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_is_color_dict():
    assert CXRGBColor.is_color_dict({"r": 0, "g": 0, "b": 0})
    assert not CXRGBColor.is_color_dict({"r": -1, "g": 0, "b": 0})
    assert not CXRGBColor.is_color_dict({"r": 1, "g": 0, "b": 0, "a": -1})
    assert not CXRGBColor.is_color_dict({"r": 0, "g": 0, "b": 0, "q": 1})
    assert not CXRGBColor.is_color_dict({"r": 0, "g": 0, "b": 0, "q": 1})
    assert not CXRGBColor.is_color_dict({"r": "0", "g": 0, "b": 0})
    assert not CXRGBColor.is_color_dict([0, 0, 0, 1])
    assert not CXRGBColor.is_color_dict("rgb(0,0,0)")
    assert not CXRGBColor.is_color_dict("fred(0,0,0,1)")


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_label():
    subject: CXRGBColor = CXRGBColor("1", None)
    assert subject.label == "1"

    with pytest.raises(AttributeError):
        subject: CXRGBColor = CXRGBColor("1", None)
        subject.label = "2"


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_value():
    subject: CXRGBColor = CXRGBColor("1", None)
    subject.value = {"r": 1, "g": 1, "b": 1}
    assert subject.value == {"r": 1, "g": 1, "b": 1}

    subject: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    subject.value = None
    assert subject.value == {"r": 0, "g": 0, "b": 0}

    subject: CXRGBColor = CXRGBColor("1", None)
    subject.value = {"r": 128, "g": 128, "b": 128}
    assert subject.value == {"r": 128, "g": 128, "b": 128}

    subject: CXRGBColor = CXRGBColor("1", None)
    subject.value = CXRGBColor("a", {"r": 128, "g": 128, "b": 128})
    assert subject.value == {"r": 128, "g": 128, "b": 128}

    subject: CXRGBColor = CXRGBColor("1", None)
    subject.value = "rgb(128, 128, 128)"
    assert subject.value == {"r": 128, "g": 128, "b": 128}

    subject: CXRGBColor = CXRGBColor("1", None)
    subject.value = [128, 128, 128]
    assert subject.value == {"r": 128, "g": 128, "b": 128}

    with pytest.raises(TypeError):
        subject: CXRGBColor = CXRGBColor("1", None)
        subject.value = 2

    with pytest.raises(ValueError):
        subject: CXRGBColor = CXRGBColor("1", None)
        subject.value = "rgb(1,1,1,q)"

    with pytest.raises(ValueError):
        subject: CXRGBColor = CXRGBColor("1", None)
        subject.value = [0, 0, 0, 1, 7]

    with pytest.raises(ValueError):
        subject: CXRGBColor = CXRGBColor("1", None)
        subject.value = {"q": 128, "y": 128, "b": "128"}


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_copy():
    subject: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    assert subject == copy(subject)


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_deepcopy():
    subject: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    assert subject == deepcopy(subject)


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_str():
    subject: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    assert str(subject) == json.dumps({subject.label: "rgb(128,128,128)"})


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_repr():
    subject: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    subject_repr = repr(subject)
    assert isinstance(subject_repr, str)
    assert subject == eval(subject_repr)


@pytest.mark.skip(reason="CXRGBColor class is deprecated")
def test_CXRGBColor_equality():
    subject1: CXRGBColor = CXRGBColor("1", None)
    subject2: CXRGBColor = CXRGBColor("1", None)
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBColor = CXRGBColor("1", {"r": 1, "g": 1, "b": 1})
    subject2: CXRGBColor = CXRGBColor("1", {"r": 1, "g": 1, "b": 1})
    assert subject1 == subject2
    assert not subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBColor = CXRGBColor("1", {"r": 1, "g": 1, "b": 1})
    subject2: CXRGBColor = CXRGBColor("1", {"r": 255, "g": 255, "b": 255})
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2

    subject1: CXRGBColor = CXRGBColor("1", None)
    subject2: CXRGBColor = CXRGBColor("2", None)
    assert subject1 != subject2
    assert subject1 < subject2
    assert not subject1 > subject2
    assert subject2 > subject1

    subject1: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    subject2: CXRGBColor = CXRGBColor("1", {"r": 1, "g": 1, "b": 1})
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    subject2: CXRGBColor = None
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2

    subject1: CXRGBColor = CXRGBColor("1", {"r": 128, "g": 128, "b": 128})
    subject2: CXBool = CXBool("1", False)
    assert subject1 != subject2
    assert not subject1 < subject2
    assert subject1 > subject2
