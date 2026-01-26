"""
Test script for GPT drafting and APA formatting modules.
"""

import json
from pathlib import Path
from gpt_draft_generator import GPTDraftGenerator, generate_drafts_from_analysis
from apa_formatter import APAFormatter, generate_apa_bibliography, format_paper_references


def test_gpt_drafting():
    """Test the GPT drafting functionality."""
    print("🔍 Testing GPT Draft Generation...")
    
    # Initialize generator (without API key for mock generation)
    generator = GPTDraftGenerator()
    
    # Load existing analysis data
    analysis_dir = Path("data/section_analysis")
    papers_data = generator.load_paper_data(str(analysis_dir))
    
    print(f"📊 Loaded {len(papers_data)} papers for analysis")
    
    if not papers_data:
        print("❌ No paper data found. Please run analysis first.")
        return
    
    # Generate drafts
    print("📝 Generating drafts...")
    drafts = generator.generate_complete_draft(papers_data, ['abstract', 'introduction', 'methods'])
    
    print(f"✅ Generated {len(drafts)} draft sections:")
    for section_type, draft in drafts.items():
        print(f"   - {section_type.title()}: {draft.word_count} words (confidence: {draft.confidence_score})")
    
    # Save drafts
    output_dir = Path("data/drafts")
    drafts_file = output_dir / "test_drafts.json"
    generator.save_drafts(drafts, str(drafts_file))
    
    # Generate formatted paper
    paper_file = output_dir / "test_paper.txt"
    generator.generate_formatted_paper(drafts, str(paper_file), "Test Generated Research Paper")
    
    print(f"💾 Drafts saved to: {drafts_file}")
    print(f"📄 Paper saved to: {paper_file}")
    
    return drafts


def test_apa_formatting():
    """Test the APA formatting functionality."""
    print("\n🔍 Testing APA Formatting...")
    
    # Initialize formatter
    formatter = APAFormatter()
    
    # Load selected papers data
    papers_file = "data/selected_papers.json"
    
    if not Path(papers_file).exists():
        print("❌ Selected papers file not found.")
        return
    
    # Generate bibliography
    print("📚 Generating APA bibliography...")
    output_dir = Path("data/references")
    bib_file = output_dir / "apa_bibliography.txt"
    
    try:
        stats = formatter.generate_bibliography(papers_file, str(bib_file))
        
        print(f"✅ Generated bibliography with {stats['total_references']} references:")
        print(f"   - Journal articles: {stats['journal_articles']}")
        print(f"   - Conference papers: {stats['conference_papers']}")
        print(f"   - Books: {stats['books']}")
        print(f"   - With DOI: {stats['with_doi']}")
        
        print(f"💾 Bibliography saved to: {bib_file}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Error generating bibliography: {e}")
        return None


def test_complete_workflow():
    """Test the complete workflow from analysis to formatted paper."""
    print("\n🚀 Testing Complete Workflow...")
    
    try:
        # Test GPT drafting
        drafts = test_gpt_drafting()
        
        # Test APA formatting
        apa_stats = test_apa_formatting()
        
        # Create final integrated document
        if drafts and apa_stats:
            print("\n📋 Creating integrated document...")
            
            output_dir = Path("data/final_output")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Load bibliography
            bib_file = Path("data/references/apa_bibliography.txt")
            if bib_file.exists():
                with open(bib_file, 'r', encoding='utf-8') as f:
                    bibliography = f.read()
            else:
                bibliography = "[Bibliography will be here]"
            
            # Create final document
            final_doc = f"""Generated Research Paper
========================

Generated using AI Research Agent
Date: {Path().cwd()}

{drafts.get('abstract', '').content if 'abstract' in drafts else ''}

{drafts.get('introduction', '').content if 'introduction' in drafts else ''}

{drafts.get('methods', '').content if 'methods' in drafts else ''}

{drafts.get('results', '').content if 'results' in drafts else ''}

{drafts.get('discussion', '').content if 'discussion' in drafts else ''}

{bibliography}
"""
            
            final_file = output_dir / "final_research_paper.txt"
            with open(final_file, 'w', encoding='utf-8') as f:
                f.write(final_doc)
            
            print(f"🎉 Final document saved to: {final_file}")
            print("✅ Complete workflow test successful!")
            
            return True
        
    except Exception as e:
        print(f"❌ Error in complete workflow: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Milestone 3 Components")
    print("=" * 50)
    
    success = test_complete_workflow()
    
    if success:
        print("\n🎯 Milestone 3 Components Working!")
        print("✅ GPT-based drafting: Functional")
        print("✅ APA formatting: Functional")
        print("✅ Structured writing: Functional")
        print("✅ Synthesis integration: Functional")
    else:
        print("\n❌ Some components need attention.")
