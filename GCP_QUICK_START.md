# 🚀 Google Cloud - Quick Start Guide

Deploy your AI Research Agent to Google Cloud in 30 minutes!

---

## ✅ Files Already Created

I've created these files for you:
- ✅ `app.yaml` - GCP configuration with your API keys
- ✅ `.gcloudignore` - Files to exclude from deployment

---

## 🎯 QUICK DEPLOYMENT STEPS

### 1. Create Google Cloud Account (5 minutes)

1. Go to: **https://console.cloud.google.com/**
2. Click **"Get started for free"**
3. Sign in with Google
4. Add credit card (for $300 free credits)
5. Accept terms
6. **Get $300 free credits!**

---

### 2. Create Project (2 minutes)

1. Click project dropdown (top-left)
2. Click **"New Project"**
3. Name: `ai-research-agent`
4. Click **"Create"**
5. Select your new project

---

### 3. Enable APIs (3 minutes)

1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - **App Engine Admin API**
   - **Cloud Build API**

---

### 4. Install gcloud CLI (5 minutes)

**Windows:**
1. Download: https://cloud.google.com/sdk/docs/install
2. Run installer
3. Follow wizard
4. Check "Run gcloud init"

**Verify:**
```bash
gcloud --version
```

---

### 5. Initialize gcloud (3 minutes)

```bash
# Initialize
gcloud init

# Follow prompts:
# - Log in with Google account
# - Select project: ai-research-agent
# - Choose region: us-central1
```

---

### 6. Deploy Application (10 minutes)

```bash
# Navigate to your project folder
cd path\to\your\project

# Create App Engine app
gcloud app create --region=us-central

# Deploy!
gcloud app deploy

# Type: Y (yes)
# Wait 5-10 minutes
```

---

### 7. Open Your App! 🎉

```bash
# Open in browser
gcloud app browse
```

**Your URL:**
```
https://ai-research-agent.uc.r.appspot.com
```

---

## ✅ VERIFICATION

Test these features:
- [ ] Application loads
- [ ] Search for papers works
- [ ] Text extraction works
- [ ] Draft generation works
- [ ] Real-time updates work

---

## 📊 VIEW LOGS

```bash
# Real-time logs
gcloud app logs tail -s default

# Recent logs
gcloud app logs read --limit=50
```

---

## 🔄 UPDATE APPLICATION

When you make changes:

```bash
# Deploy update
gcloud app deploy

# Confirm: Y
# Wait 3-5 minutes
```

---

## 💰 COST

**With $300 Credits:**
- ✅ FREE for 3+ months
- ✅ F1 instance included
- ✅ No charges until credits expire

**After Credits:**
- F1 instance: ~$36/month
- 28 hours/day FREE (Always Free tier)
- Actual cost: ~$0-10/month for low traffic

---

## 🆘 TROUBLESHOOTING

### Deployment Failed?

```bash
# Check logs
gcloud app logs tail -s default

# Common fixes:
# - Verify app.yaml exists
# - Check requirements.txt is complete
# - Ensure application.py exists
```

### Application Won't Start?

```bash
# View errors
gcloud app logs read --limit=50

# Check:
# - API keys in app.yaml
# - gunicorn in requirements.txt
# - eventlet in requirements.txt
```

### Need Help?

1. Check **GCP_DEPLOYMENT_GUIDE.md** (detailed guide)
2. View logs: `gcloud app logs tail`
3. Google Cloud Support: https://console.cloud.google.com/support

---

## 🎯 NEXT STEPS

After successful deployment:

1. **Set up monitoring**:
   - https://console.cloud.google.com/appengine

2. **Set up billing alerts**:
   - https://console.cloud.google.com/billing

3. **Add custom domain** (optional):
   - https://console.cloud.google.com/appengine/settings/domains

4. **Share your app**:
   - Send URL to users
   - Collect feedback
   - Monitor usage

---

## 📞 QUICK LINKS

- **Console**: https://console.cloud.google.com/
- **App Engine**: https://console.cloud.google.com/appengine
- **Logs**: https://console.cloud.google.com/logs
- **Billing**: https://console.cloud.google.com/billing
- **Documentation**: https://cloud.google.com/appengine/docs

---

## 🎉 YOU'RE DONE!

Your AI Research Agent is now live on Google Cloud!

**Advantages over AWS:**
- ✅ Easier deployment (no complex configuration)
- ✅ $300 free credits (vs AWS free tier limits)
- ✅ Better Gemini API integration
- ✅ Automatic HTTPS
- ✅ Simpler management

**Enjoy your deployed application!** 🚀
