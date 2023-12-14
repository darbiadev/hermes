"""File actions."""

from dataclasses import asdict
from pathlib import Path

import pandas as pd
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
    records = client.parse_file(Path(file_path))
    pd.DataFrame([asdict(record) for record in records]).to_csv("test.csv")
