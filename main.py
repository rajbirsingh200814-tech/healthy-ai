"""Main CLI entry point"""
import click
from src.commands.recommend import recommend
from src.commands.analyze import analyze
from src.commands.preferences import preferences, show_preferences
from src.commands.history import history, clear_history


@click.group()
def cli():
    """Healthy Food AI - Your personal nutrition assistant"""
    pass


# Recommendation commands
cli.add_command(recommend)
cli.add_command(analyze)

# Preference commands
cli.add_command(preferences, name='set-preferences')
cli.add_command(show_preferences, name='show-preferences')

# History commands
cli.add_command(history)
cli.add_command(clear_history, name='clear-history')


if __name__ == "__main__":
    cli()
