"""
Text extraction module for parsing PDFs using PyMuPDF.
"""

import fitz  # PyMuPDF
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import json


class PDFTextExtractor:
    """
    A class to extract text and metadata from PDF files using PyMuPDF.
    """
    
    def __init__(self):
        """Initialize the PDF text extractor."""
        self.logger = logging.getLogger(__name__)
        
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract text and metadata from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing extracted text and metadata,
                                     or None if extraction fails
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                self.logger.error(f"PDF file not found: {pdf_path}")
                return None
                
            # Open the PDF file
            doc = fitz.open(str(pdf_path))
            
            # Extract metadata
            metadata = doc.metadata
            metadata.update({
                'page_count': doc.page_count,
                'file_size': pdf_path.stat().st_size,
                'file_name': pdf_path.name
            })
            
            # Extract text from all pages
            full_text = ""
            page_texts = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_text = page.get_text()
                
                # Store page-specific text
                page_texts.append({
                    'page_number': page_num + 1,
                    'text': page_text,
                    'word_count': len(page_text.split())
                })
                
                # Add to full text
                full_text += f"\n--- Page {page_num + 1} ---\n"
                full_text += page_text
                full_text += "\n"
            
            # Close the document
            doc.close()
            
            # Prepare result
            result = {
                'metadata': metadata,
                'full_text': full_text.strip(),
                'page_texts': page_texts,
                'total_words': len(full_text.split()),
                'extraction_success': True
            }
            
            self.logger.info(f"Successfully extracted text from {pdf_path.name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return None
    
    def extract_abstract(self, extracted_data: Dict[str, Any]) -> Optional[str]:
        """
        Attempt to extract the abstract from the extracted text.
        
        Args:
            extracted_data (Dict[str, Any]): Data from extract_text_from_pdf
            
        Returns:
            Optional[str]: Extracted abstract or None if not found
        """
        if not extracted_data or 'full_text' not in extracted_data:
            return None
            
        text = extracted_data['full_text'].lower()
        
        # Common patterns for abstract sections
        abstract_patterns = [
            'abstract',
            'a b s t r a c t',
            'summary',
            'introduction'  # Sometimes abstract is under introduction
        ]
        
        lines = extracted_data['full_text'].split('\n')
        abstract_lines = []
        abstract_found = False
        abstract_end_patterns = [
            'keywords:',
            'key words:',
            'introduction',
            '1.',
            'i.',
            'methodology',
            'methods',
            'results'
        ]
        
        for line in lines:
            line_lower = line.strip().lower()
            
            # Check if we found the start of abstract
            if any(pattern in line_lower for pattern in abstract_patterns):
                abstract_found = True
                # Skip the abstract header line
                continue
                
            # If we found abstract, collect lines until we hit an end pattern
            if abstract_found:
                if any(pattern in line_lower for pattern in abstract_end_patterns):
                    break
                if line.strip():  # Skip empty lines
                    abstract_lines.append(line.strip())
        
        # Join abstract lines and limit to reasonable length
        abstract = ' '.join(abstract_lines)
        
        # If abstract is too long, it's probably not the abstract
        if len(abstract) > 2000:
            return None
            
        return abstract if abstract else None
    
    def save_extracted_data(self, extracted_data: Dict[str, Any], output_path: str, format: str = "json") -> bool:
        """
        Save extracted data to a file (JSON or TXT format).
        
        Args:
            extracted_data (Dict[str, Any]): Data to save
            output_path (str): Path to save the file
            format (str): Output format - "json" or "txt"
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == "txt":
                # Save as plain text file
                with open(output_path, 'w', encoding='utf-8') as f:
                    # Write metadata header
                    metadata = extracted_data.get('metadata', {})
                    f.write("=" * 50 + "\n")
                    f.write("METADATA\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for key, value in metadata.items():
                        if value:
                            f.write(f"{key}: {value}\n")
                    
                    f.write("\n" + "=" * 50 + "\n")
                    f.write("FULL TEXT\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Write full text
                    full_text = extracted_data.get('full_text', '')
                    f.write(full_text)
                    
                    # Write abstract if available
                    abstract = self.extract_abstract(extracted_data)
                    if abstract:
                        f.write("\n" + "=" * 50 + "\n")
                        f.write("ABSTRACT\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(abstract)
            else:
                # Save as JSON file (default)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted_data, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Saved extracted data to {output_path} ({format.upper()} format)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving extracted data to {output_path}: {str(e)}")
            return False
    
    def process_downloaded_pdfs(self, downloaded_dir: str = "Downloaded_pdfs", 
                           output_dir: str = "data/extracted_texts", format: str = "txt") -> Dict[str, Any]:
        """
        Process all PDFs in Downloaded_pdfs directory.
        
        Args:
            downloaded_dir (str): Directory containing downloaded PDFs
            output_dir (str): Directory to save extracted text
            format (str): Output format - "json" or "txt"
            
        Returns:
            Dict[str, Any]: Results including successful and failed extractions
        """
        downloaded_path = Path(downloaded_dir)
        
        if not downloaded_path.exists():
            self.logger.error(f"Downloaded directory not found: {downloaded_path}")
            return {'success': [], 'failed': [], 'total': 0}
        
        pdf_files = list(downloaded_path.glob("*.pdf"))
        results = {'success': [], 'failed': [], 'total': len(pdf_files)}
        
        for pdf_file in pdf_files:
            self.logger.info(f"Processing: {pdf_file.name}")
            
            extracted_data = self.extract_text_from_pdf(str(pdf_file))
            
            if extracted_data:
                results['success'].append({
                    'file': pdf_file.name,
                    'data': extracted_data
                })
                
                # Save to output directory
                output_path = Path(output_dir) / f"{pdf_file.stem}_extracted.{format}"
                self.save_extracted_data(extracted_data, str(output_path), format)
            else:
                results['failed'].append(pdf_file.name)
        
        self.logger.info(f"Processing complete: {len(results['success'])} successful, {len(results['failed'])} failed")
        return results
    
    def batch_extract_from_directory(self, directory_path: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Extract text from all PDFs in a directory.
        
        Args:
            directory_path (str): Path to directory containing PDFs
            output_dir (str): Optional directory to save extracted data
            
        Returns:
            Dict[str, Any]: Results including successful and failed extractions
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            self.logger.error(f"Directory not found: {directory_path}")
            return {'success': [], 'failed': [], 'total': 0}
        
        pdf_files = list(directory_path.glob('*.pdf'))
        results = {'success': [], 'failed': [], 'total': len(pdf_files)}
        
        for pdf_file in pdf_files:
            self.logger.info(f"Processing: {pdf_file.name}")
            
            extracted_data = self.extract_text_from_pdf(str(pdf_file))
            
            if extracted_data:
                results['success'].append({
                    'file': pdf_file.name,
                    'data': extracted_data
                })
                
                # Save to output directory if specified
                if output_dir:
                    output_path = Path(output_dir) / f"{pdf_file.stem}_extracted.json"
                    self.save_extracted_data(extracted_data, str(output_path))
            else:
                results['failed'].append(pdf_file.name)
        
        self.logger.info(f"Batch extraction complete: {len(results['success'])} successful, {len(results['failed'])} failed")
        return results


# Convenience function for quick extraction
def extract_pdf_text(pdf_path: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to extract text from a single PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        Optional[Dict[str, Any]]: Extracted data or None if failed
    """
    extractor = PDFTextExtractor()
    return extractor.extract_text_from_pdf(pdf_path)

# Convenience function to process Downloaded_pdfs directory
def process_downloaded_pdfs(downloaded_dir: str = "Downloaded_pdfs", 
                            output_dir: str = "data/extracted_texts", format: str = "txt") -> Dict[str, Any]:
    """
    Convenience function to process all PDFs in Downloaded_pdfs directory.
    
    Args:
        downloaded_dir (str): Directory containing downloaded PDFs
        output_dir (str): Directory to save extracted text
        format (str): Output format - "json" or "txt"
        
    Returns:
        Dict[str, Any]: Results including successful and failed extractions
    """
    extractor = PDFTextExtractor()
    return extractor.process_downloaded_pdfs(downloaded_dir, output_dir, format)
