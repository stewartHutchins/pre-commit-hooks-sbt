from pathlib import Path

import pytest
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.command_runners.shell_runner import run_via_commandline
from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.exceptions import FailedCommandError


@pytest.mark.asyncio
async def test_run_via_commandline_runs(sbt_project_without_server: Path) -> None:
    """Run a sbt command via the commandline successfully"""
    # arrange
    add_touch_command_to_sbt(sbt_project_without_server, "touch")
    file_to_create = "sample_file.txt"

    # act
    await run_via_commandline(f'touch "{file_to_create}"', sbt_project_without_server)

    # assert
    expected_file = sbt_project_without_server.joinpath(file_to_create)
    assert expected_file.exists()


@pytest.mark.asyncio
async def test_run_via_commandline_runs_invalid_command(sbt_project_without_server: Path) -> None:
    """Running an invalid sbt command via the commandline should raise an error"""

    # act & assert
    with pytest.raises(FailedCommandError) as actual:
        await run_via_commandline("non_existing_command", sbt_project_without_server)

    assert actual.value.args[0] == COMMAND_FAILED
