"""Food and nutrition data models"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Nutrition(BaseModel):
    """Nutritional information"""
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None


class Food(BaseModel):
    """Food item model"""
    id: Optional[str] = None
    name: str
    description: str
    nutrition: Nutrition
    dietary_tags: list[str] = []
    created_at: datetime = datetime.now()


class UserPreference(BaseModel):
    """User dietary preferences"""
    id: Optional[str] = None
    username: str
    dietary_needs: list[str]
    target_calories: int
    allergies: list[str] = []
    favorite_foods: list[str] = []
    created_at: datetime = datetime.now()
