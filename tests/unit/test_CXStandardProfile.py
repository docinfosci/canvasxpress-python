from copy import deepcopy

import pytest
from pandas import DataFrame

from canvasxpress.data.base import X, Z, CXDataProfileException, VARS, Y, SMPS, DATA
from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.matrix import CXDataframeData
from canvasxpress.data.profile import CXStandardProfile


def test_set_vars():
    candidate = CXStandardProfile()

    with pytest.raises(TypeError):
        candidate.vars = 123

    candidate.vars = ["a", "b", "c"]
    assert candidate.vars == ["a", "b", "c"]
    assert candidate.y[VARS] == ["a", "b", "c"]

    candidate.vars = None
    assert candidate.vars == []
    assert candidate.y[VARS] == []


def test_set_smps():
    candidate = CXStandardProfile()

    with pytest.raises(TypeError):
        candidate.smps = 123

    candidate.smps = ["a", "b", "c"]
    assert candidate.smps == ["a", "b", "c"]
    assert candidate.y[SMPS] == ["a", "b", "c"]

    candidate.smps = None
    assert candidate.smps == []
    assert candidate.y[VARS] == []


def test_set_y():
    candidate = CXStandardProfile()

    candidate.y = {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        }
    }
    assert candidate.y == {
        "vars": ["Variable1", "Variable2"],
        "smps": ["Sample1", "Sample2", "Sample3"],
        "data": [[10, 20, 30],
                 [35, 25, 15]]
    }

    candidate.y = {
        "vars": ["Variable1", "Variable2"],
        "smps": ["Sample1", "Sample2", "Sample3"],
        "data": [[10, 20, 30],
                 [35, 25, 15]]
    }
    assert candidate.y == {
        "vars": ["Variable1", "Variable2"],
        "smps": ["Sample1", "Sample2", "Sample3"],
        "data": [[10, 20, 30],
                 [35, 25, 15]]
    }

    candidate.y = None
    assert candidate.y == {
        VARS: [],
        SMPS: []
    }

    with pytest.raises(TypeError):
        candidate.y = 123

    with pytest.raises(TypeError):
        candidate.y = {
            "y": 123
        }

    with pytest.raises(TypeError):
        candidate.y = {
            "y": {
                "vars": 123,
                "smps": ["Sample1", "Sample2", "Sample3"],
                "data": [[10, 20, 30],
                         [35, 25, 15]]
            }
        }


def test_set_x():
    candidate = CXStandardProfile()

    with pytest.raises(TypeError):
        candidate.x = 123

    candidate.x = None
    assert candidate.x == {}

    candidate.x = {
        X: {
            "example": ["a"]
        }
    }
    assert candidate.x == {
        "example": ["a"]
    }

    candidate.x = {
        "example": ["a"]
    }
    assert candidate.x == {
        "example": ["a"]
    }

    with pytest.raises(TypeError):
        candidate.x = {
            X: ["a"]
        }

    with pytest.raises(TypeError):
        candidate.x = {
            X: 123
        }

    with pytest.raises(TypeError):
        candidate.x = {
            "a": 123
        }


def test_set_z():
    candidate = CXStandardProfile()

    with pytest.raises(TypeError):
        candidate.z = 123

    candidate.z = None
    assert candidate.z == {}

    candidate.z = {
        Z: {
            "example": ["a"]
        }
    }
    assert candidate.z == {
        "example": ["a"]
    }

    candidate.z = {
        "example": ["a"]
    }
    assert candidate.z == {
        "example": ["a"]
    }

    with pytest.raises(TypeError):
        candidate.z = {
            Z: ["a"]
        }

    with pytest.raises(TypeError):
        candidate.z = {
            Z: 123
        }

    with pytest.raises(TypeError):
        candidate.z = {
            "a": 123
        }


def test_render_to_profiled_dict_keypair():
    candidate = CXStandardProfile()

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "y": {
                    "vars": ["Variable1", "Variable2"],
                    "smps": ["Sample1", "Sample2", "Sample3"],
                    "data": [[10, 20, 30],
                             [35, 25, 15]]
                },
                "x": {
                    "Tissue": ["Kidney", "Lung", "Heart"],
                    "Donor": ["D1", "D1", "D2"]
                },
                "z": {
                    "Symbol": ["AAA", "BBB"],
                    "Pathway": ["P1", "P2"]
                }
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {
            "Tissue": ["Kidney", "Lung", "Heart"],
            "Donor": ["D1", "D1", "D2"]
        },
        "z": {
            "Symbol": ["AAA", "BBB"],
            "Pathway": ["P1", "P2"]
        }
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "vars": ["Variable1", "Variable2"],
                "smps": ["Sample1", "Sample2", "Sample3"],
                "data": [[10, 20, 30],
                         [35, 25, 15]]
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {}
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "vars": ["Variable1", "Variable2"],
                "smps": ["Sample1", "Sample2", "Sample3"],
                "cors": [[10, 20, 30],
                         [35, 25, 15]]
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "cors": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {}
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "cors": [[10, 20, 30],
                         [35, 25, 15]]
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": [0, 1],
            "smps": [0, 1, 2],
            "cors": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {}
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "y": {
                    "smps": ["Sample1", "Sample2", "Sample3"],
                    "data": [[10, 20, 30],
                             [35, 25, 15]]
                }
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": [0, 1],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }

    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "y": {
                    "vars": ["Variable1", "Variable2"],
                    "data": [[10, 20, 30],
                             [35, 25, 15]]
                }
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": [0, 1, 2],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }

    candidate.vars = ["a", "b"]
    candidate.smps = ["a", "b", "c"]
    result = candidate.render_to_profiled_dict(
        CXDictData(
            {
                "y": {
                    "vars": ["Variable1", "Variable2"],
                    "smps": ["Sample1", "Sample2", "Sample3"],
                    "data": [[10, 20, 30],
                             [35, 25, 15]]
                }
            }
        ),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["a", "b"],
            "smps": ["a", "b", "c"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }

    good_sample = {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {
            "Tissue": ["Kidney", "Lung", "Heart"],
            "Donor": ["D1", "D1", "D2"]
        },
        "z": {
            "Symbol": ["AAA", "BBB"],
            "Pathway": ["P1", "P2"]
        }
    }
    candidate = CXStandardProfile()

    with pytest.raises(CXDataProfileException):
        candidate.render_to_profiled_dict(None)

    with pytest.raises(CXDataProfileException):
        bad_sample = deepcopy(good_sample)
        bad_sample[Y][VARS] = 123
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(CXDataProfileException):
        bad_sample = deepcopy(good_sample)
        bad_sample[Y][SMPS] = 123
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(CXDataProfileException):
        bad_sample = deepcopy(good_sample)
        bad_sample[Y][DATA] = 123
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(TypeError):
        bad_sample = deepcopy(good_sample)
        bad_sample[X]['Tissue'] = 123
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(TypeError):
        bad_sample = deepcopy(good_sample)
        bad_sample[Z]['Pathway'] = 123
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(ValueError):
        bad_sample = deepcopy(good_sample)
        bad_sample[Z]['Pathway'] = ["P1"]
        candidate.match_z_to_vars = True
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(ValueError):
        bad_sample = deepcopy(good_sample)
        bad_sample[X]['Donor'] = ["D1", "D2"]
        candidate.match_x_to_smps = True
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(ValueError):
        bad_sample = deepcopy(good_sample)
        bad_sample[Y][VARS] = ["Variable1"]
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )

    with pytest.raises(ValueError):
        bad_sample = deepcopy(good_sample)
        bad_sample[Y][SMPS] = ["Sample1", "Sample2"]
        candidate.render_to_profiled_dict(
            CXDictData(bad_sample)
        )


def test_render_to_profiled_dict_matrix():
    candidate = CXStandardProfile()

    good_sample = DataFrame.from_dict(
        data={
            "Variable1": [10, 20, 30],
            "Variable2": [35, 25, 15]
        },
        orient="index",
        columns=["Sample1", "Sample2", "Sample3"]
    )
    result = candidate.render_to_profiled_dict(
        CXDataframeData(good_sample),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        Y: {
            "vars": ["Variable1", "Variable2"],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        X: {},
        Z: {}
    }

    good_sample = DataFrame.from_dict(
        data={
            "Sample1": [10, 35],
            "Sample2": [20, 25],
            "Sample3": [30, 15]
        },
        orient="columns"
    )
    result = candidate.render_to_profiled_dict(
        CXDataframeData(good_sample),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": [0, 1],
            "smps": ["Sample1", "Sample2", "Sample3"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }

    good_sample = DataFrame.from_dict(
        data={
            "Variable1": [10, 20, 30],
            "Variable2": [35, 25, 15]
        },
        orient="index"
    )
    result = candidate.render_to_profiled_dict(
        CXDataframeData(good_sample),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["Variable1", "Variable2"],
            "smps": [0, 1, 2],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }

    candidate.vars = ["a", "b"]
    candidate.smps = ["a", "b", "c"]
    good_sample = DataFrame.from_dict(
        data={
            "Variable1": [10, 20, 30],
            "Variable2": [35, 25, 15]
        },
        orient="index",
        columns=["Sample1", "Sample2", "Sample3"]
    )
    result = candidate.render_to_profiled_dict(
        CXDataframeData(good_sample),
        match_vars_to_rows=True,
        match_smps_to_cols=True,
        match_x_to_smps=True,
        match_z_to_vars=True
    )
    assert result == {
        "y": {
            "vars": ["a", "b"],
            "smps": ["a", "b", "c"],
            "data": [[10, 20, 30],
                     [35, 25, 15]]
        },
        "x": {},
        "z": {},
    }
