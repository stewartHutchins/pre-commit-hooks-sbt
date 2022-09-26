import sys
from pathlib import Path

from pre_commit_sbt.args import parse_args
from pre_commit_sbt.sbt.unix_shell import run_via_commandline


def main() -> int:
    command = parse_args.sbt_command(sys.argv)
    process = run_via_commandline(command, cwd=Path("."))
    return process.returncode


if __name__ == "__main__":
    SystemExit(main())
