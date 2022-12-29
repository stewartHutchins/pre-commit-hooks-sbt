import asyncio
import contextlib
import subprocess
from asyncio.subprocess import Process
from pathlib import Path
from typing import AsyncIterator

import pytest_asyncio

_PROJECT_NAME = "Test-SBT-Project".lower()


@pytest_asyncio.fixture
async def sbt_project(tmp_path: Path) -> Path:
    server = await _start_server(tmp_path)
    await _shutdown_server(server)
    return tmp_path


@pytest_asyncio.fixture
async def sbt_project_with_server(tmp_path: Path) -> AsyncIterator[Path]:
    root_dir = tmp_path.joinpath(_PROJECT_NAME)
    root_dir.mkdir()
    async with _sbt_server(root_dir):
        yield root_dir


@contextlib.asynccontextmanager
async def _sbt_server(root_dir: Path) -> AsyncIterator[Process]:
    proc: Process | None = None
    try:
        proc = await _start_server(root_dir)
        yield proc
    finally:
        if proc is not None:
            await _shutdown_server(proc)


async def _start_server(root_dir: Path) -> Process:
    return await asyncio.create_subprocess_shell(
        "sbt", cwd=root_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
    )


async def _shutdown_server(proc: Process) -> None:
    try:
        assert proc.stdin is not None
        proc.stdin.write(b"shutdown\n")
        await _wait_for_exit(proc)
    except asyncio.TimeoutError:
        proc.kill()


async def _wait_for_exit(proc: Process, *, timeout: int = 10) -> None:
    await asyncio.wait_for(_get_return_code(proc), timeout)


async def _get_return_code(proc: Process) -> int:
    while True:
        if proc.returncode == 0:
            return proc.returncode
        await asyncio.sleep(1)
