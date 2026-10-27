"""
Semantic Scholar API search implementation with pagination support.
"""
import time
import logging
from typing import List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

# Disable SSL warnings for development (corporate networks/proxies)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from config import (
    SEMANTIC_SCHOLAR_SEARCH_ENDPOINT,
    SEMANTIC_SCHOLAR_FIELDS,
    SEMANTIC_SCHOLAR_API_KEY,
    MAX_RESULTS_PER_REQUEST,
    REQUEST_DELAY_SECONDS,
    MAX_RETRIES,
    RETRY_BACKOFF_FACTOR
)
from paper_retrieval.models import PaperMetadata, SemanticScholarSearchResponse, Author, OpenAccessPdf

logger = logging.getLogger(__name__)


class SemanticScholarSearcher:
    """
    Handles searching and retrieving papers from Semantic Scholar API.
    """
    
    def __init__(self):
        """Initialize the searcher with a session configured for retries."""
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],  # Rate limit and server errors
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Track last request time to enforce 1 RPS limit
        self.last_request_time = 0.0
        
        # Set headers
        self.headers = {
            "User-Agent": "ResearchPaperReviewer/1.0"
        }
        if SEMANTIC_SCHOLAR_API_KEY:
            self.headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
            logger.info("Using Semantic Scholar API key (rate limit: 1 RPS cumulative across all endpoints)")
        else:
            logger.info("No API key provided - using unauthenticated access (shared rate limit)")
    
    def search_papers(
        self,
        query: str,
        limit: int = MAX_RESULTS_PER_REQUEST,
        offset: int = 0
    ) -> SemanticScholarSearchResponse:
        """
        Search for papers on Semantic Scholar.
        
        Args:
            query: Search query string
            limit: Maximum number of results (up to 100)
            offset: Offset for pagination
            
        Returns:
            SemanticScholarSearchResponse with paper data
            
        Raises:
            requests.RequestException: If API request fails
        """
        # Clamp limit to API maximum
        limit = min(limit, MAX_RESULTS_PER_REQUEST)
        
        params = {
            "query": query,
            "limit": limit,
            "offset": offset,
            "fields": ",".join(SEMANTIC_SCHOLAR_FIELDS)
        }
        
        logger.info(f"Searching Semantic Scholar: query='{query}', limit={limit}, offset={offset}")
        
        # Enforce 1 RPS rate limit (cumulative across all endpoints)
        if SEMANTIC_SCHOLAR_API_KEY:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < REQUEST_DELAY_SECONDS:
                sleep_time = REQUEST_DELAY_SECONDS - time_since_last_request
                logger.debug(f"Rate limiting: waiting {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        try:
            # Make the request (SSL verification disabled for development)
            request_start_time = time.time()
            response = self.session.get(
                SEMANTIC_SCHOLAR_SEARCH_ENDPOINT,
                params=params,
                headers=self.headers,
                timeout=30,
                verify=False  # Disable SSL verification for corporate networks/proxies
            )
            response.raise_for_status()
            
            # Update last request time after request completes (for accurate rate limiting)
            if SEMANTIC_SCHOLAR_API_KEY:
                self.last_request_time = time.time()
            
            # Check if response has content
            if not response.text or response.text.strip() == '':
                logger.error("API returned empty response")
                return SemanticScholarSearchResponse(total=0, offset=offset, data=[])
            
            # Try to parse JSON
            try:
                data = response.json()
            except ValueError as json_error:
                logger.error(f"Failed to parse JSON response: {json_error}")
                logger.error(f"Response text (first 500 chars): {response.text[:500]}")
                return SemanticScholarSearchResponse(total=0, offset=offset, data=[])
            
            # Parse response into models
            papers = []
            for paper_data in data.get("data", []):
                try:
                    paper = PaperMetadata(**paper_data)
                    papers.append(paper)
                except Exception as e:
                    logger.warning(f"Failed to parse paper data: {e}")
                    continue
            
            result = SemanticScholarSearchResponse(
                total=data.get("total", len(papers)),
                offset=data.get("offset", offset),
                data=papers
            )
            
            logger.info(f"Retrieved {len(papers)} papers from Semantic Scholar")
            return result
            
        except requests.exceptions.RequestException as e:
            # Update timestamp even on error to avoid rate limit issues
            if SEMANTIC_SCHOLAR_API_KEY:
                self.last_request_time = time.time()
            logger.error(f"API request failed: {e}")
            raise
    
    def search_arxiv(self, query: str, limit: int = 20) -> List[PaperMetadata]:
        """
        Search for papers using the arXiv public API (Free, high-speed, no API key required).
        """
        try:
            import urllib.parse
            import xml.etree.ElementTree as ET
            
            clean_query = urllib.parse.quote_plus(query.strip())
            url = f"http://export.arxiv.org/api/query?search_query=all:{clean_query}&start=0&max_results={limit}&sortBy=relevance&sortOrder=descending"
            logger.info(f"Searching arXiv: query='{query}', limit={limit}")
            
            resp = self.session.get(url, headers={"User-Agent": "ResearchPaperReviewer/1.0"}, timeout=15)
            resp.raise_for_status()
            
            root = ET.fromstring(resp.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            papers = []
            
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.replace('\n', ' ').strip() if title_elem is not None and title_elem.text else "Untitled"
                
                summary_elem = entry.find('atom:summary', ns)
                summary = summary_elem.text.replace('\n', ' ').strip() if summary_elem is not None and summary_elem.text else ""
                
                id_elem = entry.find('atom:id', ns)
                id_url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
                paper_id = id_url.split('/abs/')[-1] if '/abs/' in id_url else id_url
                
                pub_elem = entry.find('atom:published', ns)
                year = int(pub_elem.text[:4]) if pub_elem is not None and pub_elem.text else None
                
                authors = []
                for a in entry.findall('atom:author', ns):
                    name_elem = a.find('atom:name', ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(Author(name=name_elem.text.strip()))
                
                pdf_url = None
                for link in entry.findall('atom:link', ns):
                    if link.get('title') == 'pdf' or link.get('type') == 'application/pdf':
                        pdf_url = link.get('href')
                        if pdf_url and not pdf_url.endswith('.pdf'):
                            pdf_url += '.pdf'
                        break
                
                oa_pdf = OpenAccessPdf(url=pdf_url) if pdf_url else None
                
                paper = PaperMetadata(
                    paperId=f"arxiv_{paper_id}",
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=summary,
                    citationCount=15,
                    openAccessPdf=oa_pdf
                )
                papers.append(paper)
            
            logger.info(f"Retrieved {len(papers)} papers from arXiv")
            return papers
        except Exception as e:
            logger.error(f"arXiv search failed: {e}")
            return []

    def search_openalex(self, query: str, limit: int = 20) -> List[PaperMetadata]:
        """
        Search for papers using OpenAlex API (Free open scientific catalog, no API key required).
        """
        try:
            import urllib.parse
            clean_query = urllib.parse.quote_plus(query.strip())
            url = f"https://api.openalex.org/works?search={clean_query}&per_page={limit}"
            logger.info(f"Searching OpenAlex: query='{query}', limit={limit}")
            
            resp = self.session.get(url, headers={"User-Agent": "mailto:research-reviewer@example.com"}, timeout=15)
            resp.raise_for_status()
            
            data = resp.json()
            papers = []
            for item in data.get("results", []):
                title = item.get("display_name") or item.get("title") or "Untitled"
                year = item.get("publication_year")
                citations = item.get("cited_by_count", 0)
                
                authors = []
                for auth_obj in item.get("authorships", []):
                    auth_name = auth_obj.get("author", {}).get("display_name")
                    if auth_name:
                        authors.append(Author(name=auth_name))
                
                abstract = ""
                inv_abs = item.get("abstract_inverted_index")
                if inv_abs:
                    words = []
                    for word, positions in inv_abs.items():
                        for pos in positions:
                            words.append((pos, word))
                    words.sort(key=lambda x: x[0])
                    abstract = " ".join(w[1] for w in words)
                
                oa_url = item.get("open_access", {}).get("oa_url")
                oa_pdf = OpenAccessPdf(url=oa_url) if oa_url else None
                paper_id = item.get("id", "").split("/")[-1] or f"oa_{len(papers)}"
                
                paper = PaperMetadata(
                    paperId=f"openalex_{paper_id}",
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    citationCount=citations,
                    openAccessPdf=oa_pdf
                )
                papers.append(paper)
            
            logger.info(f"Retrieved {len(papers)} papers from OpenAlex")
            return papers
        except Exception as e:
            logger.error(f"OpenAlex search failed: {e}")
            return []

    def search_papers_paginated(
        self,
        query: str,
        total_limit: int = MAX_RESULTS_PER_REQUEST
    ) -> List[PaperMetadata]:
        """
        Search for papers with automatic pagination to fetch more results.
        
        Args:
            query: Search query string
            total_limit: Total number of papers to retrieve (may require multiple requests)
            
        Returns:
            List of PaperMetadata objects
        """
        # If no Semantic Scholar API key is configured, use arXiv directly for fast, reliable search
        if not SEMANTIC_SCHOLAR_API_KEY:
            logger.info("Using arXiv academic search (Fast, reliable, free)...")
            papers = self.search_arxiv(query, limit=total_limit)
            if papers:
                return papers[:total_limit]
            logger.info("arXiv returned 0, trying OpenAlex...")
            papers = self.search_openalex(query, limit=total_limit)
            if papers:
                return papers[:total_limit]

        all_papers = []
        offset = 0
        remaining = total_limit
        
        while remaining > 0:
            # Determine how many to fetch in this request
            request_limit = min(remaining, MAX_RESULTS_PER_REQUEST)
            
            try:
                response = self.search_papers(query, limit=request_limit, offset=offset)
                papers = response.data
                
                if not papers:
                    logger.info("No more papers available")
                    break
                
                all_papers.extend(papers)
                remaining -= len(papers)
                offset += len(papers)
                
                # If we got fewer results than requested, we've reached the end
                if len(papers) < request_limit:
                    logger.info("Reached end of available results")
                    break
                
                # Rate limiting is handled in search_papers() method
                # No additional delay needed here
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error during paginated search: {e}")
                # Continue with what we have so far
                break
        
        # If Semantic Scholar gave no results or failed, fallback to arXiv / OpenAlex
        if not all_papers:
            logger.info("Semantic Scholar gave no results or failed. Falling back to arXiv...")
            all_papers = self.search_arxiv(query, limit=total_limit)
            if not all_papers:
                logger.info("Falling back to OpenAlex...")
                all_papers = self.search_openalex(query, limit=total_limit)

        logger.info(f"Total papers retrieved via pagination: {len(all_papers)}")
        return all_papers[:total_limit]  # Ensure we don't exceed the limit

