"""
Section-wise Text Data Extraction and Analysis Tool

This script provides a command-line interface for extracting section-wise text data
from research papers and storing it for analysis.

Usage:
    python section_wise_extractor.py [options]

Examples:
    # Process all PDFs in Downloaded_pdfs directory
    python section_wise_extractor.py --process-all
    
    # Extract sections from a specific PDF
    python section_wise_extractor.py --pdf path/to/paper.pdf
    
    # Generate analysis reports for existing section data
    python section_wise_extractor.py --analyze
    
    # Compare multiple papers by their section structure
    python section_wise_extractor.py --compare
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

from section_extractor import SectionWiseExtractor, extract_sections_from_pdf, process_all_pdfs_for_sections
from section_analyzer import SectionAnalyzer, analyze_paper_sections, generate_paper_report


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('section_extraction.log')
        ]
    )


def process_single_pdf(pdf_path: str, output_dir: str = "data/section_analysis") -> bool:
    """
    Process a single PDF file for section extraction.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save section data
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return False
    
    logger.info(f"Processing single PDF: {pdf_path}")
    
    section_data = extract_sections_from_pdf(pdf_path)
    
    if section_data:
        # Save section data
        extractor = SectionWiseExtractor()
        pdf_name = Path(pdf_path).stem
        output_path = Path(output_dir) / f"{pdf_name}_sections.json"
        
        if extractor.save_section_data(section_data, str(output_path)):
            logger.info(f"Section data saved to {output_path}")
            
            # Generate analysis report
            analyzer = SectionAnalyzer()
            report_path = output_path.with_suffix('.report.json')
            analyzer.save_analysis_report(section_data, str(report_path))
            
            logger.info(f"Analysis report saved to {report_path}")
            return True
        else:
            logger.error("Failed to save section data")
            return False
    else:
        logger.error("Failed to extract sections from PDF")
        return False


def process_all_pdfs(pdf_dir: str = "Downloaded_pdfs", 
                    output_dir: str = "data/section_analysis") -> bool:
    """
    Process all PDF files in a directory.
    
    Args:
        pdf_dir (str): Directory containing PDF files
        output_dir (str): Directory to save section data
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"Processing all PDFs in {pdf_dir}")
    
    results = process_all_pdfs_for_sections(pdf_dir, output_dir)
    
    # Print results summary
    print(f"\n{'='*60}")
    print("Section Extraction Results")
    print(f"{'='*60}")
    print(f"Total PDFs processed: {results['total']}")
    print(f"Successfully extracted: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['success']:
        print(f"\nSuccessfully processed papers:")
        for success in results['success']:
            print(f"  - {success['file']}: {success['sections_found']} sections")
    
    if results['failed']:
        print(f"\nFailed to process:")
        for failed in results['failed']:
            print(f"  - {failed}")
    
    # Generate analysis reports for successful extractions
    if results['success']:
        print(f"\nGenerating analysis reports...")
        analyzer = SectionAnalyzer()
        
        for success in results['success']:
            pdf_name = Path(success['file']).stem
            section_file = Path(output_dir) / f"{pdf_name}_sections.json"
            
            if section_file.exists():
                report_path = section_file.with_suffix('.report.json')
                section_data = analyzer.load_section_data(str(section_file))
                
                if section_data:
                    analyzer.save_analysis_report(section_data, str(report_path))
                    print(f"  - Report generated for {success['file']}")
    
    return len(results['success']) > 0


def analyze_existing_data(data_dir: str = "data/section_analysis") -> None:
    """
    Analyze existing section data and generate comprehensive reports.
    
    Args:
        data_dir (str): Directory containing section data files
    """
    logger = logging.getLogger(__name__)
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return
    
    # Find all section files
    section_files = list(data_path.glob("*_sections.json"))
    
    if not section_files:
        logger.info(f"No section files found in {data_dir}")
        return
    
    print(f"\n{'='*60}")
    print("Section Analysis Dashboard")
    print(f"{'='*60}")
    print(f"Found {len(section_files)} papers with section data")
    
    analyzer = SectionAnalyzer()
    
    # Analyze each paper
    all_analyses = []
    for section_file in section_files:
        print(f"\nAnalyzing: {section_file.name}")
        
        analysis = analyze_paper_sections(str(section_file))
        if analysis:
            all_analyses.append({
                'file': section_file.name,
                'analysis': analysis
            })
            
            print(f"  - Sections: {analysis.get('total_sections', 0)}")
            print(f"  - Types: {', '.join(analysis.get('section_types', {}).keys())}")
            print(f"  - Average length: {analysis.get('average_section_length', 0)} words")
    
    # Generate comparison report
    if len(all_analyses) > 1:
        print(f"\n{'='*60}")
        print("Comparative Analysis")
        print(f"{'='*60}")
        
        comparison = analyzer.compare_papers_by_sections([str(f) for f in section_files])
        
        print(f"Average sections per paper: {comparison.get('average_sections_per_paper', 0):.1f}")
        print(f"\nCommon section types:")
        for section_type, frequency in sorted(comparison.get('section_frequency', {}).items(), 
                                            key=lambda x: x[1], reverse=True):
            percentage = (frequency / len(all_analyses)) * 100
            print(f"  - {section_type.title()}: {frequency}/{len(all_analyses)} papers ({percentage:.1f}%)")
        
        # Save comparison report
        comparison_path = data_path / "comparison_report.json"
        with open(comparison_path, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        print(f"\nComparison report saved to {comparison_path}")


def compare_papers(data_dir: str = "data/section_analysis") -> None:
    """
    Compare multiple papers based on their section structure.
    
    Args:
        data_dir (str): Directory containing section data files
    """
    logger = logging.getLogger(__name__)
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return
    
    section_files = list(data_path.glob("*_sections.json"))
    
    if len(section_files) < 2:
        logger.info("Need at least 2 papers to compare")
        return
    
    analyzer = SectionAnalyzer()
    comparison = analyzer.compare_papers_by_sections([str(f) for f in section_files])
    
    print(f"\n{'='*60}")
    print("Paper Comparison Report")
    print(f"{'='*60}")
    
    print(f"Total papers compared: {len(comparison['papers'])}")
    print(f"Average sections per paper: {comparison.get('average_sections_per_paper', 0):.1f}")
    
    print(f"\nPaper Details:")
    for paper in comparison['papers']:
        print(f"  - {paper['file']}: {paper['section_count']} sections")
        print(f"    Types: {', '.join(paper['section_types'])}")
    
    print(f"\nSection Frequency Analysis:")
    for section_type, frequency in sorted(comparison.get('section_frequency', {}).items(), 
                                        key=lambda x: x[1], reverse=True):
        percentage = (frequency / len(comparison['papers'])) * 100
        print(f"  - {section_type.title()}: {frequency}/{len(comparison['papers'])} papers ({percentage:.1f}%)")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract and analyze section-wise text data from research papers"
    )
    
    parser.add_argument(
        "--process-all",
        action="store_true",
        help="Process all PDFs in Downloaded_pdfs directory"
    )
    
    parser.add_argument(
        "--pdf",
        type=str,
        help="Process a specific PDF file"
    )
    
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze existing section data"
    )
    
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare multiple papers by section structure"
    )
    
    parser.add_argument(
        "--pdf-dir",
        type=str,
        default="Downloaded_pdfs",
        help="Directory containing PDF files (default: Downloaded_pdfs)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/section_analysis",
        help="Directory to save section data (default: data/section_analysis)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate arguments
    if not any([args.process_all, args.pdf, args.analyze, args.compare]):
        parser.error("Must specify one of: --process-all, --pdf, --analyze, --compare")
    
    try:
        if args.process_all:
            success = process_all_pdfs(args.pdf_dir, args.output_dir)
            sys.exit(0 if success else 1)
        
        elif args.pdf:
            success = process_single_pdf(args.pdf, args.output_dir)
            sys.exit(0 if success else 1)
        
        elif args.analyze:
            analyze_existing_data(args.output_dir)
        
        elif args.compare:
            compare_papers(args.output_dir)
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
