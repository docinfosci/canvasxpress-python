"""
This file can be executed to convert the reproducible JSON files located at
`[project]/tutorials/reproducible_json/*.json` into tutorials for general use.
"""
import os
from typing import List

JSON_DIR_PATH = "tutorials/reproducible_json/"
JUPYTER_TEMPLATE_PATH = ""

def get_json_file_paths() -> List[str]:
    """
    Returns a list of all reproducible JSON files tracked for tutorials.
    :returns: `list[str]`
        The file paths as a list of strings.
    """
    json_files = list()
    for file in os.listdir(JSON_DIR_PATH):
        if file.endswith(".json"):
            json_files.append(
                os.path.join(JSON_DIR_PATH, file)
            )
    return json_files


if __name__ == "__main__":
    pass
