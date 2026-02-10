# Quick Setup: Semantic Scholar API Key

## 1. Create `.env`

Create a file named `.env` in the project root (same folder as `main.py` and `config.py`).

## 2. Add your key

Put this line in `.env` (replace with your real key):

```
SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
```

- No spaces around `=`
- No quotes around the value
- Save the file

## 3. Rate limit

Your key is limited to **1 request per second (1 RPS), cumulative across all endpoints**.

The app is set up to:

- Wait at least `REQUEST_DELAY_SECONDS` between requests (see `config.py`)
- Track request times so it doesn’t exceed 1 RPS
- Retry with backoff if you get rate limit errors (e.g. 429)

## 4. Check that it works

Run:

```bash
python main.py "test query" --max-papers 1
```

You should see in the log:

```
Using Semantic Scholar API key (rate limit: 1 RPS cumulative across all endpoints)
```

If you see “No API key provided”, the `.env` file isn’t being loaded (path or variable name).

## 5. Security

- Don’t commit `.env` to git (it should be in `.gitignore`)
- Keep your API key private

## 6. Optional: Create `.env` from the command line

**PowerShell (Windows):**

```powershell
cd "C:\path\to\your\project"
"SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here" | Out-File -FilePath .env -Encoding ASCII -NoNewline
```

**Bash (Linux/macOS):**

```bash
cd /path/to/your/project
echo 'SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here' > .env
```

Replace `your_actual_key_here` and the path with your real key and project path.
