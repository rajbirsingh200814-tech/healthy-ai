# Healthy Food AI 🥗

Your personal AI-powered nutrition assistant that provides personalized food recommendations and nutritional analysis using Google Gemini API and MongoDB.

## Features

### Core Functionality
- 🤖 **AI-powered food recommendations** - Based on dietary needs and calorie goals
- 📊 **Nutritional analysis** - Detailed breakdown of food nutrients
- 💾 **Recommendation history** - Track all your recommendations
- 👤 **User preferences** - Save dietary needs and allergies
- 🌐 **REST API** - FastAPI web server with full documentation
- 📱 **CLI interface** - Easy-to-use command-line tool
- 🗄️ **MongoDB integration** - Store recommendations and preferences (optional)

### Production Features
- 🔐 **Authentication & Authorization** - Token-based API security
- ⚡ **Rate Limiting** - Protect API from abuse (10 req/min default)
- 🚀 **Caching Layer** - In-memory cache with TTL for fast responses
- 📝 **Database Migrations** - Version-controlled schema management
- 🔍 **Comprehensive Logging** - Rotating log files with metrics collection
- 🧪 **Unit Tests** - 40+ test cases with >80% coverage
- 🐳 **Docker Support** - Production-ready containerization
- 🔄 **CI/CD Pipeline** - Automated testing and deployment
- 📡 **Monitoring** - Metrics tracking and performance monitoring

## Tech Stack

- **Language**: Python 3.10+
- **AI**: Google Gemini API (Free)
- **Web Framework**: FastAPI
- **Database**: MongoDB (optional)
- **CLI**: Click
- **Testing**: pytest with >80% coverage
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Security**: HTTPBearer authentication, slowapi rate limiting
- **Monitoring**: Rotating file logger with metrics collection

## Project Structure

```
healthy-food-ai/
├── src/
│   ├── commands/              # CLI commands
│   │   ├── recommend.py       # Get recommendations
│   │   ├── analyze.py         # Nutrition analysis
│   │   ├── preferences.py     # User preferences
│   │   └── history.py         # View history
│   ├── api/
│   │   └── server.py          # FastAPI server
│   ├── ai/
│   │   └── gemini_client.py   # AI integration
│   ├── models/
│   │   ├── food.py            # Pydantic data models
│   │   ├── database.py        # MongoDB operations
│   │   └── migrations.py      # Database migrations
│   ├── utils/
│   │   ├── logging_config.py  # Logging & metrics
│   │   ├── validation.py      # Request validation
│   │   └── caching.py         # Caching & rate limiting
│   ├── auth/
│   │   └── user_manager.py    # Token authentication
│   └── config/
│       └── settings.py        # Configuration
├── tests/
│   ├── test_main.py           # Basic CLI tests
│   └── test_comprehensive.py  # 40+ integration tests
├── .github/
│   └── workflows/
│       ├── tests.yml          # CI/CD testing
│       └── docker.yml         # Docker builds
├── main.py                    # CLI entry point
├── run_server.py              # Start FastAPI server
├── Dockerfile                 # Container definition
├── docker-compose.yml         # App + MongoDB orchestration
├── Procfile                   # Heroku configuration
├── railway.json               # Railway configuration
├── render.yaml                # Render configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── DEPLOYMENT.md             # Cloud deployment guides
├── API_GUIDE.md              # REST API reference
└── README.md
```

## Installation

### 1. Clone and Install

```bash
cd healthy-food-ai
python -m venv .venv
.venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy and edit .env
copy .env.example .env

# Add your Gemini API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_key_here

# Optional: MongoDB connection
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=healthy_food_ai
```

## Usage

### CLI Commands

```bash
# Get food recommendation
python main.py recommend --dietary-needs vegetarian --calories 2000

# Analyze nutrition of food
python main.py analyze "grilled chicken with rice"

# Save your preferences
python main.py set-preferences --username john --dietary-needs vegetarian --calories 2000

# View saved preferences
python main.py show-preferences

# View recommendation history
python main.py history

# Clear history
python main.py clear-history

# Show all commands
python main.py --help
```

### REST API

Start the server:
```bash
python run_server.py
```

Server runs at: `http://localhost:8000`

**API Documentation**:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Example API Calls**:

```bash
# Get recommendation
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"dietary_needs": "vegetarian", "calories": 2000}'

# Analyze food
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"food_description": "grilled salmon"}'

# Save preferences
curl -X POST "http://localhost:8000/api/preferences" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "john", "dietary_needs": ["vegetarian"], "target_calories": 2000}'

# Get history
curl "http://localhost:8000/api/recommendations/john"
```

## Database (MongoDB)

MongoDB is optional. If not installed, the app runs in demo/local file mode.

### With MongoDB:

```bash
# Install MongoDB locally or use MongoDB Atlas
# https://www.mongodb.com/docs/manual/installation/

# Configure in .env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=healthy_food_ai
```

### Without MongoDB:

- Preferences saved to `user_preferences.json`
- Recommendations saved to `recommendations_history.json`

## Testing

```bash
pytest -v
pytest --cov=src  # With coverage
```

## API Features

See [API_GUIDE.md](API_GUIDE.md) for comprehensive API documentation.

## Free Tier Limits

- **Google Gemini API**: 60 requests/minute (free tier)
- **Perfect for**: Testing, development, CV projects
- **No credit card needed**

## Deployment

### Quick Start with Docker

```bash
# Build and run with Docker Compose (includes MongoDB)
docker-compose up --build

# Server at http://localhost:8000
```

### Production Deployment

**See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive guides:**

- ✅ **Heroku** - Includes Procfile for Easy deployment
- ✅ **Railway** - Auto-deploy from GitHub with railway.json
- ✅ **Render** - Simple Docker-based deployment with render.yaml
- ✅ **AWS ECS** - Container orchestration on AWS
- ✅ **DigitalOcean** - App Platform deployment

**Quick Cloud Deploy:**
```bash
# Heroku
git push heroku main

# Railway
# Just connect GitHub repo (auto-deploys)

# Render
# Connect GitHub repo (auto-deploys with render.yaml)
```

## Production Ready Features

This project is production-ready with enterprise-grade features:

- ✅ **Comprehensive Tests** - 40+ test cases with mocking and integration tests
- ✅ **Docker Containerization** - Dockerfile with health checks, docker-compose with MongoDB
- ✅ **CI/CD Pipeline** - GitHub Actions testing on 3.10-3.12, code linting, Docker builds
- ✅ **Input Validation** - Pydantic validators for all API requests
- ✅ **Rate Limiting** - slowapi integration (10 req/min default)
- ✅ **Caching** - TTL-based in-memory cache (30min-1hr)
- ✅ **Database Migrations** - Version-controlled schema changes
- ✅ **Logging & Monitoring** - Rotating file logs with metrics collection
- ✅ **Authentication** - Token-based security with HTTPBearer
- ✅ **Multi-Platform Deployment** - Heroku, Railway, Render, AWS, DigitalOcean ready

## Next Steps

- [ ] Add diet tracking feature (weight, nutrition trends)
- [ ] Implement meal planning (weekly plans)
- [ ] Add mobile app (Flutter/React Native)
- [ ] Integrate Spoonacular API for recipe database
- [ ] Create admin dashboard
- [ ] Add email notifications
- [ ] Scale to Redis for distributed caching

## License

MIT

## Support

- Issues: GitHub Issues
- Email: health-ai@example.com
- Docs: See README and API_GUIDE.md
