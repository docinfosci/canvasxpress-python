"""
This file can be executed to convert the reproducible JSON files located at
`[project]/tutorials/reproducible_json/*.json` into tutorials for general use.
"""
import os
from typing import List


def get_json_file_paths() -> List[str]:
    """
    Returns a list of all reproducible JSON files tracked for tutorials.
    :returns: `list[str]`
        The file paths as a list of strings.
    """
    json_dir = "tutorials/reproducible_json/"
    json_files = list()
    for file in os.listdir(json_dir):
        if file.endswith(".json"):
            json_files.append(
                os.path.join(json_dir, file)
            )
    return json_files


if __name__ == "__main__":
    pass
