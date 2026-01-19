# Section-wise Text Extraction and Analysis

This module provides comprehensive tools for extracting section-wise text data from research papers and storing it for detailed analysis.

## Files Created

1. **`section_extractor.py`** - Core section extraction functionality
2. **`section_analyzer.py`** - Analysis tools for extracted section data  
3. **`section_wise_extractor.py`** - Command-line interface for easy usage

## Features

### Section Extraction
- **Intelligent Section Detection**: Automatically identifies common research paper sections (Abstract, Introduction, Methodology, Results, etc.)
- **Content Analysis**: Extracts key phrases, sentences, and word counts for each section
- **Page Tracking**: Maintains page boundaries for each section
- **Flexible Output**: Saves data in structured JSON format for easy analysis

### Analysis Tools
- **Section Distribution Analysis**: Statistical analysis of section types and sizes
- **Paper Comparison**: Compare multiple papers by their section structure
- **Key Insight Extraction**: Identify important phrases and sentences from specific sections
- **Report Generation**: Create human-readable analysis reports

### Data Storage
- **Structured JSON Format**: Each paper's sections stored with metadata
- **Analysis Reports**: Comprehensive reports with statistics and insights
- **Batch Processing**: Process multiple papers simultaneously
- **Comparison Data**: Cross-paper analysis results

## Usage

### Command Line Interface

```bash
# Process all PDFs in Downloaded_pdfs directory
python section_wise_extractor.py --process-all

# Extract sections from a specific PDF
python section_wise_extractor.py --pdf path/to/paper.pdf

# Analyze existing section data
python section_wise_extractor.py --analyze

# Compare multiple papers by section structure
python section_wise_extractor.py --compare

# Use custom directories
python section_wise_extractor.py --process-all --pdf-dir my_pdfs --output-dir my_analysis
```

### Programmatic Usage

```python
from section_extractor import extract_sections_from_pdf
from section_analyzer import analyze_paper_sections

# Extract sections from a single PDF
section_data = extract_sections_from_pdf("paper.pdf")
print(f"Found {len(section_data['sections'])} sections")

# Analyze section distribution
analysis = analyze_paper_sections("data/section_analysis/paper_sections.json")
print(f"Section types: {list(analysis['section_types'].keys())}")
```

## Output Structure

### Section Data Format
```json
{
  "metadata": {
    "title": "Paper Title",
    "author": "Authors",
    "page_count": 10
  },
  "sections": [
    {
      "title": "Abstract",
      "type": "abstract",
      "content": "Abstract text...",
      "start_page": 1,
      "end_page": 1,
      "word_count": 150,
      "key_phrases": ["machine learning", "neural networks"],
      "sentences": ["This paper presents...", "Our approach..."]
    }
  ],
  "section_summary": {
    "total_sections": 8,
    "section_types": {"abstract": 1, "introduction": 1},
    "total_words": 5000
  }
}
```

### Analysis Report Format
```json
{
  "paper_metadata": {...},
  "section_analysis": {
    "total_sections": 8,
    "section_types": {"abstract": 1, "introduction": 1},
    "average_section_length": 625,
    "longest_section": {...},
    "shortest_section": {...}
  },
  "text_report": "Human-readable summary...",
  "raw_sections": [...]
}
```

## Integration with Existing System

This module integrates seamlessly with the existing AI Research Agent:

1. **Uses existing PDF extraction**: Builds on `paper_retrieval.text_extractor`
2. **Compatible file structure**: Works with `Downloaded_pdfs/` and `data/` directories
3. **Metadata preservation**: Maintains existing paper metadata
4. **Non-intrusive**: Doesn't modify existing functionality

## Section Types Detected

- Abstract
- Introduction  
- Related Work / Literature Review
- Methodology / Methods
- Experiments / Evaluation
- Results
- Discussion
- Conclusion
- References
- Appendix

## Analysis Capabilities

- **Section Distribution**: Word counts, page coverage, type frequency
- **Cross-Paper Comparison**: Common sections, structural patterns
- **Content Analysis**: Key phrase extraction, sentence analysis
- **Statistical Summary**: Averages, extremes, distributions
- **Report Generation**: Both JSON and text formats

## Data Storage Locations

- **Section Data**: `data/section_analysis/[paper_name]_sections.json`
- **Analysis Reports**: `data/section_analysis/[paper_name]_sections.report.json`
- **Comparison Data**: `data/section_analysis/comparison_report.json`
- **Text Reports**: `data/section_analysis/[paper_name]_sections.report.txt`

This comprehensive system provides powerful tools for extracting, analyzing, and comparing research paper structure and content at a section level, enabling detailed academic research and analysis.
