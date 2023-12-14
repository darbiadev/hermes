"""CLI app definition."""

import typer

from .files import app as files_app
from .ups import app as ups_app

app = typer.Typer()
app.add_typer(files_app, name="files")
app.add_typer(ups_app, name="ups")


@app.callback()
def callback() -> None:
    """Shipping tooling."""
