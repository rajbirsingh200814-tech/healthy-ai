"""Recommendation history CLI command"""
import sys
import click
import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("recommendations_history.json")


def save_to_history(dietary_needs: str, calories: int, recommendation: str):
    """Save recommendation to history"""
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "dietary_needs": dietary_needs,
        "calories": calories,
        "recommendation": recommendation[:200] + "..." if len(recommendation) > 200 else recommendation
    }
    
    history.append(entry)
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


@click.command()
@click.option('--limit', type=int, default=5, help='Number of recommendations to show')
def history(limit: int):
    """View your recommendation history"""
    try:
        if not HISTORY_FILE.exists():
            click.echo("\n[INFO] No recommendation history yet.\n")
            return
        
        with open(HISTORY_FILE) as f:
            all_history = json.load(f)
        
        recent = all_history[-limit:] if limit else all_history
        recent.reverse()
        
        click.echo(f"\n{'='*60}")
        click.echo(f"RECENT RECOMMENDATIONS (Last {min(limit, len(all_history))})")
        click.echo(f"{'='*60}")
        
        for i, entry in enumerate(recent, 1):
            click.echo(f"\n[{i}] {entry['timestamp']}")
            click.echo(f"    Diet: {entry['dietary_needs']} | Calories: {entry['calories']}")
            click.echo(f"    Recommendation: {entry['recommendation']}")
        
        click.echo(f"\n{'='*60}\n")
        
    except Exception as e:
        click.echo(f"\n[ERROR] Failed to load history: {str(e)}", err=True)
        sys.exit(1)


@click.command()
def clear_history():
    """Clear recommendation history"""
    try:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
            click.echo("\n[OK] History cleared.\n")
        else:
            click.echo("\n[INFO] No history to clear.\n")
            
    except Exception as e:
        click.echo(f"\n[ERROR] Failed to clear history: {str(e)}", err=True)
        sys.exit(1)
