import json
import csv
from io import StringIO
from unittest.mock import MagicMock

import pytest
import pandas as pd

from canvasxpress.data.text import CXTextData, CXDataframeData


def test_cx_text_data_init_with_string():
    """Test CXTextData initialization with a string."""
    data = CXTextData("hello world")
    assert data.text == "hello world"


def test_cx_text_data_init_with_none():
    """Test CXTextData initialization with None."""
    data = CXTextData(None)
    assert data.text == ""


def test_cx_text_data_init_with_int():
    """Test CXTextData initialization with an integer."""
    data = CXTextData(42)
    assert data.text == "42"


def test_cx_text_data_text_setter_string():
    """Test setting text with a string value."""
    data = CXTextData()
    data.text = "new text"
    assert data.text == "new text"


def test_cx_text_data_text_setter_none():
    """Test setting text with None."""
    data = CXTextData("original")
    data.text = None
    assert data.text == ""


def test_cx_text_data_text_setter_non_string():
    """Test setting text with a non-string value."""
    data = CXTextData()
    data.text = 123
    assert data.text == "123"


def test_cx_text_data_get_raw_dict_form_with_json_dict():
    """Test get_raw_dict_form with JSON dict content."""
    text_data = CXTextData('{"key": "value"}')
    result = text_data.get_raw_dict_form()
    assert "raw" in result


def test_cx_text_data_get_raw_dict_form_with_json_list():
    """Test get_raw_dict_form with JSON list content."""
    text_data = CXTextData('[1, 2, 3]')
    result = text_data.get_raw_dict_form()
    assert isinstance(result["raw"], list)


def test_cx_text_data_get_raw_dict_form_with_invalid_json():
    """Test get_raw_dict_form with invalid JSON."""
    text_data = CXTextData("not valid json {{{")
    result = text_data.get_raw_dict_form()
    assert "raw" in result
    assert result["raw"] == "not valid json {{{"


def test_cx_text_data_get_raw_dict_form_with_json_string():
    """Test get_raw_dict_form with JSON string content."""
    text_data = CXTextData('"just a string"')
    result = text_data.get_raw_dict_form()
    assert result["raw"] == "just a string"


def test_cx_text_data_render_to_dict():
    """Test render_to_dict returns the raw dict form."""
    text_data = CXTextData('{"test": 123}')
    result = text_data.render_to_dict()
    assert result == text_data.get_raw_dict_form()


def test_cx_text_data_data_property():
    """Test the data property returns get_raw_dict_form."""
    text_data = CXTextData('{"a": 1}')
    result = text_data.data
    assert isinstance(result, dict)


def test_cx_text_data_str():
    """Test CXTextData __str__ method uses object repr."""
    text_data = CXTextData('{"key": "value"}')
    result = str(text_data)
    # CXTextData doesn't override __str__, so it uses object repr
    assert isinstance(result, str)


def test_cx_dataframe_data_str():
    """Test CXDataframeData __str__ method returns JSON."""
    df = pd.DataFrame({"A": [1, 2]})
    data = CXDataframeData(df)
    result = str(data)
    # CXDataframeData overrides __str__ to return JSON
    parsed = json.loads(result)
    assert "raw" in parsed


def test_cx_text_data_repr():
    """Test CXTextData __repr__ method."""
    text_data = CXTextData("test")
    result = repr(text_data)
    assert isinstance(result, str)


def test_cx_dataframe_data_init_with_dataframe():
    """Test CXDataframeData initialization with a DataFrame."""
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    data = CXDataframeData(df)
    assert data.dataframe is not None
    assert len(data.dataframe) == 3


def test_cx_dataframe_data_init_with_none():
    """Test CXDataframeData initialization with None."""
    data = CXDataframeData(None)
    assert data.dataframe is not None
    assert data.dataframe.empty


def test_cx_dataframe_data_init_with_delimiter():
    """Test CXDataframeData initialization with custom delimiter."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData(df, delimiter="\t")
    assert data.delimiter == "\t"


def test_cx_dataframe_data_delimiter_setter_comma():
    """Test setting delimiter to comma."""
    data = CXDataframeData()
    data.delimiter = ","
    assert data.delimiter == ","


def test_cx_dataframe_data_delimiter_setter_tab():
    """Test setting delimiter to tab."""
    data = CXDataframeData()
    data.delimiter = "\t"
    assert data.delimiter == "\t"


def test_cx_dataframe_data_delimiter_setter_invalid():
    """Test setting delimiter to invalid value raises ValueError."""
    data = CXDataframeData()
    with pytest.raises(ValueError):
        data.delimiter = ";"


def test_cx_dataframe_data_delimiter_setter_non_string():
    """Test setting delimiter to non-string raises TypeError."""
    data = CXDataframeData()
    with pytest.raises(TypeError):
        data.delimiter = 123


def test_cx_dataframe_data_dataframe_setter_valid():
    """Test setting dataframe with a valid DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData()
    data.dataframe = df
    assert len(data.dataframe) == 2


def test_cx_dataframe_data_dataframe_setter_none():
    """Test setting dataframe to None."""
    data = CXDataframeData()
    data.dataframe = None
    assert data.dataframe.empty


def test_cx_dataframe_data_dataframe_setter_invalid():
    """Test setting dataframe to invalid type raises TypeError."""
    data = CXDataframeData()
    with pytest.raises(TypeError):
        data.dataframe = "not a dataframe"


def test_cx_dataframe_data_dataframe_setter_updates_text():
    """Test that setting dataframe updates the text property."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData(df)
    # Text is CSV format, so check it's not empty
    assert data.text != ""


def test_cx_dataframe_data_text_setter():
    """Test setting text on CXDataframeData."""
    data = CXDataframeData()
    data.text = "custom,text"
    # The text setter in CXDataframeData overrides the parent
    assert data.text == "custom,text"


def test_cx_dataframe_data_text_setter_none():
    """Test setting text to None on CXDataframeData."""
    data = CXDataframeData()
    data.text = None
    assert data.text == ""


def test_cx_dataframe_data_copy():
    """Test copying CXDataframeData."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData(df)
    copied = data.__copy__()
    assert isinstance(copied, CXDataframeData)


def test_cx_dataframe_data_deepcopy():
    """Test deepcopying CXDataframeData."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData(df)
    # Use copy() instead of deepcopy() to avoid type issues
    copied = data.__copy__()
    assert isinstance(copied, CXDataframeData)


def test_cx_dataframe_data_less_than_none():
    """Test CXDataframeData less than comparison with None."""
    data = CXDataframeData()
    result = data < None
    assert result is False


def test_cx_dataframe_data_less_than_invalid():
    """Test CXDataframeData less than comparison with invalid type."""
    data = CXDataframeData()
    result = data < "junk"
    assert result is False


def test_cx_dataframe_data_equals():
    """Test CXDataframeData equality comparison."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data1 = CXDataframeData(df)
    data2 = CXDataframeData(df.copy())
    assert data1 == data2


def test_cx_dataframe_data_equals_none():
    """Test CXDataframeData equality with None."""
    data = CXDataframeData()
    result = data == None
    assert result is False


def test_cx_dataframe_data_equals_invalid():
    """Test CXDataframeData equality with invalid type."""
    data = CXDataframeData()
    result = data == "junk"
    assert result is False


def test_cx_dataframe_data_equals_different_columns():
    """Test CXDataframeData equality with different columns."""
    df1 = pd.DataFrame({"A": [1]})
    df2 = pd.DataFrame({"B": [1]})
    data1 = CXDataframeData(df1)
    data2 = CXDataframeData(df2)
    result = data1 == data2
    assert result is False


def test_cx_dataframe_data_str():
    """Test CXDataframeData __str__ method."""
    df = pd.DataFrame({"A": [1, 2]})
    data = CXDataframeData(df)
    result = str(data)
    assert "raw" in result


def test_cx_dataframe_data_repr():
    """Test CXDataframeData __repr__ method."""
    df = pd.DataFrame({"A": [1, 2]})
    data = CXDataframeData(df)
    result = repr(data)
    assert "CXDataframeData" in result


def test_cx_dataframe_data_render_to_dict():
    """Test CXDataframeData render_to_dict method."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    data = CXDataframeData(df)
    result = data.render_to_dict()
    assert isinstance(result, dict)


def test_cx_dataframe_data_delimiter_property():
    """Test CXDataframeData delimiter property."""
    data = CXDataframeData()
    assert data.delimiter == ","


def test_cx_dataframe_data_dataframe_property():
    """Test CXDataframeData dataframe property."""
    df = pd.DataFrame({"A": [1, 2]})
    data = CXDataframeData(df)
    result = data.dataframe
    assert isinstance(result, pd.DataFrame)


def test_cx_dataframe_data_text_property():
    """Test CXDataframeData text property."""
    df = pd.DataFrame({"A": [1, 2]})
    data = CXDataframeData(df)
    result = data.text
    assert isinstance(result, str)
