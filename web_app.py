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
from lengthy_draft_generator import LengthyDraftGenerator
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
        self.draft_generator = LengthyDraftGenerator()
        
    def search_papers(self, query, max_papers=5, year_start=None, year_end=None):
        """Search for papers with optimized performance"""
        try:
            import subprocess
            
            # main.py supports: topic, --max-papers, --randomize, --diversity (no year filters)
            cmd = ["python", "main.py", query, "--max-papers", str(max_papers)]
            # year_start/year_end not passed - main.py does not support them yet
            
            # Add timeout and optimize execution
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=60,  # 60 second timeout
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Search completed successfully"}
            else:
                return {"success": False, "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Search timed out. Please try again."}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_text_from_pdfs(self):
        """Extract text from all downloaded PDFs (checks data/papers then Downloaded_pdfs)"""
        try:
            from paper_retrieval.text_extractor import process_downloaded_pdfs
            # Use data/papers (where main.py saves PDFs); fallback to Downloaded_pdfs
            for pdf_dir in ["data/papers", "Downloaded_pdfs"]:
                if Path(pdf_dir).exists() and list(Path(pdf_dir).glob("*.pdf")):
                    results = process_downloaded_pdfs(downloaded_dir=pdf_dir)
                    count = len(results.get("success", []))
                    return {"success": True, "extracted_count": count, "directory": pdf_dir}
            # No PDFs in either directory
            return {"success": True, "extracted_count": 0, "message": "No PDFs found in data/papers or Downloaded_pdfs"}
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
    
    def get_downloaded_papers(self):
        """Get list of downloaded PDF papers"""
        try:
            # Check both possible directories
            papers_dirs = [Path("data/papers"), Path("Downloaded_pdfs")]
            papers = []
            
            for papers_dir in papers_dirs:
                if papers_dir.exists():
                    for file_path in papers_dir.glob("*.pdf"):
                        paper_name = file_path.stem
                        papers.append({
                            "name": paper_name,
                            "file": str(file_path),
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime,
                            "directory": str(papers_dir.name)
                        })
            
            return {"papers": sorted(papers, key=lambda x: x["modified"], reverse=True)}
        except Exception as e:
            return {"papers": [], "error": str(e)}
    
    def get_search_results(self):
        """Get recent search results"""
        try:
            # This would typically read from a database or recent search cache
            # For now, we'll return the downloaded papers as search results
            return self.get_downloaded_papers()
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
    
    def generate_draft(self, papers_data, section_type="abstract", topic=""):
        """Generate lengthy draft from selected papers using Gemini"""
        try:
            # Convert papers data to format expected by lengthy draft generator
            papers_for_draft = []
            
            for paper in papers_data:
                paper_info = {
                    'title': paper.get('title', ''),
                    'content': paper.get('content', ''),
                    'sections': paper.get('sections', [])
                }
                papers_for_draft.append(paper_info)
            
            # Generate draft using LengthyDraftGenerator
            if section_type == "abstract":
                draft_content = self.draft_generator.generate_lengthy_abstract(topic, papers_for_draft)
            elif section_type == "introduction":
                draft_content = self.draft_generator.generate_lengthy_introduction(topic, papers_for_draft)
            elif section_type == "methodology":
                draft_content = self.draft_generator.generate_lengthy_methods(topic, papers_for_draft)
            elif section_type == "results":
                draft_content = self.draft_generator.generate_lengthy_results(topic, papers_for_draft)
            elif section_type == "discussion":
                draft_content = self.draft_generator.generate_lengthy_discussion(topic, papers_for_draft)
            elif section_type == "references":
                draft_content = self.draft_generator.generate_apa_references(papers_for_draft)
            else:
                return {"success": False, "error": f"Unsupported section type: {section_type}"}
            
            if draft_content:
                return {
                    "success": True,
                    "draft": {
                        "section_type": section_type,
                        "title": f"{section_type.title()} Section",
                        "content": draft_content,
                        "word_count": len(draft_content.split()),
                        "confidence_score": 0.85,  # Default confidence for lengthy drafts
                        "sources_used": [paper.get('title', '') for paper in papers_for_draft],
                        "generated_at": datetime.now().isoformat()
                    }
                }
            else:
                return {"success": False, "error": "Failed to generate draft"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_comprehensive_draft(self, papers_data, topic="", sections=["abstract", "introduction", "methodology", "results", "discussion", "references"]):
        """Generate comprehensive lengthy draft with multiple sections"""
        try:
            # Convert papers data to format expected by lengthy draft generator
            papers_for_draft = []
            
            for paper in papers_data:
                paper_info = {
                    'title': paper.get('title', ''),
                    'content': paper.get('content', ''),
                    'sections': paper.get('sections', [])
                }
                papers_for_draft.append(paper_info)
            
            # Generate complete draft using LengthyDraftGenerator
            complete_draft = self.draft_generator.generate_complete_draft(topic, papers_for_draft)
            
            if complete_draft:
                return {"success": True, "drafts": complete_draft}
            else:
                return {"success": False, "error": "Failed to generate comprehensive draft"}
            
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

@app.route('/api/view_papers_directory')
def view_papers_directory():
    """View papers directory API endpoint"""
    try:
        papers_dir = Path("data/papers")
        if not papers_dir.exists():
            return jsonify({"papers": [], "message": "Papers directory not found"})
        
        papers = []
        for file_path in papers_dir.glob("*.pdf"):
            paper_name = file_path.stem
            papers.append({
                "name": paper_name,
                "file": str(file_path),
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
                "filename": file_path.name
            })
        
        return jsonify({
            "papers": sorted(papers, key=lambda x: x["modified"], reverse=True),
            "directory": str(papers_dir),
            "total_count": len(papers)
        })
    except Exception as e:
        return jsonify({"papers": [], "error": str(e)})

@app.route('/api/get_downloaded_papers')
def get_downloaded_papers():
    """Get downloaded PDF papers API endpoint"""
    result = web_interface.get_downloaded_papers()
    return jsonify(result)

@app.route('/api/get_search_results')
def get_search_results():
    """Get search results API endpoint"""
    result = web_interface.get_search_results()
    return jsonify(result)

@app.route('/api/extract_selected_paper', methods=['POST'])
def extract_selected_paper():
    """Extract text from selected paper API endpoint"""
    data = request.json
    paper_file = data.get('paper_file')
    
    if not paper_file:
        return jsonify({"success": False, "error": "Paper file not specified"})
    
    operation_id = f"extract_selected_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_selected_extraction():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Extracting text from selected paper: {Path(paper_file).stem}',
                'progress': 10
            })
            
            # Extract text from specific PDF
            extractor = PDFTextExtractor()
            result = extractor.extract_text_from_pdf(paper_file)
            
            if result:
                # Save extracted text
                output_dir = Path("data/extracted_texts")
                output_dir.mkdir(exist_ok=True)
                
                paper_name = Path(paper_file).stem
                output_file = output_dir / f"{paper_name}_extracted.txt"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result['full_text'])
                
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": {
                        "success": True,
                        "extracted_file": str(output_file),
                        "metadata": result['metadata']
                    }
                }
                
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': f'Text extraction completed for {paper_name}',
                    'progress': 100,
                    'result': {
                        "success": True,
                        "extracted_file": str(output_file),
                        "metadata": result['metadata']
                    }
                })
            else:
                active_operations[operation_id] = {
                    "status": "error",
                    "error": "Failed to extract text from PDF"
                }
                
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'error',
                    'message': 'Failed to extract text from PDF',
                    'error': 'Failed to extract text from PDF'
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
    thread = threading.Thread(target=run_selected_extraction)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/download_paper/<path:filename>')
def download_paper(filename):
    """Download paper API endpoint"""
    try:
        # Check both possible directories
        papers_dirs = [Path("data/papers"), Path("Downloaded_pdfs")]
        
        for papers_dir in papers_dirs:
            file_path = papers_dir / filename
            if file_path.exists():
                return send_file(str(file_path), as_attachment=True)
        
        return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@app.route('/api/generate_draft', methods=['POST'])
def generate_draft():
    """Generate lengthy draft from selected papers API endpoint"""
    data = request.json
    paper_files = data.get('paper_files', [])
    section_type = data.get('section_type', 'abstract')
    topic = data.get('topic', 'Research Paper')
    
    if not paper_files:
        return jsonify({"success": False, "error": "No papers selected for draft generation"})
    
    operation_id = f"draft_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_draft_generation():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Generating {section_type} draft from {len(paper_files)} papers...',
                'progress': 10
            })
            
            # Load paper data
            papers_data = []
            for paper_file in paper_files:
                try:
                    if paper_file.endswith('_sections.json'):
                        # Load section data
                        with open(paper_file, 'r', encoding='utf-8') as f:
                            section_data = json.load(f)
                            papers_data.append({
                                'title': section_data.get('metadata', {}).get('title', ''),
                                'content': '\n'.join([s.get('content', '') for s in section_data.get('sections', [])]),
                                'sections': section_data.get('sections', [])
                            })
                    else:
                        # Load extracted text
                        with open(paper_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            papers_data.append({
                                'title': Path(paper_file).stem.replace('_extracted', ''),
                                'content': content,
                                'sections': []
                            })
                except Exception as e:
                    print(f"Error loading paper {paper_file}: {e}")
                    continue
            
            if not papers_data:
                raise Exception("No valid paper data loaded")
            
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': 'Processing paper content...',
                'progress': 40
            })
            
            # Generate draft using LengthyDraftGenerator
            result = web_interface.generate_draft(papers_data, section_type, topic)
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': f'{section_type.title()} draft generated successfully',
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
                    'message': f'Draft generation failed: {result["error"]}',
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
                'message': f'Draft generation failed: {str(e)}',
                'error': str(e)
            })
    
    # Run draft generation in background
    thread = threading.Thread(target=run_draft_generation)
    thread.daemon = True
    thread.start()
    
    return jsonify({"operation_id": operation_id, "status": "started"})

@app.route('/api/generate_comprehensive_draft', methods=['POST'])
def generate_comprehensive_draft():
    """Generate comprehensive lengthy draft with multiple sections API endpoint"""
    data = request.json
    paper_files = data.get('paper_files', [])
    sections = data.get('sections', ['abstract', 'introduction', 'methodology', 'results', 'discussion', 'references'])
    topic = data.get('topic', 'Research Paper')
    
    if not paper_files:
        return jsonify({"success": False, "error": "No papers selected for draft generation"})
    
    operation_id = f"comprehensive_draft_{int(time.time())}"
    active_operations[operation_id] = {"status": "running", "progress": 0}
    
    def run_comprehensive_draft():
        try:
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': f'Generating comprehensive draft from {len(paper_files)} papers...',
                'progress': 5
            })
            
            # Load paper data
            papers_data = []
            for paper_file in paper_files:
                try:
                    if paper_file.endswith('_sections.json'):
                        with open(paper_file, 'r', encoding='utf-8') as f:
                            section_data = json.load(f)
                            papers_data.append({
                                'title': section_data.get('metadata', {}).get('title', ''),
                                'content': '\n'.join([s.get('content', '') for s in section_data.get('sections', [])]),
                                'sections': section_data.get('sections', [])
                            })
                    else:
                        with open(paper_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            papers_data.append({
                                'title': Path(paper_file).stem.replace('_extracted', ''),
                                'content': content,
                                'sections': []
                            })
                except Exception as e:
                    print(f"Error loading paper {paper_file}: {e}")
                    continue
            
            if not papers_data:
                raise Exception("No valid paper data loaded")
            
            # Generate comprehensive draft using LengthyDraftGenerator
            socketio.emit('operation_update', {
                'operation_id': operation_id,
                'status': 'running',
                'message': 'Generating comprehensive draft...',
                'progress': 20
            })
            
            result = web_interface.generate_comprehensive_draft(papers_data, topic, sections)
            
            if result["success"]:
                active_operations[operation_id] = {
                    "status": "completed",
                    "progress": 100,
                    "result": result
                }
                socketio.emit('operation_update', {
                    'operation_id': operation_id,
                    'status': 'completed',
                    'message': 'Comprehensive draft generated successfully',
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
                    'message': f'Comprehensive draft generation failed: {result["error"]}',
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
                'message': f'Comprehensive draft generation failed: {str(e)}',
                'error': str(e)
            })
    
    # Run comprehensive draft generation in background
    thread = threading.Thread(target=run_comprehensive_draft)
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
