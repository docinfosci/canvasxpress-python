import json
import string
from copy import copy, deepcopy

import pytest
from deepdiff import DeepDiff
from hypothesis import given
from hypothesis.strategies import dictionaries, text

from canvasxpress.data.keypair import CXJSONData
from tests.util.hypothesis_support import everything_except


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_CXJSONData_init_valid_input(sample):
    cxdata = CXJSONData(sample)
    assert not DeepDiff(sample, cxdata.data)


@given(everything_except(dict))
def test_CXJSONData_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXJSONData(sample)


@given(everything_except(dict))
def test_CXJSONData_set_data_invalid(sample):
    dictdata = CXJSONData()
    with pytest.raises(TypeError):
        dictdata.data = sample


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
def test_CXJSONData_render_to_dict(sample):
    cxdict1 = CXJSONData(sample)
    output = cxdict1.render_to_dict()
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
