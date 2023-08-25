"""CLI app definition."""

import typer

from hermes.client import get_shipping_client

from .ups import app as ups_app

app = typer.Typer()
app.add_typer(ups_app, name="ups")


@app.callback()
def callback() -> None:
    """Shipping tooling."""


@app.command()
def track(tracking_number: str) -> None:
    """Track a tracking number."""
    client = get_shipping_client()
    typer.echo(client.track(tracking_number))
