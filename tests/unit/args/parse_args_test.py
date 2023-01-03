import pytest

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import DEFAULT_LOG_LEVEL
from pre_commit_sbt.args.parse_args import DEFAULT_TIMEOUT
from pre_commit_sbt.args.parse_args import files
from pre_commit_sbt.args.parse_args import log_level
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
    """parser should raise an exception if the --command argument is missing"""
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
    """parser should get the default if the --timeout argument is missing"""
    # arrange
    args = ["--command", "ignore"]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = timeout(parsed_args)

    # assert
    assert actual == DEFAULT_TIMEOUT


def test_log_level() -> None:
    """parser should get the default if the --timeout argument is missing"""
    # arrange
    expected = "some log level"
    args = ["--command", "ignore", "--log-level", expected]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = log_level(parsed_args)

    # assert
    assert actual == expected


def test_log_level_default() -> None:
    """parser should get the default if the --timeout argument is missing"""
    # arrange
    args = ["--command", "ignore"]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = log_level(parsed_args)

    # assert
    assert actual == DEFAULT_LOG_LEVEL


@pytest.mark.parametrize("expected", [["file1", "file2", "file3"], []])
def test_files(expected: list[str]) -> None:
    """parser should get the files passed into the tool"""
    # arrange
    args = ["--command", "ignore"] + expected

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = files(parsed_args)

    # assert
    assert expected == actual
