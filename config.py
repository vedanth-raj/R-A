"""
Configuration constants for the paper retrieval system.
"""
import os
from typing import List

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    from pathlib import Path
    # Load .env from the same directory as this config file
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not installed, skip
except Exception:
    pass  # If .env file doesn't exist, continue without it

# Semantic Scholar API configuration
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1"
SEMANTIC_SCHOLAR_SEARCH_ENDPOINT = f"{SEMANTIC_SCHOLAR_BASE_URL}/paper/search"

# API request settings
MAX_RESULTS_PER_REQUEST = 100  # Semantic Scholar limit
INITIAL_SEARCH_LIMIT = 100  # Fetch this many papers initially for ranking
# Rate limiting: With API key = 1 RPS (cumulative across all endpoints)
# Must be >= 1.0 to respect rate limit. Using 1.1 for safety margin.
REQUEST_DELAY_SECONDS = 1.1  # Delay between API requests (must be >= 1.0 for 1 RPS limit)
MAX_RETRIES = 3  # Maximum retry attempts for API calls
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff multiplier

# Paper selection settings
DEFAULT_MAX_PAPERS = 3
MAX_PAPERS_UPPER_LIMIT = 20  # Safety limit

# Fields to request from Semantic Scholar API
SEMANTIC_SCHOLAR_FIELDS: List[str] = [
    "title",
    "authors",
    "year",
    "abstract",
    "paperId",
    "citationCount",
    "openAccessPdf"
]

# Data storage paths
DATA_DIR = "./data"
PAPERS_DIR = os.path.join(DATA_DIR, "papers")
METADATA_FILE = os.path.join(DATA_DIR, "selected_papers.json")

# Optional API key for higher rate limits
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

