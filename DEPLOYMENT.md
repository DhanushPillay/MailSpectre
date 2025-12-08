# MailSpectre Deployment Guide

Complete guide for deploying MailSpectre to various platforms.

---

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Heroku Deployment](#heroku-deployment)
3. [Render Deployment](#render-deployment)
4. [Railway Deployment](#railway-deployment)
5. [PythonAnywhere Deployment](#pythonanywhere-deployment)
6. [Vercel + Heroku (Full Stack)](#vercel--heroku-full-stack)
7. [Docker Deployment](#docker-deployment)
8. [Custom VPS Deployment](#custom-vps-deployment)

---

## Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Debug mode disabled for production
- [ ] CORS origins updated
- [ ] API URLs updated in frontend
- [ ] Requirements.txt up to date
- [ ] .gitignore includes sensitive files
- [ ] README documentation complete

---

## Heroku Deployment

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git initialized in project

### Step-by-Step Guide

**1. Install Heroku CLI**
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use Chocolatey:
choco install heroku-cli
```

**2. Login to Heroku**
```powershell
heroku login
```

**3. Create Heroku App**
```powershell
cd "E:\Personal Projects\MailSpectre"
heroku create mailspectre-validator
# Note: App name must be unique globally
```

**4. Configure Environment Variables**
```powershell
heroku config:set DEBUG=False
heroku config:set FLASK_ENV=production
heroku config:set PORT=5000
```

**5. Verify Files**

Ensure these files exist:
- `Procfile` (already created)
- `runtime.txt` (already created)
- `backend/requirements.txt` (already created)

**6. Initialize Git (if needed)**
```powershell
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

**7. Deploy to Heroku**
```powershell
heroku git:remote -a mailspectre-validator
git push heroku main
```

**8. Scale Dynos**
```powershell
heroku ps:scale web=1
```

**9. Open Your App**
```powershell
heroku open
```

**10. View Logs**
```powershell
heroku logs --tail
```

### Troubleshooting Heroku

**App won't start:**
```powershell
heroku logs --tail
# Check for errors in dependencies or Procfile
```

**Update dependencies:**
```powershell
git add backend/requirements.txt
git commit -m "Update dependencies"
git push heroku main
```

---

## Render Deployment

### Prerequisites
- Render account (free tier available)
- GitHub repository

### Step-by-Step Guide

**1. Push to GitHub**
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/MailSpectre.git
git push -u origin main
```

**2. Create Render Account**
- Visit https://render.com
- Sign up with GitHub

**3. Create Web Service**
- Click "New +"
- Select "Web Service"
- Connect your GitHub repository
- Select "MailSpectre" repository

**4. Configure Service**
```
Name: mailspectre
Environment: Python 3
Region: Choose closest to you
Branch: main
Build Command: pip install -r backend/requirements.txt
Start Command: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
```

**5. Add Environment Variables**
```
DEBUG=False
FLASK_ENV=production
```

**6. Deploy**
- Click "Create Web Service"
- Wait for build to complete
- Access your app at: https://mailspectre.onrender.com

### Auto-Deploy Setup
- Enable "Auto-Deploy" in Render dashboard
- Every git push triggers automatic deployment

---

## Railway Deployment

### Prerequisites
- Railway account (free tier: $5 credit/month)
- GitHub repository

### Step-by-Step Guide

**1. Push to GitHub** (if not already done)

**2. Create Railway Account**
- Visit https://railway.app
- Sign up with GitHub

**3. Create New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose "MailSpectre" repository

**4. Configure**
Railway auto-detects Python and uses:
- Start command from `Procfile`
- Dependencies from `requirements.txt`

**5. Add Environment Variables**
```
DEBUG=False
FLASK_ENV=production
PORT=$PORT
```

**6. Generate Domain**
- Go to "Settings" → "Networking"
- Click "Generate Domain"
- Access your app at: https://mailspectre.up.railway.app

### Railway Features
- Automatic deployments on git push
- Built-in metrics and logs
- Easy rollback to previous versions

---

## PythonAnywhere Deployment

### Prerequisites
- PythonAnywhere account (free tier available)

### Step-by-Step Guide

**1. Create Account**
- Visit https://www.pythonanywhere.com
- Sign up for free account

**2. Upload Files**
```powershell
# Option 1: Upload via web interface
# Option 2: Clone from GitHub
```

On PythonAnywhere console:
```bash
git clone https://github.com/yourusername/MailSpectre.git
cd MailSpectre
```

**3. Create Virtual Environment**
```bash
mkvirtualenv mailspectre --python=python3.11
workon mailspectre
pip install -r backend/requirements.txt
```

**4. Create Web App**
- Go to "Web" tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.11

**5. Configure WSGI File**

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/MailSpectre'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add backend directory
backend_path = os.path.join(project_home, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import Flask app
from backend.app import app as application
```

**6. Set Virtual Environment**
- In Web tab, set virtualenv path:
  `/home/yourusername/.virtualenvs/mailspectre`

**7. Reload Web App**
- Click "Reload" button
- Visit: https://yourusername.pythonanywhere.com

---

## Vercel + Heroku (Full Stack)

Deploy frontend on Vercel, backend on Heroku.

### Backend (Heroku)
Follow [Heroku Deployment](#heroku-deployment) above.

### Frontend (Vercel)

**1. Install Vercel CLI**
```powershell
npm install -g vercel
```

**2. Create vercel.json**

In `frontend/` directory, create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ]
}
```

**3. Update API URL**

In `frontend/script.js`, update:
```javascript
const CONFIG = {
    API_BASE_URL: 'https://your-app.herokuapp.com',
    API_ENDPOINT: '/api/validate',
    REQUEST_TIMEOUT: 10000
};
```

**4. Deploy**
```powershell
cd frontend
vercel
# Follow prompts
```

**5. Set Production Domain**
```powershell
vercel --prod
```

---

## Docker Deployment

### Create Dockerfile

Create `Dockerfile` in root:
```dockerfile
# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV DEBUG=False

# Run application
CMD ["gunicorn", "--chdir", "backend", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEBUG=False
      - FLASK_ENV=production
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend
    restart: unless-stopped
```

### Deploy with Docker

```powershell
# Build image
docker build -t mailspectre .

# Run container
docker run -d -p 5000:5000 mailspectre

# Or use docker-compose
docker-compose up -d
```

### Deploy to Docker Hub

```powershell
# Login
docker login

# Tag image
docker tag mailspectre yourusername/mailspectre:latest

# Push
docker push yourusername/mailspectre:latest
```

---

## Custom VPS Deployment

### Prerequisites
- Ubuntu 22.04 VPS (DigitalOcean, Linode, AWS EC2)
- Domain name (optional)
- SSH access

### Step-by-Step Guide

**1. Connect to VPS**
```powershell
ssh root@your-server-ip
```

**2. Update System**
```bash
apt update && apt upgrade -y
```

**3. Install Dependencies**
```bash
apt install python3.11 python3.11-venv python3-pip nginx git -y
```

**4. Clone Repository**
```bash
cd /var/www
git clone https://github.com/yourusername/MailSpectre.git
cd MailSpectre
```

**5. Create Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install gunicorn
```

**6. Create Systemd Service**

Create `/etc/systemd/system/mailspectre.service`:
```ini
[Unit]
Description=MailSpectre Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/MailSpectre
Environment="PATH=/var/www/MailSpectre/venv/bin"
ExecStart=/var/www/MailSpectre/venv/bin/gunicorn --chdir backend app:app --bind 127.0.0.1:5000 --workers 2

[Install]
WantedBy=multi-user.target
```

**7. Start Service**
```bash
systemctl daemon-reload
systemctl start mailspectre
systemctl enable mailspectre
systemctl status mailspectre
```

**8. Configure Nginx**

Create `/etc/nginx/sites-available/mailspectre`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/MailSpectre/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**9. Enable Site**
```bash
ln -s /etc/nginx/sites-available/mailspectre /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

**10. Configure Firewall**
```bash
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw enable
```

**11. SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## Post-Deployment

### Monitoring

**Heroku:**
```powershell
heroku logs --tail
heroku ps
```

**VPS:**
```bash
journalctl -u mailspectre -f
systemctl status mailspectre
```

### Updates

**Heroku:**
```powershell
git add .
git commit -m "Update"
git push heroku main
```

**VPS:**
```bash
cd /var/www/MailSpectre
git pull
systemctl restart mailspectre
```

---

## Free Deployment Options Summary

| Platform | Backend | Frontend | Custom Domain | SSL |
|----------|---------|----------|---------------|-----|
| Heroku | ✅ Free | ❌ | ✅ | ✅ |
| Render | ✅ Free | ✅ Free | ✅ | ✅ |
| Railway | ✅ $5 credit | ✅ | ✅ | ✅ |
| PythonAnywhere | ✅ Free | ✅ Free | ❌ | ✅ |
| Vercel | ❌ | ✅ Free | ✅ | ✅ |
| Netlify | ❌ | ✅ Free | ✅ | ✅ |

---

**Choose the platform that best fits your needs!**
