"""Hermes."""

from pathlib import Path
from typing import Self

from hermes.config import Config
from hermes.files import get_config_file_contents, get_data_file_contents

from .parser import OutputRow, parse_rows, shipment_from_parts, shipment_to_output_rows


class Hermes:
    """Hermes."""

    def __init__(self: Self) -> None: ...

    def parse_file(self: Self, config_file: Path, data_file: Path) -> list[OutputRow]:
        """Parse file."""
        config_data = get_config_file_contents(config_file)
        config = Config(**config_data)  # type: ignore[arg-type]
        raw_rows = get_data_file_contents(data_file)
        shipments = [shipment_from_parts(config, row) for row in parse_rows(config, raw_rows)]
        rows = []
        for shipment in shipments:
            rows.extend(shipment_to_output_rows(shipment))
        return rows
