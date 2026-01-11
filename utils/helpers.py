"""
Helper utility functions for filename sanitization, logging, and common operations.
"""
import re
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Sanitize a string to be used as a filename.
    
    Args:
        text: The text to sanitize
        max_length: Maximum length of the resulting filename
        
    Returns:
        Sanitized filename-safe string
    """
    if not text:
        return "unknown"
    
    # Remove or replace invalid filename characters
    # Windows: < > : " / \ | ? *
    # Unix: / and null
    sanitized = re.sub(r'[<>:"/\\|?*\x00]', '_', text)
    
    # Replace multiple spaces/underscores with single underscore
    sanitized = re.sub(r'[\s_]+', '_', sanitized)
    
    # Remove leading/trailing dots and spaces (Windows doesn't allow these)
    sanitized = sanitized.strip('. ')
    
    # Truncate to max_length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unknown"
    
    return sanitized


def get_first_author_lastname(authors: Optional[list]) -> str:
    """
    Extract the last name of the first author from the authors list.
    
    Args:
        authors: List of Author objects (Pydantic models) with 'name' attribute
        
    Returns:
        Last name of first author, or 'unknown' if not available
    """
    if not authors or len(authors) == 0:
        return "unknown"
    
    first_author = authors[0]
    # Handle both Pydantic models and dictionaries
    if hasattr(first_author, 'name'):
        name = first_author.name
    elif isinstance(first_author, dict):
        name = first_author.get("name", "")
    else:
        return "unknown"
    
    if not name:
        return "unknown"
    
    # Split name and get last part (last name)
    name_parts = name.strip().split()
    if name_parts:
        return sanitize_filename(name_parts[-1], max_length=20)
    
    return "unknown"


def generate_pdf_filename(title: str, authors: Optional[list], year: Optional[int]) -> str:
    """
    Generate a safe filename for a PDF based on paper metadata.
    
    Format: {first_author_lastname}{year}_{sanitized_title[:50]}.pdf
    
    Args:
        title: Paper title
        authors: List of author dictionaries
        year: Publication year
        
    Returns:
        Safe filename string
    """
    author_lastname = get_first_author_lastname(authors)
    year_str = str(year) if year else "unknown"
    sanitized_title = sanitize_filename(title, max_length=50)
    
    filename = f"{author_lastname}{year_str}_{sanitized_title}.pdf"
    return filename


def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {path}")

