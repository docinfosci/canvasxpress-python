/*
 * CanvasXpress React
 *
 * A React component that renders a CanvasXpress chart, shipped with the
 * canvasxpress Python package. It is plain JavaScript that needs no build
 * step and uses the page's global React (>= 16.8), as provided by hosts such
 * as Plotly Dash.
 *
 * The CanvasXpress library, stylesheet and license are loaded on demand from
 * the given URLs, once per page, by window.canvasxpress.loadLibrary from
 * canvasxpress-loader.js, which must be loaded first. The component creates
 * its own <canvas> so that React never reconciles the DOM that CanvasXpress
 * manages, and it recreates the chart whenever its inputs change.
 *
 * Exposed as window.canvasxpress.CanvasXpressReact.
 *
 * Props:
 *   id          Required. The canvas element ID (the CanvasXpress renderTo).
 *   data        CanvasXpress data (object or string).
 *   config      CanvasXpress configuration object.
 *   events      CanvasXpress events object.
 *   afterRender Array of [functionName, [args...]] calls applied to the chart.
 *   width       Canvas width. Defaults to 500.
 *   height      Canvas height. Defaults to 500.
 *   jsUrl       CanvasXpress library URL, if CanvasXpress is not yet loaded.
 *   cssUrl      CanvasXpress stylesheet URL.
 *   licenseUrl  CanvasXpress license script URL.
 *   fillToWidth True to keep the chart as wide as the component's container,
 *               redrawing it as that changes.
 *   fillToHeight
 *               True to keep the chart as tall as the component's container,
 *               redrawing it as that changes. The container needs a height
 *               set by the layout.
 *
 * Either fill option uses window.canvasxpress.fillContainer from
 * canvasxpress-fill.js, which must then be loaded first. A dimension that is
 * not filled keeps its width or height prop.
 */
(function (root) {
  "use strict";

  var React = root.React;
  var e = React.createElement;

  // The shared CanvasXpress loader (canvasxpress-loader.js), loaded first.
  var loadLibrary = root.canvasxpress.loadLibrary;

  function applyAfterRender(chart, afterRender) {
    if (!Array.isArray(afterRender)) {
      return;
    }
    afterRender.forEach(function (call) {
      var name = call[0];
      var args = Array.isArray(call[1]) ? call[1] : [];
      try {
        if (typeof chart[name] !== "function") {
          throw new Error("CanvasXpress has no function " + name);
        }
        chart[name].apply(chart, args);
      } catch (error) {
        console.error("CanvasXpress afterRender " + name + " failed:", error);
      }
    });
  }

  function CanvasXpressReact(props) {
    var hostRef = React.useRef(null);
    var errorState = React.useState(null);
    var error = errorState[0];
    var setError = errorState[1];

    React.useEffect(
      function () {
        var host = hostRef.current;
        var cancelled = false;
        var chart = null;
        var stopFill = null;

        var canvas = document.createElement("canvas");
        canvas.id = props.id;
        // Kept as numbers: hosts such as Dash pass sizes as strings, and
        // CanvasXpress may rescale the canvas element once it draws.
        var width = Number(props.width) || 500;
        canvas.width = width;
        var height = Number(props.height) || 500;
        canvas.height = height;
        host.appendChild(canvas);
        setError(null);

        loadLibrary({ jsUrl: props.jsUrl, cssUrl: props.cssUrl, licenseUrl: props.licenseUrl })
          .then(function (CanvasXpress) {
            if (cancelled) {
              return;
            }
            chart = new CanvasXpress({
              renderTo: props.id,
              data: props.data || false,
              config: props.config || {},
              events: props.events || false,
            });
            applyAfterRender(chart, props.afterRender);
            if (props.fillToWidth || props.fillToHeight) {
              if (typeof root.canvasxpress.fillContainer === "function") {
                stopFill = root.canvasxpress.fillContainer(host, props.id, {
                  fillToWidth: props.fillToWidth,
                  fillToHeight: props.fillToHeight,
                  width: width,
                  height: height,
                });
              } else {
                console.error("CanvasXpress fillContainer requires canvasxpress-fill.js");
              }
            }
          })
          .catch(function (err) {
            console.error(err);
            if (!cancelled) {
              setError(err.message);
            }
          });

        return function () {
          cancelled = true;
          if (stopFill) {
            stopFill();
          }
          try {
            var existing = chart || (root.CanvasXpress && root.CanvasXpress.getObject(props.id));
            if (existing) {
              existing.destroy();
            }
          } catch (err) {
            console.error("CanvasXpress chart " + props.id + " could not be destroyed:", err);
          }
          while (host.firstChild) {
            host.removeChild(host.firstChild);
          }
        };
      },
      [
        props.id,
        props.data,
        props.config,
        props.events,
        props.afterRender,
        props.width,
        props.height,
        props.jsUrl,
        props.cssUrl,
        props.licenseUrl,
        props.fillToWidth,
        props.fillToHeight,
      ]
    );

    return e(
      "div",
      {
        className: "canvasxpress-react",
        // Passes a height given to the component on to the chart's container.
        style: props.fillToHeight ? { height: "100%" } : undefined,
      },
      error ? e("div", { role: "alert" }, "CanvasXpress could not be loaded: " + error) : null,
      e("div", { ref: hostRef })
    );
  }

  root.canvasxpress = root.canvasxpress || {};
  root.canvasxpress.CanvasXpressReact = CanvasXpressReact;
})(window);
