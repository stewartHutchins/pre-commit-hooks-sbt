import asyncio
import subprocess
from asyncio.subprocess import Process
from pathlib import Path
from socket import SocketType
from typing import AsyncGenerator

import pytest_asyncio
from _pytest.fixtures import SubRequest

from pre_commit_sbt.lsp.conn import connect_to_sbt_server
from pre_commit_sbt.lsp.port_file import connection_details
from pre_commit_sbt.lsp.port_file import port_path
from pre_commit_sbt.lsp.server import is_server_running

_PROJECT_NAME = "Test-SBT-Project".lower()
_TIMEOUT = 30


@pytest_asyncio.fixture(params=[False, True])
async def sbt_project(tmp_path: Path, request: SubRequest) -> AsyncGenerator[Path, None]:
    root_dir = tmp_path.joinpath(_PROJECT_NAME)
    root_dir.mkdir()
    server_process = await _start_server(root_dir)
    if request.param:  # whether the server should remain running during the test
        yield root_dir
        await _shutdown_server(server_process)
    else:
        await _shutdown_server(server_process)
        yield root_dir


@pytest_asyncio.fixture
async def sbt_project_without_server(tmp_path: Path) -> AsyncGenerator[Path, None]:
    server_process = await _start_server(tmp_path)
    await _shutdown_server(server_process)
    yield tmp_path


@pytest_asyncio.fixture
async def sbt_project_with_server(
    tmp_path: Path,
) -> AsyncGenerator[Path, None]:
    server_process = await _start_server(tmp_path)
    yield tmp_path
    await _shutdown_server(server_process)


@pytest_asyncio.fixture
async def sbt_project_with_server_and_socket(
    sbt_project_with_server: Path,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator[tuple[Path, SocketType], None]:
    with (
        port_path(sbt_project_with_server).open() as port_file,
        connect_to_sbt_server(connection_details(port_file)) as conn,
    ):
        yield sbt_project_with_server, conn


async def _start_server(root_dir: Path, shutdown_timeout: int = _TIMEOUT) -> Process:
    process = await asyncio.create_subprocess_shell(
        "sbt", cwd=root_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
    )
    await asyncio.wait_for(_wait_for_server_to_start(root_dir), timeout=shutdown_timeout)
    return process


async def _wait_for_server_to_start(root_dir: Path) -> None:
    while not is_server_running(root_dir):
        await asyncio.sleep(1)


async def _shutdown_server(proc: Process, *, timeout: int = _TIMEOUT) -> None:
    try:
        await asyncio.wait_for(proc.communicate(b"shutdown\n"), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
