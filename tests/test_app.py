"""Testing the app"""

from typer.testing import CliRunner

from hermes.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app)
    assert result.stdout_bytes == 0
    assert result.stderr_bytes == 0
