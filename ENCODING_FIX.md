# Unicode Encoding Fix for Windows Console

## Problem
Windows console (cmd.exe and PowerShell) uses CP1252 encoding by default, which cannot display Unicode characters like Greek letters (α, β, γ), mathematical symbols, or special characters commonly found in academic paper titles.

## Error Example
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u03b1' in position 11: character maps to <undefined>
```

## Solution Implemented

### 1. Encoding Fix Utility (`utils/encoding_fix.py`)
Created a reusable utility module that:
- Automatically configures console to use UTF-8 encoding
- Provides `safe_print()` function for fallback printing
- Works with Python 3.7+ and earlier versions

### 2. Updated Scripts
Added encoding fixes to:
- `main.py` - Paper search and download
- `ai_research_agent.py` - Main research agent
- `start_web_interface.py` - Web interface launcher

### 3. How It Works
```python
from utils.encoding_fix import fix_console_encoding, safe_print

# Fix encoding at script start
fix_console_encoding()

# Use safe_print for Unicode text
safe_print(f"Paper title: {title_with_unicode}")
```

## Usage

### For New Scripts
Add this at the top of any script that prints to console:
```python
from utils.encoding_fix import fix_console_encoding
fix_console_encoding()
```

### For Existing Code
Replace problematic `print()` calls with `safe_print()`:
```python
from utils.encoding_fix import safe_print

# Instead of:
# print(f"Title: {paper.title}")

# Use:
safe_print(f"Title: {paper.title}")
```

## Alternative: Set Console Encoding Manually

### PowerShell
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### CMD
```cmd
chcp 65001
```

## Testing
The fix has been tested with paper titles containing:
- Greek letters (α, β, γ, etc.)
- Mathematical symbols
- Special Unicode characters
- Emoji and other symbols

All scripts now handle these characters gracefully.
