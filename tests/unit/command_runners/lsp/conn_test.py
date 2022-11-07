import socket
from pathlib import Path

from pre_commit_sbt.command_runners.lsp.conn import connect_to_sbt_server


def test_connect_to_sbt_server(tmp_path: Path) -> None:
    """connect_to_sbt_server, should connect to an existing socket"""
    # arrange & act
    sock_file = tmp_path.joinpath("socket.sock")
    with (_create_listening_socket(sock_file) as sock_listen, connect_to_sbt_server(sock_file) as sock_under_test):
        expected = "sample text"
        conn, _ = sock_listen.accept()
        sock_under_test.send(expected.encode("UTF-8"))

        # assert
        actual = conn.recv(len(expected)).decode("UTF-8")
        assert actual == expected


def _create_listening_socket(path: Path) -> socket.socket:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(path))
    sock.listen()
    return sock
