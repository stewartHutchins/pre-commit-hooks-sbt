import socket
from pathlib import Path


def connect_to_sbt_server(socket_file: Path) -> socket.socket:
    sbt_connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sbt_connection.connect(str(socket_file))
    return sbt_connection
