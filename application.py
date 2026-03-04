"""
AWS Elastic Beanstalk entry point
This file is required for EB deployment
"""

from web_app import app, socketio

# Elastic Beanstalk looks for 'application' variable
application = app

if __name__ == '__main__':
    # For local testing
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
