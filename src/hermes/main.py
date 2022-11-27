"""CLI app definition"""

import typer

from . import get_shipping_client
from .quick_actions import app as quick_actions_app

app = typer.Typer()
app.add_typer(quick_actions_app, name="quick")


@app.callback()
def callback():
    """Automated shipping tooling"""


@app.command()
def track(tracking_number: str):
    """Track a tracking number"""
    client = get_shipping_client()
    typer.echo(client.track(tracking_number))
