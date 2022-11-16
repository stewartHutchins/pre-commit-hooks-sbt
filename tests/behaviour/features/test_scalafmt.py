import json
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


@given("an sbt project with scalafmt configured")
def create_sbt_project(sbt_project: Path) -> None:
    plugins_file = sbt_project.joinpath("project/plugins.sbt")
    plugins_file.parent.mkdir(parents=True, exist_ok=True)
    plugins_file.write_text(
        f'addSbtPlugin("org.scalameta" % "sbt-scalafmt" % "{_get_test_config()["scalafmt.plugun.version"]}")'
    )
    scalafmt_conf = sbt_project.joinpath(".scalafmt.conf")
    scalafmt_conf.write_text(
        f"""
runner.dialect = {_get_test_config()["runner.dialect"]}
version = {_get_test_config()["scalafmt.version"]}
"""
    )
    git_init(sbt_project)
    git_add(sbt_project, plugins_file)
    git_add(sbt_project, scalafmt_conf)
    git_commit(sbt_project, "Add sbt project with scalafmt set up.")


@given(parsers.cfparse("there is unformatted code in {file_name:Path}", extra_types={"Path": Path}))
def create_unformatted_file(sbt_project: Path, file_name: Path) -> None:
    file = sbt_project.joinpath(file_name)
    file.parent.mkdir(parents=True, exist_ok=True)
    if str(file_name).endswith("scala"):
        file.write_text(_UNFORMATTED_SCALA_CODE)
    elif str(file_name).endswith("sbt"):
        file.write_text(_UNFORMATTED_SBT_CODE)
    else:
        raise ValueError("Was not scala or sbt files.")


@given(parsers.cfparse("I git add {file_name:Path}", extra_types={"Path": Path}))
def git_add_file(sbt_project: Path, file_name: Path) -> None:
    git_add(sbt_project, file_name)


@given(parsers.cfparse("the file {file_name:Path} is in the commit history", extra_types={"Path": Path}))
def commit_to_history(sbt_project: Path, file_name: Path) -> None:
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
    if str(file_name).endswith("scala"):
        assert actual_content == _FORMATTED_SCALA_CODE
    elif str(file_name).endswith("sbt"):
        assert actual_content == _FORMATTED_SBT_CODE


@then(parsers.cfparse("the code in the code in {file_name:Path} should not be formatted", extra_types={"Path": Path}))
def assert_code_not_formatted(sbt_project: Path, file_name: Path) -> None:
    actual_content = sbt_project.joinpath(file_name).read_text()
    if str(file_name).endswith("scala"):
        assert actual_content == _UNFORMATTED_SCALA_CODE
    elif str(file_name).endswith("sbt"):
        assert actual_content == _UNFORMATTED_SBT_CODE


def _get_test_config() -> dict[str, str]:
    config_file = Path("tests/behaviour/features/test_config.json")
    config: dict[str, str] = json.load(config_file.open("r", encoding="UTF-8"))
    return config
