import json
from pathlib import Path
from typing import TextIO
from urllib.parse import urlparse

_ACTIVE_JSON_PATH = "project/target/active.json"


def port_path(root_dir: Path) -> Path:
    """
    Get the location of a port file, given the directory an SBT server is running in
    :param root_dir: The root directory of an SBT server
    :return: The path to the port file
    """
    return root_dir.joinpath(_ACTIVE_JSON_PATH)


def connection_details(active_json_io: TextIO) -> Path:
    """
    Get the location of the unix socket, from the opened port file
    :param active_json_io: An opened port file
    :return: The path to the unix socket
    """
    parsed_json: dict[str, str] = json.load(active_json_io)
    uri = parsed_json["uri"]
    return Path(urlparse(uri).path)
