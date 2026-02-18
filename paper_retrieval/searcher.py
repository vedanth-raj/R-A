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
from paper_retrieval.models import PaperMetadata, SemanticScholarSearchResponse

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
        
        logger.info(f"Total papers retrieved via pagination: {len(all_papers)}")
        return all_papers[:total_limit]  # Ensure we don't exceed the limit

