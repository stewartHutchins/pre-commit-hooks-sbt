import json
from pathlib import Path
from typing import TextIO
from urllib.parse import urlparse

_ACTIVE_JSON_PATH = "project/target/active.json"


def port_path(root_dir: Path) -> Path:
    return root_dir.joinpath(_ACTIVE_JSON_PATH)


def connection_details(active_json_io: TextIO) -> Path:
    parsed_json: dict[str, str] = json.load(active_json_io)
    uri = parsed_json["uri"]
    return Path(urlparse(uri).path)
