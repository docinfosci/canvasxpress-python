from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.popup import CXBrowserPopup

import pandas as pd

# Each file is a tab-delimited matrix with columns and an index, and we can
# use pandas to read each at their URL to create dataframes

y_data_url = "https://www.canvasxpress.org/data/cX-scatterR2-dat.txt"
y_data = pd.read_csv(y_data_url, sep="\t", index_col=0)

z_data_url = "https://www.canvasxpress.org/data/cX-scatterR2-var.txt"
z_data = pd.read_csv(z_data_url, sep="\t", index_col=0)

# The dict structure is an easy way to shape and submit data to CanvasXpress
volcano_data = {
    # Data
    "y": {
        # Samples, which can be considered the columns
        "smps": y_data.columns.to_list(),
        # Variables, which can be considered the index
        "vars": y_data.index.tolist(),
        # The data itself, split into rows per variable and ordered by samples
        "data": y_data.values.tolist(),
    },
    # Variable annotations
    "z": {col: z_data[col].to_list() for col in z_data.columns.to_list()},
}

chart = CanvasXpress(
    data=volcano_data,
    config={
        "graphType": "Scatter2D",
        "title": "Volcano plot",
        "axisAlgorithm": "rPretty",
        "backgroundType": "window",
        "backgroundWindow": "rgb(238,238,238)",
        "colorBy": "Group",
        "colors": ["rgba(0,104,139,0.5)", "rgba(205,0,0,0.5)", "rgba(64,64,64,0.5)"],
        "decorations": {
            "line": [
                {"color": "rgba(205,0,0,0.5)", "width": 2, "x": 0.5},
                {"x": -0.5, "width": 2, "color": "rgba(0,104,139,0.5)"},
            ]
        },
        "legendBackgroundColor": "rgb(238,238,238)",
        "legendBox": True,
        "legendBoxColor": "rgb(0,0,0)",
        "plotBox": False,
        "showDecorations": True,
        "showTransition": False,
        "sizeBy": "FC",
        "sizes": [4, 14, 16, 18],
        "theme": "CanvasXpress",
        "xAxis": ["logFC"],
        "xAxisTickColor": "rgb(255,255,255)",
        "yAxis": ["-log-pVal"],
        "yAxisTickColor": "rgb(255,255,255)",
    },
    width=613,
    height=613,
)

browser = CXBrowserPopup(chart)
browser.render()
