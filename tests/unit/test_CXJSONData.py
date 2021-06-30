import json
import string
from copy import copy, deepcopy

import requests

import pytest
from deepdiff import DeepDiff
from hypothesis import given, settings
from hypothesis.strategies import dictionaries, text

from canvasxpress.data.keypair import CXJSONData


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_init_valid_input(sample):
    cxdata = CXJSONData(sample)
    assert not DeepDiff(
        sample,
        cxdata.get_raw_dict_form()
    )


def test_CXJSONData_init_invalid_input():
    for sample in [1, '1', [12, 13], 4.5, ]:
        with pytest.raises(TypeError):
            CXJSONData(sample)


def test_CXJSONData_set_data_invalid():
    for sample in [1, '1', [12, 13], 4.5, ]:
        with pytest.raises(TypeError):
            subject: CXJSONData = CXJSONData({})
            subject.data = sample


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_get_valid_data(sample):
    cxdata = CXJSONData()
    cxdata.data = sample
    assert not DeepDiff(sample, cxdata.data)


def test_CXJSONData_set_invalid_url():
    sample_url = "http://toddsbadurl.com/data.json"
    with pytest.raises(ValueError):
        candidate: CXJSONData = CXJSONData()
        candidate.json = sample_url


def test_CXJSONData_set_url():
    sample_url = "https://raw.githubusercontent.com/docinfosci/" \
                 "canvasxpress-python/develop/readme/examples/iris.json"

    candidate: CXJSONData = CXJSONData()
    sample = requests.get(sample_url).json()

    candidate.json = sample_url
    assert candidate.json == json.dumps(sample)

@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_set_valid_json(sample):
    candidate: CXJSONData = CXJSONData()
    json_sample = json.dumps(sample)

    candidate.json = json_sample
    assert candidate.data == sample
    assert candidate.json == json_sample

    candidate.json = sample
    assert candidate.data == sample
    assert candidate.json == json_sample

    candidate.data = CXJSONData(sample)
    assert candidate.data == sample
    assert candidate.json == json_sample


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_set_valid_dict(sample):
    candidate: CXJSONData = CXJSONData()

    candidate.json = sample
    assert json.loads(candidate.json) == sample

    candidate.data = sample
    assert candidate.data == sample


@settings(deadline=None)
@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_copy_CXJSONData(sample):
    cxdict1 = CXJSONData(sample)
    cxdict2 = copy(cxdict1)
    assert cxdict1 == cxdict2


@settings(deadline=None)
@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_deepcopy_CXJSONData(sample):
    cxdict1 = CXJSONData(sample)
    cxdict2 = deepcopy(cxdict1)
    assert cxdict1 == cxdict2


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_str_perspective(sample):
    cxdict1 = CXJSONData(sample)
    cxdict1_str = str(cxdict1)
    assert cxdict1_str == json.dumps(cxdict1.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_repr_perspective(sample):
    cxdict1 = CXJSONData(sample)
    cxdict1_repr = repr(cxdict1)
    assert isinstance(cxdict1_repr, str)
    cxdict2: CXJSONData = eval(cxdict1_repr)
    assert not DeepDiff(cxdict1.data, cxdict2.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_get_raw_dict_form(sample):
    cxdict1 = CXJSONData(sample)
    output = cxdict1.get_raw_dict_form()
    assert output == cxdict1.data


def test_CXJSONData_equality_None():
    sample_a: CXJSONData = CXJSONData(
        {
            "a": 1
        }
    )

    assert sample_a != None
    assert None < sample_a
    assert sample_a > None


def test_CXJSONData_equality_junk():
    sample_a: CXJSONData = CXJSONData(
        {
            "a": 1
        }
    )

    for junk in [0, "0", [0]]:
        assert sample_a != junk
        assert junk < sample_a
        assert sample_a > junk


def test_CXJSONData_equality():
    sample_a: CXJSONData = CXJSONData(
        {
            "a": 1
        }
    )
    sample_b: CXJSONData = CXJSONData(
        {
            "a": 1
        }
    )

    assert sample_a == sample_b

    sample_c: CXJSONData = CXJSONData(
        {
            "c": 1
        }
    )

    assert sample_a != sample_c
    assert sample_a < sample_c
    assert sample_c > sample_a

    sample_d: CXJSONData = CXJSONData()

    assert sample_a != sample_d
    assert sample_d < sample_a
    assert sample_a > sample_d

    sample_e: CXJSONData = CXJSONData(
        {
            "c": 2
        }
    )

    assert sample_c != sample_e
    assert sample_c < sample_e
    assert sample_e > sample_c

    sample_f: CXJSONData = CXJSONData(
        {
            "c": 2,
            "d": 1
        }
    )

    assert sample_c != sample_f
    assert sample_c < sample_f
    assert sample_f > sample_c
