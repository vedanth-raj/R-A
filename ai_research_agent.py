"""
AI Research Agent - Complete Research Paper Generation System
Main entry point for all features: Search, Extract, Analyze, Generate, Format

Usage:
    python ai_research_agent.py --help
    python ai_research_agent.py --topic "machine learning" --max-papers 5
    python ai_research_agent.py --generate-drafts
    python ai_research_agent.py --format-apa
    python ai_research_agent.py --complete-workflow "deep learning"
"""

import argparse
import sys
import os
from pathlib import Path
import json
import logging
from datetime import datetime

# Fix Windows console encoding for Unicode characters
try:
    from utils.encoding_fix import fix_console_encoding
    fix_console_encoding()
except ImportError:
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Import all modules
from paper_retrieval.text_extractor import PDFTextExtractor
from section_extractor import SectionWiseExtractor
from section_analyzer import SectionAnalyzer, analyze_paper_sections
from enhanced_gpt_generator import EnhancedGPTDraftGenerator, generate_drafts_from_analysis
from content_reviewer import ContentReviewer, perform_full_revision_cycle
from apa_formatter import APAFormatter, generate_apa_bibliography
from final_integration import FinalIntegration, run_complete_workflow
from final_testing import run_comprehensive_tests
from final_documentation import FinalDocumentation
from web_app import WebInterface

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_research_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AIResearchAgent:
    """Complete AI Research Agent system"""
    
    def __init__(self):
        """Initialize the AI Research Agent"""
        self.logger = logging.getLogger(__name__)
        self.base_dir = Path.cwd()
        self.data_dir = self.base_dir / "data"
        
        # Ensure data directories exist
        self.data_dir.mkdir(exist_ok=True)
        (self.data_dir / "papers").mkdir(exist_ok=True)
        (self.data_dir / "extracted_texts").mkdir(exist_ok=True)
        (self.data_dir / "sections").mkdir(exist_ok=True)
        (self.data_dir / "section_analysis").mkdir(exist_ok=True)
        (self.data_dir / "drafts").mkdir(exist_ok=True)
        (self.data_dir / "references").mkdir(exist_ok=True)
        (self.data_dir / "final_output").mkdir(exist_ok=True)
        
        # Initialize components
        self.text_extractor = PDFTextExtractor()
        self.section_extractor = SectionWiseExtractor()
        self.section_analyzer = SectionAnalyzer()
        self.draft_generator = EnhancedGPTDraftGenerator(preferred_provider="gemini")
        self.content_reviewer = ContentReviewer(preferred_provider="gemini")
        self.integration = FinalIntegration()
        self.apa_formatter = APAFormatter()
        self.web_interface = WebInterface()
    
    def search_papers(self, topic: str, max_papers: int = 5) -> dict:
        """Search for papers on a topic"""
        self.logger.info(f"Searching for papers on: {topic}")
        
        try:
            import subprocess
            
            cmd = ["python", "main.py", topic, "--max-papers", str(max_papers)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info("Paper search completed successfully")
                return {"success": True, "message": "Search completed"}
            else:
                self.logger.error(f"Search failed: {result.stderr}")
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            self.logger.error(f"Error searching papers: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_text_from_papers(self) -> dict:
        """Extract text from all downloaded papers"""
        self.logger.info("Extracting text from papers...")
        
        try:
            papers_dir = self.data_dir / "papers"
            extracted_dir = self.data_dir / "extracted_texts"
            
            if not papers_dir.exists():
                return {"success": False, "error": "No papers directory found"}
            
            pdf_files = list(papers_dir.glob("*.pdf"))
            if not pdf_files:
                return {"success": False, "error": "No PDF files found"}
            
            extracted_count = 0
            for pdf_file in pdf_files:
                try:
                    result = self.text_extractor.extract_text_from_pdf(str(pdf_file))
                    if result:
                        output_file = extracted_dir / f"{pdf_file.stem}_extracted.txt"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(result['full_text'])
                        extracted_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to extract {pdf_file}: {e}")
            
            self.logger.info(f"Extracted text from {extracted_count} papers")
            return {"success": True, "extracted": extracted_count}
            
        except Exception as e:
            self.logger.error(f"Error extracting text: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_sections(self) -> dict:
        """Extract sections from extracted texts"""
        self.logger.info("Extracting sections...")
        
        try:
            extracted_dir = self.data_dir / "extracted_texts"
            sections_dir = self.data_dir / "sections"
            
            txt_files = list(extracted_dir.glob("*_extracted.txt"))
            if not txt_files:
                return {"success": False, "error": "No extracted text files found"}
            
            sections_count = 0
            for txt_file in txt_files:
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if len(content) > 100:  # Only process non-empty files
                        sections = self.section_extractor.detect_sections_from_text(content)
                        
                        # Save sections
                        sections_file = sections_dir / f"{txt_file.stem}_sections.json"
                        with open(sections_file, 'w', encoding='utf-8') as f:
                            json.dump([{
                                'title': s.title,
                                'content': s.content[:500] + '...' if len(s.content) > 500 else s.content,
                                'start_page': s.start_page,
                                'end_page': s.end_page,
                                'section_type': s.section_type,
                                'word_count': s.word_count
                            } for s in sections], f, indent=2, ensure_ascii=False)
                        
                        sections_count += 1
                        
                except Exception as e:
                    self.logger.warning(f"Failed to process {txt_file}: {e}")
            
            self.logger.info(f"Extracted sections from {sections_count} papers")
            return {"success": True, "processed": sections_count}
            
        except Exception as e:
            self.logger.error(f"Error extracting sections: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_sections(self) -> dict:
        """Analyze extracted sections"""
        self.logger.info("Analyzing sections...")
        
        try:
            sections_dir = self.data_dir / "sections"
            analysis_dir = self.data_dir / "section_analysis"
            
            sections_files = list(sections_dir.glob("*_sections.json"))
            if not sections_files:
                return {"success": False, "error": "No section files found"}
            
            analyzed_count = 0
            for sections_file in sections_files:
                try:
                    analysis = analyze_paper_sections(str(sections_file))
                    if analysis:
                        analysis_file = analysis_dir / f"{sections_file.stem}_analysis.json"
                        with open(analysis_file, 'w', encoding='utf-8') as f:
                            json.dump(analysis, f, indent=2, ensure_ascii=False)
                        analyzed_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to analyze {sections_file}: {e}")
            
            self.logger.info(f"Analyzed {analyzed_count} papers")
            return {"success": True, "analyzed": analyzed_count}
            
        except Exception as e:
            self.logger.error(f"Error analyzing sections: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_drafts(self, sections: list = None) -> dict:
        """Generate GPT-based drafts"""
        self.logger.info("Generating drafts...")
        
        try:
            analysis_dir = self.data_dir / "section_analysis"
            drafts_dir = self.data_dir / "drafts"
            
            papers_data = self.draft_generator.load_paper_data(str(analysis_dir))
            if not papers_data:
                return {"success": False, "error": "No analysis data found"}
            
            drafts = self.draft_generator.generate_complete_draft(papers_data, sections)
            
            # Save drafts
            drafts_file = drafts_dir / "generated_drafts.json"
            self.draft_generator.save_drafts(drafts, str(drafts_file))
            
            # Generate formatted paper
            paper_file = drafts_dir / "generated_paper.txt"
            self.draft_generator.generate_formatted_paper(drafts, str(paper_file))
            
            self.logger.info(f"Generated {len(drafts)} draft sections")
            return {"success": True, "drafts": len(drafts)}
            
        except Exception as e:
            self.logger.error(f"Error generating drafts: {e}")
            return {"success": False, "error": str(e)}
    
    def format_references(self) -> dict:
        """Format APA references"""
        self.logger.info("Formatting references...")
        
        try:
            selected_papers_file = self.data_dir / "selected_papers.json"
            references_dir = self.data_dir / "references"
            
            if not selected_papers_file.exists():
                return {"success": False, "error": "No selected papers file found"}
            
            stats = self.apa_formatter.generate_bibliography(
                str(selected_papers_file), 
                str(references_dir / "apa_bibliography.txt")
            )
            
            self.logger.info(f"Formatted {stats['total_references']} references")
            return {"success": True, "references": stats['total_references']}
            
        except Exception as e:
            self.logger.error(f"Error formatting references: {e}")
            return {"success": False, "error": str(e)}
    
    def create_final_paper(self) -> dict:
        """Create final integrated paper"""
        self.logger.info("Creating final paper...")
        
        try:
            drafts_dir = self.data_dir / "drafts"
            references_dir = self.data_dir / "references"
            final_dir = self.data_dir / "final_output"
            
            # Load drafts
            drafts_file = drafts_dir / "generated_drafts.json"
            if not drafts_file.exists():
                return {"success": False, "error": "No drafts found"}
            
            with open(drafts_file, 'r', encoding='utf-8') as f:
                drafts_data = json.load(f)
            
            # Load references
            bib_file = references_dir / "apa_bibliography.txt"
            bibliography = ""
            if bib_file.exists():
                with open(bib_file, 'r', encoding='utf-8') as f:
                    bibliography = f.read()
            
            # Create final document
            final_content = f"""Generated Research Paper
========================

Generated using AI Research Agent
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # Add sections in order
            section_order = ['abstract', 'introduction', 'methods', 'results', 'discussion']
            
            for section_type in section_order:
                if section_type in drafts_data:
                    section = drafts_data[section_type]
                    final_content += f"\n{section['title'].title()}\n{'-' * len(section['title'])}\n\n"
                    final_content += section['content']
                    final_content += "\n\n"
            
            final_content += bibliography
            
            # Save final paper
            final_file = final_dir / "final_research_paper.txt"
            with open(final_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            self.logger.info("Final paper created successfully")
            return {"success": True, "file": str(final_file)}
            
        except Exception as e:
            self.logger.error(f"Error creating final paper: {e}")
            return {"success": False, "error": str(e)}
    
    def start_web_interface(self, port: int = 5000) -> dict:
        """Start the web interface"""
        self.logger.info(f"Starting web interface on port {port}")
        
        try:
            import subprocess
            cmd = ["python", "start_web_interface.py"]
            subprocess.Popen(cmd)
            self.logger.info(f"Web interface started at http://localhost:{port}")
            return {"success": True, "url": f"http://localhost:{port}"}
        except Exception as e:
            self.logger.error(f"Error starting web interface: {e}")
            return {"success": False, "error": str(e)}
    
    def complete_workflow(self, topic: str, max_papers: int = 5) -> dict:
        """Run complete workflow from search to final paper"""
        self.logger.info(f"Starting complete workflow for: {topic}")
        
        results = {"steps": [], "success": True}
        
        # Step 1: Search papers
        result = self.search_papers(topic, max_papers)
        results["steps"].append({"step": "Search", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 2: Extract text
        result = self.extract_text_from_papers()
        results["steps"].append({"step": "Extract", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 3: Extract sections
        result = self.extract_sections()
        results["steps"].append({"step": "Sections", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 4: Analyze sections
        result = self.analyze_sections()
        results["steps"].append({"step": "Analyze", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 5: Generate drafts
        result = self.generate_drafts()
        results["steps"].append({"step": "Drafts", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 6: Format references
        result = self.format_references()
        results["steps"].append({"step": "References", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        # Step 7: Create final paper
        result = self.create_final_paper()
        results["steps"].append({"step": "Final Paper", "result": result})
        if not result["success"]:
            results["success"] = False
            return results
        
        self.logger.info("Complete workflow finished successfully")
        return results
    
    def cleanup_unnecessary_files(self):
        """Remove unnecessary files"""
        self.logger.info("Cleaning up unnecessary files...")
        
        files_to_remove = [
            "analyze_sections.py",
            "compare_papers.py", 
            "simple_analysis.py",
            "test_milestone3.py",
            "test_openai_direct.py",
            "test_openai_integration.py",
            "text_extraction_errors.log",
            "section_extraction.log"
        ]
        
        removed_count = 0
        for file_name in files_to_remove:
            file_path = self.base_dir / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    removed_count += 1
                    self.logger.info(f"Removed: {file_name}")
                except Exception as e:
                    self.logger.warning(f"Could not remove {file_name}: {e}")
        
        self.logger.info(f"Cleanup completed. Removed {removed_count} files.")
        return {"removed": removed_count}


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Research Agent - Complete Research Paper Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --topic "machine learning" --max-papers 5
  %(prog)s --complete-workflow "deep learning"
  %(prog)s --generate-drafts
  %(prog)s --format-apa
  %(prog)s --web-interface
  %(prog)s --cleanup
        """
    )
    
    parser.add_argument("--topic", help="Research topic for paper search")
    parser.add_argument("--max-papers", type=int, default=5, help="Maximum number of papers to search")
    parser.add_argument("--search", action="store_true", help="Search for papers")
    parser.add_argument("--extract", action="store_true", help="Extract text from papers")
    parser.add_argument("--sections", action="store_true", help="Extract sections")
    parser.add_argument("--analyze", action="store_true", help="Analyze sections")
    parser.add_argument("--generate-drafts", action="store_true", help="Generate GPT drafts")
    parser.add_argument("--format-apa", action="store_true", help="Format APA references")
    parser.add_argument("--final-paper", action="store_true", help="Create final paper")
    parser.add_argument("--complete-workflow", help="Run complete workflow for topic")
    parser.add_argument('--review-content', action='store_true', help='Review and refine generated content')
    parser.add_argument('--test-system', action='store_true', help='Run comprehensive system tests')
    parser.add_argument('--generate-docs', action='store_true', help='Generate documentation and presentation materials')
    parser.add_argument('--gradio-interface', action='store_true', help='Launch Gradio web interface')
    parser.add_argument('--web-interface', action='store_true', help='Start web interface')
    parser.add_argument('--port', type=int, default=5000, help='Web interface port')
    parser.add_argument('--cleanup', action='store_true', help='Remove unnecessary files')
    parser.add_argument('--status', action='store_true', help='Show system status')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = AIResearchAgent()
    
    # Handle cleanup first
    if args.cleanup:
        result = agent.cleanup_unnecessary_files()
        print(f"✅ Cleanup completed. Removed {result['removed']} files.")
        return
    
    # Show status
    if args.status:
        print("🔍 AI Research Agent Status")
        print("=" * 40)
        
        # Check directories
        dirs = ["papers", "extracted_texts", "sections", "section_analysis", "drafts", "references"]
        for dir_name in dirs:
            dir_path = agent.data_dir / dir_name
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*")))
                print(f"✅ data/{dir_name}: {file_count} files")
            else:
                print(f"❌ data/{dir_name}: Missing")
        
        print(f"📁 Base directory: {agent.base_dir}")
        print(f"📊 Data directory: {agent.data_dir}")
        return
    
    # Handle complete workflow
    if args.complete_workflow:
        print(f"🚀 Starting complete workflow for: {args.complete_workflow}")
        result = agent.complete_workflow(args.complete_workflow, args.max_papers)
        
        print("\n📊 Workflow Results:")
        print("=" * 30)
        
        for step_result in result["steps"]:
            status = "✅" if step_result["result"]["success"] else "❌"
            print(f"{status} {step_result['step']}: {step_result['result']}")
        
        if result["success"]:
            print(f"\n🎉 Complete workflow successful!")
            print(f"📄 Final paper: {agent.data_dir}/final_output/final_research_paper.txt")
        else:
            print(f"\n❌ Workflow failed. Check logs for details.")
        
        return
    
    # Handle Gradio interface
    if args.gradio_interface:
        try:
            from gradio_interface import GradioInterface
            app = GradioInterface()
            app.launch(share=False, port=7860)
            return
        except Exception as e:
            print(f"❌ Failed to start Gradio interface: {e}")
            return
    
    # Handle content review
    if args.review_content:
        print("🔍 Reviewing and refining generated content...")
        try:
            # Load existing drafts
            drafts_dir = agent.data_dir / "drafts"
            drafts_file = drafts_dir / "generated_drafts.json"
            
            if not drafts_file.exists():
                print("❌ No drafts found to review. Please generate drafts first.")
                return
            
            with open(drafts_file, 'r', encoding='utf-8') as f:
                drafts_data = json.load(f)
            
            reviewed_sections = {}
            
            for section_type, content_data in drafts_data.items():
                print(f"\n📝 Reviewing {section_type}...")
                
                # Review content
                review = agent.content_reviewer.review_content(content_data['content'], section_type)
                
                # Perform revision if quality is low
                if review.quality_metrics.overall_quality < 0.8:
                    print(f"🔄 Revising {section_type} (Quality: {review.quality_metrics.overall_quality:.2f})")
                    revised_content = agent.content_reviewer.revise_content(
                        content_data['content'], section_type, review.revision_suggestions
                    )
                    reviewed_sections[section_type] = revised_content
                else:
                    print(f"✅ {section_type} quality is good (Quality: {review.quality_metrics.overall_quality:.2f})")
                    reviewed_sections[section_type] = content_data['content']
            
            # Save reviewed drafts
            reviewed_file = drafts_dir / "reviewed_drafts.json"
            with open(reviewed_file, 'w', encoding='utf-8') as f:
                json.dump(reviewed_sections, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Content review completed. Reviewed drafts saved to: {reviewed_file}")
            
        except Exception as e:
            print(f"❌ Error during content review: {e}")
        return
    
    # Handle system testing
    if args.test_system:
        print("🧪 Running comprehensive system tests...")
        try:
            test_results = run_comprehensive_tests()
            
            print(f"\n📊 Test Results:")
            print(f"Overall Success: {'✅ PASSED' if test_results['overall_success'] else '❌ FAILED'}")
            
            if 'summary' in test_results:
                summary = test_results['summary']
                print(f"Categories: {summary['passed_categories']}/{summary['total_categories']} passed")
                print(f"Tests: {summary['passed_tests']}/{summary['total_tests']} passed")
                print(f"Execution Time: {summary['execution_time']:.2f} seconds")
            
            if 'recommendations' in test_results:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(test_results['recommendations'], 1):
                    print(f"{i}. {rec}")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
        return
    
    # Handle documentation generation
    if args.generate_docs:
        print("📚 Generating documentation and presentation materials...")
        try:
            doc_generator = FinalDocumentation()
            files = doc_generator.generate_all_documentation()
            
            print(f"\n📚 Documentation Generated Successfully!")
            print("=" * 50)
            for doc_type, file_path in files.items():
                print(f"{doc_type}: {file_path}")
            
            print(f"\n📁 All documentation saved to: {doc_generator.output_dir}")
            
        except Exception as e:
            print(f"❌ Error generating documentation: {e}")
        return
    
    # Handle individual commands
    if args.topic and args.search:
        result = agent.search_papers(args.topic, args.max_papers)
        print(f"{'✅' if result['success'] else '❌'} Search: {result}")
    
    if args.extract:
        result = agent.extract_text_from_papers()
        print(f"{'✅' if result['success'] else '❌'} Extract: {result}")
    
    if args.sections:
        result = agent.extract_sections()
        print(f"{'✅' if result['success'] else '❌'} Sections: {result}")
    
    if args.analyze:
        result = agent.analyze_sections()
        print(f"{'✅' if result['success'] else '❌'} Analyze: {result}")
    
    if args.generate_drafts:
        result = agent.generate_drafts()
        print(f"{'✅' if result['success'] else '❌'} Drafts: {result}")
    
    if args.format_apa:
        result = agent.format_references()
        print(f"{'✅' if result['success'] else '❌'} APA: {result}")
    
    if args.final_paper:
        result = agent.create_final_paper()
        print(f"{'✅' if result['success'] else '❌'} Final: {result}")
    
    # If topic provided without specific flags, run complete workflow
    if args.topic and not any([args.search, args.extract, args.sections, args.analyze, 
                             args.generate_drafts, args.format_apa, args.final_paper]):
        print(f"🚀 Running complete workflow for: {args.topic}")
        result = agent.complete_workflow(args.topic, args.max_papers)
        
        if result["success"]:
            print("🎉 Complete workflow successful!")
            print(f"📄 Final paper: {agent.data_dir}/final_output/final_research_paper.txt")
        else:
            print("❌ Workflow failed. Check logs for details.")


if __name__ == "__main__":
    main()
