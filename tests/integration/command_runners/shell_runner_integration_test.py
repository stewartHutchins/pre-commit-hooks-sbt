from pathlib import Path

import pytest
from testing_utils.sbt import add_touch_command_to_sbt

from pre_commit_sbt.command_runners.shell_runner import run_via_commandline
from pre_commit_sbt.err.exceptions import ShellRunnerError


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
    with pytest.raises(ShellRunnerError) as actual:
        await run_via_commandline("non_existing_command", sbt_project_without_server)

    actual_msg = actual.value.args[0]
    assert "Not a valid command: non_existing_command" in actual_msg
    assert "Error Code: 1" in actual_msg
