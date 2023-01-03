import shutil
from pathlib import Path

from pre_commit_sbt.run_sbt_command import main
from pre_commit_sbt.run_sbt_command import run_sbt_command


def test_run_sbt_command(tmp_path: Path) -> None:
    # arrange
    project_root = tmp_path
    shutil.copytree(
        "testing/project_with_touch_command",
        project_root,
        dirs_exist_ok=True,
    )
    # act
    ret_code = run_sbt_command("touch", ["a.txt", "b.txt", "c.txt"], cwd=project_root)

    # assert
    assert ret_code == 0
    assert project_root.joinpath("a.txt").exists()
    assert project_root.joinpath("b.txt").exists()
    assert project_root.joinpath("c.txt").exists()


def test_run_sbt_command_non_existent_command(tmp_path: Path) -> None:
    # arrange
    project_root = tmp_path

    # act
    ret_code = run_sbt_command("non-existent-command", [], cwd=project_root)

    # assert
    assert ret_code != 0


def test_main(tmp_path: Path) -> None:
    # arrange
    project_root = tmp_path
    shutil.copytree(
        "testing/project_with_touch_command",
        project_root,
        dirs_exist_ok=True,
    )
    # act
    ret_code = main(["--command", "touch", "a.txt", "b.txt", "c.txt"], cwd=project_root)

    # assert
    assert ret_code == 0
    assert project_root.joinpath("a.txt").exists()
    assert project_root.joinpath("b.txt").exists()
    assert project_root.joinpath("c.txt").exists()
