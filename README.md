# MailSpectre 👻

**Free Email Validation Service - No Paid APIs Required**

MailSpectre is a production-ready email validation tool that checks if an email address is real or fake using multiple free validation techniques. Built with Python Flask backend and vanilla JavaScript frontend.

![MailSpectre](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

MailSpectre performs **5 comprehensive validation checks** on every email:

1. **📝 Format Validation** - Validates email format using RFC 5322 compliant regex
2. **🌐 Domain Existence** - Checks if the domain exists via DNS lookup
3. **📬 MX Records** - Verifies mail servers are properly configured
4. **🗑️ Disposable Detection** - Identifies temporary/disposable email providers
5. **🔍 Pattern Analysis** - Detects suspicious patterns in email addresses

### Additional Features
- Clean, modern UI with dark theme
- Real-time validation results
- Detailed JSON output
- Copy-to-clipboard functionality
- Responsive design for all devices
- No data storage - all checks performed in real-time
- Batch validation API endpoint
- Production-ready error handling

---

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
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A modern web browser

### Installation & Setup

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

---

## 🧪 Testing

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

4. **Test Suspicious Pattern:**
   - Enter: `test12345@gmail.com`
   - Expected: Pattern check may flag

### API Testing with cURL

```powershell
# Test validation endpoint
curl -X POST http://localhost:5000/api/validate `
  -H "Content-Type: application/json" `
  -d '{"email": "test@gmail.com"}'

# Test health endpoint
curl http://localhost:5000/api/health

# Test batch validation
curl -X POST http://localhost:5000/api/batch-validate `
  -H "Content-Type: application/json" `
  -d '{"emails": ["test@gmail.com", "user@example.com"]}'
```

### Python Testing Script

Create a test file `test_validation.py`:

```python
import requests

API_URL = "http://localhost:5000/api/validate"

test_emails = [
    "valid@gmail.com",
    "invalid@nonexistentdomain.com",
    "test@tempmail.com",
    "test12345@yahoo.com"
]

for email in test_emails:
    response = requests.post(API_URL, json={"email": email})
    result = response.json()
    print(f"\n{email}: Valid={result['valid']}, Score={result['score']}%")
```

Run: `python test_validation.py`

---

## 📚 How It Works

### Backend Architecture

**1. checker.py - EmailChecker Class**
- `validate_format()`: Uses regex to validate RFC 5322 email format
- `check_domain_exists()`: Performs DNS A record lookup
- `check_mx_records()`: Queries DNS MX records for mail servers
- `check_disposable()`: Compares against known disposable domains
- `check_suspicious_patterns()`: Regex pattern matching for suspicious strings
- `validate_email()`: Orchestrates all checks and calculates score

**2. app.py - Flask API Server**
- `/api/validate`: Single email validation endpoint
- `/api/batch-validate`: Multiple email validation endpoint
- `/api/health`: Service health check
- CORS enabled for cross-origin requests
- Comprehensive error handling
- Request logging

### Frontend Architecture

**1. index.html**
- Semantic HTML5 structure
- Accessibility features
- Progressive enhancement

**2. styles.css**
- CSS custom properties (variables)
- Responsive grid layout
- Dark theme design
- Smooth animations
- Print-friendly styles

**3. script.js**
- Fetch API for HTTP requests
- DOM manipulation
- Error handling
- Clipboard API integration
- Request timeout handling

### Validation Flow

```
User Input → Frontend Validation → API Request → Backend Processing
                                                        ↓
                                                  5 Parallel Checks
                                                        ↓
                                                  Score Calculation
                                                        ↓
                                            JSON Response → Frontend
                                                        ↓
                                                 Results Display
```

---

## 📊 API Documentation

### POST /api/validate

Validate a single email address.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "email": "user@example.com",
  "valid": true,
  "score": 100.0,
  "checks": [
    {
      "check": "format",
      "valid": true,
      "message": "Valid email format",
      "details": "Email follows standard format"
    },
    {
      "check": "domain_exists",
      "valid": true,
      "message": "Domain exists",
      "details": "Domain example.com has valid DNS records"
    },
    {
      "check": "mx_records",
      "valid": true,
      "message": "MX records found",
      "details": "Domain has 1 mail server(s): mail.example.com"
    },
    {
      "check": "disposable",
      "valid": true,
      "message": "Not a disposable email",
      "details": "Domain not in known disposable providers"
    },
    {
      "check": "suspicious_patterns",
      "valid": true,
      "message": "No suspicious patterns",
      "details": "Email looks legitimate"
    }
  ],
  "summary": "Email passed all validation checks"
}
```

### POST /api/batch-validate

Validate multiple emails (max 50).

**Request:**
```json
{
  "emails": [
    "user1@example.com",
    "user2@example.com"
  ]
}
```

**Response:**
```json
{
  "total": 2,
  "results": [
    { /* validation result 1 */ },
    { /* validation result 2 */ }
  ]
}
```

### GET /api/health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "service": "MailSpectre API",
  "timestamp": "2025-12-08"
}
```

---

**Built with ❤️ for the community**

*MailSpectre - Uncover the truth behind every email address* 👻
