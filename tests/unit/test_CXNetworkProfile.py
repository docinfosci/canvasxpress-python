import pytest

from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.matrix import CXCSVData
from canvasxpress.data.profile import CXNetworkProfile


def test_render_to_profiled_dict_matrix():
    candidate = CXNetworkProfile()

    data = CXCSVData(
        """
        A, B
        1, 2
        """
    )

    with pytest.raises(TypeError):
        candidate.render_to_profiled_dict(None)

    with pytest.raises(TypeError):
        candidate.render_to_profiled_dict(data)


def test_render_to_profiled_dict_keypair():
    data = CXDictData(
        {
            "nodes": [
                {"id": "Node1", "color": "rgb(255,0,0)", "shape": "circle", "size": 1},
                {
                    "id": "Node2",
                    "color": "rgb(0,255,0)",
                    "shape": "square",
                    "size": 1.5,
                },
                {
                    "id": "Node3",
                    "color": "rgb(0,0,255)",
                    "shape": "triangle",
                    "size": 2,
                },
            ],
            "edges": [
                {"id1": "Node1", "id2": "Node2", "color": "rgb(125,125,0)"},
                {"id1": "Node1", "id2": "Node3", "color": "rgb(0,125,125)"},
                {"id1": "Node2", "id2": "Node3", "color": "rgb(125,0,125)"},
            ],
        }
    )

    candidate = CXNetworkProfile()

    result = candidate.render_to_profiled_dict(data)
    assert result == data.get_raw_dict_form()

    with pytest.raises(TypeError):
        candidate.render_to_profiled_dict(None)

    with pytest.raises(ValueError):
        candidate.render_to_profiled_dict(CXDictData())
