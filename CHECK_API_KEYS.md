# 🔑 Check API Keys on App Engine

## ✅ API Keys Are Set in app.yaml

Your `app.yaml` has:
```yaml
env_variables:
  GEMINI_API_KEY: "AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0"
  SEMANTIC_SCHOLAR_API_KEY: "Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld"
  SECRET_KEY: "litwise-ai-secret-2024-prod-key-secure"
```

---

## 🔍 Verify Deployment

### 1. Check if Latest Version is Deployed

```bash
# List versions
gcloud app versions list

# Should show your latest version as SERVING
```

### 2. Check Environment Variables

```bash
# View logs to see if API key is loaded
gcloud app logs read --limit=50 | grep -i "gemini\|api"
```

---

## 🚀 Redeploy to Ensure API Keys Are Applied

Sometimes environment variables don't update properly. Let's redeploy:

```bash
gcloud app deploy --stop-previous-version
```

**Type: Y**
**Wait: 3-5 minutes**

---

## 🔍 After Deployment - Test API Keys

### 1. Check Logs for Gemini Initialization

```bash
gcloud app logs tail -s default
```

Look for:
```
✅ "AI Conversation Engine initialized with Gemini"
❌ "Failed to initialize Gemini"
```

### 2. Test in Browser

1. Open your app
2. Go to "Conversational AI" tab
3. Try to chat
4. Should work now ✅

---

## 🆘 If Still Not Working

### Option 1: Check Logs

```bash
gcloud app logs read --limit=100 | grep -i "gemini"
```

### Option 2: Verify API Key is Valid

Test your Gemini API key locally:

```python
import os
import google.genai as genai

api_key = "AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0"
client = genai.Client(api_key=api_key)

# Test
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Hello, test"
)
print(response.text)
```

### Option 3: Check API Key Quota

1. Go to: https://makersuite.google.com/app/apikey
2. Check if key is active
3. Check quota/usage
4. Regenerate if needed

---

## 💡 Most Likely Issue

**Environment variables not applied** - Solution:

```bash
# Force redeploy with new environment
gcloud app deploy --stop-previous-version

# This ensures:
# 1. Old version stops
# 2. New version starts fresh
# 3. Environment variables loaded
```

---

## 🎯 Quick Fix Steps

### 1. Redeploy Now

```bash
cd C:\Users\Vedanth Raj\Downloads\R_A
gcloud app deploy --stop-previous-version
```

### 2. Wait for Deployment

```
Uploading files...
Building...
Deploying...
Done! ✅
```

### 3. Test Conversational AI

```
1. Open app
2. Go to Conversational AI tab
3. Type a message
4. Should work! ✅
```

---

## 📊 Expected Behavior After Redeploy

### Logs Should Show:
```
INFO - AI Conversation Engine initialized with Gemini ✅
INFO - Using Gemini API key ✅
```

### App Should Show:
```
Conversational AI tab:
- Chat interface ✅
- AI responds ✅
- No "API key" error ✅
```

---

## 🚀 DEPLOY NOW

```bash
gcloud app deploy --stop-previous-version
```

**The `--stop-previous-version` flag ensures clean deployment with fresh environment variables!**

---

## 🔑 Alternative: Use Google Cloud Secret Manager (Optional)

For better security, you can use Secret Manager:

### 1. Create Secret

```bash
echo -n "AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0" | gcloud secrets create gemini-api-key --data-file=-
```

### 2. Update app.yaml

```yaml
env_variables:
  GEMINI_API_KEY: "projects/YOUR_PROJECT_ID/secrets/gemini-api-key/versions/latest"
```

But for now, direct environment variables should work!

---

## ✅ DEPLOY COMMAND

```bash
gcloud app deploy --stop-previous-version
```

**This will fix the API key issue!** 🚀
