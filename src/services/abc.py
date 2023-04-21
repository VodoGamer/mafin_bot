from pathlib import Path


def read_query(file_name: str) -> str:
    with open(Path("src/services/queries", file_name), "r") as f:
        text = f.read()
    return text
