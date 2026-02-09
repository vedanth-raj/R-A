# API Key Setup Guide

## Current Issue: Rate Limit Exceeded

The app is currently hitting Semantic Scholar API rate limits (429 errors) because it's using unauthenticated access.

## Semantic Scholar API Key (Recommended for Higher Rate Limits)

### Why Use an API Key?

The Semantic Scholar API works without authentication, but using an API key gives you:

- **Dedicated rate limit:** 1 request per second (1 RPS) per key, instead of a shared limit
- **More reliable usage:** Less risk of throttling during peak traffic
- **Better support:** Easier to get help if something goes wrong

### How to Get Your API Key

1. **Open the API key form**
   - Go to: https://www.semanticscholar.org/product/api#api-key-form
   - Fill in your project details

2. **Receive your key**
   - You'll get your private API key by email
   - **Do not share this key** or commit it to version control

3. **Configure the project**

   **Option A: `.env` file (recommended)**  
   Create a `.env` file in the project root and add:

   ```
   SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
   ```

   **Option B: Environment variable**

   - **Windows PowerShell:**
     ```powershell
     $env:SEMANTIC_SCHOLAR_API_KEY="your_actual_api_key_here"
     ```
   - **Windows Command Prompt:**
     ```cmd
     set SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
     ```
   - **Linux / macOS:**
     ```bash
     export SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
     ```

## Gemini API Key (For Draft Generation)

The new draft generation feature requires Gemini API:

### Getting Gemini API Key:
1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it to your `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Complete .env File Example:
```
# Semantic Scholar API Key for paper search
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key_here

# Gemini API Key for draft generation
GEMINI_API_KEY=your_gemini_key_here
```

## Quick Fix for Current Issue

### Option 1: Add API Keys (Recommended)
1. Create `.env` file in project root
2. Add both API keys as shown above
3. Restart the application

### Option 2: Use Existing Papers
If you have papers in the `Downloaded_pdfs/` folder:
1. Go to the "Extract Text" tab
2. Extract text from existing PDFs
3. Skip the search step entirely

### Option 3: Wait and Retry
Unauthenticated access has shared rate limits. Wait a few minutes and try again.

## Check That Keys Are Working

When you run the app, you should see in the logs:

```
Using Semantic Scholar API key (rate limit: 1 RPS cumulative across all endpoints)
Gemini client initialized for lengthy draft generation
```

If you see:
```
No API key provided - using unauthenticated access (shared rate limit)
```

then the key is not being loaded (e.g. wrong `.env` path or missing variable).

## Rate Limit Information

- **Without API Key**: Shared limit (you're hitting this now)
- **With API Key**: 1 request per second (dedicated, more reliable)
- **Current Issue**: Too many 429 errors = rate limit exceeded

## Security

- Do not commit `.env` or your API keys to git (`.env` should be in `.gitignore`)
- If keys are exposed, request new ones from the respective services

## References

- [Semantic Scholar API overview](https://www.semanticscholar.org/product/api)
- [API key form](https://www.semanticscholar.org/product/api#api-key-form)
- [Google AI Studio (Gemini)](https://makersuite.google.com/app/apikey)
