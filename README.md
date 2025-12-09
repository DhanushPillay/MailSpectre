# MailSpectre 👻

MailSpectre is a production-ready email validation tool that checks if an email address is real or fake using multiple free validation techniques. Built with Python Flask backend and vanilla JavaScript frontend.

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

### Additional Highlights
- **Clean UI:** Modern dark theme interface with real-time results.
- **Privacy Focused:** No data storage - all checks performed in real-time.
- **Developer Friendly:** Simple REST API for batch validation.
- **Zero Cost:** Uses DNS and algorithmic checks, no paid services needed.
- **Fraud Detection:** Built-in database of known spam/fraud emails and verified company contacts.

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

### Data Sources & Intelligence
- [ ] **Integration with Public Blocklists:** Sync with community-maintained disposable email lists (Stopforumspam, Disposable Email Blocklist).
- [ ] **Machine Learning Model:** Train an ML classifier on patterns to detect new disposable/fake email services automatically.
- [ ] **Domain Reputation Score:** Cross-reference domains with spam databases and reputation services.

---

## 📖 Documentation

- **[Installation Guide](INSTALLATION.md)** - Setup instructions for local development.
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

---

## Made BY

**Shubhangini Dixit & Dhanush Pillay**
