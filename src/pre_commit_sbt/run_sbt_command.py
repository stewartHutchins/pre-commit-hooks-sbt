import sys
from pathlib import Path

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.sbt.unix_shell import run_via_commandline


def run_sbt_command(command: str) -> int:
    process = run_via_commandline(command, cwd=Path("."))
    return process.returncode


def main(args: list[str] | None = None) -> int:
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    command = sbt_command(parsed_args)
    return run_sbt_command(command)


if __name__ == "__main__":
    sys.exit(main())
