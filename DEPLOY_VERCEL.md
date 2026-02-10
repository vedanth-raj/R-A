# Deploy to Vercel - Step by Step Guide

## ⚠️ Important Limitations

**Vercel has limitations for this application:**
- ❌ **No WebSocket support** (Flask-SocketIO won't work)
- ❌ **10-second timeout** for serverless functions
- ❌ **Limited file storage** (ephemeral filesystem)
- ❌ **No background tasks**

**Recommendation**: Use AWS instead for full functionality.

However, if you want to deploy a **simplified version** without real-time features:

---

## Prerequisites

1. **GitHub account** (your code is already there)
2. **Vercel account** (free tier available)
3. **API keys** ready

---

## Step 1: Prepare for Vercel

### 1.1 Create Simplified Web App

Create `web_app_vercel.py`:

```python
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

# Add other routes without WebSocket

if __name__ == '__main__':
    app.run()
```

### 1.2 Update vercel.json

Already created! File: `vercel.json`

### 1.3 Update requirements

Use `requirements-vercel.txt` (already created)

---

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel**:
   ```
   https://vercel.com
   ```

2. **Sign in** with GitHub

3. **Import Project**:
   - Click "Add New" → "Project"
   - Select your repository: `research-bot`
   - Select branch: `Vedanth_Raj`

4. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

5. **Add Environment Variables**:
   Click "Environment Variables":
   ```
   GEMINI_API_KEY = your_gemini_key
   SEMANTIC_SCHOLAR_API_KEY = your_semantic_scholar_key
   ```

6. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your URL: `https://your-app.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Follow prompts:
# - Link to existing project? No
# - Project name: research-bot
# - Directory: ./
# - Override settings? No

# 5. Add environment variables
vercel env add GEMINI_API_KEY
vercel env add SEMANTIC_SCHOLAR_API_KEY

# 6. Deploy to production
vercel --prod
```

---

## Step 3: Configure Environment Variables

### Via Vercel Dashboard:

1. Go to your project on Vercel
2. Click "Settings"
3. Click "Environment Variables"
4. Add:
   ```
   GEMINI_API_KEY = AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM
   SEMANTIC_SCHOLAR_API_KEY = Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld
   ```
5. Click "Save"
6. Redeploy

---

## Step 4: Test Deployment

1. **Visit your URL**:
   ```
   https://your-app.vercel.app
   ```

2. **Test basic functionality**:
   - Homepage loads ✅
   - Search works (without real-time updates) ✅
   - Static features work ✅

3. **Known limitations**:
   - No real-time progress updates ❌
   - No WebSocket features ❌
   - File uploads may not persist ❌

---

## Troubleshooting

### Error: "Function execution timed out"
**Cause**: Vercel has 10-second timeout
**Solution**: 
- Reduce processing time
- Use background jobs (Vercel doesn't support)
- **Switch to AWS** (recommended)

### Error: "Module not found"
**Cause**: Missing dependencies
**Solution**:
```bash
# Update requirements-vercel.txt
# Redeploy
```

### Error: "Environment variable not found"
**Cause**: API keys not set
**Solution**:
- Add in Vercel dashboard
- Redeploy

---

## Limitations Summary

### What Works on Vercel:
✅ Static pages
✅ Basic API endpoints
✅ Simple searches (with timeout)

### What Doesn't Work:
❌ Real-time updates (WebSocket)
❌ Long-running tasks (>10s)
❌ File persistence
❌ Background jobs
❌ Draft generation (too slow)

---

## Recommendation

**For full functionality, use AWS instead!**

Vercel is great for:
- Static sites
- Next.js apps
- Simple APIs

But your app needs:
- WebSockets
- Long-running tasks
- File storage
- Background processing

**→ See DEPLOY_AWS.md for full deployment**

---

## Alternative: Vercel + External Services

If you want to use Vercel:

1. **Deploy frontend** on Vercel (static HTML/JS)
2. **Deploy backend** on AWS/Heroku/Railway
3. **Connect** frontend to backend API

This gives you:
- Fast frontend (Vercel CDN)
- Full backend features (AWS)

---

## Cost

**Vercel Free Tier**:
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Serverless functions
- ❌ Limited execution time
- ❌ No WebSocket support

**Vercel Pro** ($20/month):
- Same limitations for WebSockets
- Not worth it for this app

**Recommendation**: Use AWS Free Tier instead

---

## Next Steps

1. ❌ **Don't use Vercel** for this app (too limited)
2. ✅ **Use AWS** instead (see DEPLOY_AWS.md)
3. ✅ **Or use Railway/Render** (easier than AWS)

---

**Status**: ⚠️ Not Recommended
**Reason**: WebSocket and long-running task limitations
**Alternative**: AWS, Railway, or Render
