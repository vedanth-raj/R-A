# Fix Rate Limit Error (429) - Semantic Scholar API

## Error Message
```
Search failed: too many 429 error responses
HTTPSConnectionPool(host='api.semanticscholar.org', port=443): Max retries exceeded
```

## What This Means
- **429 = Rate Limit Exceeded**
- You're making too many requests without an API key
- Semantic Scholar limits unauthenticated requests very strictly
- The limit is shared across ALL users without API keys

## Solution: Get a Free API Key

### Step 1: Sign Up for Semantic Scholar API
1. Go to: **https://www.semanticscholar.org/product/api**
2. Click **"Get API Key"** or **"Sign Up"**
3. Create a free account (email + password)
4. Verify your email
5. Go to your account settings
6. Find your API key (looks like: `abc123xyz456...`)

### Step 2: Add API Key to .env File
1. Open `.env` file in your project root
2. Add this line (replace with your actual key):
   ```
   SEMANTIC_SCHOLAR_API_KEY=your_actual_api_key_here
   ```
3. Save the file

**Example .env file:**
```
GEMINI_API_KEY=AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```

### Step 3: Restart the Application
```bash
# Stop current process (Ctrl+C in terminal)
# Then restart:
python web_app.py
```

### Step 4: Test Search Again
1. Go to http://localhost:5000
2. Click "Search" tab
3. Enter topic: "machine learning"
4. Click "Search Papers"
5. Should work now! ✅

## Benefits of Using API Key

### Without API Key (Current):
- ❌ Very strict rate limits
- ❌ Shared limit with all users
- ❌ Frequent 429 errors
- ❌ Can't search reliably

### With API Key (After Fix):
- ✅ 100 requests per 5 minutes
- ✅ Personal rate limit (not shared)
- ✅ Reliable searches
- ✅ Better performance
- ✅ Priority access

## Alternative: Wait and Retry

If you can't get an API key immediately:

### Option 1: Wait 5-10 Minutes
- Rate limits reset after time
- Try searching again later
- Not recommended for regular use

### Option 2: Use Different Search Terms
- Sometimes helps avoid cached rate limits
- Try more specific queries
- Still limited without API key

### Option 3: Reduce Number of Papers
- In search form, set "Max Papers" to 1-2
- Reduces API calls
- Still may hit rate limits

## Checking If API Key Works

After adding the key, you should see in logs:
```
✅ GOOD:
INFO - Using Semantic Scholar API key (rate limit: 1 RPS cumulative)

❌ BAD:
INFO - No API key provided - using unauthenticated access
```

## Troubleshooting

### Problem: Still getting 429 errors after adding key
**Solutions:**
1. Verify key is correct (no extra spaces)
2. Restart the application completely
3. Check .env file encoding (should be UTF-8)
4. Verify key is active on Semantic Scholar website

### Problem: Can't find API key on Semantic Scholar
**Solutions:**
1. Log in to semanticscholar.org
2. Go to Account Settings
3. Look for "API Keys" or "Developer" section
4. Generate new key if needed

### Problem: .env file not loading
**Solutions:**
1. Verify file is named exactly `.env` (not `env.txt`)
2. File should be in project root directory
3. Check file encoding (UTF-8)
4. Restart application after changes

## Rate Limits with API Key

### Free Tier (With API Key):
- **100 requests per 5 minutes**
- **1 request per second** (cumulative across all endpoints)
- Sufficient for most research tasks
- Can search 20-30 papers per session

### Usage Examples:
- Search 5 papers: ~5 seconds
- Search 10 papers: ~10 seconds
- Search 20 papers: ~20 seconds

## Important Notes

1. **Keep API Key Secret**: Don't share or commit to GitHub
2. **One Key Per User**: Each person should get their own key
3. **Free Forever**: Semantic Scholar API is free for academic use
4. **No Credit Card**: Free tier doesn't require payment info

## Quick Reference

### Get API Key:
https://www.semanticscholar.org/product/api

### Add to .env:
```
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```

### Restart App:
```bash
python web_app.py
```

### Test:
Search for papers → Should work without 429 errors ✅

---

## Status After Fix
✅ Reliable paper searches
✅ No more rate limit errors
✅ Better performance
✅ Ready for regular use

---

**Next Step**: Get your free API key and add it to `.env` file!
