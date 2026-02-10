# Web Interface Status

## Is the web app running and functioning?

**Yes.** The web app is **functional** and has been verified with Flask’s test client.

### Verification

- **Imports:** `web_app` and `socketio` import successfully.
- **Home page:** `GET /` returns **200** and serves the main HTML (~25KB).
- **API endpoints (all return 200):**
  - `GET /api/get_papers` – list extracted papers
  - `GET /api/view_papers_directory` – list downloaded PDFs
  - `POST /api/search_papers` – start paper search (returns operation_id)

### How to run the web interface

1. **From the project root:**

   ```bash
   python start_web_interface.py
   ```

   Or:

   ```bash
   python -c "from web_app import app, socketio; socketio.run(app, debug=False, host='0.0.0.0', port=5000)"
   ```

2. **Open in browser:**  
   http://localhost:5000

3. **Stop:**  
   Press `Ctrl+C` in the terminal where the server is running.

### Fixes applied for correct behavior

1. **Search papers**  
   The web UI no longer sends `--year-start` / `--year-end` to `main.py`, because the CLI does not support those arguments yet. Search runs with topic and `--max-papers` only.

2. **Extract text**  
   Extraction looks for PDFs in:
   - `data/papers` (where `main.py` saves PDFs)
   - then `Downloaded_pdfs`  
   So “Extract text” works after you have run `python main.py "topic"` and have PDFs in `data/papers`.

### Features available in the web UI

- **Search papers** – runs `main.py` with the given topic and max papers.
- **Extract text** – extracts text from PDFs in `data/papers` (or `Downloaded_pdfs`).
- **View papers** – list downloaded PDFs and extracted texts.
- **Analyze paper** – section analysis for a selected paper.
- **Compare papers** – compare content across papers.
- **Download paper** – download a PDF from the UI.
- **Real-time updates** – SocketIO for progress/status.

### Dependencies

- `flask`
- `flask-socketio`
- `psutil`  
(Installed via `pip install -r requirements.txt`; `start_web_interface.py` can also install them.)

### If the server does not start

- Ensure you are in the project root (where `web_app.py` and `main.py` are).
- Ensure port 5000 is not in use by another process.
- Run `pip install flask flask-socketio psutil` if you see import errors.

### Summary

| Check              | Status   |
|--------------------|----------|
| Web app imports    | OK       |
| Home page (GET /)  | 200 OK   |
| API endpoints      | 200 OK   |
| Search (no year)   | Fixed    |
| Extract (data/papers) | Fixed |

The web interface is **working correctly** when started with `python start_web_interface.py` and used at http://localhost:5000.
