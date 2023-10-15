"""File actions."""

from pathlib import Path

import typer

from hermes import Hermes

app = typer.Typer()


@app.callback()
def callback() -> None:
    """File actions."""


@app.command()
def load_customer_file(file_path: str) -> None:
    """Load a customer file."""
    client = Hermes()
    typer.echo(client.parse_file(Path(file_path)))
