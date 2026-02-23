# 🛠️ Tech Stack - AI Research Agent

## 📋 Complete Technology Stack

### **Backend Technologies**

#### **Core Framework**
- **Python 3.13** - Primary programming language
- **Flask 2.3+** - Web application framework
- **Flask-SocketIO 5.3+** - Real-time bidirectional communication

#### **AI & Machine Learning**
- **LangChain 0.1+** - LLM application framework
- **LangGraph 0.0.26+** - Graph-based LLM workflows
- **LangSmith 0.0.87+** - LLM observability and debugging
- **OpenAI API 1.12+** - GPT models integration
- **Google Gemini API** - Alternative LLM provider
- **Hugging Face Hub 0.20+** - Model repository access

#### **Document Processing**
- **PyMuPDF 1.26+** - PDF text extraction
- **pymupdf4llm 0.0.8+** - LLM-optimized PDF processing
- **ReportLab 4.0+** - PDF generation and formatting
- **pdfplumber** - Advanced PDF parsing
- **BeautifulSoup4** - HTML/XML parsing

#### **Data & APIs**
- **Semantic Scholar API** - Academic paper search
- **Requests 2.31+** - HTTP client library
- **Pydantic 2.5+** - Data validation and settings management

#### **Text Processing**
- **tiktoken 0.5+** - OpenAI tokenization
- **regex** - Advanced pattern matching
- **lxml** - XML/HTML processing

#### **Database & Storage**
- **psycopg 3.1+** - PostgreSQL adapter (optional)
- **JSON** - Local data storage
- **File System** - PDF and text storage

#### **Utilities**
- **python-dotenv 1.0+** - Environment variable management
- **tqdm 4.66+** - Progress bars
- **psutil 5.9+** - System and process monitoring
- **grandalf 0.6+** - Graph algorithms

---

### **Frontend Technologies**

#### **Core**
- **HTML5** - Markup language
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Client-side logic

#### **Libraries & Frameworks**
- **Socket.IO Client** - Real-time communication
- **Fetch API** - HTTP requests
- **DOM API** - Dynamic content manipulation

#### **UI Components**
- **Font Awesome** - Icon library
- **Custom CSS** - Dark theme design
- **Responsive Design** - Mobile-friendly layout

#### **Features**
- **Real-time Updates** - WebSocket-based progress tracking
- **Drag & Drop** - File upload interface
- **Dynamic Forms** - Interactive user inputs
- **Notifications** - Toast-style alerts

---

### **Development & Deployment**

#### **Version Control**
- **Git** - Source control
- **GitHub** - Repository hosting

#### **Deployment Platforms**
- **Ngrok** - Local development tunneling
- **Vercel** - Serverless deployment (alternative)
- **Docker** - Containerization (optional)

#### **Development Tools**
- **VS Code / Cursor** - Code editor
- **Python Virtual Environment** - Dependency isolation
- **pip** - Package management

---

### **Architecture & Patterns**

#### **Design Patterns**
- **MVC Pattern** - Model-View-Controller separation
- **Repository Pattern** - Data access abstraction
- **Factory Pattern** - Object creation
- **Observer Pattern** - Event-driven updates

#### **Architecture**
- **Client-Server** - Web-based architecture
- **RESTful API** - HTTP endpoints
- **WebSocket** - Real-time communication
- **Modular Design** - Separated concerns

---

### **Key Features & Technologies**

#### **1. Paper Search & Retrieval**
```
Semantic Scholar API → Python Requests → JSON Storage
```

#### **2. PDF Processing**
```
PyMuPDF → Text Extraction → Section Analysis → JSON
```

#### **3. AI Draft Generation**
```
LangChain → OpenAI/Gemini → Prompt Engineering → Text Output
```

#### **4. PDF Export**
```
ReportLab → Formatted PDF → File Download
```

#### **5. Real-time Updates**
```
Flask-SocketIO → WebSocket → JavaScript Client → UI Updates
```

#### **6. Conversational AI**
```
LangChain → Context Management → Multi-turn Dialogue
```

---

### **API Integrations**

| Service | Purpose | Authentication |
|---------|---------|----------------|
| **Semantic Scholar** | Paper search & metadata | API Key |
| **OpenAI GPT** | Draft generation | API Key |
| **Google Gemini** | Alternative LLM | API Key |
| **Ngrok** | Public URL tunneling | Auth Token |

---

### **File Structure**

```
📁 Project Root
├── 📁 paper_retrieval/      # Paper search & download
├── 📁 static/               # Frontend assets
│   ├── 📁 css/             # Stylesheets
│   └── 📁 js/              # JavaScript
├── 📁 templates/            # HTML templates
├── 📁 data/                 # Data storage
│   ├── 📁 papers/          # Downloaded PDFs
│   ├── 📁 extracted_texts/ # Extracted content
│   └── 📁 generated_pdfs/  # Generated PDFs
├── 📁 utils/                # Utility functions
├── 📄 web_app.py            # Main Flask application
├── 📄 pdf_generator.py      # PDF generation
├── 📄 lengthy_draft_generator.py  # Draft generation
├── 📄 ai_conversation_engine.py   # Conversational AI
├── 📄 section_extractor.py  # PDF section parsing
├── 📄 requirements.txt      # Python dependencies
└── 📄 .env                  # Environment variables
```

---

### **Performance Optimizations**

- **Async Operations** - Non-blocking I/O
- **Progress Tracking** - Real-time feedback
- **Caching** - Session-based data storage
- **Lazy Loading** - On-demand resource loading
- **Error Handling** - Graceful degradation

---

### **Security Features**

- **Environment Variables** - Secure API key storage
- **CORS Configuration** - Cross-origin security
- **Input Validation** - Pydantic models
- **Error Sanitization** - Safe error messages
- **Session Management** - User isolation

---

### **Browser Compatibility**

- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ IE11 (Limited support)

---

### **System Requirements**

#### **Development**
- Python 3.10+
- 4GB RAM minimum
- 2GB free disk space
- Internet connection

#### **Production**
- Python 3.10+
- 8GB RAM recommended
- 5GB free disk space
- Stable internet connection

---

### **Third-Party Services**

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| **Semantic Scholar** | ✅ Yes | N/A |
| **OpenAI API** | ❌ No | Pay-per-use |
| **Google Gemini** | ✅ Yes | Pay-per-use |
| **Ngrok** | ✅ Yes (2hr sessions) | $8/month+ |
| **Vercel** | ✅ Yes | $20/month+ |

---

### **Development Timeline**

- **Phase 1**: Paper search & retrieval ✅
- **Phase 2**: PDF processing & extraction ✅
- **Phase 3**: AI draft generation ✅
- **Phase 4**: Web interface ✅
- **Phase 5**: Real-time features ✅
- **Phase 6**: Conversational AI ✅
- **Phase 7**: PDF export ✅
- **Phase 8**: Deployment ✅

---

### **Future Enhancements**

- 🔄 Database integration (PostgreSQL)
- 🔄 User authentication
- 🔄 Multi-user support
- 🔄 Citation management
- 🔄 Export to Word/LaTeX
- 🔄 Advanced analytics
- 🔄 Mobile app

---

### **License & Credits**

- **Framework**: Flask (BSD License)
- **AI**: LangChain (MIT License)
- **PDF**: ReportLab (BSD License)
- **Icons**: Font Awesome (Free License)

---

## 📊 Technology Summary

| Category | Technologies |
|----------|-------------|
| **Backend** | Python, Flask, Flask-SocketIO |
| **AI/ML** | LangChain, OpenAI, Gemini |
| **Frontend** | HTML5, CSS3, JavaScript, Socket.IO |
| **Document** | PyMuPDF, ReportLab, pdfplumber |
| **Data** | JSON, File System, PostgreSQL (optional) |
| **Deployment** | Ngrok, Vercel, Docker |
| **APIs** | Semantic Scholar, OpenAI, Gemini |

---

**Total Dependencies**: 20+ Python packages
**Lines of Code**: ~5000+ (estimated)
**Supported Formats**: PDF, JSON, TXT
**API Integrations**: 3 major services

---

*Last Updated: February 2026*
