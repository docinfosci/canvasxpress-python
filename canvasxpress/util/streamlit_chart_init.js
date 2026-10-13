<script type="text/javascript">
// Initialize chart when CanvasXpress is loaded
(function() {
    var chartId = "@cx_target_id@";
    var globalKey = "cx_initialized_" + chartId;
    if (window[globalKey]) return;
    
    function initChart() {
        if (window[globalKey]) return;
        if (typeof CanvasXpress !== 'undefined') {
            @code@
            window[globalKey] = true;
        } else {
            setTimeout(initChart, 50);
        }
    }
    initChart();
})();
</script>