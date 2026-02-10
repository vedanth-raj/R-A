import gradio as gr
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple
import logging

from enhanced_gpt_generator import EnhancedGPTDraftGenerator
from content_reviewer import ContentReviewer
from final_integration import FinalIntegration
from final_testing import run_comprehensive_tests
from final_documentation import FinalDocumentation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedGradioInterface:
    """Enhanced Gradio interface with Lab Pulse styling"""
    
    def __init__(self):
        self.draft_generator = EnhancedGPTDraftGenerator()
        self.content_reviewer = ContentReviewer()
        self.final_integration = FinalIntegration()
        self.doc_generator = FinalDocumentation()
        
        # Initialize session state
        self.current_content = {}
        self.current_reviews = {}
        self.generation_history = []
        
    def get_system_status(self) -> str:
        """Get formatted system status"""
        try:
            data_dir = Path("data")
            status_info = []
            
            # Check data directories
            directories = ["papers", "extracted_texts", "sections", "section_analysis", "drafts", "references"]
            for directory in directories:
                dir_path = data_dir / directory
                if dir_path.exists():
                    file_count = len(list(dir_path.glob("*")))
                    status_info.append(f"✅ {directory}: {file_count} files")
                else:
                    status_info.append(f"❌ {directory}: Not found")
            
            # AI Provider status
            providers = self.draft_generator.available_providers
            status_info.append(f"🤖 AI Providers: {', '.join(providers)}")
            
            return "\n".join(status_info)
        except Exception as e:
            return f"❌ Error getting status: {str(e)}"
    
    def generate_content(self, section_type: str, topic: str, max_papers: int) -> Tuple[str, str, str]:
        """Generate content for selected section"""
        try:
            start_time = time.time()
            
            # Load paper data
            papers_data = self.draft_generator.load_paper_data("data/section_analysis")
            if not papers_data:
                return "❌ No analysis data found. Please run section analysis first.", "", ""
            
            # Generate content
            content = self.draft_generator.generate_draft(section_type, papers_data)
            
            # Review content
            review = self.content_reviewer.review_content(content, section_type)
            
            # Store results
            self.current_content[section_type] = {
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'word_count': len(content.split())
            }
            self.current_reviews[section_type] = review
            
            # Format quality metrics
            quality_metrics = f"""
## 📊 Quality Assessment

### Overall Score: {review.quality_metrics.overall_quality:.2f}/1.00

| Metric | Score | Status |
|--------|-------|--------|
| **Clarity** | {review.quality_metrics.clarity_score:.2f} | {"🟢" if review.quality_metrics.clarity_score > 0.7 else "🟡" if review.quality_metrics.clarity_score > 0.5 else "🔴"} |
| **Coherence** | {review.quality_metrics.coherence_score:.2f} | {"🟢" if review.quality_metrics.coherence_score > 0.7 else "🟡" if review.quality_metrics.coherence_score > 0.5 else "🔴"} |
| **Academic Tone** | {review.quality_metrics.academic_tone_score:.2f} | {"🟢" if review.quality_metrics.academic_tone_score > 0.7 else "🟡" if review.quality_metrics.academic_tone_score > 0.5 else "🔴"} |
| **Completeness** | {review.quality_metrics.completeness_score:.2f} | {"🟢" if review.quality_metrics.completeness_score > 0.7 else "🟡" if review.quality_metrics.completeness_score > 0.5 else "🔴"} |
| **Citation Quality** | {review.quality_metrics.citation_quality_score:.2f} | {"🟢" if review.quality_metrics.citation_quality_score > 0.7 else "🟡" if review.quality_metrics.citation_quality_score > 0.5 else "🔴"} |

**Word Count:** {review.quality_metrics.word_count}  
**Sentence Count:** {review.quality_metrics.sentence_count}  
**Average Sentence Length:** {review.quality_metrics.avg_sentence_length:.1f}
"""
            
            # Format suggestions
            if review.revision_suggestions:
                suggestions = "## 💡 Revision Suggestions\n\n"
                for i, suggestion in enumerate(review.revision_suggestions, 1):
                    severity_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴"}[suggestion.severity]
                    suggestions += f"""
### {severity_emoji} {suggestion.category.title()} (Priority: {suggestion.severity})

**Issue:** {suggestion.description}  
**Suggestion:** {suggestion.suggestion}  
**Location:** {suggestion.location}

---
"""
            else:
                suggestions = "## ✅ No Revision Suggestions\n\nContent quality is excellent!"
            
            generation_time = time.time() - start_time
            
            # Add to history
            self.generation_history.append({
                'section_type': section_type,
                'timestamp': datetime.now().isoformat(),
                'quality_score': review.quality_metrics.overall_quality,
                'generation_time': generation_time
            })
            
            return content, quality_metrics, suggestions
            
        except Exception as e:
            error_msg = f"❌ Error generating content: {str(e)}"
            return error_msg, "", ""
    
    def revise_content(self, section_type: str) -> Tuple[str, str, str]:
        """Revise content based on suggestions"""
        try:
            if section_type not in self.current_content:
                return "❌ No content found for revision. Please generate content first.", "", ""
            
            if section_type not in self.current_reviews:
                return "❌ No review found for this section. Please generate content first.", "", ""
            
            original_content = self.current_content[section_type]['content']
            review = self.current_reviews[section_type]
            
            # Perform revision
            revised_content = self.content_reviewer.revise_content(
                original_content, section_type, review.revision_suggestions
            )
            
            # Review revised content
            new_review = self.content_reviewer.review_content(revised_content, section_type)
            
            # Update stored content
            self.current_content[section_type]['content'] = revised_content
            self.current_content[section_type]['revised'] = True
            self.current_reviews[section_type] = new_review
            
            # Calculate improvement
            improvement = new_review.quality_metrics.overall_quality - review.quality_metrics.overall_quality
            
            # Format results
            quality_metrics = f"""
## 🔄 Revision Results

### Quality Improvement: {improvement:+.2f}

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Overall** | {review.quality_metrics.overall_quality:.2f} | {new_review.quality_metrics.overall_quality:.2f} | {improvement:+.2f} |
| **Clarity** | {review.quality_metrics.clarity_score:.2f} | {new_review.quality_metrics.clarity_score:.2f} | {new_review.quality_metrics.clarity_score - review.quality_metrics.clarity_score:+.2f} |
| **Coherence** | {review.quality_metrics.coherence_score:.2f} | {new_review.quality_metrics.coherence_score:.2f} | {new_review.quality_metrics.coherence_score - review.quality_metrics.coherence_score:+.2f} |
| **Academic Tone** | {review.quality_metrics.academic_tone_score:.2f} | {new_review.quality_metrics.academic_tone_score:.2f} | {new_review.quality_metrics.academic_tone_score - review.quality_metrics.academic_tone_score:+.2f} |
| **Completeness** | {review.quality_metrics.completeness_score:.2f} | {new_review.quality_metrics.completeness_score:.2f} | {new_review.quality_metrics.completeness_score - review.quality_metrics.completeness_score:+.2f} |
| **Citation Quality** | {review.quality_metrics.citation_quality_score:.2f} | {new_review.quality_metrics.citation_quality_score:.2f} | {new_review.quality_metrics.citation_quality_score - review.quality_metrics.citation_quality_score:+.2f} |

**Word Count:** {new_review.quality_metrics.word_count}  
**Sentence Count:** {new_review.quality_metrics.sentence_count}  
**Average Sentence Length:** {new_review.quality_metrics.avg_sentence_length:.1f}
"""
            
            suggestions = "## ✅ Revision Complete\n\nContent has been revised based on suggestions. Generate new suggestions to see further improvements."
            
            return revised_content, quality_metrics, suggestions
            
        except Exception as e:
            error_msg = f"❌ Error revising content: {str(e)}"
            return error_msg, "", ""
    
    def run_complete_workflow(self, topic: str, max_papers: int) -> str:
        """Run complete workflow"""
        try:
            results = self.final_integration.complete_workflow(topic, max_papers)
            
            if results['success']:
                return f"""
## 🎉 Complete Workflow Successful!

### 📊 Summary
- **Topic:** {results['topic']}
- **Papers Processed:** {results['max_papers']}
- **Stages Completed:** {len(results['stages'])}
- **Success Rate:** 100%

### 📝 Generated Sections
{chr(10).join([f"- **{stage}**: ✅" for stage in results['stages'].keys() if results['stages'][stage].get('success', False)])}

### 📄 Final Report
{results.get('final_report', 'Report generation in progress...')}

### 💾 Results Saved
All results have been saved to the data directory with timestamp.
"""
            else:
                return f"""
## ❌ Workflow Failed

**Error:** {results.get('error', 'Unknown error')}

**Completed Stages:** {len(results['stages'])}

Please check the logs for more details.
"""
                
        except Exception as e:
            return f"❌ Error running workflow: {str(e)}"
    
    def run_system_tests(self) -> str:
        """Run comprehensive system tests"""
        try:
            results = run_comprehensive_tests()
            
            if results['overall_success']:
                return f"""
## 🧪 System Tests - PASSED

### 📊 Test Results
- **Overall Success:** ✅ PASSED
- **Categories Passed:** {results['summary']['passed_categories']}/{results['summary']['total_categories']}
- **Tests Passed:** {results['summary']['passed_tests']}/{results['summary']['total_tests']}
- **Execution Time:** {results['summary']['execution_time']:.2f} seconds

### 📋 Category Results
{chr(10).join([f"- **{cat}**: ✅" for cat in results['categories'] if results['categories'][cat]['passed']])}

### 💡 Recommendations
{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(results['recommendations'])])}
"""
            else:
                return f"""
## 🧪 System Tests - FAILED

### 📊 Test Results
- **Overall Success:** ❌ FAILED
- **Categories Passed:** {results['summary']['passed_categories']}/{results['summary']['total_categories']}
- **Tests Passed:** {results['summary']['passed_tests']}/{results['summary']['total_tests']}
- **Execution Time:** {results['summary']['execution_time']:.2f} seconds

### 💡 Recommendations
{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(results['recommendations'])])}
"""
                
        except Exception as e:
            return f"❌ Error running tests: {str(e)}"
    
    def generate_documentation(self) -> str:
        """Generate documentation"""
        try:
            files = self.doc_generator.generate_all_documentation()
            
            return f"""
## 📚 Documentation Generated Successfully!

### 📁 Generated Files
{chr(10).join([f"- **{doc_type}**: `{file_path}`" for doc_type, file_path in files.items()])}

### 📂 Output Directory
{self.doc_generator.output_dir}

### 📖 Documentation Includes
- **User Manual**: Complete installation and usage guide
- **Technical Documentation**: System architecture and API reference
- **Presentation Slides**: Professional 20-slide deck
- **Documentation Index**: Complete navigation guide

All documentation has been generated with version control and timestamps.
"""
                
        except Exception as e:
            return f"❌ Error generating documentation: {str(e)}"
    
    def create_interface(self):
        """Create enhanced Gradio interface with Lab Pulse styling"""
        
        with gr.Blocks(
            title="AI Research Agent - Enhanced Lab Pulse Edition"
        ) as interface:
            
            # Enhanced CSS with Lab Pulse styling
            gr.HTML("""
            <style>
            :root {
                --background: #000000;
                --foreground: #ffffff;
                --muted: #6b7280;
                --accent: #800020;
                --maroon-50: #fdf2f4;
                --maroon-100: #fce7eb;
                --maroon-200: #f9d0d9;
                --maroon-300: #f4a8b8;
                --maroon-400: #ec7491;
                --maroon-500: #e0486d;
                --maroon-600: #cc2952;
                --maroon-700: #800020;
                --maroon-800: #6b001a;
                --maroon-900: #5a0016;
                --maroon-950: #3d000f;
            }
            
            body {
                background: var(--background);
                color: var(--foreground);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                text-rendering: optimizeLegibility;
            }
            
            .gradio-container {
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2d1b1b 100%);
                min-height: 100vh;
            }
            
            .main-header {
                text-align: center;
                background: linear-gradient(135deg, var(--maroon-700) 0%, var(--maroon-900) 100%);
                color: white;
                padding: 3rem 2rem;
                border-radius: 16px;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(128, 0, 32, 0.3);
            }
            
            .main-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 30% 10%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
                           radial-gradient(circle at 70% 20%, rgba(204, 41, 82, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .main-header h1 {
                margin: 0;
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, var(--maroon-400) 0%, var(--foreground) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                position: relative;
                z-index: 1;
            }
            
            .main-header h2 {
                margin: 0.5rem 0;
                font-size: 1.5rem;
                font-weight: 400;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            .main-header p {
                margin: 1rem 0 0 0;
                opacity: 0.8;
                font-size: 1.1rem;
                position: relative;
                z-index: 1;
            }
            
            .glass-surface {
                border: 1px solid rgba(255, 255, 255, 0.08);
                background: rgba(255, 255, 255, 0.04);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                padding: 1.5rem;
            }
            
            .card-glow {
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35),
                           0 0 0 1px rgba(255, 255, 255, 0.04);
            }
            
            .quality-metric {
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 12px;
                border-left: 4px solid var(--maroon-600);
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(8px);
            }
            
            .quality-high { 
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
                border-left-color: #22c55e;
                color: #86efac;
            }
            
            .quality-medium { 
                background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%);
                border-left-color: #fbbf24;
                color: #fde047;
            }
            
            .quality-low { 
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
                border-left-color: #ef4444;
                color: #fca5a5;
            }
            
            .tab-nav {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 0.5rem;
                margin-bottom: 1rem;
            }
            
            .tab-button {
                background: transparent;
                border: none;
                color: var(--muted);
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .tab-button:hover {
                background: rgba(128, 0, 32, 0.1);
                color: var(--maroon-400);
            }
            
            .tab-button.active {
                background: linear-gradient(135deg, var(--maroon-700) 0%, var(--maroon-900) 100%);
                color: white;
            }
            
            .status-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 0.5rem;
                animation: pulse 2s infinite;
            }
            
            .status-indicator.online {
                background: #22c55e;
            }
            
            .status-indicator.offline {
                background: #ef4444;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .btn-primary {
                background: linear-gradient(135deg, var(--maroon-700) 0%, var(--maroon-900) 100%);
                border: 1px solid var(--maroon-600);
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(128, 0, 32, 0.3);
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(128, 0, 32, 0.4);
            }
            
            .btn-secondary {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--maroon-600);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--maroon-500);
            }
            </style>
            """)
            
            # Enhanced Header
            gr.HTML("""
            <div class="main-header">
                <div class="status-indicator online"></div>
                <h1>🤖 AI Research Agent</h1>
                <h2>Enhanced Lab Pulse Edition</h2>
                <p>Advanced Academic Content Generation with Real-Time Quality Assessment</p>
            </div>
            """)
            
            # Main Interface with Tabs
            with gr.Tabs() as tabs:
                
                # Tab 1: Content Generation
                with gr.TabItem("📝 Content Generation", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.HTML("""
                            <div class="glass-surface card-glow">
                                <h3>🚀 Generate Academic Content</h3>
                                <p>Select a section type and generate high-quality academic content with AI-powered quality assessment.</p>
                            </div>
                            """)
                            
                            with gr.Row():
                                section_type = gr.Dropdown(
                                    choices=["abstract", "introduction", "methods", "results", "discussion"],
                                    label="📋 Section Type",
                                    value="abstract",
                                    info="Choose the section to generate"
                                )
                                
                                topic = gr.Textbox(
                                    label="🎯 Research Topic",
                                    value="machine learning",
                                    placeholder="Enter your research topic..."
                                )
                            
                            with gr.Row():
                                max_papers = gr.Slider(
                                    minimum=1,
                                    maximum=20,
                                    value=5,
                                    step=1,
                                    label="📚 Max Papers to Analyze"
                                )
                            
                            with gr.Row():
                                generate_btn = gr.Button(
                                    "🚀 Generate Content",
                                    elem_classes=["btn-primary"],
                                    size="lg"
                                )
                                
                                revise_btn = gr.Button(
                                    "🔄 Revise Content",
                                    elem_classes=["btn-secondary"],
                                    size="lg"
                                )
                        
                        with gr.Column(scale=3):
                            content_output = gr.Textbox(
                                label="📄 Generated Content",
                                lines=20,
                                placeholder="Generated content will appear here...",
                                show_label=True
                            )
                    
                    with gr.Row():
                        with gr.Column():
                            quality_output = gr.Markdown(
                                label="📊 Quality Metrics",
                                value="Quality metrics will appear here..."
                            )
                        
                        with gr.Column():
                            suggestions_output = gr.Markdown(
                                label="💡 Revision Suggestions",
                                value="Revision suggestions will appear here..."
                            )
                
                # Tab 2: Complete Workflow
                with gr.TabItem("🔄 Complete Workflow", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface card-glow">
                                <h3>🎯 End-to-End Workflow</h3>
                                <p>Run the complete workflow from data loading to final report generation with automated quality assessment.</p>
                            </div>
                            """)
                            
                            workflow_topic = gr.Textbox(
                                label="🎯 Research Topic",
                                value="machine learning",
                                placeholder="Enter your research topic..."
                            )
                            
                            workflow_max_papers = gr.Slider(
                                minimum=1,
                                maximum=20,
                                value=5,
                                step=1,
                                label="📚 Max Papers to Analyze"
                            )
                            
                            workflow_btn = gr.Button(
                                "🚀 Run Complete Workflow",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            workflow_output = gr.Markdown(
                                label="📊 Workflow Results",
                                value="Workflow results will appear here..."
                            )
                
                # Tab 3: System Testing
                with gr.TabItem("🧪 System Testing", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface card-glow">
                                <h3>🧪 Comprehensive Testing</h3>
                                <p>Run comprehensive system tests to verify all components are working correctly.</p>
                            </div>
                            """)
                            
                            test_btn = gr.Button(
                                "🧪 Run System Tests",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            test_output = gr.Markdown(
                                label="📊 Test Results",
                                value="Test results will appear here..."
                            )
                
                # Tab 4: Documentation
                with gr.TabItem("📚 Documentation", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface card-glow">
                                <h3>📚 Documentation Generation</h3>
                                <p>Generate comprehensive documentation including user manual, technical docs, and presentation slides.</p>
                            </div>
                            """)
                            
                            docs_btn = gr.Button(
                                "📚 Generate Documentation",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            docs_output = gr.Markdown(
                                label="📊 Documentation Results",
                                value="Documentation generation results will appear here..."
                            )
                
                # Tab 5: System Status
                with gr.TabItem("📊 System Status", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface card-glow">
                                <h3>📊 System Status</h3>
                                <p>Monitor system status, data directories, and AI provider availability.</p>
                            </div>
                            """)
                            
                            refresh_status_btn = gr.Button(
                                "🔄 Refresh Status",
                                elem_classes=["btn-secondary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            status_output = gr.Markdown(
                                label="📊 System Information",
                                value=self.get_system_status()
                            )
            
            # Footer
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.6);">
                <p>🤖 <strong>AI Research Agent - Enhanced Lab Pulse Edition</strong></p>
                <p>Powered by Google Gemini AI | APA 7th Edition Compliant | Real-Time Quality Assessment</p>
            </div>
            """)
            
            # Event Handlers
            generate_btn.click(
                fn=self.generate_content,
                inputs=[section_type, topic, max_papers],
                outputs=[content_output, quality_output, suggestions_output]
            )
            
            revise_btn.click(
                fn=self.revise_content,
                inputs=[section_type],
                outputs=[content_output, quality_output, suggestions_output]
            )
            
            workflow_btn.click(
                fn=self.run_complete_workflow,
                inputs=[workflow_topic, workflow_max_papers],
                outputs=[workflow_output]
            )
            
            test_btn.click(
                fn=self.run_system_tests,
                outputs=[test_output]
            )
            
            docs_btn.click(
                fn=self.generate_documentation,
                outputs=[docs_output]
            )
            
            refresh_status_btn.click(
                fn=self.get_system_status,
                outputs=[status_output]
            )
        
        return interface
    
    def launch(self, share=False, port=7860):
        """Launch the enhanced Gradio interface"""
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_name="0.0.0.0",
            server_port=port,
            show_error=True,
            inbrowser=True
        )

def main():
    """Main function to launch the enhanced Gradio interface"""
    app = EnhancedGradioInterface()
    app.launch(share=False, port=7860)

if __name__ == "__main__":
    main()
