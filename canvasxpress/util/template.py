def render_from_template(
        template: str,
        data: dict
) -> str:
    """
    Updates the template text with the provided data.
    :param template: `str` The name of the template file
    :param data: The `dict` of str values with which to update the template text
    :returns The adjusted template text
    """
    template_text = template

    for key in data.keys():
        template_text = template_text.replace(
            f"@{str(key)}@",
            str(data[key])
        )

    return template_text
