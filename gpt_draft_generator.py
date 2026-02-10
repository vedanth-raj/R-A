"""
GPT-based automated drafting module for research paper sections.
Generates structured drafts for Abstract, Methods, and Results sections.
Now uses Google Gemini API exclusively.
"""

import json
import logging
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

# Import Gemini
try:
    import google.genai as genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


@dataclass
class DraftSection:
    """Represents a generated draft section."""
    section_type: str
    title: str
    content: str
    word_count: int
    confidence_score: float
    sources_used: List[str]
    generated_at: str
    
    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now().isoformat()


class GPTDraftGenerator:
    """
    Generates automated drafts for research paper sections using Gemini AI.
    Integrates findings from multiple papers to create coherent sections.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the draft generator with Gemini.
        
        Args:
            api_key (Optional[str]): Gemini API key
            model (str): Gemini model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.client = None
        
        # Get API key from parameter or environment
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key and GEMINI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=api_key)
                self.logger.info("Gemini client initialized successfully")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Gemini: {e}. Using mock generation.")
        elif api_key and not GEMINI_AVAILABLE:
            self.logger.warning("Gemini library not installed. Using mock generation.")
        else:
            self.logger.warning("No Gemini API key provided. Using mock generation.")
        
        # Section-specific prompts and templates
        self.section_templates = {
            'abstract': {
                'prompt_template': """
                Based on the following research papers, generate a comprehensive abstract for a literature review paper.
                Focus on synthesizing the key findings, methodologies, and implications.
                
                Papers analyzed:
                {paper_summaries}
                
                Generate an abstract that:
                1. Provides context and motivation
                2. Summarizes key findings from the papers
                3. Highlights methodological approaches
                4. Identifies gaps and future directions
                5. Is 200-300 words
                
                Abstract:
                """,
                'max_tokens': 400,
                'temperature': 0.7
            },
            'methods': {
                'prompt_template': """
                Based on the following research papers, generate a comprehensive Methods section for a systematic review or meta-analysis.
                
                Papers analyzed:
                {paper_summaries}
                
                Generate a Methods section that:
                1. Describes the search strategy and inclusion criteria
                2. Explains the data extraction and analysis approach
                3. Details the quality assessment methodology
                4. Describes any statistical methods used
                5. Is 400-600 words
                
                Methods:
                """,
                'max_tokens': 600,
                'temperature': 0.3
            },
            'results': {
                'prompt_template': """
                Based on the following research papers and their analyses, generate a comprehensive Results section.
                
                Papers and their key findings:
                {paper_findings}
                
                Generate a Results section that:
                1. Summarizes the main findings across papers
                2. Presents statistical information and trends
                3. Compares and contrasts different approaches
                4. Highlights significant patterns and relationships
                5. Is 500-700 words
                
                Results:
                """,
                'max_tokens': 700,
                'temperature': 0.4
            },
            'introduction': {
                'prompt_template': """
                Based on the following research papers, generate an introduction that sets up a comprehensive literature review.
                
                Papers analyzed:
                {paper_summaries}
                
                Generate an Introduction that:
                1. Provides background and context
                2. Identifies the research problem/gap
                3. States the purpose and objectives
                4. Outlines the paper structure
                5. Is 400-600 words
                
                Introduction:
                """,
                'max_tokens': 600,
                'temperature': 0.6
            },
            'discussion': {
                'prompt_template': """
                Based on the following research papers and their findings, generate a Discussion section.
                
                Papers and their implications:
                {paper_implications}
                
                Generate a Discussion that:
                1. Interprets the findings
                2. Compares with existing literature
                3. Discusses limitations and implications
                4. Suggests future research directions
                5. Is 500-700 words
                
                Discussion:
                """,
                'max_tokens': 700,
                'temperature': 0.5
            }
        }
    
    def load_paper_data(self, analysis_dir: str) -> Dict[str, Any]:
        """
        Load paper analysis data for drafting.
        
        Args:
            analysis_dir (str): Directory containing paper analysis files
            
        Returns:
            Dict[str, Any]: Consolidated paper data
        """
        try:
            analysis_path = Path(analysis_dir)
            papers_data = {}
            
            for analysis_file in analysis_path.glob('*_analysis.json'):
                if analysis_file.name == 'summary_report.json':
                    continue
                    
                try:
                    with open(analysis_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        papers_data[data['paper_name']] = data
                except Exception as e:
                    self.logger.warning(f"Error loading {analysis_file}: {e}")
            
            return papers_data
            
        except Exception as e:
            self.logger.error(f"Error loading paper data: {e}")
            return {}
    
    def extract_paper_summaries(self, papers_data: Dict[str, Any]) -> List[str]:
        """
        Extract concise summaries from paper data.
        
        Args:
            papers_data (Dict[str, Any]): Paper analysis data
            
        Returns:
            List[str]: Paper summaries
        """
        summaries = []
        
        for paper_name, data in papers_data.items():
            summary = f"• {paper_name}: "
            
            # Add key insights if available
            if data.get('key_insights'):
                summary += "; ".join(data['key_insights'][:2])
            
            # Add section information
            if data.get('sections'):
                section_types = [s.get('type', 'unknown') for s in data['sections']]
                unique_types = list(set(section_types))
                summary += f" (Sections: {', '.join(unique_types)})"
            
            # Add word count
            if data.get('total_words'):
                summary += f" - {data['total_words']} words"
            
            summaries.append(summary)
        
        return summaries
    
    def extract_paper_findings(self, papers_data: Dict[str, Any]) -> List[str]:
        """
        Extract key findings from paper data.
        
        Args:
            papers_data (Dict[str, Any]): Paper analysis data
            
        Returns:
            List[str]: Paper findings
        """
        findings = []
        
        for paper_name, data in papers_data.items():
            paper_findings = f"• {paper_name}:\n"
            
            # Extract insights from abstract sections
            for section in data.get('sections', []):
                if section.get('type') == 'abstract':
                    content = section.get('content', '')
                    # Extract key sentences
                    sentences = content.split('. ')
                    important_sentences = [
                        s for s in sentences 
                        if any(keyword in s.lower() for keyword in 
                              ['found', 'showed', 'demonstrated', 'revealed', 'indicated', 'significant'])
                    ]
                    if important_sentences:
                        paper_findings += "  Key findings: " + "; ".join(important_sentences[:3])
                    break
            
            findings.append(paper_findings)
        
        return findings
    
    def extract_paper_implications(self, papers_data: Dict[str, Any]) -> List[str]:
        """
        Extract implications from paper data.
        
        Args:
            papers_data (Dict[str, Any]): Paper analysis data
            
        Returns:
            List[str]: Paper implications
        """
        implications = []
        
        for paper_name, data in papers_data.items():
            paper_imp = f"• {paper_name}:\n"
            
            # Look for conclusion or discussion sections
            for section in data.get('sections', []):
                if section.get('type') in ['conclusion', 'discussion']:
                    content = section.get('content', '')
                    # Extract implication sentences
                    sentences = content.split('. ')
                    imp_sentences = [
                        s for s in sentences 
                        if any(keyword in s.lower() for keyword in 
                              ['implication', 'suggest', 'recommend', 'future', 'limitation', 'potential'])
                    ]
                    if imp_sentences:
                        paper_imp += "  Implications: " + "; ".join(imp_sentences[:2])
                    break
            
            implications.append(paper_imp)
        
        return implications
    
    def generate_mock_content(self, section_type: str, papers_data: Dict[str, Any]) -> str:
        """
        Generate mock content when OpenAI API is not available.
        
        Args:
            section_type (str): Type of section to generate
            papers_data (Dict[str, Any]): Paper analysis data
            
        Returns:
            str: Generated content
        """
        num_papers = len(papers_data)
        
        if section_type == 'abstract':
            return f"""This systematic review analyzed {num_papers} research papers to examine current trends and findings in the field. 
Our analysis reveals significant methodological diversity across studies, with varying approaches to data collection and analysis. 
Key findings indicate emerging patterns in research methodology and growing consensus on best practices. 
The papers collectively demonstrate substantial progress in the field, while also highlighting important gaps that require further investigation. 
This review provides a comprehensive foundation for future research and identifies critical areas for continued study."""
        
        elif section_type == 'methods':
            return f"""This study employed a systematic review methodology to analyze {num_papers} research papers. 
Papers were selected based on predefined inclusion criteria focusing on relevance and methodological rigor. 
Data extraction was performed independently by two reviewers using a standardized form. 
Quality assessment was conducted using established guidelines to ensure the reliability of included studies. 
Statistical analysis included descriptive statistics and synthesis of findings across studies. 
The review protocol was registered and followed PRISMA guidelines for transparency and reproducibility."""
        
        elif section_type == 'results':
            return f"""The analysis of {num_papers} papers revealed several important patterns. 
Methodological approaches varied significantly, with quantitative methods dominating the field (60% of studies). 
Sample sizes ranged from small pilot studies to large-scale implementations, with a median of 150 participants. 
Key findings were consistent across 75% of studies, suggesting strong reliability of results. 
Statistical significance was achieved in 80% of quantitative studies, with effect sizes ranging from small to large. 
The results demonstrate both convergence and divergence in research approaches and outcomes."""
        
        elif section_type == 'introduction':
            return f"""The field has experienced rapid growth in recent years, with increasing attention from researchers and practitioners alike. 
This growth has led to a proliferation of research approaches and methodologies, creating both opportunities and challenges. 
While significant progress has been made, important gaps remain in our understanding of key phenomena. 
The current literature lacks comprehensive synthesis of findings across different methodological approaches. 
This paper addresses this gap by providing a systematic review of {num_papers} studies, offering insights into current trends and future directions."""
        
        elif section_type == 'discussion':
            return f"""The findings from this review of {num_papers} papers reveal important insights for the field. 
The consistency of findings across diverse methodological approaches strengthens confidence in the results. 
However, the variation in study quality and approaches suggests the need for standardization in future research. 
Limitations include the heterogeneity of studies and potential publication bias in the available literature. 
Future research should focus on longitudinal studies and standardized methodologies to build upon these findings."""
        
        else:
            return f"Generated content for {section_type} based on {num_papers} analyzed papers."
    
    def generate_section_draft(self, section_type: str, papers_data: Dict[str, Any]) -> DraftSection:
        """
        Generate a draft for a specific section.
        
        Args:
            section_type (str): Type of section to generate
            papers_data (Dict[str, Any]): Paper analysis data
            
        Returns:
            DraftSection: Generated draft section
        """
        try:
            if section_type not in self.section_templates:
                raise ValueError(f"Unknown section type: {section_type}")
            
            template = self.section_templates[section_type]
            
            # Prepare input data
            if section_type in ['abstract', 'introduction']:
                input_data = self.extract_paper_summaries(papers_data)
                prompt_input = "\n".join(input_data)
            elif section_type == 'methods':
                input_data = self.extract_paper_summaries(papers_data)
                prompt_input = "\n".join(input_data)
            elif section_type == 'results':
                input_data = self.extract_paper_findings(papers_data)
                prompt_input = "\n".join(input_data)
            elif section_type == 'discussion':
                input_data = self.extract_paper_implications(papers_data)
                prompt_input = "\n".join(input_data)
            else:
                input_data = self.extract_paper_summaries(papers_data)
                prompt_input = "\n".join(input_data)
            
            # Generate content
            if self.client:
                content = self._generate_with_gpt(section_type, prompt_input, template)
            else:
                content = self.generate_mock_content(section_type, papers_data)
            
            # Create draft section
            draft = DraftSection(
                section_type=section_type,
                title=section_type.title(),
                content=content,
                word_count=len(content.split()),
                confidence_score=0.8 if self.client else 0.6,
                sources_used=list(papers_data.keys()),
                generated_at=datetime.now().isoformat()
            )
            
            return draft
            
        except Exception as e:
            self.logger.error(f"Error generating {section_type} draft: {e}")
            raise
    
    def _generate_with_gpt(self, section_type: str, prompt_input: str, template: Dict[str, Any]) -> str:
        """
        Generate content using Gemini model.
        
        Args:
            section_type (str): Section type
            prompt_input (str): Input data for prompt
            template (Dict[str, Any]): Template configuration
            
        Returns:
            str: Generated content
        """
        try:
            prompt = template['prompt_template'].format(
                paper_summaries=prompt_input,
                paper_findings=prompt_input,
                paper_implications=prompt_input
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=template['temperature'],
                    max_output_tokens=template['max_tokens']
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating content with Gemini: {e}")
            raise
    
    def generate_complete_draft(self, papers_data: Dict[str, Any], 
                             sections: List[str] = None) -> Dict[str, DraftSection]:
        """
        Generate a complete draft with multiple sections.
        
        Args:
            papers_data (Dict[str, Any]): Paper analysis data
            sections (List[str]): Sections to generate (default: all)
            
        Returns:
            Dict[str, DraftSection]: Generated sections
        """
        if sections is None:
            sections = ['abstract', 'introduction', 'methods', 'results', 'discussion']
        
        drafts = {}
        
        for section_type in sections:
            try:
                self.logger.info(f"Generating {section_type} section...")
                draft = self.generate_section_draft(section_type, papers_data)
                drafts[section_type] = draft
                self.logger.info(f"Generated {section_type}: {draft.word_count} words")
            except Exception as e:
                self.logger.error(f"Failed to generate {section_type}: {e}")
                continue
        
        return drafts
    
    def save_drafts(self, drafts: Dict[str, DraftSection], output_file: str):
        """
        Save generated drafts to file.
        
        Args:
            drafts (Dict[str, DraftSection]): Generated sections
            output_file (str): Output file path
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to serializable format
            drafts_data = {}
            for section_type, draft in drafts.items():
                drafts_data[section_type] = {
                    'section_type': draft.section_type,
                    'title': draft.title,
                    'content': draft.content,
                    'word_count': draft.word_count,
                    'confidence_score': draft.confidence_score,
                    'sources_used': draft.sources_used,
                    'generated_at': draft.generated_at
                }
            
            # Add metadata
            drafts_data['metadata'] = {
                'total_sections': len(drafts),
                'total_words': sum(d.word_count for d in drafts.values()),
                'average_confidence': sum(d.confidence_score for d in drafts.values()) / len(drafts) if drafts else 0,
                'generated_at': datetime.now().isoformat(),
                'model_used': self.model
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(drafts_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Drafts saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving drafts: {e}")
            raise
    
    def generate_formatted_paper(self, drafts: Dict[str, DraftSection], 
                               output_file: str, title: str = "Generated Research Paper"):
        """
        Generate a formatted research paper.
        
        Args:
            drafts (Dict[str, DraftSection]): Generated sections
            output_file (str): Output file path
            title (str): Paper title
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate formatted content
            content = f"{title}\n{'=' * len(title)}\n\n"
            
            # Add sections in logical order
            section_order = ['abstract', 'introduction', 'methods', 'results', 'discussion']
            
            for section_type in section_order:
                if section_type in drafts:
                    draft = drafts[section_type]
                    content += f"\n{draft.title}\n{'-' * len(draft.title)}\n\n"
                    content += draft.content
                    content += "\n\n"
            
            # Add references placeholder
            content += "References\n----------\n\n"
            content += "[References will be formatted here using APA style]\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Formatted paper saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error generating formatted paper: {e}")
            raise


# Convenience functions
def generate_drafts_from_analysis(analysis_dir: str, output_dir: str, 
                                 api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to generate drafts from analysis directory.
    
    Args:
        analysis_dir (str): Directory containing paper analysis files
        output_dir (str): Output directory for drafts
        api_key (Optional[str]): OpenAI API key
        
    Returns:
        Dict[str, Any]: Generation results
    """
    generator = GPTDraftGenerator(api_key=api_key)
    
    # Load paper data
    papers_data = generator.load_paper_data(analysis_dir)
    
    if not papers_data:
        raise ValueError("No paper data found for drafting")
    
    # Generate drafts
    drafts = generator.generate_complete_draft(papers_data)
    
    # Save drafts
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    drafts_file = output_path / "generated_drafts.json"
    generator.save_drafts(drafts, str(drafts_file))
    
    # Generate formatted paper
    paper_file = output_path / "generated_paper.txt"
    generator.generate_formatted_paper(drafts, str(paper_file))
    
    return {
        'drafts_generated': len(drafts),
        'papers_analyzed': len(papers_data),
        'output_files': [str(drafts_file), str(paper_file)],
        'total_words': sum(d.word_count for d in drafts.values())
    }
