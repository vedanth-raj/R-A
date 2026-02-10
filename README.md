# AI System to Automatically Review and Summarize Research Papers

## Milestone 1: Paper Search and Retrieval ✅

This milestone implements automated paper search, selection, and PDF download functionality using the Semantic Scholar API.

### ✨ Features

- **🔍 Automated Paper Search**: Search Semantic Scholar API for research papers by topic
- **🎯 Intelligent Selection**: Rank and select papers by relevance, citations, year, and open-access PDF availability
- **📥 PDF Download**: Automatically download open-access PDFs when available
- **💾 Metadata Storage**: Save structured paper metadata as JSON
- **🎲 Randomized Selection**: Get different papers each time with `--randomize` option
- **⚡ Rate Limiting**: Automatic 1 RPS rate limit enforcement for API key users

### 🚀 Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Set Up API Key (Optional but Recommended)

Create a `.env` file in the project root:

```bash
SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
```

**Why use an API key?**
- **Without API key**: Shared rate limit of 1000 requests/second (may be throttled)
- **With API key**: Dedicated rate limit of 1 request/second (more reliable)

See [API_KEY_SETUP.md](API_KEY_SETUP.md) for detailed instructions.

#### 3. Run the System

**Basic usage:**
```bash
python main.py "quantum machine learning"
```

**With custom number of papers:**
```bash
python main.py "large language models safety" --max-papers 5
```

**Get different papers each time (randomized):**
```bash
python main.py "machine learning" --randomize --diversity 0.5
```

### 📋 Command Line Options

```bash
python main.py <topic> [OPTIONS]

Arguments:
  topic                  Research topic to search for (required)

Options:
  --max-papers N         Maximum number of papers to select (default: 3, max: 20)
  --randomize            Randomly select papers from top-ranked results (for variety)
  --diversity FACTOR     Diversity factor (0.0-1.0) when using --randomize
                         - 0.0 = Only top papers (minimal variety)
                         - 0.3 = Top 30% of ranked papers (default, balanced)
                         - 0.5 = Top 50% of ranked papers (more variety)
                         - 1.0 = Entire list (maximum variety)
```

### 📊 Output

The system creates:

- **`./data/selected_papers.json`**: Structured metadata for selected papers
  - Title, authors, year, abstract
  - Citation count, paper ID
  - PDF availability and URLs
  
- **`./data/papers/`**: Directory containing downloaded PDF files
  - Filenames: `{author}{year}_{title}.pdf`

### 📖 View Papers

To view full paper details in the terminal:

```bash
python view_papers.py
```

This displays all papers from `selected_papers.json` with:
- Full title and abstract
- Complete author list
- Citation counts and publication year
- PDF availability status

### 🎯 Paper Selection Logic

Papers are ranked by:
1. **Open-Access PDF Availability** (prioritized)
2. **Citation Count** (higher is better)
3. **Publication Year** (recent papers preferred)
4. **Relevance** (from Semantic Scholar API)

### ⚙️ Configuration

Key settings in `config.py`:

- `DEFAULT_MAX_PAPERS = 3` - Default number of papers to select
- `INITIAL_SEARCH_LIMIT = 20` - Papers fetched for ranking
- `REQUEST_DELAY_SECONDS = 0.5` - Delay between API requests
- `MAX_PAPERS_UPPER_LIMIT = 20` - Maximum papers allowed

### 🔄 Rate Limits

**Semantic Scholar API:**
- **Without API key**: Shared 1000 requests/second (may be throttled during heavy use)
- **With API key**: 1 request/second (1 RPS) cumulative across all endpoints

The system automatically:
- Enforces rate limiting with request timing
- Retries with exponential backoff on rate limit errors (429)
- Tracks request timestamps for accurate rate limiting

### 🛠️ Error Handling

The system includes robust error handling for:
- API request failures (with retry and exponential backoff)
- PDF download failures
- Network timeouts
- Invalid responses
- Rate limit errors (automatic retry)

### 📁 Project Structure

```
.
├── main.py                      # Entry point (CLI)
├── config.py                    # Configuration constants
├── view_papers.py               # View saved papers in terminal
├── paper_retrieval/
│   ├── __init__.py
│   ├── searcher.py              # Semantic Scholar API search
│   ├── selector.py              # Paper ranking and selection
│   ├── downloader.py            # PDF download functionality
│   ├── models.py                # Pydantic data models
│   └── text_extractor.py        # Text extraction (later milestones)
├── utils/
│   ├── __init__.py
│   └── helpers.py               # Utility functions
├── data/
│   ├── papers/                  # Downloaded PDFs
│   └── selected_papers.json    # Paper metadata
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── PROJECT_STRUCTURE.md         # File responsibilities
├── API_KEY_SETUP.md             # API key setup guide
├── SETUP_API_KEY.md             # Quick API key setup
├── CREATE_ENV_FILE.md           # Create .env file guide
└── FEATURES.md                  # All features (beyond Milestone 1)
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed file responsibilities.

### 🧩 All Features (Beyond Milestone 1)

The project includes many more features beyond paper search and retrieval:

| Area | Features | Entry Points |
|------|----------|--------------|
| **Text extraction** | PDF text extraction, section detection | `paper_retrieval/text_extractor.py`, `section_extractor.py`, `section_wise_extractor.py` |
| **Section analysis** | Analyze sections, compare papers | `section_analyzer.py` |
| **Draft generation** | AI-generated section drafts (GPT/Gemini) | `gpt_draft_generator.py`, `enhanced_gpt_generator.py` |
| **Content review** | Quality metrics, revision suggestions, revision cycles | `content_reviewer.py` |
| **APA formatting** | APA bibliography and references | `apa_formatter.py` |
| **Full workflow** | End-to-end: load → generate → review → revise → report | `final_integration.py` |
| **Web UI (Flask)** | Search, extract, analyze, compare, download | `python start_web_interface.py` → http://localhost:5000 |
| **Gradio UI** | Tabs: Generation, Review, Final Report, APA | `gradio_interface.py`, `enhanced_gradio_interface.py` |
| **Unified CLI** | One entry for search, drafts, APA, workflow, tests, docs | `ai_research_agent.py` |
| **Testing & docs** | Test suite, user manual, technical docs, slides | `final_testing.py`, `final_documentation.py` |

**Quick commands:**

```bash
# Full CLI (search, drafts, APA, workflow, tests, docs)
python ai_research_agent.py --help

# Web interface (then open http://localhost:5000)
python start_web_interface.py

# Gradio interface
python gradio_interface.py

# Run tests
python final_testing.py
```

See **[FEATURES.md](FEATURES.md)** for a complete list of features, modules, and usage.

### 🔮 Next Steps (Future Milestones)

- **Milestone 2**: Text extraction from PDFs
- **Milestone 3**: Analysis and summarization
- **Milestone 4**: Review generation
- **Milestone 5**: LangGraph workflow integration
- **Milestone 6**: Gradio UI

### 📝 Examples

**Example 1: Basic search**
```bash
python main.py "neural networks"
```
Output: Top 3 papers about neural networks

**Example 2: More papers with randomization**
```bash
python main.py "deep learning" --max-papers 5 --randomize --diversity 0.4
```
Output: 5 randomly selected papers from top 40% of results

**Example 3: View saved papers**
```bash
python view_papers.py
```
Output: Full details of all saved papers

### 🐛 Troubleshooting

**Problem**: "No API key provided"
- **Solution**: Create `.env` file with `SEMANTIC_SCHOLAR_API_KEY=your_key`

**Problem**: Rate limit errors
- **Solution**: System automatically retries. If persistent, check API key rate limit (1 RPS)

**Problem**: No PDFs downloaded
- **Solution**: Some papers don't have open-access PDFs. Check `selected_papers.json` for PDF URLs.

**Problem**: Same papers every time
- **Solution**: Use `--randomize` flag to get different papers

### 📄 License

This project is part of an academic research system.

### 🤝 Contributing

This is Milestone 1 of a larger project. Code is modular and ready for integration with future milestones.
