import csv
from copy import copy, deepcopy

import pytest
from hypothesis import given
from hypothesis.extra.pandas import data_frames, column

from canvasxpress.data.matrix import CXCSVData
from tests.util.hypothesis_support import everything_except

csv_sample = """
"C1","C2","C3"
1,2,3
4,5,6
"""


@given(data_frames([column("A", dtype=int), column("B", dtype=int)]))
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


def test_CXCSVData_get_valid_data():
    cxdata = CXCSVData()
    cxdf_sample = csv_sample
    cxdata.csv = cxdf_sample


def test_copy_CXCSVData():
    cxdata1 = CXCSVData(csv_sample)
    cxdata2 = copy(cxdata1)
    assert cxdata1 == cxdata2


def test_deepcopy_CXCSVData():
    cxdata1 = CXCSVData(csv_sample)
    cxdata2 = deepcopy(cxdata1)
    assert cxdata1 == cxdata2


def test_CXCSVData_str_perspective():
    cxdata1 = CXCSVData(csv_sample)
    cxdata1_str = str(cxdata1).strip()
    assert cxdata1_str == csv_sample.strip()


def test_CXCSVData_repr_perspective():
    cxdata1 = CXCSVData(csv_sample)
    cxdata1_repr = repr(cxdata1)
    assert isinstance(cxdata1_repr, str)

    cxdata2: CXCSVData = eval(cxdata1_repr)
    assert cxdata1.csv == cxdata2.csv
