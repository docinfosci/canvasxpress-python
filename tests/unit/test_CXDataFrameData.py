import json
from copy import copy, deepcopy
from io import StringIO

import pandas
from pandas import DataFrame  # Required for eval

FORCE_INCLUDE_DATAFRAME_IN_PYCHARM = DataFrame()  # Prevents clean=up removal

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis.extra.pandas import data_frames, column

from canvasxpress.data.matrix import CXDataframeData, merge_dataframes_into_xyz_object
from tests.util.hypothesis_support import everything_except

csv_sample = """
"C1","C2","C3"
1,2,3
4,5,6
"""

df_sample = pandas.read_csv(StringIO(csv_sample), index_col=False)


def test_CXDataframeData_init_valid_input():
    cxdata = CXDataframeData(df_sample)
    df_sample.equals(cxdata.dataframe)

    cxdata = CXDataframeData(DataFrame())
    DataFrame().equals(cxdata.dataframe)

    cxdata = CXDataframeData(None)
    DataFrame().equals(cxdata.dataframe)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(everything_except(dict, str))
def test_CXDataframeData_init_invalid_input(sample):
    if sample is not None:
        with pytest.raises(TypeError):
            CXDataframeData(sample)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(everything_except(dict, str))
def test_CXDataframeData_set_data_invalid(sample):
    dictdata = CXDataframeData()
    if sample is not None:
        with pytest.raises(TypeError):
            dictdata.data = sample


def test_CXDataframeData_get_valid_data():
    cxdata = CXDataframeData()
    cxdf_sample = df_sample
    cxdata.dataframe = cxdf_sample

    # Comparing with CSV conversions is tricky because rounding, etc. for
    # numbers is not exact.  So, we inspect other aspects for general assurance
    # and assume if the other checks work then this likely has too.
    assert df_sample.shape == cxdata.dataframe.shape
    assert set(df_sample.columns.unique()) == set(cxdata.dataframe.columns.unique())

    cxdata = CXDataframeData()
    cxdata.dataframe = df_sample
    assert df_sample.equals(cxdata.dataframe)


def test_copy_CXDataframeData():
    cxdata1 = CXDataframeData(df_sample)
    cxdata2 = copy(cxdata1)
    assert cxdata1 == cxdata2


def test_deepcopy_CXDataframeData():
    cxdata1 = CXDataframeData(df_sample)
    cxdata2 = deepcopy(cxdata1)
    assert cxdata1 == cxdata2


def test_CXDataframeData_str_perspective():
    cxdata1 = CXDataframeData(df_sample)
    cxdata1_str = str(cxdata1)
    assert cxdata1_str == json.dumps(cxdata1.render_to_dict())


def test_CXDataframeData_repr_perspective():
    cxdata1 = CXDataframeData(df_sample)
    cxdata1_repr = repr(cxdata1)
    assert isinstance(cxdata1_repr, str)

    cxdata2: CXDataframeData = eval(cxdata1_repr)
    assert cxdata1 == cxdata2


def test_CXDataframeData_equality_None():
    sample_a: CXDataframeData = CXDataframeData(df_sample)

    assert sample_a != None
    assert None < sample_a
    assert sample_a > None


def test_CXDataframeData_equality_junk():
    sample_a: CXDataframeData = CXDataframeData(df_sample)

    for junk in [0, "0", [0]]:
        assert sample_a != junk
        assert junk < sample_a
        assert sample_a > junk


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(
    data_frames([column("A", dtype=int), column("B", dtype=float)]),
    data_frames([column("C", dtype=int), column("D", dtype=float)]),
    data_frames([column("E", dtype=int), column("F", dtype=float)]),
    data_frames([column("G", dtype=int), column("H", dtype=float)]),
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


def test_CXDataFrameData_xyz_assembly_meta_in_indexes():
    data = pandas.read_csv(
        StringIO('\n"C1","C2","C3"\n1,2,3\n4,5,6'),
        index_col=False,
    )

    sample_annotation = pandas.read_csv(
        StringIO('\n"C1", "a", "b"\n"C2", "c", "d"\n"C3", "e", "f"'),
        index_col=0,
        header=None,
    )

    variable_annotation = pandas.read_csv(
        StringIO('\n"0", "a", "b", "c"\n"1", "e", "f", "g"'),
        index_col=0,
        header=None,
    )

    xyz = merge_dataframes_into_xyz_object(
        data=CXDataframeData(data),
        sample_annotation=CXDataframeData(sample_annotation),
        variable_annotation=CXDataframeData(variable_annotation),
    )

    assert "y" in xyz
    assert "data" in xyz["y"]
    assert "smps" in xyz["y"]
    assert "vars" in xyz["y"]

    assert "x" in xyz
    assert all([key in xyz["y"]["smps"] for key in xyz["x"].keys()])

    assert "z" in xyz
    assert all([key in xyz["y"]["vars"] for key in xyz["z"].keys()])


def test_CXDataFrameData_xyz_assembly_meta_in_first_column():
    data = pandas.read_csv(
        StringIO('"C1","C2","C3"\n1,2,3\n4,5,6'),
        index_col=False,
    )

    sample_annotation = pandas.read_csv(
        StringIO('"C1","a","b"\n"C2","c","d"\n"C3","e","f"'),
        index_col=False,
        header=None,
    )

    variable_annotation = pandas.read_csv(
        StringIO('0,"a","b","c"\n1,"e","f","g"'),
        index_col=False,
        header=None,
    )

    xyz = merge_dataframes_into_xyz_object(
        data=CXDataframeData(data),
        sample_annotation=CXDataframeData(sample_annotation),
        variable_annotation=CXDataframeData(variable_annotation),
    )

    assert "y" in xyz
    assert "data" in xyz["y"]
    assert "smps" in xyz["y"]
    assert "vars" in xyz["y"]

    assert "x" in xyz
    assert all([key in xyz["y"]["smps"] for key in xyz["x"].keys()])

    assert "z" in xyz
    assert all([key in xyz["y"]["vars"] for key in xyz["z"].keys()])


def test_CXDataFrameData_xyz_assembly_meta_in_header():
    data = pandas.read_csv(
        StringIO('"C1","C2","C3"\n1,2,3\n4,5,6'),
        index_col=False,
    )

    sample_annotation = pandas.read_csv(
        StringIO('"C1","C2","C3"\n"a","b","c"\n"d","e","f"'),
        index_col=False,
    )

    variable_annotation = pandas.read_csv(
        StringIO('0,1\n"a","b"\n"c","d"\n"e","f"'),
        index_col=False,
    )
    variable_annotation.columns = variable_annotation.columns.astype(int)

    xyz = merge_dataframes_into_xyz_object(
        data=CXDataframeData(data),
        sample_annotation=CXDataframeData(sample_annotation),
        variable_annotation=CXDataframeData(variable_annotation),
    )

    assert "y" in xyz
    assert "data" in xyz["y"]
    assert "smps" in xyz["y"]
    assert "vars" in xyz["y"]

    assert "x" in xyz
    assert all([key in xyz["y"]["smps"] for key in xyz["x"].keys()])

    assert "z" in xyz
    assert all([key in xyz["y"]["vars"] for key in xyz["z"].keys()])


def test_CXDataFrameData_xyz_assembly_meta_in_first_row():
    data = pandas.read_csv(
        StringIO('"C1","C2","C3"\n1,2,3\n4,5,6'),
        index_col=False,
    )

    sample_annotation = pandas.read_csv(
        StringIO('"C1","C2","C3"\n"a","b","c"\n"d","e","f"'),
        index_col=False,
        header=None,
    )

    variable_annotation = pandas.read_csv(
        StringIO('0,1\n"a","b"\n"c","d"\n"e","f"'),
        index_col=False,
        header=None,
    )

    xyz = merge_dataframes_into_xyz_object(
        data=CXDataframeData(data),
        sample_annotation=CXDataframeData(sample_annotation),
        variable_annotation=CXDataframeData(variable_annotation),
    )

    assert "y" in xyz
    assert "data" in xyz["y"]
    assert "smps" in xyz["y"]
    assert "vars" in xyz["y"]

    assert "x" in xyz
    assert all([key in xyz["y"]["smps"] for key in xyz["x"].keys()])

    assert "z" in xyz
    assert all([key in xyz["y"]["vars"] for key in xyz["z"].keys()])


def test_CXDataFrameData_xyz_assembly_empty_annotations():
    data = pandas.read_csv(
        StringIO('"C1","C2","C3"\n1,2,3\n4,5,6'),
        index_col=False,
    )

    sample_annotation = DataFrame()
    variable_annotation = DataFrame()

    xyz = merge_dataframes_into_xyz_object(
        data=CXDataframeData(data),
        sample_annotation=CXDataframeData(sample_annotation),
        variable_annotation=CXDataframeData(variable_annotation),
    )

    assert "y" in xyz
    assert "data" in xyz["y"]
    assert "smps" in xyz["y"]
    assert "vars" in xyz["y"]

    assert "x" not in xyz

    assert "z" not in xyz
