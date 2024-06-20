"""CLI app definition."""

import typer

from .files import app as files_app

app = typer.Typer()
app.add_typer(files_app, name="files")


@app.callback()
def callback() -> None:
    """Shipping tooling."""
