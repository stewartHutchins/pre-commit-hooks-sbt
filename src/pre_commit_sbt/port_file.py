from pathlib import Path

_ACTIVE_JSON_PATH = "project/target/active.json"


def port_path(root: Path) -> Path:
    """
    The path of the port file in the project
    :param root: The root of the project
    :return: The path to the port file
    """
    return root.joinpath(_ACTIVE_JSON_PATH)


def is_server_runner(root: Path) -> bool:
    """
    Whether SBT server is running or not
    :param root: The root of the project
    :return: True if SBT server is running otherwise False
    """
    return port_path(root).exists()
