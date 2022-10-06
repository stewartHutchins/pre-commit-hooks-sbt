from pathlib import Path
from subprocess import CompletedProcess

import pytest
from test_utils.file import read_file
from test_utils.file import write_to_file
from test_utils.git import git_add
from test_utils.git import git_init
from test_utils.pre_commit import install_pre_commit
from test_utils.pre_commit import pre_commit_try_repo
from test_utils.text import strip_margin

_PRE_COMMIT_CONFIG_FILE = ".pre-commit-config.yaml"
_SCALAFMT_PLUGIN_VERSION = "2.4.6"
_RUNNER_DIALECT = "scala3"
_SCALAFMT_VERSION = "3.5.9"


@pytest.mark.parametrize(
    "src_file",
    [
        "src/main/scala/Main.scala",
        # pytest.param(
        #     "worksheet.sc",
        #     marks=pytest.mark.xfail(reason="scalafmt plugin does not format worksheet files"),
        # ),
    ],
)
def test_scalafmt_hook_should_format_scala_code(sbt_project_dir: Path, src_file: str) -> None:
    # arrange
    git_init(sbt_project_dir)
    install_pre_commit(sbt_project_dir)

    unformatted_code = strip_margin(
        """ |object Main {
            |  def main(args: Array[String]): Unit = {
            |    println     ("Hello, World!")
            |  }
            |}
            |"""
    )
    write_to_file(sbt_project_dir.joinpath(src_file), unformatted_code)
    write_to_file(
        sbt_project_dir.joinpath("project/plugins.sbt"),
        strip_margin(
            f"""|addSbtPlugin("org.scalameta" % "sbt-scalafmt" % "{_SCALAFMT_PLUGIN_VERSION}")
                |"""
        ),
    )
    write_to_file(
        sbt_project_dir.joinpath(".scalafmt.conf"),
        strip_margin(
            f"""|runner.dialect = {_RUNNER_DIALECT}
                |version = {_SCALAFMT_VERSION}
                |"""
        ),
    )

    # act
    git_add(sbt_project_dir, src_file)
    pre_commit_process: CompletedProcess[bytes] = pre_commit_try_repo(
        sbt_project_dir, hook_repo=Path(".").absolute(), hook_id="scalafmt"
    )

    # assert
    # code commit should not complete
    assert pre_commit_process.returncode != 0

    # code should be formatted
    actual_code = read_file(sbt_project_dir.joinpath(src_file))
    formatted_code = strip_margin(
        """|object Main {
           |  def main(args: Array[String]): Unit = {
           |    println("Hello, World!")
           |  }
           |}
           |"""
    )
    assert actual_code == formatted_code
