# Deployment Guides

## Quick Start with Docker

### Local Development
```bash
# Build and run with Docker Compose
docker-compose up --build

# Server runs at http://localhost:8000
# MongoDB runs at localhost:27017
```

### Production with Docker
```bash
# Build image
docker build -t healthy-food-ai:latest .

# Run with environment variables
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e MONGODB_URI=production_mongodb_uri \
  healthy-food-ai:latest
```

---

## Deploy to Heroku

### Prerequisites
- Heroku CLI installed
- Heroku account
- GitHub account

### Steps

1. **Create Heroku app**
```bash
heroku login
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set GEMINI_API_KEY=your_key
heroku config:set MONGODB_URI=your_mongodb_uri
```

3. **Deploy from GitHub**
```bash
git push heroku main
```

4. **View logs**
```bash
heroku logs --tail
```

5. **Access your app**
```
https://your-app-name.herokuapp.com
```

**Procfile** should contain:
```
web: gunicorn src.api.server:app
```

Install gunicorn:
```bash
pip install gunicorn
```

---

## Deploy to Railway

### Prerequisites
- Railway account
- GitHub account connected to Railway

### Steps

1. **Connect GitHub repo**
   - Go to https://railway.app/
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Set environment variables**
   - Go to Variables tab
   - Add `GEMINI_API_KEY`
   - Add `MONGODB_URI` (optional, use Railway MongoDB)

3. **Add MongoDB (optional)**
   - Click "+ Add" → "Database" → "MongoDB"
   - Railway auto-connects with `MONGODB_URI`

4. **Deploy**
   - Railway auto-deploys on push to main
   - View logs in Railway dashboard

5. **Access your app**
```
https://your-project.up.railway.app
```

---

## Deploy to Render

### Prerequisites
- Render account
- GitHub account

### Steps

1. **Create new service**
   - Go to https://render.com/
   - Click "New+" → "Web Service"
   - Connect GitHub repo

2. **Configure**
   - Runtime: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.api.server:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables**
   - Add `GEMINI_API_KEY`
   - Add `MONGODB_URI`

4. **Deploy MongoDB (optional)**
   - Use MongoDB Atlas cloud database
   - Add connection string to `MONGODB_URI`

5. **Deploy**
   - Render auto-deploys on push
   - View logs in dashboard

---

## Deploy to AWS

### Using Elastic Container Service (ECS)

1. **Push Docker image to ECR**
```bash
aws configure
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag healthy-food-ai:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/healthy-food-ai:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/healthy-food-ai:latest
```

2. **Create ECS cluster and service**
   - Use AWS Management Console
   - Create cluster → Create service
   - Use pushed ECR image

3. **Set up RDS MongoDB alternative (DocumentDB or use Atlas)**
   - Configure security groups
   - Set connection string in environment

4. **Access via Load Balancer**
   - Configure Target Group
   - Get Load Balancer DNS

---

## Deploy to DigitalOcean App Platform

1. **Connect GitHub**
   - Go to DigitalOcean
   - Click "Create" → "Apps"
   - Connect GitHub account

2. **Configure**
   - Select repository
   - DigitalOcean auto-detects Dockerfile
   - Set HTTP port to 8000

3. **Add environment variables**
   - Add `GEMINI_API_KEY`
   - Add `MONGODB_URI`

4. **Deploy**
   - Click "Deploy"
   - Get app URL

---

## Environment Variables Required for All Platforms

```
GEMINI_API_KEY=your_google_gemini_api_key
MONGODB_URI=mongodb://user:pass@host:port/db  # Optional
MONGODB_DB_NAME=healthy_food_ai
DEBUG=false  # Set to True only in development
LOG_LEVEL=INFO
```

---

## Health Checks and Monitoring

### Health Check Endpoint
```bash
curl https://your-app.com/health
```

Response:
```json
{"status": "ok", "message": "Healthy Food AI API is running"}
```

### Monitoring Setup

**For Render/Railway/Heroku:**
- Built-in logs and monitoring
- Set alerts in dashboard

**For Docker/self-hosted:**
- Use Prometheus for metrics
- Use ELK Stack for logging
- Set up Grafana dashboards

---

## Database Setup for Production

### MongoDB Atlas (Cloud - Recommended)

1. **Create account** at https://www.mongodb.com/cloud/atlas
2. **Create cluster** (Free tier available)
3. **Create database user**
4. **Get connection string**:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/healthy_food_ai?retryWrites=true
   ```
5. **Set as `MONGODB_URI` environment variable**

### Self-Hosted MongoDB

```bash
# Docker
docker run -d -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=healthy_food_ai \
  mongo:latest

# Connect
MONGODB_URI=mongodb://localhost:27017/healthy_food_ai
```

---

## CI/CD Pipeline

GitHub Actions automatically runs:
- ✅ Tests on every push
- ✅ Code linting
- ✅ Coverage reports
- ✅ Docker build and push (on merge to main)

View workflow status: `.github/workflows/`

---

## Troubleshooting

### MongoDB Connection Issues
```
Error: Connection timeout
Solution: 
  1. Check URI is correct
  2. Whitelist IP in MongoDB Atlas
  3. Verify credentials
```

### API Returns 401 on requests
```
Error: Invalid or expired token
Solution:
  1. Generate new API token via user endpoint
  2. Include token in Authorization header
```

### High Memory Usage
```
Error: Out of memory
Solution:
  1. Increase container memory
  2. Clear cache: DELETE /api/cache
  3. Use pagination for large queries
```

---

## Scaling Recommendations

- **Low traffic (< 1K req/day)**: Railway/Render free tier
- **Medium traffic (1K-10K req/day)**: Railway Pro or Render Standard
- **High traffic (> 10K req/day)**: AWS ECS or DigitalOcean App Platform

Use Redis for caching at scale:
```python
# Upgrade from in-memory cache to Redis
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

---

## Support & Documentation

- API Docs: `/docs` (Swagger)
- Alternative Docs: `/redoc`
- GitHub Issues: Report bugs
- Email: support@healthyfoodai.com
