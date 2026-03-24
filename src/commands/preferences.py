"""User preferences CLI command"""
import sys
import click
import json
from pathlib import Path

PREFS_FILE = Path("user_preferences.json")


@click.command()
@click.option('--username', prompt='Username', help='Your name')
@click.option('--dietary-needs', prompt='Dietary needs (comma-separated)', help='e.g., vegetarian, vegan, gluten-free')
@click.option('--calories', type=int, prompt='Target daily calories', help='e.g., 2000')
@click.option('--allergies', prompt='Allergies (comma-separated, or skip)', default='', help='e.g., nuts, dairy')
def preferences(username: str, dietary_needs: str, calories: int, allergies: str):
    """Save your dietary preferences"""
    try:
        prefs = {
            "username": username,
            "dietary_needs": [d.strip() for d in dietary_needs.split(',')],
            "target_calories": calories,
            "allergies": [a.strip() for a in allergies.split(',') if a.strip()] or []
        }
        
        with open(PREFS_FILE, 'w') as f:
            json.dump(prefs, f, indent=2)
        
        click.echo(f"\n[OK] Preferences saved for {username}!")
        click.echo(json.dumps(prefs, indent=2))
        
    except Exception as e:
        click.echo(f"\n[ERROR] Failed to save preferences: {str(e)}", err=True)
        sys.exit(1)


@click.command()
def show_preferences():
    """Show your saved preferences"""
    try:
        if not PREFS_FILE.exists():
            click.echo("\n[INFO] No preferences saved yet. Run 'preferences' command first.\n")
            return
        
        with open(PREFS_FILE) as f:
            prefs = json.load(f)
        
        click.echo("\n" + "="*60)
        click.echo("YOUR PREFERENCES")
        click.echo("="*60)
        click.echo(f"Username: {prefs['username']}")
        click.echo(f"Dietary needs: {', '.join(prefs['dietary_needs'])}")
        click.echo(f"Target calories: {prefs['target_calories']}")
        if prefs['allergies']:
            click.echo(f"Allergies: {', '.join(prefs['allergies'])}")
        click.echo("="*60 + "\n")
        
    except Exception as e:
        click.echo(f"\n[ERROR] Failed to load preferences: {str(e)}", err=True)
        sys.exit(1)
