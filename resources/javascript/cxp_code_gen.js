/**
 * This module provides a means by which CanvasXpress for Python code can be generated.
 * Example: See cxp_code_gen_example.js
 */

/**
 * Formats an object into a string acceptable for use in the generated Python code.
 * @param json_compliant_object The value to format.
 * @param code_indent The number of spaces to indent.  Python standard is 4, but where space should be saved 2
 *  is a typical compromise.
 * @returns {string}
 */
function format_object_to_python_string(
    json_compliant_object,
    code_indent = 4
) {
    let pre_indent = ""
    for (let i = 0; i < code_indent; i++) {
        pre_indent += " "
    }
    return JSON.stringify(json_compliant_object, null, code_indent)
               .split("\n")
               .map(f => pre_indent + f)
               .join("\n")
               .slice(code_indent)
               .replace(/true/g, "True")
               .replace(/false/g, "False")
               .replace(/null/g, "None");
}


/**
 * CanvasXpress charts can create a reproducible JSON using the UI menu system:
 *   File > Save as JSON
 * The content of this file can be provided as a JSON string.  The JSON will be parsed and corresponding
 * CanvasXpress for Python code declaring a chart plus optional supporting view logic will be returned
 * as a string.
 * @param repr_json A string representing the content of a reproducible JSON.
 * @param code_indent The number of spaces to indent.  Python standard is 4, but where space should be saved 2
 *  is a typical compromise.
 * @param code_ctx A string indicating the execution context.  Values can be "jupyter" or "terminal".
 * @param show_include A bool indicating whether
 * @param show_chart A bool indicating whether code to show the chart should be included.
 */
function generate_cx_python_code_from_json(
    repr_json,
    code_indent = 4,
    code_ctx = "terminal",
    show_include = true,
    show_chart = true
) {
    // Indent for code blocks
    let indent = ""
    for (let i = 0; i < code_indent; i++) {
        indent += " "
    }

    // The code block to be built
    let p_code = "";

    // Add includes
    if (show_include) {
        p_code += "from canvasxpress.canvas import CanvasXpress \n";
        if (show_chart) {
            if (code_ctx === "jupyter") {
                p_code += "from canvasxpress.render.jupyter import CXNoteBook \n";
            }
            else {
                p_code += "from canvasxpress.render.popup import CXBrowserPopup \n";
            }
        }
        p_code += "\n";
    }

    // Obtain a valid JSON
    let cx_json = {};
    if (typeof repr_json !== "undefined") {
        try {
            cx_json = JSON.parse(repr_json);
        }
        catch (e) {
            console.log("Error:", e.stack);
        }
    }

    // Extract data and place it into a Python class
    let extra_params = {};
    let width = 500;
    let height = 500;

    p_code += "cx = CanvasXpress( \n";
    for (param of Object.keys(cx_json)) {
        if (cx_json[param] === false) {
            continue
        }
        if (param === "renderTo") {
            p_code += indent + "render_to = \"" + cx_json[param] + "\",\n";
        }
        else if (param === "data") {
            p_code += indent + "data = " + format_object_to_python_string(cx_json[param], code_indent) + ",\n";
        }
        else if (param === "config") {
            if (Object.keys(cx_json[param]).length > 0) {
                p_code += indent + "config = " + format_object_to_python_string(cx_json[param], code_indent) + ",\n";
            }
        }
        else if (param === "events") {
            if (Object.keys(cx_json[param]).length > 0) {
                p_code += indent + "events = " + format_object_to_python_string(cx_json[param], code_indent) + ",\n";
            }
        }
        else if (param === "width") {
            width = cx_json[param];
        }
        else if (param === "height") {
            height = cx_json[param];
        }
        else if (param === "afterRender") {
            let alt_after_render = [];
            for (after_render_fx of cx_json[param]) {
                if (after_render_fx[0] === "setDimensions") {
                    width = after_render_fx[1][0];
                    height = after_render_fx[1][1];
                }
                else {
                    let disallowed_fx = ["userEventsClick"];
                    if (disallowed_fx.includes(after_render_fx[0]) === false) {
                        alt_after_render.push(after_render_fx);
                    }
                }
            }
            if (Object.keys(alt_after_render).length > 0) {
                p_code += indent + "after_render = " + format_object_to_python_string(alt_after_render, code_indent) + ",\n";
            }
        }
        else {
            let disallowed_params_as_extras = [
                "renderTo", "data", "config", "afterRender", "width", "height", "factory", "system", "version", "events", "info"
            ];
            if (disallowed_params_as_extras.includes(param) === false) {
                extra_params[param] = cx_json[param];
            }
        }
    }
    if (Object.keys(extra_params).length > 0) {
        p_code += indent + "other_init_params = " + format_object_to_python_string(extra_params, code_indent) + ",\n";
    }
    p_code += indent + "width = " + width + ",\n";
    p_code += indent + "height = " + height + "\n";
    p_code += ") \n\n";

    // Convert JS and JSON artifacts to Python equivalents
    p_code = p_code
        .replace(/true/g, "True")
        .replace(/false/g, "False")
        .replace(/null/g, "None");

    // Add chart display
    if (show_chart) {
        if (code_ctx === "jupyter") {
            p_code += "display = CXNoteBook(cx) \n";
        }
        else {
            p_code += "display = CXBrowserPopup(cx) \n";
        }
        p_code += "display.render() \n";
    }

    return p_code;
}

module.exports = {generate_cx_python_code_from_json};
