import subprocess
from pathlib import Path
from subprocess import CompletedProcess


def pre_commit_try_repo(repo: Path, *, hook_repo: Path, hook_id: str) -> CompletedProcess[bytes]:
    proc = subprocess.run(
        f"pre-commit try-repo {hook_repo} {hook_id} --verbose --all-files",
        cwd=repo,
        check=False,
        shell=True,
        capture_output=True,
    )
    return proc
