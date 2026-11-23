"""
The minimal Streamlit app captured by test_platform_streamlit.py: one chart at
its configured size, and one that fills the width of the page.
"""

import streamlit as st

from canvasxpress.plot import graph
from tests.functional.platform.charts import fill_chart, fixed_chart

st.set_page_config(page_title="CanvasXpress platform test", layout="wide")

st.header("CanvasXpress in Streamlit")

graph(fixed_chart())
graph(fill_chart(), fill_to_width=True)
