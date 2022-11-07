from io import StringIO

from pre_commit_sbt.command_runners.lsp.port_file import connection_details


def test_connection_details() -> None:
    """connection_details should extract the socket's path from the json."""
    # arrange
    expected_path = "/path/to/socket"

    json_with_uri = f"""{{"uri": "local://{expected_path}"}}"""

    # act
    actual_path = connection_details(StringIO(json_with_uri))

    # assert
    assert expected_path == str(actual_path)
