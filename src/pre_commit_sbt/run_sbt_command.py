import asyncio
import sys
from pathlib import Path

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.command_runners.shell_runner import run_via_commandline


async def run_sbt_command(command: str, cwd: Path) -> None:
    await run_via_commandline(command, cwd)


async def main_async(args: list[str] | None = None) -> int:
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    command = sbt_command(parsed_args)
    await run_via_commandline(command, Path("."))
    return 0


def main(args: list[str] | None = None) -> int:
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
