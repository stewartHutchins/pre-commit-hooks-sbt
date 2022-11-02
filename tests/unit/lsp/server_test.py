from pathlib import Path

from pre_commit_sbt.lsp.port_file import port_path
from pre_commit_sbt.lsp.server import is_server_running


def test_is_server_running_when_file_is_present(tmp_path: Path) -> None:
    """is_server_running should return true false if the file exits"""
    # arrange
    port_file = port_path(tmp_path)
    port_file.parent.mkdir(parents=True)
    port_file.open("w")

    # act
    actual = is_server_running(tmp_path)

    # assert
    assert actual


def test_is_server_running_when_file_is_not_present(tmp_path: Path) -> None:
    """is_server_running should return false if the file exits"""
    # act
    actual = is_server_running(port_path(tmp_path))

    # assert
    assert not actual
