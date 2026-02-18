"""
Ngrok Deployment Script for AI Research Agent
Runs the Flask app and creates a public ngrok tunnel
"""

import subprocess
import sys
import os
import time
from threading import Thread

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok_instructions():
    """Print instructions to install ngrok"""
    print("\n" + "="*60)
    print("NGROK NOT FOUND - Installation Instructions")
    print("="*60)
    print("\n1. Download ngrok from: https://ngrok.com/download")
    print("2. Extract the ngrok.exe file")
    print("3. Move ngrok.exe to this project folder OR add to PATH")
    print("4. Sign up at https://ngrok.com to get your auth token")
    print("5. Run: ngrok config add-authtoken YOUR_TOKEN")
    print("\nAlternatively, if you have ngrok.exe in this folder:")
    print("Run: .\\ngrok.exe http 5000")
    print("="*60 + "\n")

def run_flask_app():
    """Run the Flask application"""
    print("Starting Flask application...")
    # Use web_app.py which has full features including SocketIO
    subprocess.run([sys.executable, 'web_app.py'])

def run_ngrok():
    """Run ngrok tunnel"""
    print("Starting ngrok tunnel on port 5000...")
    subprocess.run(['ngrok', 'http', '5000'])

def main():
    print("\n" + "="*60)
    print("AI Research Agent - Ngrok Deployment")
    print("="*60 + "\n")
    
    # Check if ngrok is installed
    if not check_ngrok():
        install_ngrok_instructions()
        
        # Check if ngrok.exe exists in current directory
        if os.path.exists('ngrok.exe'):
            print("Found ngrok.exe in current directory!")
            print("\nStarting deployment...\n")
        else:
            print("Please install ngrok first, then run this script again.")
            return
    
    print("Ngrok is installed!\n")
    print("Starting deployment...")
    print("\nIMPORTANT:")
    print("1. Flask app will start on http://localhost:5000")
    print("2. Ngrok will create a public URL (look for 'Forwarding' line)")
    print("3. Share the ngrok URL to access your app from anywhere")
    print("4. Press Ctrl+C to stop both services\n")
    
    time.sleep(2)
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("Waiting for Flask to start...")
    time.sleep(5)
    
    # Start ngrok (this will block)
    try:
        run_ngrok()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        print("Deployment stopped.")

if __name__ == '__main__':
    main()
