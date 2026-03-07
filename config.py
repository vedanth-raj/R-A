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
INITIAL_SEARCH_LIMIT = 20  # Reduced from 100 for faster initial search
# Rate limiting: With API key = 1 RPS (cumulative across all endpoints)
# Must be >= 1.0 to respect rate limit. Using 1.1 for safety margin.
REQUEST_DELAY_SECONDS = 0.5  # Reduced from 1.1 for faster response
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
# Use /tmp for App Engine (writable), fallback to ./data for local
# GAE_ENV=standard on App Engine; K_SERVICE set on Cloud Run
IS_APP_ENGINE = (
    os.getenv('GAE_ENV', '').startswith('standard') or
    bool(os.getenv('K_SERVICE'))
)
if IS_APP_ENGINE:
    DATA_DIR = "/tmp/data"
else:
    DATA_DIR = "./data"

PAPERS_DIR = os.path.join(DATA_DIR, "papers")
EXTRACTED_TEXTS_DIR = os.path.join(DATA_DIR, "extracted_texts")
SECTIONS_DIR = os.path.join(DATA_DIR, "sections")
SECTION_ANALYSIS_DIR = os.path.join(DATA_DIR, "section_analysis")
DRAFTS_DIR = os.path.join(DATA_DIR, "drafts")
METADATA_FILE = os.path.join(DATA_DIR, "selected_papers.json")

# Optional API key for higher rate limits
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

# Gemini model - use gemini-2.5-flash (current); requires google-genai package
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

