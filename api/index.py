"""
Vercel serverless function handler for MailSpectre backend
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Create Flask app first
app = Flask(__name__)
CORS(app)

# Try to import the checker
checker = None
import_error = None

try:
    # Add backend directory to Python path
    backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend')
    sys.path.insert(0, backend_path)
    
    # Import checker
    from checker import EmailChecker
    checker = EmailChecker()
except Exception as e:
    import_error = str(e)

@app.route('/api/validate', methods=['POST', 'OPTIONS'])
def validate_email():
    # Handle preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    # Check if checker loaded
    if checker is None:
        return jsonify({
            'valid': False,
            'error': f'Backend initialization error: {import_error}',
            'checks': {}
        }), 500
    
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'valid': False, 'error': 'Email is required', 'checks': {}}), 400
        
        email = data['email'].strip()
        result = checker.validate(email)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Validation error: {str(e)}',
            'checks': {}
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok' if checker else 'error',
        'error': import_error
    })

# Vercel handler
handler = app
