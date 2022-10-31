from argparse import ArgumentParser
from argparse import Namespace

DEFAULT_TIMEOUT = 30


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
