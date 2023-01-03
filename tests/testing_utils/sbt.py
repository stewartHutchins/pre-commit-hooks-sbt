import subprocess
from pathlib import Path


def sbt_reload(root_dir: Path) -> None:
    subprocess.run("sbt --client reload", shell=True, cwd=root_dir, check=True)
