from pathlib import Path

from pre_commit_sbt.lsp.port_file import port_path


def is_server_running(root_dir: Path) -> bool:
    return port_path(root_dir).exists()
