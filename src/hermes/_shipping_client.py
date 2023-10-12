"""Shipping client."""

from darbiadev_shipping import ShippingServices

from .constants import UPS


def get_shipping_client() -> ShippingServices:
    """Build an authenticated shipping client."""
    return ShippingServices(
        ups_auth={
            "base_url": UPS.base_url,
            "username": UPS.username,
            "password": UPS.password,
            "access_license_number": UPS.access_license_number,
        },
    )
