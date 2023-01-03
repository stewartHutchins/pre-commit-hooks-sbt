from argparse import ArgumentParser
from argparse import Namespace


def arg_parser() -> ArgumentParser:
    """
    Create an argument parser
    :return: An argument parser
    """
    parser = ArgumentParser()
    parser.add_argument("--command", help="The sbt command to run.", required=True, type=str)
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


def files(parsed_args: Namespace) -> list[str]:
    """
    Get the files passed into the tool by the pre-commit framework
    :param parsed_args: The args passed to the program
    :return: The files which have been staged for commit
    """
    files_: list[str] = parsed_args.files
    return files_
