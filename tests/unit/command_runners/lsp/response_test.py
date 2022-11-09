import json
from asyncio import StreamReader

import pytest

from pre_commit_sbt.command_runners.lsp.response import error_message
from pre_commit_sbt.command_runners.lsp.response import get_next_message
from pre_commit_sbt.command_runners.lsp.response import is_completion_message
from pre_commit_sbt.command_runners.lsp.response import JsonType
from pre_commit_sbt.command_runners.lsp.response import return_code


@pytest.mark.asyncio
async def test_get_next_message() -> None:
    """get_next_message should read the next message"""
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
    actual = await get_next_message(reader)

    # assert
    assert actual["id"] == expected_task_id
    assert actual["result"]["exitCode"] == expected_exit_code  # type: ignore


@pytest.mark.parametrize(
    ["task_id", "body", "expected"], [[10, {"id": 10}, True], [10, {"id": 9}, False], [10, {}, False]]
)
def test_is_response_message(task_id: int, body: JsonType, expected: bool) -> None:
    # act
    actual = is_completion_message(body, task_id)

    # assert
    assert actual == expected


def test_error_message() -> None:
    # arrange
    expected = "some text"
    body: JsonType = {"error": {"message": expected}}

    # act
    actual = error_message(body)

    # assert
    assert actual == expected


@pytest.mark.parametrize(
    ["body", "expected"],
    [
        [{"result": {"exitCode": 10}}, 10],
        [{"error": {"code": 11}}, 11],
    ],
)
def test_return_code(body: JsonType, expected: int) -> None:
    # act
    actual = return_code(body)

    # assert
    assert actual == expected


def _create_reader_with_msg(msg: str) -> StreamReader:
    reader = StreamReader()
    reader.feed_data(msg.encode("UTF-8"))
    return reader
