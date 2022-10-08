"""An automated shipping client"""

from darbiadev_shipping import ShippingServices
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Settings for the application."""

    ups_base_url: str
    ups_username: str
    ups_password: str
    ups_access_license_number: str


def get_shipping_client() -> ShippingServices:
    """Build an authenticated shipping client."""

    settings = Settings()
    return ShippingServices(
        ups_auth={
            "base_url": settings.ups_base_url,
            "username": settings.ups_username,
            "password": settings.ups_password,
            "access_license_number": settings.ups_access_license_number,
        },
    )
