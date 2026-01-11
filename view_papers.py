"""
View full paper details from selected_papers.json in a readable format.
"""
import json
import sys
from pathlib import Path
from config import METADATA_FILE


def display_paper(paper_data: dict, index: int):
    """Display a single paper's full details."""
    print("\n" + "="*80)
    print(f"PAPER {index}")
    print("="*80)
    
    # Title
    print(f"\n[TITLE]")
    print(f"   {paper_data.get('title', 'N/A')}")
    
    # Authors
    authors = paper_data.get('authors', [])
    if authors:
        print(f"\n[AUTHORS] ({len(authors)} total):")
        author_names = []
        for author in authors:
            if isinstance(author, dict):
                name = author.get('name', 'Unknown')
                author_id = author.get('authorId', '')
                if author_id:
                    author_names.append(f"{name} (ID: {author_id})")
                else:
                    author_names.append(name)
            else:
                author_names.append(str(author))
        for i, name in enumerate(author_names, 1):
            print(f"   {i}. {name}")
    
    # Year
    year = paper_data.get('year')
    if year:
        print(f"\n[YEAR] {year}")
    
    # Citations
    citations = paper_data.get('citationCount', 0)
    if citations:
        print(f"\n[CITATIONS] {citations:,}")
    
    # Paper ID
    paper_id = paper_data.get('paperId', '')
    if paper_id:
        print(f"\n[PAPER ID] {paper_id}")
    
    # Abstract
    abstract = paper_data.get('abstract', '')
    if abstract:
        print(f"\n[ABSTRACT]")
        # Word wrap the abstract
        words = abstract.split()
        line = "   "
        for word in words:
            if len(line + word) > 75:
                print(line)
                line = "   " + word + " "
            else:
                line += word + " "
        if line.strip():
            print(line)
    else:
        print(f"\n[ABSTRACT] Not available")
    
    # PDF Information
    has_pdf = paper_data.get('hasOpenAccessPdf', False)
    pdf_url = paper_data.get('pdfUrl', '')
    
    print(f"\n[PDF STATUS]")
    if has_pdf and pdf_url:
        print(f"   [PDF Available]")
        print(f"   URL: {pdf_url}")
    elif has_pdf:
        print(f"   [PDF Available but URL not provided]")
    else:
        print(f"   [No Open-Access PDF]")
    
    print("\n" + "="*80)


def main():
    """Main function to display all papers."""
    metadata_file = Path(METADATA_FILE)
    
    if not metadata_file.exists():
        print(f"Error: Metadata file not found: {METADATA_FILE}")
        print("Please run 'python main.py <topic>' first to fetch papers.")
        sys.exit(1)
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        if not papers:
            print("No papers found in metadata file.")
            sys.exit(1)
        
        print(f"\n{'='*80}")
        print(f"FULL PAPER DETAILS - {len(papers)} PAPER(S)")
        print(f"{'='*80}")
        
        for i, paper in enumerate(papers, 1):
            display_paper(paper, i)
        
        print(f"\n{'='*80}")
        print(f"Total: {len(papers)} paper(s)")
        print(f"Metadata file: {METADATA_FILE}")
        print(f"{'='*80}\n")
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in metadata file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading metadata file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

