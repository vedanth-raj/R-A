# Quick Start Guide 🚀

## Get Started in 30 Seconds

### 1. Start the Plasma Waves UI
```bash
python futuristic_flask_app.py
```

### 2. Open Your Browser
Navigate to: **http://localhost:8080**

### 3. Use the Interface
1. Enter a research topic (e.g., "machine learning in healthcare")
2. Adjust number of papers (1-10)
3. Click **"START RESEARCH"**
4. Watch the magic happen! ✨

---

## What You'll See

### Interactive Plasma Waves 🌊
- 5 glowing orange-gold energy waves
- Move your mouse → waves bend away
- Move away → waves spring back smoothly
- Cosmic gradient background

### Real-Time Progress 📊
- Planning → Searching → Downloading → Analyzing → Synthesizing → Complete
- Live progress bar
- Status updates every step

### Results Display 📚
1. **Retrieved Papers** - Table with titles, authors, years, citations
2. **Key Findings** - Themes, overlaps, research gaps
3. **Generated Draft** - Complete systematic review:
   - Abstract
   - Introduction
   - Methods
   - Results
   - Discussion
   - APA References

---

## Troubleshooting

### Rate Limit Errors (429)
**Problem**: Too many API requests without key
**Solution**: Add Semantic Scholar API key to `.env`:
```
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```
Get free key: https://www.semanticscholar.org/product/api

### Port Already in Use
**Problem**: Port 8080 is busy
**Solution**: Stop other processes or change port in `futuristic_flask_app.py`:
```python
socketio.run(app, debug=False, host='0.0.0.0', port=8081)
```

### No Papers Found
**Problem**: Search returns no results
**Solution**: 
- Try broader search terms
- Check internet connection
- Add API key to avoid rate limits

---

## Alternative Interfaces

### Gradio App (Diagonal Rays)
```bash
python futuristic_gradio_app.py
```
URL: http://localhost:7861

### Original Flask App
```bash
python start_web_interface.py
```
URL: http://localhost:5000

### Command Line Interface
```bash
python main.py "your topic" --max-papers 5
```

---

## Features

### ✨ UI Features
- Interactive plasma waves with mouse repulsion
- Glassmorphic design with backdrop blur
- Neon orange-gold accents
- Smooth animations and transitions
- Responsive design (mobile-friendly)
- Real-time WebSocket updates

### 🔬 Research Features
- Semantic Scholar paper search
- PDF download and text extraction
- Section-wise analysis
- Key findings extraction
- Comprehensive draft generation
- APA-formatted references

### 🛠️ Technical Features
- Pure Flask + Flask-SocketIO backend
- Canvas-based animations
- Physics simulation (spring forces)
- WebSocket real-time communication
- Gemini API integration
- UTF-8 encoding support

---

## Tips for Best Results

### 1. Choose Good Topics
✅ Good: "machine learning in climate prediction"
✅ Good: "CRISPR gene editing applications"
❌ Too broad: "science"
❌ Too narrow: "specific protein XYZ123"

### 2. Adjust Paper Count
- **1-3 papers**: Quick overview
- **4-6 papers**: Balanced review
- **7-10 papers**: Comprehensive analysis

### 3. Wait for Complete Results
- Don't refresh during processing
- Watch progress bar
- All sections appear progressively

---

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- Modern browser (Chrome, Firefox, Edge)
- Internet connection

### Recommended
- Python 3.10+
- 8GB RAM
- Chrome/Edge (best canvas performance)
- Semantic Scholar API key

---

## File Locations

### Generated Files
- **Papers**: `data/papers/` or `Downloaded_pdfs/`
- **Extracted Text**: `data/extracted_texts/`
- **Metadata**: `data/selected_papers.json`
- **Logs**: `ai_research_agent.log`, `performance_monitor.log`

### Configuration
- **API Keys**: `.env`
- **Settings**: `config.py`

---

## Need Help?

### Check Documentation
- `README.md` - Main documentation
- `FINAL_COMPLETE_STATUS.md` - Complete status
- `PLASMA_WAVES_COMPLETE.md` - UI implementation details

### Common Issues
1. **SSL Errors**: Fixed! (verify=False added)
2. **Unicode Errors**: Fixed! (UTF-8 encoding)
3. **Rate Limits**: Add API key to `.env`

---

## Enjoy Your Research! 🎉

The system is ready to help you conduct systematic literature reviews with a stunning, futuristic interface.

**Start now**: `python futuristic_flask_app.py`

**Access**: http://localhost:8080

---

*Happy Researching! 📚✨*
