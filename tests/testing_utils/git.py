import subprocess
from pathlib import Path


def git_init(repo: Path) -> None:
    subprocess.run("git init", cwd=repo, check=True, shell=True, capture_output=True)


def git_add(repo: Path, file: Path | str) -> None:
    subprocess.run(f"git add {file}", cwd=repo, check=True, shell=True)


def git_commit(repo: Path, msg: str, additional_flags: str = "") -> None:
    subprocess.run(
        f'git -c user.name="username" -c user.email="user@email.com" commit -m "{msg}" {additional_flags}',
        cwd=repo,
        check=True,
        shell=True,
    )
