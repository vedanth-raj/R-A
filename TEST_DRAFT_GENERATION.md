# Test Draft Generation - Quick Guide

## Fixed Issue
✅ JavaScript error "Cannot read properties of null (reading 'style')" has been fixed

## How to Test

### 1. Start the Web App
```bash
python web_app.py
```

### 2. Open Browser
Navigate to: http://localhost:5000

### 3. Prepare Papers
- Go to "Search" tab
- Search for papers (e.g., "machine learning")
- Wait for download to complete
- Go to "Extract" tab
- Click "Extract All PDFs"
- Wait for extraction to complete

### 4. Generate Draft
- Go to "Draft Generator" tab
- Enter research topic (e.g., "Machine Learning Applications")
- Select section type (Abstract, Introduction, etc.)
- Check boxes next to papers you want to use
- Click "Generate Single Draft" or "Generate Comprehensive Draft"

### 5. Verify Success
- ✅ No JavaScript errors in browser console (F12)
- ✅ Progress bar appears and updates
- ✅ Draft content displays after generation
- ✅ No "Cannot read properties of null" error

## What Was Fixed
- Added null checks before accessing DOM element properties
- Functions now handle missing elements gracefully
- Better error logging for debugging

## If Issues Persist
1. Check browser console (F12) for errors
2. Verify papers are extracted (check data/extracted_texts/)
3. Ensure Gemini API key is set in .env file
4. Check web_app.py logs for backend errors

---
**Status**: ✅ Ready to test
