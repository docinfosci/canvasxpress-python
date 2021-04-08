import json
from copy import copy, deepcopy

from pandas import DataFrame  # Required for eval

FORCE_INCLUDE_DATAFRAME_IN_PYCHARM = DataFrame()  # Prevents clean=up removal

import numpy
import pytest
from deepdiff import DeepDiff
from hypothesis import given
from hypothesis.extra.pandas import data_frames, column

from canvasxpress.data.matrix import CXDataframeData
from tests.util.hypothesis_support import everything_except


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_init_valid_input(sample):
    cxdata = CXDataframeData(sample)
    assert sample.equals(cxdata.dataframe)


@given(everything_except(dict, str))
def test_CXDataframeData_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXDataframeData(sample)


@given(everything_except(dict, str))
def test_CXDataframeData_set_data_invalid(sample):
    dictdata = CXDataframeData()
    with pytest.raises(TypeError):
        dictdata.data = sample


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_get_valid_data(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata = CXDataframeData()
    cxdf_sample = json.dumps(dict_sample)
    cxdata.dataframe = cxdf_sample
    assert cxdf_sample == json.dumps(cxdata.data)

    cxdata = CXDataframeData()
    cxdf_sample = sample.to_csv(index=False)
    cxdata.dataframe = cxdf_sample

    # Comparing with CSV conversions is tricky because rounding, etc. for
    # numbers is not exact.  So, we inspect other aspects for general assurance
    # and assume if the other checks work then this likely has too.
    assert sample.shape == cxdata.dataframe.shape
    assert set(sample.columns.unique()) == \
           set(cxdata.dataframe.columns.unique())

    cxdata = CXDataframeData()
    cxdf_sample = CXDataframeData(sample)
    cxdata.dataframe = cxdf_sample
    assert cxdf_sample == cxdata

    cxdata = CXDataframeData()
    cxdf_sample = CXDataframeData(sample)
    cxdata.data = cxdf_sample
    assert cxdf_sample == cxdata

    cxdata = CXDataframeData()
    cxdata.dataframe = sample
    assert sample.equals(cxdata.dataframe)

    cxdata = CXDataframeData()
    cxdata.dataframe = dict_sample
    assert not DeepDiff(dict_sample, cxdata.data)

    cxdata = CXDataframeData()
    cxdata.data = dict_sample
    assert not DeepDiff(dict_sample, cxdata.data)


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_copy_CXDataframeData(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata1 = CXDataframeData(sample)
    cxdata2 = copy(cxdata1)
    assert cxdata1 == cxdata2


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_deepcopy_CXDataframeData(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata1 = CXDataframeData(sample)
    cxdata2 = deepcopy(cxdata1)
    assert cxdata1 == cxdata2


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_str_perspective(sample):
    cxdata1 = CXDataframeData(sample)
    cxdata1_str = str(cxdata1)
    assert cxdata1_str == json.dumps(cxdata1.data)


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_repr_perspective(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata1 = CXDataframeData(sample)
    cxdata1_repr = repr(cxdata1)
    assert isinstance(cxdata1_repr, str)

    cxdata2: CXDataframeData = eval(cxdata1_repr)
    assert cxdata1 == cxdata2


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_render_to_dict(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata1 = CXDataframeData(dict_sample)
    output = cxdata1.render_to_dict()
    assert not DeepDiff(output, cxdata1.data)


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_equality_None(sample):
    sample_a: CXDataframeData = CXDataframeData(sample)

    assert sample_a != None
    assert None < sample_a
    assert sample_a > None


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXDataframeData_equality_junk(sample):
    sample_a: CXDataframeData = CXDataframeData(sample)

    for junk in [0, "0", [0]]:
        assert sample_a != junk
        assert junk < sample_a
        assert sample_a > junk


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)]),
    data_frames([column('C', dtype=int), column('D', dtype=float)]),
    data_frames([column('E', dtype=int), column('F', dtype=float)]),
    data_frames([column('G', dtype=int), column('H', dtype=float)])
)
def test_CXDataframeData_equality(sample1, sample2, sample3, sample4):
    for sample in [sample1, sample2, sample3, sample4]:
        # Do not test with empty dataframes
        if sample.empty:
            return

        # Do not test with NaN, etc. values (cannot be compared)
        elif sample.isnull().values.any(axis=None):
            return

    sample_a: CXDataframeData = CXDataframeData(sample1)
    sample_b: CXDataframeData = CXDataframeData(sample1)
    assert sample_a == sample_b

    if not sample1.eq(sample2).all(axis=None):
        sample_c: CXDataframeData = CXDataframeData(sample2)
        assert sample_a != sample_c
        assert sample_a < sample_c
        assert sample_c > sample_a

    sample_d: CXDataframeData = CXDataframeData()
    assert sample_a != sample_d
    assert sample_d < sample_a
    assert sample_a > sample_d

    if not sample2.eq(sample3).all(axis=None):
        sample_e: CXDataframeData = CXDataframeData(sample3)
        assert sample_c != sample_e
        assert sample_c < sample_e
        assert sample_e > sample_c

    if not sample2.eq(sample4).all(axis=None):
        sample_f: CXDataframeData = CXDataframeData(sample4)
        assert sample_c != sample_f
        assert sample_c < sample_f
        assert sample_f > sample_c
