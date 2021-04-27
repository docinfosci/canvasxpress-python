import csv
from copy import copy, deepcopy

import numpy
import pytest
from hypothesis import given
from hypothesis.extra.pandas import data_frames, column

from canvasxpress.data.matrix import CXCSVData
from tests.util.hypothesis_support import everything_except


@given(
    data_frames([column('A', dtype=int), column('B', dtype=int)])
)
def test_CXCSVData_init_valid_input(sample):
    csv_sample = sample.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
    cxdata = CXCSVData(csv_sample)
    assert csv_sample == cxdata.csv


@given(everything_except(dict, str))
def test_CXCSVData_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXCSVData(sample)


@given(everything_except(dict, str))
def test_CXCSVData_set_data_invalid(sample):
    csvdata = CXCSVData()
    if sample is not None:
        with pytest.raises(TypeError):
            csvdata.csv = sample


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_CXCSVData_get_valid_data(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    cxdata = CXCSVData()
    cxdf_sample = sample.to_csv(index=False)
    cxdata.csv = cxdf_sample


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_copy_CXCSVData(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    csv_sample = sample.to_csv(index=False)

    cxdata1 = CXCSVData(csv_sample)
    cxdata2 = copy(cxdata1)
    assert cxdata1 == cxdata2


@given(
    data_frames([column('A', dtype=int), column('B', dtype=float)])
)
def test_deepcopy_CXCSVData(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    csv_sample = sample.to_csv(index=False)

    cxdata1 = CXCSVData(csv_sample)
    cxdata2 = deepcopy(cxdata1)
    assert cxdata1 == cxdata2


@given(
    data_frames([column('A', dtype=int), column('B', dtype=int)])
)
def test_CXCSVData_str_perspective(sample):
    csv_sample = sample.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
    cxdata1 = CXCSVData(csv_sample)
    cxdata1_str = str(cxdata1)
    assert cxdata1_str == csv_sample


@given(
    data_frames([column('A', dtype=int), column('B', dtype=int)])
)
def test_CXCSVData_repr_perspective(sample):
    dict_sample = sample.to_dict(orient="list")
    for k in dict_sample.keys():
        for i in dict_sample[k]:
            if numpy.isnan(i): return  # Cannot compare dicts with NaN

    csv_sample = sample.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)

    cxdata1 = CXCSVData(csv_sample)
    cxdata1_repr = repr(cxdata1)
    assert isinstance(cxdata1_repr, str)

    cxdata2: CXCSVData = eval(cxdata1_repr)
    assert cxdata1.csv == cxdata2.csv
