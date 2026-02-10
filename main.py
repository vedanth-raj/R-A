import argparse
import json
import logging
import sys
import os
from pathlib import Path
from typing import List

# Fix Windows console encoding for Unicode characters
from utils.encoding_fix import fix_console_encoding, safe_print
fix_console_encoding()

from config import (
    DEFAULT_MAX_PAPERS,
    MAX_PAPERS_UPPER_LIMIT,
    INITIAL_SEARCH_LIMIT,
    METADATA_FILE,
    PAPERS_DIR
)
from paper_retrieval.searcher import SemanticScholarSearcher
from paper_retrieval.selector import PaperSelector
from paper_retrieval.downloader import PDFDownloader
from paper_retrieval.models import PaperMetadata
from utils.helpers import ensure_directory

logger = logging.getLogger(__name__)


def save_metadata(papers: List[PaperMetadata], filepath: str) -> None:

    ensure_directory(Path(filepath).parent)
    
    # Convert to dict format for JSON serialization
    papers_data = []
    for paper in papers:
        paper_dict = paper.model_dump(mode='json', exclude_none=True)
        # Add download status info
        paper_dict["hasOpenAccessPdf"] = paper.has_open_pdf()
        paper_dict["pdfUrl"] = paper.get_pdf_url()
        papers_data.append(paper_dict)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(papers_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved metadata for {len(papers)} papers to {filepath}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="AI System to Automatically Review and Summarize Research Papers - Milestone 1"
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Research topic to search for (e.g., 'quantum machine learning')"
    )
    parser.add_argument(
        "--max-papers",
        type=int,
        default=DEFAULT_MAX_PAPERS,
        help=f"Maximum number of papers to select (default: {DEFAULT_MAX_PAPERS}, max: {MAX_PAPERS_UPPER_LIMIT})"
    )
    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Randomly select papers from top-ranked results (for variety)"
    )
    parser.add_argument(
        "--diversity",
        type=float,
        default=0.3,
        metavar="FACTOR",
        help="Diversity factor (0.0-1.0) when using --randomize. Higher = more variety (default: 0.3)"
    )
    parser.add_argument(
        "--generate-draft",
        action="store_true",
        help="Generate lengthy APA-formatted draft after paper retrieval"
    )
    
    args = parser.parse_args()
    
    # Validate max_papers
    max_papers = min(max(1, args.max_papers), MAX_PAPERS_UPPER_LIMIT)
    if args.max_papers != max_papers:
        logger.warning(
            f"max_papers adjusted from {args.max_papers} to {max_papers} "
            f"(must be between 1 and {MAX_PAPERS_UPPER_LIMIT})"
        )
    
    topic = args.topic.strip()
    if not topic:
        logger.error("Topic cannot be empty")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"AI Research Paper Review System - Milestone 1")
    print(f"{'='*60}")
    print(f"Searching Semantic Scholar for: {topic}")
    print(f"Maximum papers to select: {max_papers}\n")
    
    try:
        # Step 1: Search for papers
        searcher = SemanticScholarSearcher()
        print(f"Fetching up to {INITIAL_SEARCH_LIMIT} papers for ranking...")
        papers = searcher.search_papers_paginated(topic, total_limit=INITIAL_SEARCH_LIMIT)
        
        if not papers:
            print("No papers found for the given topic.")
            sys.exit(1)
        
        selection_mode = "randomly selecting" if args.randomize else "selecting top"
        print(f"Retrieved {len(papers)} papers, {selection_mode} {max_papers} "
              f"(prioritizing open-access PDFs)...")
        
        # Step 2: Select top papers
        selector = PaperSelector()
        diversity = max(0.0, min(1.0, args.diversity))  # Clamp between 0 and 1
        selected_papers = selector.select_papers(
            papers, 
            max_papers=max_papers,
            randomize=args.randomize,
            diversity_factor=diversity
        )
        
        if not selected_papers:
            print("No papers selected.")
            sys.exit(1)
        
        papers_with_pdfs = sum(1 for p in selected_papers if p.has_open_pdf())
        print(f"Selected {len(selected_papers)} papers ({papers_with_pdfs} with open PDFs)\n")
        
        # Step 3: Download PDFs
        print("Downloading open-access PDFs...")
        downloader = PDFDownloader()
        download_results = downloader.download_papers(selected_papers)
        
        downloaded_count = sum(1 for r in download_results.values() if r["downloaded"])
        print(f"Downloaded {downloaded_count} PDFs to {PAPERS_DIR}/\n")
        
        # Step 4: Save metadata
        print("Saving metadata...")
        save_metadata(selected_papers, METADATA_FILE)
        print(f"Metadata saved to {METADATA_FILE}\n")
        
        # Step 5: Generate draft if requested
        if args.generate_draft:
            print(f"{'='*60}")
            print("Generating Lengthy APA-Formatted Draft...")
            print(f"{'='*60}\n")
            
            from lengthy_draft_generator import LengthyDraftGenerator
            
            draft_generator = LengthyDraftGenerator()
            
            # Prepare paper data
            papers_data = []
            for paper in selected_papers:
                papers_data.append({
                    'title': paper.title,
                    'authors': [author.name for author in (paper.authors or [])],
                    'year': paper.year or 'n.d.',
                    'doi': paper.paperId  # Use paperId as DOI
                })
            
            # Generate draft
            draft_output = Path(PAPERS_DIR) / "generated_draft.txt"
            draft = draft_generator.generate_complete_draft(topic, papers_data, str(draft_output))
            
            print(f"\n✅ Draft generated successfully!")
            print(f"   Saved to: {draft_output}")
            print(f"\n   Word counts:")
            for section, content in draft.items():
                word_count = len(content.split())
                print(f"     - {section.title()}: {word_count} words")
            
            total_words = sum(len(content.split()) for content in draft.values())
            print(f"     - Total: {total_words} words\n")
        
        # Summary
        print(f"{'='*60}")
        print("Milestone 1 Complete – Ready for text extraction.")
        if args.generate_draft:
            print("Draft Generation Complete – Ready for review.")
        print(f"{'='*60}")
        print(f"\nSummary:")
        print(f"  - Papers selected: {len(selected_papers)}")
        print(f"  - Papers with PDFs: {papers_with_pdfs}")
        print(f"  - PDFs downloaded: {downloaded_count}")
        print(f"  - Metadata file: {METADATA_FILE}")
        print(f"  - PDFs directory: {PAPERS_DIR}")
        print(f"\nSelected papers:")
        for i, paper in enumerate(selected_papers, 1):
            pdf_status = "[PDF]" if paper.has_open_pdf() else "[No PDF]"
            year = paper.year or "N/A"
            citations = paper.citationCount or 0
            # Use safe_print for Unicode characters
            title_preview = paper.title[:60]
            safe_print(f"  {i}. {title_preview}...")
            safe_print(f"     ({year}, {citations} citations, {pdf_status})")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error during execution: {e}")
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

