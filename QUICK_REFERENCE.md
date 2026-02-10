# Quick Reference Guide

## 🚀 Start Applications

### Enhanced Flask App (Recommended)
```bash
python futuristic_flask_app.py
```
Then open: **http://localhost:8080**

### Original Research System
```bash
python main.py "your research topic" --max-papers 5 --generate-draft
```

## 📝 Draft Generation

### Via Web Interface (http://localhost:8080)
1. Enter topic
2. Select papers (1-10)
3. Click "START RESEARCH"
4. Wait for complete workflow
5. View generated draft at bottom

### Via Command Line
```bash
# Basic
python main.py "AI in healthcare" --generate-draft

# With options
python main.py "quantum computing" --max-papers 10 --randomize --generate-draft

# Output location
./data/papers/generated_draft.txt
```

## 🎨 Features

### Enhanced Flask App
- ✅ Plasma waves with mouse repulsion
- ✅ Glassmorphic design
- ✅ Real-time progress
- ✅ Paper retrieval
- ✅ Key findings analysis
- ✅ Lengthy draft (3000-4000 words)
- ✅ APA references

### Command Line
- ✅ Paper search & download
- ✅ Metadata extraction
- ✅ Lengthy draft generation
- ✅ APA formatting
- ✅ Gemini AI powered

## 📊 Draft Sections

All drafts include:
1. **Abstract** (300-400 words)
2. **Introduction** (800-1000 words)
3. **Methods** (700-900 words)
4. **Results** (900-1200 words)
5. **Discussion** (900-1200 words)
6. **References** (APA format)

**Total: 3,400-4,700 words**

## 🔧 Troubleshooting

### Flask app not loading?
```bash
# Stop and restart
Ctrl+C
python futuristic_flask_app.py
```

### Draft not generating?
- Check Gemini API key in `.env`
- System falls back to templates automatically
- Check console for errors

### Unicode errors?
- Already fixed with encoding_fix.py
- Should work automatically

## 📍 Currently Running

- Port 5000: Original Flask
- Port 7861: Gradio (diagonal rays)
- **Port 8080: Enhanced Flask (plasma waves)** ⭐

## 💡 Tips

1. **Best experience**: Use http://localhost:8080
2. **Quick drafts**: Use command line with `--generate-draft`
3. **More papers**: Increase `--max-papers` (max 10)
4. **Variety**: Add `--randomize` flag

## ✅ Everything Works!

Both systems fully functional with comprehensive draft generation.
