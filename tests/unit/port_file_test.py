from pathlib import Path

from pre_commit_sbt.port_file import is_server_runner
from pre_commit_sbt.port_file import port_path


def test_active_json_is_file(sbt_project_with_server: Path) -> None:
    # arrange
    project_root = sbt_project_with_server

    # act
    port_file = port_path(project_root)

    # assert
    assert port_file.exists()


def test_active_json_is_not_file(tmp_path: Path) -> None:
    # arrange
    project_root = tmp_path

    # act
    port_file = port_path(project_root)

    # assert
    assert not port_file.exists()


def test_is_server_runner_false(sbt_project_with_server: Path) -> None:
    # arrange
    project_root = sbt_project_with_server

    # act
    actual = is_server_runner(project_root)

    # assert
    assert actual


def test_is_server_runner_true(tmp_path: Path) -> None:
    # arrange
    project_root = tmp_path

    # act
    actual = is_server_runner(project_root)

    # assert
    assert not actual
