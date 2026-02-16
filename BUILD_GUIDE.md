# 🚀 ADFLOWAI - VS Code Build Guide

## 📋 Step-by-Step Instructions

Follow this guide to build ADFLOWAI in VS Code from scratch!

---

## ✅ Prerequisites

1. **Install Required Software:**
   - VS Code
   - Python 3.9+
   - Docker Desktop
   - Git
   - Node.js (for frontend, later)

2. **Create Project Folder:**
   ```bash
   mkdir ADFLOWAI
   cd ADFLOWAI
   code .
   ```

---

## 📁 Step 1: Create Folder Structure

In VS Code terminal, run:

```bash
# Create main directories
mkdir -p src/{core,models,ml,api,integrations,utils}
mkdir -p config docs scripts tests examples frontend

# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py
touch src/models/__init__.py
touch src/ml/__init__.py
touch src/api/__init__.py
touch src/integrations/__init__.py
touch src/utils/__init__.py
touch config/__init__.py
touch tests/__init__.py
```

Your structure should look like:
```
ADFLOWAI/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── ml/
│   │   └── __init__.py
│   ├── api/
│   │   └── __init__.py
│   ├── integrations/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── config/
│   └── __init__.py
├── docs/
├── scripts/
├── tests/
│   └── __init__.py
├── examples/
└── frontend/
```

---

## 📝 Step 2: Create Core Configuration Files

### 2.1: Create `requirements.txt`

```txt
# Core Framework
flask==3.0.0
flask-cors==4.0.0
flask-jwt-extended==4.6.0
gunicorn==21.2.0

# Database
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23
redis==5.0.1

# Machine Learning
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2

# Task Queue
celery==5.3.4

# Utilities
python-dotenv==1.0.0
requests==2.31.0
```

### 2.2: Create `.env.example`

```bash
# Application
APP_NAME=ADFLOWAI
SECRET_KEY=change-this-secret-key
JWT_SECRET_KEY=change-this-jwt-secret
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/adflowai

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (add your own)
GOOGLE_ADS_CLIENT_ID=your_client_id
FACEBOOK_APP_ID=your_app_id
LINKEDIN_CLIENT_ID=your_client_id
```

### 2.3: Create `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
venv/
env/

# Environment
.env

# IDE
.vscode/
.idea/

# Data
*.db
*.sqlite
models/*.pkl
uploads/
logs/
```

---

## 📝 Step 3: Create Database Models

### Create `src/models/campaign.py`

This file contains all database models. Copy the complete model code here.

**Key models:**
- Campaign
- PlatformCampaign  
- MetricsHistory
- User
- OptimizationLog

---

## 🤖 Step 4: Create AI/ML Engine

### Create `src/ml/optimizer.py`

This is the AI brain of your system!

**Key components:**
- `AIOptimizer` class
- `predict_performance()` - ML prediction
- `optimize_budget_allocation()` - Budget optimization
- `should_pause_campaign()` - Auto-pause logic

---

## 🔧 Step 5: Create Core Business Logic

### Create `src/core/database.py`

Database connection and session management.

### Create `src/core/campaign_manager.py`

Core campaign operations:
- Create campaigns
- Update metrics
- Run optimization
- Get analytics

---

## 🌐 Step 6: Create API Routes

### Create `src/api/routes.py`

RESTful API endpoints:
```python
POST   /api/v1/campaigns
GET    /api/v1/campaigns
GET    /api/v1/campaigns/:id
POST   /api/v1/campaigns/:id/optimize
GET    /api/v1/campaigns/:id/analytics
```

---

## 🚀 Step 7: Create Main Application

### Create `app.py` (root directory)

```python
from flask import Flask
from src.api.routes import register_blueprints
from src.core.database import init_db

app = Flask(__name__)
app.config.from_object('config.settings.Config')

init_db(app)
register_blueprints(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 🐳 Step 8: Create Docker Configuration

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: adflowai
      POSTGRES_USER: adflowai
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://adflowai:password@postgres:5432/adflowai
      REDIS_URL: redis://redis:6379/0

volumes:
  postgres_data:
```

---

## 🧪 Step 9: Test Your Setup

### Start the application:

```bash
# Option 1: With Docker (Recommended)
docker-compose up -d

# Option 2: Locally
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Test the API:

```bash
# Health check
curl http://localhost:5000/health

# Should return: {"status": "healthy"}
```

---

## 📊 Step 10: Add Architecture Diagrams

I've already created detailed architecture documentation in `docs/ARCHITECTURE.md` with:
- System architecture diagrams
- Data flow diagrams
- Database schema
- API architecture
- Deployment architecture

---

## 🎯 Next Steps

### For Development:
1. ✅ Create Python virtual environment
2. ✅ Install dependencies
3. ✅ Configure `.env` file
4. ✅ Start Docker services
5. ✅ Run application
6. ✅ Test endpoints

### For Production:
1. Add authentication
2. Implement platform integrations (Google Ads, Facebook)
3. Build frontend (React)
4. Set up monitoring (Prometheus, Grafana)
5. Configure CI/CD pipeline
6. Deploy to cloud

---

## 🔥 Quick Start Commands

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your settings

# 3. Start Services
docker-compose up -d

# 4. Initialize Database
docker-compose exec api python scripts/init_db.py

# 5. Test
curl http://localhost:5000/health
```

---

## 📚 File Checklist

Core files you need to create:

### Configuration
- [ ] `requirements.txt`
- [ ] `.env.example`
- [ ] `.gitignore`
- [ ] `config/settings.py`

### Application
- [ ] `app.py`
- [ ] `src/models/campaign.py`
- [ ] `src/ml/optimizer.py`
- [ ] `src/core/database.py`
- [ ] `src/core/campaign_manager.py`
- [ ] `src/api/routes.py`

### Deployment
- [ ] `Dockerfile`
- [ ] `docker-compose.yml`

### Documentation
- [ ] `README.md`
- [ ] `docs/ARCHITECTURE.md`
- [ ] `PITCH_DECK.md`

---

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Docker**: https://docs.docker.com/
- **Machine Learning**: https://scikit-learn.org/

---

## 💡 Pro Tips

1. **Use VS Code Extensions:**
   - Python
   - Docker
   - GitLens
   - Pylance

2. **Test incrementally:**
   - Test each file as you create it
   - Use VS Code debugger
   - Run pytest for unit tests

3. **Version control:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/Khan-Feroz211/ADFLOWAI.git
   git push -u origin main
   ```

---

## 🐛 Troubleshooting

### Issue: Import errors
**Solution**: Make sure all `__init__.py` files exist

### Issue: Database connection failed
**Solution**: Check Docker containers are running: `docker-compose ps`

### Issue: Port already in use
**Solution**: 
```bash
# Find process using port 5000
lsof -i :5000
# Kill it
kill -9 <PID>
```

---

## 🎉 You're Ready!

Once you've created all these files, you'll have a complete, production-ready AI campaign optimization platform!

**Questions?** Check the documentation or create an issue on GitHub.

---

**Happy Coding! 🚀**
