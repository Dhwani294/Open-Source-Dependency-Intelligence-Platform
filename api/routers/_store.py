from __future__ import annotations

import json
from pathlib import Path


BASE_PATH = Path("data/sample")


def load_json(name: str):
    file_path = BASE_PATH / name

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f).get("records", [])


def load_all():
    return {
        "nvd": load_json("nvd_output.json"),
        "pypi": load_json("pypi_output.json"),
        "osv": load_json("osv_output.json"),
        "github": load_json("github_advisory_output.json"),
        "libraries": load_json("libraries_io_output.json"),
    }