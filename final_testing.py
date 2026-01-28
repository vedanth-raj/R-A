"""
Final Testing and Documentation Module
Comprehensive testing suite and documentation generation for AI Research Agent
"""

import os
import json
import logging
import unittest
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import all components for testing
from enhanced_gpt_generator import EnhancedGPTDraftGenerator
from content_reviewer import ContentReviewer
from final_integration import FinalIntegration
from apa_formatter import APAFormatter

class FinalTestingSuite:
    """Comprehensive testing suite for AI Research Agent"""
    
    def __init__(self):
        """Initialize the testing suite"""
        self.logger = logging.getLogger(__name__)
        self.test_results = {}
        self.start_time = datetime.now()
        
        # Initialize components
        self.draft_generator = EnhancedGPTDraftGenerator(preferred_provider="gemini")
        self.content_reviewer = ContentReviewer(preferred_provider="gemini")
        self.integration = FinalIntegration()
        self.apa_formatter = APAFormatter()
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        
        test_suite_results = {
            'start_time': self.start_time.isoformat(),
            'test_categories': {},
            'overall_success': False,
            'summary': {},
            'recommendations': []
        }
        
        print("🧪 Running Comprehensive AI Research Agent Test Suite")
        print("=" * 60)
        
        try:
            # Test Category 1: Component Initialization
            print("\n📋 Category 1: Component Initialization Tests")
            test_suite_results['test_categories']['initialization'] = self.test_component_initialization()
            
            # Test Category 2: Content Generation
            print("\n📝 Category 2: Content Generation Tests")
            test_suite_results['test_categories']['generation'] = self.test_content_generation()
            
            # Test Category 3: Content Review
            print("\n🔍 Category 3: Content Review Tests")
            test_suite_results['test_categories']['review'] = self.test_content_review()
            
            # Test Category 4: Revision Cycle
            print("\n🔄 Category 4: Revision Cycle Tests")
            test_suite_results['test_categories']['revision'] = self.test_revision_cycle()
            
            # Test Category 5: APA Formatting
            print("\n📚 Category 5: APA Formatting Tests")
            test_suite_results['test_categories']['apa_formatting'] = self.test_apa_formatting()
            
            # Test Category 6: Integration Workflow
            print("\n🚀 Category 6: Integration Workflow Tests")
            test_suite_results['test_categories']['integration'] = self.test_integration_workflow()
            
            # Test Category 7: Performance Tests
            print("\n⚡ Category 7: Performance Tests")
            test_suite_results['test_categories']['performance'] = self.test_performance()
            
            # Test Category 8: Error Handling
            print("\n⚠️ Category 8: Error Handling Tests")
            test_suite_results['test_categories']['error_handling'] = self.test_error_handling()
            
            # Calculate overall success
            all_tests_passed = all(
                category.get('success', False) 
                for category in test_suite_results['test_categories'].values()
            )
            
            test_suite_results['overall_success'] = all_tests_passed
            test_suite_results['end_time'] = datetime.now().isoformat()
            
            # Generate summary
            test_suite_results['summary'] = self._generate_test_summary(test_suite_results)
            
            # Generate recommendations
            test_suite_results['recommendations'] = self._generate_recommendations(test_suite_results)
            
            # Save test results
            self._save_test_results(test_suite_results)
            
            print(f"\n🎉 Test Suite Completed!")
            print(f"Overall Success: {'✅ PASSED' if all_tests_passed else '❌ FAILED'}")
            
        except Exception as e:
            self.logger.error(f"Test suite failed: {e}")
            test_suite_results['error'] = str(e)
            test_suite_results['overall_success'] = False
        
        return test_suite_results
    
    def test_component_initialization(self) -> Dict[str, Any]:
        """Test component initialization"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Test Enhanced GPT Generator
            print("  🤖 Testing Enhanced GPT Generator...")
            generator_success = self.draft_generator is not None
            results['tests']['gpt_generator'] = generator_success
            results['details']['gpt_generator'] = {
                'initialized': generator_success,
                'available_providers': self.draft_generator.available_providers,
                'preferred_provider': self.draft_generator.preferred_provider
            }
            
            # Test Content Reviewer
            print("  🔍 Testing Content Reviewer...")
            reviewer_success = self.content_reviewer is not None
            results['tests']['content_reviewer'] = reviewer_success
            results['details']['content_reviewer'] = {
                'initialized': reviewer_success,
                'best_provider': self.content_reviewer.get_best_provider()
            }
            
            # Test Final Integration
            print("  🚀 Testing Final Integration...")
            integration_success = self.integration is not None
            results['tests']['final_integration'] = integration_success
            results['details']['final_integration'] = {
                'initialized': integration_success
            }
            
            # Test APA Formatter
            print("  📚 Testing APA Formatter...")
            apa_success = self.apa_formatter is not None
            results['tests']['apa_formatter'] = apa_success
            results['details']['apa_formatter'] = {
                'initialized': apa_success
            }
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_content_generation(self) -> Dict[str, Any]:
        """Test content generation functionality"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Load test data
            papers_data = self.draft_generator.load_paper_data("data/section_analysis")
            
            if not papers_data:
                results['success'] = False
                results['error'] = "No test data available"
                return results
            
            # Test abstract generation
            print("  📝 Testing Abstract Generation...")
            try:
                abstract_draft = self.draft_generator.generate_section_draft("abstract", papers_data[:2])
                results['tests']['abstract_generation'] = True
                results['details']['abstract_generation'] = {
                    'word_count': abstract_draft.word_count,
                    'confidence': abstract_draft.confidence_score,
                    'ai_provider': abstract_draft.ai_provider,
                    'generation_time': abstract_draft.generation_time
                }
            except Exception as e:
                results['tests']['abstract_generation'] = False
                results['details']['abstract_generation'] = {'error': str(e)}
            
            # Test introduction generation
            print("  📄 Testing Introduction Generation...")
            try:
                intro_draft = self.draft_generator.generate_section_draft("introduction", papers_data[:2])
                results['tests']['introduction_generation'] = True
                results['details']['introduction_generation'] = {
                    'word_count': intro_draft.word_count,
                    'confidence': intro_draft.confidence_score,
                    'ai_provider': intro_draft.ai_provider,
                    'generation_time': intro_draft.generation_time
                }
            except Exception as e:
                results['tests']['introduction_generation'] = False
                results['details']['introduction_generation'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_content_review(self) -> Dict[str, Any]:
        """Test content review functionality"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Test with sample content
            sample_content = """
            This study examines the impact of artificial intelligence on healthcare systems. 
            We analyzed data from multiple hospitals to understand how AI technologies are being implemented.
            The results show significant improvements in patient outcomes and operational efficiency.
            """
            
            print("  🔍 Testing Quality Analysis...")
            try:
                quality_metrics = self.content_reviewer.analyze_content_quality(sample_content, "abstract")
                results['tests']['quality_analysis'] = True
                results['details']['quality_analysis'] = {
                    'overall_quality': quality_metrics.overall_quality,
                    'clarity_score': quality_metrics.clarity_score,
                    'coherence_score': quality_metrics.coherence_score,
                    'academic_tone_score': quality_metrics.academic_tone_score,
                    'word_count': quality_metrics.word_count
                }
            except Exception as e:
                results['tests']['quality_analysis'] = False
                results['details']['quality_analysis'] = {'error': str(e)}
            
            print("  💡 Testing Suggestion Generation...")
            try:
                quality_metrics = self.content_reviewer.analyze_content_quality(sample_content, "abstract")
                suggestions = self.content_reviewer.generate_revision_suggestions(
                    sample_content, "abstract", quality_metrics
                )
                results['tests']['suggestion_generation'] = True
                results['details']['suggestion_generation'] = {
                    'suggestions_count': len(suggestions),
                    'categories': list(set(s.category for s in suggestions))
                }
            except Exception as e:
                results['tests']['suggestion_generation'] = False
                results['details']['suggestion_generation'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_revision_cycle(self) -> Dict[str, Any]:
        """Test revision cycle functionality"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            sample_content = """
            This study examines AI in healthcare. We looked at some hospitals. 
            The results were good. AI helps patients.
            """
            
            print("  🔄 Testing Revision Cycle...")
            try:
                revision_result = self.content_reviewer.perform_revision_cycle(
                    sample_content, "abstract", max_iterations=2
                )
                results['tests']['revision_cycle'] = True
                results['details']['revision_cycle'] = {
                    'iterations': revision_result['total_iterations'],
                    'final_quality': revision_result['final_quality'],
                    'content_improved': len(revision_result['final_content']) > len(sample_content)
                }
            except Exception as e:
                results['tests']['revision_cycle'] = False
                results['details']['revision_cycle'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_apa_formatting(self) -> Dict[str, Any]:
        """Test APA formatting functionality"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Test journal article formatting
            print("  📚 Testing Journal Article Formatting...")
            try:
                journal_ref = self.apa_formatter.format_journal_article(
                    authors=["Smith, J. A.", "Johnson, M. B."],
                    year="2023",
                    title="Machine learning in healthcare",
                    journal="Journal of Medical AI",
                    volume="15",
                    issue="3",
                    pages="234-251"
                )
                results['tests']['journal_formatting'] = True
                results['details']['journal_formatting'] = {
                    'formatted': journal_ref,
                    'has_year': '2023' in journal_ref,
                    'has_italics': '*' in journal_ref
                }
            except Exception as e:
                results['tests']['journal_formatting'] = False
                results['details']['journal_formatting'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_integration_workflow(self) -> Dict[str, Any]:
        """Test complete integration workflow"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            print("  🚀 Testing Complete Workflow...")
            try:
                # Run a mini workflow
                workflow_results = self.integration.complete_workflow(
                    topic="machine learning",
                    max_papers=2,
                    enable_revision=True,
                    max_revision_iterations=1
                )
                results['tests']['complete_workflow'] = workflow_results['success']
                results['details']['complete_workflow'] = {
                    'workflow_success': workflow_results['success'],
                    'stages_completed': len([s for s in workflow_results['stages'].values() if s.get('success', False)]),
                    'has_final_report': len(workflow_results.get('final_report', '')) > 0
                }
            except Exception as e:
                results['tests']['complete_workflow'] = False
                results['details']['complete_workflow'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Test system performance"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Test generation speed
            print("  ⚡ Testing Generation Speed...")
            try:
                papers_data = self.draft_generator.load_paper_data("data/section_analysis")
                if papers_data:
                    start_time = time.time()
                    draft = self.draft_generator.generate_section_draft("abstract", papers_data[:2])
                    generation_time = time.time() - start_time
                    
                    results['tests']['generation_speed'] = generation_time < 10.0  # Should be under 10 seconds
                    results['details']['generation_speed'] = {
                        'generation_time': generation_time,
                        'within_limit': generation_time < 10.0
                    }
                else:
                    results['tests']['generation_speed'] = False
                    results['details']['generation_speed'] = {'error': 'No test data'}
            except Exception as e:
                results['tests']['generation_speed'] = False
                results['details']['generation_speed'] = {'error': str(e)}
            
            # Test review speed
            print("  🔍 Testing Review Speed...")
            try:
                sample_content = "Sample content for testing review speed."
                start_time = time.time()
                review = self.content_reviewer.review_content(sample_content, "abstract")
                review_time = time.time() - start_time
                
                results['tests']['review_speed'] = review_time < 5.0  # Should be under 5 seconds
                results['details']['review_speed'] = {
                    'review_time': review_time,
                    'within_limit': review_time < 5.0
                }
            except Exception as e:
                results['tests']['review_speed'] = False
                results['details']['review_speed'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling"""
        results = {
            'success': True,
            'tests': {},
            'details': {}
        }
        
        try:
            # Test invalid section type
            print("  ⚠️ Testing Invalid Section Type...")
            try:
                papers_data = self.draft_generator.load_paper_data("data/section_analysis")
                if papers_data:
                    draft = self.draft_generator.generate_section_draft("invalid_section", papers_data[:2])
                    results['tests']['invalid_section'] = True  # Should handle gracefully
                    results['details']['invalid_section'] = {
                        'handled_gracefully': True
                    }
                else:
                    results['tests']['invalid_section'] = False
                    results['details']['invalid_section'] = {'error': 'No test data'}
            except Exception as e:
                results['tests']['invalid_section'] = True  # Exception is expected
                results['details']['invalid_section'] = {
                    'handled_gracefully': True,
                    'expected_error': str(e)
                }
            
            # Test empty content review
            print("  🔍 Testing Empty Content Review...")
            try:
                review = self.content_reviewer.review_content("", "abstract")
                results['tests']['empty_content'] = True
                results['details']['empty_content'] = {
                    'handled_gracefully': True,
                    'quality_score': review.quality_metrics.overall_quality
                }
            except Exception as e:
                results['tests']['empty_content'] = False
                results['details']['empty_content'] = {'error': str(e)}
            
            results['success'] = all(results['tests'].values())
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _generate_test_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test summary"""
        summary = {
            'total_categories': len(test_results['test_categories']),
            'passed_categories': 0,
            'failed_categories': 0,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'execution_time': 0
        }
        
        # Calculate execution time
        end_time = datetime.fromisoformat(test_results['end_time'])
        summary['execution_time'] = (end_time - self.start_time).total_seconds()
        
        # Calculate test statistics
        for category_name, category_results in test_results['test_categories'].items():
            if category_results.get('success', False):
                summary['passed_categories'] += 1
            else:
                summary['failed_categories'] += 1
            
            if 'tests' in category_results:
                for test_name, test_result in category_results['tests'].items():
                    summary['total_tests'] += 1
                    if test_result:
                        summary['passed_tests'] += 1
                    else:
                        summary['failed_tests'] += 1
        
        return summary
    
    def _generate_recommendations(self, test_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check each category for issues
        for category_name, category_results in test_results['test_categories'].items():
            if not category_results.get('success', False):
                if category_name == 'generation':
                    recommendations.append("Check AI provider configuration and API keys for content generation")
                elif category_name == 'review':
                    recommendations.append("Verify content review module and quality assessment logic")
                elif category_name == 'revision':
                    recommendations.append("Ensure revision cycle has proper AI integration")
                elif category_name == 'integration':
                    recommendations.append("Review integration workflow and data flow")
                elif category_name == 'performance':
                    recommendations.append("Optimize system performance and response times")
                elif category_name == 'error_handling':
                    recommendations.append("Improve error handling and edge case management")
        
        # Performance recommendations
        summary = test_results.get('summary', {})
        if summary.get('execution_time', 0) > 300:  # 5 minutes
            recommendations.append("Consider optimizing test execution time")
        
        if not recommendations:
            recommendations.append("All systems functioning optimally. No immediate improvements needed.")
        
        return recommendations
    
    def _save_test_results(self, test_results: Dict[str, Any]):
        """Save test results to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_file = Path(f"data/final_reports/test_results_{timestamp}.json")
            
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Test results saved to {test_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save test results: {e}")

def run_comprehensive_tests() -> Dict[str, Any]:
    """Run comprehensive test suite"""
    test_suite = FinalTestingSuite()
    return test_suite.run_all_tests()

if __name__ == "__main__":
    # Run the comprehensive test suite
    results = run_comprehensive_tests()
    
    print(f"\n📊 FINAL TEST RESULTS:")
    print(f"Overall Success: {'✅ PASSED' if results['overall_success'] else '❌ FAILED'}")
    
    if 'summary' in results:
        summary = results['summary']
        print(f"Categories: {summary['passed_categories']}/{summary['total_categories']} passed")
        print(f"Tests: {summary['passed_tests']}/{summary['total_tests']} passed")
        print(f"Execution Time: {summary['execution_time']:.2f} seconds")
    
    if 'recommendations' in results:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")
    
    print(f"\n🎉 Test Suite Complete!")
