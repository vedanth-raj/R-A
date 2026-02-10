# How to Use Draft Generator - Step by Step Guide

## Quick Start (5 Minutes)

### Step 1: Start the Web App
```bash
python web_app.py
```
Open browser: **http://localhost:5000**

---

### Step 2: Search for Papers
1. Click **"Search"** tab (first tab)
2. Enter topic: `machine learning` or `artificial intelligence`
3. Set max papers: `3-5`
4. Click **"Search Papers"**
5. Wait for search to complete (10-30 seconds)

**What you'll see:**
- Progress bar appears
- "Search completed successfully" notification
- Papers appear in search results

---

### Step 3: Extract Text from PDFs
1. Click **"Extract"** tab (second tab)
2. Click **"Extract All PDFs"** button
3. Wait for extraction (5-15 seconds)

**What you'll see:**
- Progress bar: "Extracting text from PDFs..."
- "Text extraction completed. X papers processed" notification

---

### Step 4: Generate Draft
1. Click **"Draft Generator"** tab (fourth tab)
2. **Enter Research Topic**: 
   - Example: "Machine Learning in Healthcare"
   - Example: "Deep Learning for Image Recognition"
3. **Select Section Type**:
   - Abstract (short, 200-400 words)
   - Introduction (longer, 600-800 words)
   - Methodology, Results, Discussion, or References
4. **Select Papers**:
   - Check boxes next to papers you want to use
   - Minimum: 1 paper
   - Recommended: 2-3 papers for better quality
5. Click **"Generate Single Draft"** button

**What you'll see:**
- Progress bar: "Generating draft..."
- Takes 5-15 seconds (Gemini API processing)
- Draft appears below with:
  - Title: "Generated Draft"
  - Section name (e.g., "Abstract Section")
  - Word count and confidence score
  - **Full draft content** (readable, formatted text)

---

### Step 5: Generate Comprehensive Draft (Optional)
1. Same setup as Step 4
2. Click **"Generate Comprehensive Draft"** instead
3. Wait 30-60 seconds (generates multiple sections)

**What you'll see:**
- Title: "Comprehensive Draft"
- Multiple sections:
  - Abstract
  - Introduction
  - Methodology
  - Results
  - Discussion
  - References
- Each section shows:
  - Section name
  - Word count
  - Confidence score
  - **Full content**

---

## What the Draft Looks Like

### Single Draft Example:
```
┌──────────────────────────────────────────────────┐
│ 📄 Generated Draft                               │
├──────────────────────────────────────────────────┤
│ 📄 Abstract Section                              │
│ Word Count: 350 | Confidence: 85.0%             │
├──────────────────────────────────────────────────┤
│                                                  │
│ This comprehensive systematic review examines    │
│ the current state of machine learning in         │
│ healthcare, analyzing 3 peer-reviewed studies    │
│ published between 2020 and 2024. The primary    │
│ objective is to synthesize existing knowledge... │
│                                                  │
│ [Full draft content continues...]               │
│ [Scrollable if content is long]                 │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Comprehensive Draft Example:
```
┌──────────────────────────────────────────────────┐
│ 📄 Comprehensive Draft                           │
├──────────────────────────────────────────────────┤
│ Abstract                                         │
│ Word Count: 350 | Confidence: 85.0%            │
│ [Full abstract content...]                      │
├──────────────────────────────────────────────────┤
│ Introduction                                     │
│ Word Count: 650 | Confidence: 82.0%            │
│ [Full introduction content...]                  │
├──────────────────────────────────────────────────┤
│ Methodology                                      │
│ Word Count: 500 | Confidence: 88.0%            │
│ [Full methodology content...]                   │
├──────────────────────────────────────────────────┤
│ [More sections...]                              │
└──────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Problem: No papers to select
**Solution**: 
- Go to Extract tab first
- Click "Extract All PDFs"
- Wait for extraction to complete
- Return to Draft Generator tab

### Problem: "Please enter a research topic"
**Solution**: 
- Fill in the "Research Topic" field
- Must not be empty

### Problem: Draft generation takes too long
**Possible causes**:
- Gemini API rate limiting
- Large papers being processed
- Network issues

**Solution**:
- Wait up to 60 seconds
- Check browser console (F12) for errors
- Verify Gemini API key in .env file

### Problem: Draft not visible after generation
**Solution**: 
- Scroll down on the page
- Check if "Generated Draft" title appears
- Refresh page and try again
- Check browser console for JavaScript errors

### Problem: Low confidence score (<60%)
**Causes**:
- Not enough papers selected
- Papers not relevant to topic
- Poor quality extracted text

**Solution**:
- Select more papers (3-5 recommended)
- Use more relevant papers
- Try different section type

---

## Tips for Best Results

### 1. Choose Good Topics
✅ **Good Examples:**
- "Machine Learning in Climate Prediction"
- "CRISPR Gene Editing Applications"
- "Deep Learning for Medical Diagnosis"

❌ **Too Broad:**
- "Science"
- "Technology"
- "Research"

❌ **Too Narrow:**
- "Specific protein XYZ123 in mice"

### 2. Select Relevant Papers
- Read paper titles before selecting
- Choose papers related to your topic
- Mix different perspectives (2-3 papers minimum)

### 3. Section Types
- **Abstract**: Quick overview (200-400 words)
- **Introduction**: Background and context (600-800 words)
- **Methodology**: Research methods comparison
- **Results**: Findings synthesis
- **Discussion**: Implications and analysis
- **References**: APA-formatted citations

### 4. Comprehensive vs Single Draft
- **Single Draft**: Fast, one section only
- **Comprehensive**: Slow, all sections, complete review

---

## Features

### ✅ What Works
- Search papers from Semantic Scholar
- Download PDFs automatically
- Extract text from PDFs
- Generate AI-powered drafts using Gemini
- Single section drafts (5-15 seconds)
- Comprehensive multi-section drafts (30-60 seconds)
- Real-time progress updates
- Confidence scoring
- Word count tracking
- Dark-themed interface

### 🚧 Coming Soon
- Copy to clipboard
- Download as PDF/DOCX
- Edit draft functionality
- Save draft history
- Share drafts

---

## System Requirements
- Python 3.8+
- Gemini API key (in .env file)
- Internet connection
- Modern browser (Chrome, Firefox, Edge)

---

## Need Help?
1. Check browser console (F12) for errors
2. Check terminal for backend errors
3. Verify .env file has GEMINI_API_KEY
4. Ensure papers are extracted before generating drafts

---

**Web App**: http://localhost:5000
**Status**: ✅ Ready to use
**Last Updated**: February 10, 2026
