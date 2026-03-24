# API Endpoints Guide

## Health Check
- `GET /health` - Server health status

## Recommendations
- `POST /api/recommend` - Get AI food recommendation
  ```json
  {
    "dietary_needs": "vegetarian",
    "calories": 2000,
    "user_id": "default"
  }
  ```

- `GET /api/recommendations/{user_id}` - Get recommendation history
  - Query params: `limit` (default: 10)

## Food Analysis
- `POST /api/analyze` - Analyze nutritional content
  ```json
  {
    "food_description": "grilled salmon with vegetables"
  }
  ```

## User Preferences
- `POST /api/preferences` - Save user preferences
  ```json
  {
    "user_id": "default",
    "dietary_needs": ["vegetarian", "gluten-free"],
    "target_calories": 2000,
    "allergies": []
  }
  ```

- `GET /api/preferences/{user_id}` - Get user preferences

## Running the Server
```bash
python run_server.py
```

Server will run at: `http://localhost:8000`

API Docs: `http://localhost:8000/docs` (Swagger UI)
Alternative Docs: `http://localhost:8000/redoc` (ReDoc)
