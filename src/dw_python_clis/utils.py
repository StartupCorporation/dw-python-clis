import tomllib
from pathlib import Path


def get_pyproject_content(file_path: Path) -> dict:
    with open(file_path, "rb") as f:
        parsed_file = tomllib.load(f)

    return parsed_file
