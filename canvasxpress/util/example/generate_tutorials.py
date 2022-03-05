"""
This file can be executed to render the reproducible JSON files located at
`[project]/tutorials/reproducible_json/*.json` into tutorials for general use.
"""
import json
import os
from pathlib import Path
from typing import List

from canvasxpress.util.example.generator import (
    generate_canvasxpress_code_from_json_file,
)

JSON_DIR_PATH = f"{os.getcwd()}/../../../tutorials/reproducible_json/"
JUPYTER_TEMPLATE_PATH = (
    f"{os.getcwd()}/../../../canvasxpress/util/" f"example/template_tutorials.ipynb"
)
JUPYTER_EXAMPLES_DIR_PATH = (
    f"{os.getcwd()}/../../../tutorials/notebook/" f"cx_site_chart_examples/"
)


def get_json_file_paths() -> List[str]:
    """
    Returns a list of all reproducible JSON files tracked for tutorials.
    :returns: `list[str]`
        The file paths as a list of strings.
    """
    json_files = list()
    for file in os.listdir(JSON_DIR_PATH):
        if file.endswith(".json"):
            json_files.append(os.path.join(JSON_DIR_PATH, file))
    return sorted(json_files)


def get_type_from_filename(file_name: str) -> str:
    """
    Returns the type of chart from a reproducible JSON filename.
    :param file_name: `str`
        The name of the file without parent path.
    :returns: `str`
        The name of the chart (e.g., bar) or an empty string.
    """
    assembled_type = ""
    started_type = False
    for name_char in file_name.replace(".json", "")[::-1]:
        if not started_type and name_char.isnumeric():
            continue

        else:
            started_type = True
            assembled_type += name_char

    return assembled_type[::-1]


def get_index_from_filename(file_name: str) -> str:
    """
    Returns the index of chart from a reproducible JSON filename.
    :param file_name: `str`
        The name of the file without parent path.
    :returns: `str`
        The index of the chart (e.g., 1) or an empty string.
    """
    assembled_index = ""
    for name_char in file_name.replace(".json", "")[::-1]:
        if name_char.isnumeric():
            assembled_index += name_char

        else:
            break

    return assembled_index[::-1]


def create_jupyer_template_text(
    chart_type: str, chart_index: str, chart_code: str
) -> str:
    """
    Generates the text for a Jupyter Notebook example given a chart's type,
    index, and code.
    :param: chart_type: `str`
        The type text (e.g., bar) for the chart.
    :param chart_index: `str`
        The index text (e.g., 1) for the chart.
    :param chart_code: `str`
        The chart source code.
    :returns: `str`
        The text for the full example and instruction.
    """
    with open(JUPYTER_TEMPLATE_PATH, "r") as template_file:
        example_text = template_file.read()
        example_text = example_text.replace("@type@", chart_type)
        example_text = example_text.replace("@index@", chart_index)

        ipython_json = json.loads(example_text)
        for line in chart_code.splitlines():
            candidate = line

            # Convert render statement to explicit output
            if "display.render()" in candidate:
                candidate = candidate.replace(
                    "display.render()",
                    f'display.render(output_file="{chart_type}_{chart_index}.html")',
                )

            # Add the source line to the document
            ipython_json["cells"][1]["source"].append(candidate + "\n")

        ipython_text = json.dumps(ipython_json)
        return ipython_text


if __name__ == "__main__":
    json_paths = get_json_file_paths()
    for json_path in json_paths:
        try:
            json_name = Path(json_path).name

            chart_type = get_type_from_filename(json_name)
            chart_index = get_index_from_filename(json_name)

            jupyter_notebook_content = create_jupyer_template_text(
                chart_type,
                chart_index,
                generate_canvasxpress_code_from_json_file(
                    json_path, document_jupyter_render=True
                ),
            )

            example_file_name = f"{chart_type}_{chart_index}.ipynb"
            example_file_path = str(
                Path(JUPYTER_EXAMPLES_DIR_PATH).joinpath(example_file_name)
            )
            with open(example_file_path, "w") as example_file:
                example_file.write(jupyter_notebook_content)

        except Exception as e:
            print(f"Cannot process file: {json_path}")
            print(f"Exception: {e}")
