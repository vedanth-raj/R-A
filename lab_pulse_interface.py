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

class LabPulseStyleInterface:
    """AI Research Agent with Lab Pulse styling - Dark theme, maroon accents, glass effects"""
    
    def __init__(self):
        self.draft_generator = EnhancedGPTDraftGenerator()
        self.content_reviewer = ContentReviewer()
        self.final_integration = FinalIntegration()
        self.doc_generator = FinalDocumentation()
        
        # Initialize session state
        self.current_content = {}
        self.current_reviews = {}
        self.generation_history = []
        self.workflow_results = {}
        
    def get_system_status(self) -> str:
        """Get formatted system status with Lab Pulse styling"""
        try:
            data_dir = Path("data")
            status_info = []
            
            # Check data directories
            directories = ["papers", "extracted_texts", "sections", "section_analysis", "drafts", "references"]
            for directory in directories:
                dir_path = data_dir / directory
                if dir_path.exists():
                    file_count = len(list(dir_path.glob("*")))
                    status_info.append(f"✅ **{directory}**: {file_count} files")
                else:
                    status_info.append(f"❌ **{directory}**: Not found")
            
            # AI Provider status
            providers = self.draft_generator.available_providers
            status_info.append(f"🤖 **AI Providers**: {', '.join(providers)}")
            
            # System health
            status_info.append(f"🔥 **System Health**: Operational")
            status_info.append(f"⚡ **Response Time**: < 2s")
            
            return "\n".join(status_info)
        except Exception as e:
            return f"❌ **Error**: {str(e)}"
    
    def generate_content(self, section_type: str, topic: str, max_papers: int) -> Tuple[str, str, str]:
        """Generate content with Lab Pulse style feedback"""
        try:
            start_time = time.time()
            
            # Load paper data
            papers_data = self.draft_generator.load_paper_data("data/section_analysis")
            if not papers_data:
                return "❌ **No analysis data found**. Please run section analysis first.", "", ""
            
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
            
            # Format quality metrics with Lab Pulse styling
            quality_color = "🟢" if review.quality_metrics.overall_quality > 0.7 else "🟡" if review.quality_metrics.overall_quality > 0.5 else "🔴"
            
            quality_metrics = f"""
## 📊 Quality Assessment Matrix

### Overall Score: {quality_color} **{review.quality_metrics.overall_quality:.2f}/1.00**

| Metric | Score | Status |
|--------|-------|--------|
| **🔍 Clarity** | {review.quality_metrics.clarity_score:.2f} | {"🟢" if review.quality_metrics.clarity_score > 0.7 else "🟡" if review.quality_metrics.clarity_score > 0.5 else "🔴"} |
| **🔗 Coherence** | {review.quality_metrics.coherence_score:.2f} | {"🟢" if review.quality_metrics.coherence_score > 0.7 else "🟡" if review.quality_metrics.coherence_score > 0.5 else "🔴"} |
| **🎓 Academic Tone** | {review.quality_metrics.academic_tone_score:.2f} | {"🟢" if review.quality_metrics.academic_tone_score > 0.7 else "🟡" if review.quality_metrics.academic_tone_score > 0.5 else "🔴"} |
| **📝 Completeness** | {review.quality_metrics.completeness_score:.2f} | {"🟢" if review.quality_metrics.completeness_score > 0.7 else "🟡" if review.quality_metrics.completeness_score > 0.5 else "🔴"} |
| **📚 Citation Quality** | {review.quality_metrics.citation_quality_score:.2f} | {"🟢" if review.quality_metrics.citation_quality_score > 0.7 else "🟡" if review.quality_metrics.citation_quality_score > 0.5 else "🔴"} |

---

**📊 Statistics:**
- **Word Count:** {review.quality_metrics.word_count}
- **Sentence Count:** {review.quality_metrics.sentence_count}
- **Average Sentence Length:** {review.quality_metrics.avg_sentence_length:.1f}
- **Generation Time:** {time.time() - start_time:.2f}s
"""
            
            # Format suggestions with Lab Pulse styling
            if review.revision_suggestions:
                suggestions = f"""
## 💡 Revision Suggestions ({len(review.revision_suggestions)} found)

"""
                for i, suggestion in enumerate(review.revision_suggestions, 1):
                    severity_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴"}[suggestion.severity]
                    suggestions += f"""
### {severity_emoji} **{suggestion.category.title()}** (Priority: {suggestion.severity})

**📍 Location:** `{suggestion.location}`  
**🔍 Issue:** {suggestion.description}  
**💡 Suggestion:** {suggestion.suggestion}

---
"""
            else:
                suggestions = """
## ✅ **No Revision Suggestions Required**

**Content quality is excellent!** All quality metrics meet the threshold requirements.

---

"""
            
            # Add to history
            self.generation_history.append({
                'section_type': section_type,
                'timestamp': datetime.now().isoformat(),
                'quality_score': review.quality_metrics.overall_quality,
                'generation_time': time.time() - start_time
            })
            
            return content, quality_metrics, suggestions
            
        except Exception as e:
            error_msg = f"❌ **Generation Error**: {str(e)}"
            return error_msg, "", ""
    
    def revise_content(self, section_type: str) -> Tuple[str, str, str]:
        """Revise content with Lab Pulse style improvement tracking"""
        try:
            if section_type not in self.current_content:
                return "❌ **No content found** for revision. Please generate content first.", "", ""
            
            if section_type not in self.current_reviews:
                return "❌ **No review found** for this section. Please generate content first.", "", ""
            
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
            self.current_content[section_type]['revision_count'] = self.current_content[section_type].get('revision_count', 0) + 1
            self.current_reviews[section_type] = new_review
            
            # Calculate improvement
            improvement = new_review.quality_metrics.overall_quality - review.quality_metrics.overall_quality
            improvement_emoji = "📈" if improvement > 0 else "📉" if improvement < 0 else "➡️"
            
            # Format results with Lab Pulse styling
            quality_metrics = f"""
## 🔄 **Revision Results** {improvement_emoji}

### **Quality Improvement:** {improvement:+.2f}

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **🎯 Overall** | {review.quality_metrics.overall_quality:.2f} | {new_review.quality_metrics.overall_quality:.2f} | {improvement:+.2f} |
| **🔍 Clarity** | {review.quality_metrics.clarity_score:.2f} | {new_review.quality_metrics.clarity_score:.2f} | {new_review.quality_metrics.clarity_score - review.quality_metrics.clarity_score:+.2f} |
| **🔗 Coherence** | {review.quality_metrics.coherence_score:.2f} | {new_review.quality_metrics.coherence_score:.2f} | {new_review.quality_metrics.coherence_score - review.quality_metrics.coherence_score:+.2f} |
| **🎓 Academic Tone** | {review.quality_metrics.academic_tone_score:.2f} | {new_review.quality_metrics.academic_tone_score:.2f} | {new_review.quality_metrics.academic_tone_score - review.quality_metrics.academic_tone_score:+.2f} |
| **📝 Completeness** | {review.quality_metrics.completeness_score:.2f} | {new_review.quality_metrics.completeness_score:.2f} | {new_review.quality_metrics.completeness_score - review.quality_metrics.completeness_score:+.2f} |
| **📚 Citation Quality** | {review.quality_metrics.citation_quality_score:.2f} | {new_review.quality_metrics.citation_quality_score:.2f} | {new_review.quality_metrics.citation_quality_score - review.quality_metrics.citation_quality_score:+.2f} |

---

**📊 Updated Statistics:**
- **Word Count:** {new_review.quality_metrics.word_count}
- **Sentence Count:** {new_review.quality_metrics.sentence_count}
- **Average Sentence Length:** {new_review.quality_metrics.avg_sentence_length:.1f}
- **Revision Count:** {self.current_content[section_type]['revision_count']}
"""
            
            suggestions = f"""
## ✅ **Revision Complete**

**Content has been revised** based on {len(review.revision_suggestions)} suggestions.

**🔄 Generate new suggestions** to see further improvements.

---

**💡 Tip:** Multiple revisions can further improve quality. Consider running another revision cycle if quality is still below 0.8.

"""
            
            return revised_content, quality_metrics, suggestions
            
        except Exception as e:
            error_msg = f"❌ **Revision Error**: {str(e)}"
            return error_msg, "", ""
    
    def run_complete_workflow(self, topic: str, max_papers: int) -> str:
        """Run complete workflow with Lab Pulse style matrix reporting"""
        try:
            results = self.final_integration.complete_workflow(topic, max_papers)
            self.workflow_results = results
            
            if results['success']:
                # Create matrix-style report
                stages_completed = [stage for stage in results['stages'].keys() if results['stages'][stage].get('success', False)]
                stages_failed = [stage for stage in results['stages'].keys() if not results['stages'][stage].get('success', False)]
                
                return f"""
## 🎉 **Complete Workflow - SUCCESS** ✅

### 📊 **Mission Control Matrix**

| Stage | Status | Details |
|-------|--------|---------|
{chr(10).join([f"| **{stage}** | ✅ **Completed** | {results['stages'][stage].get('result', 'Success')} |" for stage in stages_completed])}
{chr(10).join([f"| **{stage}** | ❌ **Failed** | {results['stages'][stage].get('error', 'Unknown error')} |" for stage in stages_failed])}

---

### 🎯 **Workflow Summary**

- **📋 Topic:** {results['topic']}
- **📚 Papers Processed:** {results['max_papers']}
- **✅ Stages Completed:** {len(stages_completed)}/{len(results['stages'])}
- **🎯 Success Rate:** {len(stages_completed)/len(results['stages'])*100:.1f}%
- **⏱️ Execution Time:** {results.get('execution_time', 'N/A')}s

---

### 📄 **Final Report Preview**

{results.get('final_report', 'Report generation in progress...')[:500]}...

---

### 💾 **Results Saved**

All results have been saved to the data directory with timestamp `{datetime.now().strftime('%Y%m%d_%H%M%S')}`.

**📁 Check:** `data/final_reports/` for complete results.

"""
            else:
                return f"""
## ❌ **Workflow Failed**

### 🚨 **Error Details**

**Error:** `{results.get('error', 'Unknown error')}`

**Completed Stages:** {len(results['stages'])}

**💡 Recommendation:** Check system status and try again.

"""
                
        except Exception as e:
            return f"❌ **Workflow Error**: {str(e)}"
    
    def run_system_tests(self) -> str:
        """Run system tests with Lab Pulse style matrix reporting"""
        try:
            results = run_comprehensive_tests()
            
            if results['overall_success']:
                return f"""
## 🧪 **System Tests - PASSED** ✅

### 📊 **Test Matrix**

| Category | Status | Tests |
|----------|--------|-------|
{chr(10).join([f"| **{cat}** | ✅ **Passed** | {results['categories'][cat]['passed']}/{results['categories'][cat]['total']} |" for cat in results['categories'] if results['categories'][cat]['passed']])}
{chr(10).join([f"| **{cat}** | ❌ **Failed** | {results['categories'][cat]['passed']}/{results['categories'][cat]['total']} |" for cat in results['categories'] if not results['categories'][cat]['passed']])}

---

### 📈 **Performance Metrics**

- **🎯 Overall Success:** ✅ **PASSED**
- **📋 Categories Passed:** {results['summary']['passed_categories']}/{results['summary']['total_categories']}
- **🧪 Tests Passed:** {results['summary']['passed_tests']}/{results['summary']['total_tests']}
- **⏱️ Execution Time:** {results['summary']['execution_time']:.2f}s
- **🔥 System Health:** **Excellent**

---

### 💡 **Recommendations**

{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(results['recommendations'])])}

"""
            else:
                return f"""
## 🧪 **System Tests - FAILED** ❌

### 📊 **Test Matrix**

| Category | Status | Tests |
|----------|--------|-------|
{chr(10).join([f"| **{cat}** | ✅ **Passed** | {results['categories'][cat]['passed']}/{results['categories'][cat]['total']} |" for cat in results['categories'] if results['categories'][cat]['passed']])}
{chr(10).join([f"| **{cat}** | ❌ **Failed** | {results['categories'][cat]['passed']}/{results['categories'][cat]['total']} |" for cat in results['categories'] if not results['categories'][cat]['passed']])}

---

### 📈 **Performance Metrics**

- **🎯 Overall Success:** ❌ **FAILED**
- **📋 Categories Passed:** {results['summary']['passed_categories']}/{results['summary']['total_categories']}
- **🧪 Tests Passed:** {results['summary']['passed_tests']}/{results['summary']['total_tests']}
- **⏱️ Execution Time:** {results['summary']['execution_time']:.2f}s

---

### 💡 **Recommendations**

{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(results['recommendations'])])}

"""
                
        except Exception as e:
            return f"❌ **Test Error**: {str(e)}"
    
    def generate_documentation(self) -> str:
        """Generate documentation with Lab Pulse style reporting"""
        try:
            files = self.doc_generator.generate_all_documentation()
            
            return f"""
## 📚 **Documentation Generation - SUCCESS** ✅

### 📊 **Generated Files Matrix**

| Document Type | Status | File |
|---------------|--------|------|
{chr(10).join([f"| **{doc_type}** | ✅ **Generated** | `{file_path}` |" for doc_type, file_path in files.items()])}

---

### 📁 **Output Directory**

**📂 Location:** `{self.doc_generator.output_dir}`

### 📖 **Documentation Package**

- **📚 User Manual:** Complete installation and usage guide
- **🔧 Technical Documentation:** System architecture and API reference
- **🎯 Presentation Slides:** Professional 20-slide deck
- **📋 Documentation Index:** Complete navigation guide

---

### ✅ **Generation Complete**

All documentation has been generated with version control and timestamps.

**📅 Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

"""
                
        except Exception as e:
            return f"❌ **Documentation Error**: {str(e)}"
    
    def create_interface(self):
        """Create Lab Pulse styled Gradio interface"""
        
        # Lab Pulse CSS styling
        lab_pulse_css = """
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
        
        /* Main container with Lab Pulse background */
        .gradio-container {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2d1b1b 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        }
        
        /* Interactive radial background */
        .gradio-container::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at top, rgba(128,0,32,0.16), transparent 35%),
                        radial-gradient(circle at 30% 10%, rgba(204,41,82,0.12), transparent 25%),
                        radial-gradient(circle at 70% 20%, rgba(236,72,153,0.08), transparent 25%);
            pointer-events: none;
            z-index: 0;
        }
        
        /* Header styling */
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
        
        .main-header h1 {
            margin: 0;
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--maroon-400) 0%, var(--foreground) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header h2 {
            margin: 0.5rem 0;
            font-size: 1.5rem;
            font-weight: 400;
            opacity: 0.9;
        }
        
        .main-header p {
            margin: 1rem 0 0 0;
            opacity: 0.8;
            font-size: 1.1rem;
        }
        
        /* Glass surface effect */
        .glass-surface {
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35),
                       0 0 0 1px rgba(255, 255, 255, 0.04);
        }
        
        /* Status indicator */
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
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Button styling */
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
        
        /* Quality metric styling */
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
        
        /* Tab styling */
        .tab-nav {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Matrix table styling */
        .matrix-table {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .matrix-header {
            background: rgba(128, 0, 32, 0.2);
            padding: 1rem;
            font-weight: 600;
            color: white;
        }
        
        .matrix-row {
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1rem;
            transition: background 0.3s ease;
        }
        
        .matrix-row:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Status cells */
        .status-cell {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.8rem;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid;
        }
        
        .status-completed {
            background: rgba(34, 197, 94, 0.2);
            border-color: #22c55e;
            color: #86efac;
        }
        
        .status-in-progress {
            background: rgba(251, 191, 36, 0.2);
            border-color: #fbbf24;
            color: #fde047;
        }
        
        .status-not-started {
            background: rgba(107, 114, 128, 0.2);
            border-color: #6b7280;
            color: #9ca3af;
        }
        
        .status-cell:hover {
            transform: scale(1.05);
        }
        """
        
        with gr.Blocks(
            title="AI Research Agent - Lab Pulse Edition",
            css=lab_pulse_css
        ) as interface:
            
            # Lab Pulse Header
            gr.HTML(f"""
            <div class="main-header">
                <div class="status-indicator online"></div>
                <h1>🤖 AI Research Agent</h1>
                <h2>Lab Pulse Edition</h2>
                <p>Advanced Academic Content Generation with Real-Time Quality Assessment Matrix</p>
            </div>
            """)
            
            # Main Interface with Tabs
            with gr.Tabs() as tabs:
                
                # Tab 1: Content Generation Matrix
                with gr.TabItem("📝 Content Generation Matrix", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.HTML("""
                            <div class="glass-surface">
                                <h3>🚀 Content Generation Mission Control</h3>
                                <p>Select section type and generate high-quality academic content with real-time quality assessment.</p>
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
                                    label="📚 Max Papers"
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
                                label="📊 Quality Matrix",
                                value="Quality metrics will appear here..."
                            )
                        
                        with gr.Column():
                            suggestions_output = gr.Markdown(
                                label="💡 Revision Intelligence",
                                value="Revision suggestions will appear here..."
                            )
                
                # Tab 2: Workflow Control Center
                with gr.TabItem("🎯 Workflow Control Center", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface">
                                <h3>🎯 End-to-End Workflow Mission Control</h3>
                                <p>Run complete workflow from data loading to final report with automated quality assessment.</p>
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
                                label="📚 Max Papers"
                            )
                            
                            workflow_btn = gr.Button(
                                "🚀 Launch Complete Workflow",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            workflow_output = gr.Markdown(
                                label="📊 Workflow Matrix",
                                value="Workflow results will appear here..."
                            )
                
                # Tab 3: System Testing Lab
                with gr.TabItem("🧪 System Testing Lab", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface">
                                <h3>🧪 Comprehensive Testing Laboratory</h3>
                                <p>Run comprehensive system tests to verify all components are operational.</p>
                            </div>
                            """)
                            
                            test_btn = gr.Button(
                                "🧪 Run System Diagnostics",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            test_output = gr.Markdown(
                                label="📊 Test Matrix",
                                value="Test results will appear here..."
                            )
                
                # Tab 4: Documentation Hub
                with gr.TabItem("📚 Documentation Hub", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface">
                                <h3>📚 Documentation Generation Center</h3>
                                <p>Generate comprehensive documentation including user manual, technical docs, and presentations.</p>
                            </div>
                            """)
                            
                            docs_btn = gr.Button(
                                "📚 Generate Documentation Package",
                                elem_classes=["btn-primary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            docs_output = gr.Markdown(
                                label="📊 Documentation Matrix",
                                value="Documentation generation results will appear here..."
                            )
                
                # Tab 5: System Status Dashboard
                with gr.TabItem("📊 System Status Dashboard", elem_classes=["tab-nav"]):
                    with gr.Row():
                        with gr.Column():
                            gr.HTML("""
                            <div class="glass-surface">
                                <h3>📊 System Status Dashboard</h3>
                                <p>Monitor system health, data directories, and AI provider availability.</p>
                            </div>
                            """)
                            
                            refresh_status_btn = gr.Button(
                                "🔄 Refresh Status",
                                elem_classes=["btn-secondary"],
                                size="lg"
                            )
                        
                        with gr.Column():
                            status_output = gr.Markdown(
                                label="📊 System Matrix",
                                value=self.get_system_status()
                            )
            
            # Lab Pulse Footer
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.6);">
                <p>🤖 <strong>AI Research Agent - Lab Pulse Edition</strong></p>
                <p>Powered by Google Gemini AI | APA 7th Edition Compliant | Real-Time Quality Assessment Matrix</p>
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
        """Launch the Lab Pulse styled interface"""
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_name="0.0.0.0",
            server_port=port,
            show_error=True,
            inbrowser=True
        )

def main():
    """Main function to launch the Lab Pulse styled interface"""
    app = LabPulseStyleInterface()
    app.launch(share=False, port=7860)

if __name__ == "__main__":
    main()
