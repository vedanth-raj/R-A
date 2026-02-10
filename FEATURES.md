# AI Research Agent – All Features

This document lists all features in the project beyond Milestone 1 (paper search and retrieval).

---

## Milestone 1: Paper Search & Retrieval (CLI)

**Entry point:** `main.py`

| Feature | Description |
|--------|-------------|
| **Semantic Scholar search** | Search papers by topic via Semantic Scholar API |
| **Paper selection** | Rank by PDF availability, citations, year; optional `--randomize` |
| **PDF download** | Download open-access PDFs to `data/papers/` |
| **Metadata storage** | Save paper metadata to `data/selected_papers.json` |
| **View papers (CLI)** | `view_papers.py` – show full paper details in terminal |

**Usage:** `python main.py "topic" [--max-papers N] [--randomize] [--diversity FACTOR]`

---

## Text Extraction & Section Analysis

**Modules:** `paper_retrieval/text_extractor.py`, `section_extractor.py`, `section_wise_extractor.py`, `section_analyzer.py`

| Feature | Description |
|--------|-------------|
| **PDF text extraction** | Extract full text and metadata from PDFs (PyMuPDF) |
| **Section extraction** | Detect and extract sections (Abstract, Introduction, Methods, etc.) |
| **Section-wise processing** | Process all PDFs in a directory and save section data |
| **Section analysis** | Analyze extracted sections and generate per-paper reports |
| **Compare papers** | Compare section content across papers |

**Output:** `data/extracted_texts/`, `data/section_analysis/`

---

## Advanced Text Processing

**Module:** `advanced_text_processor.py`

| Feature | Description |
|--------|-------------|
| **Text quality metrics** | Analyze readability, structure, and quality |
| **Citation extraction** | Extract in-text citations from content |
| **Paper summary** | Generate short summaries (e.g. max N sentences) |
| **Comprehensive analysis** | Combined text analysis (quality, citations, summary) |

---

## Draft Generation (AI)

**Modules:** `gpt_draft_generator.py`, `enhanced_gpt_generator.py`

| Feature | Description |
|--------|-------------|
| **Section drafts** | Generate draft text for each section (Introduction, Methods, etc.) |
| **Complete draft** | Generate full draft from section analysis data |
| **Multiple providers** | OpenAI (GPT) and Gemini support; configurable preferred provider |
| **Mock fallback** | Offline/testing mode when API is unavailable |

**Input:** `data/section_analysis/`  
**Output:** Draft sections / full draft

---

## Content Review & Revision

**Module:** `content_reviewer.py`

| Feature | Description |
|--------|-------------|
| **Quality metrics** | Clarity, coherence, academic tone, completeness, citation quality |
| **Revision suggestions** | AI-generated suggestions (low/medium/high severity) |
| **Revision cycle** | Apply suggestions and re-review (configurable iterations) |
| **Quality scoring** | 0.0–1.0 scale with weighted metrics |

---

## APA Formatting

**Module:** `apa_formatter.py`

| Feature | Description |
|--------|-------------|
| **APA bibliography** | Generate APA-formatted bibliography from papers file |
| **Paper references** | Format references for selected papers and write to output dir |

**Input:** `data/selected_papers.json` (or similar)  
**Output:** APA-formatted references / bibliography files

---

## Final Integration (End-to-End Workflow)

**Module:** `final_integration.py`

| Feature | Description |
|--------|-------------|
| **Complete workflow** | Load analysis → generate drafts → review → revise → final report |
| **Quality thresholds** | Optional acceptance/rejection by quality score |
| **Revision cycles** | Configurable max revision iterations |
| **Result aggregation** | Collect and store workflow results |

**Usage:** `FinalIntegration().complete_workflow(topic, max_papers, enable_revision, max_revision_iterations)`  
**Helper:** `run_complete_workflow()` in same module

---

## Web Interface (Flask)

**Modules:** `web_app.py`, `start_web_interface.py`

| Feature | Description |
|--------|-------------|
| **Search papers** | Trigger paper search from the web UI (calls `main.py`) |
| **Extract text** | Extract text from downloaded PDFs |
| **View papers** | List and view extracted papers and metadata |
| **Analyze paper** | Run section analysis on a selected paper |
| **Compare papers** | Compare content across papers |
| **Download paper** | Download PDFs from the UI |
| **Real-time updates** | SocketIO for progress and status |

**Start:** `python start_web_interface.py` or run `web_app.py` (Flask app)  
**URL:** http://localhost:5000

---

## Gradio Interfaces

**Modules:** `gradio_interface.py`, `enhanced_gradio_interface.py`, `lab_pulse_interface.py`

| Feature | Description |
|--------|-------------|
| **Gradio UI** | Tab-based UI: Generation, Review & Refine, Final Report, APA References |
| **Enhanced Gradio** | Extended UI with more options and polish |
| **Lab Pulse style** | Alternative Gradio theme/layout |

**Usage:** `python gradio_interface.py` or `python enhanced_gradio_interface.py`

---

## AI Research Agent (Unified CLI)

**Module:** `ai_research_agent.py`

| Feature | Description |
|--------|-------------|
| **Unified CLI** | Single entry point for search, extract, analyze, generate, format |
| **Search papers** | `--topic "..." --max-papers N` (delegates to `main.py`) |
| **Generate drafts** | `--generate-drafts` from section analysis |
| **Format APA** | `--format-apa` for references/bibliography |
| **Complete workflow** | `--complete-workflow "topic"` (search → extract → analyze → generate → review) |
| **Review content** | `--review-content` for quality review |
| **Test system** | `--test-system` runs comprehensive tests |
| **Generate docs** | `--generate-docs` for documentation |
| **Launch Gradio** | `--gradio-interface` to start Gradio UI |

**Usage:** `python ai_research_agent.py --help`

---

## Error Handling & Performance

**Modules:** `error_handler.py`, `performance_monitor.py`

| Feature | Description |
|--------|-------------|
| **Structured errors** | Custom exceptions (e.g. TextExtractionError, AnalysisError) |
| **Error context** | Capture context and severity for logging/reporting |
| **Retry with backoff** | `retry_with_backoff()` for transient failures |
| **Safe execute** | `safe_execute()` wrapper with default return on error |
| **Performance metrics** | Track timing and resource usage per operation |
| **Performance report** | Save summary to JSON (e.g. `performance_report.json`) |

---

## Testing & Documentation

**Modules:** `final_testing.py`, `final_documentation.py`

| Feature | Description |
|--------|-------------|
| **Test suite** | Component init, generation, review, revision, APA, integration, performance, errors |
| **Test reporting** | Summarized results and recommendations |
| **Documentation generation** | User manual, technical docs, presentation slides |
| **Versioned docs** | Output under `documentation/` with version/timestamp |

**Usage:**  
- Tests: `python final_testing.py` or via `ai_research_agent.py --test-system`  
- Docs: `python final_documentation.py` or via `ai_research_agent.py --generate-docs`

---

## Quick Reference: How to Run What

| Goal | Command |
|------|--------|
| Search & download papers (Milestone 1) | `python main.py "topic" [--max-papers N]` |
| View saved papers in terminal | `python view_papers.py` |
| Full CLI (search, drafts, APA, workflow, tests, docs) | `python ai_research_agent.py --help` |
| Web UI (Flask) | `python start_web_interface.py` |
| Gradio UI | `python gradio_interface.py` or `python enhanced_gradio_interface.py` |
| End-to-end workflow (drafts + review) | `python final_integration.py` or via `ai_research_agent.py --complete-workflow "topic"` |
| Run tests | `python final_testing.py` |
| Generate documentation | `python final_documentation.py` |

---

## Data Flow (Full Pipeline)

```
1. main.py           → Search & download papers → data/papers/, data/selected_papers.json
2. text_extractor    → Extract text from PDFs   → data/extracted_texts/
3. section_*         → Extract & analyze sections → data/section_analysis/
4. draft_generator   → Generate section drafts  → data/drafts/
5. content_reviewer   → Review & revise         → data/reviews/, data/revisions/
6. final_integration → Final report            → data/final_reports/
7. apa_formatter     → APA references          → data/references/ or output files
```

For **Milestone 1 only**, you use step 1 and optionally `view_papers.py` to inspect `data/selected_papers.json`.
