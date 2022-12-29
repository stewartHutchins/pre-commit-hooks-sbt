import subprocess
from pathlib import Path
from subprocess import CompletedProcess


def run_via_commandline(command: str, *, cwd: Path) -> CompletedProcess[bytes]:
    return subprocess.run(f"sbt {command}", cwd=cwd, shell=True, check=True)
