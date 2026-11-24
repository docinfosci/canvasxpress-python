"""Model-evaluation plot builders for canvasxpress.

Thin, data-frame-first wrappers that turn a classifier's outputs (truth labels,
scores, predictions, importances or SHAP values) into CanvasXpress charts,
mirroring the JavaScript engine's ``CanvasXpress.rocConfig`` / ``prConfig`` /
``confusionConfig`` / ``calibrationConfig`` / ``learningCurveConfig`` /
``importanceConfig`` / ``shapConfig`` builders (engine >= 73.9) and the R
``cx_roc`` / ``cx_pr`` / ``cx_confusion`` / ``cx_calibration`` /
``cx_learning_curve`` / ``cx_importance`` / ``cx_shap`` functions.

The ROC/PR sweep, AUC, average precision, calibration bins/ECE, confusion counts
and mean absolute SHAP are all computed here in pure Python (no numpy/sklearn
dependency), so the charts render the same as the JS and R paths. Each builder
returns a :class:`~canvasxpress.canvas.CanvasXpress` object.

Example
-------
>>> import pandas as pd
>>> from canvasxpress.eval import cx_roc, cx_confusion
>>> df = pd.DataFrame({"truth": [0, 0, 1, 1], "score": [0.1, 0.4, 0.35, 0.8]})
>>> chart = cx_roc(df, "truth", "score")          # ROC curve, AUC in the title
>>> cm = cx_confusion(df.assign(pred=[0, 1, 1, 1]), "truth", "pred")

Suggested placement: ``canvasxpress/eval.py``, re-exported from
``canvasxpress/__init__.py`` (see the accompanying PR note).
"""

from canvasxpress.canvas import CanvasXpress

__all__ = [
    "cx_roc",
    "cx_pr",
    "cx_confusion",
    "cx_calibration",
    "cx_learning_curve",
    "cx_importance",
    "cx_shap",
]


def _positive_label(truth, positive=None):
    """Pick the positive class: an explicit value, else a truthy token, else the max."""
    if positive is not None:
        return positive
    seen = list(dict.fromkeys(truth))
    for p in (1, "1", True, "true", "yes", "positive", "pos", "Y"):
        for s in seen:
            if s == p:
                return s
    return sorted(seen)[-1] if seen else 1


def _sweep(truth, score, positive):
    """Distinct-threshold sweep (ties collapsed). Returns (tp, fp, P, N) or None."""
    rows = sorted(
        zip((float(s) for s in score), (t == positive for t in truth)),
        key=lambda r: r[0],
        reverse=True,
    )
    total_pos = sum(1 for _, p in rows if p)
    total_neg = len(rows) - total_pos
    if total_pos == 0 or total_neg == 0:
        return None
    tps, fps = [0], [0]
    tp = fp = 0
    i, n = 0, len(rows)
    while i < n:
        at = rows[i][0]
        while i < n and rows[i][0] == at:
            if rows[i][1]:
                tp += 1
            else:
                fp += 1
            i += 1
        tps.append(tp)
        fps.append(fp)
    return tps, fps, total_pos, total_neg


def _curve(render_to, x_name, y_name, ids, matrix, title, x_title, y_title, decoration, extra):
    data = {"y": {"vars": ids, "smps": [x_name, y_name], "data": matrix}}
    config = {
        "graphType": "Scatter2D",
        "scatterType": "line",
        "xAxis": [x_name],
        "yAxis": [y_name],
        "setMinX": 0, "setMaxX": 1,
        "setMinY": 0, "setMaxY": 1,
        "xAxisTitle": x_title,
        "yAxisTitle": y_title,
        "title": title,
        "showLoessFit": False,
        "showTransition": False,
        "decorations": {"line": [decoration]},
    }
    config.update(extra or {})
    return CanvasXpress(render_to=render_to, data=data, config=config)


def cx_roc(data, truth, score, positive=None, title=None, render_to=None, **config):
    """ROC curve from a DataFrame's truth and score columns (returns CanvasXpress)."""
    y_true = list(data[truth])
    y_score = list(data[score])
    positive = _positive_label(y_true, positive)
    swept = _sweep(y_true, y_score, positive)
    if swept is None:
        raise ValueError("cx_roc: truth must contain both classes")
    tps, fps, P, N = swept
    ids, matrix, auc = [], [], 0.0
    prev_fpr = prev_tpr = 0.0
    for i in range(len(tps)):
        fpr, tpr = fps[i] / N, tps[i] / P
        ids.append("t%d" % i)
        matrix.append([fpr, tpr])
        auc += (fpr - prev_fpr) * (tpr + prev_tpr) / 2
        prev_fpr, prev_tpr = fpr, tpr
    title = title or ("ROC curve (AUC = %.3f)" % auc)
    deco = {"x": 0, "y": 0, "x2": 1, "y2": 1, "color": "#999999",
            "width": 1, "type": "dashed", "label": "Chance"}
    return _curve(render_to, "FPR", "TPR", ids, matrix, title,
                  "False positive rate", "True positive rate", deco, config)


def cx_pr(data, truth, score, positive=None, title=None, render_to=None, **config):
    """Precision-recall curve from a DataFrame's truth and score columns."""
    y_true = list(data[truth])
    y_score = list(data[score])
    positive = _positive_label(y_true, positive)
    swept = _sweep(y_true, y_score, positive)
    if swept is None:
        raise ValueError("cx_pr: truth must contain both classes")
    tps, fps, P, N = swept
    ids, matrix, ap = ["t0"], [[0, 1]], 0.0
    prev_recall = 0.0
    for i in range(1, len(tps)):
        tp, fp = tps[i], fps[i]
        recall = tp / P
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        ids.append("t%d" % i)
        matrix.append([recall, precision])
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    title = title or ("Precision-Recall (AP = %.3f)" % ap)
    baseline = P / (P + N)
    deco = {"x": 0, "y": baseline, "x2": 1, "y2": baseline, "color": "#999999",
            "width": 1, "type": "dashed", "label": "No skill"}
    return _curve(render_to, "Recall", "Precision", ids, matrix, title,
                  "Recall", "Precision", deco, config)


def cx_confusion(data, truth, pred, labels=None, title=None, render_to=None, **config):
    """Confusion-matrix heatmap from a DataFrame's truth and prediction columns."""
    y_true = list(data[truth])
    y_pred = list(data[pred])
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred), key=lambda v: str(v))
    index = {str(v): i for i, v in enumerate(labels)}
    matrix = [[0] * len(labels) for _ in labels]
    for t, p in zip(y_true, y_pred):
        ri, ci = index.get(str(t)), index.get(str(p))
        if ri is not None and ci is not None:
            matrix[ri][ci] += 1
    row_names = ["Actual %s" % v for v in labels]
    col_names = ["Pred %s" % v for v in labels]
    cell_text = [{"variable": row_names[r], "sample": col_names[c], "text": str(matrix[r][c])}
                 for r in range(len(labels)) for c in range(len(labels))]
    cfg = {
        "graphType": "Heatmap",
        "title": title or "Confusion matrix",
        "varTitle": "Actual",
        "smpTitle": "Predicted",
        "heatmapCellBox": True,
        "heatmapCellText": cell_text,
        "showTransition": False,
    }
    cfg.update(config)
    data_obj = {"y": {"vars": row_names, "smps": col_names, "data": matrix}}
    return CanvasXpress(render_to=render_to, data=data_obj, config=cfg)


def cx_calibration(data, truth, prob, positive=None, bins=10, title=None, render_to=None, **config):
    """Calibration (reliability) curve from a DataFrame's truth and probability columns."""
    y_true = list(data[truth])
    y_prob = [float(p) for p in data[prob]]
    positive = _positive_label(y_true, positive)
    sum_prob = [0.0] * bins
    pos = [0] * bins
    cnt = [0] * bins
    for t, p in zip(y_true, y_prob):
        idx = min(bins - 1, max(0, int(p * bins)))
        sum_prob[idx] += p
        cnt[idx] += 1
        if t == positive:
            pos[idx] += 1
    ids, matrix, ece, n = [], [], 0.0, len(y_prob)
    for k in range(bins):
        if cnt[k] == 0:
            continue
        mp, of = sum_prob[k] / cnt[k], pos[k] / cnt[k]
        ids.append("b%d" % k)
        matrix.append([mp, of])
        ece += (cnt[k] / n) * abs(mp - of)
    title = title or ("Calibration (ECE = %.3f)" % ece)
    deco = {"x": 0, "y": 0, "x2": 1, "y2": 1, "color": "#999999",
            "width": 1, "type": "dashed", "label": "Perfect"}
    return _curve(render_to, "Predicted", "Observed", ids, matrix, title,
                  "Mean predicted probability", "Observed frequency", deco, config)


def cx_learning_curve(data, size, train, val, title=None, render_to=None, **config):
    """Learning curve (training vs validation score over set size) from a DataFrame."""
    sizes = [str(s) for s in data[size]]
    train_row = [float(v) for v in data[train]]
    val_row = [float(v) for v in data[val]]
    cfg = {"graphType": "Line", "smpTitle": "Training set size", "yAxisTitle": "Score",
           "showLegend": True, "showTransition": False, "title": title or "Learning curve"}
    cfg.update(config)
    data_obj = {"y": {"vars": ["Training score", "Validation score"],
                      "smps": sizes, "data": [train_row, val_row]}}
    return CanvasXpress(render_to=render_to, data=data_obj, config=cfg)


def cx_importance(data, feature, importance, top=None, title=None, render_to=None, **config):
    """Horizontal feature-importance bar chart from a DataFrame (returns CanvasXpress)."""
    pairs = sorted(zip((str(f) for f in data[feature]), (float(v) for v in data[importance])),
                   key=lambda r: r[1], reverse=True)
    if top:
        pairs = pairs[:top]
    names = [p[0] for p in pairs]
    row = [p[1] for p in pairs]
    cfg = {"graphType": "Bar", "graphOrientation": "horizontal", "smpTitle": "Feature",
           "xAxisTitle": "Importance", "showLegend": False, "showTransition": False,
           "title": title or "Feature importance"}
    cfg.update(config)
    return CanvasXpress(render_to=render_to,
                        data={"y": {"vars": ["Importance"], "smps": names, "data": [row]}},
                        config=cfg)


def cx_shap(shap, values, features=None, top=None, title=None, render_to=None, **config):
    """SHAP summary beeswarm from samples x features SHAP and feature-value matrices.

    ``shap`` and ``values`` may be pandas DataFrames or 2-D lists; feature names
    default to the DataFrame columns. Features are ordered by descending mean
    absolute SHAP value.
    """
    shap_rows = shap.values.tolist() if hasattr(shap, "values") else [list(r) for r in shap]
    value_rows = values.values.tolist() if hasattr(values, "values") else [list(r) for r in values]
    if features is None:
        features = list(shap.columns) if hasattr(shap, "columns") else \
            ["f%d" % i for i in range(len(shap_rows[0]))]
    n = len(shap_rows)
    n_features = len(features)
    mean_abs = [sum(abs(float(shap_rows[s][f])) for s in range(n)) / (n or 1)
                for f in range(n_features)]
    order = sorted(range(n_features), key=lambda f: mean_abs[f], reverse=True)
    if top:
        order = order[:top]
    ids, shap_row, feature_col, value_col = [], [], [], []
    for f in order:
        for s in range(n):
            ids.append("p%d_%d" % (f, s))
            shap_row.append(float(shap_rows[s][f]))
            feature_col.append(str(features[f]))
            value_col.append(float(value_rows[s][f]))
    cfg = {"graphType": "Dotplot", "graphOrientation": "horizontal", "xAxis": ["SHAP value"],
           "groupingFactors": ["Feature"], "colorBy": "Feature value",
           "colorSpectrum": config.pop("colorSpectrum", ["#2166ac", "#f7f7f7", "#b2182b"]),
           "jitter": True, "xAxisTitle": "SHAP value (impact on model output)",
           "showLegend": True, "showTransition": False, "title": title or "SHAP summary"}
    cfg.update(config)
    data_obj = {"y": {"vars": ["SHAP value"], "smps": ids, "data": [shap_row]},
                "x": {"Feature": feature_col, "Feature value": value_col}}
    return CanvasXpress(render_to=render_to, data=data_obj, config=cfg)
