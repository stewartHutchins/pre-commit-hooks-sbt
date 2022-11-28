import socket
from pathlib import Path


def connect_to_sbt_server(socket_file: Path) -> socket.socket:
    """
    Create a connection to a unix socket
    :param socket_file: The path to the socket
    :return: A socket connection
    """
    sbt_connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sbt_connection.connect(str(socket_file))
    return sbt_connection
