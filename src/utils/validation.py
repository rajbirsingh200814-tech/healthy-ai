"""Input validation utilities"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List


class RecommendationRequest(BaseModel):
    """Validated recommendation request"""
    dietary_needs: str = Field(..., min_length=1, max_length=100)
    calories: int = Field(..., gt=0, le=10000)  # 0 to 10000 calories
    user_id: str = "default"
    
    @validator('dietary_needs')
    def validate_dietary_needs(cls, v):
        """Validate dietary needs"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Dietary needs cannot be empty")
        return v.strip().lower()


class AnalysisRequest(BaseModel):
    """Validated analysis request"""
    food_description: str = Field(..., min_length=1, max_length=500)
    
    @validator('food_description')
    def validate_food_description(cls, v):
        """Validate food description"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Food description cannot be empty")
        return v.strip()


class PreferencesRequest(BaseModel):
    """Validated preferences request"""
    user_id: str = Field(default="default", min_length=1, max_length=100)
    dietary_needs: List[str] = Field(..., min_items=1, max_items=10)
    target_calories: int = Field(..., gt=0, le=10000)
    allergies: List[str] = Field(default_factory=list, max_items=20)
    
    @validator('dietary_needs', pre=True)
    def validate_dietary_needs(cls, v):
        """Validate dietary needs list"""
        if isinstance(v, str):
            v = [x.strip() for x in v.split(',')]
        return [x.strip().lower() for x in v if x.strip()]
    
    @validator('allergies', pre=True)
    def validate_allergies(cls, v):
        """Validate allergies list"""
        if isinstance(v, str):
            v = [x.strip() for x in v.split(',')]
        return [x.strip().lower() for x in v if x.strip()]


class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = "error"
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None


class SuccessResponse(BaseModel):
    """Standard success response"""
    status: str = "success"
    data: dict
