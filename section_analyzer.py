"""
Section Analysis Tools - Utilities for analyzing extracted section data.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
import re


class SectionAnalyzer:
    """
    Analyzes section-wise extracted data from research papers.
    Provides tools for statistical analysis, content analysis, and comparison.
    """
    
    def __init__(self):
        """Initialize the section analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def load_section_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load section data from JSON file.
        
        Args:
            file_path (str): Path to section data JSON file
            
        Returns:
            Optional[Dict[str, Any]]: Section data or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading section data from {file_path}: {str(e)}")
            return None
    
    def analyze_section_distribution(self, section_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the distribution of sections in a paper.
        
        Args:
            section_data (Dict[str, Any]): Section data from extraction
            
        Returns:
            Dict[str, Any]: Distribution analysis
        """
        if not section_data or 'sections' not in section_data:
            return {}
        
        sections = section_data['sections']
        analysis = {
            'total_sections': len(sections),
            'section_types': {},
            'word_distribution': {},
            'page_distribution': {},
            'average_section_length': 0,
            'longest_section': None,
            'shortest_section': None
        }
        
        total_words = 0
        max_words = 0
        min_words = float('inf')
        
        for section in sections:
            section_type = section['type']
            word_count = section['word_count']
            
            # Count section types
            analysis['section_types'][section_type] = analysis['section_types'].get(section_type, 0) + 1
            
            # Word distribution by type
            if section_type not in analysis['word_distribution']:
                analysis['word_distribution'][section_type] = []
            analysis['word_distribution'][section_type].append(word_count)
            
            # Page distribution
            page_range = f"{section['start_page']}-{section['end_page']}"
            analysis['page_distribution'][page_range] = analysis['page_distribution'].get(page_range, 0) + 1
            
            # Track longest and shortest sections
            total_words += word_count
            if word_count > max_words:
                max_words = word_count
                analysis['longest_section'] = {
                    'title': section['title'],
                    'type': section_type,
                    'word_count': word_count
                }
            if word_count < min_words and word_count > 0:
                min_words = word_count
                analysis['shortest_section'] = {
                    'title': section['title'],
                    'type': section_type,
                    'word_count': word_count
                }
        
        # Calculate averages
        if sections:
            analysis['average_section_length'] = total_words // len(sections)
            
            # Calculate average word count by section type
            for section_type in analysis['word_distribution']:
                word_counts = analysis['word_distribution'][section_type]
                analysis['word_distribution'][section_type] = {
                    'count': len(word_counts),
                    'total': sum(word_counts),
                    'average': sum(word_counts) // len(word_counts),
                    'min': min(word_counts),
                    'max': max(word_counts)
                }
        
        return analysis
    
    def compare_papers_by_sections(self, section_files: List[str]) -> Dict[str, Any]:
        """
        Compare multiple papers based on their section structure.
        
        Args:
            section_files (List[str]): List of section data file paths
            
        Returns:
            Dict[str, Any]: Comparison analysis
        """
        comparison = {
            'papers': [],
            'common_sections': Counter(),
            'section_frequency': defaultdict(int),
            'average_sections_per_paper': 0,
            'section_type_distribution': defaultdict(list)
        }
        
        total_sections = 0
        
        for file_path in section_files:
            paper_data = self.load_section_data(file_path)
            if not paper_data:
                continue
            
            paper_info = {
                'file': Path(file_path).name,
                'title': paper_data.get('metadata', {}).get('title', 'Unknown'),
                'section_count': len(paper_data.get('sections', [])),
                'section_types': list(set(s['type'] for s in paper_data.get('sections', [])))
            }
            
            comparison['papers'].append(paper_info)
            total_sections += paper_info['section_count']
            
            # Track section types
            for section_type in paper_info['section_types']:
                comparison['section_frequency'][section_type] += 1
                comparison['common_sections'][section_type] += 1
        
        # Calculate averages
        if comparison['papers']:
            comparison['average_sections_per_paper'] = total_sections / len(comparison['papers'])
        
        # Convert Counter to regular dict for JSON serialization
        comparison['common_sections'] = dict(comparison['common_sections'])
        comparison['section_frequency'] = dict(comparison['section_frequency'])
        
        return comparison
    
    def extract_key_insights(self, section_data: Dict[str, Any], section_type: str = 'abstract') -> List[str]:
        """
        Extract key insights from specific sections.
        
        Args:
            section_data (Dict[str, Any]): Section data
            section_type (str): Type of section to analyze
            
        Returns:
            List[str]: Key insights/phrases
        """
        if not section_data or 'sections' not in section_data:
            return []
        
        insights = []
        
        for section in section_data['sections']:
            if section['type'] == section_type:
                # Extract key phrases already identified
                key_phrases = section.get('key_phrases', [])
                insights.extend(key_phrases)
                
                # Extract important sentences (containing keywords like "significant", "novel", etc.)
                sentences = section.get('sentences', [])
                important_sentences = [
                    s for s in sentences 
                    if any(keyword in s.lower() for keyword in 
                          ['significant', 'novel', 'innovative', 'breakthrough', 'important', 'key', 'crucial'])
                ]
                insights.extend(important_sentences[:3])  # Top 3 important sentences
        
        return insights[:10]  # Return top 10 insights
    
    def generate_section_summary_report(self, section_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary report of section analysis.
        
        Args:
            section_data (Dict[str, Any]): Section data
            
        Returns:
            str: Summary report
        """
        if not section_data:
            return "No section data available."
        
        analysis = self.analyze_section_distribution(section_data)
        metadata = section_data.get('metadata', {})
        
        report = f"""
Section Analysis Report
{'='*50}

Paper Information:
- Title: {metadata.get('title', 'Unknown')}
- Authors: {metadata.get('author', 'Unknown')}
- Pages: {metadata.get('page_count', 'Unknown')}

Section Overview:
- Total Sections: {analysis.get('total_sections', 0)}
- Average Section Length: {analysis.get('average_section_length', 0)} words

Section Distribution:
"""
        
        section_types = analysis.get('section_types', {})
        for section_type, count in sorted(section_types.items(), key=lambda x: x[1], reverse=True):
            report += f"- {section_type.title()}: {count} section(s)\n"
        
        if analysis.get('longest_section'):
            longest = analysis['longest_section']
            report += f"\nLongest Section: {longest['title']} ({longest['word_count']} words)\n"
        
        if analysis.get('shortest_section'):
            shortest = analysis['shortest_section']
            report += f"Shortest Section: {shortest['title']} ({shortest['word_count']} words)\n"
        
        # Add key insights from abstract
        abstract_insights = self.extract_key_insights(section_data, 'abstract')
        if abstract_insights:
            report += f"\nKey Insights from Abstract:\n"
            for insight in abstract_insights[:5]:
                report += f"- {insight}\n"
        
        return report
    
    def save_analysis_report(self, section_data: Dict[str, Any], output_path: str) -> bool:
        """
        Save comprehensive analysis report to file.
        
        Args:
            section_data (Dict[str, Any]): Section data
            output_path (str): Path to save the report
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            analysis = self.analyze_section_distribution(section_data)
            report = self.generate_section_summary_report(section_data)
            
            # Prepare comprehensive report data
            report_data = {
                'paper_metadata': section_data.get('metadata', {}),
                'section_analysis': analysis,
                'text_report': report,
                'raw_sections': section_data.get('sections', [])
            }
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            # Also save text version
            text_path = output_path.with_suffix('.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.logger.info(f"Analysis report saved to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving analysis report: {str(e)}")
            return False


# Convenience functions
def analyze_paper_sections(section_file_path: str) -> Dict[str, Any]:
    """
    Convenience function to analyze sections of a single paper.
    
    Args:
        section_file_path (str): Path to section data file
        
    Returns:
        Dict[str, Any]: Analysis results
    """
    analyzer = SectionAnalyzer()
    section_data = analyzer.load_section_data(section_file_path)
    return analyzer.analyze_section_distribution(section_data)


def generate_paper_report(section_file_path: str, output_path: str = None) -> str:
    """
    Convenience function to generate a report for a paper.
    
    Args:
        section_file_path (str): Path to section data file
        output_path (str): Optional path to save the report
        
    Returns:
        str: Generated report
    """
    analyzer = SectionAnalyzer()
    section_data = analyzer.load_section_data(section_file_path)
    report = analyzer.generate_section_summary_report(section_data)
    
    if output_path:
        analyzer.save_analysis_report(section_data, output_path)
    
    return report


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Analyze all section files in data/section_analysis
    section_dir = Path("data/section_analysis")
    if section_dir.exists():
        section_files = list(section_dir.glob("*_sections.json"))
        
        if section_files:
            print(f"Found {len(section_files)} section files to analyze")
            
            for section_file in section_files:
                print(f"\nAnalyzing: {section_file.name}")
                analysis = analyze_paper_sections(str(section_file))
                print(f"Sections: {analysis.get('total_sections', 0)}")
                print(f"Types: {list(analysis.get('section_types', {}).keys())}")
        else:
            print("No section files found. Run section_extractor.py first.")
    else:
        print("Section analysis directory not found. Run section_extractor.py first.")
