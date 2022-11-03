import json


def command_rpc(command_id: int, sbt_command: str) -> str:
    rpc_body = _body(command_id, f"reload;{sbt_command}")
    bsp_header = _header(len(rpc_body) + 2)
    return bsp_header + "\r\n" + rpc_body + "\r\n"


def _header(length: int) -> str:
    return f"""Content-Type: application/vscode-jsonrpc; charset=utf-8\r\n""" f"""Content-Length: {length}\r\n"""


def _body(command_id: int, sbt_command: str) -> str:
    return json.dumps(
        {"jsonrpc": "2.0", "id": command_id, "method": "sbt/exec", "params": {"commandLine": sbt_command}}
    )
