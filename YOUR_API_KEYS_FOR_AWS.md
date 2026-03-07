# 🔑 Your API Keys for AWS Deployment

## ✅ API Keys Ready to Use

You already have all the required API keys! Here's what to enter in AWS Console:

---

## 📋 COPY THESE VALUES TO AWS CONSOLE

When you reach **Step 9: Configure Environment Variables** in the deployment guide, enter these exact values:

### Environment Properties to Add:

#### 1. GEMINI_API_KEY
```
Name:  GEMINI_API_KEY
Value: AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0
```

#### 2. SEMANTIC_SCHOLAR_API_KEY
```
Name:  SEMANTIC_SCHOLAR_API_KEY
Value: Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld
```

#### 3. FLASK_ENV
```
Name:  FLASK_ENV
Value: production
```

#### 4. SECRET_KEY
```
Name:  SECRET_KEY
Value: litwise-ai-secret-2024-prod-key-secure
```

---

## 🎯 HOW TO ADD THESE IN AWS CONSOLE

### Step-by-Step:

1. **Navigate to Configuration**:
   - Go to your Elastic Beanstalk environment
   - Click "Configuration" in the left sidebar

2. **Edit Software Settings**:
   - Find "Software" category
   - Click "Edit" button

3. **Scroll to Environment Properties**:
   - Scroll down to "Environment properties" section
   - You'll see a table with Name/Value columns

4. **Add Each Property**:

   **First Property:**
   - Click in the "Name" field
   - Type: `GEMINI_API_KEY`
   - Click in the "Value" field
   - Paste: `AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0`

   **Second Property:**
   - Click "Add environment property" button
   - Name: `SEMANTIC_SCHOLAR_API_KEY`
   - Value: `Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld`

   **Third Property:**
   - Click "Add environment property" button
   - Name: `FLASK_ENV`
   - Value: `production`

   **Fourth Property:**
   - Click "Add environment property" button
   - Name: `SECRET_KEY`
   - Value: `litwise-ai-secret-2024-prod-key-secure`

5. **Save Changes**:
   - Scroll to bottom
   - Click "Apply" button
   - Wait 2-3 minutes for restart

---

## 📸 VISUAL REFERENCE

Your environment properties table should look like this:

```
┌──────────────────────────────┬────────────────────────────────────────────┐
│ Name                         │ Value                                      │
├──────────────────────────────┼────────────────────────────────────────────┤
│ GEMINI_API_KEY              │ AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0   │
├──────────────────────────────┼────────────────────────────────────────────┤
│ SEMANTIC_SCHOLAR_API_KEY    │ Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld │
├──────────────────────────────┼────────────────────────────────────────────┤
│ FLASK_ENV                   │ production                                 │
├──────────────────────────────┼────────────────────────────────────────────┤
│ SECRET_KEY                  │ litwise-ai-secret-2024-prod-key-secure     │
└──────────────────────────────┴────────────────────────────────────────────┘
```

---

## ✅ VERIFICATION

After adding the keys and restarting:

1. **Check Logs**:
   - Go to Logs → Request Logs → Last 100 Lines
   - Look for successful API initialization
   - Should NOT see "API key not found" errors

2. **Test Features**:
   - Try searching for papers (uses Semantic Scholar API)
   - Try generating drafts (uses Gemini API)
   - Both should work without errors

---

## 🔒 SECURITY NOTES

### ✅ Good Practices:
- ✅ Keys are stored as environment variables (secure)
- ✅ Keys are NOT in your code (good!)
- ✅ Keys are NOT committed to Git (verified in .gitignore)

### ⚠️ Important:
- **Never share these keys publicly**
- **Never commit .env file to Git**
- **Rotate keys if exposed**
- **Use different keys for dev/prod** (optional but recommended)

---

## 🔄 IF YOU NEED NEW KEYS

### Gemini API Key (Google AI Studio)

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Select project or create new one
5. Copy the key (starts with `AIza...`)
6. Replace in AWS environment variables

**Current Key Status**: ✅ Active and working

### Semantic Scholar API Key

1. Go to: https://www.semanticscholar.org/product/api
2. Click "Get API Key"
3. Sign up or sign in
4. Request API key
5. Copy the key from email or dashboard
6. Replace in AWS environment variables

**Current Key Status**: ✅ Active and working

### SECRET_KEY

This is just a random string for Flask session security.

**Generate new one**:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use any random string like:
- `my-super-secret-key-2024`
- `litwise-production-secret-xyz`

**Current Key**: ✅ Set and ready

---

## 📝 QUICK COPY-PASTE FORMAT

For easy copying, here are all values in one place:

```
GEMINI_API_KEY=AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0
SEMANTIC_SCHOLAR_API_KEY=Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld
FLASK_ENV=production
SECRET_KEY=litwise-ai-secret-2024-prod-key-secure
```

---

## 🎯 READY TO DEPLOY!

You have everything you need:
- ✅ Gemini API Key
- ✅ Semantic Scholar API Key
- ✅ Flask Environment
- ✅ Secret Key

**Next Step**: Continue with AWS deployment guide at Step 9!

---

## 🆘 TROUBLESHOOTING

### If Gemini API doesn't work:
1. Verify key is correct (no extra spaces)
2. Check API quota at: https://makersuite.google.com/app/apikey
3. Ensure billing is enabled (if required)
4. Try regenerating the key

### If Semantic Scholar API doesn't work:
1. Verify key is correct
2. Check rate limits (1 request per second with key)
3. Ensure key is activated
4. Contact Semantic Scholar support if needed

### If Application won't start:
1. Check all 4 environment variables are set
2. Verify no typos in variable names
3. Check logs for specific errors
4. Ensure values have no quotes or extra characters

---

**You're all set! Use these keys in your AWS deployment.** 🚀
