import json
from asyncio import StreamReader
from typing import TypeAlias

JsonType: TypeAlias = dict[str, str | int | dict[str, object]]


class _HeaderKeys:  # pylint: disable=too-few-public-methods
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"


async def get_next_message(reader: StreamReader) -> JsonType:
    """
    Read the next message sent by SBT server
    :param reader: A stream reader connected to the socket
    :return: The next message
    """
    headers = _parse_headers(await _read_headers(reader))
    content_length: int = headers[_HeaderKeys.CONTENT_LENGTH]  # type: ignore
    body = _parse_body(await _read_body(content_length, reader))
    return body


def _parse_headers(headers: list[str]) -> JsonType:
    return dict(_parse_header(header) for header in headers)


def _parse_header(header: str) -> tuple[str, str | int]:
    match header.split(":"):
        case [_HeaderKeys.CONTENT_LENGTH as key, number]:
            return key, int(number.strip())
        case [key, value]:
            return key, value.strip()
        case _:
            raise ValueError("Not a header")


async def _read_headers(reader: StreamReader) -> list[str]:
    headers: list[str] = []
    while True:
        line = (await reader.readline()).decode("UTF-8")
        if line == "\r\n":
            break
        headers = headers + [line]
    return headers


async def _read_body(content_length: int, reader: StreamReader) -> str:
    return (await reader.readexactly(content_length)).decode("UTF-8")


def _parse_body(content: str) -> JsonType:
    body: JsonType = json.loads(content)
    return body


def is_completion_message(message: JsonType, task_id: int) -> bool:
    """
    Determine whether the message sent indicates whether the SBT command has
    completed
    :param message: A message from sbt server
    :param task_id: The task ID of the message
    :return: True if the message sent indicates completion of the command,
    else False
    """
    return message.get("id") == task_id


def error_message(completion_msg: JsonType) -> str:
    """
    Get the error message from the final response message
    :param completion_msg: The final response
    :return: The error message
    """
    return completion_msg["error"]["message"]  # type: ignore


def return_code(completion_msg: JsonType) -> int:
    """
    Get the return code from the final response message
    :param completion_msg: The final response
    :return: The return code
    """
    if "result" in completion_msg:  # pylint: disable=no-else-return
        return completion_msg["result"]["exitCode"]  # type: ignore
    else:
        return completion_msg["error"]["code"]  # type: ignore


_EXIT_CODES: dict[int, str] = {
    -32700: "ParseError - Invalid JSON.",
    -32600: "InvalidRequest - JSON was valid, but did not conform to specification.",
    -32601: "MethodNotFound - The method does not exist / is not available.",
    -32602: "InvalidParams - Invalid method parameter(s).",
    -32603: "InternalError - Internal JSON-RPC error.",
    -32099: "serverErrorStart",
    -32000: "serverErrorEnd",
    -32001: "UnknownServerError",
    -32002: "ServerNotInitialized - Request sent before the server was initialized.",
    -32800: "RequestCancelled - The request was cancelled.",
    -33000: "UnknownError - unspecified error, but this is probably a malformed or non-existent SBT command",
}


def error_code_to_human_readable(err_code: int) -> str:
    """
    Convert an error code to a more human-readable reason for the error, as defined by:
    https://github.com/sbt/sbt/blob/1.8.x/protocol/src/main/scala/sbt/internal/langserver/ErrorCodes.scala
    :param err_code: The error code
    :return: A human-readable reason for the error.
    """
    return _EXIT_CODES.get(err_code, "Unknown error code, please raise an issue.")
