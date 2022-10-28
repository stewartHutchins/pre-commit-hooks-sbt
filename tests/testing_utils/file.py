from pathlib import Path


def write_to_file(file: Path, text: str) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)


def read_file(file: Path) -> str:
    with open(file, "r", encoding="utf-8") as f:
        return f.read()
