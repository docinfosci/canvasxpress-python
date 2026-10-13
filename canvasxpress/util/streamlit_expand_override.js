<script type="text/javascript">
// Override expand to open in new window (waits for CanvasXpress)
(function() {
    function initExpand() {
        if (typeof CanvasXpress === 'undefined') {
            setTimeout(initExpand, 50);
            return;
        }
        // Ensure expand method exists on prototype
        if (!CanvasXpress.prototype.expand) {
            CanvasXpress.prototype.expand = function() {};
        }
        const originalExpand = CanvasXpress.prototype.expand;
        CanvasXpress.prototype.expand = function() {
            console.log('[CanvasXpress] Expand button clicked, opening expanded view');
            const chartId = this.config.renderTo;
            const chart = CanvasXpress.getObject(chartId);
            if (!chart) {
                console.error('[CanvasXpress] Chart not found:', chartId);
                return;
            }
            
            // Get the chart's reproducible JSON
            const reprJson = chart.getReproducibleJSON();
            const reprStr = JSON.stringify(reprJson);
            
            // Open new window with 80% screen size
            const w = Math.round(screen.width * 0.8);
            const h = Math.round(screen.height * 0.8);
            const left = Math.round((screen.width - w) / 2);
            const top = Math.round((screen.height - h) / 2);
            const popup = window.open('', '_blank', 
                'width=' + w + ',height=' + h + 
                ',left=' + left + ',top=' + top +
                ',scrollbars=yes,resizable=yes');
            if (popup) {
                popup.document.write(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>CanvasXpress - Expanded View</title>
                        <link href="${CanvasXpress.cssLibraryUrl}" rel="stylesheet" type="text/css" />
                        <script src="${CanvasXpress.jsLibraryUrl}"><\/script>
                        <style>
                            html, body { 
                                margin: 0; 
                                padding: 0; 
                                height: 100%; 
                                overflow: hidden; 
                                background: #f5f5f5;
                            }
                            #closeBtn {
                                position: fixed; bottom: 10px; right: 10px; z-index: 1000;
                                padding: 8px 16px; background: #333; color: white; border: none;
                                border-radius: 4px; cursor: pointer; font-size: 14px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                            }
                            #closeBtn:hover { background: #555; }
                            #chartContainer {
                                width: 100%;
                                height: calc(100vh - 50px);
                                margin-bottom: 50px;
                            }
                        </style>
                    </head>
                    <body>
                        <div id="chartContainer">
                            <canvas id="${chartId}_expanded" style="width:100%;height:100%;"><\/canvas>
                        </div>
                        <button id="closeBtn" onclick="window.close()">Close (ESC)</button>
                        <script>
                            var chartData = ${reprStr};
                            // Ensure toolbar config is preserved
                            if (chartData.config) {
                                chartData.config.showToolbar = true;
                            }
                            console.log('[CanvasXpress] Expanded chart config:', chartData.config);
                            var expandedChart = new CanvasXpress(chartData);
                            // Ensure toolbar is rendered after chart creation
                            setTimeout(function() {
                                if (expandedChart.config && expandedChart.config.showToolbar) {
                                    console.log('[CanvasXpress] Toolbar should be visible');
                                    // Force toolbar render if needed
                                    if (typeof expandedChart.showToolbar === 'function') {
                                        expandedChart.showToolbar();
                                    }
                                }
                                expandedChart.setDimensions(window.innerWidth - 20, window.innerHeight - 60);
                            }, 200);
                            setTimeout(function() {
                                expandedChart.setDimensions(window.innerWidth - 20, window.innerHeight - 60);
                            }, 100);
                            
                            // Resize handler for responsive chart
                            window.addEventListener("resize", function() {
                                expandedChart.setDimensions(window.innerWidth - 20, window.innerHeight - 60);
                            });
                            
                            // Focus the popup
                            window.focus();
                        <\/script>
                    </body>
                    </html>
                `);
                popup.document.close();
                popup.focus();
            } else {
                console.error('[CanvasXpress] Popup blocked - please allow popups for this site');
            }
        };
    }
    initExpand();
})();
</script>