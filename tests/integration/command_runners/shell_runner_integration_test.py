import asyncio
from pathlib import Path

import pytest
from testing_utils.sbt import add_sleep_command_to_sbt
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.command_runners.shell_runner import run_via_commandline
from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.failed_command_error import FailedCommandError


@pytest.mark.asyncio
async def test_run_via_commandline_runs_sbt_valid(sbt_project: Path) -> None:
    """Run a sbt command via the commandline successfully"""
    # arrange
    add_touch_command_to_sbt(sbt_project, "touch")
    expected_file = "sample_file.txt"

    # act
    await run_via_commandline(f'touch "{expected_file}"', sbt_project, timeout=60)

    # assert
    assert sbt_project.joinpath(expected_file).exists()


@pytest.mark.asyncio
async def test_run_via_commandline_runs_invalid_command(sbt_project: Path) -> None:
    """Running an invalid sbt command via the commandline should raise an error"""

    # act & assert
    with pytest.raises(FailedCommandError) as actual:
        await run_via_commandline("non_existing_command", sbt_project)

    assert actual.value.args[0] == COMMAND_FAILED


@pytest.mark.asyncio
async def test_run_via_commandline_runs_timeout(sbt_project: Path) -> None:
    """If a command takes too long it should raise an error"""
    add_sleep_command_to_sbt(sbt_project, "sleep")

    # act & assert
    with pytest.raises(asyncio.TimeoutError):
        await run_via_commandline("sleep 10 ", sbt_project, timeout=1)
