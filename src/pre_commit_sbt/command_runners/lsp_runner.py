import random
from asyncio import open_unix_connection
from asyncio import StreamReader
from logging import debug
from socket import SocketType
from typing import AsyncIterable

from pre_commit_sbt.command_runners.lsp.request import create_exec_request
from pre_commit_sbt.command_runners.lsp.response import error_code_to_human_readable
from pre_commit_sbt.command_runners.lsp.response import error_message
from pre_commit_sbt.command_runners.lsp.response import get_next_message
from pre_commit_sbt.command_runners.lsp.response import is_completion_message
from pre_commit_sbt.command_runners.lsp.response import JsonType
from pre_commit_sbt.command_runners.lsp.response import return_code
from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.error_msgs import LSP_FAILURE_MSG
from pre_commit_sbt.err.exceptions import FailedCommandError
from pre_commit_sbt.err.exceptions import ShellRunnerError

_MIN_ID = 1
_MAX_ID = 10**6


async def run_via_lsp(sbt_command: str, socket: SocketType) -> None:
    """
    Run a command via LSP
    :param sbt_command: The command to run
    :param socket: A connection to sbt server
    :return: None
    """
    reader, writer = await open_unix_connection(sock=socket)
    task_id = random.randint(_MIN_ID, _MAX_ID)
    json_rpc = create_exec_request(task_id, sbt_command)
    writer.write(json_rpc.encode("UTF-8"))
    completion_msg = await _read_until_complete_message(reader, task_id)
    if (_return_code := return_code(completion_msg)) != 0:
        raise ShellRunnerError(
            LSP_FAILURE_MSG.format(
                short_reason=error_code_to_human_readable(_return_code),
                err_code=_return_code,
                err_msg=error_message(completion_msg),
            )
        )


async def _read_until_complete_message(reader: StreamReader, task_id: int) -> JsonType:
    async for message in _message_iterator(reader):
        debug(message)
        if is_completion_message(message, task_id):
            return message
    raise FailedCommandError(COMMAND_FAILED)


async def _message_iterator(reader: StreamReader) -> AsyncIterable[JsonType]:
    while not reader.at_eof():
        yield await get_next_message(reader)
