import json

import cxdash
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    cxdash.CXDashElement(
        id="test_cx_component",
        data=json.dumps(
            {
                "x": {
                    "Description": ["Survival time in days"]
                },
                "z": {
                    "Organ": ["Stomach", "Stomach", "Stomach", "Stomach", "Stomach", "Stomach", "Stomach", "Stomach",
                              "Stomach", "Stomach", "Stomach", "Stomach", "Stomach", "Bronchus", "Bronchus", "Bronchus",
                              "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus",
                              "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Bronchus", "Colon",
                              "Colon", "Colon", "Colon", "Colon", "Colon", "Colon", "Colon", "Colon", "Colon", "Colon",
                              "Colon", "Colon", "Colon", "Colon", "Colon", "Colon", "Ovary", "Ovary", "Ovary", "Ovary",
                              "Ovary", "Ovary", "Breast", "Breast", "Breast", "Breast", "Breast", "Breast", "Breast",
                              "Breast", "Breast", "Breast", "Breast"]
                },
                "y": {
                    "smps": ["Survival"],
                    "vars": ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15",
                             "s16", "s17", "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27", "s28",
                             "s29", "s30", "s31", "s32", "s33", "s34", "s35", "s36", "s37", "s38", "s39", "s40", "s41",
                             "s42", "s43", "s44", "s45", "s46", "s47", "s48", "s49", "s50", "s51", "s52", "s53", "s54",
                             "s55", "s56", "s57", "s58", "s59", "s60", "s61", "s62", "s63", "s64"],
                    "data": [
                        [124],
                        [42],
                        [25],
                        [45],
                        [412],
                        [51],
                        [1112],
                        [46],
                        [103],
                        [876],
                        [146],
                        [340],
                        [396],
                        [81],
                        [461],
                        [20],
                        [450],
                        [246],
                        [166],
                        [63],
                        [64],
                        [155],
                        [859],
                        [151],
                        [166],
                        [37],
                        [223],
                        [138],
                        [72],
                        [245],
                        [248],
                        [377],
                        [189],
                        [1843],
                        [180],
                        [537],
                        [519],
                        [455],
                        [406],
                        [365],
                        [942],
                        [776],
                        [372],
                        [163],
                        [101],
                        [20],
                        [283],
                        [1234],
                        [89],
                        [201],
                        [356],
                        [2970],
                        [456],
                        [1235],
                        [24],
                        [1581],
                        [1166],
                        [40],
                        [727],
                        [3808],
                        [791],
                        [1804],
                        [3460],
                        [719]
                    ],
                    "desc": ["days"]
                }
            }
        ),
        config=json.dumps(
            {
                "axisTitleFontStyle": "italic",
                "citation": "Cameron, E. and Pauling, L. (1978). Proceedings of the National Academy of Science USA, 75.",
                "colors": ["rgb(215,48,39)", "rgb(69,117,180)"],
                "decorationsBackgroundBorderLineType": False,
                "graphType": "Scatter2D",
                "histogramBins": 30,
                "histogramStackRatio": 1,
                "legendBackgroundBorderLineType": False,
                "legendKeyBackgroundBorderLineType": False,
                "subtitleBackgroundBorderLineType": False,
                "theme": "CanvasXpress",
                "title": "Patients with advanced cancers of the stomach,bronchus, colon, ovary or breast treated with ascorbate.",
                "titleBackgroundBorderLineType": False,
                "xAxis": ["Bin"],
                "xAxisExact": True,
                "xAxisTitle": "Survival (days)",
                "yAxis": ["Survival"],
                "yAxisTitle": "Number of Subjects"
            }
        ),
        after_render=json.dumps(
            [
                [
                    "createHistogram",
                    [False, None, None],
                ],
                [
                    "setDimensions",
                    [450, 600],
                ],
            ]
        ),
        # canvasxpress_version="35.9",
        width="609",
        height="609"
    ),
    html.Div(id='output')
])


if __name__ == '__main__':
    app.run_server(debug=True)
