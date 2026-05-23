# 🚀 Deployment Guide - AdiZenWorks Web Application

Complete deployment instructions for hosting the web version.

---

## 📋 Quick Deploy Options

### 🏠 Local Development

```bash
python app.py
```
Access at: http://localhost:5000

---

### 🐳 Docker Deployment

#### Create Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copy application
COPY . .

# Create reports directory
RUN mkdir -p AdiZenWorks_Reports

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
```

#### Build and Run:

```bash
# Build image
docker build -t adizenworks-web .

# Run container
docker run -d -p 5000:5000 \
  -v $(pwd)/AdiZenWorks_Reports:/app/AdiZenWorks_Reports \
  -v $(pwd)/adizen_config.json:/app/adizen_config.json \
  adizenworks-web
```

---

### ☁️ Cloud Platforms

## Heroku

### 1. Create Procfile:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 app:app
```

### 2. Deploy:

```bash
# Login to Heroku
heroku login

# Create app
heroku create adizenworks-toolkit

# Set config (if using AI)
heroku config:set GEMINI_API_KEY=your_key_here

# Deploy
git push heroku main

# Open
heroku open
```

---

## Railway

### 1. Create railway.json:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Deploy:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

---

## Vercel

### 1. Create vercel.json:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 2. Deploy:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

---

## AWS Elastic Beanstalk

### 1. Create .ebextensions/python.config:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
```

### 2. Deploy:

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.12 adizenworks-toolkit

# Create environment
eb create adizenworks-env

# Deploy
eb deploy

# Open
eb open
```

---

## 🔐 Environment Variables

### For AI Features:

```bash
# .env file (don't commit this!)
GEMINI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

### Load in app.py:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

---

## 🔒 Production Security

### 1. Use HTTPS

```bash
# Let's Encrypt (free SSL)
certbot --nginx -d yourdomain.com
```

### 2. Set Environment Variables

Never hardcode API keys!

```bash
# Heroku
heroku config:set GEMINI_API_KEY=xxx

# Railway
railway variables set GEMINI_API_KEY=xxx

# Docker
docker run -e GEMINI_API_KEY=xxx ...
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/scan/ports', methods=['POST'])
@limiter.limit("10 per minute")
def scan_ports():
    ...
```

---

## 📊 Monitoring

### Application Logs:

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Docker
docker logs -f container_id
```

### Health Check Endpoint:

```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'version': '2.0'}), 200
```

---

## ⚡ Performance Optimization

### 1. Use Production WSGI Server

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### 2. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/tools/hash', methods=['POST'])
@cache.cached(timeout=300)
def generate_hash():
    ...
```

### 3. Compress Responses

```python
from flask_compress import Compress

Compress(app)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml):

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "adizenworks-toolkit"
          heroku_email: "your@email.com"
```

---

## 📦 Database (Optional)

### For storing scan results:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scans.db'
db = SQLAlchemy(app)

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(50))
    data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime)
```

---

## 🌍 Custom Domain

### 1. Configure DNS:

```
Type: A
Name: @
Value: your_server_ip

Type: CNAME
Name: www
Value: yourdomain.com
```

### 2. Update Platform:

```bash
# Heroku
heroku domains:add www.yourdomain.com

# Railway
# Add custom domain in dashboard

# Vercel
vercel domains add yourdomain.com
```

---

## 🎯 Scaling

### Horizontal Scaling:

```bash
# Heroku
heroku ps:scale web=3

# Railway
# Adjust replicas in dashboard

# AWS
eb scale 3
```

---

## 📞 Support

Having deployment issues?

- **GitHub Issues**: Report deployment problems
- **Email**: deploy@adizenworks.com
- **Docs**: docs.adizenworks.com

---

<div align="center">

**Your toolkit is ready for production! 🚀**

[Back to README](README.md) | [Installation Guide](INSTALLATION.md)

© 2026 AdiZenWorks Inc.

</div>
