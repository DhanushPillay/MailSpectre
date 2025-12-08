"""
MailSpectre Flask Backend
Email validation API server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from checker import EmailChecker
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize email checker
email_checker = EmailChecker()


@app.route('/')
def index():
    """Health check endpoint."""
    return jsonify({
        'service': 'MailSpectre',
        'version': '1.0.0',
        'status': 'running',
        'description': 'Email validation API'
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Detailed health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'MailSpectre API',
        'timestamp': '2025-12-08'
    })


@app.route('/api/validate', methods=['POST', 'OPTIONS'])
def validate_email():
    """
    Validate an email address.
    
    Expects JSON payload:
    {
        "email": "user@example.com"
    }
    
    Returns validation results with all checks.
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            logger.warning('No JSON data received')
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must be JSON with an email field'
            }), 400
        
        email = data.get('email')
        
        if not email:
            logger.warning('No email field in request')
            return jsonify({
                'error': 'Missing email field',
                'message': 'Please provide an email address to validate'
            }), 400
        
        if not isinstance(email, str):
            logger.warning(f'Invalid email type: {type(email)}')
            return jsonify({
                'error': 'Invalid email type',
                'message': 'Email must be a string'
            }), 400
        
        # Log the validation request
        logger.info(f'Validating email: {email}')
        
        # Perform validation
        result = email_checker.validate_email(email)
        
        # Log the result
        logger.info(f'Validation result for {email}: valid={result["valid"]}, score={result["score"]}')
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f'Validation error: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred during validation',
            'details': str(e)
        }), 500


@app.route('/api/batch-validate', methods=['POST', 'OPTIONS'])
def batch_validate():
    """
    Validate multiple email addresses at once.
    
    Expects JSON payload:
    {
        "emails": ["user1@example.com", "user2@example.com"]
    }
    
    Returns validation results for all emails.
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must be JSON with an emails array'
            }), 400
        
        emails = data.get('emails', [])
        
        if not isinstance(emails, list):
            return jsonify({
                'error': 'Invalid format',
                'message': 'Emails must be an array'
            }), 400
        
        if len(emails) == 0:
            return jsonify({
                'error': 'Empty list',
                'message': 'Please provide at least one email address'
            }), 400
        
        if len(emails) > 50:
            return jsonify({
                'error': 'Too many emails',
                'message': 'Maximum 50 emails per request'
            }), 400
        
        logger.info(f'Batch validating {len(emails)} emails')
        
        # Validate all emails
        results = []
        for email in emails:
            result = email_checker.validate_email(email)
            results.append(result)
        
        return jsonify({
            'total': len(emails),
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f'Batch validation error: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred during batch validation',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f'Internal server error: {str(e)}', exc_info=True)
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Starting MailSpectre on port {port}')
    logger.info(f'Debug mode: {debug}')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
