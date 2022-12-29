import subprocess
from asyncio import StreamReader
from asyncio.subprocess import create_subprocess_exec
from pathlib import Path
from typing import AsyncIterable

from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.exceptions import FailedCommandError


async def run_via_commandline(command: str, cwd: Path) -> None:
    proc = await create_subprocess_exec("sbt", command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdout is not None
    is_successful = await _is_command_successful(proc.stdout)
    _assert_successful(is_successful)


def _assert_successful(successful: bool) -> None:
    if not successful:
        raise FailedCommandError(COMMAND_FAILED)


async def _msg_iterator(reader: StreamReader) -> AsyncIterable[str]:
    while not reader.at_eof():
        yield (await reader.readline()).decode("UTF-8")


async def _is_command_successful(reader: StreamReader) -> bool:
    async for msg in _msg_iterator(reader):
        print(msg)
        if msg.startswith("[error]"):
            return False
    return True
