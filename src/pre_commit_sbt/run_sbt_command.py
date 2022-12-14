import subprocess
import sys
from pathlib import Path

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import files
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.port_file import is_server_runner


def run_sbt_command(_sbt_command: str, _files: list[str], *, cwd: Path) -> int:
    shell_command = _create_command(_sbt_command, _files, is_server_runner(cwd))
    completed_proc = subprocess.run(shell_command, cwd=cwd, shell=True, check=False)
    return completed_proc.returncode


def _create_command(_sbt_command: str, _files: list[str], server_running: bool) -> str:
    sbt_part = "sbt --client" if server_running else "sbt"
    files_part = " ".join(_quote(filename) for filename in _files)
    return f"{sbt_part} '{_sbt_command} {files_part}'"


def _quote(filename: str) -> str:
    return f'"{filename}"'


def main(args: list[str] | None = None, cwd: Path = Path(".")) -> int:
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    _sbt_command = sbt_command(parsed_args)
    _files = files(parsed_args)
    return run_sbt_command(_sbt_command, _files, cwd=cwd)


if __name__ == "__main__":
    sys.exit(main())
