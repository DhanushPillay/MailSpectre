"""
Vercel serverless function handler for MailSpectre backend
Full validation with all checks
"""
from flask import Flask, request, jsonify
import re
import hashlib

# Create Flask app
app = Flask(__name__)

# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ============ DATA CONSTANTS ============

DISPOSABLE_DOMAINS = {
    'tempmail.com', 'guerrillamail.com', '10minutemail.com', 'mailinator.com',
    'throwaway.email', 'temp-mail.org', 'fakeinbox.com', 'maildrop.cc',
    'getnada.com', 'trashmail.com', 'yopmail.com', 'sharklasers.com',
    'guerrillamailblock.com', 'grr.la', 'mintemail.com', 'tempmail.net',
    'dispostable.com', 'mailnesia.com', 'spambox.us', 'mohmal.com'
}

SUSPICIOUS_PATTERNS = [
    r'test\d+@', r'fake\d*@', r'spam\d*@', r'trash\d*@', r'temp\d*@',
    r'dummy\d*@', r'asdf', r'qwerty', r'12345', r'[a-z]{20,}', r'^\d+@',
]

MAJOR_PROVIDERS = {
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com',
    'msn.com', 'aol.com', 'icloud.com', 'protonmail.com', 'mail.com',
    'yahoo.co.uk', 'yahoo.ca', 'yahoo.fr', 'hotmail.co.uk', 'googlemail.com'
}

SUSPICIOUS_TLDS = {
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click',
    '.link', '.download', '.racing', '.loan', '.win', '.bid', '.stream',
    '.science', '.party', '.review', '.trade'
}

EDU_DOMAINS = {
    '.edu', '.ac.uk', '.edu.au', '.edu.in', '.edu.cn', '.edu.sg',
    '.ac.in', '.ac.jp', '.edu.my', '.edu.pk', '.edu.bd', '.edu.np',
    '.ac.za', '.edu.eg', '.edu.sa', '.edu.ae', '.ac.nz', '.ac.th'
}

DOMAIN_TYPOS = {
    'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com', 'gmil.com': 'gmail.com',
    'gmail.co': 'gmail.com', 'gmail.cm': 'gmail.com', 'gmaill.com': 'gmail.com',
    'yahooo.com': 'yahoo.com', 'yaho.com': 'yahoo.com', 'yahoo.co': 'yahoo.com',
    'hotmial.com': 'hotmail.com', 'hotmal.com': 'hotmail.com', 'hotmail.co': 'hotmail.com',
    'outlok.com': 'outlook.com', 'outloo.com': 'outlook.com', 'outlook.co': 'outlook.com',
}

WORK_KEYWORDS = {
    'info', 'contact', 'support', 'admin', 'sales', 'help', 'service',
    'team', 'office', 'business', 'corporate', 'hr', 'recruitment'
}


# ============ VALIDATION FUNCTIONS ============

def check_format(email):
    """Check email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(email_regex, email))
    return {
        'check': 'format',
        'valid': is_valid,
        'message': 'Valid email format' if is_valid else 'Invalid email format'
    }


def check_disposable(email):
    """Check if using disposable email domain"""
    domain = email.split('@')[1].lower()
    is_disposable = domain in DISPOSABLE_DOMAINS
    return {
        'check': 'disposable',
        'valid': not is_disposable,
        'message': 'Disposable email detected' if is_disposable else 'Not a disposable email'
    }


def check_suspicious_patterns(email):
    """Check for suspicious patterns in email"""
    email_lower = email.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, email_lower):
            return {
                'check': 'suspicious_patterns',
                'valid': False,
                'message': 'Suspicious pattern detected'
            }
    return {
        'check': 'suspicious_patterns',
        'valid': True,
        'message': 'No suspicious patterns found'
    }


def check_suspicious_tld(email):
    """Check for suspicious TLDs"""
    domain = email.split('@')[1].lower()
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            return {
                'check': 'suspicious_tld',
                'valid': False,
                'message': f'Suspicious TLD detected: {tld}',
                'risk_level': 'high'
            }
    return {
        'check': 'suspicious_tld',
        'valid': True,
        'message': 'TLD appears safe'
    }


def check_typo_suggestion(email):
    """Check for common typos in domain"""
    domain = email.split('@')[1].lower()
    if domain in DOMAIN_TYPOS:
        suggestion = DOMAIN_TYPOS[domain]
        username = email.split('@')[0]
        return {
            'check': 'typo_detection',
            'valid': False,
            'message': f'Possible typo detected',
            'suggestion': f'{username}@{suggestion}',
            'typo_domain': domain,
            'correct_domain': suggestion
        }
    return {
        'check': 'typo_detection',
        'valid': True,
        'message': 'No typos detected'
    }


def check_username_quality(email):
    """Analyze username quality"""
    username = email.split('@')[0].lower()
    issues = []
    risk_score = 0
    
    # Check for keyboard patterns
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'qazwsx', '123456', 'abcdef']
    for pattern in keyboard_patterns:
        if pattern in username:
            issues.append(f'Keyboard pattern: {pattern}')
            risk_score += 25
    
    # Check for excessive numbers
    numbers = re.findall(r'\d+', username)
    if numbers:
        total_digits = sum(len(n) for n in numbers)
        if total_digits > len(username) * 0.5:
            issues.append('Excessive numbers')
            risk_score += 20
    
    # Check for random-looking strings
    consonant_clusters = re.findall(r'[bcdfghjklmnpqrstvwxyz]{4,}', username)
    if consonant_clusters:
        issues.append('Random character sequences')
        risk_score += 30
    
    # Check length
    if len(username) < 3:
        issues.append('Username too short')
        risk_score += 15
    elif len(username) > 30:
        issues.append('Username suspiciously long')
        risk_score += 20
    
    is_valid = risk_score < 50
    
    return {
        'check': 'username_quality',
        'valid': is_valid,
        'message': 'Username appears legitimate' if is_valid else 'Username appears suspicious',
        'risk_score': risk_score,
        'issues': issues if issues else None
    }


def classify_email_type(email):
    """Classify email as Student, Work, Personal, or Temporary"""
    domain = email.split('@')[1].lower()
    username = email.split('@')[0].lower()
    
    # Check for disposable/temporary
    if domain in DISPOSABLE_DOMAINS:
        return {
            'check': 'email_type',
            'valid': True,
            'message': 'Temporary/Disposable Email',
            'email_type': 'Temporary',
            'confidence': 100
        }
    
    # Check for educational
    for edu_domain in EDU_DOMAINS:
        if domain.endswith(edu_domain):
            return {
                'check': 'email_type',
                'valid': True,
                'message': 'Student/Educational Email',
                'email_type': 'Student',
                'confidence': 95
            }
    
    # Check for work email indicators
    if domain not in MAJOR_PROVIDERS:
        # Custom domain - likely work
        if any(kw in username for kw in WORK_KEYWORDS):
            confidence = 90
        else:
            confidence = 75
        return {
            'check': 'email_type',
            'valid': True,
            'message': 'Work/Business Email',
            'email_type': 'Work',
            'confidence': confidence
        }
    
    # Major provider - personal
    return {
        'check': 'email_type',
        'valid': True,
        'message': 'Personal Email',
        'email_type': 'Personal',
        'confidence': 85
    }


def validate_email(email):
    """Run all validation checks"""
    email = email.strip().lower()
    checks = []
    
    # Run all checks
    format_check = check_format(email)
    checks.append(format_check)
    
    # Only continue if format is valid
    if not format_check['valid']:
        return {
            'valid': False,
            'email': email,
            'checks': checks
        }
    
    # Run remaining checks
    checks.append(check_disposable(email))
    checks.append(check_suspicious_tld(email))
    checks.append(check_typo_suggestion(email))
    checks.append(check_suspicious_patterns(email))
    checks.append(check_username_quality(email))
    checks.append(classify_email_type(email))
    
    # Calculate overall validity
    critical_checks = ['format', 'disposable', 'suspicious_tld']
    is_valid = all(
        c['valid'] for c in checks 
        if c['check'] in critical_checks
    )
    
    return {
        'valid': is_valid,
        'email': email,
        'checks': checks
    }


# ============ ROUTES ============

@app.route('/api/validate', methods=['POST', 'OPTIONS'])
def api_validate():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'valid': False, 'error': 'Email is required', 'checks': []}), 400
        
        result = validate_email(data['email'])
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e),
            'checks': []
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'version': 'full'})
