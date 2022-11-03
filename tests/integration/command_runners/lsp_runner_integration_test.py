from pathlib import Path
from socket import SocketType

import pytest
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.command_runners.lsp_runner import run_via_lsp
from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.failed_command_error import FailedCommandError


@pytest.mark.asyncio
async def test_run_via_lsp(sbt_project_with_server_and_socket: tuple[Path, SocketType]) -> None:
    """Run command via the lsp"""
    # arrange
    project_path, sbt_conn = sbt_project_with_server_and_socket
    add_touch_command_to_sbt(project_path, "touch")
    file_to_create = "test_file.txt"

    # act
    await run_via_lsp(f'touch "{file_to_create}"', sbt_conn)

    # assert
    expected_file = project_path.joinpath(file_to_create)
    assert expected_file.exists()


@pytest.mark.asyncio
async def test_run_via_lsp_invalid_command(sbt_project_with_server_and_socket: tuple[Path, SocketType]) -> None:
    """Run command via the lsp"""
    # arrange
    _, sbt_conn = sbt_project_with_server_and_socket

    # act & assert
    with pytest.raises(FailedCommandError) as ex:
        await run_via_lsp("non_existent_command", sbt_conn)

    # assert
    assert ex.value.args[0] == COMMAND_FAILED
