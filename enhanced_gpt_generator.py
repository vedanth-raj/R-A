"""
Enhanced GPT Draft Generator with Multiple AI Providers
Supports OpenAI, Google Gemini, and Mock generation
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

# Import AI providers
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.genai as genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

@dataclass
class DraftSection:
    """Represents a generated draft section."""
    title: str
    content: str
    word_count: int
    confidence_score: float
    ai_provider: str
    generation_time: float
    sources_used: List[str]

class EnhancedGPTDraftGenerator:
    """Enhanced GPT draft generator with multiple AI providers."""
    
    def __init__(self, preferred_provider: str = "gemini"):
        """Initialize the enhanced draft generator.
        
        Args:
            preferred_provider: Preferred AI provider ("openai", "gemini", "mock")
        """
        self.logger = logging.getLogger(__name__)
        self.preferred_provider = preferred_provider
        
        # Initialize AI providers
        self.openai_client = None
        self.gemini_client = None
        self.mock_generator = MockDraftGenerator()
        
        # Setup providers
        self._setup_providers()
        
        # Section templates
        self.section_templates = {
            'abstract': {
                'prompt_template': """Based on the following research papers, write a comprehensive abstract (200-300 words) that synthesizes the key findings and implications:

Paper Summaries:
{paper_summaries}

Key Findings:
{paper_findings}

Implications:
{paper_implications}

Write a professional abstract that includes:
1. Background context
2. Main findings from the papers
3. Key implications
4. Future research directions

Abstract:""",
                'max_tokens': 300,
                'temperature': 0.7
            },
            'introduction': {
                'prompt_template': """Based on the following research papers, write an introduction (400-600 words) that establishes the research context and objectives:

Paper Summaries:
{paper_summaries}

Key Findings:
{paper_findings}

Implications:
{paper_implications}

Write a comprehensive introduction that includes:
1. Background and context
2. Research problem statement
3. Objectives and scope
4. Significance of the study
5. Paper structure overview

Introduction:""",
                'max_tokens': 600,
                'temperature': 0.7
            },
            'methods': {
                'prompt_template': """Based on the following research papers, write a methods section (400-600 words) describing the systematic review methodology:

Paper Summaries:
{paper_summaries}

Methodological Approaches:
{paper_findings}

Write a detailed methods section that includes:
1. Research design and approach
2. Search strategy and selection criteria
3. Data extraction and analysis methods
4. Quality assessment procedures
5. Ethical considerations

Methods:""",
                'max_tokens': 600,
                'temperature': 0.6
            },
            'results': {
                'prompt_template': """Based on the following research papers, write a results section (500-700 words) presenting the key findings:

Paper Summaries:
{paper_summaries}

Key Findings:
{paper_findings}

Statistical Results:
{paper_implications}

Write a comprehensive results section that includes:
1. Overview of included studies
2. Main findings and patterns
3. Statistical analysis results
4. Comparative analysis
5. Significant observations

Results:""",
                'max_tokens': 700,
                'temperature': 0.6
            },
            'discussion': {
                'prompt_template': """Based on the following research papers, write a discussion section (500-700 words) interpreting the findings:

Paper Summaries:
{paper_summaries}

Key Findings:
{paper_findings}

Implications:
{paper_implications}

Write an insightful discussion that includes:
1. Interpretation of main findings
2. Comparison with existing literature
3. Theoretical and practical implications
4. Limitations of the study
5. Future research directions

Discussion:""",
                'max_tokens': 700,
                'temperature': 0.7
            }
        }
    
    def _setup_providers(self):
        """Setup available AI providers."""
        
        # Setup OpenAI
        if OPENAI_AVAILABLE:
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                try:
                    self.openai_client = openai.OpenAI(api_key=openai_key)
                    self.logger.info("OpenAI client initialized successfully")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize OpenAI: {e}")
        
        # Setup Gemini
        if GEMINI_AVAILABLE:
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key and gemini_key != 'your_gemini_api_key_here':
                try:
                    import google.genai as genai
                    from google.genai import types
                    self.gemini_client = genai.Client(api_key=gemini_key)
                    self.gemini_model = "gemini-2.5-flash"
                    self.logger.info("Gemini client initialized successfully")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize Gemini: {e}")
        
        # Determine available providers
        self.available_providers = []
        if self.openai_client:
            self.available_providers.append("openai")
        if self.gemini_client:
            self.available_providers.append("gemini")
        self.available_providers.append("mock")  # Always available
        
        self.logger.info(f"Available AI providers: {self.available_providers}")
    
    def get_best_provider(self) -> str:
        """Get the best available AI provider."""
        if self.preferred_provider in self.available_providers:
            return self.preferred_provider
        
        # Priority order: gemini > openai > mock
        for provider in ["gemini", "openai", "mock"]:
            if provider in self.available_providers:
                return provider
        
        return "mock"
    
    def generate_section_draft(self, section_type: str, papers_data: List[Dict], 
                             preferred_provider: Optional[str] = None) -> DraftSection:
        """Generate a draft section using the best available AI provider.
        
        Args:
            section_type: Type of section to generate
            papers_data: List of paper analysis data
            preferred_provider: Preferred AI provider
            
        Returns:
            DraftSection: Generated draft section
        """
        start_time = datetime.now()
        
        # Select provider
        provider = preferred_provider or self.get_best_provider()
        
        # Prepare input data
        summaries = self.extract_paper_summaries(papers_data)
        findings = self.extract_paper_findings(papers_data)
        implications = self.extract_paper_implications(papers_data)
        
        # Get template
        template = self.section_templates.get(section_type)
        if not template:
            raise ValueError(f"Unknown section type: {section_type}")
        
        # Generate content
        try:
            if provider == "openai" and self.openai_client:
                content = self._generate_with_openai(section_type, summaries, findings, implications, template)
            elif provider == "gemini" and self.gemini_client:
                content = self._generate_with_gemini(section_type, summaries, findings, implications, template)
            else:
                content = self.mock_generator.generate_mock_content(section_type, len(papers_data))
                provider = "mock"
            
            # Calculate metrics
            word_count = len(content.split())
            generation_time = (datetime.now() - start_time).total_seconds()
            confidence_score = self._calculate_confidence_score(content, provider)
            
            # Create draft section
            draft = DraftSection(
                title=section_type.title(),
                content=content,
                word_count=word_count,
                confidence_score=confidence_score,
                ai_provider=provider,
                generation_time=generation_time,
                sources_used=[paper.get('title', 'Unknown') for paper in papers_data[:5]]
            )
            
            self.logger.info(f"Generated {section_type} using {provider}: {word_count} words, confidence: {confidence_score:.2f}")
            return draft
            
        except Exception as e:
            self.logger.error(f"Error generating {section_type} with {provider}: {e}")
            # Fallback to mock
            return self.generate_section_draft(section_type, papers_data, "mock")
    
    def _generate_with_openai(self, section_type: str, summaries: str, findings: str, 
                            implications: str, template: Dict) -> str:
        """Generate content using OpenAI."""
        prompt = template['prompt_template'].format(
            paper_summaries=summaries,
            paper_findings=findings,
            paper_implications=implications
        )
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert academic writer specializing in research papers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=template['max_tokens'],
            temperature=template['temperature']
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_with_gemini(self, section_type: str, summaries: str, findings: str,
                            implications: str, template: Dict) -> str:
        """Generate content using Google Gemini."""
        from google.genai import types
        
        prompt = template['prompt_template'].format(
            paper_summaries=summaries,
            paper_findings=findings,
            paper_implications=implications
        )
        
        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=template['temperature'],
                max_output_tokens=template['max_tokens']
            )
        )
        
        return response.text.strip()
    
    def _calculate_confidence_score(self, content: str, provider: str) -> float:
        """Calculate confidence score for generated content."""
        base_scores = {
            "gemini": 0.85,
            "openai": 0.80,
            "mock": 0.60
        }
        
        base_score = base_scores.get(provider, 0.60)
        
        # Adjust based on content quality
        word_count = len(content.split())
        if word_count < 50:
            base_score -= 0.2
        elif word_count > 200:
            base_score += 0.1
        
        # Check for academic keywords
        academic_keywords = ["analysis", "research", "study", "findings", "methodology", "results", "conclusion"]
        keyword_count = sum(1 for keyword in academic_keywords if keyword.lower() in content.lower())
        base_score += min(keyword_count * 0.02, 0.1)
        
        return min(max(base_score, 0.0), 1.0)
    
    def extract_paper_summaries(self, papers_data: List[Dict]) -> str:
        """Extract paper summaries for context."""
        summaries = []
        for i, paper in enumerate(papers_data[:5], 1):
            title = paper.get('title', f'Paper {i}')
            summary = paper.get('summary', paper.get('abstract', 'No summary available'))
            summaries.append(f"{i}. {title}: {summary[:200]}...")
        return "\n\n".join(summaries)
    
    def extract_paper_findings(self, papers_data: List[Dict]) -> str:
        """Extract key findings from papers."""
        findings = []
        for i, paper in enumerate(papers_data[:5], 1):
            title = paper.get('title', f'Paper {i}')
            key_findings = paper.get('key_findings', paper.get('findings', []))
            if isinstance(key_findings, list):
                findings_text = "; ".join(key_findings[:3])
            else:
                findings_text = str(key_findings)[:200]
            findings.append(f"{i}. {title}: {findings_text}")
        return "\n\n".join(findings)
    
    def extract_paper_implications(self, papers_data: List[Dict]) -> str:
        """Extract implications from papers."""
        implications = []
        for i, paper in enumerate(papers_data[:5], 1):
            title = paper.get('title', f'Paper {i}')
            implications_text = paper.get('implications', paper.get('conclusions', 'No implications specified'))
            implications.append(f"{i}. {title}: {implications_text[:200]}...")
        return "\n\n".join(implications)
    
    def load_paper_data(self, analysis_dir: str) -> List[Dict]:
        """Load paper analysis data from directory."""
        papers_data = []
        analysis_path = Path(analysis_dir)
        
        if not analysis_path.exists():
            self.logger.warning(f"Analysis directory not found: {analysis_dir}")
            return papers_data
        
        # Look for analysis JSON files
        for file_path in analysis_path.glob("*_analysis.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    analysis_data = json.load(f)
                
                # Extract relevant information
                paper_data = {
                    'title': analysis_data.get('title', file_path.stem),
                    'summary': analysis_data.get('summary', ''),
                    'key_findings': analysis_data.get('key_findings', []),
                    'implications': analysis_data.get('implications', ''),
                    'methodology': analysis_data.get('methodology', ''),
                    'file_path': str(file_path)
                }
                
                papers_data.append(paper_data)
                
            except Exception as e:
                self.logger.warning(f"Error loading {file_path}: {e}")
        
        self.logger.info(f"Loaded {len(papers_data)} papers from {analysis_dir}")
        return papers_data
    
    def generate_complete_draft(self, papers_data: List[Dict], 
                              sections: Optional[List[str]] = None) -> Dict[str, DraftSection]:
        """Generate complete draft with all sections."""
        if sections is None:
            sections = ['abstract', 'introduction', 'methods', 'results', 'discussion']
        
        drafts = {}
        for section in sections:
            drafts[section] = self.generate_section_draft(section, papers_data)
        
        return drafts
    
    def save_drafts(self, drafts: Dict[str, DraftSection], output_file: str):
        """Save drafts to JSON file."""
        drafts_data = {}
        for section, draft in drafts.items():
            drafts_data[section] = {
                'title': draft.title,
                'content': draft.content,
                'word_count': draft.word_count,
                'confidence_score': draft.confidence_score,
                'ai_provider': draft.ai_provider,
                'generation_time': draft.generation_time,
                'sources_used': draft.sources_used
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(drafts_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Drafts saved to {output_file}")
    
    def generate_formatted_paper(self, drafts: Dict[str, DraftSection], output_file: str):
        """Generate formatted paper document."""
        content = f"""Generated Research Paper
========================

Generated using AI Research Agent
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Provider: {list(set(draft.ai_provider for draft in drafts.values()))}

"""
        
        # Add sections in order
        section_order = ['abstract', 'introduction', 'methods', 'results', 'discussion']
        
        for section_type in section_order:
            if section_type in drafts:
                draft = drafts[section_type]
                content += f"\n{draft.title}\n{'-' * len(draft.title)}\n\n"
                content += draft.content
                content += f"\n\n*Word count: {draft.word_count} | Confidence: {draft.confidence_score:.2f} | AI: {draft.ai_provider}*\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Formatted paper saved to {output_file}")


class MockDraftGenerator:
    """Mock draft generator for fallback scenarios."""
    
    def generate_mock_content(self, section_type: str, paper_count: int) -> str:
        """Generate mock content for a section."""
        
        mock_content = {
            'abstract': f"""This systematic review analyzed {paper_count} research papers to examine current trends and findings in the field. Our analysis reveals significant methodological diversity across studies, with varying approaches to data collection and analysis. Key findings indicate emerging patterns in research methodology and growing consensus on best practices. The papers collectively demonstrate substantial progress in the field, while also highlighting important gaps that require further investigation. This review provides a comprehensive foundation for future research and identifies critical areas for continued study.""",
            
            'introduction': f"""The field has experienced rapid growth in recent years, with increasing attention from researchers and practitioners alike. This growth has led to a proliferation of research approaches and methodologies, creating both opportunities and challenges. While significant progress has been made, important gaps remain in our understanding of key phenomena. The current literature lacks comprehensive synthesis of findings across different methodological approaches. This paper addresses this gap by providing a systematic review of {paper_count} studies, offering insights into current trends and future directions. The significance of this research lies in its potential to consolidate knowledge and guide future investigations.""",
            
            'methods': f"""This study employed a systematic review methodology to analyze {paper_count} research papers. Papers were selected based on predefined inclusion criteria focusing on relevance and methodological rigor. Data extraction was performed independently by two reviewers using a standardized form. Quality assessment was conducted using established guidelines to ensure the reliability of included studies. Statistical analysis included descriptive statistics and synthesis of findings across studies. The review protocol was registered and followed PRISMA guidelines for transparency and reproducibility. This approach ensures comprehensive and unbiased analysis of the current state of research.""",
            
            'results': f"""The analysis of {paper_count} papers revealed several important patterns and findings. A total of X studies met the inclusion criteria, representing diverse methodological approaches. Key findings include consistent trends in research methodology and emerging consensus on best practices. Statistical analysis showed significant correlations between research approach and outcome quality. The majority of studies reported positive results, with effect sizes ranging from small to large. Comparative analysis revealed important differences between subfields and research approaches. These results provide valuable insights into the current state of research and highlight areas requiring further investigation.""",
            
            'discussion': f"""The findings of this systematic review have important implications for both theory and practice. The observed trends in research methodology suggest a maturation of the field, with increasing methodological rigor and standardization. The diversity of approaches identified reflects the complexity of the research domain and the need for multiple perspectives. Limitations of this review include potential publication bias and the rapid evolution of the field. Future research should focus on longitudinal studies and cross-cultural comparisons. The findings provide a foundation for evidence-based practice and suggest several promising directions for future investigation. This review contributes to the ongoing development of the field and identifies critical gaps in current knowledge."""
        }
        
        return mock_content.get(section_type, f"Mock content for {section_type} section based on {paper_count} papers.")


# Convenience functions for backward compatibility
def generate_drafts_from_analysis(analysis_dir: str, output_dir: str = None, 
                                 preferred_provider: str = "gemini"):
    """Generate drafts from analysis directory using enhanced generator."""
    generator = EnhancedGPTDraftGenerator(preferred_provider=preferred_provider)
    
    # Load papers data
    papers_data = generator.load_paper_data(analysis_dir)
    
    if not papers_data:
        raise ValueError("No analysis data found")
    
    # Generate drafts
    drafts = generator.generate_complete_draft(papers_data)
    
    # Save drafts
    if output_dir is None:
        output_dir = Path(analysis_dir).parent / "drafts"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON and formatted versions
    generator.save_drafts(drafts, output_dir / "enhanced_drafts.json")
    generator.generate_formatted_paper(drafts, output_dir / "enhanced_paper.txt")
    
    return drafts


if __name__ == "__main__":
    # Test the enhanced generator
    generator = EnhancedGPTDraftGenerator(preferred_provider="gemini")
    
    print("🤖 Enhanced AI Draft Generator Test")
    print("=" * 40)
    print(f"Available providers: {generator.available_providers}")
    print(f"Best provider: {generator.get_best_provider()}")
    
    # Test with sample data
    sample_papers = [
        {"title": "Sample Paper 1", "summary": "This is a sample paper about AI research.", "key_findings": ["AI is advancing rapidly"], "implications": "Future research needed"},
        {"title": "Sample Paper 2", "summary": "Another paper on machine learning.", "key_findings": ["ML applications growing"], "implications": "Practical applications emerging"}
    ]
    
    # Generate a test section
    draft = generator.generate_section_draft("abstract", sample_papers)
    print(f"\n📝 Generated Abstract:")
    print(f"Provider: {draft.ai_provider}")
    print(f"Words: {draft.word_count}")
    print(f"Confidence: {draft.confidence_score:.2f}")
    print(f"Content preview: {draft.content[:200]}...")
