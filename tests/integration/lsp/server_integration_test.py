from pathlib import Path

from pre_commit_sbt.lsp.server import is_server_running


def test_is_running_server_server_is_running(sbt_project_with_server: Path) -> None:
    """should return true if the server is running"""

    # act
    actual = is_server_running(sbt_project_with_server)

    # assert
    assert actual


def test_is_running_server_should_return_flase_if_server_is_not_running(tmp_path: Path) -> None:
    """should return false if no server is not running"""

    # act
    actual = is_server_running(tmp_path)

    # assert
    assert not actual
