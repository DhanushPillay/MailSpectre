"""
Vercel serverless function handler for MailSpectre backend
Minimal version to debug deployment issues
"""
from flask import Flask, request, jsonify
import re

# Create Flask app
app = Flask(__name__)

# Add CORS headers manually to avoid flask-cors dependency issues
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def basic_validate(email):
    """Basic email validation"""
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
        result = basic_validate(email)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e),
            'checks': {}
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Basic validation only'})


# For Vercel - must be named 'app'
# Vercel Python runtime expects the WSGI app to be named 'app'
