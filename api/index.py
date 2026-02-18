"""
Vercel-compatible Flask API for AI Research Agent
Simple REST API without SocketIO for serverless deployment
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import our modules
from paper_retrieval.searcher import PaperSearcher
from lengthy_draft_generator import LengthyDraftGenerator
from ai_conversation_engine import AIConversationEngine

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 'ai_research_agent_vercel_2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
searcher = PaperSearcher()
draft_generator = LengthyDraftGenerator()

# Session-based storage
session_data = {}

@app.route('/')
def index():
    """Render main page"""
    # Use simplified template for Vercel
    return render_template('index-vercel.html')

@app.route('/api/search', methods=['POST'])
def search_papers():
    """Search for papers"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform search
        results = searcher.search_papers(query, max_results=max_results)
        
        # Store in session
        session_id = request.cookies.get('session_id', str(datetime.now().timestamp()))
        session_data[session_id] = {'results': results, 'query': query}
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_draft', methods=['POST'])
def generate_draft():
    """Generate research draft"""
    try:
        data = request.get_json()
        selected_papers = data.get('selected_papers', [])
        custom_instructions = data.get('custom_instructions', '')
        
        if not selected_papers:
            return jsonify({'error': 'No papers selected'}), 400
        
        # Generate draft
        draft = draft_generator.generate_comprehensive_draft(
            selected_papers,
            custom_instructions=custom_instructions
        )
        
        return jsonify({
            'success': True,
            'draft': draft
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Initialize conversation engine
        conversation_engine = AIConversationEngine()
        response = conversation_engine.process_message(message, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(debug=True)
