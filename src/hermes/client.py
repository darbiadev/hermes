"""Hermes."""

from pathlib import Path
from typing import Self

from .file_parser import ImportedShipment, parse_file


class Hermes:
    """Hermes."""

    def __init__(self: Self) -> None:
        pass

    def parse_file(self: Self, path: Path) -> list[ImportedShipment]:  # noqa: PLR6301
        """Parse file."""
        return parse_file(path)
