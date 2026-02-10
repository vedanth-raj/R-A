"""
Polished Gradio Interface for AI Research Agent
Provides comprehensive UI for content generation, review, and refinement
"""

import gradio as gr
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_gpt_generator import EnhancedGPTDraftGenerator
from content_reviewer import ContentReviewer, perform_full_revision_cycle
from apa_formatter import APAFormatter

class GradioInterface:
    """Polished Gradio interface for AI Research Agent"""
    
    def __init__(self):
        """Initialize the Gradio interface"""
        self.draft_generator = EnhancedGPTDraftGenerator(preferred_provider="gemini")
        self.content_reviewer = ContentReviewer(preferred_provider="gemini")
        self.apa_formatter = APAFormatter()
        
        # Storage for generated content
        self.generated_sections = {}
        self.review_results = {}
        self.revision_history = {}
        
        # Load existing data if available
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing generated data"""
        try:
            # Load sections
            sections_file = Path("data/sections")
            if sections_file.exists():
                self.section_files = list(sections_file.glob("*_sections.json"))
            else:
                self.section_files = []
            
            # Load existing drafts
            drafts_file = Path("data/drafts/generated_drafts.json")
            if drafts_file.exists():
                with open(drafts_file, 'r', encoding='utf-8') as f:
                    self.generated_sections = json.load(f)
            
            # Load references
            refs_file = Path("data/references/apa_bibliography.txt")
            if refs_file.exists():
                with open(refs_file, 'r', encoding='utf-8') as f:
                    self.references_content = f.read()
            else:
                self.references_content = ""
        
        except Exception as e:
            print(f"Error loading existing data: {e}")
            self.section_files = []
            self.generated_sections = {}
            self.references_content = ""
    
    def generate_content(self, section_type: str, progress=gr.Progress()) -> Tuple[str, str, str]:
        """Generate content for a specific section"""
        try:
            progress(0.1, desc="Initializing AI generation...")
            
            # Load paper data
            papers_data = self.draft_generator.load_paper_data("data/section_analysis")
            
            if not papers_data:
                return "❌ No analysis data found. Please run section analysis first.", "", ""
            
            progress(0.3, desc="Generating content...")
            
            # Generate draft
            draft = self.draft_generator.generate_section_draft(section_type, papers_data)
            
            progress(0.7, desc="Analyzing quality...")
            
            # Review content
            review = self.content_reviewer.review_content(draft.content, section_type)
            
            progress(0.9, desc="Finalizing...")
            
            # Store results
            self.generated_sections[section_type] = draft.content
            self.review_results[section_type] = review
            
            # Format quality metrics
            metrics = review.quality_metrics
            quality_text = f"""
            **Quality Metrics:**
            - Overall Quality: {metrics.overall_quality:.2f}/1.00
            - Clarity: {metrics.clarity_score:.2f}/1.00
            - Coherence: {metrics.coherence_score:.2f}/1.00
            - Academic Tone: {metrics.academic_tone_score:.2f}/1.00
            - Completeness: {metrics.completeness_score:.2f}/1.00
            - Citations: {metrics.citation_quality_score:.2f}/1.00
            
            **Statistics:**
            - Word Count: {metrics.word_count}
            - Sentence Count: {metrics.sentence_count}
            - Avg Sentence Length: {metrics.avg_sentence_length:.1f}
            """
            
            # Format suggestions
            suggestions_text = ""
            if review.revision_suggestions:
                suggestions_text = "**Revision Suggestions:**\n\n"
                for i, suggestion in enumerate(review.revision_suggestions, 1):
                    suggestions_text += f"{i}. **{suggestion.category.title()}** ({suggestion.severity.upper()})\n"
                    suggestions_text += f"   - {suggestion.description}\n"
                    suggestions_text += f"   - 💡 {suggestion.suggestion}\n\n"
            else:
                suggestions_text = "✅ No revision suggestions needed. Content quality is excellent!"
            
            progress(1.0, desc="Complete!")
            
            return draft.content, quality_text, suggestions_text
            
        except Exception as e:
            error_msg = f"❌ Error generating content: {str(e)}"
            return error_msg, "", ""
    
    def revise_content(self, section_type: str, progress=gr.Progress()) -> Tuple[str, str, str]:
        """Revise content based on suggestions"""
        try:
            if section_type not in self.generated_sections:
                return "❌ No content found for this section. Please generate content first.", "", ""
            
            progress(0.2, desc="Analyzing content...")
            
            original_content = self.generated_sections[section_type]
            
            # Perform revision cycle
            revision_result = perform_full_revision_cycle(original_content, section_type, max_iterations=2)
            
            progress(0.7, desc="Applying revisions...")
            
            # Store revision history
            self.revision_history[section_type] = revision_result
            
            # Get final review
            final_review = self.content_reviewer.review_content(revision_result['final_content'], section_type)
            
            progress(0.9, desc="Finalizing...")
            
            # Update stored content
            self.generated_sections[section_type] = revision_result['final_content']
            
            # Format results
            revision_text = f"""
            **Revision Completed!**
            
            **Iterations:** {revision_result['total_iterations']}
            **Quality Improvement:** {revision_result['final_quality'] - self.review_results[section_type].quality_metrics.overall_quality:+.2f}
            **Final Quality:** {revision_result['final_quality']:.2f}/1.00
            
            **Revision History:**
            """
            
            for i, review in enumerate(revision_result['revision_history'], 1):
                revision_text += f"\nIteration {i}: Quality {review.quality_metrics.overall_quality:.2f}"
            
            # Format new quality metrics
            metrics = final_review.quality_metrics
            quality_text = f"""
            **Updated Quality Metrics:**
            - Overall Quality: {metrics.overall_quality:.2f}/1.00
            - Clarity: {metrics.clarity_score:.2f}/1.00
            - Coherence: {metrics.coherence_score:.2f}/1.00
            - Academic Tone: {metrics.academic_tone_score:.2f}/1.00
            - Completeness: {metrics.completeness_score:.2f}/1.00
            - Citations: {metrics.citation_quality_score:.2f}/1.00
            """
            
            # Format remaining suggestions
            suggestions_text = ""
            if final_review.revision_suggestions:
                suggestions_text = "**Remaining Suggestions:**\n\n"
                for i, suggestion in enumerate(final_review.revision_suggestions, 1):
                    suggestions_text += f"{i}. **{suggestion.category.title()}** ({suggestion.severity.upper()})\n"
                    suggestions_text += f"   - {suggestion.description}\n"
                    suggestions_text += f"   - 💡 {suggestion.suggestion}\n\n"
            else:
                suggestions_text = "🎉 No further revisions needed. Content quality is excellent!"
            
            progress(1.0, desc="Complete!")
            
            return revision_result['final_content'], quality_text, suggestions_text
            
        except Exception as e:
            error_msg = f"❌ Error revising content: {str(e)}"
            return error_msg, "", ""
    
    def generate_final_report(self, progress=gr.Progress()) -> str:
        """Generate final comprehensive report"""
        try:
            progress(0.2, desc="Compiling sections...")
            
            if not self.generated_sections:
                return "❌ No generated sections found. Please generate content first."
            
            # Create final report
            report_content = f"""
# AI Research Agent - Final Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
            
            # Add sections in order
            section_order = ['abstract', 'introduction', 'methods', 'results', 'discussion']
            
            for section_type in section_order:
                if section_type in self.generated_sections:
                    content = self.generated_sections[section_type]
                    report_content += f"""
## {section_type.title()}

{content}

---
"""
            
            progress(0.5, desc="Adding references...")
            
            # Add references
            if self.references_content:
                report_content += f"""
## References

{self.references_content}
"""
            
            progress(0.8, desc="Adding quality summary...")
            
            # Add quality summary
            report_content += """

---

## Quality Summary

"""
            
            for section_type in section_order:
                if section_type in self.review_results:
                    metrics = self.review_results[section_type].quality_metrics
                    report_content += f"""
### {section_type.title()}
- Overall Quality: {metrics.overall_quality:.2f}/1.00
- Word Count: {metrics.word_count}
- AI Provider: {self.generated_sections.get(f'{section_type}_provider', 'Unknown')}
"""
            
            progress(1.0, desc="Complete!")
            
            return report_content
            
        except Exception as e:
            return f"❌ Error generating final report: {str(e)}"
    
    def get_system_status(self) -> str:
        """Get system status information"""
        try:
            status = f"""
## 🤖 AI Research Agent Status

**AI Providers Available:**
- Gemini: {'✅ Available' if self.draft_generator.gemini_client else '❌ Not Available'}
- Mock: {'✅ Always Available' if 'mock' in self.draft_generator.available_providers else '❌ Not Available'}

**Data Status:**
- Section Files: {len(self.section_files)} found
- Generated Sections: {len(self.generated_sections)} sections
- Reviews Completed: {len(self.review_results)} sections
- Revision History: {len(self.revision_history)} sections

**System Information:**
- Preferred Provider: {self.draft_generator.preferred_provider}
- Available Providers: {', '.join(self.draft_generator.available_providers)}
- Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            return status
            
        except Exception as e:
            return f"❌ Error getting status: {str(e)}"
    
    def create_interface(self):
        """Create the Gradio interface"""
        
        # Custom CSS for better styling
        css = """
        .gradio-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .main-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .section-card {
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: white;
        }
        .quality-metric {
            display: inline-block;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .quality-high { background: #d4edda; color: #155724; }
        .quality-medium { background: #fff3cd; color: #856404; }
        .quality-low { background: #f8d7da; color: #721c24; }
        """
        
        with gr.Blocks(title="AI Research Agent - Content Generation & Review") as interface:
            
            # Header
            gr.HTML("""
            <div class="main-header">
                <h1>🤖 AI Research Agent</h1>
                <h2>Advanced Content Generation & Review System</h2>
                <p>Generate, review, and refine academic research papers with AI-powered quality assessment</p>
            </div>
            """)
            
            # System Status
            with gr.Accordion("📊 System Status", open=False):
                status_output = gr.Markdown(self.get_system_status())
                refresh_status_btn = gr.Button("🔄 Refresh Status", size="sm")
                
                def refresh_status():
                    return self.get_system_status()
                
                refresh_status_btn.click(refresh_status, outputs=status_output)
            
            # Main Content Generation Interface
            with gr.Tabs():
                
                # Tab 1: Content Generation
                with gr.TabItem("📝 Content Generation"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.Markdown("### Generate Academic Content")
                            
                            section_dropdown = gr.Dropdown(
                                choices=["abstract", "introduction", "methods", "results", "discussion"],
                                value="abstract",
                                label="Section Type",
                                info="Select the section you want to generate"
                            )
                            
                            generate_btn = gr.Button("🚀 Generate Content", variant="primary", size="lg")
                            
                        with gr.Column(scale=1):
                            gr.Markdown("### Quick Actions")
                            gr.Markdown("""
                            **Available Sections:**
                            - **Abstract**: Brief overview (150-300 words)
                            - **Introduction**: Background and objectives (400-600 words)
                            - **Methods**: Research methodology (400-600 words)
                            - **Results**: Findings and data (500-700 words)
                            - **Discussion**: Analysis and implications (500-700 words)
                            """)
                    
                    # Generation Results
                    with gr.Row():
                        with gr.Column():
                            content_output = gr.Textbox(
                                label="Generated Content",
                                lines=15,
                                placeholder="Generated content will appear here..."
                            )
                        
                        with gr.Column():
                            quality_output = gr.Markdown(
                                label="Quality Metrics",
                                value="Quality metrics will appear here..."
                            )
                    
                    suggestions_output = gr.Markdown(
                        label="Revision Suggestions",
                        value="Revision suggestions will appear here..."
                    )
                    
                    # Generation Event
                    generate_btn.click(
                        self.generate_content,
                        inputs=[section_dropdown],
                        outputs=[content_output, quality_output, suggestions_output]
                    )
                
                # Tab 2: Review & Refine
                with gr.TabItem("🔍 Review & Refine"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Content Review & Revision")
                            
                            review_section_dropdown = gr.Dropdown(
                                choices=["abstract", "introduction", "methods", "results", "discussion"],
                                value="abstract",
                                label="Select Section to Review",
                                info="Choose a section to review and refine"
                            )
                            
                            revise_btn = gr.Button("🔄 Review & Revise", variant="secondary", size="lg")
                            
                        with gr.Column():
                            gr.Markdown("### Revision Process")
                            gr.Markdown("""
                            **What happens during revision:**
                            1. **Quality Analysis**: AI evaluates content quality
                            2. **Suggestion Generation**: Specific improvement recommendations
                            3. **Content Revision**: AI rewrites content based on suggestions
                            4. **Quality Check**: Final quality assessment
                            
                            **Revision Focus Areas:**
                            - Clarity and readability
                            - Academic tone and formality
                            - Logical coherence
                            - Content completeness
                            - Citation quality
                            """)
                    
                    # Revision Results
                    with gr.Row():
                        with gr.Column():
                            revised_content_output = gr.Textbox(
                                label="Revised Content",
                                lines=15,
                                placeholder="Revised content will appear here...",
                                show_copy_button=True
                            )
                        
                        with gr.Column():
                            revised_quality_output = gr.Markdown(
                                label="Updated Quality Metrics",
                                value="Updated quality metrics will appear here..."
                            )
                    
                    revised_suggestions_output = gr.Markdown(
                        label="Remaining Suggestions",
                        value="Remaining suggestions will appear here..."
                    )
                    
                    # Revision Event
                    revise_btn.click(
                        self.revise_content,
                        inputs=[review_section_dropdown],
                        outputs=[revised_content_output, revised_quality_output, revised_suggestions_output]
                    )
                
                # Tab 3: Final Report
                with gr.TabItem("📋 Final Report"):
                    gr.Markdown("### Generate Comprehensive Research Paper")
                    
                    with gr.Row():
                        generate_report_btn = gr.Button("📄 Generate Final Report", variant="primary", size="lg")
                        download_btn = gr.Button("💾 Download Report", variant="secondary", size="lg")
                    
                    final_report_output = gr.Markdown(
                        label="Final Research Paper",
                        value="Click 'Generate Final Report' to compile all sections into a complete research paper..."
                    )
                    
                    # Report Events
                    def generate_and_show_report():
                        report = self.generate_final_report()
                        return report
                    
                    def download_report():
                        if not self.generated_sections:
                            return None
                        
                        # Create report content
                        report_content = self.generate_final_report()
                        
                        # Save to file
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"final_report_{timestamp}.md"
                        filepath = Path(filename)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(report_content)
                        
                        return str(filepath)
                    
                    generate_report_btn.click(
                        generate_and_show_report,
                        outputs=[final_report_output]
                    )
                    
                    download_btn.click(
                        download_report,
                        outputs=[gr.File()]
                    )
                
                # Tab 4: APA References
                with gr.TabItem("📚 APA References"):
                    gr.Markdown("### APA 7th Edition References")
                    
                    with gr.Row():
                        refresh_refs_btn = gr.Button("🔄 Refresh References", size="sm")
                        format_refs_btn = gr.Button("📝 Format References", variant="secondary", size="sm")
                    
                    references_output = gr.Textbox(
                        label="APA Formatted References",
                        lines=20,
                        value=self.references_content or "No references available. Generate content first to create references.",
                        show_copy_button=True
                    )
                    
                    def refresh_references():
                        # Reload references
                        try:
                            refs_file = Path("data/references/apa_bibliography.txt")
                            if refs_file.exists():
                                with open(refs_file, 'r', encoding='utf-8') as f:
                                    return f.read()
                        except:
                            pass
                        return "No references available."
                    
                    def format_apa_references():
                        try:
                            # This would integrate with the APA formatter
                            return self.references_content or "No references to format."
                        except:
                            return "Error formatting references."
                    
                    refresh_refs_btn.click(
                        refresh_references,
                        outputs=[references_output]
                    )
                    
                    format_refs_btn.click(
                        format_apa_references,
                        outputs=[references_output]
                    )
            
            # Footer
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid #e1e5e9;">
                <p>🤖 <strong>AI Research Agent</strong> - Advanced Academic Content Generation System</p>
                <p>Powered by Google Gemini AI | APA 7th Edition Compliant</p>
            </div>
            """)
        
        return interface
    
    def launch(self, share=False, port=7860):
        """Launch the Gradio interface"""
        css = """
        .main-header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .main-header h2 {
            margin: 0.5rem 0;
            font-size: 1.5rem;
            font-weight: 400;
        }
        .main-header p {
            margin: 1rem 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        .quality-metric {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            background: #f8f9fa;
        }
        .quality-high { background: #d4edda; color: #155724; }
        .quality-medium { background: #fff3cd; color: #856404; }
        .quality-low { background: #f8d7da; color: #721c24; }
        """
        
        interface = self.create_interface()
        interface.launch(
            share=share,
            port=port,
            server_name="0.0.0.0",
            show_error=True,
            show_tips=True,
            inbrowser=True,
            css=css
        )

def main():
    """Main function to launch the Gradio interface"""
    app = GradioInterface()
    app.launch(share=False, port=7860)

if __name__ == "__main__":
    main()
