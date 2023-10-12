from logging import Logger
from pathlib import Path

import pandas as pd

logger = Logger(__name__)


def get_file_contents(path: Path, sheet_name: str | None = None) -> list[dict]:
    if not path.exists():
        msg = f"File {path} does not exist"
        raise FileNotFoundError(msg)

    if path.suffix == ".xlsx":
        sheets = pd.read_excel(io=path, sheet_name=sheet_name)
        if len(sheets) > 1:
            msg = f"File {path} has more than one sheet, please specify a sheet name"
            raise ValueError(msg)
        data = sheets.values()[0]

    elif path.suffix == ".csv":
        data = pd.read_csv(io=path)

    else:
        msg = f"File type {path.suffix} is not supported"
        raise ValueError(msg)

    return data.fillna("").to_dict(orient="records")


def parse_file(path: Path, sheet_name: str | None = None) -> None:
    """Parse file."""
    logger.info(f"Parsing file {path}")
    contents = get_file_contents(path, sheet_name)
    logger.info(f"File {path} parsed successfully")
    return contents
