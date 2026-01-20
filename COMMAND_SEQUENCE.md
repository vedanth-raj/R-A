# Paper Research and Text Extraction - Command Sequence

## Quick Start Commands

### 1. Find and Download Papers
```bash
# Basic search and download
python main.py "machine learning" --max-papers 3

# With randomization and diversity
python main.py "AI research" --max-papers 5 --randomize --diversity 0.5
```

### 2. Extract Text from Downloaded Papers
```bash
# Extract text from all downloaded PDFs
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()"

python -c "from paper_retrieval.text_extractor import PDFTextExtractor; extractor = PDFTextExtractor(); extractor.process_downloaded_pdfs('data/papers', 'data/extracted_texts')"
```

### 3. View Extracted Papers
```bash
# View all papers
python view_papers.py

# Search within papers
python view_papers.py --search "neural networks"
```

### 4. Section-wise Text Extraction and Analysis
```bash
# Process all PDFs for section extraction
python section_wise_extractor.py --process-all

# Extract sections from a specific PDF
python section_wise_extractor.py --pdf path/to/paper.pdf

# Extract specific sections only
python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,introduction,conclusion

# Analyze existing section data
python section_wise_extractor.py --analyze

# Compare multiple papers by section structure
python section_wise_extractor.py --compare

# Generate comprehensive section analysis report
python section_analyzer.py --input "data/extracted_texts/*.json" --output "section_analysis.json"

# Use custom directories
python section_wise_extractor.py --process-all --pdf-dir my_papers --output-dir my_analysis

# Advanced section extraction with filtering
python section_extractor.py --papers "paper1.json,paper2.json" --sections methodology,results --min-length 100
```

### 5. Complete Workflow (All in One)
```bash
# Search, download, extract text, and analyze sections
python main.py "your topic" --max-papers 3 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python section_wise_extractor.py --process-all && python view_papers.py
```
### 6. Check Your Files
```bash
# See downloaded PDFs
dir Downloaded_pdfs

# See extracted texts
dir data\extracted_texts
```

## Directory Structure
```
project/
├── main.py              # Main script for searching and downloading
├── view_papers.py       # Script to view extracted papers
├── section_extractor.py # Core section extraction functionality
├── section_analyzer.py  # Analysis tools for section data
├── section_wise_extractor.py # CLI for section extraction and analysis
├── Downloaded_pdfs/     # Downloaded PDF files
└── data/
    ├── extracted_texts/ # Extracted text files
    └── section_analysis/ # Section-wise extracted data and analysis
```

## Advanced Usage

### Search with Different Parameters
```bash
# Search by author
python main.py "" --author "Einstein" --max-papers 3

# Search by year range
python main.py "" --year-start 2018 --year-end 2022 --max-papers 5
```

### View Options
```bash
# View papers in JSON format
python view_papers.py --format json

# View specific number of results
python view_papers.py --limit 5

# View with pagination
python view_papers.py --page 1 --per-page 10
```

### Update and Maintenance
```bash
# Install/update dependencies
pip install -r requirements.txt

# Clear downloaded PDFs
del /s /q Downloaded_pdfs\*.pdf

# Clear extracted text
del /s /q data\extracted_texts\*.*

# Download multiple papers
python -c "from paper_retrieval.downloader import PaperDownloader; downloader = PaperDownloader(); [downloader.download_paper(arxiv_id=id, save_path='Downloaded_pdfs') for id in ['1905.11075', '2101.08779']]"
```

### Step 3: Extract Text from Downloaded PDFs
```bash
# Process all PDFs in Downloaded_pdfs (default: TXT format)
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; results = process_downloaded_pdfs()"

# Process with specific directory and format
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; results = process_downloaded_pdfs(downloaded_dir='my_papers', output_dir='output', format='txt')"

# Extract single PDF
python -c "from paper_retrieval.text_extractor import extract_pdf_text; data = extract_pdf_text('Downloaded_pdfs/paper.pdf')"
```

### Step 7: Section-wise Analysis
```bash
# Extract sections from all PDFs
python section_wise_extractor.py --process-all

# Analyze section distribution
python section_wise_extractor.py --analyze

# Compare papers by structure
python section_wise_extractor.py --compare

# Programmatic section extraction
python -c "from section_extractor import extract_sections_from_pdf; data = extract_sections_from_pdf('Downloaded_pdfs/paper.pdf'); print(f'Sections: {len(data[\"sections\"])}')"

# Analyze specific paper sections
python -c "from section_analyzer import analyze_paper_sections; analysis = analyze_paper_sections('data/section_analysis/paper_sections.json'); print(f'Section types: {list(analysis[\"section_types\"].keys())}')"
```

### Step 8: Complete Pipeline Examples
```bash
# Find papers and download them
python -c "from paper_retrieval.searcher import PaperSearcher; from paper_retrieval.downloader import PaperDownloader; searcher = PaperSearcher(); papers = searcher.search_papers(query='AI choreography', max_results=5); downloader = PaperDownloader(); [downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]"

# Download and extract in one command
python main.py "machine learning" --max-papers 3 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python section_wise_extractor.py --process-all

# Batch processing with custom settings
python main.py "deep learning" --max-papers 10 --randomize --diversity 0.7 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,methodology,results --min-length 150
```

## Performance Optimization

### Large Dataset Processing
```bash
# Process papers in batches to avoid memory issues
python main.py "neural networks" --max-papers 50 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python section_wise_extractor.py --process-all --batch-size 5

# Use specific sections to reduce processing time
python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,conclusion --output-format csv

# Parallel processing for multiple papers
python section_analyzer.py --input "data/extracted_texts/*.json" --output "analysis.json" --parallel-workers 4
```

### Memory Management
```bash
# Clear temporary files after processing
python -c "import shutil; shutil.rmtree('data/temp', ignore_errors=True)"

# Monitor disk usage
python -c "import os; print(f'Downloaded PDFs: {len(os.listdir(\"Downloaded_pdfs\"))} files'); print(f'Extracted texts: {len(os.listdir(\"data/extracted_texts\"))} files')"
```

## Troubleshooting Common Issues

### PDF Processing Problems
```bash
# Check PDF integrity
python -c "from paper_retrieval.text_extractor import PDFTextExtractor; extractor = PDFTextExtractor(); print(extractor.validate_pdf('Downloaded_pdfs/paper.pdf'))"

# Extract from problematic PDFs with fallback
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs(use_ocr=True, fallback=True)"
```

### Section Extraction Issues
```bash
# Debug section detection
python section_wise_extractor.py --pdf "problematic.pdf" --debug --verbose

# Use custom section patterns
python section_extractor.py --papers "data/extracted_texts/*.json" --custom-patterns '{"introduction": ["introduction", "background", "overview"], "methodology": ["method", "approach", "technique"]}'
```
python -c "from paper_retrieval.searcher import PaperSearcher; from paper_retrieval.downloader import PaperDownloader; from paper_retrieval.text_extractor import process_downloaded_pdfs; searcher = PaperSearcher(); papers = searcher.search_papers(query='machine learning', max_results=3); downloader = PaperDownloader(); [downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]; results = process_downloaded_pdfs()"
```

### Step 9: Utility Commands
```bash
# Check what's in Downloaded_pdfs directory
ls Downloaded_pdfs/

# Check extracted texts
ls data/extracted_texts/

# Count PDFs, extracted files, and section analyses
python -c "import os; pdfs = len([f for f in os.listdir('Downloaded_pdfs') if f.endswith('.pdf')]); txts = len([f for f in os.listdir('data/extracted_texts') if f.endswith('.txt')]); sections = len([f for f in os.listdir('data/section_analysis') if f.endswith('.json')]) if os.path.exists('data/section_analysis') else 0; print(f'PDFs: {pdfs}, TXT files: {txts}, Section analyses: {sections}')"

# View specific extracted text
head -50 data/extracted_texts/Brunton2019_Machine_Learning_for_Fluid_Mechanics_extracted.txt

# Search within extracted texts
grep -r "machine learning" data/extracted_texts/
```

### Step 10: Test and Validation
```bash
# Test text extraction
python test_txt_extraction.py

# Validate section extraction worked
python -c "from section_extractor import extract_sections_from_pdf; data = extract_sections_from_pdf('Downloaded_pdfs/paper.pdf'); print('Section extraction success!' if data and 'Failed!' if not data)"

# Test section analysis
python -c "from section_analyzer import analyze_paper_sections; import os; files = [f for f in os.listdir('data/section_analysis') if f.endswith('.json')]; print(f'Found {len(files)} section files to analyze') if files else print('No section files found')"
```

## Simple Commands (Ready to Use)

### Research and Download:
```bash
# Search and download papers (simple)
python main.py "machine learning" --max-papers 3

# Search with randomization
python main.py "AI choreography" --max-papers 5 --randomize --diversity 0.5

# Search and download multiple papers
python main.py "deep learning" --max-papers 10
```

### Section Analysis:
```bash
# Extract sections from all papers
python section_wise_extractor.py --process-all

# Analyze section data
python section_wise_extractor.py --analyze

# Compare paper structures
python section_wise_extractor.py --compare

# Extract sections from specific paper
python section_wise_extractor.py --pdf Downloaded_pdfs/paper.pdf
```
### View Extracted Papers:
```bash
# View all extracted papers
python view_papers.py

# View with search term
python view_papers.py --search "neural network"

# View JSON format
python view_papers.py --format json

# View specific file
python view_papers.py "filename.txt"
```

### Complete Pipeline:
```bash
# Search, download, extract text, and analyze sections
python main.py "fluid mechanics" --max-papers 3 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python section_wise_extractor.py --process-all && python view_papers.py
```

### Quick Examples:
```bash
# Check what you have
ls Downloaded_pdfs/
ls data/extracted_texts/
ls data/section_analysis/

# Quick search in papers
python view_papers.py --search "machine learning"

# Quick section analysis
python section_wise_extractor.py --analyze

# Count papers and sections
python -c "import os; pdfs=len([f for f in os.listdir('Downloaded_pdfs') if f.endswith('.pdf')]); sections=len([f for f in os.listdir('data/section_analysis')]) if os.path.exists('data/section_analysis') else 0; print(f'PDFs: {pdfs}, Section analyses: {sections}')"
```

## Quick Reference

### Modules:
- `paper_retrieval.searcher` - Paper search functionality
- `paper_retrieval.downloader` - Paper download functionality  
- `paper_retrieval.text_extractor` - Text extraction functionality
- `section_extractor` - Section-wise extraction functionality
- `section_analyzer` - Section analysis and comparison tools
- `section_wise_extractor` - CLI for section extraction and analysis

### Directories:
- `Downloaded_pdfs/` - Downloaded PDF files
- `data/extracted_texts/` - Extracted text files (TXT/JSON)
- `data/section_analysis/` - Section-wise extracted data and analysis reports

### File Formats:
- Input: PDF files
- Output: TXT files (default) or JSON files
- Section Data: JSON files with structured section information
- Analysis Reports: JSON and TXT format reports
- Naming: `{filename}_extracted.{format}`, `{filename}_sections.json`, `{filename}_sections.report.json`

## Common Workflows

### Research Workflow:
1. Search for relevant papers
2. Download selected papers to `Downloaded_pdfs/`
3. Extract text from downloaded PDFs
4. Extract sections from papers using section analysis
5. Analyze section structure and content
6. Compare papers by their section organization

### Advanced Research Workflow:
```bash
# Complete research pipeline with section analysis
python main.py "your topic" --max-papers 5 && \
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && \
python section_wise_extractor.py --process-all && \
python section_wise_extractor.py --analyze && \
python section_wise_extractor.py --compare
```

### Batch Processing:
```bash
# Complete research to section analysis pipeline
python -c "
from paper_retrieval.searcher import PaperSearcher
from paper_retrieval.downloader import PaperDownloader  
from paper_retrieval.text_extractor import process_downloaded_pdfs
from section_extractor import process_all_pdfs_for_sections

# Search, download, extract text, and analyze sections
searcher = PaperSearcher()
papers = searcher.search_papers(query='your topic', max_results=10)
downloader = PaperDownloader()
[downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]
results = process_downloaded_pdfs()
section_results = process_all_pdfs_for_sections()
print(f'Processed {len(results[\"success\"])} papers and extracted sections from {len(section_results[\"success\"])} papers')
"
