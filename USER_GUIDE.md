# AI Research Agent - User Guide and Examples

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Examples and Tutorials](#examples-and-tutorials)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)

## Quick Start

### 1. Search and Download Papers
```bash
# Basic search
python main.py "machine learning" --max-papers 3

# Advanced search with filters
python main.py "deep learning" --max-papers 5 --year-start 2020 --year-end 2023
```

### 2. Extract Text from PDFs
```bash
# Extract text from all downloaded PDFs
python -c "from paper_retrieval.text_extractor import process_downloaded_pdfs; process_downloaded_pdfs()"
```

### 3. Extract Sections
```bash
# Extract sections from all papers
python section_wise_extractor.py --process-all

# Extract specific sections
python section_extractor.py --papers "data/extracted_texts/*.json" --sections abstract,introduction,conclusion
```

### 4. Analyze and Compare Papers
```bash
# Generate analysis reports
python section_analyzer.py --input "data/extracted_texts/*.json" --output "analysis.json"

# Compare multiple papers
python section_wise_extractor.py --compare
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/springboardmentor23/ai_research_agent.git
cd ai_research_agent
git checkout Vedanth_Raj

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Paper Search and Download

#### Simple Search
```bash
python main.py "artificial intelligence" --max-papers 5
```

#### Search with Author
```bash
python main.py "" --author "Geoffrey Hinton" --max-papers 3
```

#### Search by Year Range
```bash
python main.py "neural networks" --year-start 2019 --year-end 2022 --max-papers 10
```

#### Search with Randomization
```bash
python main.py "machine learning" --randomize --diversity 0.7 --max-papers 8
```

### Text Extraction

#### Extract All Downloaded PDFs
```python
from paper_retrieval.text_extractor import process_downloaded_pdfs

# Process all PDFs in Downloaded_pdfs directory
results = process_downloaded_pdfs()
print(f"Extracted text from {len(results)} papers")
```

#### Extract Single PDF
```python
from paper_retrieval.text_extractor import PDFTextExtractor

extractor = PDFTextExtractor()
result = extractor.extract_text_from_pdf("Downloaded_pdfs/paper.pdf")

if result:
    print(f"Title: {result['metadata'].get('title', 'Unknown')}")
    print(f"Pages: {result['metadata'].get('page_count', 0)}")
    print(f"Text length: {len(result['full_text'])}")
```

### Section Extraction

#### Basic Section Extraction
```python
from section_extractor import SectionWiseExtractor

extractor = SectionWiseExtractor()

# Extract from text file
with open('data/extracted_texts/paper.txt', 'r') as f:
    content = f.read()

sections = extractor.detect_sections_from_text(content)
print(f"Found {len(sections)} sections")

for section in sections:
    print(f"- {section.title} ({section.section_type}): {section.word_count} words")
```

#### Extract Specific Sections
```python
from section_extractor import extract_sections_from_pdf

# Extract from PDF directly
sections_data = extract_sections_from_pdf("Downloaded_pdfs/paper.pdf")

if sections_data:
    print(f"Extracted {len(sections_data['sections'])} sections")
    
    # Find abstract
    abstract = next((s for s in sections_data['sections'] if s['type'] == 'abstract'), None)
    if abstract:
        print(f"Abstract: {abstract['content'][:200]}...")
```

### Section Analysis

#### Analyze Section Distribution
```python
from section_analyzer import SectionAnalyzer

analyzer = SectionAnalyzer()

# Load section data
with open('data/section_analysis/paper_sections.json', 'r') as f:
    section_data = json.load(f)

# Analyze distribution
distribution = analyzer.analyze_section_distribution(section_data)
print(f"Section types: {list(distribution['section_types'].keys())}")
print(f"Total sections: {distribution['total_sections']}")
```

#### Extract Key Insights
```python
# Extract key insights from abstract
insights = analyzer.extract_key_insights(section_data, 'abstract')
print("Key insights:")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")
```

#### Cross-Paper Comparison
```python
# Compare multiple papers
section_files = [
    'data/section_analysis/paper1_sections.json',
    'data/section_analysis/paper2_sections.json',
    'data/section_analysis/paper3_sections.json'
]

comparison = analyzer.compare_papers_by_sections(section_files)
print(f"Compared {len(comparison['papers'])} papers")
print(f"Common sections: {list(comparison['common_sections'].keys())}")
print(f"Average sections per paper: {comparison['average_sections_per_paper']:.1f}")
```

## Advanced Features

### Advanced Text Processing

#### Text Quality Assessment
```python
from advanced_text_processor import AdvancedTextProcessor

processor = AdvancedTextProcessor()

# Assess text quality
quality = processor.assess_text_quality(paper_text)
print(f"Overall quality: {quality.overall_quality:.2f}")
print(f"Readability: {quality.readability_score:.2f}")
print(f"Word diversity: {quality.word_diversity:.2f}")
```

#### Citation Extraction
```python
# Extract citations
citations = processor.extract_citations(paper_text)
print(f"Found {len(citations)} citations")

for citation in citations[:5]:  # Show first 5
    print(f"- {citation.citation_text} ({citation.citation_type})")
```

#### Keyword Extraction
```python
# Extract keywords
keywords = processor.extract_keywords(paper_text, max_keywords=15)
print("Top keywords:")
for keyword, score in keywords:
    print(f"- {keyword}: {score:.3f}")
```

#### Text Summarization
```python
# Generate summary
summary = processor.generate_summary(paper_text, max_sentences=5)
print("Summary:")
print(summary)
```

### Error Handling and Recovery

#### Using Error Handler
```python
from error_handler import safe_execute, handle_error

# Safe execution with error handling
result = safe_execute(
    lambda: extract_sections_from_pdf("problematic.pdf"),
    default_return=None,
    context={"operation": "section_extraction"}
)

if result is None:
    print("Extraction failed, but error was handled gracefully")
```

#### Retry with Backoff
```python
from error_handler import retry_with_backoff

@retry_with_backoff(max_retries=3, backoff_factor=1.0)
def extract_with_retry(pdf_path):
    return extract_sections_from_pdf(pdf_path)

try:
    result = extract_with_retry("large_paper.pdf")
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Performance Monitoring

#### Monitor Function Performance
```python
from performance_monitor import monitor_performance

@monitor_performance("pdf_extraction")
def extract_pdf_monitored(pdf_path):
    extractor = PDFTextExtractor()
    return extractor.extract_text_from_pdf(pdf_path)

# Function will be automatically monitored
result = extract_pdf_monitored("paper.pdf")
```

#### Get Performance Summary
```python
from performance_monitor import get_performance_summary

summary = get_performance_summary()
print(f"Total operations: {summary['operation_stats']['total_operations']}")
print(f"Success rate: {summary['operation_stats']['success_rate']:.2%}")
print(f"Average duration: {summary['operation_stats']['avg_duration_seconds']:.2f}s")
```

## Examples and Tutorials

### Example 1: Complete Research Paper Analysis Pipeline

```python
"""
Complete pipeline for analyzing research papers from search to comparison
"""

def complete_analysis_pipeline(topic: str, max_papers: int = 5):
    """Complete analysis pipeline"""
    
    # Step 1: Search and download papers
    print(f"Searching for papers on: {topic}")
    import subprocess
    result = subprocess.run([
        "python", "main.py", topic, "--max-papers", str(max_papers)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Search failed: {result.stderr}")
        return
    
    # Step 2: Extract text from PDFs
    print("Extracting text from PDFs...")
    from paper_retrieval.text_extractor import process_downloaded_pdfs
    extraction_results = process_downloaded_pdfs()
    
    # Step 3: Extract sections
    print("Extracting sections...")
    from section_extractor import SectionWiseExtractor
    extractor = SectionWiseExtractor()
    
    section_files = []
    for extracted_file in extraction_results:
        sections = extractor.detect_sections_from_text(extracted_file['full_text'])
        
        # Save section data
        section_data = {
            'metadata': extracted_file['metadata'],
            'sections': [
                {
                    'title': s.title,
                    'content': s.content,
                    'type': s.section_type,
                    'word_count': s.word_count
                }
                for s in sections
            ]
        }
        
        filename = f"data/section_analysis/{extracted_file['metadata'].get('title', 'unknown').replace(' ', '_')}_sections.json"
        with open(filename, 'w') as f:
            json.dump(section_data, f, indent=2)
        
        section_files.append(filename)
    
    # Step 4: Analyze and compare
    print("Analyzing and comparing papers...")
    from section_analyzer import SectionAnalyzer
    analyzer = SectionAnalyzer()
    
    comparison = analyzer.compare_papers_by_sections(section_files)
    
    # Step 5: Generate report
    print("Generating analysis report...")
    report = {
        'topic': topic,
        'papers_analyzed': len(section_files),
        'comparison': comparison,
        'timestamp': time.time()
    }
    
    with open(f"analysis_report_{topic.replace(' ', '_')}.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Analysis complete! Report saved to analysis_report_{topic.replace(' ', '_')}.json")
    return report

# Usage
if __name__ == "__main__":
    report = complete_analysis_pipeline("transformer models", 3)
```

### Example 2: Advanced Text Analysis

```python
"""
Advanced text analysis with quality assessment and insights extraction
"""

def advanced_text_analysis(paper_text: str):
    """Perform advanced text analysis"""
    
    from advanced_text_processor import AdvancedTextProcessor
    from section_extractor import SectionWiseExtractor
    
    processor = AdvancedTextProcessor()
    extractor = SectionWiseExtractor()
    
    # Extract sections first
    sections = extractor.detect_sections_from_text(paper_text)
    
    # Find abstract for focused analysis
    abstract_section = next((s for s in sections if s.section_type == 'abstract'), None)
    
    analysis_results = {
        'full_text_analysis': processor.process_text_comprehensive(paper_text),
        'section_count': len(sections),
        'section_types': list(set(s.section_type for s in sections))
    }
    
    if abstract_section:
        analysis_results['abstract_analysis'] = {
            'quality': processor.assess_text_quality(abstract_section.content),
            'citations': processor.extract_citations(abstract_section.content),
            'keywords': processor.extract_keywords(abstract_section.content),
            'summary': processor.generate_summary(abstract_section.content, max_sentences=3)
        }
    
    return analysis_results

# Usage
with open('data/extracted_texts/paper.txt', 'r') as f:
    text = f.read()

results = advanced_text_analysis(text)
print(f"Found {results['section_count']} sections")
print(f"Section types: {results['section_types']}")

if 'abstract_analysis' in results:
    abstract = results['abstract_analysis']
    print(f"Abstract quality: {abstract['quality'].overall_quality:.2f}")
    print(f"Keywords: {[kw for kw, _ in abstract['keywords'][:5]]}")
```

### Example 3: Batch Processing with Error Handling

```python
"""
Batch processing multiple papers with comprehensive error handling
"""

def batch_process_papers(pdf_directory: str, output_directory: str):
    """Process multiple papers with error handling"""
    
    from pathlib import Path
    from error_handler import safe_execute, handle_error
    from performance_monitor import monitor_performance
    import logging
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    pdf_dir = Path(pdf_directory)
    output_dir = Path(output_directory)
    output_dir.mkdir(exist_ok=True)
    
    results = {
        'successful': [],
        'failed': [],
        'total': 0
    }
    
    for pdf_file in pdf_dir.glob("*.pdf"):
        results['total'] += 1
        
        @monitor_performance("pdf_processing")
        def process_single_pdf(pdf_path):
            # Extract text
            from paper_retrieval.text_extractor import PDFTextExtractor
            extractor = PDFTextExtractor()
            text_result = extractor.extract_text_from_pdf(str(pdf_path))
            
            if not text_result:
                raise Exception("Text extraction failed")
            
            # Extract sections
            from section_extractor import SectionWiseExtractor
            section_extractor = SectionWiseExtractor()
            sections = section_extractor.detect_sections_from_text(text_result['full_text'])
            
            # Advanced analysis
            from advanced_text_processor import AdvancedTextProcessor
            processor = AdvancedTextProcessor()
            analysis = processor.process_text_comprehensive(text_result['full_text'])
            
            return {
                'metadata': text_result['metadata'],
                'sections': [vars(s) for s in sections],
                'analysis': analysis
            }
        
        # Process with error handling
        result = safe_execute(
            process_single_pdf,
            default_return=None,
            context={"pdf_file": str(pdf_file)}
        )
        
        if result:
            # Save successful result
            output_file = output_dir / f"{pdf_file.stem}_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            results['successful'].append(str(pdf_file))
            logger.info(f"Successfully processed: {pdf_file}")
        else:
            results['failed'].append(str(pdf_file))
            logger.error(f"Failed to process: {pdf_file}")
    
    # Save batch results
    batch_report = {
        'timestamp': time.time(),
        'total_files': results['total'],
        'successful': len(results['successful']),
        'failed': len(results['failed']),
        'success_rate': len(results['successful']) / results['total'],
        'successful_files': results['successful'],
        'failed_files': results['failed']
    }
    
    with open(output_dir / 'batch_report.json', 'w') as f:
        json.dump(batch_report, f, indent=2)
    
    print(f"Batch processing complete: {len(results['successful'])}/{results['total']} successful")
    return batch_report

# Usage
report = batch_process_papers("Downloaded_pdfs", "analysis_results")
```

## Troubleshooting

### Common Issues and Solutions

#### PDF Processing Errors
```python
# Problem: Corrupted or password-protected PDFs
from error_handler import retry_with_backoff

@retry_with_backoff(max_retries=3)
def robust_pdf_extraction(pdf_path):
    try:
        extractor = PDFTextExtractor()
        return extractor.extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"PDF extraction failed for {pdf_path}: {e}")
        raise
```

#### Memory Issues with Large Papers
```python
# Solution: Process in chunks
def process_large_pdf(pdf_path, chunk_size=10):
    """Process large PDF in chunks to avoid memory issues"""
    
    extractor = PDFTextExtractor()
    result = extractor.extract_text_from_pdf(pdf_path)
    
    if not result:
        return None
    
    # Process text in chunks
    full_text = result['full_text']
    words = full_text.split()
    
    for i in range(0, len(words), chunk_size * 1000):  # 10k word chunks
        chunk = ' '.join(words[i:i + chunk_size * 1000])
        
        # Process chunk
        processor = AdvancedTextProcessor()
        chunk_analysis = processor.assess_text_quality(chunk)
        
        # Store or process chunk results
        yield chunk_analysis
```

#### Section Detection Issues
```python
# Solution: Custom section patterns
def extract_with_custom_patterns(text):
    extractor = SectionWiseExtractor()
    
    # Add custom patterns
    extractor.section_patterns['methodology'].extend([
        r'^method\s*$',
        r'^approach\s*$',
        r'^technical\s+approach\s*$'
    ])
    
    sections = extractor.detect_sections_from_text(text)
    return sections
```

### Performance Optimization

#### Parallel Processing
```python
import concurrent.futures

def process_multiple_papers_parallel(pdf_files, max_workers=4):
    """Process multiple papers in parallel"""
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(extract_sections_from_pdf, pdf_file): pdf_file
            for pdf_file in pdf_files
        }
        
        results = {}
        for future in concurrent.futures.as_completed(future_to_file):
            pdf_file = future_to_file[future]
            try:
                result = future.result()
                results[pdf_file] = result
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
                results[pdf_file] = None
    
    return results
```

## API Reference

### Core Classes

#### PDFTextExtractor
```python
class PDFTextExtractor:
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]
```

#### SectionWiseExtractor
```python
class SectionWiseExtractor:
    def detect_sections_from_text(self, text: str) -> List[Section]
    def extract_sections_from_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]
```

#### SectionAnalyzer
```python
class SectionAnalyzer:
    def analyze_section_distribution(self, section_data: Dict[str, Any]) -> Dict[str, Any]
    def extract_key_insights(self, section_data: Dict[str, Any], section_type: str) -> List[str]
    def compare_papers_by_sections(self, section_files: List[str]) -> Dict[str, Any]
```

#### AdvancedTextProcessor
```python
class AdvancedTextProcessor:
    def assess_text_quality(self, text: str) -> TextQualityMetrics
    def extract_citations(self, text: str) -> List[CitationInfo]
    def extract_keywords(self, text: str, max_keywords: int = 20) -> List[Tuple[str, float]]
    def generate_summary(self, text: str, max_sentences: int = 5) -> str
```

### Utility Functions

#### Error Handling
```python
def safe_execute(func: Callable, default_return: Any = None, context: Dict[str, Any] = None)
def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0)
```

#### Performance Monitoring
```python
def monitor_performance(operation_name: str)
def get_performance_summary() -> Dict[str, Any]
```

## Contributing

We welcome contributions! Please see the main README.md for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
