"""Configuration for Hermes."""

from pydantic import BaseModel


class Address(BaseModel):
    company: str
    attention_to: str
    address1: str
    address2: str
    address3: str
    city: str
    state: str
    postal_code: str
    country: str


class Config(BaseModel):
    """Configuration for Hermes."""

    sender: Address
    third_party: Address
    third_party_account_number: str

    item_column_names: list[str] = None  # type: ignore[assignment]
