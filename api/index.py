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
from paper_retrieval.searcher import SemanticScholarSearcher
from lengthy_draft_generator import LengthyDraftGenerator
from ai_conversation_engine import AIConversationEngine

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 'ai_research_agent_vercel_2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
searcher = SemanticScholarSearcher()
draft_generator = LengthyDraftGenerator()

# Session-based storage
session_data = {}

@app.route('/')
def index():
    """Render main page"""
    # Use simplified template for Vercel
    return render_template('index-vercel.html')

@app.route('/api/live_search', methods=['GET', 'POST'])
def live_search():
    """Fast live search for instant results as user types"""
    query = request.args.get('query') or (request.get_json() or {}).get('query', '')
    query = query.strip()
    if not query or len(query) < 2:
        return jsonify({"results": []})
    try:
        papers = searcher.search_papers_paginated(query, total_limit=5)
        results = []
        for p in papers:
            authors = p.authors or []
            authors_str = ", ".join([
                a.name if hasattr(a, 'name') and a.name else (a.get('name', '') if isinstance(a, dict) else str(a))
                for a in authors[:3]
            ])
            results.append({
                "title": p.title or "Untitled",
                "authors": authors_str or "Unknown Authors",
                "year": p.year or "n.d.",
                "citations": getattr(p, 'citationCount', 0) or 0,
                "abstract": (p.abstract or "")[:180] + ("..." if p.abstract and len(p.abstract) > 180 else ""),
                "has_pdf": p.has_open_pdf() if hasattr(p, 'has_open_pdf') else False,
                "pdf_url": p.get_pdf_url() if hasattr(p, 'get_pdf_url') else None
            })
        return jsonify({"results": results, "query": query})
    except Exception as e:
        return jsonify({"results": [], "error": str(e)})

@app.route('/api/search', methods=['POST'])
@app.route('/api/search_papers', methods=['POST'])
def search_papers():
    """Search for papers"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        max_results = data.get('max_results') or data.get('maxPapers') or 10
        try:
            max_results = int(max_results)
        except (ValueError, TypeError):
            max_results = 10
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform search using paginated search with fallback (arXiv / OpenAlex)
        papers = searcher.search_papers_paginated(query, total_limit=max_results)
        
        # Serialize PaperMetadata objects to JSON-serializable dictionaries
        results = []
        for p in papers:
            p_dict = p.model_dump(mode='json', exclude_none=True)
            authors = p_dict.get('authors', [])
            if isinstance(authors, list):
                p_dict['authors'] = ', '.join([
                    a.get('name', '') if isinstance(a, dict) else str(a)
                    for a in authors if a
                ])
            p_dict['hasOpenAccessPdf'] = p.has_open_pdf()
            p_dict['pdfUrl'] = p.get_pdf_url()
            results.append(p_dict)
        
        # Store in session
        session_id = request.cookies.get('session_id', str(datetime.now().timestamp()))
        session_data[session_id] = {'results': results, 'query': query}
        
        return jsonify({
            'success': True,
            'results': results,
            'papers': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_search_results', methods=['GET'])
def get_search_results_api():
    """Get search results for current or latest session"""
    session_id = request.cookies.get('session_id')
    if session_id and session_id in session_data:
        return jsonify({'papers': session_data[session_id].get('results', [])})
    for s_id in reversed(list(session_data.keys())):
        return jsonify({'papers': session_data[s_id].get('results', [])})
    return jsonify({'papers': []})

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

# For Vercel serverless deployment
if __name__ == '__main__':
    app.run(debug=True)
