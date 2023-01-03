import contextlib
import subprocess
import time
from pathlib import Path
from subprocess import Popen
from subprocess import SubprocessError
from typing import Callable
from typing import Iterator

import pytest
from pytest_asyncio.plugin import SubRequest

from pre_commit_sbt.port_file import is_server_runner

_TIMEOUT = 30


@pytest.fixture(params=[False, True])
def sbt_project(tmp_path: Path, request: SubRequest) -> Iterator[Path]:
    if request.param:  # start SBT server
        with _sbt_server(tmp_path):
            yield tmp_path
    else:  # don't start SBT server
        yield tmp_path


@pytest.fixture
def sbt_project_with_server(tmp_path: Path) -> Iterator[Path]:
    with _sbt_server(tmp_path):
        yield tmp_path


@contextlib.contextmanager
def _sbt_server(root_dir: Path) -> Iterator[Popen[bytes]]:
    proc: Popen[bytes] | None = None
    try:
        proc = _start_server(root_dir)
        _wait_for(lambda: is_server_runner(root_dir))
        yield proc
    finally:
        if proc is not None:
            _shutdown_server(proc)


def _start_server(root_dir: Path) -> Popen[bytes]:
    return Popen("sbt", cwd=root_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)


def _wait_for(pred: Callable[[], bool], timeout: int = _TIMEOUT) -> None:
    end = time.time() + timeout
    while not pred():
        if time.time() <= end:
            time.sleep(1)


def _shutdown_server(proc: Popen[bytes]) -> None:
    try:
        proc.communicate(b"shutdown\n")
        proc.wait(timeout=_TIMEOUT)
    except SubprocessError:
        proc.kill()
