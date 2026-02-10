# Project Structure & File Responsibilities

This document explains what each file in the project is responsible for.

---

## Root Level Files

### `main.py` – **Entry Point & Orchestration**
**Responsibility:** Main CLI application that coordinates the paper retrieval workflow.

**What it does:**
- Parses command-line arguments (`topic`, `--max-papers`, `--randomize`, `--diversity`)
- Orchestrates the 4-step workflow:
  1. **Search** → Calls `SemanticScholarSearcher` to find papers
  2. **Select** → Calls `PaperSelector` to rank and choose top papers
  3. **Download** → Calls `PDFDownloader` to get PDFs
  4. **Save** → Saves metadata to JSON file
- Validates user input and prints progress
- Handles errors and exits cleanly

**Key functions:**
- `main()` – Entry point, argument parsing, workflow orchestration
- `save_metadata()` – Converts paper objects to JSON and writes to file

---

### `config.py` – **Configuration & Constants**
**Responsibility:** Central configuration for the paper retrieval system.

**What it does:**
- Defines Semantic Scholar API base URL and search endpoint
- Sets rate limiting (e.g. `REQUEST_DELAY_SECONDS` for 1 RPS with API key)
- Configures API request settings (retries, timeouts, delays)
- Defines paper selection limits (`DEFAULT_MAX_PAPERS`, `MAX_PAPERS_UPPER_LIMIT`)
- Lists fields requested from the API
- Defines data paths (`DATA_DIR`, `PAPERS_DIR`, `METADATA_FILE`)
- Loads environment variables (including API key from `.env`)

**Key constants:**
- `SEMANTIC_SCHOLAR_SEARCH_ENDPOINT` – API endpoint URL
- `SEMANTIC_SCHOLAR_FIELDS` – Fields to request (title, authors, year, etc.)
- `REQUEST_DELAY_SECONDS` – Delay between API requests
- `DEFAULT_MAX_PAPERS` – Default number of papers to select (3)

---

### `view_papers.py` – **View Saved Papers**
**Responsibility:** Displays full paper details from `selected_papers.json` in the terminal.

**What it does:**
- Reads `data/selected_papers.json`
- Prints each paper’s title, authors, year, citations, paper ID, abstract, and PDF status
- Word-wraps long text for readability
- Uses ASCII-only labels (e.g. `[TITLE]`, `[ABSTRACT]`) for Windows compatibility

**Usage:** `python view_papers.py`

---

### `requirements.txt` – **Dependencies**
**Responsibility:** Lists Python packages required for the project.

---

## `paper_retrieval/` Module

### `paper_retrieval/searcher.py` – **API Search**
**Responsibility:** All communication with the Semantic Scholar API.

**What it does:**
- Sends HTTP GET requests to the Semantic Scholar search endpoint
- Enforces 1 RPS rate limiting when an API key is set
- Supports pagination to fetch multiple pages of results
- Sends API key in `x-api-key` header when available
- Retries failed requests with exponential backoff
- Parses API responses into `PaperMetadata` objects

**Key class:** `SemanticScholarSearcher`

**Key methods:**
- `search_papers()` – Single API request with rate limiting
- `search_papers_paginated()` – Fetches multiple pages automatically

---

### `paper_retrieval/selector.py` – **Paper Ranking & Selection**
**Responsibility:** Ranking and selecting papers from search results.

**What it does:**
- Ranks papers by:
  1. Open-access PDF availability (prioritized)
  2. Citation count (higher is better)
  3. Publication year (recent preferred)
- Selects top N papers by default
- Optional **randomized selection** (`randomize=True`) for variety
- `diversity_factor` (0.0–1.0) controls how wide the selection pool is

**Key class:** `PaperSelector`

**Key methods:**
- `rank_papers()` – Sorts papers by quality metrics
- `select_papers()` – Returns top N papers, with optional randomization

---

### `paper_retrieval/downloader.py` – **PDF Download**
**Responsibility:** Downloading open-access PDFs.

**What it does:**
- Downloads PDFs from `openAccessPdf.url` when present
- Generates safe filenames: `{author}{year}_{title}.pdf`
- Validates downloaded content (e.g. PDF magic bytes)
- Skips files that already exist
- Handles errors and applies delays between requests

**Key class:** `PDFDownloader`

**Key methods:**
- `download_pdf()` – Downloads a single PDF
- `download_papers()` – Downloads PDFs for a list of papers

---

### `paper_retrieval/models.py` – **Data Models**
**Responsibility:** Pydantic models for type-safe paper metadata.

**What it does:**
- Defines structures that match Semantic Scholar API responses
- Validates and serializes paper data
- Provides helpers for PDF availability

**Key classes:**
- `Author` – Author name and ID
- `OpenAccessPdf` – PDF URL and status
- `PaperMetadata` – Full paper metadata
- `SemanticScholarSearchResponse` – API response wrapper

**Key methods (on `PaperMetadata`):**
- `has_open_pdf()` – Whether an open-access PDF is available
- `get_pdf_url()` – Returns PDF URL if available

---

### `paper_retrieval/text_extractor.py` – **Text Extraction** (later milestones)
**Responsibility:** Extracting text from PDFs for analysis (used in later milestones).

---

## `utils/` Module

### `utils/helpers.py` – **Utility Functions**
**Responsibility:** Reusable helpers for filenames, authors, and paths.

**What it does:**
- **Filename sanitization** – Converts text to safe filenames (removes invalid chars, truncates)
- **Author name extraction** – Gets last name from author list (supports Pydantic models and dicts)
- **PDF filename generation** – Builds safe filenames from paper metadata
- **Directory creation** – Ensures directories exist
- **Logging** – Configures log format

**Key functions:**
- `sanitize_filename()` – Makes strings safe for filenames
- `get_first_author_lastname()` – First author’s last name
- `generate_pdf_filename()` – Filename from title, authors, year
- `ensure_directory()` – Creates directory if missing

---

## Workflow: How Files Work Together

```
1. User runs: python main.py "quantum computing"
   ↓
2. main.py parses arguments and calls:
   ↓
3. SemanticScholarSearcher.search_papers_paginated()
   → Uses config.py for endpoint and settings
   → Returns List[PaperMetadata]
   ↓
4. PaperSelector.select_papers()
   → Ranks by PDF, citations, year
   → Optionally randomizes (--randomize, --diversity)
   → Returns top N papers
   ↓
5. PDFDownloader.download_papers()
   → Uses utils/helpers.py for filenames
   → Writes PDFs to ./data/papers/
   ↓
6. main.save_metadata()
   → Converts PaperMetadata to JSON
   → Writes ./data/selected_papers.json
```

---

## Data Flow

```
Semantic Scholar API (JSON)
    ↓
searcher.py → List[PaperMetadata]
    ↓
selector.py → Ranked & selected papers
    ↓
downloader.py → PDF files + metadata
    ↓
main.py → data/selected_papers.json + data/papers/
```

---

## Other Feature Modules (Beyond Milestone 1)

| File | Responsibility |
|------|----------------|
| **advanced_text_processor.py** | Text quality metrics, citation extraction, summaries |
| **apa_formatter.py** | APA bibliography and reference formatting |
| **content_reviewer.py** | Quality review, revision suggestions, revision cycles |
| **enhanced_gpt_generator.py** | AI draft generation (GPT/Gemini) from section analysis |
| **gpt_draft_generator.py** | GPT-based draft generation |
| **section_analyzer.py** | Analyze extracted sections, generate reports |
| **section_extractor.py** | Extract sections from PDFs (SectionWiseExtractor) |
| **section_wise_extractor.py** | Process PDFs for sections, compare papers |
| **final_integration.py** | End-to-end workflow (drafts → review → revise → report) |
| **final_testing.py** | Comprehensive test suite |
| **final_documentation.py** | Generate user manual, technical docs, slides |
| **error_handler.py** | Custom exceptions, retry, safe_execute |
| **performance_monitor.py** | Performance metrics and reporting |
| **web_app.py** | Flask web UI (search, extract, analyze, compare) |
| **start_web_interface.py** | Launcher for web app |
| **gradio_interface.py** | Gradio UI (tabs: Generation, Review, Report, APA) |
| **enhanced_gradio_interface.py** | Enhanced Gradio UI |
| **lab_pulse_interface.py** | Lab Pulse–style Gradio UI |
| **ai_research_agent.py** | Unified CLI for all features |

See **[FEATURES.md](FEATURES.md)** for full feature list and usage.

---

## Future Integration (LangGraph)

- `searcher.py` → Node: `"search_papers"`
- `selector.py` → Node: `"select_papers"`
- `downloader.py` → Node: `"download_pdfs"`
- `main.py` → Replaced or extended by LangGraph workflow
