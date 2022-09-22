import subprocess
from pathlib import Path
from subprocess import CompletedProcess


def install_pre_commit(repo: Path) -> None:
    subprocess.run("pre-commit install", cwd=repo, check=True, shell=True)


def pre_commit_try_repo(repo: Path, *, hook_repo: Path, hook_id: str) -> CompletedProcess[bytes]:
    return subprocess.run(
        f"pre-commit try-repo {hook_repo} {hook_id} --verbose --all-files",
        cwd=repo,
        check=False,
        shell=True,
    )
