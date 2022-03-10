import json
import string
from copy import copy, deepcopy

import pytest
from deepdiff import DeepDiff
from hypothesis import given
from hypothesis.strategies import dictionaries, text

from canvasxpress.data.keypair import CXDictData
from tests.util.hypothesis_support import everything_except


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_init_valid_input(sample):
    cxdata = CXDictData(sample)
    assert not DeepDiff(sample, cxdata.data)


@given(everything_except(dict))
def test_CXDictData_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXDictData(sample)


@given(everything_except(dict))
def test_CXDictData_set_data_invalid(sample):
    dictdata = CXDictData()
    if sample is not None:
        with pytest.raises(TypeError):
            dictdata.data = sample


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_set_valid_dict(sample):
    candidate: CXDictData = CXDictData()

    candidate.data = sample
    assert candidate.data == sample

    candidate.data = CXDictData(sample)
    assert candidate.data == sample

    candidate.data = None
    assert len(candidate.data.keys()) == 0


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_get_valid_data(sample):
    cxdata = CXDictData()
    cxdata.data = sample
    assert not DeepDiff(sample, cxdata.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_copy_cxdictdata(sample):
    cxdict1 = CXDictData(sample)
    cxdict2 = copy(cxdict1)
    assert cxdict1 == cxdict2


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_deepcopy_cxdictdata(sample):
    cxdict1 = CXDictData(sample)
    cxdict2 = deepcopy(cxdict1)
    assert cxdict1 == cxdict2


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_str_perspective(sample):
    cxdict1 = CXDictData(sample)
    cxdict1_str = str(cxdict1)
    assert cxdict1_str == json.dumps(cxdict1.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_repr_perspective(sample):
    cxdict1 = CXDictData(sample)
    cxdict1_repr = repr(cxdict1)
    assert isinstance(cxdict1_repr, str)
    cxdict2: CXDictData = eval(cxdict1_repr)
    assert not DeepDiff(cxdict1.data, cxdict2.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1,
    )
)
def test_CXDictData_get_raw_dict_form(sample):
    cxdict1 = CXDictData(sample)
    output = cxdict1.get_raw_dict_form()
    assert output == cxdict1.data


def test_CXDictData_equality_None():
    sample_a: CXDictData = CXDictData({"a": 1})

    assert sample_a != None
    assert None < sample_a
    assert sample_a > None


def test_CXDictData_equality_junk():
    sample_a: CXDictData = CXDictData({"a": 1})

    for junk in [0, "0", [0]]:
        assert sample_a != junk
        assert junk < sample_a
        assert sample_a > junk


def test_CXDictData_equality():
    sample_a: CXDictData = CXDictData({"a": 1})
    sample_b: CXDictData = CXDictData({"a": 1})

    assert sample_a == sample_b

    sample_c: CXDictData = CXDictData({"c": 1})

    assert sample_a != sample_c
    assert sample_a < sample_c
    assert sample_c > sample_a

    sample_d: CXDictData = CXDictData()

    assert sample_a != sample_d
    assert sample_d < sample_a
    assert sample_a > sample_d

    sample_e: CXDictData = CXDictData({"c": 2})

    assert sample_c != sample_e
    assert sample_c < sample_e
    assert sample_e > sample_c

    sample_f: CXDictData = CXDictData({"c": 2, "d": 1})

    assert sample_c != sample_f
    assert sample_c < sample_f
    assert sample_f > sample_c
