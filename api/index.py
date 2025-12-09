"""
Vercel serverless function handler for MailSpectre backend
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import re

# Create Flask app
app = Flask(__name__)
CORS(app)

# Try to import the full checker, fall back to basic validation
checker = None
import_error = None

try:
    # Add backend directory to Python path
    api_dir = os.path.dirname(os.path.abspath(__file__))
    backend_path = os.path.abspath(os.path.join(api_dir, '..', 'backend'))
    sys.path.insert(0, backend_path)
    
    from checker import EmailChecker
    checker = EmailChecker()
except Exception as e:
    import_error = str(e)


def basic_validate(email):
    """Basic email validation fallback"""
    result = {
        'valid': False,
        'email': email,
        'checks': {}
    }
    
    # Basic format check
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        result['valid'] = True
        result['checks']['format'] = {
            'passed': True,
            'message': 'Valid email format'
        }
    else:
        result['checks']['format'] = {
            'passed': False,
            'message': 'Invalid email format'
        }
    
    return result


@app.route('/api/validate', methods=['POST', 'OPTIONS'])
def validate_email():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'valid': False, 'error': 'Email is required', 'checks': {}}), 400
        
        email = data['email'].strip()
        
        # Use full checker if available, otherwise basic validation
        if checker:
            result = checker.validate(email)
        else:
            result = basic_validate(email)
            result['warning'] = f'Using basic validation. Full checker unavailable: {import_error}'
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e),
            'checks': {}
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok' if checker else 'fallback',
        'checker_loaded': checker is not None,
        'error': import_error,
        'python_path': sys.path[:3]
    })


# For Vercel
handler = app
