"""UPS actions."""

import typer

from hermes._shipping_client import get_shipping_client

app = typer.Typer()


@app.callback()
def callback() -> None:
    """UPS actions."""


@app.command()
def track(tracking_number: str) -> None:
    """Track a tracking number."""
    client = get_shipping_client()
    typer.echo(client.track(tracking_number))
