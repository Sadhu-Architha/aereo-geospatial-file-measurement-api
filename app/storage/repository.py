from typing import Any


files_store: dict[str, dict[str, Any]] = {}


def save_file(file_id: str, data: dict[str, Any]) -> None:
    files_store[file_id] = data


def get_file(file_id: str) -> dict[str, Any] | None:
    return files_store.get(file_id)