from asyncio import open_unix_connection
from pathlib import Path

import pytest
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.lsp.conn import connect_to_sbt_server
from pre_commit_sbt.lsp.port_file import connection_details
from pre_commit_sbt.lsp.port_file import port_path
from pre_commit_sbt.lsp.receive import read_until_complete_message
from pre_commit_sbt.lsp.rpc import command_rpc


@pytest.mark.asyncio
async def test_rpc_is_interperatable_by_server(sbt_project_with_server: Path) -> None:
    # arrange
    add_touch_command_to_sbt(sbt_project_with_server, "touch")
    task_id = 10
    file_to_create = "sample_file.txt"

    with connect_to_sbt_server(connection_details(port_path(sbt_project_with_server).open("r"))) as conn:
        reader, writer = await open_unix_connection(sock=conn)

        # act
        rpc = command_rpc(task_id, rf"""touch "{file_to_create}" """)
        writer.write(rpc.encode("UTF-8"))
        await read_until_complete_message(reader, task_id)

        # assert
        expected_file = sbt_project_with_server.joinpath(file_to_create)
        assert expected_file.exists()
