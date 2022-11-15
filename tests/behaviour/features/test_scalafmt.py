import json
import subprocess
from pathlib import Path

from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from testing_utils.git import git_add
from testing_utils.git import git_commit
from testing_utils.git import git_init

_PRE_COMMIT_CONFIG_FILE = ".pre-commit-config.yaml"

_UNFORMATTED_CODE = """\
object Main {
  def main(args: Array[String]): Unit = {
    println     ("Hello, World!")
  }
}
"""

_EXPECTED_FORMATTED_CODE = """\
object Main {
  def main(args: Array[String]): Unit = {
    println("Hello, World!")
  }
}
"""


@scenario("scalafmt.feature", "scala code is formatted")
def test_scalafmt(sbt_project: Path) -> None:  # pylint: disable=unused-argument
    pass


@given("an sbt project with scalafmt configured")
def create_sbt_project(sbt_project: Path) -> None:
    _create_plugins_file(
        sbt_project,
        content=f"""
addSbtPlugin("org.scalameta" % "sbt-scalafmt" % "{get_test_config()["scalafmt.plugun.version"]}")
""",
    )
    _create_scalafmt_config_file(
        sbt_project,
        content=f"""
runner.dialect = {get_test_config()["runner.dialect"]}
version = {get_test_config()["scalafmt.version"]}
""",
    )

    git_init(sbt_project)
    git_add(sbt_project, sbt_project.joinpath("project/plugins.sbt"))
    git_commit(sbt_project, "Add sbt project with scalafmt set up.")


@given("there is an unformatted scala file in src/")
def create_src_file(sbt_project: Path) -> None:
    sbt_project.joinpath("src/main/scala").mkdir(parents=True)
    sbt_project.joinpath("src/main/scala/Main.scala").open("w").write(_UNFORMATTED_CODE)


@when("I run pre-commit")
def run_pre_commit(sbt_project: str) -> None:
    subprocess.run(
        f"pre-commit try-repo {Path('.').absolute()} scalafmt --verbose --all-files",
        cwd=sbt_project,
        check=False,
        shell=True,
    )


@then("the code should be formatted")
def assert_src_code_is_formatted(sbt_project: Path) -> None:
    actual_code = sbt_project.joinpath("src/main/scala/Main.scala").open("r").read()
    assert actual_code == _EXPECTED_FORMATTED_CODE


def _create_plugins_file(root: Path, content: str) -> None:
    root.joinpath("project/plugins.sbt").open("w").writelines(content)


def _create_build_file(root: Path, content: str) -> None:
    root.joinpath("build.sbt").open("w").write(content)


def _create_scalafmt_config_file(root: Path, content: str) -> None:
    root.joinpath(".scalafmt.conf").open("w").write(content)


def get_test_config() -> dict[str, str]:
    file = Path("tests/behaviour/features/test_config.json").open("r", encoding="UTF-8")
    config: dict[str, str] = json.load(file)
    return config
