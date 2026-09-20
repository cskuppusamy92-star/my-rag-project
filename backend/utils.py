from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not exist."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_hash(path: str | Path) -> str:
    """Return SHA256 hash of a file."""
    path = Path(path)

    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def text_hash(text: str) -> str:
    """Return SHA256 hash of text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save_json(
    data: Any,
    path: str | Path,
) -> None:
    """Save Python data as JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def load_json(path: str | Path) -> Any:
    """Load JSON from a file."""
    path = Path(path)

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_text(text: str) -> str:
    """Normalize whitespace in text."""
    return " ".join(text.split())


def safe_filename(filename: str) -> str:
    """Create a filesystem-friendly filename."""
    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(char, "_")

    return filename.strip()