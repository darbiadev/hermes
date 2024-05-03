"""Configuration for Hermes."""

from pydantic import BaseModel


class Address(BaseModel):
    """Address."""

    company: str
    attention_to: str
    address1: str
    address2: str
    address3: str
    city: str
    state: str
    postal_code: str
    country: str


class ThirdParty(BaseModel):
    """Third Party."""

    account_number: str
    address: Address


class Config(BaseModel):
    """Configuration for Hermes."""

    sender: Address
    third_party: ThirdParty

    item_column_names: list[str] = None  # type: ignore[assignment]
