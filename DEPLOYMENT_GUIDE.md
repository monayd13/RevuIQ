# 🚀 RevuIQ Deployment Guide

Complete guide for deploying RevuIQ to production

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Database Setup](#database-setup)
5. [API Keys Configuration](#api-keys-configuration)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🏠 Local Development

### **Prerequisites**
- Python 3.13+
- Node.js 20+
- PostgreSQL 15+ (optional, can use SQLite)

### **Setup Steps**

1. **Clone Repository**
```bash
git clone <your-repo-url>
cd RevuIQ
```

2. **Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt
pip install sqlalchemy psycopg2-binary

# Download NLP data
python -m textblob.download_corpora

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run backend
cd backend
python main_complete.py
```

3. **Frontend Setup**
```bash
# Install Node dependencies
cd frontend
npm install

# Run frontend
npm run dev
```

4. **Access Application**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Analytics: http://localhost:3000/analytics

---

## 🐳 Docker Deployment

### **Using Docker Compose** (Recommended)

1. **Build and Start All Services**
```bash
# Create .env file with your configuration
cp .env.example .env

# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

2. **Individual Service Management**
```bash
# Restart backend only
docker-compose restart backend

# View backend logs
docker-compose logs -f backend

# Rebuild after code changes
docker-compose up -d --build
```

3. **Database Access**
```bash
# Connect to PostgreSQL
docker-compose exec database psql -U revuiq -d revuiq_db

# Backup database
docker-compose exec database pg_dump -U revuiq revuiq_db > backup.sql

# Restore database
docker-compose exec -T database psql -U revuiq revuiq_db < backup.sql
```

---

## ☁️ Cloud Deployment

### **Option 1: Vercel (Frontend) + Railway (Backend)**

#### **Frontend on Vercel**

1. **Connect Repository**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select `frontend` as root directory

2. **Configure Build**
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will auto-deploy on every push to main

#### **Backend on Railway**

1. **Create New Project**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Configure Service**
   - Root Directory: `backend`
   - Start Command: `python main_complete.py`

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will auto-configure DATABASE_URL

4. **Environment Variables**
   ```
   DATABASE_URL=<auto-configured>
   GOOGLE_PLACES_API_KEY=your_key
   YELP_API_KEY=your_key
   META_ACCESS_TOKEN=your_token
   ```

5. **Deploy**
   - Railway will auto-deploy
   - Get your backend URL from settings

---

### **Option 2: AWS (Full Stack)**

#### **Backend on AWS Lambda + API Gateway**

1. **Prepare Lambda Function**
```bash
# Install dependencies in a directory
pip install -r requirements.txt -t lambda_package/
cp -r backend/* lambda_package/
cp -r nlp_pipeline/* lambda_package/

# Create deployment package
cd lambda_package
zip -r ../revuiq-lambda.zip .
```

2. **Create Lambda Function**
   - Runtime: Python 3.13
   - Handler: `main_complete.handler`
   - Upload `revuiq-lambda.zip`
   - Set environment variables

3. **Configure API Gateway**
   - Create REST API
   - Add routes for all endpoints
   - Deploy to stage

#### **Frontend on AWS Amplify**

1. **Connect Repository**
   - Go to AWS Amplify Console
   - Connect GitHub repository

2. **Build Settings**
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm install
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL`

---

### **Option 3: DigitalOcean App Platform**

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect GitHub repository

2. **Configure Components**

**Backend:**
```yaml
name: revuiq-backend
source:
  repo: your-repo
  branch: main
  dir: /backend
run_command: python main_complete.py
envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
```

**Frontend:**
```yaml
name: revuiq-frontend
source:
  repo: your-repo
  branch: main
  dir: /frontend
build_command: npm run build
run_command: npm start
```

**Database:**
```yaml
name: revuiq-db
engine: PG
version: "15"
```

---

## 🗄️ Database Setup

### **PostgreSQL (Production)**

1. **Create Database**
```sql
CREATE DATABASE revuiq_db;
CREATE USER revuiq WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE revuiq_db TO revuiq;
```

2. **Run Migrations**
```python
# The database_manager.py automatically creates tables
# Just run the backend once:
python backend/main_complete.py
```

3. **Backup Strategy**
```bash
# Daily backup
pg_dump -U revuiq revuiq_db > backup_$(date +%Y%m%d).sql

# Automated backup (cron)
0 2 * * * pg_dump -U revuiq revuiq_db > /backups/revuiq_$(date +\%Y\%m\%d).sql
```

### **SQLite (Development)**

```python
# In .env file:
DATABASE_URL=sqlite:///./revuiq.db

# Database file will be created automatically
```

---

## 🔑 API Keys Configuration

### **Google Places API**

1. Go to https://console.cloud.google.com
2. Enable "Places API"
3. Create credentials → API Key
4. Restrict key to Places API
5. Add to `.env`: `GOOGLE_PLACES_API_KEY=your_key`

### **Yelp Fusion API**

1. Go to https://www.yelp.com/developers
2. Create App
3. Get API Key
4. Add to `.env`: `YELP_API_KEY=your_key`

### **Meta Graph API**

1. Go to https://developers.facebook.com
2. Create App
3. Get Access Token
4. Add to `.env`: `META_ACCESS_TOKEN=your_token`

### **TripAdvisor API**

1. Apply for partnership at https://developer.tripadvisor.com
2. Get API Key
3. Add to `.env`: `TRIPADVISOR_API_KEY=your_key`

---

## 📊 Monitoring & Maintenance

### **Health Checks**

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/api/analytics/stats
```

### **Logging**

```python
# Add to main_complete.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('revuiq.log'),
        logging.StreamHandler()
    ]
)
```

### **Performance Monitoring**

```bash
# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/analyze

# Database query performance
EXPLAIN ANALYZE SELECT * FROM reviews WHERE sentiment = 'POSITIVE';
```

### **Backup Automation**

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U revuiq revuiq_db > /backups/revuiq_$DATE.sql
find /backups -name "revuiq_*.sql" -mtime +7 -delete

# Add to crontab
0 2 * * * /path/to/backup.sh
```

---

## 🔒 Security Checklist

- [ ] Change default passwords
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Implement rate limiting
- [ ] Add authentication (JWT)
- [ ] Encrypt database connections
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Backup encryption

---

## 🚦 Production Checklist

- [ ] Database configured and tested
- [ ] All API keys added to environment
- [ ] CORS configured for production domain
- [ ] SSL certificates installed
- [ ] Health check endpoints working
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Documentation updated

---

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test database connection
4. Check API key validity
5. Review firewall rules

---

## 🎉 Post-Deployment

After successful deployment:

1. **Test All Features**
   - Analyze a review
   - Fetch reviews from platforms
   - Check analytics dashboard
   - Approve responses

2. **Monitor Performance**
   - Response times
   - Error rates
   - Database performance
   - API usage

3. **Set Up Alerts**
   - Downtime alerts
   - Error rate thresholds
   - Database capacity
   - API quota limits

---

**Deployment Status: Ready for Production** ✅

For questions or issues, refer to the main README.md or create an issue in the repository.
