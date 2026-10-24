/*
 * CanvasXpress React
 *
 * A React component that renders a CanvasXpress chart, shipped with the
 * canvasxpress Python package. It is plain JavaScript that needs no build
 * step and uses the page's global React (>= 16.8), as provided by hosts such
 * as Plotly Dash.
 *
 * The CanvasXpress library, stylesheet and license are loaded on demand from
 * the given URLs, once per page. The component creates its own <canvas> so
 * that React never reconciles the DOM that CanvasXpress manages, and it
 * recreates the chart whenever its inputs change.
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
 */
(function (root) {
  "use strict";

  var React = root.React;
  var e = React.createElement;

  // Script loads are shared by every chart on the page, keyed by URL.
  var scriptLoads = {};

  function loadScript(url) {
    if (!scriptLoads[url]) {
      scriptLoads[url] = new Promise(function (resolve, reject) {
        var script = document.createElement("script");
        script.src = url;
        script.type = "text/javascript";
        script.referrerPolicy = "origin-when-cross-origin";
        script.onload = function () {
          resolve();
        };
        script.onerror = function () {
          delete scriptLoads[url];
          reject(new Error("Unable to load " + url));
        };
        document.head.appendChild(script);
      });
    }
    return scriptLoads[url];
  }

  function loadStylesheet(url) {
    var links = document.head.querySelectorAll("link[rel='stylesheet']");
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute("href") === url) {
        return;
      }
    }
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = url;
    link.referrerPolicy = "origin-when-cross-origin";
    document.head.appendChild(link);
  }

  function loadLibrary(jsUrl, cssUrl, licenseUrl) {
    if (cssUrl) {
      loadStylesheet(cssUrl);
    }
    if (root.CanvasXpress) {
      return Promise.resolve(root.CanvasXpress);
    }
    var license = licenseUrl ? loadScript(licenseUrl) : Promise.resolve();
    return license
      .then(function () {
        return jsUrl ? loadScript(jsUrl) : undefined;
      })
      .then(function () {
        if (!root.CanvasXpress) {
          throw new Error("CanvasXpress is not available; provide jsUrl");
        }
        return root.CanvasXpress;
      });
  }

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

        var canvas = document.createElement("canvas");
        canvas.id = props.id;
        canvas.width = props.width || 500;
        canvas.height = props.height || 500;
        host.appendChild(canvas);
        setError(null);

        loadLibrary(props.jsUrl, props.cssUrl, props.licenseUrl)
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
          })
          .catch(function (err) {
            console.error(err);
            if (!cancelled) {
              setError(err.message);
            }
          });

        return function () {
          cancelled = true;
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
      ]
    );

    return e(
      "div",
      { className: "canvasxpress-react" },
      error ? e("div", { role: "alert" }, "CanvasXpress could not be loaded: " + error) : null,
      e("div", { ref: hostRef })
    );
  }

  root.canvasxpress = root.canvasxpress || {};
  root.canvasxpress.CanvasXpressReact = CanvasXpressReact;
})(window);
