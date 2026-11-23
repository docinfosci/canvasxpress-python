/*
 * CanvasXpress Loader
 *
 * Loads the CanvasXpress stylesheet, license and library on demand, once per
 * page, for every way the canvasxpress Python package puts charts into a page:
 * Jupyter outputs, the Streamlit component and the CanvasXpress React wrapper
 * (and so Plotly Dash). It is plain JavaScript that needs no build step.
 *
 * Exposed as window.canvasxpress.loadLibrary(library), where library is
 * {jsUrl, cssUrl, licenseUrl} (each optional). It returns a Promise for the
 * CanvasXpress constructor. The stylesheet does not delay charts. A license is
 * loaded before the library so that charts are created with it, and the
 * library is not loaded again if the page already provides CanvasXpress.
 *
 * The script can run any number of times, as it does when it is embedded in
 * each Jupyter output; loads already made by the page are reused.
 */
(function (root) {
  "use strict";

  var namespace = (root.canvasxpress = root.canvasxpress || {});

  // Script loads are shared by every chart on the page, keyed by URL. They are
  // kept on the namespace so that separately executed copies of this script
  // share them.
  var scriptLoads = (namespace._scriptLoads = namespace._scriptLoads || {});

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
          // Forget the failure so that a later chart can try again.
          delete scriptLoads[url];
          if (script.parentNode) {
            script.parentNode.removeChild(script);
          }
          reject(new Error("Unable to load " + url));
        };
        document.head.appendChild(script);
      });
    }
    return scriptLoads[url];
  }

  function loadStylesheet(url) {
    var links = document.querySelectorAll("link[rel='stylesheet']");
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

  function loadLibrary(library) {
    library = library || {};
    if (library.cssUrl) {
      loadStylesheet(library.cssUrl);
    }
    var license = library.licenseUrl ? loadScript(library.licenseUrl) : Promise.resolve();
    return license
      .then(function () {
        if (!root.CanvasXpress && library.jsUrl) {
          return loadScript(library.jsUrl);
        }
      })
      .then(function () {
        if (!root.CanvasXpress) {
          throw new Error("CanvasXpress is not available; provide jsUrl");
        }
        return root.CanvasXpress;
      });
  }

  namespace.loadLibrary = loadLibrary;
})(window);
