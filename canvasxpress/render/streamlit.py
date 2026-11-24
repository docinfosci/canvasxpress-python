import hashlib
from itertools import count
from typing import Optional

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context import (
    FILL_JS,
    LOADER_JS,
    CXChartAssets,
    CXHtmlDocument,
)

try:
    # Custom Components v2 (CCv2): renders in the app's DOM rather than an iframe.
    from streamlit.components.v2 import component as _component_v2

except ImportError:
    # Older Streamlit releases, such as those available for Python 3.8.
    _component_v2 = None

_cx_iframe_padding = 50

_cx_component_html = """
<div class="canvasxpress-streamlit"></div>
"""

# The shared loader defines window.canvasxpress.loadLibrary(), which loads the
# CanvasXpress library once for every chart on the page, and the fill script
# defines window.canvasxpress.fillContainer() for the fill_to_width and
# fill_to_height options.
_cx_component_js = (
    LOADER_JS
    + FILL_JS
    + """
// Per-instance state, keyed by the component's parent element.
const instances = new WeakMap();

// Suffix counter for charts whose ID is already in use on the page.
let duplicateCount = 0;

function destroyChart(targetId) {
  if (!targetId || !window.CanvasXpress) {
    return;
  }
  try {
    const chart = window.CanvasXpress.getObject(targetId);
    if (chart) {
      chart.destroy();
    }
  } catch (error) {
    console.error("Chart " + targetId + " could not be destroyed:", error);
  }
}

function stopFilling(instance) {
  if (instance.stopFill) {
    instance.stopFill();
    instance.stopFill = null;
  }
}

export default function (component) {
  const { data, parentElement } = component;
  const root = parentElement.querySelector(".canvasxpress-streamlit");
  if (!root || !data) {
    return;
  }

  // Each run replaces the previous chart for this instance.
  const instance = instances.get(parentElement) || {
    run: 0,
    targetId: null,
    stopFill: null,
  };
  instance.run += 1;
  const run = instance.run;
  stopFilling(instance);
  destroyChart(instance.targetId);

  // Charts share the page's DOM, so give a chart a unique ID if another chart
  // already uses its render_to ID, as separate iframes once did implicitly.
  let targetId = data.target_id;
  const existing = document.getElementById(targetId);
  if (existing && !root.contains(existing)) {
    duplicateCount += 1;
    targetId = targetId + "_" + duplicateCount;
  }
  instance.targetId = targetId;
  instances.set(parentElement, instance);
  const chartJs = data.js.split(data.placeholder_id).join(targetId);

  root.innerHTML = data.canvas.split(data.placeholder_id).join(targetId);

  window.canvasxpress
    .loadLibrary({
      jsUrl: data.js_url,
      cssUrl: data.css_url,
      licenseUrl: data.license_url,
    })
    .then(
      () => {
        // Skip if a newer run has replaced this chart while the library loaded.
        if (instance.run !== run) {
          return;
        }
        // As with a script tag, a chart script error is logged and leaves the
        // chart's DOM in place for CanvasXpress.
        try {
          new Function(chartJs)();
        } catch (error) {
          console.error("CanvasXpress chart " + targetId + " failed:", error);
        }
        if (data.fill_to_width || data.fill_to_height) {
          if (data.fill_to_height && parentElement.style) {
            // Passes the height Streamlit gives the element on to the chart.
            parentElement.style.height = "100%";
          }
          instance.stopFill = window.canvasxpress.fillContainer(root, targetId, {
            fillToWidth: data.fill_to_width,
            fillToHeight: data.fill_to_height,
            width: data.width,
            height: data.height,
          });
        }
      },
      (error) => {
        console.error(error);
        root.textContent = "CanvasXpress could not be loaded: " + error.message;
      }
    );

  return () => {
    stopFilling(instance);
    destroyChart(instance.targetId);
    instances.delete(parentElement);
  };
}
"""
)

# Declared once at import so that Streamlit registers the component a single time.
_cx_component = (
    _component_v2(
        "canvasxpress_chart",
        html=_cx_component_html,
        js=_cx_component_js,
        # CanvasXpress locates its canvas by document ID and attaches menus and
        # tooltips to the document body, so it must render in the app's DOM.
        isolate_styles=False,
    )
    if _component_v2 is not None
    else None
)


def _get_chart_display_code(cx: CanvasXpress, fill_to_width: bool = False) -> tuple:
    """
    Get the html display code and iframe dimensions for rendering a CanvasXpress
    object in a Streamlit application that predates Custom Components v2.

    An iframe is given a fixed height, so there is no container height for the
    chart to fill; it is drawn at its configured height.

    Args:
        cx: The CanvasXpress object to be rendered.
        fill_to_width: Whether the chart follows the width of the iframe, which
            then takes the width of its Streamlit container.

    Returns:
        A tuple of (html, iframe_width, iframe_height) containing the HTML string,
        the iframe width in pixels or None for the container width, and the
        iframe height in pixels.
    """
    document = CXHtmlDocument(cx, fill_to_width=fill_to_width)
    width, height = document.size

    return (
        document.page(),
        None if fill_to_width else width + _cx_iframe_padding,
        height + _cx_iframe_padding,
    )


def _get_chart_component_data(
    cx: CanvasXpress,
    fill_to_width: bool = False,
    fill_to_height: bool = False,
) -> dict:
    """
    Get the data passed to the Custom Components v2 CanvasXpress component.

    Args:
        cx: The CanvasXpress object to be rendered.
        fill_to_width: Whether the chart follows the width of its Streamlit
            container.
        fill_to_height: Whether the chart follows the height of its Streamlit
            container.

    Returns:
        A dict with the chart's target ID, the placeholder ID used in the canvas
        element HTML and initialization JavaScript, the CanvasXpress library,
        stylesheet and license URLs, the chart's configured width and height,
        and which of them follow the container.
    """
    # Captured once because anonymous charts generate a new ID on each access.
    target_id = cx.render_to

    # Render with a placeholder ID that the browser replaces with the target ID,
    # or with a unique variant if another chart on the page already uses it.
    # IDs are limited to alphanumerics and "_", so the placeholder is exact.
    placeholder_id = "cXplaceholder" + hashlib.sha1(target_id.encode()).hexdigest()
    chart = CXChartAssets.from_canvas(cx, target_id=placeholder_id)

    return {
        "target_id": target_id,
        "placeholder_id": placeholder_id,
        "canvas": chart.canvas,
        "js": chart.js,
        "js_url": CanvasXpress.js_library_url(),
        "css_url": CanvasXpress.css_library_url(),
        "license_url": chart.license_url,
        "width": chart.width,
        "height": chart.height,
        "fill_to_width": bool(fill_to_width),
        "fill_to_height": bool(fill_to_height),
    }


def _mount_chart_component(data: dict, key: Optional[str]) -> None:
    """
    Mounts the Custom Components v2 CanvasXpress component.

    Without a key, Streamlit identifies an element by its parameters, so mounting
    the same chart twice in one run raises a duplicate element error. Iframe
    rendering allowed that, so such repeats are given generated keys instead.

    Args:
        data: The component data from `_get_chart_component_data`.
        key: The caller's Streamlit element key, or None.
    """
    # A chart that fills a dimension needs the container's full extent in it;
    # otherwise the element is sized to the chart.
    size = {
        "width": "stretch" if data.get("fill_to_width") else "content",
        "height": "stretch" if data.get("fill_to_height") else "content",
    }

    if key is not None:
        _cx_component(data=data, key=key, **size)
        return

    from streamlit.errors import (
        StreamlitDuplicateElementId,
        StreamlitDuplicateElementKey,
    )

    try:
        _cx_component(data=data, **size)
        return

    except StreamlitDuplicateElementId:
        pass

    for occurrence in count(2):
        try:
            _cx_component(
                data=data,
                key=f"canvasxpress_{data['target_id']}_{occurrence}",
                **size,
            )
            return

        except StreamlitDuplicateElementKey:
            continue


def plot(
    cx: CanvasXpress,
    key: Optional[str] = None,
    fill_to_width: bool = False,
    fill_to_height: bool = False,
) -> None:
    """
    Renders the provided CanvasXpress object for display in a Streamlit application.

    With Streamlit releases that provide Custom Components v2 the chart renders
    directly in the app, so charts share one copy of the CanvasXpress library and
    can broadcast to each other. Older releases render each chart in an iframe.

    Args:
        cx: The CanvasXpress object to be rendered.
        key: An optional Streamlit element key that keeps the chart's identity
            stable across reruns. Ignored by Streamlit releases that predate
            Custom Components v2.
        fill_to_width: True to have the chart take the full width of its
            Streamlit container, such as the page or a column, and follow it as
            it changes, rather than keeping its configured width. Default is
            False.
        fill_to_height: True to have the chart take the full height of its
            Streamlit container and follow it as it changes, rather than keeping
            its configured height. This needs a container with a height, such
            as `st.container(height=500)`; most Streamlit containers take their
            height from their content, and there the chart keeps its configured
            height. Ignored by Streamlit releases that predate Custom Components
            v2, whose iframes have a fixed height. Default is False.

    Raises:
        TypeError: If cx is not a CanvasXpress object.
    """

    if cx is None:
        return None

    elif not isinstance(cx, CanvasXpress):
        raise TypeError("Argument 'cx' is not a CanvasXpress object")

    if _cx_component is not None:
        _mount_chart_component(
            _get_chart_component_data(cx, fill_to_width, fill_to_height), key
        )

    else:
        import streamlit.components.v1 as components

        html, iframe_width, iframe_height = _get_chart_display_code(cx, fill_to_width)
        components.html(html, width=iframe_width, height=iframe_height)
