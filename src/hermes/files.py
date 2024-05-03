"""Handle file related operations."""

import tomllib
from pathlib import Path

import pandas as pd

from hermes.parser import OutputRow


def get_config_file_contents(path: Path) -> dict[str, str | bool | float]:
    """Get config contents."""
    if not path.exists():
        msg = f"File '{path}' does not exist"
        raise FileNotFoundError(msg)
    if path.suffix != ".toml":
        msg = f"Config files must be of type '.toml', not '{path.suffix}'"
        raise ValueError(msg)
    return tomllib.loads(path.read_text())


def get_data_file_contents(path: Path, sheet_name: str | None = None) -> list[dict[str, str | float]]:
    """Get file contents."""
    if not path.exists():
        msg = f"File {path} does not exist"
        raise FileNotFoundError(msg)

    if path.suffix == ".xlsx":
        sheets = pd.read_excel(io=path, sheet_name=sheet_name)
        if len(sheets) > 1:
            msg = f"File '{path}' has more than one sheet, please specify a sheet name"
            raise ValueError(msg)
        data = next(iter(sheets.values()))  # type: ignore[operator] # false positive?

    elif path.suffix == ".csv":
        data = pd.read_csv(path)

    else:
        msg = f"File type '{path.suffix}' is not supported, please use '.csv' or '.xlsx'"
        raise ValueError(msg)

    return data.fillna("").to_dict(orient="records")  # type: ignore[return-value]


def rows_to_file(rows: list[OutputRow]) -> None:
    """Write rows to file."""
    pd.DataFrame(rows).to_csv("output.csv", index=False)
