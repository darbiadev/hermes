"""File parser."""

from dataclasses import dataclass, field
from enum import Enum
from logging import getLogger
from pathlib import Path

import pandas as pd
from darbia.shipping.types import Address  # type: ignore[import-untyped]

logger = getLogger(__name__)


@dataclass
class ImportedShipment:
    """A imported record from a file."""

    shipment_id: str
    ship_to: Address
    items: dict[str, int] = field(default_factory=dict)


class Columns(Enum):
    """Columns."""

    REFERENCE = "REFERENCE"
    COMPANY = "company"
    NAME = "attention_to"
    ADDRESS_1 = "address1"
    ADDRESS_2 = "address2"
    ADDRESS_3 = "address3"
    CITY = "city"
    STATE = "state"
    POSTAL_CODE = "postal_code"
    COUNTRY = "country"
    PHONE = "phone"
    EMAIL = "email"
    DISCARD = "DISCARD"


ADDRESS_COLUMNS = [
    Columns.COMPANY,
    Columns.NAME,
    Columns.ADDRESS_1,
    Columns.ADDRESS_2,
    Columns.ADDRESS_3,
    Columns.CITY,
    Columns.STATE,
    Columns.POSTAL_CODE,
    Columns.COUNTRY,
    Columns.PHONE,
    Columns.EMAIL,
]


def _guess_column(column_name: str) -> Columns | None:
    mapping = {
        "ordernumber": Columns.REFERENCE,
        "shipmentid": Columns.REFERENCE,
        "po#": Columns.REFERENCE,
        "company": Columns.COMPANY,
        "attention": Columns.NAME,
        "address1": Columns.ADDRESS_1,
        "streetaddress": Columns.ADDRESS_1,
        "address2": Columns.ADDRESS_2,
        "address3": Columns.ADDRESS_3,
        "city": Columns.CITY,
        "state": Columns.STATE,
        "postalcode": Columns.POSTAL_CODE,
        "zip": Columns.POSTAL_CODE,
        "country": Columns.COUNTRY,
        "unnamed:": Columns.DISCARD,
    }

    text = column_name.lower().replace(" ", "").replace("_", "")

    if len(text) == 0:
        return Columns.DISCARD

    if text in mapping:
        return mapping[text]

    return None


def get_file_contents(path: Path, sheet_name: str | None = None) -> list[dict]:
    """Get file contents."""
    if not path.exists():
        msg = f"File {path} does not exist"
        raise FileNotFoundError(msg)

    if path.suffix == ".xlsx":
        sheets = pd.read_excel(io=path, sheet_name=sheet_name)
        if len(sheets) > 1:
            msg = f"File {path} has more than one sheet, please specify a sheet name"
            raise ValueError(msg)
        data = next(iter(sheets.values()))  # type: ignore[operator] # false positive?

    elif path.suffix == ".csv":
        data = pd.read_csv(path)

    else:
        msg = f"File type {path.suffix} is not supported"
        raise ValueError(msg)

    return data.fillna("").to_dict(orient="records")


def parse_file(path: Path, sheet_name: str | None = None) -> list[ImportedShipment]:
    """Parse file."""
    rows = get_file_contents(path, sheet_name)

    keys = rows[0].keys()
    mapping = {_guess_column(key): key for key in keys}

    records = []
    for row in rows:
        address = Address(
            **{
                const.value: row.get(mapping.get(const))
                for const in ADDRESS_COLUMNS
                if row.get(mapping.get(const)) is not None
            },
        )
        shipment_id = row.get(mapping.get(Columns.REFERENCE))
        records.append(ImportedShipment(shipment_id=shipment_id, ship_to=address))  # type: ignore[arg-type]
    return records
