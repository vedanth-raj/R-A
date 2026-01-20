# AI Research Agent - Advanced Paper Analysis System

A comprehensive AI-powered system for finding, downloading, extracting, and analyzing research papers with advanced section-wise text extraction capabilities. This tool provides intelligent paper retrieval and structured content analysis for researchers and academics.

## 🚀 Key Features

- 🔍 **Smart Paper Search**: Find research papers by keywords, authors, topics, or year ranges
- 📥 **Automated Download**: Download papers in PDF format from Semantic Scholar
- 📝 **Advanced Text Extraction**: Extract full text and metadata from downloaded papers
- 🎯 **Section-Wise Analysis**: Intelligent extraction of specific sections (Abstract, Introduction, Methodology, Results, Conclusion, References)
- 🔍 **Content Search**: Search within extracted papers and sections
- 📊 **Structured Output**: Export extracted content in JSON format for further analysis
- 🎛️ **Simple CLI Interface**: User-friendly command-line interface with comprehensive options

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

**Check Python version**:
```bash
python --version
# or
python3 --version
```

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/springboardmentor23/ai_research_agent.git
   cd ai_research_agent
   git checkout Vedanth_Raj
   ```

2. **Create and activate virtual environment**:
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys if needed
   ```

## Quick Start

1. **Search and download papers**:
   ```bash
   # Search for machine learning papers and download up to 3 papers
   python main.py "machine learning" --max-papers 3
   ```

2. **Extract full text from downloaded papers**:
   ```bash
   # Process all downloaded PDFs and extract text content
   python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()"
   ```

3. **Extract specific sections from papers**:
   ```bash
   # Extract abstract, introduction, and conclusion sections
   python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,introduction,conclusion
   ```

4. **View extracted papers**:
   ```bash
   # Interactive viewer for extracted paper content
   python view_papers.py
   ```

5. **Analyze sections with detailed breakdown**:
   ```bash
   # Generate comprehensive section analysis report
   python section_analyzer.py --input "data/extracted_texts/*.json" --output "section_analysis.json"
   ```

## Project Structure

```
project/
├── main.py                      # Main script for searching and downloading papers
├── view_papers.py               # Script to view and search extracted papers
├── section_extractor.py         # Advanced section-wise text extraction
├── section_analyzer.py          # Section content analysis and quality assessment
├── section_wise_extractor.py    # Comprehensive section extraction tool
├── config.py                    # Configuration settings and constants
├── paper_retrieval/             # Core functionality modules
│   ├── searcher.py             # Semantic Scholar API integration
│   ├── downloader.py           # PDF download management
│   ├── selector.py             # Paper selection and filtering
│   ├── text_extractor.py       # PDF text extraction engine
│   └── models.py               # Data models and schemas
├── utils/                       # Utility functions and helpers
│   └── helpers.py              # Common utility functions
├── Downloaded_pdfs/             # Downloaded PDF files
├── data/
│   └── extracted_texts/        # Extracted text files in JSON format
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys, etc.)
├── .gitignore                   # Git ignore file
├── COMMAND_SEQUENCE.md          # Detailed command reference
└── SECTION_EXTRACTION_README.md # Section extraction guide
```

## Usage Examples

### Search and Download
```bash
# Basic search
python main.py "deep learning" --max-papers 5

# Search with randomization
python main.py "AI research" --randomize --diversity 0.5

# Search by author
python main.py "" --author "Einstein" --max-papers 3
```

### View Extracted Papers
```bash
# View all papers
python view_papers.py

# Search within papers
python view_papers.py --search "neural networks"

# View in JSON format
python view_papers.py --format json
```

## 🔧 Section Extraction Features

The system provides advanced section-wise extraction capabilities for detailed paper analysis:

### Available Sections
- **Abstract**: Paper summary and key findings
- **Introduction**: Background and problem statement
- **Methodology**: Research methods and approaches
- **Results**: Experimental outcomes and data
- **Conclusion**: Summary and implications
- **References**: Citation list and bibliography

### Section Extraction Commands

```bash
# Extract specific sections from multiple papers
python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,introduction,conclusion

# Extract all sections with detailed analysis
python section_wise_extractor.py --input "data/extracted_texts/" --output "sections_output/"

# Analyze section content and structure
python section_analyzer.py --input "data/extracted_texts/*.json" --output "section_analysis.json"

# Extract sections with custom filtering
python section_extractor.py --papers "paper1.json,paper2.json" --sections methodology,results --min-length 100
```

### Section Analysis Features
- **Content Classification**: Automatically identify and categorize sections
- **Quality Assessment**: Evaluate section completeness and quality
- **Cross-Paper Comparison**: Compare similar sections across multiple papers
- **Export Options**: Save extracted sections in JSON, CSV, or TXT formats
- **Custom Filtering**: Filter sections by length, keywords, or quality metrics
- **Batch Processing**: Process multiple papers simultaneously for efficiency

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.