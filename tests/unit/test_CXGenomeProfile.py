import pytest

from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.matrix import CXCSVData
from canvasxpress.data.profile import CXGenomeProfile


def test_render_to_profiled_dict_matrix():
    candidate = CXGenomeProfile()

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
            "tracks": [
                {
                    "name": "Affy Probes",
                    "type": "box",
                    "connect": True,
                    "fill": "rgb(255,255,51)",
                    "line": "rgb(0,0,0)",
                    "data": [
                        {
                            "id": "123456_at",
                            "dir": "right",
                            "data": [[100, 120], [123, 132], [141, 160]],
                        },
                        {
                            "id": "234567_at",
                            "dir": "left",
                            "data": [[181, 200], [211, 230], [251, 270]],
                        },
                        {
                            "id": "345678_at",
                            "dir": "right",
                            "data": [[281, 300], [311, 330], [351, 370]],
                        },
                    ],
                },
                {
                    "hide": True,
                    "type": "bar",
                    "height": 20,
                    "fill": ["rgb(255,0,0)", "rgb(0,0,255)", "rgb(255,255,0)"],
                    "line": ["rgb(255,0,0)", "rgb(0,0,255)", "rgb(255,255,0)"],
                    "data": [
                        {"id": "123456_at", "data": [100, 25, 35, 46]},
                        {"id": "234567_at", "data": [181, 80, 45, 10]},
                        {"id": "345678_at", "data": [281, 65, 46, 29]},
                    ],
                },
                {
                    "name": "Tissue Distribution (Heart, Liver, Kidney)",
                    "hide": False,
                    "type": "heatmap",
                    "autowidth": True,
                    "height": 20,
                    "line": "rgb(0,0,0)",
                    "smps": ["Heart", "Kidney", "Liver"],
                    "data": [
                        {"id": "123456_at", "data": [100, 25, 35, 46]},
                        {"id": "234567_at", "data": [181, 80, 45, 10]},
                        {"id": "345678_at", "data": [281, 65, 46, 29]},
                    ],
                },
                {
                    "name": "SNP",
                    "type": "triangle",
                    "fill": "rgb(100,0,0)",
                    "line": "rgb(0,0,0)",
                    "data": [
                        {"id": "SNP123", "data": 123},
                        {"id": "SNP234", "data": 145},
                        {"id": "SNP789", "data": 220},
                    ],
                },
                {
                    "name": "SNP",
                    "type": "line",
                    "line": "rgb(0,255,0)",
                    "data": [
                        {"id": "SNP123", "data": 123},
                        {"id": "SNP234", "data": 145},
                        {"id": "SNP789", "data": 220},
                    ],
                },
                {
                    "type": "sequence",
                    "subtype": "DNA",
                    "hide": True,
                    "line": "rgb(255,255,255)",
                    "data": [
                        {"id": "SNP123", "data": [119, "AGCT[TA]CGAG"]},
                        {"id": "SNP234", "data": [141, "ATCG[TG]AATA"]},
                        {"id": "SNP789", "data": [216, "GCCC[CT]AGGG"]},
                    ],
                },
            ]
        }
    )

    candidate = CXGenomeProfile()

    result = candidate.render_to_profiled_dict(data)
    assert result == data.get_raw_dict_form()

    with pytest.raises(TypeError):
        candidate.render_to_profiled_dict(None)

    with pytest.raises(ValueError):
        candidate.render_to_profiled_dict(CXDictData())

    with pytest.raises(ValueError):
        candidate.render_to_profiled_dict(
            CXDictData(
                {
                    "fred": [
                        {
                            "name": "Affy Probes",
                            "type": "box",
                            "connect": True,
                            "fill": "rgb(255,255,51)",
                            "line": "rgb(0,0,0)",
                            "data": [
                                {
                                    "id": "123456_at",
                                    "dir": "right",
                                    "data": [[100, 120], [123, 132], [141, 160]],
                                },
                                {
                                    "id": "234567_at",
                                    "dir": "left",
                                    "data": [[181, 200], [211, 230], [251, 270]],
                                },
                                {
                                    "id": "345678_at",
                                    "dir": "right",
                                    "data": [[281, 300], [311, 330], [351, 370]],
                                },
                            ],
                        }
                    ]
                }
            )
        )

    with pytest.raises(ValueError):
        candidate.render_to_profiled_dict(
            CXDictData({"tracks": [{"name": "Affy Probes"}]})
        )

    with pytest.raises(ValueError):
        candidate.render_to_profiled_dict(CXDictData({"tracks": [123]}))
