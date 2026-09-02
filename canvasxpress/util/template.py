def render_from_template(template: str, data: dict) -> str:
    """
    Updates the template text with the provided data.

    Replaces all occurrences of `@key@` in the template with the
    corresponding value from the data dictionary.

    Args:
        template: The template string containing `@key@` placeholders.
        data: A dictionary of key-value pairs used to replace placeholders.

    Returns:
        The template string with all placeholders replaced by their
        corresponding values.
    """
    template_text = template

    for key in data.keys():
        template_text = template_text.replace(f"@{str(key)}@", str(data[key]))

    return template_text
