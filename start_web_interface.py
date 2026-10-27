#!/usr/bin/env python3
"""
AI Research Agent Web Interface Launcher
Simple script to start the web interface with proper setup
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding for Unicode characters
try:
    from utils.encoding_fix import fix_console_encoding
    fix_console_encoding()
except ImportError:
    # Fallback if utils module not available
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'flask_socketio', 'psutil']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        'templates',
        'static/css',
        'static/js',
        'data/extracted_texts',
        'Downloaded_pdfs',
        'data/section_analysis'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure ready!")

def main():
    """Main launcher function"""
    print("🚀 AI Research Agent - Web Interface Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check if web app exists
    if not Path('web_app.py').exists():
        print("❌ web_app.py not found. Please ensure you're in the correct directory.")
        sys.exit(1)
    
    print("\n🌐 Starting AI Research Agent Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🎨 Dark-themed interface will be available!")
    print("\n⚡ Features available:")
    print("   🔍 Search research papers")
    print("   📄 Extract text from PDFs")
    print("   🔬 Analyze paper content")
    print("   ⚖️ Compare multiple papers")
    print("   📊 View detailed results")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the web app
        from web_app import app, socketio
        socketio.run(app, debug=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Research Agent...")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
