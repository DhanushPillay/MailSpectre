# Installation & Setup Guide

## 📁 Project Structure

```
MailSpectre/
├── backend/
│   ├── app.py              # Flask API server
│   ├── checker.py          # Email validation logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main webpage
│   ├── styles.css          # Styling
│   └── script.js           # Frontend logic
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
├── Procfile                # Heroku deployment config
├── runtime.txt             # Python version for deployment
└── README.md               # Main documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A modern web browser

### Installation Steps

**Step 1: Clone or Navigate to the Project**
```powershell
cd "E:\Personal Projects\MailSpectre"
```

**Step 2: Create Virtual Environment**
```powershell
python -m venv venv
```

**Step 3: Activate Virtual Environment**
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Step 4: Install Dependencies**
```powershell
pip install -r backend\requirements.txt
```

**Step 5: Start the Flask Backend**
```powershell
python backend\app.py
```

You should see:
```
Starting MailSpectre on port 5000
Debug mode: True
 * Running on http://0.0.0.0:5000
```

**Step 6: Open the Frontend**

Open `frontend\index.html` in your web browser, or use a simple HTTP server:

```powershell
# Option 1: Direct file open
start frontend\index.html

# Option 2: Python HTTP server (recommended)
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 🧪 Verifying Installation

### Manual Testing

1. **Test Valid Email:**
   - Enter: `test@gmail.com`
   - Expected: All checks pass, score 100%

2. **Test Invalid Domain:**
   - Enter: `user@nonexistentdomain12345.com`
   - Expected: Domain and MX checks fail

3. **Test Disposable Email:**
   - Enter: `test@tempmail.com`
   - Expected: Disposable check fails

### API Testing with cURL

```powershell
# Test validation endpoint
curl -X POST http://localhost:5000/api/validate `
  -H "Content-Type: application/json" `
  -d '{"email": "test@gmail.com"}'

# Test health endpoint
curl http://localhost:5000/api/health
```
