from argparse import ArgumentParser
from argparse import Namespace


def arg_parser() -> ArgumentParser:
    """
    Create an argument parser
    :return: An argument parser
    """
    parser = ArgumentParser()
    parser.add_argument("--command", help="The sbt command to run.", required=True, type=str)
    return parser


def sbt_command(parsed_args: Namespace) -> str:
    """
    Get the value from the "--command" flag.
    :param parsed_args: The args passed to the program
    :return: The sbt command to run
    """
    command: str = parsed_args.command
    return command
