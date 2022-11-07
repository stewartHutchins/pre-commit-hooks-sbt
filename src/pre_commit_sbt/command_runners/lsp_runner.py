import random
from asyncio import open_unix_connection
from asyncio import StreamWriter
from socket import SocketType

from pre_commit_sbt.command_runners.lsp.error_codes import error_code_to_human_readable
from pre_commit_sbt.command_runners.lsp.receive import read_until_complete_message
from pre_commit_sbt.command_runners.lsp.rpc import command_rpc
from pre_commit_sbt.err.error_msgs import LSP_FAILURE_MSG
from pre_commit_sbt.err.exceptions import LspRunnerError

_MIN_ID = 1
_MAX_ID = 10**6


async def run_via_lsp(sbt_command: str, socket: SocketType) -> None:
    reader, writer = await open_unix_connection(sock=socket)
    task_id = random.randint(_MIN_ID, _MAX_ID)
    json_rpc = command_rpc(task_id, sbt_command)
    _send_to_server(writer, json_rpc)
    completion_msg = await read_until_complete_message(reader, task_id)
    err_code: int = _err_code(completion_msg)  # type: ignore
    if err_code != 0:
        raise LspRunnerError(
            LSP_FAILURE_MSG.format(
                short_reason=error_code_to_human_readable(err_code),
                err_code=err_code,
                err_msg=_error_message(completion_msg),  # type: ignore
            )
        )


def _send_to_server(writer: StreamWriter, json_rpc: str) -> None:
    writer.write(json_rpc.encode("UTF-8"))


def _err_code(completion_msg: dict[str, dict[str, int]]) -> int:
    if "result" in completion_msg:  # pylint: disable=no-else-return
        return completion_msg["result"]["exitCode"]
    else:
        return completion_msg["error"]["code"]


def _error_message(completion_msg: dict[str, dict[str, str]]) -> str:
    return completion_msg["error"]["message"]
