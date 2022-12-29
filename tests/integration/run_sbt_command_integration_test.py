import asyncio
from pathlib import Path

import pytest
from testing_utils.sbt import add_sleep_command_to_sbt
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.exceptions import FailedCommandError
from pre_commit_sbt.run_sbt_command import main_async


@pytest.mark.asyncio
async def test_main_async(sbt_project: Path) -> None:
    """main_async should run a command"""
    # arrange
    add_touch_command_to_sbt(sbt_project, "touch")
    files_to_create = ["sample1.txt", "sample2.txt", "sample 3.txt"]

    # act
    await main_async(["--command", "touch"] + files_to_create, sbt_project)

    # assert
    for file in files_to_create:
        expected_file = sbt_project.joinpath(file)
        assert expected_file.exists()


@pytest.mark.asyncio
async def test_main_async_timeout(sbt_project: Path) -> None:
    """main_async should time out if the command takes too long"""
    # arrange
    add_sleep_command_to_sbt(sbt_project, "sleep")

    # act & assert
    with pytest.raises(asyncio.TimeoutError):
        await main_async(["--command", "sleep 10", "--timeout", "1"], sbt_project)


@pytest.mark.asyncio
async def test_main_async_invalid_command(sbt_project: Path) -> None:
    """main_async should fail if a command is invalid"""

    # act & assert
    with pytest.raises(FailedCommandError) as ex:
        await main_async(["--command", "non existent command"], sbt_project)

    assert ex.value.args[0] == COMMAND_FAILED
