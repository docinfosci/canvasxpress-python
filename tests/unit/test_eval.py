"""Unit tests for the model-evaluation plot builders (canvasxpress.eval)."""

import json

import pandas as pd

from canvasxpress.eval import (
    cx_roc,
    cx_pr,
    cx_confusion,
    cx_calibration,
    cx_learning_curve,
    cx_importance,
    cx_shap,
)


def _config(chart):
    return json.loads(str(chart.config))


def _data(chart):
    return json.loads(str(chart.data))


# Reference case: sklearn roc_auc_score([0,0,1,1],[0.1,0.4,0.35,0.8]) == 0.75
# and average_precision_score(...) == 0.8333.
_DF = pd.DataFrame({"truth": [0, 0, 1, 1], "score": [0.1, 0.4, 0.35, 0.8]})


def test_cx_roc_auc_and_axes():
    cfg = _config(cx_roc(_DF, "truth", "score", positive=1))
    assert cfg["graphType"] == "Scatter2D"
    assert cfg["scatterType"] == "line"
    assert "AUC = 0.750" in cfg["title"]
    data = _data(cx_roc(_DF, "truth", "score", positive=1))
    assert data["y"]["smps"] == ["FPR", "TPR"]
    assert data["y"]["data"][0] == [0, 0]
    assert data["y"]["data"][-1] == [1, 1]


def test_cx_pr_average_precision():
    cfg = _config(cx_pr(_DF, "truth", "score", positive=1))
    assert "AP = 0.833" in cfg["title"]
    assert _data(cx_pr(_DF, "truth", "score", positive=1))["y"]["smps"] == ["Recall", "Precision"]


def test_cx_confusion_counts():
    df = pd.DataFrame({"t": ["a", "a", "b", "b", "a"], "p": ["a", "b", "b", "b", "a"]})
    chart = cx_confusion(df, "t", "p")
    cfg, data = _config(chart), _data(chart)
    assert cfg["graphType"] == "Heatmap"
    assert data["y"]["vars"] == ["Actual a", "Actual b"]
    assert data["y"]["data"] == [[2, 1], [0, 2]]
    assert len(cfg["heatmapCellText"]) == 4


def test_cx_calibration_bins_and_diagonal():
    p = [i / 100 for i in range(100)]
    y = [1 if (i * 7 % 10) / 10 < pp else 0 for i, pp in enumerate(p)]
    chart = cx_calibration(pd.DataFrame({"t": y, "p": p}), "t", "p", positive=1, bins=5)
    cfg, data = _config(chart), _data(chart)
    assert cfg["graphType"] == "Scatter2D"
    assert "ECE =" in cfg["title"]
    assert data["y"]["smps"] == ["Predicted", "Observed"]
    assert len(cfg["decorations"]["line"]) == 1


def test_cx_learning_curve_two_series():
    df = pd.DataFrame({"s": [10, 50, 100], "tr": [0.7, 0.85, 0.9], "va": [0.6, 0.75, 0.82]})
    data = _data(cx_learning_curve(df, "s", "tr", "va"))
    assert data["y"]["vars"] == ["Training score", "Validation score"]
    assert data["y"]["smps"] == ["10", "50", "100"]


def test_cx_importance_sorted_and_horizontal():
    df = pd.DataFrame({"f": ["age", "bmi", "bp", "sex"], "i": [0.1, 0.5, 0.3, 0.05]})
    chart = cx_importance(df, "f", "i", top=3)
    cfg, data = _config(chart), _data(chart)
    assert cfg["graphOrientation"] == "horizontal"
    assert data["y"]["smps"] == ["bmi", "bp", "age"]
    assert data["y"]["data"][0] == [0.5, 0.3, 0.1]


def test_cx_shap_beeswarm():
    shap = pd.DataFrame([[0.2, -0.1, 0.05], [-0.3, 0.4, -0.02], [0.1, 0.2, 0.15]],
                        columns=["age", "bmi", "bp"])
    vals = pd.DataFrame([[55, 22, 120], [40, 30, 110], [60, 25, 130]],
                        columns=["age", "bmi", "bp"])
    chart = cx_shap(shap, vals)
    cfg, data = _config(chart), _data(chart)
    assert cfg["graphType"] == "Dotplot"
    assert cfg["groupingFactors"] == ["Feature"]
    assert cfg["colorBy"] == "Feature value"
    assert len(data["y"]["data"][0]) == 9  # 3 samples x 3 features
    assert set(["Feature", "Feature value"]).issubset(data["x"].keys())
