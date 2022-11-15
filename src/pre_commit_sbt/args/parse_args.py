from argparse import ArgumentParser
from argparse import Namespace

DEFAULT_TIMEOUT = 30
DEFAULT_LOG_LEVEL = "INFO"


def arg_parser() -> ArgumentParser:
    """
    Create an argument parser
    :return: An argument parser
    """
    parser = ArgumentParser()
    parser.add_argument("--command", help="The sbt command to run.", required=True, type=str)
    parser.add_argument(
        "--timeout", help="The timeout for running the command.", required=False, type=int, default=DEFAULT_TIMEOUT
    )
    parser.add_argument(
        "--log-level", help="The logging threshold level.", required=False, type=str, default=DEFAULT_LOG_LEVEL
    )
    parser.add_argument("files", nargs="*")
    return parser


def sbt_command(parsed_args: Namespace) -> str:
    """
    Get the value from the "--command" flag.
    :param parsed_args: The args passed to the program
    :return: The sbt command to run
    """
    command: str = parsed_args.command
    return command


def timeout(parsed_args: Namespace) -> int:
    """
    Get the value from the "--timeout" flag.
    :param parsed_args: The args passed to the program
    :return: The timeout
    """
    _timeout: int = parsed_args.timeout
    return _timeout


def log_level(parsed_args: Namespace) -> str:
    """
    Get the value from the "--log-level" flag.
    :param parsed_args: The args passed to the program
    :return: The logging threshold level
    """
    level: str = parsed_args.log_level
    return level


def files(parsed_args: Namespace) -> list[str]:
    """
    Get the files passed into the tool by the pre-commit framework
    :param parsed_args: The args passed to the program
    :return: The files which have been staged for commit
    """
    files_: list[str] = parsed_args.files
    return files_
