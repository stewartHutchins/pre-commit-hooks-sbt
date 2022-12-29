import asyncio
import logging
import sys
from logging import info
from logging import warning
from pathlib import Path

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import files
from pre_commit_sbt.args.parse_args import log_level
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.args.parse_args import timeout
from pre_commit_sbt.command_runners.lsp_runner import run_via_lsp
from pre_commit_sbt.command_runners.shell_runner import run_via_commandline
from pre_commit_sbt.lsp.conn import connect_to_sbt_server
from pre_commit_sbt.lsp.port_file import connection_details
from pre_commit_sbt.lsp.port_file import port_path
from pre_commit_sbt.lsp.server import is_server_running


async def main_async(args: list[str] | None = None, cwd: Path = Path(".")) -> int:
    parser = arg_parser()
    parsed_args = parser.parse_args(args)

    _set_up_logging(log_level(parsed_args))

    command: str = _create_command(sbt_command(parsed_args), files(parsed_args))
    await asyncio.wait_for(_run_sbt_command(command, cwd), timeout=timeout(parsed_args))
    return 0


def _create_command(base_command: str, files_: list[str]) -> str:
    return f"""{base_command} {" ".join(_quote(file) for file in files_)}"""


def _quote(string: str) -> str:
    return f'"{string}"'


def _set_up_logging(level: str) -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.getLevelName(level))


async def _run_sbt_command(command: str, cwd: Path) -> None:
    info(f'Running command: "{command}"')
    if is_server_running(cwd):
        with (open(port_path(cwd), encoding="UTF-8") as fp, connect_to_sbt_server(connection_details(fp)) as conn):
            info("Running command via LSP")
            await run_via_lsp(command, conn)
    else:
        info("Running command via commandline")
        warning("Running commands via the commandline can be slow. Start an SBT server to avoid unnecessary overhead.")
        await run_via_commandline(command, cwd)
    info("Successfully ran hook")


def main(args: list[str] | None = None) -> int:
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
