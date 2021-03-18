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
        min_size=1
    )
)
def test_cxdictdata_init_valid_input(sample):
    cxdata = CXDictData(sample)
    assert not DeepDiff(sample, cxdata.data)


@given(everything_except(dict))
def test_cxdictdata_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXDictData(sample)


@given(everything_except(dict))
def test_cxdictdata_set_data_invalid(sample):
    dictdata = CXDictData()
    with pytest.raises(TypeError):
        dictdata.data = sample


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_cxdictdata_get_valid_data(sample):
    cxdata = CXDictData()
    cxdata.data = sample
    assert not DeepDiff(sample, cxdata.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
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
        min_size=1
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
        min_size=1
    )
)
def test_cxdictdata_str_perspective(sample):
    cxdict1 = CXDictData(sample)
    cxdict1_str = str(cxdict1)
    assert cxdict1_str == json.dumps(cxdict1.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_cxdictdata_repr_perspective(sample):
    cxdict1 = CXDictData(sample)
    cxdict1_repr = repr(cxdict1)
    assert isinstance(cxdict1_repr, str)
    cxdict2: CXDictData = eval(cxdict1_repr)
    assert not DeepDiff(cxdict1.data, cxdict2.data)


@given(
    dictionaries(
        keys=text(alphabet=string.ascii_letters, min_size=5),
        values=text(alphabet=string.ascii_letters, min_size=5),
        min_size=1
    )
)
def test_cxdictdata_render_to_dict(sample):
    cxdict1 = CXDictData(sample)
    output = cxdict1.render_to_dict()
    assert output == cxdict1.data
