/*
 * CanvasXpress for Plotly Dash
 *
 * The CXDashElement Dash component, shipped with the canvasxpress Python
 * package (see canvasxpress/render/dash.py). It adapts the component's string
 * properties to window.canvasxpress.CanvasXpressReact, which must be loaded
 * first.
 *
 * Exposed as window.canvasxpress.CXDashElement, the Dash namespace and type
 * declared by the Python component.
 */
(function (root) {
  "use strict";

  var React = root.React;
  var e = React.createElement;
  var CanvasXpressReact = root.canvasxpress.CanvasXpressReact;

  // JSON when possible; otherwise the raw value, e.g. raw (non-JSON) data.
  function parseJson(value) {
    if (value === undefined || value === null || value === "") {
      return undefined;
    }
    try {
      return JSON.parse(value);
    } catch (error) {
      return value;
    }
  }

  // Events are a JavaScript object literal, as rendered by CXEvents.
  function parseEvents(value) {
    if (!value) {
      return undefined;
    }
    try {
      return new Function("return (" + value + ");")() || undefined;
    } catch (error) {
      console.error("CanvasXpress events could not be parsed:", error);
      return undefined;
    }
  }

  // Dash pattern-matching IDs are objects; CanvasXpress needs a string ID.
  function targetId(id) {
    if (id !== null && typeof id === "object") {
      return Object.keys(id)
        .sort()
        .map(function (key) {
          return key + "_" + id[key];
        })
        .join("_")
        .replace(/[^A-Za-z0-9_]/g, "_");
    }
    return String(id);
  }

  function CXDashElement(props) {
    var id = targetId(props.id);
    var data = React.useMemo(
      function () {
        return parseJson(props.data);
      },
      [props.data]
    );
    var config = React.useMemo(
      function () {
        return parseJson(props.config);
      },
      [props.config]
    );
    var events = React.useMemo(
      function () {
        return parseEvents(props.events);
      },
      [props.events]
    );
    var afterRender = React.useMemo(
      function () {
        return parseJson(props.after_render);
      },
      [props.after_render]
    );

    return e(
      "div",
      { id: id + "-dcxc-parent-context" },
      e(CanvasXpressReact, {
        id: id,
        data: data,
        config: config,
        events: events,
        afterRender: afterRender,
        width: props.width,
        height: props.height,
        jsUrl: props.js_url,
        cssUrl: props.css_url,
        licenseUrl: props.license_url,
      })
    );
  }

  root.canvasxpress.CXDashElement = CXDashElement;
})(window);
