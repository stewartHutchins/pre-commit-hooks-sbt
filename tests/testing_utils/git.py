import subprocess
from pathlib import Path


def git_init(repo: Path) -> None:
    subprocess.run("git init", cwd=repo, check=True, shell=True)


def git_add(repo: Path, file: str) -> None:
    subprocess.run(f"git add {file}", cwd=repo, check=True, shell=True)
