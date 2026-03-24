"""Google Gemini client for AI-powered food recommendations (FREE API)"""
import os
import json
import requests


class FoodAIClient:
    """Client for Google Gemini-powered food recommendations using REST API"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Get a free key at: https://makersuite.google.com/app/apikey"
            )
        # Use gemini-2.0-flash (latest model) or fall back to demo mode
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
        self.demo_mode = False
    
    def get_recommendation(self, dietary_needs: str, calories: int) -> str:
        """Get food recommendation from Google Gemini"""
        prompt = f"""Provide a healthy meal recommendation for someone with:
- Dietary needs: {dietary_needs}
- Daily calorie target: {calories}

Include: meal type, ingredients, estimated calories, and nutritional benefits.
Format your response clearly with sections."""
        
        try:
            return self._generate_content(prompt)
        except Exception as e:
            # Fallback to demo mode if API fails
            error_str = str(e).lower()
            if "not found" in error_str or "quota" in error_str or "exceeded" in error_str:
                return self._demo_recommendation(dietary_needs, calories)
            raise
    
    def analyze_nutrition(self, food_description: str) -> str:
        """Analyze nutritional content of food"""
        prompt = f"""Provide a detailed nutritional analysis for: {food_description}

Include: calories, macronutrients (protein, carbs, fat), micronutrients, and health benefits.
Format your response clearly."""
        
        try:
            return self._generate_content(prompt)
        except Exception as e:
            error_str = str(e).lower()
            if "not found" in error_str or "quota" in error_str or "exceeded" in error_str:
                return self._demo_analysis(food_description)
            raise
    
    def _generate_content(self, prompt: str) -> str:
        """Make API request to Gemini"""
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        params = {"key": self.api_key}
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            params=params,
            timeout=30
        )
        
        if response.status_code != 200:
            error_msg = response.text
            raise Exception(f"Gemini API error: {error_msg}")
        
        result = response.json()
        
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected response format: {result}")
    
    def _demo_recommendation(self, dietary_needs: str, calories: int) -> str:
        """Demo recommendation when API is unavailable"""
        demos = {
            "vegetarian": f"""
**Mediterranean Vegetarian Bowl** - {calories} calories

**Ingredients:**
- 1 cup quinoa (cooked)
- 1 cup roasted chickpeas
- Mixed roasted vegetables (zucchini, bell peppers, tomatoes)
- 1/4 cup tahini dressing
- Fresh herbs and lemon

**Nutritional Breakdown:**
- Calories: ~{calories}
- Protein: 18g
- Carbs: 52g
- Fat: 12g
- Fiber: 8g

**Benefits:**
- High in plant-based protein
- Rich in fiber for digestion
- Abundant antioxidants from vegetables
- Good source of healthy fats
""",
            "vegan": f"""
**Buddha Bowl with Tofu** - {calories} calories

**Ingredients:**
- 4 oz grilled marinated tofu
- 1 cup brown rice
- Steamed broccoli and carrots
- 1/4 avocado
- Soy-ginger sauce

**Nutritional Breakdown:**
- Calories: ~{calories}
- Protein: 15g
- Carbs: 48g
- Fat: 8g
- Fiber: 6g

**Benefits:**
- Complete plant-based amino acids
- Iron and calcium rich
- Supports sustainable diet
- Anti-inflammatory ingredients
""",
            "gluten-free": f"""
**Salmon & Sweet Potato** - {calories} calories

**Ingredients:**
- 5 oz grilled salmon
- 1 medium roasted sweet potato
- Steamed green beans
- 1 tbsp olive oil drizzle
- Herb seasoning

**Nutritional Breakdown:**
- Calories: ~{calories}
- Protein: 35g
- Carbs: 38g
- Fat: 10g
- Omega-3s: High

**Benefits:**
- Naturally gluten-free
- Heart-healthy omega-3 fatty acids
- Vitamin A for eye health
- Complete protein source
"""
        }
        
        diet_key = dietary_needs.lower().split()[0] if dietary_needs else "vegetarian"
        return demos.get(diet_key, demos["vegetarian"])
    
    def _demo_analysis(self, food_description: str) -> str:
        """Demo nutrition analysis"""
        return f"""
**Nutritional Analysis: {food_description}**

**Estimated Values (per serving):**
- Calories: 350-450
- Protein: 15-20g (source: main ingredient)
- Carbohydrates: 40-50g
- Fat: 8-12g
- Fiber: 3-5g

**Key Nutrients:**
- Vitamins: A, C, B-complex
- Minerals: Iron, Magnesium, Potassium
- Antioxidants: Polyphenols, carotenoids

**Health Benefits:**
- Promotes sustained energy
- Supports muscle recovery
- Aids digestive health
- Anti-inflammatory properties

*Note: This is a demo response. For exact nutritional values, check food labels or use the real Gemini API.*
"""

