"""
Quick test of Gemini API with timeout
"""
import os
import time
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
    from google.genai import types
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("Testing Gemini API...")
        print(f"API Key: {api_key[:20]}...")
        
        client = genai.Client(api_key=api_key)
        
        # Test simple generation
        print("\nTest 1: Simple generation")
        start = time.time()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Write a 50-word abstract about machine learning.",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=100
                )
            )
            elapsed = time.time() - start
            print(f"✅ Success in {elapsed:.2f} seconds")
            print(f"Response: {response.text[:100]}...")
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ Failed after {elapsed:.2f} seconds: {e}")
        
        # Test with custom instructions
        print("\nTest 2: With custom instructions")
        start = time.time()
        try:
            prompt = """Write a concise academic abstract (250-350 words) for a review on "machine learning" analyzing 3 papers.

USER INSTRUCTIONS: Focus on recent advances

Incorporate these instructions while maintaining quality."""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=600
                )
            )
            elapsed = time.time() - start
            print(f"✅ Success in {elapsed:.2f} seconds")
            print(f"Response length: {len(response.text)} characters")
            print(f"Word count: {len(response.text.split())} words")
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ Failed after {elapsed:.2f} seconds: {e}")
    else:
        print("No API key found")
        
except ImportError:
    print("google.genai not installed")
except Exception as e:
    print(f"Error: {e}")
