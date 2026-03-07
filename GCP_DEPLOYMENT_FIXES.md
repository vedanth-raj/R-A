# GCP Deployment Fixes - LitWise AI

This document summarizes the fixes applied to make the app fully functional on Google Cloud Platform (App Engine).

## Issues Fixed

### 1. **Paper search not working**
- **Problem**: Search used `subprocess.run(["python", "main.py", ...])` which fails on GCP (no subprocess, wrong paths).
- **Fix**: Replaced subprocess with direct Python API calls (SemanticScholarSearcher, PaperSelector, PDFDownloader). Papers are now fetched in-process.

### 2. **Papers not visible / operations appear to hang**
- **Problem**: WebSocket is disabled on GCP (gunicorn doesn't support it), but the frontend never polled for operation completion.
- **Fix**: Added `pollOperationStatus()` that polls `/api/operation_status/<id>` every 1.5 seconds until search, extract, analyze, draft, etc. complete. Users now see results.

### 3. **API keys not working**
- **Problem**: Config paths and env detection may have been incorrect.
- **Fix**: 
  - Improved `IS_APP_ENGINE` detection (GAE_ENV, K_SERVICE, GAE_APPLICATION).
  - Data dirs use `/tmp/data` on GCP (writable).
  - Added `/api/health` endpoint to verify API keys are configured.
  - API keys from `app.yaml` env_variables are passed to the app.

### 4. **File paths on GCP**
- **Fix**: All file operations (papers, extracted texts) use `config.PAPERS_DIR` and `config.EXTRACTED_TEXTS_DIR`, which resolve to `/tmp/data/...` on App Engine.

### 5. **Session storage**
- **Fix**: Switched to default Flask cookie-based session (works on read-only GCP filesystem).

### 6. **Download button**
- **Fix**: Search results download button now uses `paper.filename` correctly and handles paths from GCP.

## Deploy to GCP

```bash
gcloud app deploy
```

## Verify Deployment

1. **Health check**: Visit `https://YOUR_APP_URL/api/health`
   - Should return `{"status": "ok", "semantic_scholar_configured": true, "gemini_configured": true}`

2. **Search for papers**: Enter a topic (e.g. "machine learning"), click Search. Wait ~30–60 seconds. Papers should appear.

3. **Extract text**: After search, click "Extract Text from All PDFs" to extract text from downloaded papers.

4. **Generate draft**: Select papers, enter topic, generate draft (requires Gemini API key).

## API Keys

- **Semantic Scholar**: For paper search. Get from https://www.semanticscholar.org/product/api
- **Gemini**: For AI draft generation. Get from https://aistudio.google.com/apikey

Keys are configured in `app.yaml` under `env_variables`. For production, consider using [Secret Manager](https://cloud.google.com/secret-manager).

## Note on Data Persistence

On App Engine, `/tmp` is **ephemeral**—data is lost when instances scale down. Each request may hit a different instance. For production with persistent storage, consider Cloud Storage or Firestore.
