"""
Advanced Text Processing Module for Research Paper Analysis

This module provides advanced text processing capabilities including:
- Text quality assessment
- Language detection
- Citation extraction
- Keyword extraction
- Text summarization
- Plagiarism detection basics
- Readability analysis
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class TextQualityMetrics:
    """Metrics for text quality assessment."""
    readability_score: float
    word_diversity: float
    sentence_complexity: float
    technical_term_density: float
    overall_quality: float

@dataclass
class CitationInfo:
    """Information about extracted citations."""
    citation_text: str
    citation_type: str  # 'author_year', 'numbered', 'footnote'
    confidence: float
    position: int

class AdvancedTextProcessor:
    """Advanced text processing capabilities for research papers."""
    
    def __init__(self):
        """Initialize the advanced text processor."""
        self.logger = logging.getLogger(__name__)
        
        # Technical terms for different fields
        self.technical_terms = {
            'machine_learning': [
                'neural network', 'deep learning', 'algorithm', 'training',
                'model', 'dataset', 'accuracy', 'precision', 'recall', 'f1-score'
            ],
            'physics': [
                'quantum', 'particle', 'energy', 'momentum', 'wave function',
                'equation', 'theory', 'experiment', 'measurement', 'observation'
            ],
            'biology': [
                'cell', 'protein', 'gene', 'dna', 'rna', 'enzyme',
                'metabolism', 'organism', 'evolution', 'mutation'
            ],
            'computer_science': [
                'algorithm', 'complexity', 'data structure', 'programming',
                'software', 'hardware', 'network', 'database', 'security'
            ]
        }
        
        # Citation patterns
        self.citation_patterns = [
            # Author-year format: (Smith, 2020)
            r'\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s+\d{4}\)',
            # Numbered format: [1], [2-5]
            r'\[\d+(?:-\d+)?\]',
            # Author-year with page: (Smith, 2020, p. 123)
            r'\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s+\d{4},\s+p\.\s+\d+\)',
            # Footnote style: ¹, ²
            r'[¹²³⁴⁵⁶⁷⁸⁹₀]+'
        ]
        
        # Common academic phrases
        self.academic_phrases = [
            'in this paper', 'we propose', 'our method', 'experimental results',
            'conclusion', 'future work', 'related work', 'methodology',
            'abstract', 'introduction', 'we show', 'we demonstrate', 'we present'
        ]
    
    def assess_text_quality(self, text: str) -> TextQualityMetrics:
        """
        Assess the quality of extracted text.
        
        Args:
            text (str): Text to assess
            
        Returns:
            TextQualityMetrics: Quality assessment metrics
        """
        if not text or len(text.strip()) < 100:
            return TextQualityMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
        
        # Basic text statistics
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if not words or not sentences:
            return TextQualityMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
        
        # Readability score (simplified Flesch-Kincaid)
        avg_sentence_length = len(words) / len(sentences)
        syllable_count = sum(self._count_syllables(word) for word in words)
        avg_syllables = syllable_count / len(words)
        
        readability_score = max(0, 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables))
        readability_score = min(100, readability_score) / 100  # Normalize to 0-1
        
        # Word diversity (unique words / total words)
        unique_words = set(word.lower().strip('.,!?;:') for word in words)
        word_diversity = len(unique_words) / len(words)
        
        # Sentence complexity (average sentence length variation)
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        length_variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
        sentence_complexity = min(1.0, length_variance / 100)  # Normalize
        
        # Technical term density
        technical_count = 0
        for field, terms in self.technical_terms.items():
            for term in terms:
                technical_count += len(re.findall(rf'\b{re.escape(term)}\b', text, re.IGNORECASE))
        
        technical_term_density = technical_count / len(words)
        
        # Overall quality score
        overall_quality = (
            readability_score * 0.3 +
            word_diversity * 0.25 +
            sentence_complexity * 0.2 +
            min(1.0, technical_term_density * 10) * 0.25
        )
        
        return TextQualityMetrics(
            readability_score=readability_score,
            word_diversity=word_diversity,
            sentence_complexity=sentence_complexity,
            technical_term_density=technical_term_density,
            overall_quality=overall_quality
        )
    
    def extract_citations(self, text: str) -> List[CitationInfo]:
        """
        Extract citations from the text.
        
        Args:
            text (str): Text to extract citations from
            
        Returns:
            List[CitationInfo]: List of extracted citations
        """
        citations = []
        
        for i, pattern in enumerate(self.citation_patterns):
            matches = re.finditer(pattern, text)
            for match in matches:
                citation_text = match.group()
                position = match.start()
                
                # Determine citation type
                if i == 0 or i == 2:  # Author-year formats
                    citation_type = 'author_year'
                elif i == 1:  # Numbered format
                    citation_type = 'numbered'
                else:  # Footnote
                    citation_type = 'footnote'
                
                # Calculate confidence based on pattern specificity
                confidence = 0.9 if i < 2 else 0.7
                
                citations.append(CitationInfo(
                    citation_text=citation_text,
                    citation_type=citation_type,
                    confidence=confidence,
                    position=position
                ))
        
        return citations
    
    def extract_keywords(self, text: str, max_keywords: int = 20) -> List[Tuple[str, float]]:
        """
        Extract keywords from text using TF-IDF-like scoring.
        
        Args:
            text (str): Text to extract keywords from
            max_keywords (int): Maximum number of keywords to return
            
        Returns:
            List[Tuple[str, float]]: List of (keyword, score) tuples
        """
        # Clean and tokenize text
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Calculate word frequencies
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)
        
        # Calculate TF-IDF-like scores
        keyword_scores = []
        for word, freq in word_freq.most_common(max_keywords * 2):  # Get more to filter
            tf = freq / total_words
            
            # Boost technical terms
            is_technical = any(
                word in term.lower() or term.lower() in word
                for terms in self.technical_terms.values()
                for term in terms
            )
            
            # Boost academic phrases
            is_academic = any(phrase in word for phrase in self.academic_phrases)
            
            # Calculate final score
            score = tf * (1.5 if is_technical else 1.0) * (1.2 if is_academic else 1.0)
            
            # Boost multi-word terms
            if len(word) > 6:
                score *= 1.1
            
            keyword_scores.append((word, score))
        
        # Sort by score and return top keywords
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        return keyword_scores[:max_keywords]
    
    def detect_language(self, text: str) -> Dict[str, float]:
        """
        Detect the language of the text (basic implementation).
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, float]: Language probabilities
        """
        # Common word patterns for different languages
        language_patterns = {
            'english': {
                'common_words': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with'],
                'patterns': [r'\bthe\b', r'\band\b', r'\bof\b']
            },
            'academic_english': {
                'common_words': ['however', 'therefore', 'furthermore', 'moreover', 'consequently'],
                'patterns': [r'\bhowever\b', r'\btherefore\b', r'\bfurthermore\b']
            }
        }
        
        scores = {}
        text_lower = text.lower()
        
        for language, patterns in language_patterns.items():
            score = 0
            total_patterns = len(patterns['patterns'])
            
            for pattern in patterns['patterns']:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            # Normalize score
            scores[language] = score / total_patterns if total_patterns > 0 else 0
        
        # Normalize to probabilities
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {lang: score / total_score for lang, score in scores.items()}
        else:
            scores['unknown'] = 1.0
        
        return scores
    
    def generate_summary(self, text: str, max_sentences: int = 5) -> str:
        """
        Generate a simple extractive summary of the text.
        
        Args:
            text (str): Text to summarize
            max_sentences (int): Maximum number of sentences in summary
            
        Returns:
            str: Generated summary
        """
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + '.'
        
        # Score sentences based on various features
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            
            # Length preference (not too short, not too long)
            words = sentence.split()
            if 10 <= len(words) <= 30:
                score += 1
            elif len(words) > 30:
                score += 0.5
            
            # Keyword presence
            keywords = self.extract_keywords(sentence, max_keywords=5)
            score += len(keywords) * 0.5
            
            # Citation presence (often important sentences)
            citations = self.extract_citations(sentence)
            score += len(citations) * 0.3
            
            # Position preference (beginning and end)
            if i < len(sentences) * 0.2:  # First 20%
                score += 0.5
            elif i > len(sentences) * 0.8:  # Last 20%
                score += 0.5
            
            sentence_scores.append((i, score, sentence))
        
        # Sort by score and select top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        selected_indices = sorted([score[0] for score in sentence_scores[:max_sentences]])
        
        # Generate summary maintaining original order
        summary_sentences = [sentences[i] for i in selected_indices]
        return '. '.join(summary_sentences) + '.'
    
    def analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the structure of the text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Structure analysis results
        """
        lines = text.split('\n')
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = text.split()
        
        # Line analysis
        empty_lines = sum(1 for line in lines if not line.strip())
        non_empty_lines = len(lines) - empty_lines
        
        # Sentence analysis
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # Paragraph analysis
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        return {
            'total_lines': len(lines),
            'empty_lines': empty_lines,
            'non_empty_lines': non_empty_lines,
            'total_sentences': len(sentences),
            'total_words': len(words),
            'total_paragraphs': len(paragraphs),
            'avg_sentence_length': avg_sentence_length,
            'avg_paragraph_length': avg_paragraph_length,
            'sentence_length_variance': self._calculate_variance(sentence_lengths),
            'paragraph_length_variance': self._calculate_variance(paragraph_lengths)
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified implementation)."""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_char_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_was_vowel:
                syllable_count += 1
            prev_char_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def process_text_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Comprehensive analysis results
        """
        return {
            'quality_metrics': self.assess_text_quality(text),
            'citations': [vars(citation) for citation in self.extract_citations(text)],
            'keywords': self.extract_keywords(text),
            'language_detection': self.detect_language(text),
            'summary': self.generate_summary(text),
            'structure_analysis': self.analyze_text_structure(text)
        }


# Convenience functions
def analyze_text_quality(text: str) -> TextQualityMetrics:
    """Convenience function to analyze text quality."""
    processor = AdvancedTextProcessor()
    return processor.assess_text_quality(text)


def extract_paper_citations(text: str) -> List[CitationInfo]:
    """Convenience function to extract citations."""
    processor = AdvancedTextProcessor()
    return processor.extract_citations(text)


def generate_paper_summary(text: str, max_sentences: int = 5) -> str:
    """Convenience function to generate paper summary."""
    processor = AdvancedTextProcessor()
    return processor.generate_summary(text, max_sentences)


def comprehensive_text_analysis(text: str) -> Dict[str, Any]:
    """Convenience function for comprehensive text analysis."""
    processor = AdvancedTextProcessor()
    return processor.process_text_comprehensive(text)
