# 🚀 Google Cloud Platform Deployment Guide

Complete guide for deploying your AI Research Agent to Google Cloud Platform (GCP).

---

## 📋 Why Google Cloud?

✅ **Better for your app**:
- Native Gemini API integration (same company!)
- $300 free credits for new accounts
- Always Free tier available
- Simpler deployment than AWS
- Better Python support
- Automatic HTTPS

✅ **Cost-effective**:
- $300 free credits (3 months)
- Always Free tier after credits
- Pay-as-you-go pricing
- No surprise charges

---

## 🎯 DEPLOYMENT METHOD

**We'll use Google App Engine** - the easiest option:
- ✅ Fully managed
- ✅ Auto-scaling
- ✅ Free tier available
- ✅ No server management
- ⏱️ Time: 20-30 minutes

---

## 📦 PART 1: PREPARE YOUR APPLICATION

### Step 1: Create app.yaml Configuration File

Create a file named `app.yaml` in your project root with this content:

```yaml
runtime: python311

instance_class: F1

env_variables:
  FLASK_ENV: "production"
  GEMINI_API_KEY: "AIzaSyBaVWtZkWfeFhdgaX6bD_RinoYhd5b2tD0"
  SEMANTIC_SCHOLAR_API_KEY: "Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld"
  SECRET_KEY: "litwise-ai-secret-2024-prod-key-secure"

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 3
  min_pending_latency: 30ms
  max_pending_latency: automatic
  max_concurrent_requests: 50

handlers:
- url: /static
  static_dir: static
  secure: always

- url: /.*
  script: auto
  secure: always

entrypoint: gunicorn --worker-class eventlet -w 1 --bind :$PORT application:application
```

### Step 2: Create .gcloudignore File

Create `.gcloudignore` in your project root:

```
.git
.gitignore
.venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist/
build/
data/
*.log
.env
.vscode/
.idea/
node_modules/
```

### Step 3: Verify Required Files

Ensure you have:
- ✅ `application.py` (entry point)
- ✅ `requirements.txt` (dependencies)
- ✅ `app.yaml` (GCP configuration) - just created
- ✅ `.gcloudignore` (exclude files) - just created
- ✅ `templates/` folder
- ✅ `static/` folder

---

## 🌐 PART 2: GOOGLE CLOUD CONSOLE SETUP

### Step 1: Create Google Cloud Account

1. Go to: **https://console.cloud.google.com/**
2. Click **"Get started for free"**
3. Sign in with your Google account
4. **Enter billing information** (required for $300 credits)
   - Credit card needed but won't be charged
   - $300 free credits for 90 days
5. Accept terms and conditions
6. Click **"Start my free trial"**

**You'll get:**
- ✅ $300 free credits
- ✅ 90 days to use them
- ✅ Always Free tier after credits expire

---

### Step 2: Create a New Project

1. **Click project dropdown** (top-left, next to "Google Cloud")
2. Click **"New Project"**
3. **Project name**: `ai-research-agent`
4. **Organization**: Leave as default
5. **Location**: Leave as default
6. Click **"Create"**
7. Wait 10-20 seconds
8. **Select your new project** from the dropdown

---

### Step 3: Enable Required APIs

1. **Go to APIs & Services**:
   - Click hamburger menu (☰) top-left
   - Click **"APIs & Services"** → **"Library"**

2. **Enable these APIs** (search and enable each):
   
   **App Engine Admin API**:
   - Search: "App Engine Admin API"
   - Click on it
   - Click **"Enable"**
   - Wait for activation

   **Cloud Build API**:
   - Search: "Cloud Build API"
   - Click on it
   - Click **"Enable"**

---

### Step 4: Install Google Cloud SDK (gcloud CLI)

**On Windows:**

1. Download: **https://cloud.google.com/sdk/docs/install**
2. Run the installer: `GoogleCloudSDKInstaller.exe`
3. Follow installation wizard
4. Check: ☑️ "Run 'gcloud init'"
5. Complete installation

**Verify Installation:**
```bash
gcloud --version
```

Should show: `Google Cloud SDK 4xx.x.x`

---

### Step 5: Initialize gcloud CLI

Open Command Prompt or PowerShell:

```bash
# Initialize gcloud
gcloud init

# Follow the prompts:
# 1. Choose: "Log in with a new account"
# 2. Browser opens - sign in with your Google account
# 3. Allow access
# 4. Select your project: ai-research-agent
# 5. Choose region: us-central1 (or closest to you)
```

**Set your project:**
```bash
gcloud config set project ai-research-agent
```

---

## 🚀 PART 3: DEPLOY TO APP ENGINE

### Step 1: Navigate to Your Project

```bash
# Open Command Prompt/PowerShell
cd path\to\your\project

# Example:
cd C:\Users\YourName\Documents\your-project-folder
```

### Step 2: Create App Engine Application

```bash
# Create App Engine app (one-time setup)
gcloud app create --region=us-central

# Choose region closest to you:
# us-central (Iowa)
# us-east1 (South Carolina)
# europe-west (Belgium)
# asia-northeast1 (Tokyo)
```

**Note**: Region cannot be changed after creation!

---

### Step 3: Deploy Your Application

```bash
# Deploy to App Engine
gcloud app deploy

# You'll see:
# - Services to deploy
# - Target project
# - Target service
# - Target url

# Type: Y (yes) to confirm
# Press Enter
```

**Deployment Process:**
```
Uploading files...
Building application...
Installing dependencies...
Starting application...
Deployment complete!
```

**Time**: 5-10 minutes

---

### Step 4: Access Your Application

```bash
# Open your app in browser
gcloud app browse

# Or get the URL manually
gcloud app describe
```

**Your URL will be:**
```
https://ai-research-agent.uc.r.appspot.com
```

**Features:**
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ✅ Auto-scaling
- ✅ Global CDN

---

## 📊 PART 4: MANAGE YOUR APPLICATION

### View Logs

**Via CLI:**
```bash
# Tail logs in real-time
gcloud app logs tail -s default

# Read recent logs
gcloud app logs read --limit=50
```

**In Console:**
1. Go to: https://console.cloud.google.com/logs
2. Select your project
3. Filter: `resource.type="gae_app"`

### View Application

```bash
# Open in browser
gcloud app browse
```

### Check Status

```bash
# View app details
gcloud app describe

# View versions
gcloud app versions list

# View services
gcloud app services list
```

### Monitor Performance

1. Go to: https://console.cloud.google.com/appengine
2. Click **"Dashboard"**
3. View:
   - Requests per second
   - Latency
   - Errors
   - Memory usage
   - CPU usage

---

## 🔄 UPDATE YOUR APPLICATION

When you make code changes:

```bash
# 1. Test locally
python application.py

# 2. Deploy update
gcloud app deploy

# 3. Confirm: Y

# 4. Wait 3-5 minutes

# 5. Verify
gcloud app browse
```

**Deployment versions:**
- Each deployment creates a new version
- Old versions are kept (can rollback)
- Traffic automatically routes to new version

---

## 💰 COST ESTIMATION

### Free Tier (Always Free)

**App Engine F1 Instance:**
- 28 instance hours/day FREE
- ~$0 for single instance
- After free hours: $0.05/hour

**With $300 Credits:**
- Covers 3 months of usage
- F1 instance: ~$36/month after free tier
- Credits last: 8+ months for single instance

### After Free Credits

**F1 Instance (Smallest):**
- Cost: ~$36/month
- 600 MHz CPU, 256 MB RAM
- Good for testing

**F2 Instance (Recommended):**
- Cost: ~$72/month
- 1.2 GHz CPU, 512 MB RAM
- Better performance

**F4 Instance (Production):**
- Cost: ~$144/month
- 2.4 GHz CPU, 1 GB RAM
- Best performance

### Cost Optimization

Edit `app.yaml`:
```yaml
automatic_scaling:
  min_instances: 0  # Scale to zero when idle
  max_instances: 3
```

Redeploy:
```bash
gcloud app deploy
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: Deployment Failed

**Check logs:**
```bash
gcloud app logs tail -s default
```

**Common fixes:**
- Verify `application.py` exists
- Check `requirements.txt` is complete
- Ensure `app.yaml` is correct
- Check Python version (3.11)

### Issue 2: Application Won't Start

**Check:**
```bash
# View recent logs
gcloud app logs read --limit=50
```

**Fix:**
- Verify entrypoint in app.yaml
- Check port binding (use $PORT)
- Verify gunicorn is in requirements.txt
- Ensure eventlet is in requirements.txt

### Issue 3: API Keys Not Working

**Verify in app.yaml:**
- Check GEMINI_API_KEY is set
- Check SEMANTIC_SCHOLAR_API_KEY is set
- No extra spaces or quotes

**Redeploy:**
```bash
gcloud app deploy
```

### Issue 4: Out of Memory

**Upgrade instance:**

Edit `app.yaml`:
```yaml
instance_class: F2  # or F4
```

Redeploy:
```bash
gcloud app deploy
```

---

## 🔒 SECURITY BEST PRACTICES

### 1. HTTPS Only (Already Enabled)

In app.yaml:
```yaml
handlers:
- url: /.*
  secure: always  # Forces HTTPS
```

### 2. Environment Variables

API keys are in app.yaml (secure for App Engine)

### 3. Firewall Rules (Optional)

```bash
# Restrict access by IP
gcloud app firewall-rules create 1000 \
    --source-range="YOUR_IP/32" \
    --action=allow
```

---

## 🎯 CUSTOM DOMAIN (Optional)

### Add Your Domain

1. **Go to App Engine Settings**:
   - https://console.cloud.google.com/appengine/settings/domains

2. **Click "Add a custom domain"**

3. **Verify domain ownership**

4. **Update DNS records**:
   - Add CNAME record
   - Point to: `ghs.googlehosted.com`

5. **Wait for SSL certificate** (automatic, 15 minutes)

**Your app will be at:**
```
https://yourdomain.com
```

---

## 📱 MONITORING & ALERTS

### Set Up Alerts

1. Go to: https://console.cloud.google.com/monitoring
2. Click **"Alerting"** → **"Create Policy"**
3. Add conditions:
   - High error rate
   - High latency
   - High memory usage
4. Add notification channels (email)
5. Save policy

---

## 🛑 STOP/DELETE APPLICATION

### Stop Serving Traffic

```bash
# Stop specific version
gcloud app versions stop VERSION_ID

# List versions first
gcloud app versions list
```

### Delete Application

**Warning**: Cannot undo!

1. Go to: https://console.cloud.google.com/appengine/settings
2. Click **"Disable application"**
3. Type application ID to confirm
4. Click **"Disable"**

---

## ✅ DEPLOYMENT CHECKLIST

### Before Deployment:
- [ ] Google Cloud account created
- [ ] $300 credits activated
- [ ] Project created: ai-research-agent
- [ ] APIs enabled (App Engine, Cloud Build)
- [ ] gcloud CLI installed
- [ ] gcloud initialized
- [ ] app.yaml created with API keys
- [ ] .gcloudignore created

### During Deployment:
- [ ] Navigated to project folder
- [ ] App Engine app created (gcloud app create)
- [ ] Application deployed (gcloud app deploy)
- [ ] Deployment successful

### After Deployment:
- [ ] Application accessible via URL
- [ ] All features tested
- [ ] Logs checked (no errors)
- [ ] Monitoring dashboard viewed
- [ ] Billing alerts set (optional)

---

## 🎉 SUCCESS!

Your application is now live on Google Cloud Platform!

**Your URL:**
```
https://ai-research-agent.uc.r.appspot.com
```

**Features:**
- ✅ Automatic HTTPS
- ✅ Auto-scaling
- ✅ Global CDN
- ✅ 99.95% uptime SLA
- ✅ Integrated with Gemini API
- ✅ $300 free credits

**Next Steps:**
1. Test all features
2. Monitor performance
3. Set up alerts
4. Share with users
5. Enjoy your deployed app!

---

## 📞 SUPPORT

- **Documentation**: https://cloud.google.com/appengine/docs
- **Community**: https://stackoverflow.com/questions/tagged/google-app-engine
- **Support**: https://console.cloud.google.com/support
- **Pricing**: https://cloud.google.com/appengine/pricing

---

**Ready to deploy? Start with PART 1: PREPARE YOUR APPLICATION!** 🚀
