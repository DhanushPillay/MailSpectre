# MailSpectre 👻

**Free Email Validation Service - No Paid APIs Required**

MailSpectre is a production-ready email validation tool that checks if an email address is real or fake using multiple free validation techniques. Built with Python Flask backend and vanilla JavaScript frontend.

![MailSpectre](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What is MailSpectre?

MailSpectre is designed to help developers and businesses verify email addresses in real-time without relying on expensive third-party APIs. It performs a series of deep checks to ensure email validity, from syntax verification to DNS lookups.

### Key Features

MailSpectre performs **5 comprehensive validation checks** on every email:

1. **📝 Format Validation** - Validates email format using RFC 5322 compliant regex
2. **🌐 Domain Existence** - Checks if the domain exists via DNS lookup
3. **📬 MX Records** - Verifies mail servers are properly configured
4. **🗑️ Disposable Detection** - Identifies temporary/disposable email providers
5. **🔍 Pattern Analysis** - Detects suspicious patterns in email addresses

### Additional Highlights
- **Clean UI:** Modern dark theme interface with real-time results.
- **Privacy Focused:** No data storage - all checks performed in real-time.
- **Developer Friendly:** Simple REST API for batch validation.
- **Zero Cost:** Uses DNS and algorithmic checks, no paid services needed.

---

## 📚 How It Works

The validation process flows through a pipeline of checks:

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

1. **Frontend:** Captures input and sends to Flask API.
2. **Backend:** The `EmailChecker` class runs parallel validations.
3. **Response:** Returns a detailed JSON object with a validity score (0-100%).

---

## 📖 Documentation

- **[Installation Guide](INSTALLATION.md)** - Setup instructions for local development.
- **[Deployment Guide](DEPLOYMENT.md)** - How to deploy to Heroku, Render, etc.
- **[Testing Guide](TESTING.md)** - Unit and integration testing procedures.

---

## 🔌 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/validate` | POST | Validate a single email address |
| `/api/batch-validate` | POST | Validate multiple emails (max 50) |
| `/api/health` | GET | Check service health status |

---

**Built with ❤️ for the community**

*MailSpectre - Uncover the truth behind every email address* 👻
