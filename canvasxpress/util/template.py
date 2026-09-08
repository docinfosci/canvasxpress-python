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
    compiled = {f"@{k}@": str(v).replace("@", "\\@") for k, v in data.items()}

    for placeholder, value in compiled.items():
        template = template.replace(placeholder, value)

    return template
