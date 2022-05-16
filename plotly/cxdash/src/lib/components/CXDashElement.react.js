import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CanvasXpressReact from "canvasxpress-react";


/**
 * CXDashElement implements a Plotly Dash integration of CanvasXpress React.
 * Properties are defined for use by the CanvasXpress class to update
 * CanvasXpress aspects such as data, config, and sizing.
 */
export default class CXDashElement extends Component {

    after_render_functions = []
    after_render_target = ""

    /**
     * Adds the CanvasXpress script resource if it is not yet part of the DOM.
     */
    add_canvasxpress_script(cdn_edition) {

        let resource_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js";
        if (typeof(cdn_edition) !== "undefined") {
            resource_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/"
                + cdn_edition
                + "/canvasXpress.min.js";
        }

        const dom_rsrc_id = "CXDashElementIncludeScript";
        if (!document.getElementById(dom_rsrc_id)) {
            var head = document.getElementsByTagName("head")[0];
            var s = document.createElement("script");
            s.type = "text/javascript";
            s.src = resource_url;
            s.id = dom_rsrc_id;
            head.appendChild(s);
        }
    }

    /**
     * Adds the CanvasXpress CSS resource if it is not yet part of the DOM.
     */
    add_canvasxpress_css(cdn_edition) {

        let resource_url = "https://www.canvasxpress.org/dist/canvasXpress.css";
        if (typeof(cdn_edition) !== "undefined") {
            resource_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/"
                + cdn_edition
                + "canvasXpress.css";
        }

        const dom_rsrc_id = "CXDashElementIncludeCSS";
        if (!document.getElementById(dom_rsrc_id)) {
            var head = document.getElementsByTagName("head")[0];
            var s = document.createElement("style");
            s.type = "text/css";
            s.src = resource_url;
            s.id = dom_rsrc_id;
            head.appendChild(s);
        }
    }

    /**
     * Applies afterRender functions once the component exists.
     */
    componentDidMount() {
        try {
            for (const fx of this.after_render_functions) {
                let fx_string = "CanvasXpress.$('" + this.after_render_target + "')." + fx[0] + "(";
                let first_param = true
                for (const p of fx[1]) {
                    if (first_param === false) {
                        fx_string = fx_string + ", ";
                    }
                    if (typeof(p) !== "undefined") {
                        fx_string = fx_string + p;
                    }
                    else {
                        fx_string = fx_string + "null";
                    }
                    if (first_param) {
                        first_param = false
                    }
                }
                fx_string = fx_string + ");";
                console.log("Executing " + fx_string);

                // eslint-disable-next-line no-eval
                eval(fx_string);
            }
        }
        catch(err) {
            console.log(
                "CanvasXpress afterRender error: " + err.toString()
            )
        }
    }

    /**
     * Renders the Plotly Dash component using CanvasXpress React.
     * @returns {JSX.Element}
     */
    render() {
        const {id, data, config, events, after_render, cdn_edition, width, height} = this.props;

        // Provide CX resources to the page
        this.add_canvasxpress_script(cdn_edition);
        this.add_canvasxpress_css(cdn_edition);

        if (typeof(after_render) !== "undefined") {
            try {
                // eslint-disable-next-line no-eval
                this.after_render_functions = eval("(" + after_render + ")")
            }
            catch(err) {
                this.after_render_functions = []
            }
        }
        this.after_render_target = id

        let adjusted_data;
        if (typeof(data) !== "undefined") {
            try {
                adjusted_data = JSON.parse(data)
            }
            catch(err) {
                adjusted_data = data
            }
        }

        let adjusted_config;
        if (typeof(config) !== "undefined") {
            try {
                adjusted_config = JSON.parse(config)
            }
            catch(err) {
                adjusted_config = config
            }
        }

        let adjusted_events;
        if (typeof(events) !== "undefined") {
            try {
                // eslint-disable-next-line no-eval
                adjusted_events = eval("(" + events + ")")
            }
            catch(err) {
                adjusted_events = events
            }
        }

        return (
            <div id={id + "-dcxc-parent-context"}>
                <CanvasXpressReact
                    target={id}
                    data={adjusted_data}
                    config={adjusted_config}
                    events={adjusted_events}
                    width={width}
                    height={height}
                />
            </div>
        );
    }
}

CXDashElement.defaultProps = {};

CXDashElement.propTypes = {
    /**
     * The ID of the element for use in function calls and element identification.
     */
    id: PropTypes.string.isRequired,

    /**
     * The data JSON, generally in the XYZ format.
     */
    data: PropTypes.string,

    /**
     * The configuration JSON dictating formatting and content management.
     */
    config: PropTypes.string,

    /**
     * The events functions for increased reactivity.
     */
    events: PropTypes.string,

    /**
     * The events functions for increased reactivity.
     */
    after_render: PropTypes.string,

    /**
     * The Javascript and CSS CDN edition that should be used for CanvasXpress functionality.
     */
    cdn_edition: PropTypes.string,

    /**
     * The element width.
     */
    width: PropTypes.string,

    /**
     * The element height.
     */
    height: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
