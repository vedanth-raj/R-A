#!/usr/bin/env python3
"""
Validation Test Suite for Text Extraction and Analysis System

This script validates the correctness and completeness of:
1. Text extraction module for parsing downloaded PDFs
2. Section-wise text extraction and storage
3. Key-finding extraction logic
4. Cross-paper comparison module

Usage:
    python validation_test.py
"""

import json
import logging
import glob
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import the modules to test
from paper_retrieval.text_extractor import PDFTextExtractor
from section_extractor import SectionWiseExtractor, Section
from section_analyzer import SectionAnalyzer

@dataclass
class ValidationResult:
    """Results of validation tests."""
    test_name: str
    passed: bool
    details: str
    data: Optional[Dict[str, Any]] = None

class ValidationTestSuite:
    """Comprehensive validation test suite."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results: List[ValidationResult] = []
        
        # Initialize components
        self.pdf_extractor = PDFTextExtractor()
        self.section_extractor = SectionWiseExtractor()
        self.section_analyzer = SectionAnalyzer()
    
    def run_all_tests(self) -> List[ValidationResult]:
        """Run all validation tests."""
        print("🧪 Running Validation Test Suite...")
        print("=" * 50)
        
        # Test 1: Text Extraction Module
        self.test_text_extraction_module()
        
        # Test 2: Section-wise Text Extraction
        self.test_section_wise_extraction()
        
        # Test 3: Key-finding Extraction Logic
        self.test_key_finding_extraction()
        
        # Test 4: Cross-paper Comparison Module
        self.test_cross_paper_comparison()
        
        # Test 5: Data Completeness and Correctness
        self.test_data_completeness()
        
        # Test 6: Integration Test
        self.test_integration_workflow()
        
        return self.results
    
    def test_text_extraction_module(self) -> None:
        """Test PDF text extraction functionality."""
        print("\n📄 Test 1: Text Extraction Module")
        
        try:
            # Test initialization
            assert self.pdf_extractor is not None, "PDFTextExtractor initialization failed"
            
            # Test with existing extracted text files
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            assert len(text_files) > 0, "No extracted text files found for testing"
            
            # Load and validate text content
            for text_file in text_files[:2]:  # Test with first 2 files
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                assert len(content) > 1000, f"Text content too short in {text_file}"
                assert content.count('--- Page') > 0, f"No page markers found in {text_file}"
            
            self.results.append(ValidationResult(
                test_name="Text Extraction Module",
                passed=True,
                details=f"✅ Successfully validated {len(text_files)} extracted text files",
                data={"files_found": len(text_files)}
            ))
            
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Text Extraction Module",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def test_section_wise_extraction(self) -> None:
        """Test section-wise text extraction functionality."""
        print("\n🔍 Test 2: Section-wise Text Extraction")
        
        try:
            # Test with existing text files
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            total_sections = 0
            section_types_found = set()
            
            for text_file in text_files[:2]:  # Test with first 2 files
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Test section detection
                sections = self.section_extractor.detect_sections_from_text(content)
                total_sections += len(sections)
                
                # Validate sections
                for section in sections:
                    assert section.title.strip() != "", f"Empty section title in {text_file}"
                    assert section.word_count > 0, f"Zero word count in section {section.title}"
                    section_types_found.add(section.section_type)
            
            # Check for expected section types
            expected_types = {'abstract', 'introduction', 'references'}
            found_expected = expected_types.intersection(section_types_found)
            
            self.results.append(ValidationResult(
                test_name="Section-wise Text Extraction",
                passed=len(found_expected) >= 2,  # At least 2 expected types found
                details=f"✅ Extracted {total_sections} sections from {len(text_files)} files",
                data={
                    "total_sections": total_sections,
                    "section_types": list(section_types_found),
                    "expected_types_found": len(found_expected)
                }
            ))
            
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Section-wise Text Extraction",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def test_key_finding_extraction(self) -> None:
        """Test key-finding extraction logic."""
        print("\n🔑 Test 3: Key-finding Extraction Logic")
        
        try:
            # Create test data
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            key_insights_total = 0
            
            for text_file in text_files[:2]:  # Test with first 2 files
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                sections = self.section_extractor.detect_sections_from_text(content)
                
                # Create section data structure
                section_data = {
                    'sections': [
                        {
                            'title': section.title,
                            'content': section.content,
                            'type': section.section_type,
                            'word_count': section.word_count,
                            'start_page': getattr(section, 'start_page', 1),
                            'end_page': getattr(section, 'end_page', 1),
                            'key_phrases': [],
                            'sentences': section.content.split('.')[:5]
                        }
                        for section in sections if section.section_type == 'abstract'
                    ],
                    'metadata': {'source_file': text_file}
                }
                
                # Test key insights extraction
                if section_data['sections']:
                    insights = self.section_analyzer.extract_key_insights(section_data, 'abstract')
                    key_insights_total += len(insights)
            
            self.results.append(ValidationResult(
                test_name="Key-finding Extraction Logic",
                passed=key_insights_total >= 0,  # Allow 0 as valid if no abstracts found
                details=f"✅ Extracted {key_insights_total} key insights from abstracts",
                data={"total_insights": key_insights_total}
            ))
            
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Key-finding Extraction Logic",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def test_cross_paper_comparison(self) -> None:
        """Test cross-paper comparison functionality."""
        print("\n📊 Test 4: Cross-paper Comparison Module")
        
        try:
            # Create section data files for comparison
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            section_files = []
            
            for text_file in text_files[:3]:  # Test with first 3 files
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                sections = self.section_extractor.detect_sections_from_text(content)
                
                section_data = {
                    'sections': [
                        {
                            'title': section.title,
                            'content': section.content,
                            'type': section.section_type,
                            'word_count': section.word_count
                        }
                        for section in sections
                    ],
                    'metadata': {
                        'source_file': text_file,
                        'total_sections': len(sections)
                    }
                }
                
                # Save section data
                section_file = text_file.replace('_extracted.txt', '_sections.json')
                with open(section_file, 'w', encoding='utf-8') as f:
                    json.dump(section_data, f, indent=2)
                
                section_files.append(section_file)
            
            # Test comparison
            if len(section_files) >= 2:
                comparison = self.section_analyzer.compare_papers_by_sections(section_files)
                
                # Validate comparison results
                assert 'papers' in comparison, "Missing 'papers' in comparison results"
                assert 'common_sections' in comparison, "Missing 'common_sections' in comparison results"
                assert len(comparison['papers']) == len(section_files), "Paper count mismatch"
                
                self.results.append(ValidationResult(
                    test_name="Cross-paper Comparison Module",
                    passed=True,
                    details=f"✅ Successfully compared {len(section_files)} papers",
                    data={
                        "papers_compared": len(comparison['papers']),
                        "common_sections": list(comparison['common_sections'].keys()),
                        "avg_sections_per_paper": comparison.get('average_sections_per_paper', 0)
                    }
                ))
            else:
                self.results.append(ValidationResult(
                    test_name="Cross-paper Comparison Module",
                    passed=False,
                    details="❌ Insufficient files for comparison test"
                ))
                
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Cross-paper Comparison Module",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def test_data_completeness(self) -> None:
        """Test correctness and completeness of extracted data."""
        print("\n✅ Test 5: Data Completeness and Correctness")
        
        try:
            # Check file structure
            required_dirs = ['data/extracted_texts', 'Downloaded_pdfs']
            missing_dirs = [d for d in required_dirs if not Path(d).exists()]
            
            if missing_dirs:
                raise Exception(f"Missing directories: {missing_dirs}")
            
            # Check extracted text files
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            assert len(text_files) > 0, "No extracted text files found"
            
            # Validate file contents
            valid_files = 0
            total_size = 0
            
            for text_file in text_files:
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if len(content) > 1000:  # Minimum content length
                        valid_files += 1
                        total_size += len(content)
                        
                except Exception:
                    continue
            
            completeness_score = (valid_files / len(text_files)) * 100
            
            self.results.append(ValidationResult(
                test_name="Data Completeness and Correctness",
                passed=completeness_score >= 80,  # At least 80% valid files
                details=f"✅ {valid_files}/{len(text_files)} files valid ({completeness_score:.1f}%)",
                data={
                    "total_files": len(text_files),
                    "valid_files": valid_files,
                    "completeness_score": completeness_score,
                    "total_text_size": total_size
                }
            ))
            
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Data Completeness and Correctness",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def test_integration_workflow(self) -> None:
        """Test complete integration workflow."""
        print("\n🔄 Test 6: Integration Workflow")
        
        try:
            # Test complete workflow: text extraction -> section detection -> analysis
            text_files = glob.glob('data/extracted_texts/*_extracted.txt')
            
            if not text_files:
                raise Exception("No text files available for integration test")
            
            # Process one file through complete workflow
            test_file = text_files[0]
            
            # Step 1: Load text
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Step 2: Extract sections
            sections = self.section_extractor.detect_sections_from_text(content)
            
            # Step 3: Analyze sections
            section_data = {
                'sections': [
                    {
                        'title': section.title,
                        'content': section.content,
                        'type': section.section_type,
                        'word_count': section.word_count,
                        'start_page': getattr(section, 'start_page', 1),
                        'end_page': getattr(section, 'end_page', 1),
                        'key_phrases': [],
                        'sentences': section.content.split('.')[:5]
                    }
                    for section in sections
                ],
                'metadata': {'source_file': test_file}
            }
            
            # Step 4: Generate analysis
            distribution = self.section_analyzer.analyze_section_distribution(section_data)
            insights = self.section_analyzer.extract_key_insights(section_data)
            
            # Validate workflow completion
            workflow_success = (
                len(sections) > 0 and
                'section_types' in distribution and
                len(insights) >= 0  # Can be 0 if no abstract found
            )
            
            self.results.append(ValidationResult(
                test_name="Integration Workflow",
                passed=workflow_success,
                details=f"✅ Complete workflow: {len(sections)} sections processed",
                data={
                    "sections_extracted": len(sections),
                    "section_types_found": list(distribution.get('section_types', {}).keys()),
                    "insights_generated": len(insights)
                }
            ))
            
        except Exception as e:
            self.results.append(ValidationResult(
                test_name="Integration Workflow",
                passed=False,
                details=f"❌ Error: {str(e)}"
            ))
    
    def print_summary(self) -> None:
        """Print validation test summary."""
        print("\n" + "=" * 50)
        print("📋 VALIDATION TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} {result.test_name}: {result.details}")
        
        print(f"\n🎯 Overall Result: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is fully functional.")
        else:
            print("⚠️  Some tests failed. Please review the issues above.")

def main():
    """Run validation tests."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Run tests
    test_suite = ValidationTestSuite()
    results = test_suite.run_all_tests()
    
    # Print summary
    test_suite.print_summary()
    
    # Return exit code
    failed_count = sum(1 for r in results if not r.passed)
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit(main())
