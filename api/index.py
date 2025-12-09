"""
Vercel serverless function handler for MailSpectre backend
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

# Vercel expects a variable named 'app' or 'handler'
# This file acts as the entry point for Vercel serverless functions
handler = app
