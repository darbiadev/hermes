"""File parser."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from logging import getLogger

from darbia.shipping.types import Address, BillingInfo, Package, Shipment
from darbia.shipping.types.models import BillToSelector

from hermes.config import Config

logger = getLogger(__name__)


@dataclass
class OutputRow:
    shipment_id: str = ""
    sender_company: str = ""
    sender_attention_to: str = ""
    sender_address1: str = ""
    sender_address2: str = ""
    sender_address3: str = ""
    sender_city: str = ""
    sender_state: str = ""
    sender_postal_code: str = ""
    sender_country: str = ""
    recipient_company: str = ""
    recipient_attention_to: str = ""
    recipient_address1: str = ""
    recipient_address2: str = ""
    recipient_address3: str = ""
    recipient_city: str = ""
    recipient_state: str = ""
    recipient_postal_code: str = ""
    recipient_country: str = ""
    recipient_phone: str = ""
    recipient_email: str = ""
    third_party_company: str = ""
    third_party_attention_to: str = ""
    third_party_address1: str = ""
    third_party_address2: str = ""
    third_party_address3: str = ""
    third_party_city: str = ""
    third_party_state: str = ""
    third_party_postal_code: str = ""
    third_party_country: str = ""
    third_party_account_number: str = ""
    bill_to: str = ""
    package_type: str = ""
    number_of_packages: str = ""
    weight: str = ""
    length: str = ""
    width: str = ""
    height: str = ""
    package_reference1: str = ""
    package_reference2: str = ""
    package_reference3: str = ""
    package_reference4: str = ""
    package_reference5: str = ""
    shipping_service: str = ""
    general_goods_description: str = ""
    invoice_currency: str = ""
    invoice_comments: str = ""
    goods_description: str = ""
    goods_country_origin: str = ""
    goods_quantity: str = ""
    goods_unit_of_measure: str = ""
    goods_price_per: str = ""


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


def parse_rows(config: Config, rows: list[dict[str, str | float]]) -> list[ImportedShipment]:
    """Parse rows."""
    keys = rows[0].keys()
    mapping = {_guess_column(key): key for key in keys}

    records = []
    for row in rows:
        address = Address(
            **{
                const.value: row.get(mapping.get(const))  # type: ignore[arg-type]
                for const in ADDRESS_COLUMNS
                if row.get(mapping.get(const)) is not None  # type: ignore[arg-type]
            },
        )
        shipment_id = row.get(mapping.get(Columns.REFERENCE))  # type: ignore[arg-type]

        imported_shipment = ImportedShipment(shipment_id=shipment_id, ship_to=address)

        items = {}
        if config.item_column_names is not None:
            for item_column_name in config.item_column_names:
                try:
                    items[item_column_name] = int(row.get(item_column_name))
                except ValueError:
                    msg = f"Invalid value for '{item_column_name}' in order '{shipment_id}'"
                    raise ValueError(msg) from None
                except TypeError:
                    msg = f"Column '{item_column_name}' not found for order '{shipment_id}'"
                    raise ValueError(msg) from None

        if len(items) > 0:
            imported_shipment.items = items

        records.append(imported_shipment)  # type: ignore[arg-type]

    return records


def shipment_from_parts(config: Config, imported_shipment: ImportedShipment) -> Shipment:
    """Create a shipment from an imported shipment."""
    return Shipment(
        shipment_id=imported_shipment.shipment_id,
        ship_from=Address(**config.sender.model_dump()),
        ship_to=imported_shipment.ship_to,
        billing=BillingInfo(
            bill_to=BillToSelector.THIRD_PARTY,
            billing_account=config.third_party_account_number,
            billing_address=Address(**config.third_party.model_dump()),
        ),
        packages=[
            Package(
                weight=1.0,
                length=1.0,
                width=1.0,
                height=1.0,
                reference1=imported_shipment.shipment_id,
            ),
            Package(
                weight=1.0,
                length=2.0,
                width=3.0,
                height=4.0,
                reference1=f"{imported_shipment.shipment_id}  (2)",
            ),
        ],
    )


def shipment_to_output_rows(shipment: Shipment) -> list[OutputRow]:
    """Convert a shipment to an output row."""
    rows = []

    columns = {
        "shipment_id": shipment.shipment_id,
        "third_party_account_number": shipment.billing.billing_account,
        "bill_to": shipment.billing.bill_to.value,
        "package_type": "Package",
    }

    for key, value in asdict(shipment.ship_from).items():
        columns[f"sender_{key}"] = value
    for key, value in asdict(shipment.ship_to).items():
        columns[f"recipient_{key}"] = value
    for key, value in asdict(shipment.billing.billing_address).items():
        columns[f"third_party_{key}"] = value

    for package in shipment.packages:
        columns["weight"] = package.weight
        columns["length"] = package.length
        columns["width"] = package.width
        columns["height"] = package.height
        columns["package_reference1"] = package.reference1
        columns["package_reference2"] = package.reference2
        columns["package_reference3"] = package.reference3
        columns["package_reference4"] = package.reference4
        columns["package_reference5"] = package.reference5

        rows.append(OutputRow(**columns))

    return rows
