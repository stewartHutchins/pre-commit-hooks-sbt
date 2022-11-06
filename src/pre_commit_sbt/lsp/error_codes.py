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


def error_code_to_human_readable(error_code: int) -> str:
    """
    Convert an error code to a more human-readable reason for the error, as defined by:
    https://github.com/sbt/sbt/blob/1.8.x/protocol/src/main/scala/sbt/internal/langserver/ErrorCodes.scala
    :param error_code: The error code
    :return: A human-readable reason for the error.
    """
    return _EXIT_CODES.get(error_code, "Unknown error code, please raise an issue.")
