"""
Flask Web Application for AI Research Agent
Dark-themed interactive web interface for the research paper analysis tool
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit
import json
import os
import sys
import threading
import time
from pathlib import Path
from datetime import datetime
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from paper_retrieval.text_extractor import PDFTextExtractor
from section_extractor import SectionWiseExtractor
from section_analyzer import SectionAnalyzer
from advanced_text_processor import AdvancedTextProcessor
from error_handler import handle_error, safe_execute
from performance_monitor import monitor_performance

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai_research_agent_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for tracking operations
active_operations = {}
operation_results = {}

class WebInterface:
    """Main web interface class"""
    
    def __init__(self):
        self.pdf_extractor = PDFTextExtractor()
        self.section_extractor = SectionWiseExtractor()
        self.section_analyzer = SectionAnalyzer()
        self.text_processor = AdvancedTextProcessor()
        
    def search_papers(self, query, max_papers=5, year_start=None, year_end=None):
        """Search for papers"""
        try:
            import subprocess
            
            cmd = ["python", "main.py", query, "--max-papers", str(max_papers)]
            if year_start:
                cmd.extend(["--year-start", str(year_start)])
            if year_end:
                cmd.extend(["--year-end", str(year_end)])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": "Search completed successfully"}
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_text_from_pdfs(self):
        """Extract text from all downloaded PDFs"""
        try:
            from paper_retrieval.text_extractor import process_downloaded_pdfs
            results = process_downloaded_pdfs()
            return {"success": True, "extracted_count": len(results)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_papers(self):
        """Get list of available extracted papers"""
        try:
            papers_dir = Path("data/extracted_texts")
            if not papers_dir.exists():
                return {"papers": []}
            
            papers = []
            for file_path in papers_dir.glob("*_extracted.txt"):
                paper_name = file_path.stem.replace("_extracted", "")
                papers.append({
                    "name": paper_name,
                    "file": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                })
            
            return {"papers": sorted(papers, key=lambda x: x["modified"], reverse=True)}
        except Exception as e:
            return {"papers": [], "error": str(e)}
    
    def analyze_paper(self, paper_file):
        """Analyze a specific paper"""
        try:
            # Read the paper text
            with open(paper_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract sections
            sections = self.section_extractor.detect_sections_from_text(content)
            
            # Advanced text analysis
            text_analysis = self.text_processor.process_text_comprehensive(content)
            
            # Section analysis
            section_data = {
                'sections': [
                    {
                        'title': s.title,
                        'content': s.content,
                        'type': s.section_type,
                        'word_count': s.word_count,
                        'start_page': getattr(s, 'start_page', 1),
                        'end_page': getattr(s, 'end_page', 1)
                    }
                    for s in sections
                ],
                'metadata': {'source_file': paper_file}
            }
            
            section_analysis = self.section_analyzer.analyze_section_distribution(section_data)
            key_insights = self.section_analyzer.extract_key_insights(section_data)
            
            return {
                "success": True,
                "sections": [vars(s) for s in sections],
                "text_analysis": text_analysis,
                "section_analysis": section_analysis,
                "key_insights": key_insights,
                "total_sections": len(sections),
                "total_words": sum(s.word_count for s in sections)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compare_papers(self, paper_files):
        """Compare multiple papers"""
        try:
            # Create section data files for comparison
            section_files = []
            
            for paper_file in paper_files:
                with open(paper_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                sections = self.section_extractor.detect_sections_from_text(content)
                
                section_data = {
                    'sections': [
                        {
                            'title': s.title,
                            'content': s.content,
                            'type': s.section_type,
                            'word_count': s.word_count
                        }
                        for s in sections
                    ],
                    'metadata': {
                        'source_file': paper_file,
                        'total_sections': len(sections)
                    }
                }
                
                # Save temporary section file
                temp_file = paper_file.replace('_extracted.txt', '_sections_temp.json')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(section_data, f, indent=2)
                
                section_files.append(temp_file)
            
            # Compare papers
            comparison = self.section_analyzer.compare_papers_by_sections(section_files)
            
            # Clean up temp files
            for temp_file in section_files:
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            return {"success": True, "comparison": comparison}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize web interface
web_interface = WebInterface()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/search_papers', methods=['POST'])
def search_papers():
    """Search for papers API endpoint"""
    data = request.json
    query = data.get('query', '')
    max_papers = data.get('max_papers', 5)
    year_start = data.get('year_start')
    year_end = data.get('year_end')
    
    operation_id = f"search_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_search():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Searching for papers: {query}',
                'progress': 10
            })
            
            result = web_interface.search_papers(query, max_papers, year_start, year_end)
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': 'Search completed successfully',
                    'progress': 100,
                    'result': result
                })
            else:
                active_operations[operation_id] = {
                    "status": "error",
                    "error": result["error"]
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'error',
                    'message': f'Search failed: {result["error"]}',
                    'error': result["error"]
                })
                
        except Exception as e:
            active_operations[operation_id] = {
                "status": "error",
                "error": str(e)
            }
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'error',
                'message': f'Search failed: {str(e)}',
                'error': str(e)
            })
    
    # Run search in background
    thread = threading.Thread(target=run_search)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/extract_text', methods=['POST'])
def extract_text():
    """Extract text from PDFs API endpoint"""
    operation_id = f"extract_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_extraction():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': 'Extracting text from PDFs...',
                'progress': 10
            })
            
            result = web_interface.extract_text_from_pdfs()
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': f'Text extraction completed. {result["extracted_count"]} papers processed.',
                    'progress': 100,
                    'result': result
                })
            else:
                active_operations[operation_id] = {
                    "status": "error",
                    "error": result["error"]
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'error',
                    'message': f'Extraction failed: {result["error"]}',
                    'error': result["error"]
                })
                
        except Exception as e:
            active_operations[operation_id] = {
                "status": "error",
                "error": str(e)
            }
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'error',
                'message': f'Extraction failed: {str(e)}',
                'error': str(e)
            })
    
    # Run extraction in background
    thread = threading.Thread(target=run_extraction)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/get_papers')
def get_papers():
    """Get available papers API endpoint"""
    result = web_interface.get_available_papers()
    return jsonify(result)

@app.route('/api/analyze_paper', methods=['POST'])
def analyze_paper():
    """Analyze paper API endpoint"""
    data = request.json
    paper_file = data.get('paper_file')
    
    if not paper_file:
        return jsonify({"success": False, "error": "Paper file not specified"})
    
    operation_id = f"analyze_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_analysis():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Analyzing paper: {Path(paper_file).stem}',
                'progress': 10
            })
            
            result = web_interface.analyze_paper(paper_file)
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': 'Analysis completed successfully',
                    'progress': 100,
                    'result': result
                })
            else:
                active_operations[operation_id] = {
                    "status": "error",
                    "error": result["error"]
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'error',
                    'message': f'Analysis failed: {result["error"]}',
                    'error': result["error"]
                })
                
        except Exception as e:
            active_operations[operation_id] = {
                "status": "error",
                "error": str(e)
            }
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'error',
                'message': f'Analysis failed: {str(e)}',
                'error': str(e)
            })
    
    # Run analysis in background
    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/compare_papers', methods=['POST'])
def compare_papers():
    """Compare papers API endpoint"""
    data = request.json
    paper_files = data.get('paper_files', [])
    
    if len(paper_files) < 2:
        return jsonify({"success": False, "error": "At least 2 papers required for comparison"})
    
    operation_id = f"compare_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_comparison():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Comparing {len(paper_files)} papers...',
                'progress': 10
            })
            
            result = web_interface.compare_papers(paper_files)
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': 'Comparison completed successfully',
                    'progress': 100,
                    'result': result
                })
            else:
                active_operations[operation_id] = {
                    "status": "error",
                    "error": result["error"]
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'error',
                    'message': f'Comparison failed: {result["error"]}',
                    'error': result["error"]
                })
                
        except Exception as e:
            active_operations[operation_id] = {
                "status": "error",
                "error": str(e)
            }
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'error',
                'message': f'Comparison failed: {str(e)}',
                'error': str(e)
            })
    
    # Run comparison in background
    thread = threading.Thread(target=run_comparison)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/operation_status/<operation_id>')
def operation_status(operation_id):
    """Get operation status"""
    operation = active_operations.get(operation_id)
    if operation:
        return jsonify(operation)
    else:
        return jsonify({"error": "Operation not found"}), 404

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to AI Research Agent'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Starting AI Research Agent Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🌙 Dark-themed interface ready!")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
