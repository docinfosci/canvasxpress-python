"""
The Streamlit columns app captured by test_platform_streamlit.py: two charts
side by side in `st.columns`, each filling the width of its column.
"""

import streamlit as st

from canvasxpress.plot import graph
from tests.functional.platform.charts import left_chart, right_chart

st.set_page_config(page_title="CanvasXpress platform test", layout="wide")

st.header("CanvasXpress in Streamlit columns")

left, right = st.columns(2)
with left:
    graph(left_chart(), fill_to_width=True)
with right:
    graph(right_chart(), fill_to_width=True)
