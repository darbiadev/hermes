"""Testing the app"""

from typer.testing import CliRunner

from hermes.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
