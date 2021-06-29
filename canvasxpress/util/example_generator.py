from canvasxpress.canvas import CanvasXpress


def generate_canvasxpress_code(
        cx: CanvasXpress,
        document_includes: bool = True,
        document_render: bool = True,
        document_jupyter_render = False,
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
        example_text += "from canvasxpress.canvas import CanvasXpress"

        if document_render:
            if document_jupyter_render:
                example_text += "from canvasxpress.render.jupyter" \
                                " import CXNoteBook"
            else:
                example_text += "from canvasxpress.render.popup" \
                                " import CXBrowserPopup"

    example_text += "\n"
    example_text += "cx = " + repr(cx)

    if document_render:
        if document_jupyter_render:
            example_text += "\n"
            example_text += "renderer = CXNoteBook(cx) \n"

        else:
            example_text += "\n"
            example_text += "renderer: CXBrowserPopup(cx) \n"

    example_text += "renderer.render() \n"

    return example_text
