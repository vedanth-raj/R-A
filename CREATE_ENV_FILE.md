# Create `.env` File for API Keys

## Purpose

The `.env` file holds secrets (e.g. Semantic Scholar API key) so they are not hard-coded or committed to git.

## Semantic Scholar API Key

1. Get a key from: https://www.semanticscholar.org/product/api#api-key-form  
2. Create a file named `.env` in the project root (same folder as `main.py`).  
3. Add one line:

   ```
   SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
   ```

4. Save the file. The app will load it via `python-dotenv` in `config.py`.

## Rate limit

- **Limit:** 1 request per second (1 RPS), cumulative across all endpoints.  
- The app uses `REQUEST_DELAY_SECONDS` in `config.py` and tracks request times to stay under this limit.

## Windows: Create `.env` with PowerShell

```powershell
cd "C:\Users\YourName\Downloads\R_A"
"SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here" | Out-File -FilePath .env -Encoding ASCII -NoNewline
```

Replace `YourName` and `your_actual_key_here` with your path and key.

## Windows: Create `.env` with Command Prompt

```cmd
cd C:\Users\YourName\Downloads\R_A
echo SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here > .env
```

## Linux / macOS

```bash
cd /path/to/R_A
echo 'SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here' > .env
```

## Verify

Run:

```bash
python main.py "test" --max-papers 1
```

If the key is loaded, the log will show:

```
Using Semantic Scholar API key (rate limit: 1 RPS cumulative across all endpoints)
```

## Security

- `.env` is listed in `.gitignore`; do not remove it from there.  
- Never commit `.env` or share your API key.  
- If the key is compromised, generate a new one from Semantic Scholar.
