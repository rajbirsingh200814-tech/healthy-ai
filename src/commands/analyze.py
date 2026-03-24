"""Nutrition analysis CLI command"""
import sys
import click
from dotenv import load_dotenv
from src.ai.gemini_client import FoodAIClient

load_dotenv()


@click.command()
@click.argument('food_description')
def analyze(food_description: str):
    """Analyze nutritional content of food"""
    try:
        click.echo(f"\n[ANALYZING] Nutritional breakdown for: {food_description}\n")
        
        ai_client = FoodAIClient()
        analysis = ai_client.analyze_nutrition(food_description)
        
        click.echo("\n" + "="*60)
        click.echo("NUTRITIONAL ANALYSIS")
        click.echo("="*60)
        click.echo(analysis)
        click.echo("="*60 + "\n")
        
    except Exception as e:
        click.echo(f"\n[ERROR] Analysis failed: {str(e)}", err=True)
        sys.exit(1)
