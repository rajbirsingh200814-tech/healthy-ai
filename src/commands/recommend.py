"""Food recommendation CLI command"""
import click
import sys
from dotenv import load_dotenv
from src.ai.gemini_client import FoodAIClient
from src.commands.history import save_to_history

# Load environment variables from .env
load_dotenv()


@click.command()
@click.option('--dietary-needs', prompt='Your dietary needs', help='e.g., vegetarian, vegan, gluten-free')
@click.option('--calories', type=int, prompt='Target calories', help='Daily calorie goal')
def recommend(dietary_needs: str, calories: int):
    """Get personalized food recommendations using Google Gemini (FREE)"""
    try:
        click.echo(f"\n[SEARCHING] Getting recommendations for {dietary_needs} diet with {calories} calories...\n")
        
        # Initialize Gemini client
        ai_client = FoodAIClient()
        
        # Get recommendation from Gemini
        recommendation = ai_client.get_recommendation(dietary_needs, calories)
        
        click.echo("\n" + "="*60)
        click.echo("MEAL RECOMMENDATION")
        click.echo("="*60)
        click.echo(recommendation)
        click.echo("="*60 + "\n")
        
        # Save to history
        save_to_history(dietary_needs, calories, recommendation)
        click.echo("[OK] Saved to history. Run 'python main.py history' to view.\n")
        
    except Exception as e:
        click.echo(f"\n[ERROR] Failed to get recommendation: {str(e)}", err=True)
        click.echo("Make sure your Gemini API key is set in .env file", err=True)
        sys.exit(1)
