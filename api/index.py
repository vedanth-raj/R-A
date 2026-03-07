"""
Vercel-compatible version of web_app.py
Full Flask application for AI Research Agent
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the main Flask app from web_app.py
from web_app import app

# Export for Vercel
application = app

# For local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
