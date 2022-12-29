import json
from asyncio import StreamReader

import pytest

from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.failed_command_error import FailedCommandError
from pre_commit_sbt.lsp.receive import read_until_complete_message


@pytest.mark.asyncio
async def test_read_until_complete_message_to_complete() -> None:
    """read_until_complete_message should wait for a completion message"""
    # arrange
    expected_task_id = 10
    expected_exit_code = 0
    expected_json = json.dumps({"id": expected_task_id, "result": {"exitCode": expected_exit_code}})
    reader = _create_reader_with_msg(
        f"""Content-Length: {len(expected_json)}\r\n"""
        f"""Content-Type: application/vscode-jsonrpc; charset=utf-8\r\n"""
        f"""\r\n"""
        f"{expected_json}\r\n"
    )

    # act
    actual = await read_until_complete_message(reader, expected_task_id)

    # assert
    assert actual["id"] == expected_task_id
    assert actual["result"]["exitCode"] == expected_exit_code  # type: ignore


@pytest.mark.asyncio
async def test_read_until_complete_message_no_completion_msg() -> None:
    """wait_for_task_to_complete should raise an exception if no message is returned"""
    # arrange
    empty_reader = _create_reader_with_eof()

    # act & assert
    with pytest.raises(FailedCommandError) as ex:
        await read_until_complete_message(empty_reader, 10)
    assert ex.value.args[0] == COMMAND_FAILED


def _create_reader_with_msg(msg: str) -> StreamReader:
    reader = StreamReader()
    reader.feed_data(msg.encode("UTF-8"))
    return reader


def _create_reader_with_eof() -> StreamReader:
    reader = StreamReader()
    reader.feed_eof()
    return reader
