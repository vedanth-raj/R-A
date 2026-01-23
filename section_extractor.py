"""
Section-wise text extraction module for research papers.
Enhances the existing text extraction with intelligent section detection and analysis.
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from paper_retrieval.text_extractor import PDFTextExtractor


@dataclass
class Section:
    """Represents a section of a research paper."""
    title: str
    content: str
    start_page: int = 1
    end_page: int = 1
    section_type: str = "unknown"
    word_count: int = 0
    
    def __post_init__(self):
        self.word_count = len(self.content.split())


class SectionWiseExtractor:
    """
    Extracts and analyzes text from research papers section by section.
    Provides intelligent section detection and structured storage for analysis.
    """
    
    def __init__(self):
        """Initialize the section-wise extractor."""
        self.logger = logging.getLogger(__name__)
        self.base_extractor = PDFTextExtractor()
        
        # Common section patterns in research papers
        self.section_patterns = {
            'abstract': [
                r'^abstract\s*$',
                r'^a b s t r a c t\s*$',
                r'^summary\s*$'
            ],
            'introduction': [
                r'^introduction\s*$',
                r'^1\s+introduction\s*$',
                r'^i\s+introduction\s*$'
            ],
            'related_work': [
                r'^related\s+work\s*$',
                r'^literature\s+review\s*$',
                r'^background\s*$',
                r'^2\s+related\s+work\s*$'
            ],
            'methodology': [
                r'^methodology\s*$',
                r'^methods\s*$',
                r'^method\s*$',
                r'^approach\s*$',
                r'^3\s+methodology\s*$'
            ],
            'experiments': [
                r'^experiments?\s*$',
                r'^experimental\s+setup\s*$',
                r'^evaluation\s*$',
                r'^4\s+experiments?\s*$'
            ],
            'results': [
                r'^results\s*$',
                r'^findings\s*$',
                r'^5\s+results\s*$'
            ],
            'discussion': [
                r'^discussion\s*$',
                r'^analysis\s*$',
                r'^6\s+discussion\s*$'
            ],
            'conclusion': [
                r'^conclusion\s*$',
                r'^conclusions\s*$',
                r'^summary\s*$',
                r'^7\s+conclusion\s*$'
            ],
            'references': [
                r'^references\s*$',
                r'^bibliography\s*$',
                r'^8\s+references\s*$'
            ],
            'appendix': [
                r'^appendix\s*$',
                r'^appendices\s*$',
                r'^a\s+appendix\s*$'
            ]
        }
    
    def detect_sections_from_text(self, full_text: str) -> List[Section]:
        """
        Detect sections from full text without page information.
        
        Args:
            full_text (str): Full text of the paper
            
        Returns:
            List[Section]: Detected sections
        """
        # Create a simple page_texts structure for compatibility
        page_texts = [{'page_num': 1, 'text': full_text}]
        return self.detect_sections(full_text, page_texts)
    
    def detect_sections(self, full_text: str, page_texts: List[Dict]) -> List[Section]:
        """
        Detect sections in the research paper text.
        
        Args:
            full_text (str): Full text of the paper
            page_texts (List[Dict]): List of page texts with page numbers
            
        Returns:
            List[Section]: Detected sections
        """
        sections = []
        lines = full_text.split('\n')
        current_section = None
        current_content = []
        current_start_page = 1
        
        # Find page number for each line
        line_to_page = {}
        current_page = 1
        page_text_index = 0
        
        for i, line in enumerate(lines):
            # Update current page based on page markers
            if "--- Page" in line:
                page_match = re.search(r'Page (\d+)', line)
                if page_match:
                    current_page = int(page_match.group(1))
                continue
            
            line_to_page[i] = current_page
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Skip page markers
            if "--- Page" in line_stripped:
                continue
            
            # Check if this line matches a section header
            section_type, confidence = self._identify_section_type(line_stripped)
            
            if confidence > 0.7:  # High confidence section header
                # Save previous section if exists
                if current_section:
                    content = '\n'.join(current_content).strip()
                    if content:
                        sections.append(Section(
                            title=current_section['title'],
                            content=content,
                            start_page=current_section['start_page'],
                            end_page=line_to_page.get(i, current_section['start_page']),
                            section_type=current_section['type']
                        ))
                
                # Start new section
                current_section = {
                    'title': line_stripped,
                    'type': section_type,
                    'start_page': line_to_page.get(i, 1)
                }
                current_content = []
            elif current_section:
                # Add content to current section
                current_content.append(line)
        
        # Save the last section
        if current_section and current_content:
            content = '\n'.join(current_content).strip()
            if content:
                sections.append(Section(
                    title=current_section['title'],
                    content=content,
                    start_page=current_section['start_page'],
                    end_page=line_to_page.get(len(lines) - 1, current_section['start_page']),
                    section_type=current_section['type']
                ))
        
        return sections
    
    def _identify_section_type(self, line: str) -> Tuple[str, float]:
        """
        Identify the type of section based on the line content.
        
        Args:
            line (str): Section header line
            
        Returns:
            Tuple[str, float]: Section type and confidence score
        """
        line_lower = line.lower()
        
        for section_type, patterns in self.section_patterns.items():
            for pattern in patterns:
                if re.match(pattern, line_lower, re.IGNORECASE):
                    return section_type, 1.0
        
        # Check for numbered sections (e.g., "1. Introduction", "2. Methodology")
        numbered_pattern = r'^(\d+|[ivx]+)\.?\s+(.+)$'
        match = re.match(numbered_pattern, line_lower)
        if match:
            section_title = match.group(2)
            for section_type, patterns in self.section_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, section_title, re.IGNORECASE):
                        return section_type, 0.8
        
        return "unknown", 0.0
    
    def extract_sections_from_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract sections from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing section-wise data
        """
        try:
            # First extract basic text using existing extractor
            extracted_data = self.base_extractor.extract_text_from_pdf(pdf_path)
            
            if not extracted_data:
                return None
            
            # Detect sections
            sections = self.detect_sections(
                extracted_data['full_text'], 
                extracted_data['page_texts']
            )
            
            # Prepare section-wise data
            section_data = {
                'metadata': extracted_data['metadata'],
                'sections': [],
                'section_summary': {},
                'extraction_success': True
            }
            
            # Process each section
            for section in sections:
                section_dict = {
                    'title': section.title,
                    'type': section.section_type,
                    'content': section.content,
                    'start_page': section.start_page,
                    'end_page': section.end_page,
                    'word_count': section.word_count,
                    'key_phrases': self._extract_key_phrases(section.content),
                    'sentences': self._split_sentences(section.content)
                }
                section_data['sections'].append(section_dict)
            
            # Create summary statistics
            section_data['section_summary'] = self._create_section_summary(sections)
            
            self.logger.info(f"Successfully extracted {len(sections)} sections from {Path(pdf_path).name}")
            return section_data
            
        except Exception as e:
            self.logger.error(f"Error extracting sections from {pdf_path}: {str(e)}")
            return None
    
    def _extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """
        Extract key phrases from section content.
        
        Args:
            text (str): Section content
            max_phrases (int): Maximum number of phrases to extract
            
        Returns:
            List[str]: Key phrases
        """
        # Simple keyword extraction based on common academic terms
        # This can be enhanced with NLP techniques
        words = text.lower().split()
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Filter words and count frequency
        filtered_words = [word for word in words if len(word) > 3 and word not in stop_words]
        word_freq = {}
        
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top phrases
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in top_words[:max_phrases]]
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text (str): Section content
            
        Returns:
            List[str]: Sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _create_section_summary(self, sections: List[Section]) -> Dict[str, Any]:
        """
        Create a summary of all sections.
        
        Args:
            sections (List[Section]): List of detected sections
            
        Returns:
            Dict[str, Any]: Section summary statistics
        """
        summary = {
            'total_sections': len(sections),
            'section_types': {},
            'total_words': 0,
            'page_coverage': {}
        }
        
        for section in sections:
            # Count section types
            section_type = section.section_type
            summary['section_types'][section_type] = summary['section_types'].get(section_type, 0) + 1
            
            # Total word count
            summary['total_words'] += section.word_count
            
            # Page coverage
            for page in range(section.start_page, section.end_page + 1):
                summary['page_coverage'][page] = summary['page_coverage'].get(page, 0) + 1
        
        return summary
    
    def save_section_data(self, section_data: Dict[str, Any], output_path: str) -> bool:
        """
        Save section-wise data to JSON file.
        
        Args:
            section_data (Dict[str, Any]): Section data to save
            output_path (str): Path to save the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(section_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved section data to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving section data to {output_path}: {str(e)}")
            return False
    
    def process_pdfs_for_sections(self, pdf_dir: str = "Downloaded_pdfs", 
                                 output_dir: str = "data/section_analysis") -> Dict[str, Any]:
        """
        Process all PDFs in directory for section-wise analysis.
        
        Args:
            pdf_dir (str): Directory containing PDF files
            output_dir (str): Directory to save section analysis
            
        Returns:
            Dict[str, Any]: Processing results
        """
        pdf_path = Path(pdf_dir)
        
        if not pdf_path.exists():
            self.logger.error(f"PDF directory not found: {pdf_dir}")
            return {'success': [], 'failed': [], 'total': 0}
        
        pdf_files = list(pdf_path.glob("*.pdf"))
        results = {'success': [], 'failed': [], 'total': len(pdf_files)}
        
        for pdf_file in pdf_files:
            self.logger.info(f"Processing sections for: {pdf_file.name}")
            
            section_data = self.extract_sections_from_pdf(str(pdf_file))
            
            if section_data:
                results['success'].append({
                    'file': pdf_file.name,
                    'sections_found': len(section_data['sections']),
                    'data': section_data
                })
                
                # Save section data
                output_path = Path(output_dir) / f"{pdf_file.stem}_sections.json"
                self.save_section_data(section_data, str(output_path))
            else:
                results['failed'].append(pdf_file.name)
        
        self.logger.info(f"Section processing complete: {len(results['success'])} successful, {len(results['failed'])} failed")
        return results


# Convenience functions
def extract_sections_from_pdf(pdf_path: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to extract sections from a single PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        Optional[Dict[str, Any]]: Section data or None if failed
    """
    extractor = SectionWiseExtractor()
    return extractor.extract_sections_from_pdf(pdf_path)


def process_all_pdfs_for_sections(pdf_dir: str = "Downloaded_pdfs", 
                                 output_dir: str = "data/section_analysis") -> Dict[str, Any]:
    """
    Convenience function to process all PDFs for section analysis.
    
    Args:
        pdf_dir (str): Directory containing PDF files
        output_dir (str): Directory to save section analysis
        
    Returns:
        Dict[str, Any]: Processing results
    """
    extractor = SectionWiseExtractor()
    return extractor.process_pdfs_for_sections(pdf_dir, output_dir)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Process all PDFs for section analysis
    results = process_all_pdfs_for_sections()
    
    print(f"Section Analysis Results:")
    print(f"Total PDFs: {results['total']}")
    print(f"Successfully processed: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    
    for success in results['success']:
        print(f"  - {success['file']}: {success['sections_found']} sections found")
