import subprocess
from pathlib import Path

import pytest

_PROJECT_NAME = "Test-SBT-Project".lower()


@pytest.fixture
def sbt_project_dir(tmp_path: Path) -> Path:
    subprocess.run(
        f"echo {_PROJECT_NAME} | sbt new scala/scala-seed.g8",
        cwd=tmp_path,
        check=True,
        shell=True,
    )
    return tmp_path.joinpath(_PROJECT_NAME)
