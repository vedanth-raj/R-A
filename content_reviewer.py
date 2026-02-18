"""
Content Review and Refinement Module
Provides quality evaluation and revision suggestions for generated content
"""

import os
import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

try:
    import google.genai as genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

@dataclass
class QualityMetrics:
    """Quality metrics for generated content"""
    clarity_score: float
    coherence_score: float
    academic_tone_score: float
    completeness_score: float
    citation_quality_score: float
    overall_quality: float
    word_count: int
    sentence_count: int
    avg_sentence_length: float

@dataclass
class RevisionSuggestion:
    """Revision suggestion for content improvement"""
    category: str  # 'clarity', 'coherence', 'academic_tone', 'structure', 'citations'
    severity: str  # 'low', 'medium', 'high'
    description: str
    suggestion: str
    location: Optional[str] = None  # Section or paragraph reference

@dataclass
class ContentReview:
    """Complete content review results"""
    content: str
    section_type: str
    quality_metrics: QualityMetrics
    revision_suggestions: List[RevisionSuggestion]
    revised_content: Optional[str] = None
    review_timestamp: str = ""

class ContentReviewer:
    """Advanced content reviewer with AI-powered evaluation and revision"""
    
    def __init__(self, preferred_provider: str = "gemini"):
        """Initialize the content reviewer"""
        self.logger = logging.getLogger(__name__)
        self.preferred_provider = preferred_provider
        
        # Initialize AI providers
        self.gemini_client = None
        self.openai_client = None
        
        self._setup_providers()
        
        # Quality evaluation criteria
        self.quality_criteria = {
            'clarity': {
                'indicators': ['clear language', 'well-structured sentences', 'logical flow'],
                'weight': 0.25
            },
            'coherence': {
                'indicators': ['logical connections', 'consistent arguments', 'smooth transitions'],
                'weight': 0.25
            },
            'academic_tone': {
                'indicators': ['formal language', 'objective perspective', 'technical accuracy'],
                'weight': 0.20
            },
            'completeness': {
                'indicators': ['comprehensive coverage', 'adequate depth', 'relevant content'],
                'weight': 0.15
            },
            'citations': {
                'indicators': ['proper formatting', 'relevant sources', 'adequate references'],
                'weight': 0.15
            }
        }
    
    def _setup_providers(self):
        """Setup available AI providers"""
        
        # Setup Gemini
        if GEMINI_AVAILABLE:
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key and gemini_key != 'your_gemini_api_key_here':
                try:
                    self.gemini_client = genai.Client(api_key=gemini_key)
                    self.logger.info("Gemini client initialized for content review")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize Gemini: {e}")
        
        # Setup OpenAI
        if OPENAI_AVAILABLE:
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                try:
                    self.openai_client = openai.OpenAI(api_key=openai_key)
                    self.logger.info("OpenAI client initialized for content review")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize OpenAI: {e}")
    
    def get_best_provider(self) -> str:
        """Get the best available AI provider"""
        if self.preferred_provider == "gemini" and self.gemini_client:
            return "gemini"
        elif self.preferred_provider == "openai" and self.openai_client:
            return "openai"
        elif self.gemini_client:
            return "gemini"
        elif self.openai_client:
            return "openai"
        else:
            return "mock"
    
    def analyze_content_quality(self, content: str, section_type: str) -> QualityMetrics:
        """Analyze content quality using multiple metrics"""
        
        # Basic text statistics
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Quality scoring (simplified version)
        clarity_score = self._calculate_clarity_score(content, sentences)
        coherence_score = self._calculate_coherence_score(content)
        academic_tone_score = self._calculate_academic_tone_score(content)
        completeness_score = self._calculate_completeness_score(content, section_type)
        citation_quality_score = self._calculate_citation_quality_score(content)
        
        # Overall quality (weighted average)
        overall_quality = (
            clarity_score * 0.25 +
            coherence_score * 0.25 +
            academic_tone_score * 0.20 +
            completeness_score * 0.15 +
            citation_quality_score * 0.15
        )
        
        return QualityMetrics(
            clarity_score=clarity_score,
            coherence_score=coherence_score,
            academic_tone_score=academic_tone_score,
            completeness_score=completeness_score,
            citation_quality_score=citation_quality_score,
            overall_quality=overall_quality,
            word_count=word_count,
            sentence_count=sentence_count,
            avg_sentence_length=avg_sentence_length
        )
    
    def _calculate_clarity_score(self, content: str, sentences: List[str]) -> float:
        """Calculate clarity score based on sentence structure and readability"""
        score = 0.7  # Base score
        
        # Check sentence length variety
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if 15 <= avg_length <= 25:  # Ideal academic sentence length
            score += 0.2
        
        # Check for clear transitions
        transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently']
        transition_count = sum(1 for word in transition_words if word.lower() in content.lower())
        if transition_count > 0:
            score += min(0.1, transition_count * 0.02)
        
        return min(1.0, score)
    
    def _calculate_coherence_score(self, content: str) -> float:
        """Calculate coherence score based on logical flow"""
        score = 0.7  # Base score
        
        # Check for logical connectors
        connectors = ['because', 'since', 'therefore', 'thus', 'consequently', 'as a result']
        connector_count = sum(1 for connector in connectors if connector.lower() in content.lower())
        score += min(0.2, connector_count * 0.03)
        
        # Check paragraph structure
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 1:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_academic_tone_score(self, content: str) -> float:
        """Calculate academic tone score"""
        score = 0.7  # Base score
        
        # Academic vocabulary
        academic_words = ['analysis', 'methodology', 'significant', 'findings', 'research', 'study', 'results', 'conclusion']
        academic_count = sum(1 for word in academic_words if word.lower() in content.lower())
        score += min(0.2, academic_count * 0.02)
        
        # Avoid informal language
        informal_words = ['really', 'very', 'quite', 'pretty', 'sort of', 'kind of']
        informal_count = sum(1 for word in informal_words if word.lower() in content.lower())
        score -= min(0.2, informal_count * 0.05)
        
        return max(0.0, min(1.0, score))
    
    def _calculate_completeness_score(self, content: str, section_type: str) -> float:
        """Calculate completeness score based on section requirements"""
        score = 0.7  # Base score
        
        # Section-specific requirements
        section_requirements = {
            'abstract': {'min_words': 150, 'elements': ['background', 'methods', 'results', 'conclusion']},
            'introduction': {'min_words': 300, 'elements': ['background', 'problem', 'objectives', 'significance']},
            'methods': {'min_words': 400, 'elements': ['procedure', 'materials', 'analysis', 'validation']},
            'results': {'min_words': 400, 'elements': ['findings', 'data', 'statistics', 'observations']},
            'discussion': {'min_words': 500, 'elements': ['interpretation', 'implications', 'limitations', 'future']}
        }
        
        if section_type in section_requirements:
            req = section_requirements[section_type]
            word_count = len(content.split())
            
            # Word count requirement
            if word_count >= req['min_words']:
                score += 0.2
            else:
                score += (word_count / req['min_words']) * 0.2
            
            # Content elements
            elements_found = sum(1 for element in req['elements'] if element.lower() in content.lower())
            score += (elements_found / len(req['elements'])) * 0.1
        
        return min(1.0, score)
    
    def _calculate_citation_quality_score(self, content: str) -> float:
        """Calculate citation quality score"""
        score = 0.7  # Base score
        
        # Check for citation patterns
        citation_patterns = [r'\(\d{4}\)', r'\[.*?\]', r'\(.*?,.*?\d{4}.*?\)']
        has_citations = any(re.search(pattern, content) for pattern in citation_patterns)
        
        if has_citations:
            score += 0.3
        
        return min(1.0, score)
    
    def generate_revision_suggestions(self, content: str, section_type: str, quality_metrics: QualityMetrics) -> List[RevisionSuggestion]:
        """Generate AI-powered revision suggestions"""
        
        suggestions = []
        
        # Generate suggestions based on quality metrics
        if quality_metrics.clarity_score < 0.7:
            suggestions.append(RevisionSuggestion(
                category='clarity',
                severity='medium',
                description='Content clarity could be improved',
                suggestion='Consider breaking down complex sentences and adding more transition words to improve readability.'
            ))
        
        if quality_metrics.coherence_score < 0.7:
            suggestions.append(RevisionSuggestion(
                category='coherence',
                severity='medium',
                description='Logical flow could be enhanced',
                suggestion='Add more logical connectors between ideas and ensure smooth transitions between paragraphs.'
            ))
        
        if quality_metrics.academic_tone_score < 0.7:
            suggestions.append(RevisionSuggestion(
                category='academic_tone',
                severity='high',
                description='Academic tone needs improvement',
                suggestion='Replace informal language with more formal academic terminology and maintain objective perspective.'
            ))
        
        if quality_metrics.completeness_score < 0.7:
            suggestions.append(RevisionSuggestion(
                category='completeness',
                severity='high',
                description='Content may be incomplete',
                suggestion=f'Ensure the {section_type} section includes all required elements and meets minimum length requirements.'
            ))
        
        if quality_metrics.citation_quality_score < 0.7:
            suggestions.append(RevisionSuggestion(
                category='citations',
                severity='medium',
                description='Citation quality needs attention',
                suggestion='Add proper citations to support claims and ensure consistent citation formatting.'
            ))
        
        # AI-powered suggestions
        ai_suggestions = self._generate_ai_suggestions(content, section_type, quality_metrics)
        suggestions.extend(ai_suggestions)
        
        return suggestions
    
    def _generate_ai_suggestions(self, content: str, section_type: str, quality_metrics: QualityMetrics) -> List[RevisionSuggestion]:
        """Generate AI-powered revision suggestions"""
        provider = self.get_best_provider()
        
        if provider == "mock":
            return self._generate_mock_suggestions(content, section_type, quality_metrics)
        
        prompt = f"""
        Analyze this {section_type} section and provide specific revision suggestions:
        
        Content:
        {content}
        
        Quality Scores:
        - Clarity: {quality_metrics.clarity_score:.2f}
        - Coherence: {quality_metrics.coherence_score:.2f}
        - Academic Tone: {quality_metrics.academic_tone_score:.2f}
        - Completeness: {quality_metrics.completeness_score:.2f}
        - Citations: {quality_metrics.citation_quality_score:.2f}
        
        Provide 3-4 specific, actionable suggestions for improvement. Format each suggestion as:
        CATEGORY: [clarity/coherence/academic_tone/completeness/citations]
        SEVERITY: [low/medium/high]
        DESCRIPTION: [brief description of the issue]
        SUGGESTION: [specific actionable advice]
        """
        
        try:
            if provider == "gemini" and self.gemini_client:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",  # Latest stable model
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=500
                    )
                )
                return self._parse_ai_suggestions(response.text.strip())
            
            elif provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert academic writing reviewer."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                return self._parse_ai_suggestions(response.choices[0].message.content.strip())
        
        except Exception as e:
            self.logger.warning(f"AI suggestion generation failed: {e}")
        
        return []
    
    def _parse_ai_suggestions(self, ai_response: str) -> List[RevisionSuggestion]:
        """Parse AI response into structured suggestions"""
        suggestions = []
        
        # Simple parsing logic - can be enhanced
        lines = ai_response.split('\n')
        current_suggestion = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('CATEGORY:'):
                if current_suggestion:
                    suggestions.append(RevisionSuggestion(**current_suggestion))
                current_suggestion = {'category': line.split(':', 1)[1].strip()}
            elif line.startswith('SEVERITY:'):
                current_suggestion['severity'] = line.split(':', 1)[1].strip()
            elif line.startswith('DESCRIPTION:'):
                current_suggestion['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('SUGGESTION:'):
                current_suggestion['suggestion'] = line.split(':', 1)[1].strip()
        
        if current_suggestion and len(current_suggestion) == 4:
            suggestions.append(RevisionSuggestion(**current_suggestion))
        
        return suggestions
    
    def _generate_mock_suggestions(self, content: str, section_type: str, quality_metrics: QualityMetrics) -> List[RevisionSuggestion]:
        """Generate mock revision suggestions"""
        suggestions = []
        
        # Add one general suggestion
        suggestions.append(RevisionSuggestion(
            category='structure',
            severity='low',
            description='General improvement opportunity',
            suggestion='Consider reviewing the overall structure and flow of the section to ensure logical progression of ideas.'
        ))
        
        return suggestions
    
    def revise_content(self, content: str, section_type: str, suggestions: List[RevisionSuggestion]) -> str:
        """Revise content based on suggestions using AI"""
        provider = self.get_best_provider()
        
        if provider == "mock":
            return self._generate_mock_revision(content, suggestions)
        
        # Create revision prompt
        suggestions_text = "\n".join([
            f"- {s.category}: {s.suggestion}" for s in suggestions
        ])
        
        prompt = f"""
        Revise this {section_type} section based on the following suggestions:
        
        Original Content:
        {content}
        
        Revision Suggestions:
        {suggestions_text}
        
        Please provide an improved version that addresses these suggestions while maintaining the core content and academic tone. Focus on:
        1. Improving clarity and coherence
        2. Enhancing academic tone
        3. Ensuring completeness
        4. Maintaining proper citations
        
        Revised Content:
        """
        
        try:
            if provider == "gemini" and self.gemini_client:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",  # Latest stable model
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        max_output_tokens=1000
                    )
                )
                return response.text.strip()
            
            elif provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert academic writer and editor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.4
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            self.logger.warning(f"Content revision failed: {e}")
        
        return content  # Return original if revision fails
    
    def _generate_mock_revision(self, content: str, suggestions: List[RevisionSuggestion]) -> str:
        """Generate mock revision"""
        # Simple mock revision - just add a note
        return content + "\n\n[Note: This is a mock revision. In production, AI would revise the content based on suggestions.]"
    
    def review_content(self, content: str, section_type: str) -> ContentReview:
        """Perform complete content review"""
        
        # Analyze quality
        quality_metrics = self.analyze_content_quality(content, section_type)
        
        # Generate suggestions
        suggestions = self.generate_revision_suggestions(content, section_type, quality_metrics)
        
        # Create review
        review = ContentReview(
            content=content,
            section_type=section_type,
            quality_metrics=quality_metrics,
            revision_suggestions=suggestions,
            review_timestamp=datetime.now().isoformat()
        )
        
        return review
    
    def perform_revision_cycle(self, content: str, section_type: str, max_iterations: int = 3) -> Dict[str, Any]:
        """Perform complete revision cycle"""
        
        revision_history = []
        current_content = content
        
        for iteration in range(max_iterations):
            # Review current content
            review = self.review_content(current_content, section_type)
            
            # Check if quality is good enough
            if review.quality_metrics.overall_quality >= 0.8:
                review.revised_content = current_content
                revision_history.append(review)
                break
            
            # Generate revision
            revised_content = self.revise_content(current_content, section_type, review.revision_suggestions)
            review.revised_content = revised_content
            
            revision_history.append(review)
            current_content = revised_content
        
        return {
            'original_content': content,
            'final_content': current_content,
            'revision_history': revision_history,
            'total_iterations': len(revision_history),
            'final_quality': revision_history[-1].quality_metrics.overall_quality if revision_history else 0.0
        }

# Convenience functions
def review_section_content(content: str, section_type: str) -> ContentReview:
    """Review a single section of content"""
    reviewer = ContentReviewer()
    return reviewer.review_content(content, section_type)

def revise_section_content(content: str, section_type: str, suggestions: List[RevisionSuggestion]) -> str:
    """Revise content based on suggestions"""
    reviewer = ContentReviewer()
    return reviewer.revise_content(content, section_type, suggestions)

def perform_full_revision_cycle(content: str, section_type: str, max_iterations: int = 3) -> Dict[str, Any]:
    """Perform complete revision cycle for content"""
    reviewer = ContentReviewer()
    return reviewer.perform_revision_cycle(content, section_type, max_iterations)

if __name__ == "__main__":
    # Test the content reviewer
    reviewer = ContentReviewer()
    
    sample_content = """
    This study examines the impact of artificial intelligence on healthcare systems. 
    We analyzed data from multiple hospitals to understand how AI technologies are being implemented.
    The results show significant improvements in patient outcomes and operational efficiency.
    """
    
    print("🔍 Content Review Test")
    print("=" * 40)
    
    review = reviewer.review_content(sample_content, "abstract")
    
    print(f"Section: {review.section_type}")
    print(f"Overall Quality: {review.quality_metrics.overall_quality:.2f}")
    print(f"Clarity: {review.quality_metrics.clarity_score:.2f}")
    print(f"Coherence: {review.quality_metrics.coherence_score:.2f}")
    print(f"Academic Tone: {review.quality_metrics.academic_tone_score:.2f}")
    print(f"Completeness: {review.quality_metrics.completeness_score:.2f}")
    print(f"Citations: {review.quality_metrics.citation_quality_score:.2f}")
    
    print(f"\nRevision Suggestions: {len(review.revision_suggestions)}")
    for i, suggestion in enumerate(review.revision_suggestions, 1):
        print(f"{i}. {suggestion.category} ({suggestion.severity}): {suggestion.description}")
        print(f"   Suggestion: {suggestion.suggestion}")
    
    print("\n✅ Content review test completed!")
