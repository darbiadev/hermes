"""File actions."""

from pathlib import Path

import typer
from pydantic import ValidationError
from rich import print

from hermes import Hermes
from hermes.files import rows_to_file

app = typer.Typer()


@app.callback()
def callback() -> None:
    """File actions."""


@app.command()
def load_customer_file(config_file: str, data_file: str) -> None:
    """Load a customer file."""
    try:
        client = Hermes()
        records = client.parse_file(Path(config_file), Path(data_file))
        rows_to_file(records)
    except (FileNotFoundError, ValidationError, ValueError) as error:
        print(f"[bold red]{error}[/bold red]")
        raise typer.Exit(code=1)  # noqa: B904,TRY200
