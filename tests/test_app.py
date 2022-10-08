"""Testing the app"""

from typer.testing import CliRunner

from hermes.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0
