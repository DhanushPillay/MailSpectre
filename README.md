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

## 🌐 Deployment

### Deploy to Heroku (Free Tier)

**Prerequisites:**
- Heroku account (sign up at https://heroku.com)
- Heroku CLI installed

**Deployment Steps:**

```powershell
# 1. Login to Heroku
heroku login

# 2. Create new Heroku app
heroku create mailspectre-validator

# 3. Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# 4. Add Heroku remote
heroku git:remote -a mailspectre-validator

# 5. Deploy to Heroku
git push heroku main

# 6. Open your deployed app
heroku open
```

**Environment Variables:**
```powershell
heroku config:set DEBUG=False
heroku config:set PORT=5000
```

**View Logs:**
```powershell
heroku logs --tail
```

### Deploy to Render (Free Tier)

1. Push your code to GitHub
2. Visit https://render.com
3. Create new "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3.11

### Deploy to Railway (Free Tier)

1. Visit https://railway.app
2. Create new project from GitHub repo
3. Railway auto-detects configuration
4. Deploy automatically

### Deploy Frontend to Netlify/Vercel

**For Netlify:**
1. Visit https://netlify.com
2. Drag & drop the `frontend` folder
3. Update `script.js` API_BASE_URL to your backend URL

**For Vercel:**
```powershell
npm install -g vercel
cd frontend
vercel
```

### Deploy to PythonAnywhere (Free Tier)

1. Sign up at https://pythonanywhere.com
2. Upload your files
3. Create new web app with Flask
4. Set working directory to `/home/yourusername/MailSpectre/backend`
5. Update WSGI file to import your app

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
FLASK_APP=backend/app.py
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
ALLOWED_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
```

### Customization

**Add More Disposable Domains:**

Edit `backend/checker.py`, add to `DISPOSABLE_DOMAINS` set:
```python
DISPOSABLE_DOMAINS = {
    'tempmail.com',
    'yourdomain.com',  # Add here
    # ... more domains
}
```

**Adjust Validation Scoring:**

In `checker.py`, modify the `validate_email()` method:
```python
# Current: needs 4/5 checks to pass
critical_passed and valid_checks >= 4

# More strict: needs all checks
critical_passed and valid_checks == 5
```

**Frontend Styling:**

Modify CSS variables in `frontend/styles.css`:
```css
:root {
    --primary-color: #6366f1;  /* Change colors */
    --success-color: #10b981;
    /* ... more variables */
}
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

## 🛠️ Troubleshooting

### Backend Won't Start

**Error: Module not found**
```powershell
# Reinstall dependencies
pip install --upgrade -r backend\requirements.txt
```

**Error: Port already in use**
```powershell
# Change port in app.py or kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Frontend Can't Connect to Backend

1. **Check backend is running**: Visit http://localhost:5000
2. **Check CORS**: Ensure frontend origin is allowed
3. **Update API URL**: In `script.js`, verify `API_BASE_URL`

### DNS Resolution Errors

**Error: dns.resolver timeout**
- Check internet connection
- Some networks block DNS queries
- Try different network or VPN

### Validation Always Fails

1. **Check DNS resolver**: Test with `nslookup gmail.com`
2. **Firewall blocking**: Allow Python through Windows Firewall
3. **Increase timeout**: In `checker.py`, increase `self.dns_resolver.timeout`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint rules for JavaScript
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- Flask framework and community
- dnspython library developers
- Open source disposable email lists
- RFC 5322 email specification

---

## 📧 Contact & Support

- **Issues**: Open an issue on GitHub
- **Email**: [Your email]
- **Documentation**: See this README

---

## 🔄 Changelog

### Version 1.0.0 (2025-12-08)
- Initial release
- 5 validation checks implemented
- Frontend and backend complete
- Production-ready deployment configs
- Comprehensive documentation

---

## 🎯 Roadmap

Future enhancements planned:

- [ ] SMTP connection test (optional)
- [ ] Email deliverability score
- [ ] Catch-all domain detection
- [ ] Role-based email detection (info@, admin@)
- [ ] Historical validation caching
- [ ] API rate limiting
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] Webhook support
- [ ] CSV bulk upload

---

**Built with ❤️ for the community**

*MailSpectre - Uncover the truth behind every email address* 👻
