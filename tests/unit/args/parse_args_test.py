import pytest

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import DEFAULT_TIMEOUT
from pre_commit_sbt.args.parse_args import sbt_command
from pre_commit_sbt.args.parse_args import timeout


def test_sbt_command() -> None:
    """parser should get the --command argument"""
    # arrange
    expected = "sample_command"
    args = ["--command", expected]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = sbt_command(parsed_args)

    # assert
    assert actual == expected


def test_missing_sbt_command() -> None:
    """parser should get the --command argument"""
    # arrange
    args: list[str] = []

    # act
    parser = arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(args)


def test_timeout() -> None:
    """parser should get the --timeout argument"""
    # arrange
    expected = 10
    args = ["--command", "ignore", "--timeout", f"{expected}"]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = timeout(parsed_args)

    # assert
    assert actual == expected


def test_timeout_default() -> None:
    """parser should get the --command argument"""
    # arrange
    args = ["--command", "ignore"]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = timeout(parsed_args)

    # assert
    assert actual == DEFAULT_TIMEOUT
