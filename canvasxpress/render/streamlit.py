import copy
import hashlib
from itertools import count
from typing import Optional

from canvasxpress.canvas import CanvasXpress

try:
    # Custom Components v2 (CCv2): renders in the app's DOM rather than an iframe.
    from streamlit.components.v2 import component as _component_v2

except ImportError:
    # Older Streamlit releases, such as those available for Python 3.8.
    _component_v2 = None

_cx_iframe_padding = 50

_cx_fx_template = """
<script type="text/javascript">
    @code@
</script>
"""

_cx_html_template = """
<html>
    <head>
        <meta charset="UTF-8">
        <title>CanvasXpress</title>

        <!-- 1. Include the CanvasXpress library -->
        @canvasxpress_license@
        <link
                href='@css_url@'
                rel='stylesheet'
                type='text/css'
                referrerpolicy='origin-when-cross-origin'
        />
        <script
                src='@js_url@'
                type='text/javascript'>
                referrerpolicy='origin-when-cross-origin'
        </script>
    </head>
    <body>
        <!-- 3. DOM element where the visualization will be displayed -->
        @canvases@
        <!-- 2. Include script to initialize object -->
        @js_functions@
     </body>
</html>
"""

_cx_component_html = """
<div class="canvasxpress-streamlit"></div>
"""

_cx_component_js = """
// Library loads are shared by every chart on the page, keyed by URL.
const libraryLoads = new Map();

// Per-instance state, keyed by the component's parent element.
const instances = new WeakMap();

// Suffix counter for charts whose ID is already in use on the page.
let duplicateCount = 0;

function loadScript(url) {
  if (!libraryLoads.has(url)) {
    libraryLoads.set(url, new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = url;
      script.type = "text/javascript";
      script.referrerPolicy = "origin-when-cross-origin";
      script.onload = () => resolve();
      script.onerror = () => {
        libraryLoads.delete(url);
        reject(new Error("Unable to load " + url));
      };
      document.head.appendChild(script);
    }));
  }
  return libraryLoads.get(url);
}

function loadStylesheet(url) {
  const links = document.head.querySelectorAll("link[rel='stylesheet']");
  for (const link of links) {
    if (link.getAttribute("href") === url) {
      return;
    }
  }
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.type = "text/css";
  link.href = url;
  link.referrerPolicy = "origin-when-cross-origin";
  document.head.appendChild(link);
}

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

export default function (component) {
  const { data, parentElement } = component;
  const root = parentElement.querySelector(".canvasxpress-streamlit");
  if (!root || !data) {
    return;
  }

  // Each run replaces the previous chart for this instance.
  const instance = instances.get(parentElement) || { run: 0, targetId: null };
  instance.run += 1;
  const run = instance.run;
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
  loadStylesheet(data.css_url);

  const license = data.license_url ? loadScript(data.license_url) : Promise.resolve();
  license
    .then(() => loadScript(data.js_url))
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
      },
      (error) => {
        console.error(error);
        root.textContent = "CanvasXpress could not be loaded: " + error.message;
      }
    );

  return () => {
    destroyChart(instance.targetId);
    instances.delete(parentElement);
  };
}
"""

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


def _get_chart_display_code(cx: CanvasXpress) -> tuple:
    """
    Get the html display code and iframe dimensions for rendering a CanvasXpress
    object in a Streamlit application that predates Custom Components v2.

    Args:
        cx: The CanvasXpress object to be rendered.

    Returns:
        A tuple of (html, iframe_width, iframe_height) containing the HTML string,
        the iframe width in pixels, and the iframe height in pixels.
    """
    html_parts = cx.render_to_html_parts()
    canvases = html_parts["cx_canvas"]
    js_functions = _cx_fx_template.replace("@code@", html_parts["cx_js"])

    cx_license = ""
    if html_parts.get("cx_license"):
        cx_license = html_parts["cx_license"]

    css_url = CanvasXpress.css_library_url()
    js_url = CanvasXpress.js_library_url()

    html = (
        _cx_html_template.replace("@canvases@", canvases)
        .replace("@canvasxpress_license@", cx_license)
        .replace("@js_functions@", js_functions)
        .replace("@css_url@", css_url)
        .replace("@js_url@", js_url)
    )

    iframe_width = cx.width + _cx_iframe_padding
    iframe_height = cx.height + _cx_iframe_padding

    return html, iframe_width, iframe_height


def _get_chart_component_data(cx: CanvasXpress) -> dict:
    """
    Get the data passed to the Custom Components v2 CanvasXpress component.

    Args:
        cx: The CanvasXpress object to be rendered.

    Returns:
        A dict with the chart's target ID, the placeholder ID used in the canvas
        element HTML and initialization JavaScript, and the CanvasXpress library,
        stylesheet and license URLs.
    """
    # Captured once because anonymous charts generate a new ID on each access.
    target_id = cx.render_to

    # Render with a placeholder ID that the browser replaces with the target ID,
    # or with a unique variant if another chart on the page already uses it.
    # IDs are limited to alphanumerics and "_", so the placeholder is exact.
    placeholder_id = "cXplaceholder" + hashlib.sha1(target_id.encode()).hexdigest()
    rendered = copy.copy(cx)
    rendered.render_to = placeholder_id
    html_parts = rendered.render_to_html_parts()

    return {
        "target_id": target_id,
        "placeholder_id": placeholder_id,
        "canvas": html_parts["cx_canvas"],
        "js": html_parts["cx_js"],
        "js_url": CanvasXpress.js_library_url(),
        "css_url": CanvasXpress.css_library_url(),
        "license_url": cx.license_url if cx.license_available else None,
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
    if key is not None:
        _cx_component(data=data, key=key, width="content")
        return

    from streamlit.errors import (
        StreamlitDuplicateElementId,
        StreamlitDuplicateElementKey,
    )

    try:
        _cx_component(data=data, width="content")
        return

    except StreamlitDuplicateElementId:
        pass

    for occurrence in count(2):
        try:
            _cx_component(
                data=data,
                key=f"canvasxpress_{data['target_id']}_{occurrence}",
                width="content",
            )
            return

        except StreamlitDuplicateElementKey:
            continue


def plot(cx: CanvasXpress, key: Optional[str] = None) -> None:
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

    Raises:
        TypeError: If cx is not a CanvasXpress object.
    """

    if cx is None:
        return None

    elif not isinstance(cx, CanvasXpress):
        raise TypeError("Argument 'cx' is not a CanvasXpress object")

    if _cx_component is not None:
        _mount_chart_component(_get_chart_component_data(cx), key)

    else:
        import streamlit.components.v1 as components

        html, iframe_width, iframe_height = _get_chart_display_code(cx)
        components.html(html, width=iframe_width, height=iframe_height)
