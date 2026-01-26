"""
APA reference formatting module for research papers.
Formats references according to APA 7th edition guidelines.
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import unicodedata


@dataclass
class Reference:
    """Represents a research paper reference."""
    authors: List[str]
    year: int
    title: str
    journal: str
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    book_title: Optional[str] = None
    edition: Optional[str] = None
    ref_type: str = "journal"  # journal, book, conference, etc.


class APAFormatter:
    """
    Formats references according to APA 7th edition guidelines.
    Handles various source types including journal articles, books, and conference papers.
    """
    
    def __init__(self):
        """Initialize the APA formatter."""
        self.logger = logging.getLogger(__name__)
        
        # Common journal name abbreviations
        self.journal_abbreviations = {
            "Journal of the American Medical Association": "JAMA",
            "New England Journal of Medicine": "N Engl J Med",
            "Nature": "Nature",
            "Science": "Science",
            "Proceedings of the National Academy of Sciences": "Proc Natl Acad Sci USA",
            "PLoS ONE": "PLoS ONE",
            "Public Library of Science ONE": "PLoS ONE"
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for APA formatting.
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\-\.,;:!?()[\]/"\'&@#%*+=<>]', '', text)
        
        return text
    
    def format_authors(self, authors: List[str]) -> str:
        """
        Format author names according to APA style.
        
        Args:
            authors (List[str]): List of author names
            
        Returns:
            str: Formatted author string
        """
        if not authors:
            return ""
        
        formatted_authors = []
        
        for i, author in enumerate(authors):
            author = self.clean_text(author)
            
            # Handle different name formats
            if ',' in author:
                # Format: "Last, First" or "Last, First Middle"
                parts = author.split(',', 1)
                last_name = parts[0].strip()
                first_part = parts[1].strip() if len(parts) > 1 else ""
                
                # Extract initials
                initials = []
                for part in first_part.split():
                    if part:
                        initials.append(part[0].upper() + '.')
                
                if initials:
                    formatted_author = f"{last_name}, {' '.join(initials)}"
                else:
                    formatted_author = last_name
            else:
                # Format: "First Last" or "First Middle Last"
                parts = author.split()
                if len(parts) >= 2:
                    last_name = parts[-1]
                    first_parts = parts[:-1]
                    initials = [p[0].upper() + '.' for p in first_parts]
                    formatted_author = f"{last_name}, {' '.join(initials)}"
                else:
                    formatted_author = author
            
            formatted_authors.append(formatted_author)
        
        # Apply APA rules for multiple authors
        if len(formatted_authors) == 1:
            return formatted_authors[0]
        elif len(formatted_authors) == 2:
            return f"{formatted_authors[0]} & {formatted_authors[1]}"
        elif len(formatted_authors) <= 20:
            return ', '.join(formatted_authors[:-1]) + f", & {formatted_authors[-1]}"
        else:
            # More than 20 authors: list first 19, ..., last author
            first_19 = ', '.join(formatted_authors[:19])
            last_author = formatted_authors[-1]
            return f"{first_19}, ... {last_author}"
    
    def format_title(self, title: str, ref_type: str = "journal") -> str:
        """
        Format title according to APA style.
        
        Args:
            title (str): Title to format
            ref_type (str): Type of reference
            
        Returns:
            str: Formatted title
        """
        title = self.clean_text(title)
        
        if ref_type == "journal":
            # Journal article titles: sentence case
            return title.capitalize()
        elif ref_type == "book":
            # Book titles: sentence case with italics
            return f"*{title}*"
        else:
            # Other types: sentence case
            return title.capitalize()
    
    def format_journal_info(self, journal: str, volume: Optional[str] = None, 
                          issue: Optional[str] = None, pages: Optional[str] = None) -> str:
        """
        Format journal information according to APA style.
        
        Args:
            journal (str): Journal name
            volume (Optional[str]): Volume number
            issue (Optional[str]): Issue number
            pages (Optional[str]): Page numbers
            
        Returns:
            str: Formatted journal information
        """
        journal = self.clean_text(journal)
        
        # Use abbreviation if available
        if journal in self.journal_abbreviations:
            journal = self.journal_abbreviations[journal]
        
        parts = [f"*{journal}*"]
        
        if volume:
            volume = self.clean_text(volume)
            parts.append(f"*{volume}*")
            
            if issue:
                issue = self.clean_text(issue)
                parts.append(f"({issue})")
        
        if pages:
            pages = self.clean_text(pages)
            # Ensure proper page range format
            if '-' in pages and not pages.startswith('pp.'):
                pages = f"pp. {pages}"
            parts.append(pages)
        
        return ', '.join(parts)
    
    def format_doi_url(self, doi: Optional[str] = None, url: Optional[str] = None) -> str:
        """
        Format DOI and URL according to APA style.
        
        Args:
            doi (Optional[str]): DOI
            url (Optional[str]): URL
            
        Returns:
            str: Formatted DOI/URL
        """
        if doi:
            doi = self.clean_text(doi)
            if not doi.startswith('https://doi.org/'):
                doi = f"https://doi.org/{doi}"
            return doi
        elif url:
            url = self.clean_text(url)
            return url
        else:
            return ""
    
    def format_journal_reference(self, reference: Reference) -> str:
        """
        Format a journal article reference.
        
        Args:
            reference (Reference): Reference data
            
        Returns:
            str: Formatted reference
        """
        authors = self.format_authors(reference.authors)
        year_part = f"({reference.year})."
        title = self.format_title(reference.title, "journal")
        journal_info = self.format_journal_info(
            reference.journal, reference.volume, reference.issue, reference.pages
        )
        doi_url = self.format_doi_url(reference.doi, reference.url)
        
        parts = [authors, year_part, title, journal_info]
        if doi_url:
            parts.append(doi_url)
        
        return ' '.join(parts)
    
    def format_book_reference(self, reference: Reference) -> str:
        """
        Format a book reference.
        
        Args:
            reference (Reference): Reference data
            
        Returns:
            str: Formatted reference
        """
        authors = self.format_authors(reference.authors)
        year_part = f"({reference.year})."
        title = self.format_title(reference.title, "book")
        
        parts = [authors, year_part, title]
        
        if reference.edition:
            parts.append(f"({reference.edition} ed.).")
        
        if reference.publisher:
            parts.append(reference.publisher)
        
        return ' '.join(parts)
    
    def format_conference_reference(self, reference: Reference) -> str:
        """
        Format a conference paper reference.
        
        Args:
            reference (Reference): Reference data
            
        Returns:
            str: Formatted reference
        """
        authors = self.format_authors(reference.authors)
        year_part = f"({reference.year})."
        title = self.format_title(reference.title, "conference")
        
        parts = [authors, year_part, title]
        
        if reference.book_title:
            parts.append(f"In *{reference.book_title}*")
        
        if reference.pages:
            parts.append(f"(pp. {reference.pages})")
        
        if reference.publisher:
            parts.append(reference.publisher)
        
        return ' '.join(parts)
    
    def format_reference(self, reference: Reference) -> str:
        """
        Format a reference based on its type.
        
        Args:
            reference (Reference): Reference data
            
        Returns:
            str: Formatted reference
        """
        if reference.ref_type == "journal":
            return self.format_journal_reference(reference)
        elif reference.ref_type == "book":
            return self.format_book_reference(reference)
        elif reference.ref_type == "conference":
            return self.format_conference_reference(reference)
        else:
            # Default to journal format
            return self.format_journal_reference(reference)
    
    def format_references_list(self, references: List[Reference]) -> str:
        """
        Format a list of references.
        
        Args:
            references (List[Reference]): List of references
            
        Returns:
            str: Formatted references list
        """
        if not references:
            return ""
        
        formatted_refs = []
        
        for ref in references:
            try:
                formatted = self.format_reference(ref)
                formatted_refs.append(formatted)
            except Exception as e:
                self.logger.warning(f"Error formatting reference: {e}")
                continue
        
        return '\n\n'.join(formatted_refs)
    
    def parse_semantic_scholar_data(self, paper_data: Dict[str, Any]) -> Reference:
        """
        Parse Semantic Scholar data into Reference object.
        
        Args:
            paper_data (Dict[str, Any]): Paper data from Semantic Scholar
            
        Returns:
            Reference: Parsed reference
        """
        # Extract authors
        authors = []
        if 'authors' in paper_data:
            for author in paper_data['authors']:
                if isinstance(author, dict) and 'name' in author:
                    authors.append(author['name'])
                elif isinstance(author, str):
                    authors.append(author)
        
        # Extract year
        year = paper_data.get('year', datetime.now().year)
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        
        # Extract title
        title = paper_data.get('title', '')
        
        # Determine reference type and extract relevant info
        venue = paper_data.get('venue', '')
        journal = paper_data.get('journal', venue)
        
        # Check if it's a conference paper
        ref_type = "journal"
        if any(keyword in venue.lower() for keyword in ['conference', 'proceedings', 'symposium', 'workshop']):
            ref_type = "conference"
        
        # Extract publication info
        volume = paper_data.get('volume')
        issue = paper_data.get('issue')
        pages = paper_data.get('pages')
        doi = paper_data.get('doi')
        url = paper_data.get('url')
        
        return Reference(
            authors=authors,
            year=year,
            title=title,
            journal=journal,
            volume=volume,
            issue=issue,
            pages=pages,
            doi=doi,
            url=url,
            ref_type=ref_type
        )
    
    def load_papers_from_json(self, json_file: str) -> List[Reference]:
        """
        Load papers from JSON file and convert to references.
        
        Args:
            json_file (str): Path to JSON file
            
        Returns:
            List[Reference]: List of references
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            references = []
            
            if isinstance(data, dict) and 'papers' in data:
                papers = data['papers']
            elif isinstance(data, list):
                papers = data
            else:
                papers = [data]
            
            for paper in papers:
                try:
                    ref = self.parse_semantic_scholar_data(paper)
                    references.append(ref)
                except Exception as e:
                    self.logger.warning(f"Error parsing paper data: {e}")
                    continue
            
            return references
            
        except Exception as e:
            self.logger.error(f"Error loading papers from {json_file}: {e}")
            return []
    
    def generate_bibliography(self, papers_file: str, output_file: str) -> Dict[str, Any]:
        """
        Generate APA-formatted bibliography from papers data.
        
        Args:
            papers_file (str): Path to papers JSON file
            output_file (str): Output file path
            
        Returns:
            Dict[str, Any]: Generation results
        """
        try:
            # Load papers
            references = self.load_papers_from_json(papers_file)
            
            if not references:
                raise ValueError("No valid references found")
            
            # Format references
            formatted_refs = self.format_references_list(references)
            
            # Save to file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("References\n")
                f.write("==========\n\n")
                f.write(formatted_refs)
            
            # Generate statistics
            stats = {
                'total_references': len(references),
                'journal_articles': sum(1 for r in references if r.ref_type == 'journal'),
                'conference_papers': sum(1 for r in references if r.ref_type == 'conference'),
                'books': sum(1 for r in references if r.ref_type == 'book'),
                'with_doi': sum(1 for r in references if r.doi),
                'output_file': str(output_path)
            }
            
            self.logger.info(f"Generated bibliography with {len(references)} references")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error generating bibliography: {e}")
            raise
    
    def format_in_text_citation(self, reference: Reference, citation_type: str = "parenthetical") -> str:
        """
        Format in-text citation according to APA style.
        
        Args:
            reference (Reference): Reference data
            citation_type (str): Type of citation ("parenthetical" or "narrative")
            
        Returns:
            str: Formatted in-text citation
        """
        if not reference.authors:
            return f"({reference.year})"
        
        # Format author names for in-text citation
        if len(reference.authors) == 1:
            author_text = reference.authors[0].split(',')[0]  # Last name only
        elif len(reference.authors) == 2:
            author1 = reference.authors[0].split(',')[0]
            author2 = reference.authors[1].split(',')[0]
            author_text = f"{author1} & {author2}"
        elif len(reference.authors) <= 6:
            last_names = [author.split(',')[0] for author in reference.authors]
            author_text = ', '.join(last_names[:-1]) + f", & {last_names[-1]}"
        else:
            # More than 6 authors: first author et al.
            author_text = f"{reference.authors[0].split(',')[0]} et al."
        
        if citation_type == "narrative":
            return f"{author_text} ({reference.year})"
        else:
            return f"({author_text}, {reference.year})"


# Convenience functions
def generate_apa_bibliography(papers_file: str, output_file: str) -> Dict[str, Any]:
    """
    Convenience function to generate APA bibliography.
    
    Args:
        papers_file (str): Path to papers JSON file
        output_file (str): Output file path
        
    Returns:
        Dict[str, Any]: Generation results
    """
    formatter = APAFormatter()
    return formatter.generate_bibliography(papers_file, output_file)


def format_paper_references(selected_papers_file: str, output_dir: str) -> Dict[str, Any]:
    """
    Format references for selected papers.
    
    Args:
        selected_papers_file (str): Path to selected papers JSON
        output_dir (str): Output directory
        
    Returns:
        Dict[str, Any]: Formatting results
    """
    formatter = APAFormatter()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate bibliography
    bib_file = output_path / "apa_references.txt"
    stats = formatter.generate_bibliography(selected_papers_file, str(bib_file))
    
    # Generate in-text citations guide
    references = formatter.load_papers_from_json(selected_papers_file)
    
    citations_file = output_path / "in_text_citations.txt"
    with open(citations_file, 'w', encoding='utf-8') as f:
        f.write("In-Text Citations Guide\n")
        f.write("=======================\n\n")
        
        for i, ref in enumerate(references[:10]):  # Show first 10
            parenthetical = formatter.format_in_text_citation(ref, "parenthetical")
            narrative = formatter.format_in_text_citation(ref, "narrative")
            
            f.write(f"{i+1}. {ref.title[:50]}...\n")
            f.write(f"   Parenthetical: {parenthetical}\n")
            f.write(f"   Narrative: {narrative}\n\n")
    
    stats['citations_file'] = str(citations_file)
    return stats
