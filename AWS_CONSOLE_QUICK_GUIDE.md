# 🚀 AWS Console Deployment - Quick Visual Guide

This is a simplified, step-by-step visual guide for deploying via AWS Console.

## 📦 BEFORE YOU START

### 1. Prepare Your ZIP File

Create a ZIP file containing:
```
ai-research-agent.zip
├── application.py
├── web_app.py
├── requirements.txt
├── config.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   └── js/
├── .ebextensions/
│   └── (config files)
└── (all other .py files)
```

**DO NOT include**: .venv/, .git/, data/, __pycache__/

---

## 🌐 DEPLOYMENT STEPS

### Step 1: Sign in to AWS
1. Go to: https://console.aws.amazon.com/
2. Sign in with your credentials
3. Select region: **US East (N. Virginia)** (top-right corner)

---

### Step 2: Open Elastic Beanstalk
1. Search bar → Type "Elastic Beanstalk"
2. Click on the service

---

### Step 3: Create Application
1. Click **"Create Application"** (orange button)

2. Fill in:
   - **Application name**: `ai-research-agent`
   - **Environment name**: `ai-research-prod`
   - **Domain**: Leave auto or customize
   
3. Platform:
   - **Platform**: Python
   - **Branch**: Python 3.11 on Amazon Linux 2023
   - **Version**: Recommended (latest)

4. Application code:
   - Select **"Upload your code"**
   - **Version label**: `v1.0`
   - Click **"Choose file"** → Select your ZIP
   - Wait for upload

5. Presets:
   - Select **"Single instance (free tier eligible)"**

6. Click **"Next"**

---

### Step 4: Service Access
1. **Service role**: Create and use new service role
2. **EC2 key pair**: (optional) Create new or skip
3. **EC2 instance profile**: Create and use new
4. Click **"Next"**

---

### Step 5: Networking
1. **VPC**: Default VPC
2. **Public IP**: ✅ Activated
3. **Instance subnets**: Check at least one
4. **Database**: Skip (uncheck)
5. Click **"Next"**

---

### Step 6: Instance Configuration
1. **Root volume**: General Purpose (SSD)
2. **Size**: 10 GB
3. **Instance type**: `t2.micro` (free tier) or `t2.small`
4. Click **"Next"**

---

### Step 7: Monitoring
1. **Health reporting**: Enhanced ✅
2. **Managed updates**: Enable ✅
3. **CloudWatch logs**: Enable ✅
4. Click **"Next"**

---

### Step 8: Review and Submit
1. Review all settings
2. Click **"Submit"**
3. ⏳ **Wait 10-15 minutes** for environment creation
4. Status will show "Ok" with green checkmark when ready

---

### Step 9: Add API Keys (CRITICAL!)
1. Click on your environment name
2. Left sidebar → **"Configuration"**
3. Find **"Software"** → Click **"Edit"**
4. Scroll to **"Environment properties"**
5. Add these properties:

   ```
   GEMINI_API_KEY = your_actual_gemini_api_key
   SEMANTIC_SCHOLAR_API_KEY = your_semantic_scholar_key
   FLASK_ENV = production
   SECRET_KEY = generate_random_string_here
   ```

6. Click **"Apply"** at bottom
7. ⏳ Wait 2-3 minutes for restart

---

### Step 10: Access Your App! 🎉
1. In environment overview, find the **URL**
2. Format: `http://ai-research-prod.us-east-1.elasticbeanstalk.com`
3. Click the URL or copy to browser
4. Your app should load!

---

## 🔍 QUICK CHECKS

### ✅ Is it working?
- Environment status: **Green "Ok"**
- URL opens in browser
- Can search for papers
- Real-time updates work

### ❌ Not working?
1. **Check logs**:
   - Left sidebar → "Logs"
   - "Request Logs" → "Last 100 Lines"
   - Download and check for errors

2. **Verify API keys**:
   - Configuration → Software
   - Check environment properties are set

3. **Check health**:
   - Environment overview
   - Should be green, not red/yellow

---

## 📊 MONITORING YOUR APP

### View Logs
```
Environment → Logs → Request Logs → Last 100 Lines
```

### Check Health
```
Environment → Monitoring → View graphs
```

### View Costs
```
AWS Console → Billing Dashboard → Cost Explorer
```

---

## 🔄 UPDATE YOUR APP

When you make code changes:

1. **Create new ZIP** with updated code
2. Go to **"Application versions"** (left sidebar)
3. Click **"Upload"**
4. Choose new ZIP, label it `v1.1`
5. Click **"Upload"**
6. Go back to environment
7. Click **"Upload and deploy"**
8. Select new version
9. Click **"Deploy"**
10. ⏳ Wait 3-5 minutes

---

## 💰 COST TRACKING

### Free Tier (First 12 months)
- ✅ 750 hours/month t2.micro = **FREE**
- ✅ Single instance = **FREE**
- ✅ Basic monitoring = **FREE**

### After Free Tier
- t2.micro: ~$8-10/month
- t2.small: ~$17/month (recommended)

### Stop to Save Money
```
Environment → Actions → Terminate Environment
```
(You can recreate later)

---

## 🆘 COMMON ISSUES

### Issue: 502 Bad Gateway
**Fix**: Check logs, verify application.py exists, check API keys

### Issue: Environment Degraded
**Fix**: View logs, check requirements.txt, verify all dependencies

### Issue: Out of Memory
**Fix**: Upgrade to t2.small
```
Configuration → Instances → Edit → Change type
```

### Issue: WebSocket Not Working
**Fix**: Ensure .ebextensions/03_websocket.config exists in ZIP

---

## 🎯 QUICK TIPS

1. **Always check logs first** when troubleshooting
2. **Set up billing alerts** to avoid surprise charges
3. **Use t2.micro** for testing, **t2.small** for production
4. **Enable CloudWatch logs** for better debugging
5. **Keep your ZIP file under 512MB**

---

## 📞 NEED HELP?

### AWS Support
- Console: https://console.aws.amazon.com/support/
- Documentation: https://docs.aws.amazon.com/elasticbeanstalk/

### Check These First
1. ✅ Is environment status "Ok" (green)?
2. ✅ Are API keys set in environment properties?
3. ✅ Does the ZIP file include all necessary files?
4. ✅ Is requirements.txt complete?
5. ✅ Are you in the correct AWS region?

---

## ✅ SUCCESS CHECKLIST

After deployment:
- [ ] Environment status is green "Ok"
- [ ] URL opens and shows your app
- [ ] Can search for papers
- [ ] Can extract text from PDFs
- [ ] Can generate drafts
- [ ] Real-time updates work
- [ ] No errors in logs
- [ ] Billing alerts are set up

---

## 🎉 YOU'RE DONE!

Your AI Research Agent is now live on AWS!

**Your URL**: `http://ai-research-prod.[region].elasticbeanstalk.com`

**Next Steps**:
1. Share the URL with users
2. Monitor performance and costs
3. Set up custom domain (optional)
4. Enable HTTPS (recommended)

---

**Questions?** Refer to the detailed AWS_DEPLOYMENT_GUIDE.md
