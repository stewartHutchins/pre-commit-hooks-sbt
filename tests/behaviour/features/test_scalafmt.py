import shutil
import subprocess
from pathlib import Path

from pytest_bdd import given
from pytest_bdd import parsers
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from testing_utils.git import git_add
from testing_utils.git import git_commit
from testing_utils.git import git_init
from testing_utils.sbt import sbt_reload

_PRE_COMMIT_CONFIG_FILE = ".pre-commit-config.yaml"

_UNFORMATTED_SCALA_CODE = """\
object Main {
  def main(args: Array[String]): Unit = {
    println     ("Hello, World!")
  }
}
"""

_FORMATTED_SCALA_CODE = """\
object Main {
  def main(args: Array[String]): Unit = {
    println("Hello, World!")
  }
}
"""

_UNFORMATTED_SBT_CODE = """\
lazy val root = (project in file("."))
  .settings(                    )
"""

_FORMATTED_SBT_CODE = """\
lazy val root = (project in file("."))
  .settings()
"""


@scenario("scalafmt.feature", "scala code is formatted")
def test_scalafmt_scala_code(sbt_project: Path) -> None:  # pylint: disable=unused-argument
    pass


@scenario("scalafmt.feature", "sbt code is formatted")
def test_scalafmt_sbt_code(sbt_project: Path) -> None:  # pylint: disable=unused-argument
    pass


@scenario("scalafmt.feature", "only staged code is formatted")
def test_scalafmt_working_tree(sbt_project: Path) -> None:  # pylint: disable=unused-argument
    pass


@given("a sbt project with scalafmt")
def create_sbt_project_with_scalafmt(sbt_project: Path) -> None:
    shutil.copytree(
        "testing/project_with_scalafmt_command",
        sbt_project,
        dirs_exist_ok=True,
    )
    git_init(sbt_project)
    git_add(sbt_project, ".")
    git_commit(sbt_project, "Add sbt project with scalafmt set up.")
    sbt_reload(sbt_project)


@given(parsers.cfparse("there is unformatted code in {file_name:Path}", extra_types={"Path": Path}))
def create_unformatted_file(sbt_project: Path, file_name: Path) -> None:
    file = sbt_project.joinpath(file_name)
    file.parent.mkdir(parents=True, exist_ok=True)
    file_type = file_name.suffix
    if file_type == ".scala":
        file.write_text(_UNFORMATTED_SCALA_CODE)
    elif file_type == ".sbt":
        file.write_text(_UNFORMATTED_SBT_CODE)
    else:
        raise ValueError(f"Extension {file_type} not supported.")


@given(parsers.cfparse("I git add {file_name:Path}", extra_types={"Path": Path}))
def git_add_file(sbt_project: Path, file_name: Path) -> None:
    git_add(sbt_project, file_name)


@given(parsers.cfparse("the file {file_name:Path} is in the commit history", extra_types={"Path": Path}))
def commit_no_verify(sbt_project: Path, file_name: Path) -> None:
    git_add(sbt_project, file_name)
    git_commit(sbt_project, f"Add {file_name}", "--no-verify")


@when("I run pre-commit")
def run_pre_commit(sbt_project: Path) -> None:
    subprocess.run(
        f"pre-commit try-repo {Path('.').absolute()} scalafmt --verbose",
        cwd=sbt_project,
        check=False,
        shell=True,
    )


@then(parsers.cfparse("the code in {file_name:Path} should be formatted", extra_types={"Path": Path}))
def assert_code_is_formatted(sbt_project: Path, file_name: Path) -> None:
    actual_content = sbt_project.joinpath(file_name).read_text()
    if file_name.suffix == ".scala":
        assert actual_content == _FORMATTED_SCALA_CODE
    elif file_name.suffix == ".sbt":
        assert actual_content == _FORMATTED_SBT_CODE


@then(parsers.cfparse("the code in the code in {file_name:Path} should not be formatted", extra_types={"Path": Path}))
def assert_code_not_formatted(sbt_project: Path, file_name: Path) -> None:
    actual_content = sbt_project.joinpath(file_name).read_text()
    if str(file_name).endswith("scala"):
        assert actual_content == _UNFORMATTED_SCALA_CODE
    elif str(file_name).endswith("sbt"):
        assert actual_content == _UNFORMATTED_SBT_CODE
