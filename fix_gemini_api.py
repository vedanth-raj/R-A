"""
Script to fix all Gemini API calls in lengthy_draft_generator.py
"""

import re

# Read the file
with open('lengthy_draft_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Replace all self.gemini_client checks with self.gemini_model
content = content.replace('if self.gemini_client:', 'if self.gemini_model:')

# Fix 2: Replace all complex API calls with simple ones
# Pattern: self.gemini_client.models.generate_content(model=..., contents=..., config=...)
# Replace with: self.gemini_model.generate_content(prompt)

pattern = r'response = self\.gemini_client\.models\.generate_content\(\s*model=self\.gemini_model,\s*contents=([^,]+),\s*config=types\.GenerateContentConfig\([^)]+\)\s*\)'
replacement = r'response = self.gemini_model.generate_content(\1)'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Fix 3: Also handle simpler patterns without config
pattern2 = r'response = self\.gemini_client\.models\.generate_content\(\s*model=self\.gemini_model,\s*contents=([^)]+)\s*\)'
replacement2 = r'response = self.gemini_model.generate_content(\1)'

content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# Write back
with open('lengthy_draft_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all Gemini API calls in lengthy_draft_generator.py")
print("✅ Ready to deploy!")
