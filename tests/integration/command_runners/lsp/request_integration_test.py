from asyncio import open_unix_connection
from pathlib import Path
from socket import SocketType

import pytest
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.command_runners.lsp.request import create_exec_request
from pre_commit_sbt.command_runners.lsp.response import read_until_complete_message


@pytest.mark.asyncio
async def test_request_is_interperatable_by_server(sbt_project_with_server_and_socket: tuple[Path, SocketType]) -> None:
    # arrange
    project_path, sbt_conn = sbt_project_with_server_and_socket
    add_touch_command_to_sbt(project_path, "touch")
    task_id = 10
    file_to_create = "sample_file.txt"

    reader, writer = await open_unix_connection(sock=sbt_conn)

    # act
    rpc = create_exec_request(task_id, rf"""touch "{file_to_create}" """)
    writer.write(rpc.encode("UTF-8"))
    await read_until_complete_message(reader, task_id)

    # assert
    expected_file = project_path.joinpath(file_to_create)
    assert expected_file.exists()
