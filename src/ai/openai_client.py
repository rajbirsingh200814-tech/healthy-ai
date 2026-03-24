"""OpenAI client for AI-powered food recommendations"""
import os
from openai import OpenAI


class FoodAIClient:
    """Client for OpenAI-powered food recommendations and analysis"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    def get_recommendation(self, dietary_needs: str, calories: int) -> str:
        """Get food recommendation from OpenAI"""
        prompt = f"""
        Provide a healthy meal recommendation for someone with:
        - Dietary needs: {dietary_needs}
        - Daily calorie target: {calories}
        
        Include: meal type, ingredients, estimated calories, and nutritional benefits.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    def analyze_nutrition(self, food_description: str) -> str:
        """Analyze nutritional content of food"""
        prompt = f"""
        Provide a detailed nutritional analysis for: {food_description}
        Include: calories, macronutrients, micronutrients, and health benefits.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        return response.choices[0].message.content
