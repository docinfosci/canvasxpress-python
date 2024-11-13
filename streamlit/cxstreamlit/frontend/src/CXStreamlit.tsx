import {Streamlit, StreamlitComponentBase, withStreamlitConnection,} from "streamlit-component-lib"
import React, {ReactNode} from "react"
// @ts-ignore
import CanvasXpressReact from "canvasxpress-react"

interface State {
    isFocused: boolean
}

class CXStreamlit extends StreamlitComponentBase<State> {

    public state = {isFocused: false}

    private after_render_functions = []
    private after_render_target = ""

    /**
     * Adds the CanvasXpress script resource if it is not yet part of the DOM.
     */
    private add_canvasxpress_script(cdn_edition: string) {

        let resource_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js";
        if ((typeof (cdn_edition) !== "undefined") && (cdn_edition !== null)) {
            resource_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/"
                + cdn_edition
                + "/canvasXpress.min.js";
        }

        const dom_rsrc_id = "CXStreamlitElementIncludeScript";
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
    private add_canvasxpress_css(cdn_edition: string) {

        let resource_url = "https://www.canvasxpress.org/dist/canvasXpress.css";
        if ((typeof (cdn_edition) !== "undefined") && (cdn_edition !== null)) {
            resource_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/"
                + cdn_edition
                + "/canvasXpress.css";
        }

        const dom_rsrc_id = "CXStreamlitElementIncludeCSS";
        if (!document.getElementById(dom_rsrc_id)) {
            var head = document.getElementsByTagName("head")[0];
            var s = document.createElement("link");
            s.rel = "stylesheet";
            s.href = resource_url;
            s.id = dom_rsrc_id;
            head.appendChild(s);
        }
    }

    /**
     * Applies afterRender functions once the component exists.
     */
    public componentDidMount() {
        try {
            for (const fx of this.after_render_functions) {
                let fx_string = "CanvasXpress.$('" + this.after_render_target + "')." + fx[0] + "(";
                let first_param = true
                for (const p of fx[1]) {
                    if (first_param === false) {
                        fx_string = fx_string + ", ";
                    }
                    if (typeof (p) !== "undefined") {
                        fx_string = fx_string + p;
                    } else {
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
        } catch (err) {
            console.log(
                // @ts-ignore
                "CanvasXpress afterRender error: " + err.toString()
            )
        }
    }

    public render = (): ReactNode => {
        const id = this.props.args["id"]
        const data = this.props.args["data"]
        const config = this.props.args["config"]
        const events = this.props.args["events"]
        const after_render = this.props.args["after_render"]
        const cdn_edition = this.props.args["cdn_edition"]
        const width = this.props.args["width"]
        const height = this.props.args["height"]

        // Streamlit sends us a theme object via props that we can use to ensure
        // that our component has visuals that match the active theme in a
        // streamlit app.
        const {theme} = this.props
        const style: React.CSSProperties = {}

        // Maintain compatibility with older versions of Streamlit that don't send
        // a theme object.
        if (theme) {
            // Use the theme object to style our button border. Alternatively, the
            // theme style is defined in CSS vars.
            const borderStyling = `1px solid ${
                this.state.isFocused ? theme.primaryColor : "gray"
            }`
            style.border = borderStyling
            style.outline = borderStyling
        }

        // Provide CX resources to the page
        this.add_canvasxpress_script(cdn_edition);
        this.add_canvasxpress_css(cdn_edition);

        if (typeof (after_render) !== "undefined") {
            try {
                // eslint-disable-next-line no-eval
                this.after_render_functions = eval("(" + after_render + ")")
            } catch (err) {
                this.after_render_functions = []
            }
        }
        this.after_render_target = id

        let adjusted_data;
        if (typeof (data) !== "undefined") {
            try {
                adjusted_data = JSON.parse(data)
            } catch (err) {
                adjusted_data = data
            }
        }

        let adjusted_config;
        if (typeof (config) !== "undefined") {
            try {
                adjusted_config = JSON.parse(config)
            } catch (err) {
                adjusted_config = config
            }
        }

        let adjusted_events;
        if (typeof (events) !== "undefined") {
            try {
                // eslint-disable-next-line no-eval
                adjusted_events = eval("(" + events + ")")
            } catch (err) {
                adjusted_events = events
            }
        }

        Streamlit.setFrameHeight(height + 2)

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

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(CXStreamlit)
