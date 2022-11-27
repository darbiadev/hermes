"""Standalone "quick" actions"""

import typer

from hermes import get_shipping_client

app = typer.Typer()


@app.callback()
def callback():
    """Quick actions"""


@app.command()
def track(tracking_number: str):
    """Track a tracking number"""
    client = get_shipping_client()
    typer.echo(client.track(tracking_number))
