# How to Get Semantic Scholar API Key (Step-by-Step)

## Why You Need This
Without an API key, you'll get **429 rate limit errors** when searching for papers.
With a free API key, you can search reliably without errors.

---

## Step-by-Step Instructions

### Step 1: Go to Semantic Scholar Website
Open your browser and go to:
```
https://www.semanticscholar.org/product/api
```

### Step 2: Click "Get Started" or "Sign Up"
Look for buttons like:
- "Get API Key"
- "Sign Up"
- "Create Account"
- "Get Started"

### Step 3: Create Account
Fill in:
- **Email**: Your email address
- **Password**: Create a strong password
- **Name**: Your name (optional)
- **Organization**: Your institution or "Personal" (optional)

Click "Sign Up" or "Create Account"

### Step 4: Verify Email
1. Check your email inbox
2. Look for email from Semantic Scholar
3. Click verification link
4. Return to Semantic Scholar website

### Step 5: Access API Keys
After logging in:
1. Click your profile icon (top-right)
2. Go to "Account Settings" or "API Keys"
3. Look for "API Keys" section
4. Click "Generate New Key" or "Create API Key"

### Step 6: Copy Your API Key
Your API key will look like:
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

**Important**: Copy it immediately! You may not see it again.

### Step 7: Add to .env File

#### Option A: Using Text Editor
1. Open `.env` file in your project folder
2. Add this line at the end:
   ```
   SEMANTIC_SCHOLAR_API_KEY=paste_your_key_here
   ```
3. Save the file

#### Option B: Using Command Line
```bash
echo SEMANTIC_SCHOLAR_API_KEY=your_key_here >> .env
```

### Step 8: Verify .env File
Your `.env` file should now look like:
```
GEMINI_API_KEY=AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM
SEMANTIC_SCHOLAR_API_KEY=your_actual_key_here
```

### Step 9: Restart Application
```bash
# Stop current app (Ctrl+C)
# Then restart:
python web_app.py
```

### Step 10: Test It Works
1. Open http://localhost:5000
2. Go to "Search" tab
3. Search for: "machine learning"
4. Should work without errors! ✅

---

## Visual Guide

```
┌─────────────────────────────────────────────────┐
│ 1. Go to semanticscholar.org/product/api       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. Click "Get API Key" or "Sign Up"            │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. Fill in email, password, name                │
│    Click "Create Account"                       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Check email → Click verification link        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 5. Log in → Go to Account Settings              │
│    Find "API Keys" section                      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 6. Click "Generate New Key"                     │
│    Copy the key (long string of characters)     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 7. Open .env file                               │
│    Add: SEMANTIC_SCHOLAR_API_KEY=your_key       │
│    Save file                                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 8. Restart: python web_app.py                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 9. Test search → Should work! ✅                │
└─────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Can't Find "Get API Key" Button
- Try: https://www.semanticscholar.org/me/research
- Or: https://api.semanticscholar.org/
- Look for "API" or "Developers" in menu

### Email Not Received
- Check spam/junk folder
- Wait 5-10 minutes
- Try resending verification email
- Use different email address

### Can't Find API Keys Section
After logging in:
1. Click your name/profile (top-right)
2. Try these menu items:
   - "Settings"
   - "Account"
   - "API Keys"
   - "Developer"
   - "Integrations"

### API Key Not Working
1. Verify key is copied correctly (no spaces)
2. Check .env file format:
   ```
   SEMANTIC_SCHOLAR_API_KEY=key_here
   ```
   (No quotes, no spaces around =)
3. Restart application completely
4. Check logs for "Using Semantic Scholar API key"

---

## Alternative: Contact Support

If you can't get an API key:
1. Email: api@semanticscholar.org
2. Explain you need API key for academic research
3. They usually respond within 1-2 business days

---

## What You Get (Free Tier)

✅ **100 requests per 5 minutes**
✅ **1 request per second**
✅ **Unlimited searches** (within rate limits)
✅ **No credit card required**
✅ **Free forever** for academic use
✅ **Priority access** over unauthenticated users

---

## Security Tips

🔒 **Keep Your Key Secret**
- Don't share with others
- Don't commit to GitHub
- Don't post in public forums

🔒 **If Key is Compromised**
- Generate new key on Semantic Scholar
- Update .env file
- Revoke old key

---

## Quick Commands

### Check if key is loaded:
```bash
# In Python:
python -c "from config import SEMANTIC_SCHOLAR_API_KEY; print('Key loaded!' if SEMANTIC_SCHOLAR_API_KEY else 'No key')"
```

### Test API key directly:
```bash
curl -H "x-api-key: your_key_here" "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1"
```

---

## Summary

1. ✅ Go to: https://www.semanticscholar.org/product/api
2. ✅ Sign up for free account
3. ✅ Get API key from account settings
4. ✅ Add to .env file: `SEMANTIC_SCHOLAR_API_KEY=your_key`
5. ✅ Restart app: `python web_app.py`
6. ✅ Test search → No more 429 errors!

---

**Time Required**: 5-10 minutes
**Cost**: FREE
**Benefit**: Reliable paper searches without rate limit errors

---

**Need Help?** Check `FIX_RATE_LIMIT_ERROR.md` for more details.
