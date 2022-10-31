import asyncio
import sys
from pathlib import Path

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.args.parse_args import timeout
from pre_commit_sbt.command_runners.shell_runner import run_via_commandline


async def main_async(args: list[str] | None = None, cwd: Path = Path(".")) -> int:
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    command = sbt_command(parsed_args)
    _timeout = timeout(parsed_args)
    await asyncio.wait_for(_run_sbt_command(command, cwd), timeout=_timeout)
    return 0


async def _run_sbt_command(command: str, cwd: Path) -> None:
    await run_via_commandline(command, cwd)


def main(args: list[str] | None = None) -> int:
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
