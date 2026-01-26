"""
Test enhanced generator with Gemini
"""

import os
from enhanced_gpt_generator import EnhancedGPTDraftGenerator

def test_enhanced_generator():
    """Test enhanced generator with Gemini"""
    
    print("🤖 Testing Enhanced AI Generator")
    print("=" * 40)
    
    # Set environment variables directly
    os.environ['GEMINI_API_KEY'] = "AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM"
    
    try:
        # Initialize generator
        generator = EnhancedGPTDraftGenerator(preferred_provider="gemini")
        
        print(f"✅ Available providers: {generator.available_providers}")
        print(f"🎯 Best provider: {generator.get_best_provider()}")
        
        # Test with sample data
        sample_papers = [
            {
                "title": "AI in Medical Diagnosis", 
                "summary": "This study examines AI applications in medical diagnosis, showing 85% accuracy compared to 70% for traditional methods.",
                "key_findings": ["Improved diagnostic accuracy", "Reduced false positives", "Faster processing time"],
                "implications": "AI could revolutionize medical diagnosis and reduce healthcare costs"
            },
            {
                "title": "Machine Learning in Treatment Planning",
                "summary": "Research on ML algorithms for personalized treatment planning shows 40% reduction in planning time.",
                "key_findings": ["Personalized treatment plans", "Reduced planning time", "Better patient outcomes"],
                "implications": "ML enables more efficient and effective healthcare delivery"
            }
        ]
        
        # Generate test section
        print("\n📝 Generating abstract with Gemini...")
        draft = generator.generate_section_draft("abstract", sample_papers)
        
        print(f"✅ Generation successful!")
        print(f"🤖 AI Provider: {draft.ai_provider}")
        print(f"📊 Word count: {draft.word_count}")
        print(f"🎯 Confidence: {draft.confidence_score:.2f}")
        print(f"⏱️  Generation time: {draft.generation_time:.2f}s")
        print(f"📄 Content preview: {draft.content[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_generator()
    
    if success:
        print("\n🎉 Enhanced AI Generator working perfectly!")
        print("✅ Gemini AI integration successful")
        print("🚀 Ready for production use")
    else:
        print("\n⚠️  Generator test failed")
