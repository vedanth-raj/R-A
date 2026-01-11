"""
PDF download functionality for open-access papers.
"""
import os
import logging
import time
from pathlib import Path
from typing import List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import PAPERS_DIR, REQUEST_DELAY_SECONDS, MAX_RETRIES, RETRY_BACKOFF_FACTOR
from paper_retrieval.models import PaperMetadata
from utils.helpers import generate_pdf_filename, ensure_directory

logger = logging.getLogger(__name__)


class PDFDownloader:
    """
    Handles downloading PDFs from open-access URLs.
    """
    
    def __init__(self, download_dir: str = PAPERS_DIR):
        """
        Initialize the PDF downloader.
        
        Args:
            download_dir: Directory to save downloaded PDFs
        """
        self.download_dir = download_dir
        ensure_directory(download_dir)
        
        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.session.headers.update({
            "User-Agent": "ResearchPaperReviewer/1.0"
        })
    
    def download_pdf(
        self,
        paper: PaperMetadata,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Download a PDF for a paper if available.
        
        Args:
            paper: PaperMetadata object with PDF URL
            filename: Optional custom filename (if None, generates from metadata)
            
        Returns:
            Path to downloaded PDF file, or None if download failed or no PDF available
        """
        pdf_url = paper.get_pdf_url()
        if not pdf_url:
            logger.debug(f"No open-access PDF available for: {paper.title}")
            return None
        
        # Generate filename if not provided
        if not filename:
            filename = generate_pdf_filename(
                paper.title,
                paper.authors,
                paper.year
            )
        
        filepath = os.path.join(self.download_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            logger.info(f"PDF already exists: {filename}")
            return filepath
        
        try:
            logger.info(f"Downloading PDF: {filename} from {pdf_url}")
            
            response = self.session.get(pdf_url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Verify it's actually a PDF
            content_type = response.headers.get("Content-Type", "").lower()
            if "pdf" not in content_type:
                # Check first bytes for PDF magic number
                first_bytes = response.content[:4]
                if first_bytes != b"%PDF":
                    logger.warning(
                        f"URL does not appear to be a PDF (Content-Type: {content_type})"
                    )
                    return None
            
            # Download and save
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(filepath)
            logger.info(f"Downloaded PDF: {filename} ({file_size:,} bytes)")
            
            # Respect rate limits
            time.sleep(REQUEST_DELAY_SECONDS)
            
            return filepath
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download PDF for {paper.title}: {e}")
            # Clean up partial file if it exists
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading PDF: {e}")
            return None
    
    def download_papers(self, papers: List[PaperMetadata]) -> dict:
        """
        Download PDFs for multiple papers.
        
        Args:
            papers: List of PaperMetadata objects
            
        Returns:
            Dictionary mapping paper IDs to download status:
            {
                "paper_id": {
                    "downloaded": bool,
                    "filepath": Optional[str],
                    "error": Optional[str]
                }
            }
        """
        results = {}
        
        for paper in papers:
            paper_id = paper.paperId
            result = {
                "downloaded": False,
                "filepath": None,
                "error": None
            }
            
            if paper.has_open_pdf():
                filepath = self.download_pdf(paper)
                if filepath:
                    result["downloaded"] = True
                    result["filepath"] = filepath
                else:
                    result["error"] = "Download failed or not a valid PDF"
            else:
                result["error"] = "No open-access PDF available"
            
            results[paper_id] = result
        
        downloaded_count = sum(1 for r in results.values() if r["downloaded"])
        logger.info(f"Downloaded {downloaded_count} out of {len(papers)} papers")
        
        return results

