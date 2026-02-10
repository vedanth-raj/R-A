"""
Futuristic Glassmorphic AI Systematic Review System
Built with Gradio - 2025-2026 Design Trends
Features: Interactive canvas background, mouse-responsive energy waves, glassmorphism
"""

import gradio as gr
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple, Generator

# Mock LangGraph integration
class MockGraphApp:
    """Simulates LangGraph workflow for demo purposes"""
    
    def stream(self, inputs: Dict) -> Generator:
        """Simulate streaming workflow stages"""
        topic = inputs.get("topic", "AI Research")
        num_papers = inputs.get("num_papers", 3)
        
        # Stage 1: Planning
        yield {"stage": "planning", "message": "Planning research strategy..."}
        time.sleep(0.5)
        
        # Stage 2: Searching
        yield {"stage": "searching", "message": f"Searching for papers on '{topic}'..."}
        time.sleep(1)
        
        # Stage 3: Papers found
        papers = self._generate_mock_papers(topic, num_papers)
        yield {"stage": "papers", "data": papers}
        time.sleep(0.5)
        
        # Stage 4: Downloading
        yield {"stage": "downloading", "message": f"Downloading {num_papers} papers..."}
        time.sleep(1)
        
        # Stage 5: Analyzing
        yield {"stage": "analyzing", "message": "Extracting text and analyzing content..."}
        time.sleep(1.5)
        
        # Stage 6: Findings
        findings = self._generate_findings(papers)
        yield {"stage": "findings", "data": findings}
        
        # Stage 7: Synthesizing
        yield {"stage": "synthesizing", "message": "Synthesizing results across papers..."}
        time.sleep(1)
        
        # Stage 8: Draft generation
        draft = self._generate_draft(topic, papers)
        yield {"stage": "draft", "data": draft}
        
        yield {"stage": "complete", "message": "Review complete!"}
    
    def _generate_mock_papers(self, topic: str, count: int) -> List[Dict]:
        """Generate mock paper data"""
        papers = []
        authors_list = [
            ["Smith, J.", "Johnson, A."], ["Chen, L.", "Wang, Y.", "Liu, X."],
            ["Garcia, M.", "Rodriguez, P."], ["Kumar, R.", "Patel, S."],
            ["Anderson, K.", "Brown, T."], ["Lee, H.", "Kim, J."]
        ]
        for i in range(count):
            papers.append({
                "title": f"Advanced {topic} Methods: A Comprehensive Study {i+1}",
                "authors": ", ".join(random.choice(authors_list)),
                "year": random.randint(2020, 2024),
                "citations": random.randint(10, 500),
                "doi": f"10.1000/example.{random.randint(1000, 9999)}"
            })
        return papers
    
    def _generate_findings(self, papers: List[Dict]) -> Dict:
        """Generate mock analysis findings"""
        return {
            "key_themes": [
                "Machine learning applications show 85% accuracy improvement",
                "Deep learning models outperform traditional methods",
                "Data preprocessing is critical for model performance"
            ],
            "overlaps": "All papers emphasize the importance of large datasets",
            "gaps": "Limited research on real-world deployment challenges"
        }
    
    def _generate_draft(self, topic: str, papers: List[Dict]) -> Dict:
        """Generate mock draft sections"""
        return {
            "abstract": f"This systematic review examines {topic} across {len(papers)} recent studies. "
                       f"Our analysis reveals significant advances in methodology and applications. "
                       f"Key findings indicate strong consensus on best practices with emerging opportunities for innovation.",
            "methods": f"We conducted a systematic search for papers on {topic} published between 2020-2024. "
                      f"Papers were selected based on relevance, citation count, and methodological rigor. "
                      f"Data extraction focused on research design, sample characteristics, and key outcomes.",
            "results": f"Analysis of {len(papers)} papers revealed three major themes: (1) methodological innovations, "
                      f"(2) practical applications, and (3) future research directions. "
                      f"Cross-paper comparison showed high agreement on core principles with variation in implementation details.",
            "references": "\n".join([f"{p['authors']} ({p['year']}). {p['title']}. DOI: {p['doi']}" for p in papers])
        }

# Initialize mock graph
graph_app = MockGraphApp()

# Custom CSS for futuristic glassmorphic design
CUSTOM_CSS = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

/* Global Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, #root {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a2332 50%, #2a1810 100%);
    color: #e0e0e0;
    overflow-x: hidden;
}

/* Canvas Background */
#bg-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    pointer-events: none;
}

/* Glassmorphic Container */
.glass-container {
    background: rgba(20, 20, 40, 0.25);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
        0 8px 32px 0 rgba(0, 0, 0, 0.37),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.05),
        0 0 40px rgba(255, 69, 0, 0.1);
    padding: 2rem;
    margin: 1rem 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-container:hover {
    transform: translateY(-4px);
    box-shadow: 
        0 12px 48px 0 rgba(0, 0, 0, 0.5),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.1),
        0 0 60px rgba(255, 69, 0, 0.2);
    border-color: rgba(255, 140, 0, 0.3);
}

/* Login Card */
.login-card {
    max-width: 450px;
    margin: 10vh auto;
    background: rgba(15, 15, 35, 0.3);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 28px;
    border: 2px solid rgba(255, 140, 0, 0.2);
    box-shadow: 
        0 16px 64px rgba(0, 0, 0, 0.6),
        inset 0 2px 4px rgba(255, 255, 255, 0.05),
        0 0 80px rgba(255, 69, 0, 0.15);
    padding: 3rem 2.5rem;
    animation: fadeInScale 0.6s ease-out;
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(20px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* Title Styles */
.neon-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #ff4500 0%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(255, 69, 0, 0.5);
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
}

.subtitle {
    text-align: center;
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.95rem;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}

/* Input Fields */
.gradio-textbox, .gradio-slider, input, textarea {
    background: rgba(30, 30, 50, 0.4) !important;
    border: 1px solid rgba(255, 140, 0, 0.2) !important;
    border-radius: 12px !important;
    color: #e0e0e0 !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.gradio-textbox:focus, input:focus, textarea:focus {
    border-color: rgba(255, 140, 0, 0.6) !important;
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.3) !important;
    outline: none !important;
}

/* Primary Button - Neon Orange Gradient */
.primary-btn, button.primary {
    background: linear-gradient(135deg, #ff4500 0%, #ffd700 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    color: #000 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 1rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(255, 69, 0, 0.4) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
}

.primary-btn:hover, button.primary:hover {
    transform: scale(1.08) !important;
    box-shadow: 
        0 8px 40px rgba(255, 69, 0, 0.6),
        0 0 60px rgba(255, 140, 0, 0.4) !important;
}

.primary-btn:active, button.primary:active {
    transform: scale(1.02) !important;
}

/* Secondary Buttons */
.secondary-btn, button.secondary {
    background: rgba(30, 30, 50, 0.5) !important;
    border: 1px solid rgba(255, 140, 0, 0.3) !important;
    border-radius: 12px !important;
    color: #ff8c00 !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

.secondary-btn:hover, button.secondary:hover {
    background: rgba(255, 69, 0, 0.2) !important;
    border-color: rgba(255, 140, 0, 0.6) !important;
    box-shadow: 0 4px 20px rgba(255, 69, 0, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Progress Bar */
.progress-bar {
    background: rgba(30, 30, 50, 0.6);
    border-radius: 20px;
    height: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4500, #ffd700, #ff4500);
    background-size: 200% 100%;
    animation: progressShine 2s linear infinite;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.6);
}

@keyframes progressShine {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* Table Styles */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
}

th {
    background: rgba(255, 69, 0, 0.2);
    color: #ffd700;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
}

td {
    background: rgba(30, 30, 50, 0.4);
    padding: 1rem;
    border-top: 1px solid rgba(255, 140, 0, 0.1);
    border-bottom: 1px solid rgba(255, 140, 0, 0.1);
}

tr:hover td {
    background: rgba(255, 69, 0, 0.1);
}

/* Accordion Styles */
.accordion {
    background: rgba(20, 20, 40, 0.3);
    border: 1px solid rgba(255, 140, 0, 0.2);
    border-radius: 12px;
    margin: 0.5rem 0;
    overflow: hidden;
}

.accordion-header {
    background: rgba(255, 69, 0, 0.1);
    padding: 1rem 1.5rem;
    cursor: pointer;
    font-weight: 600;
    color: #ff8c00;
    transition: all 0.3s ease;
}

.accordion-header:hover {
    background: rgba(255, 69, 0, 0.2);
}

/* Status Badge */
.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #ff4500, #ffd700);
    color: #000;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 4px 15px rgba(255, 69, 0, 0.4);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.05); }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(10, 10, 20, 0.5);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ff4500, #ffd700);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ffd700, #ff4500);
}

/* Responsive Design */
@media (max-width: 768px) {
    .login-card {
        margin: 5vh 1rem;
        padding: 2rem 1.5rem;
    }
    
    .neon-title {
        font-size: 2rem;
    }
    
    .glass-container {
        padding: 1.5rem;
    }
}

/* Animation for elements */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Glow effect on hover */
.glow-on-hover {
    transition: all 0.3s ease;
}

.glow-on-hover:hover {
    filter: drop-shadow(0 0 20px rgba(255, 69, 0, 0.6));
}
"""

# Custom JavaScript for interactive canvas background
CUSTOM_JS = """
<canvas id="bg-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Mouse position
    let mouse = { x: -1000, y: -1000 };
    
    // Diagonal rays configuration
    const rays = [];
    const numRays = 12;
    const originX = canvas.width * 1.2;  // Bottom-right origin
    const originY = canvas.height * 1.2;
    
    // Initialize rays
    for (let i = 0; i < numRays; i++) {
        const angle = -Math.PI * 0.7 + (i / numRays) * Math.PI * 0.4;
        const baseWidth = 40 + Math.random() * 60;
        const length = Math.max(canvas.width, canvas.height) * 1.5;
        
        rays.push({
            angle: angle,
            baseAngle: angle,
            width: baseWidth,
            length: length,
            opacity: 0.15 + Math.random() * 0.25,
            speed: 0.0005 + Math.random() * 0.001,
            offset: Math.random() * Math.PI * 2,
            distortion: 0,
            targetDistortion: 0,
            color: i % 3 === 0 ? 'rgba(255, 140, 0, ' : 
                   i % 3 === 1 ? 'rgba(255, 180, 0, ' : 
                   'rgba(255, 100, 0, '
        });
    }

    
    // Track mouse movement
    document.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    
    // Handle window resize
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    
    // Animation loop
    let time = 0;
    function animate() {
        // Dark background with slight gradient
        const gradient = ctx.createRadialGradient(
            canvas.width * 0.8, canvas.height * 0.8, 0,
            canvas.width * 0.8, canvas.height * 0.8, canvas.width
        );
        gradient.addColorStop(0, 'rgba(30, 20, 10, 1)');
        gradient.addColorStop(0.5, 'rgba(15, 15, 20, 1)');
        gradient.addColorStop(1, 'rgba(5, 10, 15, 1)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        time += 0.01;
        
        // Calculate mouse influence
        const mouseAngle = Math.atan2(mouse.y - originY, mouse.x - originX);
        const mouseDist = Math.sqrt(
            Math.pow(mouse.x - originX, 2) + 
            Math.pow(mouse.y - originY, 2)
        );
        
        rays.forEach((ray, index) => {
            // Animate ray angle slightly
            const angleOffset = Math.sin(time * ray.speed + ray.offset) * 0.05;
            
            // Mouse interaction - rays avoid mouse
            if (mouseDist < 400) {
                const angleDiff = mouseAngle - ray.baseAngle;
                const influence = (1 - mouseDist / 400) * 0.3;
                ray.targetDistortion = -Math.sign(angleDiff) * influence;
            } else {
                ray.targetDistortion = 0;
            }
            
            // Smooth distortion
            ray.distortion += (ray.targetDistortion - ray.distortion) * 0.1;
            ray.angle = ray.baseAngle + angleOffset + ray.distortion;
            
            // Calculate ray endpoints
            const endX = originX + Math.cos(ray.angle) * ray.length;
            const endY = originY + Math.sin(ray.angle) * ray.length;
            
            // Draw ray with gradient
            const rayGradient = ctx.createLinearGradient(
                originX, originY, endX, endY
            );
            rayGradient.addColorStop(0, ray.color + ray.opacity + ')');
            rayGradient.addColorStop(0.6, ray.color + (ray.opacity * 0.4) + ')');
            rayGradient.addColorStop(1, ray.color + '0)');
            
            // Draw main ray
            ctx.save();
            ctx.globalCompositeOperation = 'lighter';
            
            // Outer glow
            ctx.shadowBlur = 60;
            ctx.shadowColor = ray.color + (ray.opacity * 0.8) + ')';
            
            ctx.beginPath();
            ctx.moveTo(originX, originY);
            
            // Create ray shape
            const perpAngle = ray.angle + Math.PI / 2;
            const halfWidth = ray.width / 2;
            
            ctx.lineTo(
                originX + Math.cos(perpAngle) * halfWidth,
                originY + Math.sin(perpAngle) * halfWidth
            );
            ctx.lineTo(
                endX + Math.cos(perpAngle) * (halfWidth * 0.3),
                endY + Math.sin(perpAngle) * (halfWidth * 0.3)
            );
            ctx.lineTo(
                endX - Math.cos(perpAngle) * (halfWidth * 0.3),
                endY - Math.sin(perpAngle) * (halfWidth * 0.3)
            );
            ctx.lineTo(
                originX - Math.cos(perpAngle) * halfWidth,
                originY - Math.sin(perpAngle) * halfWidth
            );
            ctx.closePath();
            
            ctx.fillStyle = rayGradient;
            ctx.fill();
            
            // Inner bright core
            ctx.shadowBlur = 30;
            ctx.beginPath();
            ctx.moveTo(originX, originY);
            ctx.lineTo(
                originX + Math.cos(perpAngle) * (halfWidth * 0.3),
                originY + Math.sin(perpAngle) * (halfWidth * 0.3)
            );
            ctx.lineTo(
                endX + Math.cos(perpAngle) * (halfWidth * 0.1),
                endY + Math.sin(perpAngle) * (halfWidth * 0.1)
            );
            ctx.lineTo(
                endX - Math.cos(perpAngle) * (halfWidth * 0.1),
                endY - Math.sin(perpAngle) * (halfWidth * 0.1)
            );
            ctx.lineTo(
                originX - Math.cos(perpAngle) * (halfWidth * 0.3),
                originY - Math.sin(perpAngle) * (halfWidth * 0.3)
            );
            ctx.closePath();
            ctx.fill();
            
            ctx.restore();
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
})();
</script>
"""

# Application functions
def start_research(topic: str, num_papers: int, date_from: str, date_to: str, 
                   open_access: bool) -> Generator:
    """Start the research workflow"""
    if not topic or topic.strip() == "":
        yield (
            gr.update(value="❌ Please enter a research topic"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )
        return
    
    # Show progress panel
    yield (
        gr.update(value=f"🚀 Starting research on: {topic}"),
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False)
    )
    
    papers_data = []
    findings_data = {}
    draft_data = {}
    
    # Stream workflow stages
    for event in graph_app.stream({"topic": topic, "num_papers": num_papers}):
        stage = event.get("stage")
        message = event.get("message", "")
        
        if stage == "planning":
            yield (
                gr.update(value=f"📋 {message}"),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        
        elif stage == "searching":
            yield (
                gr.update(value=f"🔍 {message}"),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        
        elif stage == "papers":
            papers_data = event.get("data", [])
            papers_md = "## 📚 Retrieved Papers\n\n"
            papers_md += "| Title | Authors | Year | Citations |\n"
            papers_md += "|-------|---------|------|----------|\n"
            for paper in papers_data:
                papers_md += f"| {paper['title']} | {paper['authors']} | {paper['year']} | {paper['citations']} |\n"
            
            yield (
                gr.update(value=f"✅ Found {len(papers_data)} papers"),
                gr.update(visible=True),
                gr.update(value=papers_md, visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        
        elif stage == "downloading":
            yield (
                gr.update(value=f"⬇️ {message}"),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        
        elif stage == "analyzing":
            yield (
                gr.update(value=f"🔬 {message}"),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        
        elif stage == "findings":
            findings_data = event.get("data", {})
            findings_md = "## 🎯 Key Findings\n\n"
            findings_md += "### Main Themes:\n"
            for theme in findings_data.get("key_themes", []):
                findings_md += f"- {theme}\n"
            findings_md += f"\n### Cross-Paper Overlaps:\n{findings_data.get('overlaps', '')}\n"
            findings_md += f"\n### Research Gaps:\n{findings_data.get('gaps', '')}\n"
            
            yield (
                gr.update(value="✨ Analysis complete"),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(value=findings_md, visible=True),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        
        elif stage == "synthesizing":
            yield (
                gr.update(value=f"🧬 {message}"),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        
        elif stage == "draft":
            draft_data = event.get("data", {})
            draft_md = "## 📝 Generated Draft\n\n"
            draft_md += f"### Abstract\n{draft_data.get('abstract', '')}\n\n"
            draft_md += f"### Methods\n{draft_data.get('methods', '')}\n\n"
            draft_md += f"### Results\n{draft_data.get('results', '')}\n\n"
            draft_md += f"### References\n{draft_data.get('references', '')}\n"
            
            yield (
                gr.update(value="📄 Draft generated successfully!"),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(value=draft_md, visible=True)
            )
        
        elif stage == "complete":
            yield (
                gr.update(value="🎉 Review complete! Ready for download."),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True)
            )

def reset_app():
    """Reset the application"""
    return (
        "",  # topic
        3,   # num_papers
        "",  # status
        gr.update(visible=False),  # progress
        gr.update(visible=False),  # papers
        gr.update(visible=False),  # analyze btn
        gr.update(visible=False),  # findings
        gr.update(visible=False),  # generate btn
        gr.update(visible=False)   # draft
    )

# Build the Gradio interface
with gr.Blocks(
    title="AI Systematic Review Generator"
) as demo:
    
    # Add canvas background
    gr.HTML(CUSTOM_JS, visible=False)
    
    # Main Dashboard (directly visible, no login)
    with gr.Column(visible=True, elem_classes="glass-container") as dashboard:
        # Header
        with gr.Row():
            gr.HTML('<h1 class="neon-title">AI SYSTEMATIC REVIEW GENERATOR</h1>')
        
        gr.Markdown("---")
        
        # Input Panel
        with gr.Group(elem_classes="glass-container"):
            gr.Markdown("## 🎯 Research Configuration")
            
            topic_input = gr.Textbox(
                label="Research Topic",
                placeholder="e.g., Machine Learning in Climate Change Prediction",
                lines=2,
                elem_classes="glass-input"
            )
            
            num_papers_slider = gr.Slider(
                minimum=1,
                maximum=10,
                value=3,
                step=1,
                label="Number of Papers to Analyze",
                elem_classes="glass-slider"
            )
            
            with gr.Accordion("🔧 Advanced Filters", open=False):
                with gr.Row():
                    date_from = gr.Textbox(label="From Year", placeholder="2020", scale=1)
                    date_to = gr.Textbox(label="To Year", placeholder="2024", scale=1)
                open_access_only = gr.Checkbox(label="Open Access Only", value=True)
            
            start_btn = gr.Button(
                "🚀 START RESEARCH",
                elem_classes="primary-btn",
                size="lg"
            )
        
        # Status and Progress
        status_text = gr.Textbox(
            label="Status",
            interactive=False,
            elem_classes="status-display"
        )
        
        progress_panel = gr.HTML(
            '<div class="progress-bar"><div class="progress-fill" style="width: 0%"></div></div>',
            visible=False
        )
        
        # Papers Display
        papers_display = gr.Markdown(
            label="Retrieved Papers",
            visible=False,
            elem_classes="glass-container"
        )
        
        # Analysis Button
        analyze_btn = gr.Button(
            "🔬 ANALYZE & COMPARE",
            elem_classes="secondary-btn",
            size="lg",
            visible=False
        )
        
        # Findings Display
        findings_display = gr.Markdown(
            label="Analysis Results",
            visible=False,
            elem_classes="glass-container"
        )
        
        # Generate Draft Button
        generate_btn = gr.Button(
            "📝 GENERATE DRAFT",
            elem_classes="secondary-btn",
            size="lg",
            visible=False
        )
        
        # Draft Display
        draft_display = gr.Markdown(
            label="Generated Draft",
            visible=False,
            elem_classes="glass-container"
        )
        
        # Action Buttons
        gr.Markdown("---")
        with gr.Row():
            revise_btn = gr.Button("🔄 Revise Draft", elem_classes="secondary-btn")
            download_report_btn = gr.Button("📥 Download Report (PDF)", elem_classes="secondary-btn")
            download_papers_btn = gr.Button("📚 Download All Papers", elem_classes="secondary-btn")
            reset_btn = gr.Button("🔃 Reset", elem_classes="secondary-btn")
            share_btn = gr.Button("🔗 Share", elem_classes="secondary-btn")
    
    # Event Handlers
    
    # Start Research
    start_btn.click(
        fn=start_research,
        inputs=[topic_input, num_papers_slider, date_from, date_to, open_access_only],
        outputs=[
            status_text,
            progress_panel,
            papers_display,
            analyze_btn,
            findings_display,
            generate_btn,
            draft_display
        ]
    )
    
    # Reset
    reset_btn.click(
        fn=reset_app,
        outputs=[
            topic_input,
            num_papers_slider,
            status_text,
            progress_panel,
            papers_display,
            analyze_btn,
            findings_display,
            generate_btn,
            draft_display
        ]
    )
    
    # Mock handlers for other buttons
    def show_message(msg):
        return gr.update(value=f"ℹ️ {msg}")
    
    revise_btn.click(
        fn=lambda: show_message("Revision feature coming soon!"),
        outputs=status_text
    )
    
    download_report_btn.click(
        fn=lambda: show_message("Downloading report..."),
        outputs=status_text
    )
    
    download_papers_btn.click(
        fn=lambda: show_message("Downloading papers..."),
        outputs=status_text
    )
    
    share_btn.click(
        fn=lambda: show_message("Share link generated!"),
        outputs=status_text
    )

# Launch the application
if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        theme=gr.themes.Glass(
            primary_hue="orange",
            secondary_hue="amber",
            neutral_hue="slate"
        ),
        css=CUSTOM_CSS
    )
