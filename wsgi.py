"""
WSGI entry point for production deployment (Vercel, Gunicorn, etc.)
This file is used by serverless and WSGI servers to run the application.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from main
from main import app

# Export app for WSGI servers
__all__ = ['app']
