from canvasxpress.canvas import CanvasXpress


def generate_canvasxpress_code_from_json_file(
    cx_json_path: str,
    document_includes: bool = True,
    document_render: bool = True,
    document_jupyter_render=False,
) -> str:
    """
    Generates a string with a CanvasXPress in Python declaration using a
    CanvasXpress reproducible research JSON stored in a file.
    :param cx_json_path: `str`
        A valid path to the reproducible JSON text from which a CanvasXPress
        object is to be built and then converted into example code.
    :param document_includes: `bool`
        Default `True`.  Indicate if include headers should be prefixed.
    :param document_render: `bool`
        Default `True`.  Indicate if rendering should be included in the
        example code.
    :param document_jupyter_render: `bool`
        Default `False`.  Indicate if Jupyter rendering should be performed;
        otherwise, popup rendering will suffixed.
    :returns: `str`
        A string with the code example.
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
    Generates a string with a CanvasXPress in Python declaration using a
    CanvasXpress reproducible research JSON.
    :param cx_json: `str`
        The reproducible JSON text from which a CanvasXPress object is to be
        built and then converted into example code.
    :param document_includes: `bool`
        Default `True`.  Indicate if include headers should be prefixed.
    :param document_render: `bool`
        Default `True`.  Indicate if rendering should be included in the
        example code.
    :param document_jupyter_render: `bool`
        Default `False`.  Indicate if Jupyter rendering should be performed;
        otherwise, popup rendering will suffixed.
    :returns: `str`
        A string with the code example.
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
    Generates a string with a CanvasXPress in Python declaration.
    :param cx: `CanvasXpress`
        The `CanvasXpress` object from which to generate the example code.
    :param document_includes: `bool`
        Default `True`.  Indicate if include headers should be prefixed.
    :param document_render: `bool`
        Default `True`.  Indicate if rendering should be included in the
        example code.
    :param document_jupyter_render: `bool`
        Default `False`.  Indicate if Jupyter rendering should be performed;
        otherwise, popup rendering will suffixed.
    :returns: `str`
        A string with the code example.
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
