/**
 * This is an example of how to generate CanvasXpress for Python code using a reproducible JSON.  =
 */
const fs = require("fs");
const cx_gen = require("./cxp_code_gen");

// Load a reproducible JSON for area1 as provided by the canvasxpress.org site in October 12th.
let repr_json = fs.readFileSync("area1.json", "utf8");

// Generate the Python code and display it in the console.  Use defaults as provided.
let generic_p_code = cx_gen.generate_cx_python_code_from_json(repr_json);
console.log(generic_p_code);

// Space the examples
console.log("-----")

// Generate Jupyter code with small indents.
let jupyter_p_code = cx_gen.generate_cx_python_code_from_json(
    repr_json,
    indent = 2,
    code_ctx = "jupyter"
);
console.log(jupyter_p_code);
