"""FastAPI server for Healthy Food AI"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
from src.ai.gemini_client import FoodAIClient
from src.models.database import get_db

load_dotenv()

app = FastAPI(
    title="Healthy Food AI API",
    description="AI-powered nutrition recommendation API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class RecommendationRequest(BaseModel):
    dietary_needs: str
    calories: int
    user_id: str = "default"


class AnalysisRequest(BaseModel):
    food_description: str


class PreferencesRequest(BaseModel):
    user_id: str = "default"
    dietary_needs: list
    target_calories: int
    allergies: list = []


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Healthy Food AI API is running"}


# Recommendation endpoints
@app.post("/api/recommend")
def get_recommendation(request: RecommendationRequest):
    """Get AI food recommendation"""
    try:
        ai_client = FoodAIClient()
        recommendation = ai_client.get_recommendation(
            request.dietary_needs,
            request.calories
        )
        
        # Save to MongoDB if connected
        db = get_db()
        db.save_recommendation(
            request.dietary_needs,
            request.calories,
            recommendation,
            request.user_id
        )
        
        return {
            "status": "success",
            "dietary_needs": request.dietary_needs,
            "calories": request.calories,
            "recommendation": recommendation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze")
def analyze_nutrition(request: AnalysisRequest):
    """Analyze nutritional content of food"""
    try:
        ai_client = FoodAIClient()
        analysis = ai_client.analyze_nutrition(request.food_description)
        
        return {
            "status": "success",
            "food": request.food_description,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# History endpoints
@app.get("/api/recommendations/{user_id}")
def get_user_recommendations(user_id: str, limit: int = 10):
    """Get user recommendation history"""
    try:
        db = get_db()
        recommendations = db.get_recommendations(user_id, limit)
        
        return {
            "status": "success",
            "user_id": user_id,
            "count": len(recommendations),
            "recommendations": [
                {
                    "id": str(r.get("_id")),
                    "dietary_needs": r.get("dietary_needs"),
                    "calories": r.get("calories"),
                    "recommendation": r.get("recommendation")[:100] + "..." if len(r.get("recommendation", "")) > 100 else r.get("recommendation"),
                    "timestamp": r.get("timestamp")
                }
                for r in recommendations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Preferences endpoints
@app.post("/api/preferences")
def save_preferences(request: PreferencesRequest):
    """Save user preferences"""
    try:
        db = get_db()
        success = db.save_preferences(
            request.user_id,
            request.dietary_needs,
            request.target_calories,
            request.allergies
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Preferences saved for {request.user_id}"
            }
        else:
            return {
                "status": "warning",
                "message": "Preferences saved locally (MongoDB not available)"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/preferences/{user_id}")
def get_user_preferences(user_id: str):
    """Get user preferences"""
    try:
        db = get_db()
        prefs = db.get_preferences(user_id)
        
        if not prefs:
            raise HTTPException(status_code=404, detail=f"No preferences found for {user_id}")
        
        return {
            "status": "success",
            "user_id": user_id,
            "dietary_needs": prefs.get("dietary_needs"),
            "target_calories": prefs.get("target_calories"),
            "allergies": prefs.get("allergies")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
