# MailSpectre 👻

MailSpectre is a production-ready email validation tool that checks if an email address is real or fake using multiple free validation techniques. Built with Python Flask backend and vanilla JavaScript frontend.

![MailSpectre](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

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

---

## 🚀 Roadmap & Improvements

While MailSpectre is production-ready, there are several areas for potential enhancement:

- [ ] **SMTP Handshake:** Implement deep verification by connecting to the mail server and performing a `RCPT TO` check (without sending data) to verify if the specific mailbox exists.
- [ ] **Catch-All Detection:** Identify domains that accept all emails (common in business domains) which can give false positives.
- [ ] **Role-Based Detection:** Flag generic addresses like `admin@`, `support@`, `info@` which are often not personal accounts.
- [ ] **Result Caching:** Implement Redis to cache validation results for common domains to improve performance.
- [ ] **Rate Limiting:** Add API rate limiting to prevent abuse of the public endpoint.
- [ ] **Expanded Blacklist:** Integrate with larger, community-maintained lists of disposable email providers.

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

**Made BY**

Dhanush Pillay & Shubhangini Dixit
