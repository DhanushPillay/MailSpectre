# MailSpectre Testing Guide

## Overview
This guide provides comprehensive testing instructions for MailSpectre email validation system.

---

## Unit Testing

### Backend Tests

Create `backend/test_checker.py`:

```python
import unittest
from checker import EmailChecker

class TestEmailChecker(unittest.TestCase):
    
    def setUp(self):
        self.checker = EmailChecker()
    
    def test_valid_format(self):
        """Test valid email format"""
        result = self.checker.validate_format("test@example.com")
        self.assertTrue(result['valid'])
    
    def test_invalid_format(self):
        """Test invalid email format"""
        result = self.checker.validate_format("invalid-email")
        self.assertFalse(result['valid'])
    
    def test_disposable_detection(self):
        """Test disposable email detection"""
        result = self.checker.check_disposable("test@tempmail.com")
        self.assertFalse(result['valid'])
    
    def test_suspicious_patterns(self):
        """Test suspicious pattern detection"""
        result = self.checker.check_suspicious_patterns("test12345@gmail.com")
        # May or may not be flagged depending on pattern
        self.assertIn('check', result)
    
    def test_full_validation(self):
        """Test complete email validation"""
        result = self.checker.validate_email("test@gmail.com")
        self.assertIn('valid', result)
        self.assertIn('score', result)
        self.assertIn('checks', result)
        self.assertEqual(len(result['checks']), 5)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```powershell
cd backend
python -m unittest test_checker.py
```

---

## Integration Testing

### API Endpoint Tests

Create `backend/test_api.py`:

```python
import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_validate_endpoint_success(self):
        """Test successful validation"""
        response = self.app.post(
            '/api/validate',
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('valid', data)
        self.assertIn('score', data)
    
    def test_validate_endpoint_missing_email(self):
        """Test validation with missing email"""
        response = self.app.post(
            '/api/validate',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_batch_validate(self):
        """Test batch validation"""
        response = self.app.post(
            '/api/batch-validate',
            data=json.dumps({'emails': ['test@example.com', 'user@test.com']}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 2)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```powershell
python -m unittest backend/test_api.py
```

---

## Manual Testing Checklist

### Functional Tests

#### Valid Email Tests
- [ ] `user@gmail.com` - Should pass all checks
- [ ] `john.doe@company.com` - Should pass all checks
- [ ] `test+tag@example.co.uk` - Should pass all checks

#### Invalid Format Tests
- [ ] `invalid-email` - Format check should fail
- [ ] `@example.com` - Format check should fail
- [ ] `user@` - Format check should fail
- [ ] `user@.com` - Format check should fail

#### Domain Tests
- [ ] `user@nonexistentdomain12345.com` - Domain check should fail
- [ ] `user@invaliddomain999.xyz` - Domain check should fail

#### Disposable Email Tests
- [ ] `test@tempmail.com` - Disposable check should fail
- [ ] `user@guerrillamail.com` - Disposable check should fail
- [ ] `temp@10minutemail.com` - Disposable check should fail

#### Suspicious Pattern Tests
- [ ] `test12345@gmail.com` - May flag suspicious
- [ ] `fake123@yahoo.com` - Should flag suspicious
- [ ] `asdfasdf@hotmail.com` - Should flag suspicious

### UI/UX Tests

#### Layout & Display
- [ ] Page loads correctly
- [ ] All sections visible
- [ ] No console errors
- [ ] Responsive on mobile devices
- [ ] Responsive on tablets
- [ ] Works on desktop (1920x1080)

#### Input Validation
- [ ] Empty input shows error
- [ ] Email input accepts text
- [ ] Enter key triggers validation
- [ ] Button click triggers validation

#### Results Display
- [ ] Results section appears after validation
- [ ] Score bar animates correctly
- [ ] All 5 checks display
- [ ] Valid/invalid badges show correctly
- [ ] JSON output displays properly
- [ ] Copy button works

#### Error Handling
- [ ] Backend offline shows error
- [ ] Network error shows message
- [ ] Invalid JSON handled gracefully
- [ ] Timeout handled properly

---

## Performance Testing

### Load Testing with Python

Create `test_load.py`:

```python
import requests
import time
import statistics

API_URL = "http://localhost:5000/api/validate"
NUM_REQUESTS = 100

def test_load():
    times = []
    
    for i in range(NUM_REQUESTS):
        start = time.time()
        response = requests.post(API_URL, json={"email": f"test{i}@gmail.com"})
        end = time.time()
        
        times.append(end - start)
        
        if response.status_code != 200:
            print(f"Request {i} failed: {response.status_code}")
    
    print(f"\n=== Load Test Results ({NUM_REQUESTS} requests) ===")
    print(f"Average: {statistics.mean(times):.3f}s")
    print(f"Median: {statistics.median(times):.3f}s")
    print(f"Min: {min(times):.3f}s")
    print(f"Max: {max(times):.3f}s")
    print(f"Std Dev: {statistics.stdev(times):.3f}s")

if __name__ == "__main__":
    test_load()
```

Run: `python test_load.py`

---

## Browser Compatibility Testing

Test in multiple browsers:
- [ ] Google Chrome (latest)
- [ ] Mozilla Firefox (latest)
- [ ] Microsoft Edge (latest)
- [ ] Safari (if available)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

---

## Security Testing

### Input Validation
- [ ] SQL injection attempts blocked
- [ ] XSS attempts sanitized
- [ ] Very long inputs handled
- [ ] Special characters handled
- [ ] Unicode characters handled

### API Security
- [ ] CORS configured correctly
- [ ] Rate limiting (if implemented)
- [ ] No sensitive data in responses
- [ ] Error messages don't leak info

---

## Test Email Addresses Database

### Known Good Addresses
```
gmail.com domain:
- test@gmail.com
- user@gmail.com

yahoo.com domain:
- test@yahoo.com
- user@yahoo.com

outlook.com domain:
- test@outlook.com
- user@outlook.com
```

### Known Disposable
```
- test@tempmail.com
- user@guerrillamail.com
- temp@10minutemail.com
- spam@mailinator.com
```

### Known Invalid Domains
```
- user@nonexistentdomain12345.com
- test@invaliddomain999.xyz
- fake@thisdoesnotexist.com
```

---

## Automated Testing Script

Complete test runner `run_all_tests.py`:

```python
import subprocess
import sys

def run_test(command, description):
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print('='*60)
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"❌ {description} FAILED")
        return False
    else:
        print(f"✅ {description} PASSED")
        return True

def main():
    tests = [
        ("python -m unittest backend/test_checker.py", "Unit Tests"),
        ("python -m unittest backend/test_api.py", "API Tests"),
        ("python test_load.py", "Load Tests")
    ]
    
    results = []
    for command, description in tests:
        results.append(run_test(command, description))
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Total: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

Run all tests: `python run_all_tests.py`

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
    
    - name: Run tests
      run: |
        python -m unittest discover -s backend -p 'test_*.py'
```

---

## Test Coverage

Install coverage tool:
```powershell
pip install coverage
```

Run with coverage:
```powershell
coverage run -m unittest discover
coverage report
coverage html
```

Open `htmlcov/index.html` to view detailed coverage report.

---

## Acceptance Criteria

Before deployment, ensure:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Manual testing checklist complete
- [ ] No console errors
- [ ] Works in all major browsers
- [ ] Responsive design verified
- [ ] API returns correct responses
- [ ] Error handling works properly
- [ ] Performance is acceptable (<3s per validation)
- [ ] Documentation is complete

---

**Testing is crucial for production readiness!**
