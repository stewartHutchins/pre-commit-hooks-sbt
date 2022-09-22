def strip_margin(text: str) -> str:
    return "\n".join(line.lstrip().removeprefix("|") for line in text.splitlines())
