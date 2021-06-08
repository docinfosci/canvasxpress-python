import pytest
from pandas import DataFrame

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXInt
from canvasxpress.data.base import CXDataProfileException, VENN, DATA, LEGEND
from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.matrix import CXDataframeData
from canvasxpress.data.profile import CXVennProfile


def test_legend():
    candidate = CXVennProfile()
    assert candidate.legend == {}

    candidate.legend = {"A": 2}
    assert candidate.legend == {"A": 2}

    candidate.legend = None
    assert candidate.legend == {}

    with pytest.raises(TypeError):
        candidate.legend = 123


def test_render_to_profiled_dict_matrix():
    candidate = CXVennProfile()

    with pytest.raises(CXDataProfileException):
        candidate.render_to_profiled_dict(None)

    result = candidate.render_to_profiled_dict(
        CXDataframeData(
            DataFrame.from_dict(
                data={
                    "A": [10],
                    "B": [20],
                    "C": [30]
                },
                orient="index",
                columns=["data"]
            )
        )
    )
    assert result == {
        VENN: {
            DATA: {
                "A": 10,
                "B": 20,
                "C": 30
            },
            LEGEND: {}
        }
    }

    result = candidate.render_to_profiled_dict(
        CXDataframeData(
            DataFrame.from_dict(
                data={
                    "A": [10],
                    "B": [20],
                    "AB": [30]
                },
                orient="index",
                columns=["data"]
            )
        ),
        config=CXConfigs(
            CXInt("vennGroups", 2)
        )
    )
    assert result == {
        VENN: {
            DATA: {
                "A": 10,
                "B": 20,
                "AB": 30
            },
            LEGEND: {
                'A': 'Group 1',
                'B': 'Group 2'
            }
        }
    }

    candidate.legend = {
        "A": "Frankie",
        "B": "Louise"
    }
    result = candidate.render_to_profiled_dict(
        CXDataframeData(
            DataFrame.from_dict(
                data={
                    "A": [10],
                    "B": [20],
                    "AB": [30]
                },
                orient="index",
                columns=["data"]
            )
        ),
        config=CXConfigs(
            CXInt("vennGroups", 2)
        )
    )
    assert result == {
        VENN: {
            DATA: {
                "A": 10,
                "B": 20,
                "AB": 30
            },
            LEGEND: {
                'A': 'Frankie',
                'B': 'Louise'
            }
        }
    }


def test_render_to_profiled_dict_keypair():
    candidate = CXVennProfile()

    with pytest.raises(CXDataProfileException):
        candidate.render_to_profiled_dict(None)

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "venn": {
                    "data": {
                        "A": 340,
                        "AB": 639,
                        "ABC": 552,
                        "ABCD": 148,
                        "ABD": 578,
                        "AC": 456,
                        "ACD": 298,
                        "AD": 257,
                        "B": 562,
                        "BC": 915,
                        "BCD": 613,
                        "BD": 354,
                        "C": 620,
                        "CD": 143,
                        "D": 592
                    },
                    "legend": {
                        "A": "List 1",
                        "B": "List 2",
                        "C": "List 3",
                        "D": "List 4"
                    }
                }
            }
        )
    )
    assert result == {
        "venn": {
            "data": {
                "A": 340,
                "AB": 639,
                "ABC": 552,
                "ABCD": 148,
                "ABD": 578,
                "AC": 456,
                "ACD": 298,
                "AD": 257,
                "B": 562,
                "BC": 915,
                "BCD": 613,
                "BD": 354,
                "C": 620,
                "CD": 143,
                "D": 592
            },
            "legend": {
                "A": "List 1",
                "B": "List 2",
                "C": "List 3",
                "D": "List 4"
            }
        }
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "data": {
                    "A": 340,
                    "AB": 639,
                    "ABC": 552,
                    "ABCD": 148,
                    "ABD": 578,
                    "AC": 456,
                    "ACD": 298,
                    "AD": 257,
                    "B": 562,
                    "BC": 915,
                    "BCD": 613,
                    "BD": 354,
                    "C": 620,
                    "CD": 143,
                    "D": 592
                },
                "legend": {
                    "A": "List 1",
                    "B": "List 2",
                    "C": "List 3",
                    "D": "List 4"
                }
            }
        )
    )
    assert result == {
        "venn": {
            "data": {
                "A": 340,
                "AB": 639,
                "ABC": 552,
                "ABCD": 148,
                "ABD": 578,
                "AC": 456,
                "ACD": 298,
                "AD": 257,
                "B": 562,
                "BC": 915,
                "BCD": 613,
                "BD": 354,
                "C": 620,
                "CD": 143,
                "D": 592
            },
            "legend": {
                "A": "List 1",
                "B": "List 2",
                "C": "List 3",
                "D": "List 4"
            }
        }
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "data": {
                    "A": 340,
                    "AB": 639,
                    "ABC": 552,
                    "ABCD": 148,
                    "ABD": 578,
                    "AC": 456,
                    "ACD": 298,
                    "AD": 257,
                    "B": 562,
                    "BC": 915,
                    "BCD": 613,
                    "BD": 354,
                    "C": 620,
                    "CD": 143,
                    "D": 592
                }
            }
        )
    )
    assert result == {
        "venn": {
            "data": {
                "A": 340,
                "AB": 639,
                "ABC": 552,
                "ABCD": 148,
                "ABD": 578,
                "AC": 456,
                "ACD": 298,
                "AD": 257,
                "B": 562,
                "BC": 915,
                "BCD": 613,
                "BD": 354,
                "C": 620,
                "CD": 143,
                "D": 592
            },
            "legend": {}
        }
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "data": {
                    "A": 340,
                    "AB": 639,
                    "ABC": 552,
                    "ABCD": 148,
                    "ABD": 578,
                    "AC": 456,
                    "ACD": 298,
                    "AD": 257,
                    "B": 562,
                    "BC": 915,
                    "BCD": 613,
                    "BD": 354,
                    "C": 620,
                    "CD": 143,
                    "D": 592
                }
            }
        ),
        config = CXConfigs(
            CXInt("vennGroups", 4)
        )
    )
    assert result == {
        "venn": {
            "data": {
                "A": 340,
                "AB": 639,
                "ABC": 552,
                "ABCD": 148,
                "ABD": 578,
                "AC": 456,
                "ACD": 298,
                "AD": 257,
                "B": 562,
                "BC": 915,
                "BCD": 613,
                "BD": 354,
                "C": 620,
                "CD": 143,
                "D": 592
            },
            "legend": {
                "A": "Group 1",
                "B": "Group 2",
                "C": "Group 3",
                "D": "Group 4"
            }
        }
    }

    candidate.legend = {
        "A": "Frankie",
        "B": "Louise",
        "C": "Sammy",
        "D": "Cassidy"
    }
    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "data": {
                    "A": 340,
                    "AB": 639,
                    "ABC": 552,
                    "ABCD": 148,
                    "ABD": 578,
                    "AC": 456,
                    "ACD": 298,
                    "AD": 257,
                    "B": 562,
                    "BC": 915,
                    "BCD": 613,
                    "BD": 354,
                    "C": 620,
                    "CD": 143,
                    "D": 592
                }
            }
        ),
        config = CXConfigs(
            CXInt("vennGroups", 4)
        )
    )
    assert result == {
        "venn": {
            "data": {
                "A": 340,
                "AB": 639,
                "ABC": 552,
                "ABCD": 148,
                "ABD": 578,
                "AC": 456,
                "ACD": 298,
                "AD": 257,
                "B": 562,
                "BC": 915,
                "BCD": 613,
                "BD": 354,
                "C": 620,
                "CD": 143,
                "D": 592
            },
            "legend": {
                "A": "Frankie",
                "B": "Louise",
                "C": "Sammy",
                "D": "Cassidy"
            }
        }
    }
