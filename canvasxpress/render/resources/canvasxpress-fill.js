/*
 * CanvasXpress Fill
 *
 * Keeps a CanvasXpress chart as wide and/or as tall as the element that holds
 * it, for the canvasxpress Python package's fill_to_width and fill_to_height
 * options. This is behaviour of the Python package, not of the CanvasXpress
 * library: a CanvasXpress canvas is drawn at a fixed pixel size and does not
 * reflow, so following a container means measuring it and redrawing the chart
 * at the new size through setDimensions. A dimension that is not filled keeps
 * its configured size. It is plain JavaScript that needs no build step.
 *
 * Exposed as window.canvasxpress.fillContainer(container, targetId, options),
 * where options is {fillToWidth, fillToHeight, width, height}: which
 * dimensions follow the container, and the chart's configured width and
 * height. It returns a function that stops following the container. Following
 * also stops on its own once the container leaves the page.
 *
 * Height is only followed where the container's height is given to it, such
 * as by a parent with a fixed height or a fillable layout. A container whose
 * height comes from its content offers no height to fill, and the chart keeps
 * its height there rather than growing to its own size.
 *
 * After each redraw a bubbling "canvasxpress:resize" event, with detail
 * {targetId, width, height}, is dispatched from the container, so that a host
 * that reports or reserves its content's size, such as an embedded frame, can
 * measure again.
 *
 * The script can run any number of times, as it does when it is embedded in
 * each Jupyter output.
 */
(function (root) {
  "use strict";

  var namespace = (root.canvasxpress = root.canvasxpress || {});
  if (namespace.fillContainer) {
    return;
  }

  var FILL_CLASS = "canvasxpress-fill";
  var STYLE_ID = "canvasxpress-fill-style";

  // Redraws are coalesced over a burst of resize notifications.
  var DEBOUNCE_MS = 50;

  // CanvasXpress does not register a chart synchronously with its constructor,
  // so the first fit is retried. Once a fit succeeds the retries do nothing.
  var RETRY_DELAYS_MS = [0, 100, 400, 1000, 2000];

  // The smallest size a chart is drawn at, so that a container squeezed to
  // nothing, such as while hidden, does not draw a chart without room for it.
  var MIN_SIZE = 50;

  var STYLES = [
    // A canvas briefly wider than its container, between a resize and the
    // redraw, must not widen the container and feed its own width back in.
    "." + FILL_CLASS + " canvas { display: block; max-width: 100%; }",
    // CanvasXpress publishes the chart's data as a table for screen readers,
    // hidden with a one-pixel clip. A table lays out at the width its content
    // needs regardless, which can widen the container and so the chart. A
    // fixed layout holds it to the width it is given; it stays available to
    // screen readers.
    "." + FILL_CLASS + ' table[id$="-cX-a11y-table"] { table-layout: fixed; max-width: 1px; }',
  ].join("\n");

  function addStyles() {
    if (document.getElementById(STYLE_ID)) {
      return;
    }
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = STYLES;
    document.head.appendChild(style);
  }

  function getChart(targetId) {
    try {
      return root.CanvasXpress ? root.CanvasXpress.getObject(targetId) : null;
    } catch (error) {
      return null;
    }
  }

  // The height of the container's content, measured from its children so that
  // it is not limited by the container's own height.
  function contentHeight(container) {
    var top = container.getBoundingClientRect().top;
    var bottom = top;
    for (var i = 0; i < container.children.length; i++) {
      var rect = container.children[i].getBoundingClientRect();
      if (rect.bottom > bottom) {
        bottom = rect.bottom;
      }
    }
    return bottom - top;
  }

  function fillContainer(container, targetId, options) {
    options = options || {};
    var fillToWidth = Boolean(options.fillToWidth);
    var fillToHeight = Boolean(options.fillToHeight);
    if (!container || !targetId || !(fillToWidth || fillToHeight)) {
      return function () {};
    }

    addStyles();
    container.classList.add(FILL_CLASS);
    container.style.boxSizing = "border-box";
    // The container measures the space available to it, not the size of the
    // chart it holds.
    if (fillToWidth) {
      container.style.width = "100%";
      container.style.minWidth = "0";
    }
    if (fillToHeight) {
      container.style.height = "100%";
      container.style.minHeight = "0";
    }

    // The size the chart is drawn at, starting from its configuration.
    var chartWidth = Number(options.width) || 0;
    var chartHeight = Number(options.height) || 0;
    var pending = null;
    var timers = [];
    var observer = null;
    var stopped = false;

    function stop() {
      if (stopped) {
        return;
      }
      stopped = true;
      clearTimeout(pending);
      timers.forEach(clearTimeout);
      root.removeEventListener("resize", schedule);
      if (observer) {
        observer.disconnect();
      }
    }

    function targetHeight() {
      // What the content takes beyond the chart, such as the strip CanvasXpress
      // draws below its canvas, is kept free. Where the container's height
      // comes from its content this gives the chart's own height back, so a
      // chart cannot grow to fill the room it takes itself.
      var extra = contentHeight(container) - chartHeight;
      return Math.floor(container.clientHeight - Math.max(extra, 0));
    }

    function fit() {
      if (stopped) {
        return;
      }
      if (!container.isConnected) {
        stop();
        return;
      }

      // Not yet registered: a later retry or resize tries again.
      var chart = getChart(targetId);
      if (!chart) {
        return;
      }

      var width = fillToWidth ? Math.floor(container.clientWidth) : chartWidth;
      var height = fillToHeight ? targetHeight() : chartHeight;
      if ((fillToWidth && width < MIN_SIZE) || (fillToHeight && height < MIN_SIZE)) {
        return;
      }
      // Re-applying the current size would redraw the chart, and a redraw can
      // itself notify the observer.
      if (width === chartWidth && height === chartHeight) {
        return;
      }

      try {
        chart.setDimensions(width, height);
      } catch (error) {
        console.error("CanvasXpress chart " + targetId + " could not be resized:", error);
        return;
      }
      chartWidth = width;
      chartHeight = height;

      container.dispatchEvent(
        new CustomEvent("canvasxpress:resize", {
          bubbles: true,
          detail: { targetId: targetId, width: width, height: height },
        })
      );
    }

    function schedule() {
      clearTimeout(pending);
      pending = setTimeout(fit, DEBOUNCE_MS);
    }

    root.addEventListener("resize", schedule);

    // A host can change the container's size without the window resizing, such
    // as when a sidebar collapses or an expander opens.
    if ("ResizeObserver" in root) {
      observer = new root.ResizeObserver(schedule);
      observer.observe(container);
    }

    RETRY_DELAYS_MS.forEach(function (delay) {
      timers.push(setTimeout(fit, delay));
    });

    return stop;
  }

  namespace.fillContainer = fillContainer;
})(window);
