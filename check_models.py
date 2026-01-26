"""
Check available Gemini models
"""

import google.genai as genai

def check_models():
    """Check available Gemini models"""
    
    api_key = "AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM"
    
    print("🔍 Checking Available Gemini Models")
    print("=" * 40)
    
    try:
        client = genai.Client(api_key=api_key)
        
        # List available models
        models = client.models.list()
        
        print("📋 Available Models:")
        for model in models:
            print(f"  - {model.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_models()
