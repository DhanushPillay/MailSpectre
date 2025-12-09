# MailSpectre 👻

MailSpectre is a production-ready email validation tool that checks if an email address is real or fake using multiple free validation techniques. Built with Python Flask backend and vanilla JavaScript frontend.

🌐 **Live Demo:** [https://mail-spectre.vercel.app/](https://mail-spectre.vercel.app/)

![MailSpectre](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

---

## 🎯 What is MailSpectre?

MailSpectre is designed to help developers and businesses verify email addresses in real-time without relying on expensive third-party APIs. It performs a series of deep checks to ensure email validity, from syntax verification to DNS lookups.

### Key Features

MailSpectre performs **11 comprehensive validation checks** on every email:

1. **📝 Format Validation** - Validates email format using RFC 5322 compliant regex
2. **🎓 Email Type Classification** - Identifies student, work, personal, or temporary emails
3. **✍️ Typo Detection** - Catches and suggests corrections for common domain typos
4. **🌐 Domain Existence** - Checks if the domain exists via DNS lookup
5. **📬 MX Records** - Verifies mail servers are properly configured
6. **🗑️ Disposable Detection** - Identifies temporary/disposable email providers
7. **⚠️ Suspicious TLD Detection** - Flags risky domain extensions used for spam/phishing
8. **🔍 Pattern Analysis** - Detects suspicious patterns in email addresses
9. **👤 Username Quality Analysis** - Analyzes username for fraud indicators with risk scoring
10. **🔐 Data Breach Check** - Checks if email was compromised using Have I Been Pwned API
11. **🚨 Fraud Database Check** - Cross-references against 1,300+ known fraudulent emails and verifies legitimate company addresses

### Security & Safety Features
- **🔐 Data Breach Detection:** Integration with Have I Been Pwned (600M+ breached accounts)
- **🚨 Fraud Database:** 1,300+ known fraudulent emails + 200+ verified company contacts
- **⚠️ Risk Scoring:** Advanced username analysis with 12+ fraud indicators
- **🛡️ Phishing Protection:** Flags suspicious TLDs commonly used for spam/phishing
- **✍️ Typo Protection:** Suggests corrections for common domain typos

### Additional Highlights
- **Clean UI:** Modern dark theme interface with real-time results and visual indicators
- **Privacy Focused:** No data storage - all checks performed in real-time with k-anonymity for breaches
- **Developer Friendly:** Simple REST API for single and batch validation
- **Zero Cost:** Uses DNS, algorithmic checks, and free APIs - no paid services needed
- **Production Ready:** Comprehensive error handling, CORS support, and detailed logging

---

## 📚 How It Works

MailSpectre uses a multi-layered approach to validate emails without sending a single message. The backend `EmailChecker` class orchestrates these checks in parallel:

### 1. Syntax & Format Validation
- **Mechanism:** Uses strict Regular Expressions (Regex) compliant with RFC 5322.
- **What it checks:** Ensures the email contains valid characters, proper `@` placement, and a valid top-level domain (TLD).

### 2. DNS Domain Verification
- **Mechanism:** Performs a DNS `A` record lookup.
- **What it checks:** Verifies that the domain name actually exists and resolves to an IP address.

### 3. Mail Server (MX) Verification
- **Mechanism:** Queries DNS for `MX` (Mail Exchange) records.
- **What it checks:** Confirms that the domain is configured to receive emails. If no mail server is listed, the email cannot exist.

### 4. Disposable Email Detection
- **Mechanism:** Checks the domain against a curated blacklist of known temporary email providers (e.g., TempMail, GuerrillaMail).
- **What it checks:** Prevents users from signing up with throwaway accounts.

### 5. Suspicious Pattern Analysis
- **Mechanism:** Analyzes the local part (before `@`) for bot-like patterns.
- **What it checks:** Flags emails like `test12345@`, `qwerty@`, or random character strings often used by bots.

### 6. Data Breach Detection
- **Mechanism:** Uses Have I Been Pwned API with SHA-1 hashing for privacy (k-anonymity model).
- **What it checks:** Determines if the email has been compromised in known data breaches. Checks against 600+ million compromised accounts without exposing the actual email.

### 7. Fraud Database Check
- **Mechanism:** Cross-references email against CSV databases of 1,300+ known fraudulent emails and 200+ verified company contacts.
- **What it checks:** Instantly flags known spam/scam emails and validates legitimate corporate addresses. Also checks if the domain has been associated with fraudulent activity.

---

## 🚀 Roadmap & Improvements

While MailSpectre is production-ready, here are concrete improvements planned for future versions:

### Database Integration
- [x] **Known Fake Email Database:** ✅ **IMPLEMENTED** - CSV database with 1,300+ fraudulent emails and 200+ verified companies.
- [ ] **Community Reporting System:** Allow users to report fake/spam emails which get added to a shared blocklist after verification.
- [ ] **Historical Validation Logs:** Store validation history with timestamps to track email reputation over time.
- [ ] **Blacklist Management Dashboard:** Admin panel to view, add, or remove entries from the disposable/fake email database.
- [ ] **Migrate to SQL Database:** Move from CSV to SQLite/PostgreSQL for better performance and scalability.

### Advanced Validation Features
- [x] **Data Breach Detection:** ✅ **IMPLEMENTED** - Integration with Have I Been Pwned API to check compromised accounts.
- [x] **Typo Correction:** ✅ **IMPLEMENTED** - Suggests corrections for common typos (e.g., `gmial.com` → `gmail.com`).
- [x] **Email Type Classification:** ✅ **IMPLEMENTED** - Identifies student, work, personal, or temporary emails with confidence scores.
- [x] **Suspicious TLD Detection:** ✅ **IMPLEMENTED** - Flags risky domain extensions commonly used for spam/phishing.
- [x] **Username Quality Analysis:** ✅ **IMPLEMENTED** - Advanced pattern analysis with risk scoring system.
- [ ] **SMTP Handshake Verification:** Connect to mail servers and perform `RCPT TO` checks to verify if specific mailboxes actually exist (without sending emails).
- [ ] **Catch-All Domain Detection:** Identify domains configured to accept all email addresses (common false positives).
- [ ] **Role-Based Email Detection:** Flag generic business emails (`admin@`, `support@`, `noreply@`) vs personal accounts.

### Performance & Scalability
- [ ] **Redis Caching Layer:** Cache validation results for frequently checked domains to reduce API response time.
- [ ] **Rate Limiting & Throttling:** Implement token bucket or sliding window rate limiting per IP/API key.
- [ ] **Async Processing Queue:** Use Celery/RQ for handling batch validations asynchronously.

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Installation Guide](docs/INSTALLATION.md)** - Setup instructions for local development
- **[Testing Guide](docs/TESTING.md)** - Unit and integration testing procedures
- **[Safety Features](docs/SAFETY_FEATURES.md)** - Detailed security and fraud detection documentation
- **[Email Types](docs/EMAIL_TYPES.md)** - Email classification system explained
- **[Algorithm Details](docs/ALGORITHM.md)** - Deep dive into validation algorithms
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Quick API reference and examples
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions

---

## 🔌 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/validate` | POST | Validate a single email address with complete analysis |
| `/api/batch-validate` | POST | Validate multiple emails (up to 50 per request) |
| `/api/health` | GET | Check service health status |

### Example Request

```bash
curl -X POST https://mailspectre-api.onrender.com/api/validate \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### Example Response

```json
{
  "email": "user@example.com",
  "valid": true,
  "score": 91.67,
  "summary": "Email looks valid with minor concerns",
  "checks": [
    {
      "check": "format",
      "valid": true,
      "message": "Valid email format"
    },
    {
      "check": "data_breach",
      "valid": true,
      "message": "No known data breaches"
    },
    {
      "check": "fraud_database",
      "valid": true,
      "message": "Not in fraud database"
    }
  ]
}
## 🔌 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/validate` | POST | Validate a single email address |
| `/api/batch-validate` | POST | Validate multiple emails (max 50) |
| `/api/health` | GET | Check service health status |

---

**Built with ❤️ for the community**

*MailSpectre - Uncover the truth behind every email address* 👻

---

## Made BY

**Shubhangini Dixit & Dhanush Pillay**
