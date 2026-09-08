"""
Generates CanvasXpress Python code from reproducible JSON files or objects.
"""

from canvasxpress.canvas import CanvasXpress


def generate_canvasxpress_code_from_json_file(
    cx_json_path: str,
    document_includes: bool = True,
    document_render: bool = True,
    document_jupyter_render=False,
) -> str:
    """
    Generates Python code for a CanvasXpress chart from a JSON file.

    Reads a CanvasXpress reproducible research JSON file, constructs a
    CanvasXpress object, and converts it into example Python code.

    Args:
        cx_json_path: A valid path to a reproducible JSON file from which
            a CanvasXpress object is built and converted into example code.
        document_includes: If `True`, include import headers in the output.
            Defaults to `True`.
        document_render: If `True`, include rendering statements in the
            example code. Defaults to `True`.
        document_jupyter_render: If `True`, use Jupyter rendering;
            otherwise, use popup rendering. Defaults to `False`.

    Returns:
        A string containing the generated Python code example.
    """
    with open(cx_json_path, "r") as cx_json_file:
        cx_json = cx_json_file.read()

        return generate_canvasxpress_code(
            CanvasXpress.from_reproducible_json(cx_json),
            document_includes,
            document_render,
            document_jupyter_render,
        )


def generate_canvasxpress_code_from_json(
    cx_json: str,
    document_includes: bool = True,
    document_render: bool = True,
    document_jupyter_render=False,
) -> str:
    """
    Generates Python code for a CanvasXpress chart from JSON text.

    Constructs a CanvasXpress object from reproducible JSON text and
    converts it into example Python code.

    Args:
        cx_json: The reproducible JSON text from which a CanvasXpress
            object is built and converted into example code.
        document_includes: If `True`, include import headers in the output.
            Defaults to `True`.
        document_render: If `True`, include rendering statements in the
            example code. Defaults to `True`.
        document_jupyter_render: If `True`, use Jupyter rendering;
            otherwise, use popup rendering. Defaults to `False`.

    Returns:
        A string containing the generated Python code example.
    """
    return generate_canvasxpress_code(
        CanvasXpress.from_reproducible_json(cx_json),
        document_includes,
        document_render,
        document_jupyter_render,
    )


def generate_canvasxpress_code(
    cx: CanvasXpress,
    document_includes: bool = True,
    document_render: bool = True,
    document_jupyter_render=False,
) -> str:
    """
    Generates Python code for a CanvasXpress chart from an object.

    Builds a string containing import statements, the CanvasXpress object
    initialization, and rendering code based on the provided flags.

    Args:
        cx: The CanvasXpress object from which to generate the example code.
        document_includes: If `True`, include import headers in the output.
            Defaults to `True`.
        document_render: If `True`, include rendering statements in the
            example code. Defaults to `True`.
        document_jupyter_render: If `True`, use Jupyter rendering;
            otherwise, use popup rendering. Defaults to `False`.

    Returns:
        A string containing the generated Python code example with import
        statements, object initialization, and rendering calls.
    """
    example_text = ""

    if document_includes:
        example_text += "from canvasxpress.canvas import CanvasXpress \n"
        example_text += "from canvasxpress.js.collection import CXEvents \n"

        if document_render:
            if document_jupyter_render:
                example_text += (
                    "from canvasxpress.render.jupyter" " import CXNoteBook \n"
                )
            else:
                example_text += (
                    "from canvasxpress.render.popup" " import CXBrowserPopup \n"
                )

    example_text += "\n"
    example_text += "cx = " + repr(cx)

    if document_render:
        if document_jupyter_render:
            example_text += "\n"
            example_text += "display = CXNoteBook(cx) \n"

        else:
            example_text += "\n"
            example_text += "display = CXBrowserPopup(cx) \n"

    example_text += "display.render() \n"

    return example_text
