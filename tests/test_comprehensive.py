"""Comprehensive test suite for Healthy Food AI"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.ai.gemini_client import FoodAIClient
from src.models.database import MongoDB
from src.api.server import app
from fastapi.testclient import TestClient


# ===== Fixtures =====
@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_gemini():
    """Mock Gemini API client"""
    with patch('src.ai.gemini_client.requests.post') as mock:
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Test recommendation"}]
                }
            }]
        }
        yield mock


# ===== AI Client Tests =====
class TestFoodAIClient:
    """Tests for FoodAIClient"""
    
    def test_init_missing_api_key(self):
        """Test initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError):
                FoodAIClient()
    
    def test_get_recommendation(self, mock_gemini):
        """Test getting a recommendation"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            client = FoodAIClient()
            result = client.get_recommendation("vegetarian", 2000)
            assert "Test recommendation" in result
    
    def test_analyze_nutrition(self, mock_gemini):
        """Test nutritional analysis"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            client = FoodAIClient()
            result = client.analyze_nutrition("grilled chicken")
            assert "Test recommendation" in result
    
    def test_demo_recommendation_fallback(self):
        """Test demo mode fallback"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            client = FoodAIClient()
            result = client._demo_recommendation("vegetarian", 2000)
            assert "Mediterranean Vegetarian Bowl" in result or "Buddha Bowl" in result


# ===== Database Tests =====
class TestMongoDB:
    """Tests for MongoDB operations"""
    
    def test_db_init_no_connection(self):
        """Test MongoDB initialization with no connection"""
        with patch('src.models.database.MongoClient') as mock_client:
            mock_client.return_value.admin.command.side_effect = Exception("Connection failed")
            db = MongoDB()
            assert not db.is_connected()
    
    def test_save_recommendation_offline(self):
        """Test saving recommendation when DB is offline"""
        with patch('src.models.database.MongoClient') as mock_client:
            mock_client.return_value.admin.command.side_effect = Exception("Connection failed")
            db = MongoDB()
            result = db.save_recommendation("vegan", 1500, "test recommendation")
            assert result is False
    
    def test_get_recommendations_empty(self):
        """Test getting recommendations when none exist"""
        with patch('src.models.database.MongoClient') as mock_client:
            mock_client.return_value.admin.command.side_effect = Exception("Connection failed")
            db = MongoDB()
            results = db.get_recommendations("test-user")
            assert results == []


# ===== API Endpoint Tests =====
class TestAPIEndpoints:
    """Tests for FastAPI endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_recommend_endpoint(self, client, mock_gemini):
        """Test recommendation endpoint"""
        response = client.post("/api/recommend", json={
            "dietary_needs": "vegetarian",
            "calories": 2000,
            "user_id": "test-user"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_analyze_endpoint(self, client, mock_gemini):
        """Test nutrition analysis endpoint"""
        response = client.post("/api/analyze", json={
            "food_description": "grilled salmon"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_preferences_endpoint(self, client):
        """Test preferences endpoint"""
        response = client.post("/api/preferences", json={
            "user_id": "test-user",
            "dietary_needs": ["vegetarian"],
            "target_calories": 2000,
            "allergies": []
        })
        # Will succeed or warn depending on DB availability
        assert response.status_code == 200
    
    def test_invalid_request(self, client):
        """Test invalid request handling"""
        response = client.post("/api/recommend", json={
            "dietary_needs": "vegetarian"
            # Missing calories
        })
        assert response.status_code == 422  # Validation error


# ===== Input Validation Tests =====
class TestInputValidation:
    """Tests for input validation"""
    
    def test_negative_calories(self, client):
        """Test negative calories validation"""
        response = client.post("/api/recommend", json={
            "dietary_needs": "vegan",
            "calories": -100
        })
        assert response.status_code == 422
    
    def test_empty_dietary_needs(self, client):
        """Test empty dietary needs"""
        response = client.post("/api/recommend", json={
            "dietary_needs": "",
            "calories": 2000
        })
        assert response.status_code == 422
    
    def test_max_calories(self, client):
        """Test extremely high calories"""
        response = client.post("/api/recommend", json={
            "dietary_needs": "vegan",
            "calories": 999999
        })
        # Should still work, just unusual
        assert response.status_code in [200, 422]


# ===== Integration Tests =====
class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow_cli(self):
        """Test full CLI workflow"""
        from click.testing import CliRunner
        from main import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'recommend' in result.output
        assert 'analyze' in result.output
        assert 'history' in result.output
    
    def test_recommendation_and_history(self, client):
        """Test recommendation followed by history retrieval"""
        # Make recommendation
        rec_response = client.post("/api/recommend", json={
            "dietary_needs": "gluten-free",
            "calories": 1800,
            "user_id": "test-user-2"
        })
        assert rec_response.status_code == 200
        
        # Later, get history (may be empty if DB offline)
        hist_response = client.get("/api/recommendations/test-user-2")
        assert hist_response.status_code in [200, 404]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src"])
