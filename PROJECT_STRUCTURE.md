# Project Structure & File Responsibilities

This document explains what each file in the project is responsible for.

## 📁 Root Level Files

### `main.py` - **Entry Point & Orchestration**
**Responsibility**: Main CLI application that coordinates the entire workflow

**What it does**:
- Parses command-line arguments (topic, max-papers)
- Orchestrates the 4-step workflow:
  1. **Search** → Calls `SemanticScholarSearcher` to find papers
  2. **Select** → Calls `PaperSelector` to rank and choose top papers
  3. **Download** → Calls `PDFDownloader` to get PDFs
  4. **Save** → Saves metadata to JSON file
- Handles user input validation
- Provides console output and progress updates
- Error handling and graceful exit

**Key Functions**:
- `main()` - Entry point, argument parsing, workflow orchestration
- `save_metadata()` - Converts paper objects to JSON and saves to file

---

### `config.py` - **Configuration & Constants**
**Responsibility**: Central configuration file with all system settings

**What it does**:
- Defines Semantic Scholar API endpoints and URLs
- Sets rate limiting parameters (1.1 seconds for 1 RPS limit)
- Configures API request settings (retries, timeouts, delays)
- Defines paper selection limits (default: 3, max: 20)
- Specifies which fields to request from API
- Sets data storage paths (`./data/papers/`, `./data/selected_papers.json`)
- Loads environment variables (including API key from `.env`)

**Key Constants**:
- `SEMANTIC_SCHOLAR_SEARCH_ENDPOINT` - API endpoint URL
- `SEMANTIC_SCHOLAR_FIELDS` - Fields to request (title, authors, year, etc.)
- `REQUEST_DELAY_SECONDS` - Rate limiting delay (1.1 seconds)
- `DEFAULT_MAX_PAPERS` - Default number of papers to select (3)

---

### `requirements.txt` - **Dependencies**
**Responsibility**: Lists all Python packages needed for the project

**What it contains**:
- Core dependencies: `requests`, `pydantic`, `tqdm`
- LangChain ecosystem: `langchain`, `langgraph`, `langsmith` (for future milestones)
- Other libraries: `openai`, `huggingface-hub`, `gradio`, `pymupdf4llm`, etc.

---

### `README.md` - **User Documentation**
**Responsibility**: User-facing documentation with setup and usage instructions

---

### `API_KEY_SETUP.md` - **API Key Guide**
**Responsibility**: Detailed instructions for obtaining and configuring Semantic Scholar API key

---

### `SETUP_API_KEY.md` - **Quick Setup Guide**
**Responsibility**: Quick reference for setting up the API key

---

### `.gitignore` - **Version Control**
**Responsibility**: Prevents sensitive files (like `.env` with API keys) from being committed to git

---

## 📁 `paper_retrieval/` Module - Core Business Logic

### `paper_retrieval/searcher.py` - **API Search & Communication**
**Responsibility**: Handles all communication with Semantic Scholar API

**What it does**:
- Makes HTTP requests to Semantic Scholar API
- Implements rate limiting (1 RPS enforcement)
- Handles pagination to fetch multiple pages of results
- Manages API authentication (API key in headers)
- Retry logic with exponential backoff for failed requests
- Parses API responses into `PaperMetadata` objects

**Key Classes**:
- `SemanticScholarSearcher` - Main search class

**Key Methods**:
- `search_papers()` - Single API request with rate limiting
- `search_papers_paginated()` - Fetches multiple pages automatically

**Rate Limiting Logic**:
- Tracks `last_request_time` to enforce 1 RPS limit
- Waits if needed before making requests
- Updates timestamp after request completes

---

### `paper_retrieval/selector.py` - **Paper Ranking & Selection**
**Responsibility**: Intelligent ranking and selection of papers

**What it does**:
- Ranks papers by multiple criteria:
  1. **Open-access PDF availability** (prioritized)
  2. **Citation count** (higher is better)
  3. **Publication year** (recent papers preferred)
- Selects top N papers based on ranking
- Maintains relevance order from API while refining by other factors

**Key Classes**:
- `PaperSelector` - Selection and ranking logic

**Key Methods**:
- `rank_papers()` - Sorts papers by quality metrics
- `select_papers()` - Selects top N papers from ranked list

**Selection Algorithm**:
```python
Sort by: (-has_pdf, -citation_count, -year)
# Papers with PDFs come first, then by citations, then by year
```

---

### `paper_retrieval/downloader.py` - **PDF Download**
**Responsibility**: Downloads open-access PDFs from URLs

**What it does**:
- Downloads PDFs from `openAccessPdf.url` if available
- Generates safe filenames: `{author}{year}_{title}.pdf`
- Validates downloaded files (checks PDF magic bytes)
- Skips already-downloaded files
- Handles download errors gracefully
- Respects rate limits with delays

**Key Classes**:
- `PDFDownloader` - PDF download handler

**Key Methods**:
- `download_pdf()` - Downloads single PDF
- `download_papers()` - Downloads PDFs for multiple papers

**Filename Format**:
- `{first_author_lastname}{year}_{sanitized_title[:50]}.pdf`
- Example: `Smith2023_Quantum_Machine_Learning_Approaches.pdf`

---

### `paper_retrieval/models.py` - **Data Models**
**Responsibility**: Pydantic models for type-safe data structures

**What it does**:
- Defines data structures matching Semantic Scholar API responses
- Provides type validation and serialization
- Helper methods for checking PDF availability

**Key Classes**:
- `Author` - Author information (name, authorId)
- `OpenAccessPdf` - PDF URL and status
- `PaperMetadata` - Complete paper information
- `SemanticScholarSearchResponse` - API response wrapper

**Key Methods** (in `PaperMetadata`):
- `has_open_pdf()` - Checks if PDF is available
- `get_pdf_url()` - Returns PDF URL if available

---

## 📁 `utils/` Module - Utilities

### `utils/helpers.py` - **Utility Functions**
**Responsibility**: Reusable helper functions

**What it does**:
- **Filename sanitization**: Converts text to safe filenames
  - Removes invalid characters (`< > : " / \ | ? *`)
  - Handles Windows filename restrictions
  - Truncates to max length
- **Author name extraction**: Gets last name from author list
- **PDF filename generation**: Creates safe filenames from metadata
- **Directory creation**: Ensures directories exist before use
- **Logging configuration**: Sets up logging format

**Key Functions**:
- `sanitize_filename()` - Makes strings filename-safe
- `get_first_author_lastname()` - Extracts author last name
- `generate_pdf_filename()` - Creates PDF filename from paper metadata
- `ensure_directory()` - Creates directory if missing

---

## 🔄 Workflow: How Files Work Together

```
1. User runs: python main.py "quantum computing"
   ↓
2. main.py parses arguments and calls:
   ↓
3. SemanticScholarSearcher.search_papers_paginated()
   → Uses config.py for API endpoint and settings
   → Returns List[PaperMetadata] from models.py
   ↓
4. PaperSelector.select_papers()
   → Ranks papers by PDF availability, citations, year
   → Returns top N papers
   ↓
5. PDFDownloader.download_papers()
   → Uses utils/helpers.py for filename generation
   → Downloads PDFs to ./data/papers/
   ↓
6. main.py.save_metadata()
   → Converts PaperMetadata objects to JSON
   → Saves to ./data/selected_papers.json
```

---

## 📊 Data Flow

```
Semantic Scholar API
    ↓ (JSON response)
searcher.py → PaperMetadata objects
    ↓
selector.py → Ranked PaperMetadata objects
    ↓
downloader.py → PDF files + metadata
    ↓
main.py → JSON file + PDF files in ./data/
```

---

## 🔑 Key Design Patterns

1. **Separation of Concerns**: Each file has a single, clear responsibility
2. **Modularity**: Components can be used independently
3. **Type Safety**: Pydantic models ensure data integrity
4. **Error Handling**: Retry logic and graceful failures
5. **Rate Limiting**: Built into searcher to respect API limits
6. **Configuration**: Centralized in `config.py` for easy changes

---

## 🎯 Future Milestone Integration Points

These files are designed to integrate with future milestones:

- **`searcher.py`** → Will become a LangGraph node: `"search_papers"`
- **`selector.py`** → Will become a LangGraph node: `"select_papers"`
- **`downloader.py`** → Will become a LangGraph node: `"download_pdfs"`
- **`main.py`** → Will be replaced by LangGraph workflow orchestration

