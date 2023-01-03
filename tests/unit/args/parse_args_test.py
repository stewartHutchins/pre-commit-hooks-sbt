import pytest

from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import files
from pre_commit_sbt.args.parse_args import sbt_command


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
