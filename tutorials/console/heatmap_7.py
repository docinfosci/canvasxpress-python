from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.popup import CXBrowserPopup

import pandas as pd

# Each file is a tab-delimited matrix with columns and an index, and we can
# use pandas to read each at their URL to create dataframes

y_data_url = "https://www.canvasxpress.org/data/cX-heatmapR-dat.txt"
y_data = pd.read_csv(y_data_url, sep='\t', index_col=0)

x_data_url = "https://www.canvasxpress.org/data/cX-heatmapR-smp.txt"
x_data = pd.read_csv(x_data_url, sep='\t', index_col=0)

z_data_url = "https://www.canvasxpress.org/data/cX-heatmapR-var.txt"
z_data = pd.read_csv(z_data_url, sep='\t', index_col=0)

# The dict structure is an easy way to shape and submit data to CanvasXpress
hm_data = {
    # Data
    "y": {
        # Samples, which can be considered the columns
        "smps": y_data.columns.to_list(),
        # Variables, which can be considered the index
        "vars": y_data.index.tolist(),
        # The data itself, split into rows per variable and ordered by samples
        "data": y_data.values.tolist(),
    },
    # Sample annotations
    "x": {col: x_data[col].to_list() for col in x_data.columns.to_list()},
    # Variable annotations
    "z": {col: z_data[col].to_list() for col in z_data.columns.to_list()}
}

if __name__ == "__main__":

    chart = CanvasXpress(
        # Data can be structured many ways, and here we use a dict
        data=hm_data,

        # Configuration options are key-value pairs of formatting instructions
        config={
            "graphType": "Heatmap",
            "title": "Overlays in Heatmap",
            "colorSmpDendrogramBy": "Treatment",
            "colorSpectrum": ["magenta", "blue", "black", "red", "gold"],
            "colorSpectrumZeroValue": 0,
            "heatmapIndicatorHeight": 50,
            "heatmapIndicatorHistogram": True,
            "heatmapIndicatorPosition": "topLeft",
            "heatmapIndicatorWidth": 60,
            "heatmapSmpSeparateBy": "Treatment",
            "samplesClustered": True,
            "smpOverlays": ["Treatment", "Site"],
            "variablesClustered": True
        },

        # The effect depends on the renderer, and for browser popups these set
        # the canvas element width and height
        width=675,
        height=600
    )

    browser = CXBrowserPopup(chart)
    browser.render()
