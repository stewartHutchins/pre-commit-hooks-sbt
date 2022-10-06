from pre_commit_sbt.args.parse_args import arg_parser
from pre_commit_sbt.args.parse_args import sbt_command


def test_sbt_command() -> None:
    """Test should get the --command argument"""
    # arrange
    expected = "sample_command"
    args = ["--command", expected]

    # act
    parser = arg_parser()
    parsed_args = parser.parse_args(args)
    actual = sbt_command(parsed_args)

    # assert
    assert actual == expected
