"""
Loads configuration from environment variables and `.env` files.

By default, the values defined in the classes are used.
They can be overridden by an env var with the same name.

An `.env` file is used to populate env vars, if present.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    """Our default configuration for models that should load from .env files."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


class _UPS(EnvConfig, env_prefix="ups_"):
    """UPS auth."""

    base_url: str = ""
    username: str = ""
    password: str = ""
    access_license_number: str = ""


UPS = _UPS()
