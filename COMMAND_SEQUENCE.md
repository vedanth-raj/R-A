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
```

### 3. View Extracted Papers
```bash
# View all papers
python view_papers.py

# Search within papers
python view_papers.py --search "neural networks"
```

### 4. Complete Workflow (All in One)
```bash
# Search, download, and extract
python main.py "your topic" --max-papers 3 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()" && python view_papers.py
```

### 5. Check Your Files
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
├── Downloaded_pdfs/     # Downloaded PDF files
└── data/
    └── extracted_texts/ # Extracted text files
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

### Step 4: Complete Pipeline Examples
```bash
# Find papers and download them
python -c "from paper_retrieval.searcher import PaperSearcher; from paper_retrieval.downloader import PaperDownloader; searcher = PaperSearcher(); papers = searcher.search_papers(query='AI choreography', max_results=5); downloader = PaperDownloader(); [downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]"

# Download and extract in one command
python -c "from paper_retrieval.searcher import PaperSearcher; from paper_retrieval.downloader import PaperDownloader; from paper_retrieval.text_extractor import process_downloaded_pdfs; searcher = PaperSearcher(); papers = searcher.search_papers(query='machine learning', max_results=3); downloader = PaperDownloader(); [downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]; results = process_downloaded_pdfs()"
```

### Step 5: Utility Commands
```bash
# Check what's in Downloaded_pdfs directory
ls Downloaded_pdfs/

# Check extracted texts
ls data/extracted_texts/

# Count PDFs and extracted files
python -c "import os; pdfs = len([f for f in os.listdir('Downloaded_pdfs') if f.endswith('.pdf')]); txts = len([f for f in os.listdir('data/extracted_texts') if f.endswith('.txt')]); print(f'PDFs: {pdfs}, TXT files: {txts}')"

# View specific extracted text
head -50 data/extracted_texts/Brunton2019_Machine_Learning_for_Fluid_Mechanics_extracted.txt

# Search within extracted texts
grep -r "machine learning" data/extracted_texts/
```

### Step 6: Test and Validation
```bash
# Test text extraction
python test_txt_extraction.py

# Validate extraction worked
python -c "from paper_retrieval.text_extractor import extract_pdf_text; data = extract_pdf_text('Downloaded_pdfs/Brunton2019.pdf'); print('Success!' if data and 'Failed!' if not data)"
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
# Search, download, and extract in one go
python main.py "fluid mechanics" --max-papers 3 && python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()"
```

### Quick Examples:
```bash
# Check what you have
ls Downloaded_pdfs/
ls data/extracted_texts/

# Quick search in papers
python view_papers.py --search "machine learning"

# Count papers
python -c "import os; pdfs=len([f for f in os.listdir('Downloaded_pdfs') if f.endswith('.pdf')]); print(f'PDFs: {pdfs}')"
```

## Quick Reference

### Modules:
- `paper_retrieval.searcher` - Paper search functionality
- `paper_retrieval.downloader` - Paper download functionality  
- `paper_retrieval.text_extractor` - Text extraction functionality

### Directories:
- `Downloaded_pdfs/` - Downloaded PDF files
- `data/extracted_texts/` - Extracted text files (TXT/JSON)

### File Formats:
- Input: PDF files
- Output: TXT files (default) or JSON files
- Naming: `{filename}_extracted.{format}`

## Common Workflows

### Research Workflow:
1. Search for relevant papers
2. Download selected papers to `Downloaded_pdfs/`
3. Extract text from downloaded PDFs
4. Analyze extracted content

### Batch Processing:
```bash
# Complete research to extraction pipeline
python -c "
from paper_retrieval.searcher import PaperSearcher
from paper_retrieval.downloader import PaperDownloader  
from paper_retrieval.text_extractor import process_downloaded_pdfs

# Search, download, and extract
searcher = PaperSearcher()
papers = searcher.search_papers(query='your topic', max_results=10)
downloader = PaperDownloader()
[downloader.download_paper(arxiv_id=p['arxiv_id'], save_path='Downloaded_pdfs') for p in papers]
results = process_downloaded_pdfs()
print(f'Processed {len(results[\"success\"])} papers')
"
