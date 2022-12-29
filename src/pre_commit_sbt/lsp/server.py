from pathlib import Path

from pre_commit_sbt.lsp.port_file import port_path


def is_server_running(root_dir: Path) -> bool:
    """
    Determine whether the server is running, based on the presence or lack there of an SBT port file
    :param root_dir: The root directory of the project
    :return: True if SBT server is running in this directory, else False
    """
    return port_path(root_dir).exists()
