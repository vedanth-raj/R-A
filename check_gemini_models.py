"""
Check available Gemini models
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        client = genai.Client(api_key=api_key)
        
        print("Available Gemini models:")
        print("-" * 50)
        
        # Try to list models
        try:
            models = client.models.list()
            for model in models:
                print(f"- {model.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
            print("\nTrying common model names:")
            
            # Try common models
            common_models = [
                "gemini-pro",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "gemini-1.0-pro",
                "models/gemini-pro",
                "models/gemini-1.5-pro",
                "models/gemini-1.5-flash"
            ]
            
            for model_name in common_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents="Hello"
                    )
                    print(f"✅ {model_name} - WORKS")
                except Exception as e:
                    print(f"❌ {model_name} - {str(e)[:50]}")
    else:
        print("No API key found")
        
except ImportError:
    print("google.genai not installed")
