"""Tests for main CLI"""
import pytest
from click.testing import CliRunner
from main import cli


@pytest.fixture
def runner():
    """CLI test runner"""
    return CliRunner()


def test_cli_help(runner):
    """Test CLI help command"""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Healthy Food AI' in result.output


def test_recommend_command(runner):
    """Test recommend command"""
    result = runner.invoke(cli, [
        'recommend',
        '--dietary-needs', 'vegetarian',
        '--calories', '2000'
    ])
    assert result.exit_code == 0
    assert 'recommendations' in result.output.lower()
