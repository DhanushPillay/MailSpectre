"""
Vercel serverless function handler for MailSpectre backend
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Change working directory to backend so DATA folder is accessible
os.chdir(backend_path)

try:
    from app import app
    # Vercel expects a variable named 'app' or 'handler'
    handler = app
except Exception as e:
    # If import fails, create a minimal error handler
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/validate', methods=['POST', 'GET', 'OPTIONS'])
    def error_handler():
        return jsonify({
            'valid': False,
            'error': f'Backend initialization failed: {str(e)}',
            'checks': {}
        }), 500
    
    handler = app
