from pathlib import Path

from pre_commit_sbt.lsp.port_file import connection_details
from pre_commit_sbt.lsp.port_file import port_path


def test_active_json_is_file(sbt_project_with_server: Path) -> None:
    """The port file of a running sbt server can be found"""

    # act
    port_file = port_path(sbt_project_with_server)

    # assert
    assert port_file.exists()


def test_active_json_is_not_file(sbt_project_without_server: Path) -> None:
    """The port file is not present if there is no running sbt server"""

    # act
    port_file = port_path(sbt_project_without_server)

    # assert
    assert not port_file.exists()


def test_connection_details_port_file_is_readable(sbt_project_with_server: Path) -> None:
    """The port file of a running sbt server can be read"""

    # arrange
    port_file = port_path(sbt_project_with_server)

    # act
    details: Path = connection_details(port_file.open("r"))

    # assert
    assert details.exists()
