import pytest

from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.matrix import CXCSVData
from canvasxpress.data.profile import CXRawProfile


def test_render_to_profiled_dict_matrix():
    candidate = CXRawProfile()

    assert candidate.render_to_profiled_dict(None) == dict()

    data = CXCSVData(
        """
        A, B
        1, 2
        """
    )
    result = candidate.render_to_profiled_dict(data)
    assert result == data.get_raw_dict_form()


def test_render_to_profiled_dict_keypair():
    candidate = CXRawProfile()

    assert candidate.render_to_profiled_dict(None) == dict()

    data = CXDictData(
        {
            "y": {
                "vars": ["Variable1", "Variable2"],
                "smps": ["Sample1", "Sample2", "Sample3"],
                "data": [[10, 20, 30], [35, 25, 15]],
            },
            "x": {"Tissue": ["Kidney", "Lung", "Heart"], "Donor": ["D1", "D1", "D2"]},
            "z": {"Symbol": ["AAA", "BBB"], "Pathway": ["P1", "P2"]},
        }
    )
    result = candidate.render_to_profiled_dict(data)
    assert result == data.get_raw_dict_form()
