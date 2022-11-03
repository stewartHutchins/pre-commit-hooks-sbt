from __future__ import annotations

import json
from asyncio import StreamReader
from typing import AsyncIterable
from typing import TypeAlias

from pre_commit_sbt.err.error_msgs import COMMAND_FAILED
from pre_commit_sbt.err.failed_command_error import FailedCommandError

JsonType: TypeAlias = dict[str, str | int | dict[str, object]]


class _HeaderKeys:  # pylint: disable=too-few-public-methods
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"


async def read_until_complete_message(reader: StreamReader, task_id: int) -> JsonType:
    async for message in _message_iterator(reader):
        if _is_response_message(message, task_id):
            return message
    raise FailedCommandError(COMMAND_FAILED)


async def _message_iterator(reader: StreamReader) -> AsyncIterable[JsonType]:
    while not reader.at_eof():
        yield await _get_next_message(reader)


async def _get_next_message(reader: StreamReader) -> JsonType:
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


def _is_response_message(message: JsonType, task_id: int) -> bool:
    return message.get("id") == task_id
