import subprocess
from asyncio import gather
from asyncio import StreamReader
from asyncio.subprocess import create_subprocess_exec
from logging import debug
from pathlib import Path
from typing import AsyncIterable

from pre_commit_sbt.err.error_msgs import SHELL_FAILURE_MSG
from pre_commit_sbt.err.exceptions import ShellRunnerError

_DEFAULT_ERR_MSG = "No SBT error message."


async def run_via_commandline(command: str, cwd: Path) -> None:
    proc = await create_subprocess_exec("sbt", command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdout is not None  # prevent mypy from complaining
    _, error_msg_opt = await gather(proc.wait(), _read_until_error(proc.stdout))
    if proc.returncode != 0:
        raise ShellRunnerError(
            SHELL_FAILURE_MSG.format(exit_code=proc.returncode, err_msg=error_msg_opt or _DEFAULT_ERR_MSG)
        )


async def _read_until_error(reader: StreamReader) -> str | None:
    async for msg in _msg_iterator(reader):
        debug(msg.strip())
        if msg.startswith("[error]"):
            return msg.removeprefix("[error]")
    return None


async def _msg_iterator(reader: StreamReader) -> AsyncIterable[str]:
    while not reader.at_eof():
        yield (await reader.readline()).decode("UTF-8")
